"""Proposer class for Paxos Calendar."""

class Proposer(object):
    """
    Proposer class.

    uid:                        Unique id (id of Node containing this Proposer
                                is a good choice); used as number to increment.
    current_proposal_number:    Proposal number that was most recently used 
    """

    def __init__(self, uid, ip_table):
        """Construct Proposer object."""
        if type(uid) != int:
            raise TypeError("uid must be an integer")

        self._uid = uid
        self._current_proposal_number = uid
        self._queue = []
        self._ip_table = ip_table
        self._is_Proposer = True

    def _send_UDP_message(self, data, UDP_IP, UDP_PORT):
        """Send data through UDP socket bound to (UDP_IP, UDP_PORT)."""
        transmission = pickle.dumps(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(transmission, (str(UDP_IP), int(UDP_PORT)))
        s.close()

    def _send_prepare(self):
        """Send prepare message as described in Synod Algorithm."""
        m = self._current_proposal_number + 10
        for ID, IP_info in self._ip_table.items():
            pass

    def _recv_promise(self):
        """Receive promise message."""
        pass

    def _send_accept(self):
        """Send accept message as described in Synod Algorithm."""
        for ID, IP_info in self._ip_table.items():
            pass

    def _recv_ack(self):
        """Receive ack message."""
        pass

    def _send_commit(self):
        """Send commit message as described in Synod Algorithm."""
        for ID, IP_info in self._ip_table.items():
            pass

    def start(self):
        """Start the Proposer; serve messages in it's queue."""
        while True:

            if self._queue:
                message = self._queue.pop()
                message_command_type = message[0]
                print "Proposer got message:"
                if message_command_type == "propose":
                    print "type: propose" #self.send_prepare(message)
                if message_command_type == "promise":
                    print "type: promise" #self.recv_promise(message)
                if message_command_type == "ack":
                    print "type: ack" #self.recv_ack(message)
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