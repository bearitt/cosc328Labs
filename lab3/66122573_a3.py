from socket import *
import sys
import time

FILE_TRANSFER_PORT = 65535

def main():
    machine = ''
    while machine.lower()!='client' and machine.lower()!='server':
        machine = input('Are you connecting as a client or as a server? ')
    server_flag = machine.lower()=='server'
    # TODO: Maybe flesh this out?
    if(server_flag):
        server()
    else:
        client()

def open_conn(PORT,server):
    HOST = '127.0.0.1'
    sock = socket(AF_INET, SOCK_STREAM)
    if(server):
        sock.bind((HOST,PORT))
        print('Server listening on port ' + str(PORT))
        sock.listen()
    else:
        print('Client connected to server on port ' + str(PORT))
        sock.connect((HOST,PORT))
    return sock


def get(sock, filename, server_flag):
    # TODO: Figure out implementation
    print('Get',filename)
    directory = './server/' if server_flag else './client/'
    path = directory+filename
    file_sock = open_conn(FILE_TRANSFER_PORT,True)
    print(path)
    while True:
        if file_sock.recv(1024).decode('utf-8') == 'start':
            try:
                with open(path,'wb') as f:
                    data = file_sock.recv(1024)
                    if data.decode('utf-8')=='quit':
                        close(file_sock)
                        break
                    else:
                        read_data = f.write(data.decode())
            except IOError:
                print('Error writing',filename,'to disk')
                break

def put(sock, filename, server_flag):
    # TODO: Figure out implementation
    print('Put',filename)
    directory = './server/' if server_flag else './client/'
    path = directory+filename
    file_sock = open_conn(FILE_TRANSFER_PORT,False)
    print(path)
    try:
        file_sock.sendall('start'.encode('utf-8'))
        with open(path,'rb') as f:
            read_data = f.read()
            file_sock.sendall(read_data.encode())
    except FileNotFoundError:
        print('ERROR:',filename,'not found!')
    finally:
        file_sock.sendall('quit'.encode('utf-8'))
        close(file_sock)

def close(sock):
    # TODO: Is this all I need here?
    print('Connection closed')
    sock.close()

def quit():
    # TODO: Flesh this out
    print('Quit')
    sys.exit(0)

def server():
    server_flag = True
    command = ''
    while command.lower()!='open':
        data = input('Type [open] [PORT] to open a connection on port [PORT]: ')
        command = data.split(' ',1)[0]
        PORT = int(data.split(' ',1)[1])
    sock = open_conn(PORT,server_flag)
    conn, addr = sock.accept()
    print('Connected to ', addr)
    while(True):
        # TODO: figure out how to receive a filestream
        data = conn.recv(1024).decode("utf-8").lower()
        print(data)
        command = data.split(' ', 1)[0]
        if command == 'open' or command == 'help':
            continue
        elif command == 'close':
            close(sock)
            quit()
        if command == 'get' or command == 'put':
            flag = data.split(' ',1)[1]
            if command == 'get':
                put(sock,flag,server_flag)
            elif command == 'put':
                get(sock,flag,server_flag)
    close(sock)
    quit()

def client():
    server_flag = False
    command = ''
    connected = False
    sock = None
    while command.lower()!='quit':
        data = input('Please input command (type [HELP] for a list of commands): ')
        command = data.split(' ',1)[0].lower()

        if connected:
            sock.sendall(data.encode('utf-8'))

        if command.lower()=='help':
            help()
        elif command.lower()=='quit':
            if connected:
                close(sock)
            quit()
        elif command.lower()=='open':
            flag = data.split(' ',1)[1].lower()
            connected = True
            sock = open_conn(int(flag),False)
        elif connected:
            if command.lower()=='close':
                connected = False
                close(sock)
            else:
                flag = data.split(' ',1)[1].lower()
                if command.lower()=='get':
                    get(sock,flag,server_flag)
                elif command.lower()=='put':
                    put(sock,flag,server_flag)
        elif not connected:
            print('You must connect to a server before using ',command)
        else:
            print('Invalid selection, try again!')

def help():
    print('''
1. open [PORT]: Opens a connection on port number [PORT]
2. get [filename]: Requests a file named [filename] from the server.
3. put [filename]: Sends a file named [filename] to the server.
4. close: Closes connection to current server.
5. quit: Exits the program.
    '''
    )

if __name__ == "__main__":
    main()
