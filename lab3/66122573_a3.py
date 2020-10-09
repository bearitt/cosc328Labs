from socket import *
import sys
import time
import os
from os import path

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
        try:
            sock.connect((HOST,PORT))
            print('Client connected to server on port ' + str(PORT))
        except OSError:
            print('No connections available on that port!')
            return None
    return sock


def get(sock, filename, server_flag):
    # TODO: Figure out implementation
    directory = './server/' if server_flag else './client/'
    file_path = directory+filename
    destination = 'server' if not server_flag else 'client'
    if path.exists(file_path):
        if server_flag:
            sock.sendall('exists')
            response = ''
            while response!='y' or response!='n':
                response=sock.recv(1024).encode('utf-8')
        else:
            choice = ''
            while choice!='y' and choice!='n':
                choice = input(filename + ' already exists on the ' + destination + ', would you like to overwrite this file?').lower()
            if choice=='n':
                print('No file transferred')
                return
    try:
        data = sock.recv(1024)
        if data.decode('utf-8')=='NA':
            raise IOError
        elif data.decode('utf-8')=='ok':
            while True:
                data = sock.recv(1024)
                if data==None or data=='' or not data:
                    break

                with open(file_path,'ab') as f:
                    f.write(data)
            print(filename,'received from',destination)
        else:
            print('Nothing happened')
    except IOError:
        print('Error writing',filename,'to disk')

def put(sock, filename, server_flag):
    # TODO: Figure out implementation
    directory = './server/' if server_flag else './client/'
    file_path = directory+filename
    destination = 'server' if not server_flag else 'client'
    # TODO: Fix implementation for if file exists
    # hint: easy way would be to create a new file if it exists
    # why didn't i do it that way from the start...
    try:
        with open(file_path,'rb') as f:
            read_data = f.read()
            sock.sendall('ok'.encode('utf-8'))
            sock.sendall(read_data)
        print(filename,'uploaded to',destination)
    except FileNotFoundError:
        print('ERROR:',filename,'not found!')
        sock.sendall('NA'.encode('utf-8'))

def overwrite(sock, filename, destination,server_flag):
    if(server_flag):
        response = sock.recv(1024).decode('utf-8')
        if response=='exists':
            choice = input(filename + ' already exists on the ' + destination)
    else:
        print('poop')


def close(sock):
    # TODO: Is this all I need here?
    print('Connection closed')
    sock.close()

def quit():
    # TODO: Flesh this out
    print('Quit')
    sys.exit(0)

def server():
    try:
        os.makedirs('server', exist_ok=False)
        print('Server directory successfully created')
    except OSError:
        print('Server directory already exists')
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
        elif command == 'close' or command == 'quit':
            close(sock)
            quit()
        if command == 'get' or command == 'put':
            flag = data.split(' ',1)[1]
            if command == 'get':
                put(conn,flag,server_flag)
            elif command == 'put':
                get(conn,flag,server_flag)
    close(sock)
    quit()

def client():
    try:
        os.makedirs('client', exist_ok=False)
        print('Client directory successfully created')
    except OSError:
        print('Client directory already exists')
    server_flag = False
    command = ''
    connected = False
    sock = None
    commands = ['open','get','put','close','quit']
    # TODO: send command within functions instead of here
    while command.lower()!='quit':
        data = input('Please input command (type [HELP] for a list of commands): ')
        command = data.split(' ',1)[0].lower()
        if command not in commands:
            print('Invalid selection, please try again!')
            continue
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
            check = port_check(flag)
            if not check:
                print('Please input a numeric port between 1024 and 65535 inclusive')
                continue
            sock = open_conn(int(flag),False)
            connected = True if sock != None else False
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

def port_check(flag):
    port_range = range(1023)
    return flag.isdigit() and (flag not in port_range)

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
