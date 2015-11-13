"""Node (User) Class for Paxos Calendar."""

import os
import pickle
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
    log:            List of Calendar objects used in full Paxos Algorithm;
                    intially empty, Synod Algorithm is used to fill each entry
                    of log
    """

    def __init__(self, node_id):
        """Construct a Node object."""
        if type(node_id) != int:
            raise TypeError("node_id must be an int")
        if node_id < 0:
            raise ValueError("node id must be a nonnegative integer")

        self._node_id = node_id
        self._calendar = Calendar()
        self._proposer = Proposer(node_id)
        self._acceptor = Acceptor()
        self._log = {}
        self._is_Node = True

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

def main():
    """Quick tests."""
    n = Node(0)
    n._acceptor._maxPrepare = 10

    a1 = Appointment("zo","Friday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("xxboi","Wednesday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("lol","saturday","11:30am","12:30pm", [1])
    a4 = Appointment("yeee","MondAy","11:30am","12:30pm", [1])
    a5 = Appointment("fuuuuuuu","TUESDAY","11:30am","12:30pm", [1])
    a6 = Appointment("paxos","ThUrSday","11:30am","12:30pm", [1])
    a7 = Appointment("ddddd","sunday","11:30am","12:30pm", [1])
    c1 = Calendar(a1,)
    c2 = Calendar(a1, a2)
    c3 = Calendar(a1, a2, a3)
    c3 = Calendar(a1, a2, a3)
    c4 = Calendar(a1, a2, a3, a4)
    c5 = Calendar(a1, a2, a3, a4, a5)
    c6 = Calendar(a1, a2, a3, a4, a5, a6)
    c7 = Calendar(a1, a2, a3, a4, a5, a6, a7)

    n._log[0] = c1
    n._log[1] = c2
    n._log[2] = c3
    n._log[3] = c4
    n._log[4] = c5
    n._log[5] = c6
    n._log[6] = c7

    Node.save(n)

    nn = Node.load()

if __name__ == "__main__":
    main()