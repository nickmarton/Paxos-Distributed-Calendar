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
        self._log = []

    @staticmethod
    def save(Node, path="./", filename="state.pkl"):
        """Save this Node's log and Acceptor to stable storage."""
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
            pass

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

    Node.save(n)

    nn = Node.load()
    print nn._acceptor


if __name__ == "__main__":
    main()