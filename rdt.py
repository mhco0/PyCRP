from enum import Enum


class States(Enum):
	""" A enum class for my states """

	WAIT_CALL_ZERO = 0
	WAIT_ACK_ZERO = 1
	WAIT_CALL_ONE = 2
	WAIT_ACK_ONE = 3
	WAIT_SQ_ZERO = 4
	WAIT_SQ_ONE = 5
	UNKNOW = 6

	pass


class Package:
	"""Docstring for Package"""

	def __init__(self,data,MSS = 1024):
		# MSS must be multiple of 2
		self.seq_num = 0
		self.bytes_sent = 0
		self.array_bytes = bytes(data)
		self.mss = MSS

		pass

	def start(self):
		return self.bytes_sent
		pass

	def next_sq_num(self):
		self.seq_num = not self.seq_num
		self.bytes_sent = min(self.start()+self.mss,len(self.array_bytes))
		pass

	# The first byte in the package always will be the sequence number for acks in the rdt class
	def bytes_to_send(self):
		return bytes(self.seq_num) + array_bytes[self.start():min(self.start()+self.mss,len(self.array_bytes))]
		pass

	def all_sent(self):
		return self.start() == len(self.array_bytes)
		pass


class Rdt_3_0:
	""" This a RDT3.0 Simulation to run over UDP
	
		-First you need to call config_server or config_client with the address
		otherwise this class will have a unespect behavior

	"""

	def __init__(self):
		self.state = States.UNKNOW
		self.sock = None
		self.package = None
		self.server = None
		self.type = "UNKNOW"
		self.flag_from_above = False
		pass

	def config_server(self,address=('localhost',5000)):
		self.type = "SERVER"

		self.state = States.WAIT_SQ_ZERO
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.bind(address)

		self.timer = None
		pass

	def config_client(self):
		self.type = "CLIENT"

		self.state = States.WAIT_CALL_ZERO
		self.timer = threading.Timer(3.0,Rdt_3_0.timeout,args=(self,))
		pass

	def timeout(self):
		self.sock.sendto(self.package.bytes_to_send(),self.server)
		pass

	def restart_timer(self):
		if not self.timer.is_alive():
			self.timer = threading.Timer(3.0,Rdt_3_0.timeout,args=(self,))
			self.timer.start()
		pass 

	def next_state(self,nextstate):
		self.state = nextstate
		pass

	def send(self,data):
		if self.package == None or (self.package != None and self.package.all_sent()):
			self.package = Package(data)
			self.flag_from_above = True
		else:
			print("Not all data sent")
		pass

	def state_machine(self):
		if self.type == "CLIENT":
			if self.flag_from_above :
				while not self.package.all_sent():

					if self.state == States.WAIT_CALL_ZERO:
						self.sock.sendto(self.package.bytes_to_send(),self.server)
						self.timer.start()
						self.next_state(States.WAIT_ACK_ZERO)
					elif self.state == States.WAIT_ACK_ZERO:

					elif self.state == States.WAIT_CALL_ONE:

					elif self.state == States.WAIT_ACK_ONE:

					else:
						raise NameError("Invalid state")

		elif self.type == "SERVER":

		else:
			raise NameError("RDT type not defined")

		pass

