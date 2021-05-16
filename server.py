import socket
import select
from macros import *
import time
import pickle
import traceback
from _thread import *
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Starting up server...')
s.bind(('127.0.0.1', SERVER_PORT))
s.listen(2)

 
print('Done! Now listening...')
status = {'working': True, 'players': [], 'enemies': []}


def threaded_client(conn, status):
    while True:
        print(status)
        # now = time.time()
        # message = bytes(f'Connected. Server time: {now}', "utf-8")
        conn.send(pickle.dumps(status))
        ready_sockets, _, _ = select.select([conn], [], [], SERVER_TIMEOUT)
        if ready_sockets:
                response = pickle.loads(conn.recv(1024))
                try:

                    if 'movement' in response['command']:
                        for player in status['players']:
                            if player['id'] == response['id']:
                                player['pos'] = response['pos']
                                
                    elif 'damage' in response['command']:
                        print('\nreceived:', response)
                        for enemy in status['enemies']:
                            if enemy['id'] == response['hitted']['id']:
                                enemy['stats']['hp'] = response['hitted']['stats']['hp']
                                
                            print('new enemy', enemy)
                        
                except:
                    traceback.print_exc()
    


n_players = 0
while True:
    client, address = s.accept()
    conn_time = time.time()
    n_players += 1

    print(f'Connection has been established with: {address} at {conn_time}. Welcome :)')

    id = str(n_players)
    status['players'].append({'id': id, 'pos': (WIDTH/2, HEIGHT/2), 'stats': INIT_STATS()})
    status['enemies'].append({'id': id, 'pos': (np.random.randint(WIDTH), np.random.randint(HEIGHT)), 'stats': INIT_STATS()})
    
    client.send(pickle.dumps(id))
    
    try:
        start_new_thread(threaded_client, (client, status))
    except BaseException as e:
        print('Server Exception:', e)
        traceback.print_exc()
        
