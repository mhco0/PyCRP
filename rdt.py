from enum import Enum
import socket

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
	"""Docstring for Package
		Your Object must to have a explicit convertion for String
		or this class will not work
	"""

	MSS = 2048

	def __init__(self,data,myMSS = 1024):
		# MSS must be multiple of 2
		self.seq_num = '0'
		self.bytes_sent = 0
		self.array_bytes = str(data).encode()
		self.len_pack = len(self.array_bytes)
		self.first_send = False
		self.mss = myMSS

		pass

	def convert_pack(data):
		data = data.decode()
		sqn = data[0]
		real_data = data[1:]

		return sqn,real_data

	def mss(self):
		return self.mss

	def mss():
		return Package.MSS

	def set_upper_mss(upper):
		Package.MSS = upper
		pass

	def start(self):
		return self.bytes_sent

	def has_sent_first_package(self):
		return self.first_send

	def first_package_sent(self):
		self.first_send = True
		pass

	def next_sq_num(self):
		if self.seq_num == '0':
			self.seq_num = '1'
		elif self.seq_num == '1':
			self.seq_num = '0'
		else:
			raise NameError("Unespect sequence number")


		if self.has_sent_first_package() :
			self.bytes_sent = min(self.start()+self.mss,self.len_pack)

		pass

	# The first byte in the package always will be the sequence number for acks in the rdt class
	def bytes_to_send(self):
		if self.has_sent_first_package() :
			print(self.array_bytes[self.start():min(self.start()+self.mss,self.len_pack)])
			return self.seq_num.encode() + self.array_bytes[self.start():min(self.start()+self.mss,self.len_pack)]
		else:
			return self.seq_num.encode() + str(self.len_pack).encode()
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
		pass

	def config_receiever(self,address=('localhost',5000)):
		self.type = "RECEIEVER"

		self.state = States.WAIT_SQ_ZERO
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.bind(address)

		self.stop_timer()
		pass

	def config_transmitter(self,address):
		self.type = "TRANSMITTER"

		self.state = States.WAIT_CALL_ZERO
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.receiver = address

		self.stop_timer()
		pass

	def start_timer(self):
		self.sock.settimeout(3.0)
		pass

	def stop_timer(self):
		self.sock.settimeout(None)
		pass

	def timeout(self):
		self.sock.sendto(self.package.bytes_to_send(),self.receiver)
		self.start_timer()
		pass 

	def next_state(self,nextstate):
		self.state = nextstate
		pass

	def reset_state(self):

		if self.type == "TRANSMITTER":
			self.state = States.WAIT_CALL_ZERO
		elif self.type == "RECEIEVER":
			self.state = States.WAIT_SQ_ZERO
		else:
			raise NameError("Type Undefined")
		pass

	def send(self,data):
		if self.package == None or (self.package != None and self.package.all_sent()):
			self.package = Package(data)
			self.state_machine()
			self.reset_state()
		else:
			print("Not all data sent")
		pass

	def recv(self):
		recv_data = self.state_machine()
		self.reset_state()
		return recv_data

	def state_machine(self):
		all_data = ''

		if self.type == "TRANSMITTER":
			first_pack = True
			while True:

				if self.state == States.WAIT_CALL_ZERO:
					print(self.package.bytes_to_send())
					self.sock.sendto(self.package.bytes_to_send(),self.receiver)
					self.start_timer()
					self.next_state(States.WAIT_ACK_ZERO)

				elif self.state == States.WAIT_ACK_ZERO:
					try:
						ack, recv_address = self.sock.recvfrom(1024)

						if ack.decode() == '0':
							self.stop_timer()
							if first_pack:
								first_pack = False
								self.package.next_sq_num()
								self.package.first_package_sent()
							else:
								self.package.next_sq_num()

							self.next_state(States.WAIT_CALL_ONE)
						else:
							raise NameError("Corrupted Ack")

					except socket.timeout:
						self.timeout()

				elif self.state == States.WAIT_CALL_ONE:
					print(self.package.bytes_to_send())
					self.sock.sendto(self.package.bytes_to_send(),self.receiver)
					self.start_timer()
					self.next_state(States.WAIT_ACK_ONE)

				elif self.state == States.WAIT_ACK_ONE:
					try:
						ack, recv_address = self.sock.recvfrom(1024)

						if ack.decode() == '1':
							self.stop_timer()
							if first_pack:
								first_pack = False
								self.package.next_sq_num()
								self.package.first_package_sent()
							else:
								self.package.next_sq_num()

							self.next_state(States.WAIT_CALL_ZERO)
						else:
							raise NameError("Corrupted Ack")

					except socket.timeout:
						self.timeout()
				else:
					raise NameError("Invalid state Transmitter")

				if self.package.all_sent():
					break

			print("All data sent")
		elif self.type == "RECEIEVER":
			first_pack = True
			package_size = -1

			while True:
				# last this
				if self.state == States.WAIT_SQ_ZERO:
					print('here')
					try:
						bpack, tmitt_address = self.sock.recvfrom(Package.mss())

						sqn,data = Package.convert_pack(bpack)
						print(data)

						if sqn == '0' : 
							if first_pack :	
								package_size = int(data)
								first_pack = False
							else:
								all_data += data

							self.sock.sendto('0'.encode(),tmitt_address)
							self.next_state(States.WAIT_SQ_ONE)
						elif sqn == '1':
							self.sock.sendto('0'.encode(),tmitt_address)
						else:
							raise NameError("Invalid sequence number")
					finally:
						pass 

				elif self.state == States.WAIT_SQ_ONE:
					print('now here')
					try:
						bpack, tmtt_address = self.sock.recvfrom(Package.mss())	

						sqn,data = Package.convert_pack(bpack)
						print(data)

						if sqn == '1': 
							if first_pack :	
								package_size = int(data)
								first_pack = False
							else:
								all_data += data

							self.sock.sendto('1'.encode(),tmitt_address)
							self.next_state(States.WAIT_SQ_ZERO)
						elif sqn == '0':
							self.sock.sendto('1'.encode(),tmtt_address)
						else:
							raise NameError("Invalid sequence number")
					finally:
						pass

				else:
					raise NameError ("Invalid state Receiver")

				if not first_pack and len(all_data) == package_size:
					break


			print("All data received")

		else:
			raise NameError("RDT type not defined")

		return all_data