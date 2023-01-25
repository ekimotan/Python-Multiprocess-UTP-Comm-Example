import socket
import netifaces as ni

def sendDataPrimary(message):
    UDP_IP = ni.ifaddresses('lo')[ni.AF_INET][0]['addr']
    UDP_PORT = 10000

    MESSAGE = message.encode()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def readDataPrimary():

    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000
    try:
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))
    except:
        pass

    while True:
        data, addr = sock.recvfrom(1024)
        incoming = data.decode()
        if incoming:
            print("Received")
            sendDataPrimary(incoming)
            print(f"{incoming} sent")

if __name__ == '__main__':
    sendDataPrimary("Secondary")
    readDataPrimary()