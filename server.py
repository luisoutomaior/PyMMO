import socket
import select
from macros import *
import time
import pickle
import traceback
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Starting up server...')
s.bind(('127.0.0.1', SERVER_PORT))
s.listen(2)

 
print('Done! Now listening...')
status = {'working': True, 'players': [], 'enemies': []}


def threaded_client(conn, status):
    while True:
        # now = time.time()
        # message = bytes(f'Connected. Server time: {now}', "utf-8")
        conn.send(pickle.dumps(status))
        ready_sockets, _, _ = select.select([conn], [], [], SERVER_TIMEOUT)
        if ready_sockets:
                response = pickle.loads(conn.recv(1024))
                print('received:', response)
                try:
                    print(status['players'])

                    for player in status['players']:
                        if player['id'] == response['id']:
                            player['pos'] = response['pos']
                except:
                    pass
    


n_players = 0
while True:
    client, address = s.accept()
    conn_time = time.time()
    n_players += 1

    print(f'Connection has been established with: {address} at {conn_time}. Welcome :)')

    id = str(n_players)
    status['players'].append({'id': id, 'pos': (WIDTH/2, HEIGHT/2)})
    status['enemies'].append({'id': id, 'pos': (0, 0)})
    
    client.send(pickle.dumps(id))
    
    try:
        start_new_thread(threaded_client, (client, status))
    except BaseException as e:
        print('Server Exception:', e)
        traceback.print_exc()
        
