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
        self._command_queue = []
        self._my_proposals = {}
        from collections import defaultdict
        self._promise_queues = defaultdict(dict)
        self._ack_queues = defaultdict(dict)
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

        calendar, log_slot = message[1], message[2]
        self._my_proposals[log_slot] = (m, calendar)

        transmission = ("prepare", m, log_slot)
        for ID, IP_info in self._ip_table.items():
            IP, UDP_PORT = IP_info[0], IP_info[2]
            self._send_UDP_message(transmission, IP, UDP_PORT)

    def _recv_promise(self, message):
        """
        Receive promise message.

        Promise message form: ("promise", accNum, accVal, log_slot, sender_ID)
        """
        accNum, accVal, log_slot, sender_ID = message[1:]
        self._promise_queues[log_slot][sender_ID] = (accNum, accVal)

    def _send_accept(self, m, v, log_slot):
        """Send accept message as described in Synod Algorithm."""
        transmission = ("accept", m, v, log_slot)
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
        def _listen_to_promises(self):
            "Begin listening for majority of promises on each log slot"
            import math
            import time
            while True:
                log_slots = self._promise_queues.keys()
                num_nodes = len(self._ip_table.keys())
                majority = int(math.ceil(float(num_nodes) / 2.0))
                
                #for log slots for which there has been at least one promise
                for slot in log_slots:
                    #get the queue for particular log slot and calulate number
                    #of Acceptors that promised
                    slot_queue = self._promise_queues[slot]
                    num_promises = len(slot_queue.keys())

                    #if this Proposer has received a majority of responses
                    #send accept(m, v, log_slot)
                    if num_promises >= majority:
                        my_id = self._uid
                        other_ids = [uid for uid in slot_queue.keys() if uid != my_id]

                        #try to choose largest accNum accVal pair
                        m, v = -1, -1
                        for other_id in other_ids:
                            accNum, accVal = slot_queue[other_id]
                            if accNum != None and accVal != None:
                                if accNum > m:
                                    m, v = accNum, accVal

                        #Either only this Proposer's Node is up or everyone
                        #answered None, either way choose this Proposer's value
                        if m == -1 and v == -1:
                            m, v = self._my_proposals[slot]

                        self._send_accept(m, v, slot)

                time.sleep(.1)

        import thread
        thread.start_new_thread(_listen_to_promises, (self,))

        while True:
            if self._command_queue:
                message = self._command_queue.pop()
                message_command_type = message[0]
                debug_str = "Proposer got message; "
                if message_command_type == "propose":
                    print debug_str + "type: propose"
                    self._send_prepare(message)
                if message_command_type == "promise":
                    print debug_str + "type: promise"
                    self._recv_promise(message)
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