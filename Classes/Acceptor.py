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
        self._is_Acceptor = True
        self._ip_table = ip_table

    def UDP_transmission(self, data, UDP_IP, UDP_PORT):
        """Transmits data to IP:PORT via UDP"""
        transmission = pickle.dumps(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(transmission, (str(UDP_IP), int(UDP_PORT)))

    def send_promise(self):
        for i in self._ip_table:
            IP_address = self._ip_table[i][1]
            UDP_PORT = self._ip_table[i][2]
            transmission = ("promise", self._maxPrepare, 
                self._accNum, self._accVal)
            self.UDP_transmission( transmission, IP_address, int(UDP_PORT))

    def recv_prepare(self, message):
        m_value = message[1]
        if m_value > self._maxPrepare:
            self._maxPrepare = m_value
            transmission = ("promise", self._accNum, self._accVal)
            self.send_promise()

    def recv_accept(self, message):
        m_value = message[1]
        v_value = message[2]
        if m_value >= self._maxPrepare:
            self._accNum = m_value
            self._accVal = v_value
            print "TO DO: SEND ack",(self._accNum, self._accVal),")" 
    
    def recv_commit(self, message):
        v_value = message[1]
        print "TO: Record",v_value,"in log"


    def start(self):
        """Start the Acceptor; serve messages in its queue."""
        while True:
            if self._queue:
                message = self._queue.pop()
                message_command_type = message[0]
                print "Acceptor got message:"
                if message_command_type == "prepare":
                    self.recv_prepare(message)
                elif message_command_type == "accept":
                    self.recv_accept(message)
                elif message_command_type == "commit":
                    self.recv_commit(message)
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