"""Node (User) Class for Paxos Calendar."""

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

def main():
    """Quick tests."""
    n = Node(0)

if __name__ == "__main__":
    main()