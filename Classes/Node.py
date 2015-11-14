"""Node (User) Class for Paxos Calendar."""

import os
import sys
import time
import thread
import pickle
import socket
from Appointment import Appointment
from Calendar import Calendar
from Proposer import Proposer
from Acceptor import Acceptor
from Bully import leader_election

class Node(object):
    """
    Node class.

    node_id:        Unique ID used for Node identification as well as for
                    unique proposal number generation; int.
    calendar:       Calendar object which contains Appointment objects.
    proposer:       Proposer object used in Synod Algorithm; passed node_id so
                    it can create unique proposal numbers.
    acceptor:       Acceptor object used in Synod Algorithm.
    log:            List of Calendar objects used in full Paxos Algorithm;
                    intially empty, Synod Algorithm is used to fill each entry
                    of log
    """

    _ip_filename = "./IP_translations.txt"

    def __init__(self, node_id):
        """Construct a Node object."""
        if type(node_id) != int:
            raise TypeError("node_id must be an int")
        if node_id < 0:
            raise ValueError("node id must be a nonnegative integer")

        try:
            Node._ip_table = Node._make_ip_table()
        except IOError:
            raise IOError("Node-to-IP translation file: " + ip_filename + " not found.")

        self._node_id = node_id
        self._calendar = Calendar()
        self._proposer = Proposer(node_id)
        self._acceptor = Acceptor()
        self._log = {}
        self._leader = None
        self._is_Node = True

    def insert(self, appointment):
        """Insert an Appointment into this Node's Calendar."""
        print "IN INSERT"

    def delete(self, appointment):
        """Delete an Appointment in this Node's Calendar."""
        print "IN DELETE"

    @staticmethod
    def _make_ip_table():
        """Create the ID-to-IP translation table used for socket connection."""
        table = {}

        import re
        pattern = r"^\d+,\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3},\d{4}$"
        with open(Node._ip_filename, "r") as f:
                for translation in f:
                    match = re.match(pattern, translation.strip())
                    if not match:
                        raise ValueError(
                            "Every line in IP_translations.txt must be of "
                            "form ID,IP")
                    ID, IP, PORT = translation.strip().split(',')
                    table[int(ID)] = [IP, int(PORT)]

        return table

    @staticmethod
    def save(Node, path="./", filename="state.pkl"):
        """Save this Node's log and Acceptor to stable storage."""
        if not hasattr(Node, "_is_Node"):
            raise TypeError("Node parameter must be a Node object")

        if type(filename) != str or type(path) != str:
            raise TypeError("path and filename must be strings")

        if filename[-4:] != ".pkl":
            raise ValueError("filename must have .pkl extension")

        if not os.path.exists(path):
            raise ValueError("path provided does not exist")

        import pickle
        with open(path + filename, 'w') as f:
            state = (Node._node_id, Node._log, Node._acceptor)
            pickle.dump(state, f)

    @staticmethod
    def load(path="./", filename="state.pkl"):
        """
        Load log and Acceptor from stable storage if path and filename exist.
        """

        def _rebuild_calendar(node, log):
            """Rebuild the calendar of node by reconstructing it from log."""
            #Get the latest entry in the log for most up-to-date Calendar
            node._calendar = log[max(log.keys())]

        if type(filename) != str or type(path) != str:
            raise TypeError("path and filename must be strings")

        if filename[-4:] != ".pkl":
            raise ValueError("filename must have .pkl extension")

        if not os.path.exists(path+filename):
            raise ValueError("path provided does not exist")

        with open(path + filename, 'r') as f:
            state = pickle.load(f)
            node_id, log, acceptor = state
            node = Node(node_id)
            node._log = log
            node._acceptor = acceptor
            _rebuild_calendar(node, log)

            return node

    @staticmethod
    def _parse_command(command, node):
        """Parse command provided, possibly involving provided node."""
        
        def _do_show(argv, node):
            """Perform show command for debugging/user information."""
            if len(argv) == 1:
                raise ValueError(
                    "Invalid show argument; show needs argument "
                    "{calendar,log,acceptor,proposer,all}")

            #Handle showing the calendar
            if argv[1] == "calendar":
                print node._calendar
            
            #Handle showing the log
            elif argv[1] == "log":

                print "Log:"
                #copy the log into a list ordered by slot number
                ordered_slots = sorted(node._log.items(), key=lambda x: x[0])
                
                #if -short flag not thrown, print entire log
                if len(argv) == 2:
                    for slot in ordered_slots:
                        print "Slot " + str(slot[0]) + ' ' + str(slot[1])
                #Short flag is thrown, just print names of Appointments in each
                #Calendar slot
                elif len(argv) == 3:
                    if argv[2] == "-s":
                        for slot in ordered_slots:
                            log_string = "Slot " + str(slot[0]) + " Calendar: \t"
                            log_string += ', '.join(
                                slot[1].get_appointment_names())
                            print log_string
                        print
                    else:
                        raise ValueError(
                            "Invalid show arguments; Only flags \"-s\" "
                            "permitted")
                #Bad number of arguments to show log
                else:
                    raise ValueError(
                        "Invalid show arguments; show log supports only a "
                        "single optional flag argument \"-s\"")
            #Handle showing Node's Acceptor object
            elif argv[1] == "acceptor":
                print str(node._acceptor) + '\n'
            #Handle showing Node's Proposer object
            elif argv[1] == "proposer":
                print str(node._proposer) + '\n'
            #Handle printing entire state of Node
            elif argv[1] == "all":
                print "-" * 100
                print "Node ID: " + str(node._node_id)
                _do_show(['show', 'calendar'], node)
                _do_show(['show', 'log', '-s'], node)
                _do_show(['show', 'acceptor'], node)
                _do_show(['show', 'proposer'], node)
                print "-" * 100
            else:
                raise ValueError(
                    "Invalid show argument; show needs argument "
                    "{calendar,log,acceptor,proposer,all}")

        def _parse_appointment(argv):
            """Try to parse an Appointment object from given argv."""
            generic_error_msg = "Invalid command; Schedule and cancel " + \
                    "commands must be of form: \n" + \
                    "{schedule,cancel} [Appointment name] " + \
                    "(user1,user2,...usern) (start_time,end_time) [day]"

            if len(argv) != 5:
                raise ValueError(generic_error_msg)
            
            name, participants, times, day = argv[1:]
            participants = participants[1:-1].split(",")
            try:
                participants = [int(user[4:]) for user in participants]
            except ValueError:
                raise ValueError(
                    "Invalid command; participants must be of form "
                    "(user1,user2,...,usern)")
            try:
                start, end = times[1:-1].split(',')
            except ValueError:
                raise ValueError(
                    "Invalid command; times must be of form "
                    "(start_time,end_time)")

            try:
                return Appointment(name, day, start, end, participants)
            except ValueError as excinfo:
                raise ValueError("Invalid command; " + excinfo.message)

        def _do_clear():
            """Perform clear command via ASCI escape code."""
            print(chr(27) + "[2J")

        argv = command.split()

        if not argv:
            return

        if argv[0] == "clear":
            _do_clear()

        #If command was to show something, do show
        if argv[0] == "show":
            try:
                _do_show(argv, node)
            except ValueError as excinfo:
                print excinfo
                print

        #If command is to schedule or cancel an Appointment, parse then
        #initiate Synod algorithm
        if argv[0] == "schedule":
            try:
                appointment = _parse_appointment(argv)

                #determine if the Appointment the user is trying to schedule
                #is already in their Calendar or in conflict with some
                #Appointment in their Calendar
                conflict_cond = node._calendar._is_appointment_conflicting(
                                                                appointment)
                in_cond = appointment in node._calendar

                #if it's not already in the Calendar and not in conflict with
                #any Appointment in it, begin Synod
                if not conflict_cond and not in_cond:
                    node.insert(appointment)
                else:
                    print "User scheduled appointment already in their " + \
                            "own Calendar or in conflict with their own " + \
                            "Calendar; ignoring.\n"
            except ValueError as excinfo:
                print excinfo
                print

        if argv[0] == "cancel":
            try:
                appointment = _parse_appointment(argv)
                if appointment in node._calendar:
                    node.delete(appointment)
                else:
                    print "User cancelled appointment not in their own " + \
                                                        "Calendar; ignoring.\n"
            except ValueError as excinfo:
                print excinfo
                print

    @staticmethod
    def serve(conn, node):
        """Have node provided serve some client connected through conn."""
        while 1:
            data = conn.recv(8192)

            if not data:
                print("Ended connection")
                break

            if data.decode("utf-8") == "terminate" or data.decode("utf-8") == "quit":
                print("Ending connection with client")
                conn.close()
                break

            print data
            conn.send(b'ACK ' + data)

        conn.close()

