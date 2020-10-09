from socket import *
HOST = '127.0.0.1'
PORT = 12000
sock = socket(AF_INET,SOCK_STREAM)
sock.connect((HOST,PORT))

while(True):
    s = input("Message: ")
    sock.sendall(s.encode("utf-8"))
    data = sock.recv(1024).decode("utf-8")
    if data == "QUIT":
        break
    print("Received: ", data)
sock.close()
