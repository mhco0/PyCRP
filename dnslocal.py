import socket
import sys

def main():

	host = 'localhost'
	port = 8080

	sock =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	sock.bind((host,port))

	while True:
		data, client_address = sock.recvfrom(1024)

		print("recive from : {}".format(client_address))
		print(data.decode())

if __name__ == '__main__':
	main()