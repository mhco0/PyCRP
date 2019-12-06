import dns
import sys
import socket

def get_ip_from_dns(addrDomain = "crp.server.teste", dns_addr = ("localhost", 8080)):

    client_ip = socket.gethostbyname(socket.gethostname())
    msg = "FIND " + addrDomain

    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.bind((socket.gethostname(), 9090))
    udpSocket.sendto(str(msg).encode(), dns_addr)
    
    data, address = udpSocket.recvfrom(1024)
    print(data.decode())

    pass

def main():
    assert len(sys.argv) == 2
    addrServer = input("Insira o endereço de domínio hospedeiro desejado: ")

    ipServer = get_ip_from_dns()

    if sys.argv[1].lower() == "--udp":
        pass
       # sm = rdt.Rdt_3_0()
       # sm.config_client()
    elif sys.argv[1].lower() == "--tcp":
        pass

    return 0

if __name__ == "__main__":
    main()