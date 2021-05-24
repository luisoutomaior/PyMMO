from ..helpers import KILL_ENTITY, NEW_ENTITY, SERVER_IP, SERVER_PORT, TIMEOUT, INIT, KILL, RUN, LOG, SEND_MESSAGE, RECEIVE_MESSAGE
from ..client import Client
from ..world import World
from _thread import start_new_thread
import socket
import select
from threading import active_count
import time


def client_exception_handler(function):
    """Decorator for handling client exceptions

    Args:
        function: Server method
    """

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
            kill_client()
            exit('Disconnected. Bye!')

        except BaseException as e:
            LOG.error('client_handler exception!')
            LOG.exception(e)
            kill_client()

    return wrapper


class Server:
    """Server class that implements handling new clients, 
    communication of World between server and client, etc.
    """

    def __init__(self, world=World, ip=SERVER_IP, port=SERVER_PORT):
        self.socket = None
        self.ip = ip
        self.port = port
        self.world = world
        self.clients = set()

    def __str__(self):
        return str(f"PyMMO Server @ {self.ip}:{self.port}")

    def init_world(self, world_class=World):
        """Initialize the server-side World instance

        Args:
            world_class (World, optional): World class to intialize the server with. Defaults to World.
        """
        self.world = world_class()

    def start(self, retry=False):
        LOG.info(f'Starting up {self} ...')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

        start_new_thread(self.server_maintainer, ())
        LOG.info('Server running! Waiting for clients...')
        while True:
            LOG.info(
                f'{len(self.clients)} clients are currently connected. Waiting for new client connections...')

            client_socket, client_address = self.socket.accept()
            LOG.info(f'Received connection request from:  {client_address}')
            new_client = Client(len(self.clients) + 1, client_socket)

            start_new_thread(self.add_client, (new_client,))

    def server_maintainer(self):
        """Searches for issues in clients and removes them accordingly
        """
        init_time = time.time()
        while True:
            try:
                time.sleep(1)
                clients_to_remove = []
                for client in self.clients:
                    if 'socket.socket [closed]' in str(client.socket):
                        LOG.error(
                            f'{client.id} socket is closed. Removing from server...')
                        clients_to_remove.append(client)

                for client_to_be_removed in clients_to_remove:
                    self.remove_client(client_to_be_removed)

                print((time.time() - init_time),
                      active_count(), len(self.clients))
            except BaseException as e:
                LOG.exception(e)

    def stop(self):
        """Stops server and removes all clients

        """
        for client in self.clients:
            self.remove_client(client)

        self.socket.close()
        LOG.info('Server Manually Disconnected.')

    def add_client(self, client):
        """Adds new client to server

        Args:
            client (Client): new client to be added
        """
        while not client.valid:
            self.init_client(client)

        LOG.info(f'Validated. Adding client to server {self}...')
        self.clients.add(client)

        LOG.info(f'Added. Now running client {client}...')

        while client.valid:
            self.update_client(client)

    def remove_client(self, client, reason=None):
        """Removes client from server

        Args:
            client (Client): client to be removed from server
        """
        try:
            self.clients.remove(client)
            LOG.error(
                f'Client removed from server (reason: {reason}): {client}')
            client.valid = False
            client.disconnect()
            self.update_world({KILL_ENTITY: client.id})
        except:
            LOG.exception(f'Found issue while removing: {client}')

    @client_exception_handler
    def init_client(self, client):
        """Initialize client instance and update their World with most recent one

        Args:
            client (Client): client to be initialized
        """
        ready_sockets, _, _ = select.select([client.socket], [], [],
                                            TIMEOUT)
        if ready_sockets:
            received_message = RECEIVE_MESSAGE(client.socket)

            if received_message == INIT:
                client.valid = True
                LOG.info('Connection validated. Confirming...')
                SEND_MESSAGE(client.socket, RUN)
                self.update_world({NEW_ENTITY: client.id})
                SEND_MESSAGE(client.socket, self.world)

    @client_exception_handler
    def update_client(self, client):
        """Watch client messages and updates the client world when needed

        Args:
            client (Client): client to be updated
        """
        ready_sockets, _, _ = select.select([client.socket], [], [],
                                            TIMEOUT)

        if ready_sockets:
            received_message = RECEIVE_MESSAGE(client.socket)

            if received_message == KILL:
                self.remove_client(client, received_message)

            else:
                LOG.info(f'Received update from client {client})')
                self.update_world(received_message)

        LOG.info(f'Sending latest world to client {client}.')
        SEND_MESSAGE(client.socket, self.world)
        LOG.info('Sent latest world to client.')

    def update_world(self, message):
        """Updates server-wide World according to message

        Args:
            message (str, World): message to be used to update the server World. Use either a helpers.py macro keyword or a World object.

        Returns:
            bool: True if World updated successfully
        """
        LOG.info('Updating server world...')
        LOG.info(message)
        self.world.update(message)
        LOG.info('World has been updated. Summary:')
        LOG.info(self.world)
        return True
