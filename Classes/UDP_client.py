import socket
import sys
import pickle
import thread

def UDP_transmission(data, UDP_IP, UDP_PORT):
    """Transmits data to IP:PORT via UDP"""
    transmission = pickle.dumps(data)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(transmission, (UDP_IP, UDP_PORT))
    s.close()

def listen():
    """."""
    IP, UDP_PORT = "0.0.0.0", 9011
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
        print data, addr

def main():

    UDP_IP = sys.argv[1]
    UDP_PORT = sys.argv[2]

    from Calendar import Calendar
    c = Calendar()

    test_prepare = ("prepare", 2)
    test_commit = ("commit", c)
    test_accept = ("accept", 2, c)
    test_promise = ("promise", 1, c)
    test_ack = ("ack", 1, c)


    thread.start_new_thread(listen, ())

    print("@> UDP client started")
    while True:
        message = raw_input('')
        if message == "quit":
            break
        elif message == "prepare":
            UDP_transmission(test_prepare, UDP_IP, int(UDP_PORT))
        elif message == "promise":
            UDP_transmission(test_promise, UDP_IP, int(UDP_PORT))
        elif message == "accept":
            UDP_transmission(test_accept, UDP_IP, int(UDP_PORT))
        elif message == "ack":
            UDP_transmission(test_ack, UDP_IP, int(UDP_PORT))
        elif message == "commit":
            UDP_transmission(test_commit, UDP_IP, int(UDP_PORT))
        else:
            pass

if __name__ == "__main__":
    main()