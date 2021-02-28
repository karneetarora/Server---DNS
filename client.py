import argparse
from sys import argv
import socket

# First we use the argparse package to parse the arguments
parser = argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('-f', type=str, help='This is the source file for hostnames', default='PROJI-HNS.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the output file with Results', default='RESOLVED.txt',action='store', dest='out_file')
parser.add_argument('rshost_name', type=str, help='The host name',action='store')
parser.add_argument('rsListen_port', type=int, help='RS Listen Port',action='store')
parser.add_argument('tsListen_port', type=int, help='TS Listen Port',action='store')

args = parser.parse_args(argv[1:])

# next we create a client socket
try:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

# second socket
try:
    client_sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket 2 created")
except socket.error as err:
    print('socket 2 open error: {} \n'.format(err))
    exit()

server_addr = (args.rshost_name, args.rsListen_port)
client_sock.connect(server_addr)


# now we need to open both files
with open(args.out_file, 'w') as write_file:
    for line in open(args.in_file, 'r'):
        # trim the line to avoid weird new line things
        line = line.strip()
        # now we write whatever the server tells us to the out_file
        if line:
            client_sock.sendall(line.encode('utf-8'))
            answer = client_sock.recv(512)

            # decode answer
            answer = answer.decode('utf-8')

            # if hostname wasn't found in RS, string needs to be sent to TS
            if 'NS' in answer:
                server_addr2 = (args.rshost_name, args.tsListen_port)
                try:
                    client_sock2.connect(server_addr2)
                    client_sock2.sendall(line.encode('utf-8'))
                except:
                    client_sock2.sendall(line.encode('utf-8'))
                answer = client_sock2.recv(512)
                answer = answer.decode('utf-8')
                pass

            write_file.write(answer + '\n')


# close the socket (note this will be visible to the other side)
client_sock.close()

for line in open(args.out_file, 'r+'):
    if 'NS' in line:
        line = 'Replace'
    print(line)