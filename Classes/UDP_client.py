import socket
import sys
import pickle

def UDP_transmission(data, UDP_IP, UDP_PORT):
	"""Transmits data to IP:PORT via UDP"""
	tranmission = data.dumps(data)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(transmission, (UDP_IP, UDP_PORT))



def main():
	UDP_IP = sys.argv[1]
	UDP_PORT = sys.argv[2]

	print("@> UDP client started")
	while True:
		message = raw_input('')
		if message == "quit":
			break
		else:
			UDP_transmission(message, UDP_IP, UDP_PORT)

if __name__ == "__main__":
	main()
