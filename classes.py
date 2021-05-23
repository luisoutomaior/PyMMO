from dataclasses import dataclass, field
from copy import copy
from random import randint
import socket
import _pickle as pickle
from _thread import start_new_thread
import select

SERVER_PORT = 12345
SERVER_TIMEOUT = 0.001


def default(obj):
    return field(default_factory=lambda: copy(obj)())

def encode(message):
    return pickle.dumps(message)

def decode(message):
    return pickle.loads(message)

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = SERVER_PORT
        self.clients = set()
        self.world = World()

    def connect(self):
        print('Starting up server...')
        self.socket.bind('127.0.0.1', SERVER_PORT)
        self.socket.listen(2)
        print('Server running!')
        return True
    
    def num_clients(self):
        return len(self.clients)

    def open_to_clients(self):
        while True:        
            num_clients = self.num_clients()
            print(f'Server currently has {num_clients} clients connected.')

            print('Waiting for new client...')
            client_socket, client_address = self.socket.accept()

            print(f'Received connection request from:', client_address)

            new_client_id = num_clients + 1
            print(f'Adding new client # {new_client_id}')
            new_client = Client(new_client_id, client_socket)
            self.clients.add(new_client)
            print(f'Added to client {new_client} to server.')

            start_new_thread(self.refresh_client, (new_client,))


    def refresh_client(self, client):
        while True:
            ready_sockets, _, _ = select.select([client.socket], [], [], 
                                                SERVER_TIMEOUT)

            if ready_sockets:
                received_message = self.receive_message(client.socket)
                print(f'Received update from client {client.id}: {received_message}')

                ### Update game world
                update_message = self.refresh_world(received_message)

                print(f'Updating client {client.id}. sending: ', update_message)
                return self.send_message(client.socket, update_message)

    def send_message(self, socket, message):
        print('sending message:', message)
        status = socket.send(encode(message))
        return status

    def receive_message(self, socket):
        message = decode(socket.recv(1024))
        print('received message:', message)
        return message
        
    def refresh_world(self, message):
        print('Updating game world...')
        return message

class Client:
    def __init__(self, id, socket):
        self.id = id
        self.socket = socket


@dataclass
class Entity:
    name: str


@dataclass
class World:
    entities: list = default(list)

    def add_entity(self, entity: Entity):
        self.entities.append(entity)
