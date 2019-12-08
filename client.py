import dns
import sys
import socket
import rdt
import library

def get_ip_from_dns(addrDomain = "crp.server.teste", dns_addr = ("localhost", 8080)):

    print("pegando ip do server")
    client_ip = socket.gethostbyname(socket.gethostname())
    msg = "FIND " + addrDomain
    
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.bind((socket.gethostname(), 9090)) #9090 é a porta do client
    udpSocket.sendto(str(msg).encode(), dns_addr)
    
    data, dns_addr = udpSocket.recvfrom(1024)
    print(data.decode())
    return data.decode()

def main():
    assert len(sys.argv) == 2
    #addrServer = input("Insira o endereço de domínio hospedeiro desejado: ")

    ipServer = get_ip_from_dns()
    sm = rdt.Rdt()
    ip_port = (ipServer, 5000)

    print("to aq")
    library.Library(sm, ip_port, sys.argv[1].lower())
    library.mainloop()

if __name__ == "__main__":
    main()