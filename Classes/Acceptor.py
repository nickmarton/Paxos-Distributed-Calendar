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
        self._is_Acceptor = True

    def save(self, filename="./Acceptor.pkl"):
        """
        Write Acceptor object to memory, i.e., store maxPrepare, accNum, and
        accVal.

        Done easily with pickle module.
        """

        if type(filename) != str:
            print type(filename)
            raise TypeError("filename must be a string")

        if filename[-4:] != ".pkl":
            raise ValueError("filename must have .pkl extension")

        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def __str__(self):
        """Implement str(Acceptor)."""
        return str((self._maxPrepare, self._accNum, self._accVal))

    def __repr__(self):
        """Implement repr(Acceptor)."""
        return self.__str__()

def main():
    """Quick tests."""
    a = Acceptor()
    print a

if __name__ == "__main__":
    main()