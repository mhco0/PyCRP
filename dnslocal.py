import socket
import sys

def main():

	dns_address = ('localhost', 8080)

	sock =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	print('starting up on {} port {}'.format(*dns_address))

	sock.bind(dns_address)

	try:
		while True:
			data, client_address = sock.recvfrom(1024)

			print("recive from : {}".format(client_address))
			print(data.decode())
	except KeyboardInterrupt:
		print("keyboard interrupt, exiting...")
	finally:
		sock.close()

if __name__ == '__main__':
	main()

