import socket
import sys

server_mapping = {}

def get_command(data):
	return data.decode().split(' ',1)

def add_server(server_alias,ip_address):
	server_mapping[server_alias] = ip_address

def find_server(server_alias):
	if server_alias in server_mapping:
		return server_mapping[server_alias]
	else:
		return "NOT FOUND"

def send_ip(client_address):
	pass

def main():

	dnsHost = 'localhost'
	dnsPort = 8080

	dnsSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dnsSocket.bind((dnsHost,dnsPort))
	print ("DNS STARTED")
	print ("\tDNS PORT: {}".format(dnsPort)) 

	while True:
		data, client_address = dnsSocket.recvfrom(1024)
		print ("\tDATA: {}".format(get_command(data)))

		command, server_alias = get_command(data)
		print("Command:", command)

		if command == 'ADD':
			add_server(server_alias,client_address[0])
			print (server_mapping)
		elif command == 'FIND':
			result = find_server(server_alias)
			dnsSocket.sendto(str(result).encode(), client_address)

if __name__ == "__main__" :
    main()
