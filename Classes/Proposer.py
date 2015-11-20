"""Proposer class for Paxos Calendar."""

class Proposer(object):
    """
    Proposer class.

    uid:                        Unique id (id of Node containing this Proposer
                                is a good choice); used as number to increment.
    current_proposal_number:    Proposal number that was most recently used 
    """

    def __init__(self, uid):
        """Construct Proposer object."""
        if type(uid) != int:
            raise TypeError("uid must be an integer")

        self._uid = uid
        self._current_proposal_number = uid
        self._queue = []

    def start(self):
        """Start the Proposer; serve messages in it's queue."""
        while True:

            if self._queue:
                message = self._queue.pop()
                print message


    def __str__(self):
        """Implement str(Proposer)."""
        ret_str = "Proposer:\n\tUnique ID: " + str(self._uid) + '\n\t'
        ret_str += "Current Proposal number: " + str(self._current_proposal_number)
        return ret_str

    def __repr__(self):
        """Implement repr(Proposer)."""
        return self.__str__()

def main():
    """Quick tests."""
    pass

if __name__ == "__main__":
    main()