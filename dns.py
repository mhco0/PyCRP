import socket
import sys

server_mapping = {}

def get_command(data):
	return data.decode().split(' ',1)
	pass
	
def add_server(server_alias,ip_address):
	server_mapping[server_alias] = ip_address
	pass

def find_server(server_alias):
	if server_alias in server_mapping:
		return server_mapping[server_alias]
	else:
		return "NOT FOUND"
	pass

def main():

	dnsHost = socket.gethostbyname(socket.gethostname())
	dnsPort = 8080

	dnsSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dnsSocket.bind((dnsHost,dnsPort))
	print ("DNS STARTED")
	print ("\tDNS PORT: {}".format(dnsPort)) 
	print (socket.gethostbyname(socket.gethostname()))

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
			print ("server found: ip_address is {}".format(result))
			dnsSocket.sendto(str(result).encode(), client_address)

if __name__ == "__main__" :
    main()
