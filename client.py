import dns
import sys
import socket
import rdt
import library
import selectors
import types

# Selectors -> allows high-level and efficient I/O multiplexing
sel = selectors.DefaultSelector()

# Message to send
message = [b"Hello from client."]


def tcp_start_connections(server_address, connid):
    server_addr = (server_address)
    print("starting connection", connid, "to", server_addr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    # Notify if client connection is ready for read or write
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        connid=connid,
        msg_total=len(message),
        recv_total=0,
        messages=list(message),
        outb=b"",
    )
    sel.register(sock, events, data=data)


def tcp_client_connection_handler(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  
        if recv_data:
            print("received", repr(recv_data), "from connection", data.connid)
            data.recv_total += len(recv_data)
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print("sending", repr(data.outb), "to connection", data.connid)
            sent = sock.send(data.outb) 
            data.outb = data.outb[sent:]


def get_ip_from_dns(addrDomain = "crp.server.teste", dns_address = ('192.168.0.23', 8080)):

    print("pegando ip do server")
    # client_ip = socket.gethostbyname(socket.gethostname())
    # msg = "FIND " + addrDomain
    
    # udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # udpSocket.bind((socket.gethostname(), 9090)) #9090 é a porta do client
    # udpSocket.sendto(str(msg).encode(), dns_addr)
    
    # data, dns_addr = udpSocket.recvfrom(1024)
    # print(data.decode())
    # return data.decode()

    data = "FIND " + addrDomain

    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        print('sending {!r}'.format(data))
        udpSocket.sendto(str(data).encode(),dns_address)

        data, _ = udpSocket.recvfrom(1024)
        # print(data.decode())
        # print(address)
    finally:
        print('closing socket')
        udpSocket.close()
    
    return data.decode()
    
    


def main():
    assert len(sys.argv) == 2

    server_ip = get_ip_from_dns(dns_address=('192.168.0.23',8080))
    print("server ip: ", server_ip)
    sm = rdt.Rdt()
    ip_port = (server_ip, 9090)

    print("to aq")
    library.Library(sm, ip_port, sys.argv[1].lower())
    library.mainloop()
    #dns_address = ('localhost',8080)

    # server_ip = get_ip_from_dns(ipServer, dns_address)
    # print('server ip =',server_ip)
    # server_address = (server_ip,5000)

    # if sys.argv[1].lower() == "--udp":
    #     sm = rdt.Rdt()
    #     sm.config_transmitter(server_address)

    #     sm.send({232:"meme"})
    # elif sys.argv[1].lower() == "--tcp":
    #     num_conns = 1
    #     for conn_id in range(num_conns):
    #         tcp_start_connections(server_address, conn_id+1)

    #     try:
    #         while True:
    #             events = sel.select(timeout=1)
    #             if events:
    #                 for key, mask in events:
    #                     tcp_client_connection_handler(key, mask)
    #             if not sel.get_map():
    #                 break
    #     except KeyboardInterrupt:
    #         print("keyboard interrupt, exiting...")
    #     finally:
    #         sel.close()
                

if __name__ == "__main__":
    main()