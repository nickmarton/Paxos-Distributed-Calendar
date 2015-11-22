"""Acceptor class for Paxos Calendar."""
import pickle
import socket
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

    def __init__(self, ip_table):
        """Construct Acceptor object."""
        self._maxPrepare = -1
        self._accNum = None
        self._accVal = None
        self._queue = []
        self._ip_table = ip_table
        self._is_Acceptor = True

    def _send_UDP_message(self, data, UDP_IP, UDP_PORT):
        """Send data through UDP socket bound to (UDP_IP, UDP_PORT)."""
        transmission = pickle.dumps(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(transmission, (str(UDP_IP), int(UDP_PORT)))
        s.close()

    def _recv_prepare(self, message):
        """
        Handle reception of prepare message as described in Synod Algorithm.
        """

        m, sender_ID = message[1], message[2]
        if m > self._maxPrepare:
            self._maxPrepare = m
            IP, UDP_PORT = self._ip_table[sender_ID][1], self._ip_table[sender_ID][2]
            self._send_promise(IP, UDP_PORT, self._accNum, self._accVal)

    def _send_promise(self, IP, PORT, accNum, accVal):
        """Send promise message with given accNum, accVal to given IP, PORT."""
        transmission = ("promise", self._accNum, self._accVal)
        self._send_UDP_message(transmission, IP, PORT)

    def _recv_accept(self, message):
        """
        Handle reception of accept message as described in Synod Algorithm.
        """

        m, v, sender_ID = message
        if m >= self._maxPrepare:
            self._accNum = m
            self._accVal = v
            print "TO DO: SEND ack" + str((self._accNum, self._accVal)) + ")"

    def _send_ack(self, self, IP, PORT, accNum, accVal):
        """Send ack with given accNum, accVal to given IP, PORT."""
        pass

    def _recv_commit(self, message):
        """
        Handle reception of commit message as described in Synod Algorithm.
        """

        v = message[1]
        print "TO: Record",v,"in log"

    def start(self):
        """Start the Acceptor; serve messages in its queue."""
        while True:
            if self._queue:
                message = self._queue.pop()
                message_command_type = message[0]
                print "Acceptor got message:"
                if message_command_type == "prepare":
                    print "type: prepare" #self._recv_prepare(message)
                elif message_command_type == "accept":
                    print "type: accept" #self._recv_accept(message)
                elif message_command_type == "commit":
                    print "type: commit" #self._recv_commit(message)
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
