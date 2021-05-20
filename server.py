import socket
import select
from macros import *
import time
import _pickle as pickle

import traceback
from _thread import *
import numpy as np
from pprint import pprint as print

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Starting up server...')
s.bind(('127.0.0.1', SERVER_PORT))
s.listen(10)

 
print('Done! Now listening...')
status = {'working': True, 'players': [], 'enemies': []}


def threaded_client(conn, status):

    while True:
        status_update = False    
        ready_sockets, _, _ = select.select([conn], [], [], SERVER_TIMEOUT)
        if ready_sockets:
                try:
                    response = pickle.loads(conn.recv(PACKET_SIZE))
                    if 'commands' in response:
                        # print('old status:')
                        # print(status)
                        # print('received:')
                        # print(response)
                        for command in response['commands']:
                            if 'movement' in command:
                                command = command['movement']
                                for player in status['players']:
                                    if player['id'] == command['id']:
                                        player['pos'] = command['pos']
                                        player['dir'] = command['dir']
                                        
                            if 'animation' in command:
                                command = command['animation']
                                for player in status['players']:
                                    if player['id'] == command['id']:
                                        player['stats']['animating'] = command['stats']['animating']
                                        player['stats']['foreground_loc'] = command['stats']['foreground_loc']
                                        player['stats']['foreground_idx'] = command['stats']['foreground_idx']

                            if 'speak' in command:
                                command = command['speak']
                                for player in status['players']:
                                    if player['id'] == command['id']:
                                        player['stats']['text'] = command['stats']['text']
                                        player['stats']['speaking'] = command['stats']['speaking']
                                        player['stats']['speaking_time'] = command['stats']['speaking_time']

                                    if player['stats']['speaking_time'] <= 0:
                                        player['stats']['speaking_time'] = DEFAULT_CHAT_TIME
                                        
                                        if player['stats']['speaking']:
                                            player['stats']['text'] = ''
                                            player['stats']['speaking'] = False
                                        
                                        
                            if 'damage' in command:
                                command = command['damage']
                                if 'to-enemy' in command['type']:
                                    for enemy in status['enemies']:
                                        if enemy['id'] == command['hitted']['id']:
                                            enemy['stats']['hp'] = command['hitted']['stats']['hp']
                                            
                                            if command['hitted']['stats']['alive'] == False:
                                                status['enemies'].remove(enemy)
                                        
                                if 'to-player' in command['type']:
                                    for player in status['players']:
                                        if player['id'] == command['hitted']['id']:
                                            player['stats']['hp'] = command['hitted']['stats']['hp']
                                            
                                            if command['hitted']['stats']['alive'] == False:
                                                status['players'].remove(player)

                        # print('new status:')
                        # print(status)
                        
                except Exception as e:
                    
                    traceback.print_exc()
        
        # if not status_update:
        conn.send(pickle.dumps(status))

        print(str(np.random.random()) + '\t'+ (str(status_update)))


n_players = 0
clients = set()

while True:
    try:
        client, address = s.accept()
        
        clients.add(client)
        conn_time = time.time()
        n_players += 1

        print(f'Connection has been established with: {address} at {conn_time}. Welcome :)')

        id = str(n_players)
        status['players'].append({'id': id, 'kind': 'player', 'pos': (WIDTH/2, HEIGHT/2), 'dir': RIGHT, 'stats': INIT_STATS()})
        status['enemies'].append({'id': id, 'kind': 'gren', 'dir': LEFT, 'pos': (np.random.randint( WIDTH // 2 - WIDTH // 4, WIDTH // 2  + WIDTH // 4), np.random.randint(HEIGHT // 2 - HEIGHT // 4, HEIGHT // 2  + HEIGHT // 4)), 'stats': INIT_STATS()})
        
        client.send(pickle.dumps(id))
        
        try:
            start_new_thread(threaded_client, (client, status))
        except BaseException as e:
            print('Server Exception:', e)
            traceback.print_exc()
            
            
    except KeyboardInterrupt:
        s.close()
        exit()
        
            