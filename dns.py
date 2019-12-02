import socket
import sys

def main():

    dnsHost = 'localhost'
    dnsPort = 8080

    dnsSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dnsSocket.bind((dnsHost,dnsPort))
    print ("DNS local started")

if __name__ == "__main__" :
    main()
