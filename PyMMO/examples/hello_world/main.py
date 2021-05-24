from PyMMO.helpers import SERVER_PORT
from PyMMO import Server, Client
import time

def main_loop(world):
    # Do something to world
    time.sleep(1)
    print(world)
    return world

if __name__ == '__main__':
    try:
        client = Client()
        client.connect()
        
        client.run_game_loop(main_loop)

    except KeyboardInterrupt:
        client.disconnect()
        exit('Client killed manually.')

    except BaseException as e:
        print(e)
        # input('No existing servers found. Press any button to start a new server.')
        server = Server()
        server.start()

          
    server.stop()
