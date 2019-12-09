import socket
import sys
from _thread import *
import threading
import rdt
import library
import os
import selectors
import types
import dns
from get_ip import *

""" Usage ports ->
	8080 : dns local

	9090 : server
"""

mutex = threading.Lock()

def register_in_dns(dns_address, server_alias = "crp.server.teste" ): 
	udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	data = "ADD " + server_alias
	try:
		print('sending {!r}'.format(data))
		sent = udpSocket.sendto(str(data).encode(),dns_address)

	finally:
		print('closing socket')
		udpSocket.close()


def help():
	print ("Try a valid transport protocol, like:\n --TCP (or --tcp) \n --UDP (or --udp)\n")
	print ("Exiting from server.")
	pass


def OpenBook(nameBook = "marcos.txt"):
	path = "./serverbooks/" + nameBook
	book = open(path, 'r')
	text = book.read()
	print(text)
	book.close()
	return text

def SaveBook(nameBook= "Marcos", text= "oi\neu\nsou\nmarcos"):
	path = "./serverbooks/" + nameBook
	newBook = open(path, 'w+')
	newBook.write(text)
	newBook.close()



def tcp_server_setup(server_address):
	_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	_socket.bind(server_address)
	_socket.listen()
	print("tcp server listening on", server_address)

	return _socket


def tcp_server_connection_handler(conn): 
	while True: 

		# Recebe dados do cliente
		data = conn.recv(1024) 
		if not data: 
			print('Bye') 
				
			# Libera o lock do mutex
			mutex.release() 
			break

		if data.decode() == "getallnamebooks":
			serverBooks = os.listdir("./serverbooks")
			print("vou enviar: ", serverBooks)
			snd_data = ""
			for i,m in enumerate(serverBooks):
				if i != len(serverBooks) - 1:
					snd_data += m + ","
				else:
					snd_data += m
			print('len = ',len(snd_data.encode()))
			conn.send(snd_data.encode())
		else: 
			_data = data.decode()
			params = _data.split(" ", 1)
			if params[0].lower() == "download":
				nameBook = params[1] 
				txt = OpenBook(nameBook)
				conn.send(txt.encode())
			elif params[0].lower() == "upload":
				newBook = params[1]
				print("salvando o livro")
				txt = conn.recv(1024)
				SaveBook(newBook, txt.decode())
			else:
				print("closing connection to", data.addr)
				mutex.release() 
				break
    
	# Fecha a conexão 
	conn.close() 


def main():
	dns_address = ('192.168.0.23', 8080)
	server_address = (get_ip(), 9090)
	assert len(sys.argv) == 2

	if sys.argv[1].lower() == "--udp" :

		register_in_dns(dns_address)

		sm = rdt.Rdt()

		while True:
			sm.config_receiever(server_address)
			data, ip_transmissor = sm.recv()
			print("Recebi dados: ", data, ip_transmissor)
			addr_client = (ip_transmissor[0], 9090)
			if data == "getallnamebooks":
				serverBooks = os.listdir("./serverbooks")
				print("vou enviar: ", serverBooks)
				sm.config_transmitter(addr_client)
				sm.send(serverBooks)
			else: 
				params = data.split(" ", 1)
				if params[0].lower() == "download":
					nameBook = params[1] 
					txt = OpenBook(nameBook)
					sm.config_transmitter(addr_client)
					sm.send(txt)
				elif params[0].lower() == "upload":
					newBook = params[1]
					sm.config_receiever(server_address)
					txt, ip_transmissor = sm.recv()
					print("salvando o livro")
					SaveBook(newBook, txt)
				else:
					print("Opção inexistente")

	elif sys.argv[1].lower() == "--tcp":
		sock = tcp_server_setup(server_address)
		register_in_dns(dns_address)
		try:
			while True:
				# EStabelece a conexão com o cliente
				conn, addr = sock.accept() 
		
				# Lock do mutex para o novo cliente 
				mutex.acquire() 
				print('Connected to :', addr[0], ':', addr[1]) 
		
				# Começa uma nova thread para as requisições do novo cliente 
				start_new_thread(tcp_server_connection_handler, (conn,)) 

		except KeyboardInterrupt:
			print("keyboard interrupt, exiting...")
		finally:
			sock.close()
	else:
		help()
		raise NameError("You choose a invalid option")

	return 0


if __name__ == '__main__':
	main()
