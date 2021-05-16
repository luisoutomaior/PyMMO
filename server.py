import socket
import select
from macros import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Starting up server...')
s.bind(('127.0.0.1', 12345))
s.listen(5)

print('Done! Now listening...')
while True:
    clientsocket, address = s.accept()
    print('Connection has been established with: ', address)
    string = "Welcome :)"
    clientsocket.send(string)

    ready_sockets, _, _ = select.select([clientsocket], [], [], SERVER_TIMEOUT)

    if ready_sockets:
        data = clientsocket.recv(1024)
        print('received:', data)
    else:
        print('No data')