import socket
from sys import argv
import argparse

parser = argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('port', type=int, help='This is the port to connect to the server on', action='store')
args = parser.parse_args(argv[1:])


class Hostname():
    def __init__(self, host, ip_address, flag):
        self.host = host
        self.ip_address = ip_address
        self.flag = flag


# create a list that saves the hostnames as objects
table = []
file = open("PROJI-DNSTS.txt", "r")
for line in file:
    host, ip, flag = line.split()
    host_name = Hostname(host, ip, flag)
    table.append(host_name)


# checks to see if hostname is in the DNS Table
def lookup(hostname):
    found = False
    for i in table:
        if i.host == hostname:
            found = True
            return f'{i.host} {i.ip_address} {i.flag}'
    if not found:
        return f'{hostname} - Error: HOST NOT FOUND'


try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    localhost_ip = (socket.gethostbyname(host))
    print('[S]: Server socket created')
    print('[S]: The host is {}'.format(host))
    print('[S]: Server IP address is {}'.format(localhost_ip))

except socket.error as err:
    print(f"[S]: Couldn't create socket due to {err}")
    exit()
SERVER = ('', args.port)
ss.bind(SERVER)
ss.listen(1)

connection, address = ss.accept()

with connection:
    while True:
        data = connection.recv(512)
        print(data)
        data = data.decode('utf-8')
        data = lookup(data)
        connection.sendall(data.encode('utf=8'))
ss.close()
exit()