import socket
import sys
		
def register_in_dns(dns_address):

	appear = False

	server_alias = "crp.server.teste" 
	server_ip = socket.gethostbyname(socket.gethostname())

	data = (server_alias,server_ip)

	with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
		if not appear:
			print ("Trying to apply a {}".format('UDP'))
			print ("\tsocket family (AF_INET) : {},\n\tsocket type (SOCK_DGRAM): {},\n\tsocket protocol : {}".format(sock.family,sock.type,sock.proto))
			appear = True

		sock.sendto(str(data).encode(),dns_address)


	pass

def help():
	print ("Try a valid transport protocol, like:\n --TCP (or --tcp) \n --UDP (or --udp)\n")
	print ("Exiting from server.")
	pass

def main():
	assert len(sys.argv) == 2

	if sys.argv[1].lower() == "--udp" :
		##justfortst
		
		register_in_dns(('localhost',8080))

	elif sys.argv[1].lower() == "--tcp":
		"""
			you code here the tcp server.
		"""
	else:
		help()
		raise NameError("You choose a invalid option")

	return 0


if __name__ == '__main__':
	main()