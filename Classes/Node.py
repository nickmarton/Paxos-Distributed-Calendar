"""Node (User) Class for Paxos Calendar."""

import os
import sys
import time
import thread
import pickle
import socket
import logging
from Bully import bully_algorithm
from Appointment import Appointment
from Calendar import Calendar
from Proposer import Proposer
from Acceptor import Acceptor

class Node(object):
    """
    Node class.

    node_id:        Unique ID used for Node identification as well as for
                    unique proposal number generation; int.
    calendar:       Calendar object which contains Appointment objects.
    proposer:       Proposer object used in Synod Algorithm; passed node_id so
                    it can create unique proposal numbers.
    acceptor:       Acceptor object used in Synod Algorithm.
    log:            Dictionary of Calendar objects used in Paxos Algorithm;
                    intially empty, Synod Algorithm is used to fill each entry
                    of log where integer keys represents slots and the values
                    being the Calendar agreed upon via conscensus.
    leader:         The current leader elected via the bully algorithm;
                    initially None and updated every ~6 seconds.
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
        self._proposer = Proposer(node_id,self._ip_table)
        self._acceptor = Acceptor(self._ip_table)
        self._log = {}
        self._leader = None
        self._is_Node = True

    def insert(self, appointment):
        """Insert an Appointment into this Node's Calendar."""
        #First create new Calendar with new appointment
        from copy import deepcopy
        new_calendar = deepcopy(self._calendar)
        new_calendar += appointment

        next_log_slot = max(self._log.keys()) + 1

        #Then ask leader to propose the new Calendar
        try:
            leader_IP, leader_TCP, leader_UDP = self._ip_table[self._leader]
            proposal_message = pickle.dumps(
                ("propose", new_calendar, next_log_slot))
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.sendto(proposal_message, (leader_IP, leader_UDP))
            udp_socket.close()
        except KeyError as excinfo:
            print "Unable to find leader, waiting until one is selected..."
            while self._leader == None:
                pass
            print "Found leader, continuing...\n"
            self.insert(appointment)

    def delete(self, appointment):
        """Delete an Appointment in this Node's Calendar."""
        #First create new Calendar without appointment
        from copy import deepcopy
        new_calendar = Calendar()
        for self_appointment in self._calendar:
            if self_appointment != appointment:
                new_calendar += deepcopy(self_appointment)

        next_log_slot = max(self._log.key()) + 1

        #Then ask leader to propose the new Calendar
        try:
            leader_IP, leader_TCP, leader_UDP = self._ip_table[self._leader]
            proposal_message = pickle.dumps(
                ("propose", new_calendar, next_log_slot))
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.sendto(proposal_message, (leader_IP, leader_UDP))
            udp_socket.close()
        except KeyError as excinfo:
            print "Unable to find leader, waiting until one is selected..."
            while self._leader == None:
                pass
            print "Found leader, continuing...\n"
            self.delete(appointment)

    def paxos(self):
        """Engage this Node in Paxos algorithm."""
        def _parse_message(message):
            """
            Parse UDP pickled tuple message.
            Self is available from closure.
            """

            valid_message_types = [
                "propose", "prepare", "promise", "accept", "ack", "commit"]

            message_type, message_args = message[0], message[1:]

            #syntactic checking
            if message_type not in valid_message_types:
                logging.error("Invalid message type")
                return

            if 3 <= len(message_args) <= 4:
                arg_0_is_int = type(message_args[0]) == int
                arg_0_is_calendar = hasattr(message_args[0], "_is_Calendar")
                arg_1_is_calendar = hasattr(message_args[1], "_is_Calendar")
                if not arg_0_is_calendar:
                    arg_0_is_None = message_args[0] == None
                else:
                    arg_0_is_None = False
                if not arg_1_is_calendar:
                    arg_1_is_None = message_args[1] == None
                else:
                    arg_1_is_None = False

                #handle prepare messages
                if message_type == "propose":
                    if arg_0_is_calendar:
                        #If in this conditional, we are the leader.
                        #First we have to fill any empty log slots
                        '''
                        slot_ids = self._log.keys()
                        for i in range(max(slot_ids)):
                            if i not in slot_ids:
                                #TODO: do adjustments for message_args length conditional above, adjust indexes used for messages
                                dummy_message = ("propose", Calendar(), self._node_id, i)
                                self._proposer._command_queue.append(dummy_message)
                        '''
                        #Then we can add this new proposal
                        self._proposer._command_queue.append(message)
                    else:
                        logging.error(
                            "Propose message must be of form "
                            "'propose' Calendar")

                #handle prepare messages
                elif message_type == "prepare":
                    if arg_0_is_int:
                        self._acceptor._command_queue.append(message)
                    else:
                        logging.error(
                            "Prepare message must be of form 'prepare' int")
                
                #handle promise messages
                elif message_type == "promise":
                    if (arg_0_is_int and arg_1_is_calendar) or (arg_0_is_None and arg_1_is_None):
                        self._proposer._command_queue.append(message)
                    else:
                        logging.error(
                            "Promise message must be of form "
                            "'promise' int Calendar")

                #handle accept messages
                elif message_type == "accept":
                    if arg_0_is_int and arg_1_is_calendar:
                        self._acceptor._command_queue.append(message)
                    else:
                        logging.error(
                            "Accept message must be of form "
                            "'accept' int Calendar")

                #handle ack messages
                elif message_type == "ack":
                    if arg_0_is_int and arg_1_is_calendar:
                        self._proposer._command_queue.append(message)
                    else:
                        logging.error(
                            "Ack message must be of form "
                            "'ack' int Calendar")

                #handle commit messages
                elif message_type == "commit":
                    if arg_0_is_calendar:
                        self._acceptor._command_queue.append(message)
                    else:
                        logging.error(
                            "Commit message must be of form 'commit' Calendar")

            else:
                logging.error("Invalid message parameters")
                return

        def _do_paxos(self):
            """Do Paxos algorithm for this Node."""
            #Begin running the Acceptor and Proposer in the background
            thread.start_new_thread(self._acceptor.start, ())
            thread.start_new_thread(self._proposer.start, ())

            IP, UDP_PORT = '0.0.0.0', self._ip_table[self._node_id][2]
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            sock.bind((IP, UDP_PORT))
            while True:
                data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
                #Quick lookup of ID of sender from IP received
                sender_ID = filter(
                    lambda row: row[1][0] == addr[0],
                    self._ip_table.items())[0][0]
                
                message = pickle.loads(data)
                #bind sender_ID to message
                message = message + (sender_ID,)
                _parse_message(message)

                time.sleep(.01)

        thread.start_new_thread(_do_paxos, (self,))

    def elect_leader(self, poll_time=6, timeout=3):
        """Engage this Node in leader selection."""
        def _do_leader_election(self, poll_time, timeout):
            """Do leader election as new thread."""
            IP, TCP_PORT = "0.0.0.0", self._ip_table[self._node_id][1]

            recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            recv_socket.bind((IP, TCP_PORT))
            #backlog; 1 for each Node besides self
            recv_socket.listen(4)

            while True:
                thread.start_new_thread(bully_algorithm, (self, recv_socket, timeout))
                time.sleep(poll_time)
                logging.debug("NEW LEADER IS: " + str(self._leader))

            recv_socket.close()

        thread.start_new_thread(_do_leader_election, (self, poll_time, timeout))
            
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
    def _make_ip_table():
        """Create the ID-to-IP translation table used for socket connection."""
        table = {}

        import re
        pattern = r"^\d+,\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3},\d{4},\d{5}$"
        with open(Node._ip_filename, "r") as f:
                for translation in f:
                    match = re.match(pattern, translation.strip())
                    if not match:
                        raise ValueError(
                            "Every line in IP_translations.txt must be of "
                            "form ID,IP")
                    ID, IP, TCP_PORT, UDP_PORT,  = translation.strip().split(',')
                    table[int(ID)] = [IP, int(TCP_PORT), int(UDP_PORT)]

        return table

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

        #If command is to clear, clear the screen
        if argv[0] == "clear":
            _do_clear()
            return

        #If command was to show something, do show
        if argv[0] == "show":
            try:
                _do_show(argv, node)
            except ValueError as excinfo:
                print excinfo
                print
            finally:
                return

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
            #fail-safe catch in case something fucks up and we don't know what
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()[:]
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
            finally:
                return

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
            finally:
                return

        print "Invalid command; supported commands = {clear,show,schedule,cancel}"
        print

