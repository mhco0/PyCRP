from enum import Enum
import socket
import threading


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

	MSS = 2048

	def __init__(self,data,myMSS = 1024):
		# MSS must be multiple of 2
		self.seq_num = 0
		self.bytes_sent = 0
		self.array_bytes = bytes(data)
		self.len_pack = len(self.array_bytes)
		self.first_send = False
		self.mss = myMSS

		pass

	def convert_pack(data):
		sqn = int.from_bytes(data[:24],byteorder = 'big',signed = True)
		real_data = data[24:]

		return sqn,real_data

	def mss(self):
		return self.mss

	def mss():
		return Package.MSS

	def start(self):
		return self.bytes_sent

	def has_sent_first_package(self):
		return self.first_send

	def first_package_sent(self):
		self.first_send = True
		pass

	def next_sq_num(self):
		self.seq_num = not self.seq_num

		if self.has_sent_first_package() :
			self.bytes_sent = min(self.start()+self.mss,len(self.array_bytes))

		pass

	# The first byte in the package always will be the sequence number for acks in the rdt class
	def bytes_to_send(self):
		if self.has_sent_first_package() :
			return bytes(self.seq_num) + array_bytes[self.start():min(self.start()+self.mss,len(self.array_bytes))]
		else:
			return bytes(self.seq_num) + bytes(self.len_pack)
		pass

	def all_sent(self):
		return self.start() == len(self.array_bytes)
	


class Rdt:
	""" This a RDT3.0 Simulation to run over UDP
	
		-First you need to call config_server or config_client with the address
		otherwise this class will have a unespect behavior

		-We use ('localhost',5000) as default

	"""

	def __init__(self):
		self.state = States.UNKNOW
		self.sock = None
		self.package = None
		self.receiever = None
		self.type = "UNKNOW"
		self.flag_from_above = False
		self.ack = None
		pass

	def config_receiever(self,address=('localhost',5000)):
		self.type = "RECEIEVER"

		self.state = States.WAIT_SQ_ZERO
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.bind(address)

		self.timer = None
		self.ack = 0
		pass

	def config_transmitter(self,address):
		self.type = "TRANSMITTER"

		self.state = States.WAIT_CALL_ZERO
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.receiver = address
		self.timer = threading.Timer(3.0,Rdt.timeout,args=(self,))
		pass

	def restart_timer(self):
		if not self.timer.is_alive():
			self.timer = threading.Timer(3.0,Rdt_3_0.timeout,args=(self,))
			self.timer.start()
		pass

	def timeout(self):
		self.sock.sendto(self.package.bytes_to_send(),self.receiver)
		self.restart_timer()
		pass 

	def next_state(self,nextstate):
		self.state = nextstate
		pass

	def send(self,data):
		if self.package == None or (self.package != None and self.package.all_sent()):
			self.package = Package(data)
			self.flag_from_above = True

			self.state_machine()
		else:
			print("Not all data sent")
		pass

	def recv(self):
		return self.state_machine()
		pass

	def state_machine(self):
		all_data = []

		if self.type == "TRANSMITTER":
			if self.flag_from_above :
				first_pack = False
				while not self.package.all_sent():

					if self.state == States.WAIT_CALL_ZERO:
						self.sock.sendto(self.package.bytes_to_send(),self.receiver)
						self.timer.start()
						self.next_state(States.WAIT_ACK_ZERO)

					elif self.state == States.WAIT_ACK_ZERO:
						ack, recv_address = self.sock.recvfrom(1024)

						if ack.decode() == '0'  and recv_address == self.receiver:
							self.timer.cancel()
							if not first_pack:
								self.package.next_sq_num()
							else:
								first_pack = True
								self.package.first_package_sent()
								self.package.next_sq_num()
							self.next_state(States.WAIT_CALL_ONE)

					elif self.state == States.WAIT_CALL_ONE:
						self.sock.sendto(self.package.bytes_to_send(),self.receiver)
						self.timer.start()
						self.next_state(States.WAIT_ACK_ONE)

					elif self.state == States.WAIT_ACK_ONE:
						ack, recv_address = self.sock.recvfrom(1024)

						if ack.decode() == '1' and recv_address == self.receiver:
							self.timer.cancel()
							if not first_pack:
								self.package.next_sq_num()
							else:
								first_pack = True
								self.package.first_package_sent()
								self.package.next_sq_num()
							self.next_state(States.WAIT_CALL_ZERO)

					else:
						raise NameError("Invalid state Transmitter")

				print("All data sent")
		elif self.type == "RECEIEVER":
			first_pack = True
			package_size = 0

			while True:
				# last this
				if self.state == States.WAIT_SQ_ZERO:
					bpack, tmitt_address = self.sock.recvfrom(Package.mss())

					sqn,data = Package.convert_pack(bpack)

					if sqn == 0 : 
						if first_pack :	
							package_size = int.from_bytes(data,byteorder = 'big',signed = True)
							first_pack = False
						else:
							all_data += data

						self.sock.sendto('0'.encode(),tmitt_address)

				elif self.state == State.WAIT_SQ_ONE:
					bpack, tmtt_address = self.sock.recvfrom(Package.mss())	

					sqn,data = Package.convert_pack(bpack)

					if sqn == 1 : 
						if first_pack :	
							package_size = int.from_bytes(data,byteorder = 'big',signed = True)
							first_pack = False
						else:
							all_data += data

						self.sock.sendto('1'.encode(),tmitt_address)
				else:
					raise NameError ("Invalid state Receiver")

				if not first_pack and len(all_data) == package_size:
					break

			print("All data received")

		else:
			raise NameError("RDT type not defined")

		return all_data