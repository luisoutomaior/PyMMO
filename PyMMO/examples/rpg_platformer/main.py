from PyMMO import Server, Client, World, NEW_ENTITY
import time
from random import random


class HelloWorld(World):
    def __init__(self, name='HelloWorld'):
        super().__init__(name=name)
        self.prev_time = 0

    def main_loop(self, new_world):
        ########################
        # Do something to world
        # e.g. create new entities, add/change sprites, calculate stuff, etc
        time.sleep(0.001)
        print(f'Hello world! {new_world}')
        
        # whatever you return will persist in the server
        # and will be consistent across all clients
        ########################
        print('time difference:', time.time() - self.prev_time, 'seconds')
        self.prev_time = time.time()
        return new_world
        
    def update(self, message):
        if message == NEW_ENTITY:
            name = self.random_name()
            self.add_entity({'name': f'entity_{name}'})
        return self
    
    def random_name(self):
        return str(random())[2:]



if __name__ == '__main__':
    try:
        client = Client()
        client.connect()
        client.run()

    except KeyboardInterrupt:
        client.disconnect()
        exit('Client killed manually.')

    except ConnectionRefusedError:
        # input('No existing servers found. Press any button to start a new server.')
        try:
            server = Server()
            server.init_world(HelloWorld)
            server.start()
        except KeyboardInterrupt:
            client.disconnect()
            exit('Server killed manually.')
          
    server.stop()
