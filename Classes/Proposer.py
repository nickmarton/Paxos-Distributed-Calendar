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

    def _send_UDP_message(self, data, IP, UDP_PORT):
        """Send data through UDP socket bound to (IP, UDP_PORT)."""
        import pickle
        import socket
        transmission = pickle.dumps(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(transmission, (IP, UDP_PORT))
        s.close()

    def _send_prepare(self, message):
        """Send prepare message as described in Synod Algorithm."""
        m = self._current_proposal_number + 10

        log_slot = message[2]
        
        transmission = ("prepare", m, log_slot)
        for ID, IP_info in self._ip_table.items():
            IP, UDP_PORT = IP_info[0], IP_info[2]
            self._send_UDP_message(transmission, IP, UDP_PORT)

    def _recv_promise(self):
        """
        Receive promise message.

        Promise message of form ("promise", accNum, accVal, log_slot, sender_ID)
        """
        pass

    def _send_accept(self):
        """Send accept message as described in Synod Algorithm."""
        transmission = ("accept", )
        for ID, IP_info in self._ip_table.items():
            IP, UDP_PORT = IP_info[0], IP_info[2]
            self._send_UDP_message(transmission, IP, UDP_PORT)

    def _recv_ack(self):
        """Receive ack message."""
        pass

    def _send_commit(self):
        """Send commit message as described in Synod Algorithm."""
        transmission = ("commit", )
        for ID, IP_info in self._ip_table.items():
            IP, UDP_PORT = IP_info[0], IP_info[2]
            self._send_UDP_message(transmission, IP, UDP_PORT)

    def start(self):
        """Start the Proposer; serve messages in it's queue."""
        while True:
            if self._queue:
                message = self._queue.pop()
                message_command_type = message[0]
                debug_str = "Proposer got message:"
                if message_command_type == "propose":
                    print debug_str + "type: propose"
                    self._send_prepare(message)
                if message_command_type == "promise":
                    print debug_str + "type: promise"
                    #self.recv_promise(message)
                if message_command_type == "ack":
                    print debug_str + "type: ack"
                    #self.recv_ack(message)
                #print message
                #print

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