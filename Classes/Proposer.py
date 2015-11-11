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
