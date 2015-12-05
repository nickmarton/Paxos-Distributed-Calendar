"""Acceptor class for Paxos Calendar."""

import pickle
import socket
import time

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
        self._command_queue = []
        self._commits_queue = []
        self._ip_table = ip_table
        self._terminate = False
        self._is_Acceptor = True

    def _send_UDP_message(self, data, IP, UDP_PORT):
        """Send pickled data through UDP socket bound to (IP, UDP_PORT)."""
        import pickle
        import socket
        transmission = pickle.dumps(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(transmission, (IP, UDP_PORT))
        s.close()

    def _recv_prepare(self, message):
        """
        Handle reception of prepare message as described in Synod Algorithm.

        Prepare messages of form ("prepare", m, log_slot, sender_ID)
        """

        m, log_slot, sender_ID = message[1:]

        if m > self._maxPrepare:
            self._maxPrepare = m
            IP, UDP_PORT = self._ip_table[sender_ID][0], self._ip_table[sender_ID][2]
            self._send_promise(IP, UDP_PORT, self._accNum, self._accVal, log_slot)

    def _send_promise(self, IP, PORT, accNum, accVal, log_slot):
        """Send promise message with given accNum, accVal to given IP, PORT."""
        transmission = ("promise", accNum, accVal, log_slot)
        self._send_UDP_message(transmission, IP, PORT)

    def _recv_accept(self, message):
        """
        Handle reception of accept message as described in Synod Algorithm.
        """

        m, v, log_slot, sender_ID = message[1:]
        if m >= self._maxPrepare:
            self._accNum = m
            self._accVal = v
            IP, UDP_PORT = self._ip_table[sender_ID][0], self._ip_table[sender_ID][2]
            self._send_ack(IP, UDP_PORT, self._accNum, self._accVal, log_slot)

    def _send_ack(self, IP, PORT, accNum, accVal, log_slot):
        """Send ack with given accNum, accVal to given IP, PORT."""
        transmission = ("ack", accNum, accVal, log_slot)
        self._send_UDP_message(transmission, IP, PORT)

    def _recv_commit(self, message):
        """
        Handle reception of commit message as described in Synod Algorithm.
        """

        v, log_slot = message[1], message[2]
        self._commits_queue.append((log_slot, v))

    def start(self):
        """Start the Acceptor; serve messages in its queue."""
        while True:
            if self._command_queue:
                message = self._command_queue.pop()
                message_command_type = message[0]
                debug_str = "Acceptor; "
                if message_command_type == "prepare":
                    print debug_str + "type: prepare with slot = " + str(message[2]) + ", m = " + str(message[1])
                    self._recv_prepare(message)
                elif message_command_type == "accept":
                    #print debug_str + "type: accept with slot = " + str(message[3]) + ", m = " + str(message[1])
                    self._recv_accept(message)
                elif message_command_type == "commit":
                    #print debug_str + "type: commit " + + str(message[2])
                    self._recv_commit(message)

            if self._terminate:
                break

            time.sleep(.001)

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
