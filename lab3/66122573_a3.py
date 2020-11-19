from socket import *
import sys
import time
import os
from os import path

# Prompt user for client or server selection, call appropriate method
def main():
    machine = ''
    while machine.lower()!='client' and machine.lower()!='server':
        machine = input('Are you connecting as a client or as a server? ')
    server_flag = machine.lower()=='server'
    if(server_flag):
        server()
    else:
        client()

# Open connection on specified port
# Different execution based on whether server or client calls function
def open_conn(PORT,server_flag):
    HOST = '127.0.0.1'
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        if(server_flag):
            sock.bind((HOST,PORT))
            print('Server listening on port ' + str(PORT))
            sock.listen()
        else:
            sock.connect((HOST,PORT))
            print('Client connected to server on port ' + str(PORT))
    except OSError:
        print('No connections available on that port!')
        return None
    except PermissionError:
        print('Connections not allowed on that port, try another one.')
        return None
    return sock

# Get filename, called by side receiving file
# If called by client, sends get message to server
def get(sock, filename, server_flag):
    if not server_flag:
        data = 'get ' + filename
        sock.sendall(data.encode('utf-8'))
    # Specify file path to save file to
    directory = './server/' if server_flag else './client/'
    file_path = directory+filename
    destination = 'server' if not server_flag else 'client'
    # Check to see if file exists on receiving machine. Adds a postscript
    # number if the file does exist
    while path.exists(file_path):
        new_file = file_path.split('/')[-1]
        print('File',new_file,'already exists')
        suffix = new_file.split('-')[-1]
        file_number = suffix.split('.')[0]
        if file_number.isdigit():
            file_number = int(file_number) + 1
        else:
            file_number = 1
        file_path = directory+filename.split('.')[0]+'-'+str(file_number)+'.'+filename.split('.')[-1]
    try:
        print('Receiving',filename,'from',destination)
        # Look for acknowledgment message from source machine
        data = sock.recv(1024)
        if data.decode('utf-8')=='NA':
            raise IOError
        elif data.decode('utf-8')=='ok':
            file_size = int(sock.recv(1024).decode('utf-8'))
            count = 0
            while data:
                # Receives data until EOF then breaks loop
                if count>int(file_size/1024):
                    break
                count += 1
                data = sock.recv(1024)
                if not data:
                    break
                with open(file_path,'ab') as f:
                    f.write(data)
            print(filename,'received from',destination)
        else:
            print('Nothing happened')
    except IOError:
        print('Error writing',filename,'to disk')

# Sends [filename] to machine making request
# If called by client, sends message to server
def put(sock, filename, server_flag):
    if not server_flag:
        data = 'put ' + filename
        sock.sendall(data.encode('utf-8'))
    # Specify path of file to send
    directory = './server/' if server_flag else './client/'
    file_path = directory+filename
    destination = 'server' if not server_flag else 'client'
    try:
        print('Sending',filename,'to',destination)
        with open(file_path,'rb') as f:
            read_data = f.read()
            # Acknowledgment message sent
            sock.sendall('ok'.encode('utf-8'))
            # Send filesize
            sock.sendall(str(os.stat(file_path).st_size).encode('utf-8'))
            # Send data
            sock.sendall(read_data)
        print(filename,'uploaded to',destination)
    except FileNotFoundError:
        print('ERROR:',filename,'not found!')
        sock.sendall('NA'.encode('utf-8'))

# Close connection on [sock]
def close(sock):
    print('Connection closed')
    sock.close()

# Quit application
def quit():
    print('Disconnecting from FTP application, thank you!')
    sys.exit(0)

# Driver function for server behaviour
def server():
    # Make directory 'server' if it doesn't exist
    try:
        os.makedirs('server', exist_ok=False)
        print('Server directory successfully created')
    except OSError:
        print('Server directory already exists')
    server_flag = True
    sock = None
    # Obtain connection
    while sock == None:
        command = ''
        while command.lower()!='open':
            data = input('Type [open] [PORT] to open a connection on port [PORT]: ')
            command = data.split(' ',1)[0]
            try:
                PORT = int(data.split(' ',1)[1])
            except IndexError:
                print('Remember to supply a port number after [open]')
            except ValueError:
                print('Please use a numeric port number after [open]')
        sock = open_conn(PORT,server_flag)
    conn, addr = sock.accept()
    print('Connected to ', addr)
    # Receive commands from client after making connection
    while(True):
        data = conn.recv(1024).decode("utf-8").lower()
        print('client:',data)
        command = data.split(' ', 1)[0]
        if command == 'close' or command == 'quit':
            close(sock)
            quit()
        if command == 'get' or command == 'put':
            flag = data.split(' ',1)[1]
            if command == 'get':
                put(conn,flag,server_flag)
            elif command == 'put':
                get(conn,flag,server_flag)
    # Close server connection after client disconnects (I wasn't sure if
    # this was a good way to disconnect, obviously this isn't how a server
    # would work in an actual production environment)
    close(sock)
    quit()
# Driver function for client behaviour
def client():
    # Make directory 'client' if it doesn't exist
    try:
        os.makedirs('client', exist_ok=False)
        print('Client directory successfully created')
    except OSError:
        print('Client directory already exists')
    server_flag = False
    command = ''
    connected = False
    sock = None
    commands = ['open','get','put','close','quit','help']
    # Obtain command and flag from the user (e.g. 'open 8080')
    while command.lower()!='quit':
        data = input('Please input command (type [HELP] for a list of commands): ')
        command = data.split(' ',1)[0].lower()
        if command not in commands:
            print('Invalid selection, please try again!')
            continue

        if command.lower()=='help':
            help()
        elif command.lower()=='quit':
            if connected:
                sock.sendall(command.encode('utf-8'))
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
                sock.sendall(command.encode('utf-8'))
                close(sock)
            else:
                flag = data.split(' ',1)[1].lower()
                if command.lower()=='get':
                    get(sock,flag,server_flag)
                elif command.lower()=='put':
                    put(sock,flag,server_flag)
        elif not connected:
            print('You must connect to a server before using ',command)

# Check if supplied port is a digit and within the range
def port_check(flag):
    port_range = range(1023,65535)
    return flag.isdigit() and (flag not in port_range)

# Print out a list of commands for the user
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
