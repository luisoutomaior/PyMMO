import socket
import select

from pygame import sprite
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
status = {'working': True, 'entities': []}




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
                    for received_command in response['commands']:
                        if 'movement' in received_command:
                            received_entity = received_command['movement']
                            for entity in status['entities']:
                                if entity.id == received_entity.id:
                                    entity.update_position(received_entity)

                        if 'animation' in received_command:
                            received_entity = received_command['animation']
                            for entity in status['entities']:
                                if entity.id == received_entity.id:
                                    entity.update_animation(received_entity)

                        if 'speak' in received_command:
                            received_entity = received_command['speak']
                            for entity in status['entities']:
                                if entity.id == received_entity.id:
                                    entity.update_speech(received_entity)

                        if 'damage' in received_command:
                            received_command = received_command['damage']
                            for entity in status['entities']:
                                if entity.id == received_command['hitted'].id:
                                    entity.update_stats(received_command['hitted'])
                                    if received_command['hitted'].stats['alive'] == False:
                                        status['entities'].remove(entity)

                    # print('new status:')
                    # print(status)

            except Exception as e:
                traceback.print_exc()

        # if not status_update:
        conn.send(pickle.dumps(status))

        print(str(np.random.random()) + '\t' + (str(status_update)))


n_players = 0
clients = set()

while True:
    try:
        client, address = s.accept()

        clients.add(client)
        conn_time = time.time()
        n_players += 1

        print(
            f'Connection has been established with: {address} at {conn_time}. Welcome :)')

        id = str(n_players)
        status['entities'].append(Entity(id=id,
                                         kind='player',
                                         pos=(WIDTH/2, HEIGHT/2)))

        # status['entities'].append(Entity(id=id,
        #                                  kind='enemy-gren',
        #                                  pos=(np.random.randint(WIDTH // 2 - WIDTH // 4, WIDTH // 2 + WIDTH // 4),
        #                                       np.random.randint(HEIGHT // 2 - HEIGHT // 4, HEIGHT // 2 + HEIGHT // 4))))

        client.send(pickle.dumps(id))
        try:
            start_new_thread(threaded_client, (client, status))
        except BaseException as e:
            print('Server Exception:', e)
            traceback.print_exc()

    except KeyboardInterrupt:
        s.close()
        exit()
