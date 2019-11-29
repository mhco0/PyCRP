import socket
import sys
import threading
from enum import Enum

""" Usage ports ->
	8080 : dns local

	5000 : server
"""


class States(Enum):
	""" A enum class for my states """

	WAIT_CALL_ZERO = 0
	WAIT_ACK_ZERO = 1
	WAIT_CALL_ONE = 2
	WAIT_ACK_ONE = 3
	UNK = 4

	pass

class Rdt_3_0:
	""" This a RDT3.0 Simulation to run over UDP
	
		-First you need to call config_server or config_client with the address
		otherwise this class will have a unespect behavior

	"""

	def __init__(self):
		self.state = States.UNKNOW
		self.sock = None
		self.bytes_to_send = None
		self.client = None
		self.type = "UNKNOW"
	pass

	def config_server(self,address=('localhost',5000)):
		self.type = "SERVER"

		self.state = States.WAIT_ACK_ZERO
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.bind(address)

		self.timer = threading.Timer(3.0,Rdt_3_0.timeout,args=(self,))
	pass

	def config_client(self):
		self.type = "CLIENT"

		self.state = 
	pass

	def timeout(self):
		self.sock.sendto(self.bytes_to_send,self.client)
	pass

	def restart_timer(self):
		if not self.timer.is_alive():
			self.timer = threading.Timer(3.0,Rdt_3_0.timeout,args=(self,))
			self.timer.start()
	pass 

	def next_state(self,nextstate):
		self.state = nextstate
	pass

	def state_machine(self):



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

		sm = Rdt_3_0()

		sm.config_server(('localhost',5000))

		while True:
			sm.restart_timer()
			pass

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