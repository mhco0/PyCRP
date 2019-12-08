import socket
import sys
import threading
import rdt
import selectors
import types
import dns

""" Usage ports ->
	8080 : dns local

	5000 : server
"""

sel = selectors.DefaultSelector()


def tcp_server_setup(server_address):
	lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	lsock.bind(server_address)
	lsock.listen()
	print("tcp server listening on", server_address)
	lsock.setblocking(False)
	sel.register(lsock, selectors.EVENT_READ, data=None)


def tcp_accept_connections(sock):
    conn, addr = sock.accept()  
    print("accepted connection from", addr)
    # Socket operando em modo não bloqueante
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def tcp_server_connection_handler(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) 
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("echoing", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  
            data.outb = data.outb[sent:]



def register_in_dns(dns_address): 
	udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	server_alias = "crp.server.teste" 
	# server_ip = socket.gethostbyname(socket.gethostname())
	data = "ADD " + server_alias

	try:
		print('sending {!r}'.format(data))
		sent = udpSocket.sendto(str(data).encode(),dns_address)

	finally:
		print('closing socket')
		udpSocket.close()

	# appear = False

	# server_alias = "crp.server.teste" 
	# server_ip = socket.gethostbyname(socket.gethostname())

	# data = (server_alias,server_ip)

	# with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
	# 	if not appear:
	# 		print ("Trying to apply a {}".format('UDP'))
	# 		print ("\tsocket family (AF_INET) : {},\n\tsocket type (SOCK_DGRAM): {},\n\tsocket protocol : {}".format(sock.family,sock.type,sock.proto))
	# 		appear = True

	# 	sock.sendto(str(data).encode(),dns_address)

	# pass


def help():
	print ("Try a valid transport protocol, like:\n --TCP (or --tcp) \n --UDP (or --udp)\n")
	print ("Exiting from server.")
	pass


def main():
	dns_address = ('localhost',8080)
	server_address = ('localhost',5000)
	assert len(sys.argv) == 2

	if sys.argv[1].lower() == "--udp" :
		##justfortst
		
		# register_in_dns(dns_address)

		sm = rdt.Rdt()

		sm.config_receiever(server_address)

		while True:
			data = sm.recv()
			print(data)

	elif sys.argv[1].lower() == "--tcp":
		tcp_server_setup(server_address)
		register_in_dns(dns_address)
		try:
			while True:
				events = sel.select(timeout=None)
				for key, mask in events:
					if key.data is None:
						tcp_accept_connections(key.fileobj)
					else:
						tcp_server_connection_handler(key, mask)
		except KeyboardInterrupt:
			print("keyboard interrupt, exiting...")
		finally:
			sel.close()
	else:
		help()
		raise NameError("You choose a invalid option")

	return 0


if __name__ == '__main__':
	main()