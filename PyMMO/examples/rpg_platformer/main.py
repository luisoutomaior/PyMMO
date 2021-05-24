from PyMMO import Server, Client, World, NEW_ENTITY
import time
from random import random


class HelloWorld(World):
    def __init__(self, name='HelloWorld'):
        super().__init__(name=name)
        self.prev_time = 0

    def main_loop(self, new_world):
        time.sleep(1)
        print(f'{self} time difference: {time.time() - self.prev_time} seconds')
        input('Press any key to update world...')
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
            server.stop()
            exit('Server killed manually.')
          
