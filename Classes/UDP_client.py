import socket
import sys
import pickle

def UDP_transmission(data, UDP_IP, UDP_PORT):
	"""Transmits data to IP:PORT via UDP"""
	transmission = pickle.dumps(data)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(transmission, (UDP_IP, UDP_PORT))

def main():
	
	UDP_IP = sys.argv[1]
	UDP_PORT = sys.argv[2]

	from Calendar import Calendar
	c = Calendar()

	test_prepare = ("prepare", 1)
	test_commit = ("commit", c)
	test_accept = ("accept", 1, c)
	test_promise = ("promise", 1, c)
	test_ack = ("ack", 1, c)


	print("@> UDP client started")
	while True:
		message = raw_input('')
		if message == "quit":
			break
		else:
			UDP_transmission(test_ack, UDP_IP, int(UDP_PORT))

if __name__ == "__main__":
	main()