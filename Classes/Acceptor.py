"""Acceptor class for Paxos Calendar."""

class Acceptor(object):
    """
    Acceptor class.

    maxPrepare:     The maximum proposal number this Acceptor has encountered;
                    initialized at -1 so a node can have id = 0.
    accNum:         Number of highest-numbered proposal this Acceptor object
                    has accepted thus far; initialized as None.
    accVal:         Value of highest-numbered proposal this Acceptor object
                    has accepted thus far; initialized as None.

    Acceptor has to keep track of its maxPrepare, accNum and accVal in case of
    a crash and must be able to write them to stable storage.
    """

    def __init__(self):
        """Construct Acceptor object."""
        self._maxPrepare = -1
        self._accNum = None
        self._accVal = None
        self._queue = []
        self._is_Acceptor = True

    def start(self):
        """Start the Acceptor; serve messages in its queue."""
        while True:

            if self._queue:
                message = self._queue.pop()
                print "got message:"
                print message

    def __str__(self):
        """Implement str(Acceptor)."""
        ret_str = "Acceptor\n\tMaxPrepare: " + str(self._maxPrepare)
        ret_str += "\n\tAccNum: " + str(self._accNum)
        ret_str += "\n\tAccVal: " + str(self._accVal)
        return ret_str

    def __repr__(self):
        """Implement repr(Acceptor)."""
        return self.__str__()

def main():
    """Quick tests."""
    a = Acceptor()
    print a

if __name__ == "__main__":
    main()