from ..helpers import NEW_ENTITY, SERVER_IP, SERVER_PORT, TIMEOUT, INIT, KILL, RUN, LOG, SEND_MESSAGE, RECEIVE_MESSAGE
from ..client import Client
from ..world import World
from _thread import start_new_thread
import socket
import select
from threading import active_count
import time

def client_handler(function):
    def wrapper(self, client):
        def kill_client():
            client.valid = False
            client.disconnect()
            self.clients.pop(client)
        try:
            function(self, client)
        except socket.timeout:
            LOG.exception('Connection timeout.')
            kill_client()

        except (KeyboardInterrupt, ConnectionResetError, OSError, ValueError) as e:
            LOG.exception(e)
            kill_client()
            exit('Disconnected. Bye!')

        except BaseException as e:
            LOG.error('client_handler exception!')
            LOG.exception(e)
            kill_client()
            
    return wrapper


class Server:
    def __init__(self, ip=SERVER_IP, port=SERVER_PORT):
        self.socket = None
        self.ip = ip
        self.port = port

        self.clients = set()

        self.world = None

    def __str__(self):
        return str(f"PyMMO Server @ {self.ip}:{self.port}")

    def init_world(self, world_class=World):
        self.world = world_class()

    def start(self, retry=False):
        LOG.info(f'Starting up {self} ...')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

        start_new_thread(self.client_killer, (time.time(),))
        LOG.info('Server running! Waiting for clients...')
        while True:
            LOG.info(
                f'{len(self.clients)} clients are currently connected. Waiting for new client connections...')

            client_socket, client_address = self.socket.accept()
            LOG.info(f'Received connection request from:  {client_address}')
            new_client = Client(len(self.clients) + 1, client_socket)

            start_new_thread(self.add_client, (new_client,))
            
    def client_killer(self, init_time):
        while True:
            time.sleep(1)
            clients_to_remove = []
            for client in self.clients:
                if 'socket.socket [closed]' in str(client.socket):
                    LOG.error(f'{client.id} socket is closed. Removing from server...')
                    clients_to_remove.append(client)
            
            for client_to_be_removed in clients_to_remove:
                self.clients.remove(client_to_be_removed)
                LOG.error(f'{client_to_be_removed.id} removed from server.')
                
                
                
            print((time.time() - init_time), active_count(), len(self.clients))

    def stop(self):
        for client in self.clients:
            try:
                client.disconnect()
            except:
                LOG.exception(f'Found issue with: {client}')

        self.socket.close()
        LOG.info('Server Manually Disconnected.')

    def add_client(self, client):
        while not client.valid:
            self.init_client(client)

        LOG.info(f'Validated. Adding client to server {self}...')
        self.clients.add(client)

        LOG.info(f'Added. Now running client {client}...')

        while client.valid:
            self.update_client(client)

    @client_handler
    def init_client(self, client):
        ready_sockets, _, _ = select.select([client.socket], [], [],
                                            TIMEOUT)
        if ready_sockets:
            received_message = RECEIVE_MESSAGE(client.socket)

            if received_message == INIT:
                client.valid = True
                LOG.info('Connection validated. Confirming...')
                SEND_MESSAGE(client.socket, RUN)
                self.update_world(NEW_ENTITY)
                SEND_MESSAGE(client.socket, self.world)

            elif received_message:
                LOG.info(
                    f'Server Received during Init Client: {received_message}')

    @client_handler
    def update_client(self, client):
        ready_sockets, _, _ = select.select([client.socket], [], [],
                                            TIMEOUT)

        if ready_sockets:
            received_message = RECEIVE_MESSAGE(client.socket)

            if received_message == KILL:
                client.valid = False
                client.disconnect()
                exit(f'Client {client} disconnected via KILL command.')

            else:
                LOG.info(
                    f'Received update from client {client}: {received_message}')
                self.update_world(received_message)

                LOG.info(f'Sending latest world to client {client}.')
                SEND_MESSAGE(client.socket, self.world)
                LOG.info('Sent latest world to client.')
            
    def update_world(self, message):
        LOG.info('Updating server world...')
        self.world.update(message)
        LOG.info('World has been updated. Summary:')
        LOG.info(self.world)
        return True
