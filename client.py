import dns
import sys
import socket
import library


def get_ip_from_dns(addrDomain = "crp.server.teste", dns_address = ("localhost", 8080)):

    print("pegando ip do server")
    data = "FIND " + addrDomain

    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        print('sending {!r}'.format(data))
        udpSocket.sendto(str(data).encode(),dns_address)

        data, _ = udpSocket.recvfrom(1024)
    finally:
        print('closing socket')
        udpSocket.close()
    
    return data.decode()
    
    


def main():
    assert len(sys.argv) == 2

    server_ip = get_ip_from_dns()
    print("server ip: ", server_ip)
    server_adress = (server_ip, 5000)

    library.Library(server_adress, sys.argv[1].lower())
    library.mainloop()
                

if __name__ == "__main__":
    main()