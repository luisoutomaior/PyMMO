import socket
import select
from macros import *
import time
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Starting up server...')
s.bind(('127.0.0.1', SERVER_PORT))
s.listen(5)

print('Done! Now listening...')
while True:
    clientsocket, address = s.accept()
    conn_time = time.time()
    message = f'Connection has been established with: {address} at {conn_time}. Welcome :)'
    print('Sending:', message)
    clientsocket.send(pickle.dumps(message))

    while True:
        now = time.time()
        message = bytes(f'Connected. Server time: {now}', "utf-8")
        clientsocket.send(pickle.dumps(message))
        
        status = {'working': True}
        clientsocket.send(pickle.dumps(status))
        
        ready_sockets, _, _ = select.select(
            [clientsocket], [], [], SERVER_TIMEOUT)

        if ready_sockets:
            data = pickle.loads(clientsocket.recv(1024))
            print('received:', data)
        else:
            pass