def set_verbosity(verbose_level=3):
    """Set the level of verbosity of the Preprocessing."""
    if not type(verbose_level) == int:
        raise TypeError("verbose_level must be an int")

    if verbose_level < 0 or verbose_level > 4:
        raise ValueError("verbose_level must be between 0 and 4")

    verbosity = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG]

    logging.basicConfig(
        format='%(asctime)s:\t %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=verbosity[verbose_level])

def main():
    """Quick tests."""
    "schedule yaboi (user0,user1,user2,user3) (4:00pm,6:00pm) Friday"
    "cancel yaboi (user0,user1,user2,user3) (4:00pm,6:00pm) Friday"
    "schedule xxboi (user1,user4,user5) (1:30am,11:30am) Wednesday"
    "cancel xxboi (user1,user4,user5) (1:30am,11:30am) Wednesday"
    "schedule zo (user1,user2,user3) (12:30pm,1:30pm) Friday"

    a1 = Appointment("zo","Friday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("xxboi","Wednesday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("lol","saturday","11:30am","12:30pm", [1])
    a4 = Appointment("yeee","MondAy","11:30am","12:30pm", [1])
    a5 = Appointment("lolololol","Thursday","11:30am","12:30pm", [1])

    c1 = Calendar(a1)
    c2 = Calendar(a1, a2)
    c3 = Calendar(a1, a2, a3)
    c4 = Calendar(a1, a2, a3, a4)
    c5 = Calendar(a1, a2, a3, a4, a5)
    
    set_verbosity(3)

    N = Node(int(sys.argv[1]))

    
    N._log[0] = c1
    '''
    N._log[1] = c2
    N._log[2] = c3
    N._log[3] = c4
    N._log[4] = c5
    '''
    N._calendar = c1

    #try to load a previous state of this Node
    try:
        N = Node.load()
    except ValueError:
        pass
    except IOError:
        pass

    N.elect_leader(poll_time=6, timeout=3)
    N.paxos()

    print("@> Node Started")
    while True:
        message = raw_input('')
        if message == "quit":
            Node.save(N)
            break
        else:
            Node._parse_command(message, N)

if __name__ == "__main__":
    main()