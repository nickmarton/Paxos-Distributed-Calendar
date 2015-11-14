"""Bully Algorithm."""

import time
import pickle
import thread
import socket

def send_election_messages(node):
    """Send election messages to all Node's with higher IDs than this one."""
    #send election message to all higher ID processes
    for ID, ip_info in node._ip_table.items():
        IP, PORT = ip_info
        if ID > node._node_id:
            thread.start_new_thread(
                send_message, (node._node_id, IP, PORT, "Election"))
            time.sleep(0.5)

def send_okay_message(node, IP, PORT):
    """Send OKAY message to the Node object with IP, PORT."""
    thread.start_new_thread(
        send_message, (node._node_id, IP, PORT, "OKAY"))

def send_coordinator_messages(node):
    """Send Coordinator nmessage to all Node's except this one."""
    for ID, ip_info in node._ip_table.items():
        IP, PORT = ip_info

        #Don't send to self
        if ID != node._node_id:
            thread.start_new_thread(
                send_message, (node._node_id, IP, PORT, "Coordinator"))

def send_message(ID, IP, PORT, msg):
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
        print "yo"

def leader_election(node):
    """Perform Bully Algorithm to elect a leader among the Nodes."""
    ip_table = node._ip_table
    HOST, PORT = ip_table[node._node_id]

    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_socket.bind((HOST, PORT))
    recv_socket.setblocking(0)
    #backlog; 1 for each Node besides self
    recv_socket.listen(4)

    #Wait for messages
    start_time = time.time()
    end_time = time.time()
    received_okay = False
    while True:
        #Send initial election messages
        send_election_messages(node)


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
                send_okay_message(node, IP, PORT)
                send_election_messages(node)


        #If message is OKAY, wait for a while then do leader election again
        if message == "OKAY":
            received_okay = True
            continue


        #if it's been a certain amount of time and no OKAY's received,
        #we're the leader, send Coordinator to everyone
        end_time = time.time()
        if end_time - start_time > 30 and not received_okay:
            send_coordinator_messages(node)
            node._leader = node._node_id
            break


    recv_socket.close()
