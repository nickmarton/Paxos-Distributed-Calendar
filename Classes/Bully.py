"""Bully Algorithm."""

import time
import pickle
import thread
import socket
import select

def _send_election_messages(node):
    """Send election messages to all Node's with higher IDs than this one."""
    #send election message to all higher ID processes
    time.sleep(1)
    for ID, ip_info in node._ip_table.items():
        IP, PORT = ip_info
        if ID > node._node_id:
            thread.start_new_thread(
                _send_message, (node._node_id, IP, PORT, "Election"))

def _send_okay_message(node, ID):
    """Send OKAY message to the Node object with IP, PORT."""
    IP, PORT = node._ip_table[ID]
    thread.start_new_thread(
        _send_message, (node._node_id, IP, PORT, "OKAY"))

def _send_coordinator_messages(node):
    """Send Coordinator nmessage to all Node's except this one."""
    for ID, ip_info in node._ip_table.items():
        IP, PORT = ip_info

        #Don't send to self
        if ID != node._node_id:
            thread.start_new_thread(
                _send_message, (node._node_id, IP, PORT, "Coordinator"))

def _send_message(ID, IP, PORT, msg):
    """Send "Election" message to Node at given IP and PORT."""
    try:
        #Open socket for sending
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect((IP, PORT))

        #pickle election message to transmit ID for convenience too
        election_message = pickle.dumps((ID, msg))

        #send election message
        send_socket.send(election_message)
        send_socket.close()
    except socket.error:
        pass

def leader_election(node, recv_socket, timeout):
    """Perform Bully Algorithm to elect a leader among the Nodes."""
    #Send initial election messages
    thread.start_new_thread(_send_election_messages, (node,))
    
    received_okay = False
    #Wait for messages
    while True:

        #poll on recv_socket waiting for message or timeout
        r, w, x = select.select([recv_socket], [], [], timeout)

        #if a message was received, interpret it
        if r:
            #Accept any incoming connections and receive their messages,
            #unpickling the ID-message 2-tuple
            conn, addr = recv_socket.accept()
            data = conn.recv(1024)
            ID, message = pickle.loads(data)

            #If message is Coordinator, we're done
            if message == "Coordinator":
                node._leader = ID
                break

            #Respond to election if message received from higher ID
            if message == "Election":
                if ID < node._node_id:
                    _send_okay_message(node, ID)
                    thread.start_new_thread(_send_election_messages, (node,))
                    continue

            #If message is OKAY, wait for a while then do leader election again
            if message == "OKAY":
                received_okay = True
                continue
        #timeout, this Node is either the new leader or has received an OKAY 
        #from another Node
        else:
            #If this Node hasn't received an OKAY, it is the new leader, send
            #Coordinator message to everyone else
            if not received_okay:
                _send_coordinator_messages(node)
                node._leader = node._node_id
                break
