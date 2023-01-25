import ctypes
import socket
import netifaces as ni
import time
import multiprocessing

def main():
    error_secondary_counter = 0
    start = 0
    secondaryAlive.value = False
    print(f"secondaryAlive.value:{secondaryAlive.value}")
    reading1process = multiprocessing.Process(target=readDataSecondary, args=(secondaryAlive,))
    reading1process.start()
    while not secondaryAlive.value:
        print(f"secondaryAlive.value while:{secondaryAlive.value}")
        if start == 0:
            time.sleep(1)
            sendDataSecondary()
        time.sleep(0.2)
        start = 1
        error_secondary_counter = +1
        if error_secondary_counter > 45:
            start = 0
            print("Connection to secondary failed")

    reading1process.join()
    print("reading joined")
    main()


def sendDataSecondary():
    UDP_IP = ni.ifaddresses('lo')[ni.AF_INET][0]['addr']
    UDP_PORT = 5000

    MESSAGE = b"123"
    print("Message sent")
    # MESSAGE = b'Foto'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def readDataSecondary(secondaryAlive):

    UDP_IP = "127.0.0.1"
    UDP_PORT = 10000
    try:
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))
    except:
        pass

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        incoming_message = data.decode()
        if incoming_message:
            print(f"incoming message: {incoming_message}")
            secondaryAlive.value = True
            return

secondaryAlive = multiprocessing.Value(ctypes.c_bool, False)
p = multiprocessing.Process(target=main)
p.start()
p.join()
print("End")