def main():
    """Quick tests."""
    "schedule yaboi (user0,user1,user2,user3) (4:00pm,6:00pm) Friday"
    "cancel yaboi (user0,user1,user2,user3) (4:00pm,6:00pm) Friday"
    "schedule xxboi (user1,user4,user5) (1:30am,11:30am) Wednesday"
    "cancel xxboi (user1,user4,user5) (1:30am,11:30am) Wednesday"
    "schedule zo (user1,user2,user3) (12:30pm,1:30pm) Friday"

    N = Node(int(sys.argv[1]))

    a1 = Appointment("zo","Friday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("xxboi","Wednesday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("lol","saturday","11:30am","12:30pm", [1])
    a4 = Appointment("yeee","MondAy","11:30am","12:30pm", [1])

    c1 = Calendar(a1)
    c2 = Calendar(a1, a2)
    c3 = Calendar(a1, a2, a3)
    c3 = Calendar(a1, a2, a3)
    c4 = Calendar(a1, a2, a3, a4)
    
    N._log[0] = c1
    N._log[1] = c2
    N._log[2] = c3
    N._log[3] = c4

    #try to load a previous state of this Node
    try:
        N = Node.load()
    except ValueError:
        pass
    except IOError:
        pass

    ip_table = N._ip_table
    HOST, PORT = ip_table[N._node_id]

    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_socket.bind(("0.0.0.0", PORT))
    #backlog; 1 for each Node besides self
    recv_socket.listen(4)

    while True:
        thread.start_new_thread(leader_election, (N, recv_socket))
        time.sleep(12)
        print "NEW LEADER IS: " + str(N._leader)

    recv_socket.close()

    '''
    HOST = "192.168.1.214"
    PORT = 9000
    #HOST = "0.0.0.0"
    #PORT = int(sys.argv[2])
    
    #bind to host of 0.0.0.0 for any TCP traffic through AWS
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    #backlog to; 1 for each process
    sock.listen(4)
    
    import select
    print("@> Node Started")
    while True:
        r, w, x = select.select([sys.stdin, sock], [], [])
        if not r:
            continue
        #If user entered something in stdin, serve them
        if r[0] is sys.stdin:
            message = raw_input('')
            if message == "quit":
                Node.save(N)
                break
            else:
                Node._parse_command(message, N)
        #if incoming IP connection, serve that client
        else:
            conn, addr = sock.accept()
            print ('Connected with ' + addr[0] + ':' + str(addr[1]))
            thread.start_new_thread(Node.serve, (conn, N))
    sock.close()
    '''
if __name__ == "__main__":
    main()