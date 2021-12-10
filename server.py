import sys
import time
import socket
import select
import pickle
import threading
from pprint import pprint
from typing import Dict, Any

from macros import *


class ResponseHandler:
    def handle_commands(self, status: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        for command in response['commands']:
            cmd = list(command.keys())[0]
            handler = getattr(self, f'_handle_{cmd}', None)

            if callable(handler):
                status = handler(status, command[cmd])
            else:
                print(f'No handler for {cmd}')

        # print('new status:')
        # pprint(status)

        return status

    @staticmethod
    def _handle_movement(status: Dict[str, Any], command: Dict[str, Any]) -> Dict[str, Any]:
        for player in status['players']:
            if player['id'] == command['id']:
                player['pos'] = command['pos']
                player['dir'] = command['dir']

        return status

    @staticmethod
    def _handle_animation(status: Dict[str, Any], command: Dict[str, Any]) -> Dict[str, Any]:
        for player in status['players']:
            if player['id'] == command['id']:
                player['stats']['animating'] = command['stats']['animating']
                player['stats']['foreground_loc'] = command['stats']['foreground_loc']
                player['stats']['foreground_idx'] = command['stats']['foreground_idx']

        return status

    @staticmethod
    def _handle_speak(status: Dict[str, Any], command: Dict[str, Any]) -> Dict[str, Any]:
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

        return status

    @staticmethod
    def _handle_damage(status: Dict[str, Any], command: Dict[str, Any]) -> Dict[str, Any]:       
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

        return status


class PyMMOServer:
    def __init__(self, host: str, port: int, response_handler: ResponseHandler) -> None:
        self.HEADER = 1024  # Default header length
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Server socket

        self.host = host
        self.port = port

        self.response_handler = response_handler
        self.status = {'working': True, 'players': [], 'enemies': []}
        self.__total_player_count = 0

        try:
            self.server.bind((host, port))
            self.server.listen()
            self.server.settimeout(1.0)  # Allow timeout to process KeyboardInterrupt
        except Exception as error:
            print(f'[ERROR IN CREATING A SERVER] {error}')
            sys.exit()
        else:
            print(f'[SERVER IS LISTENING] @ {host}:{port}')

    def run(self) -> None:
        while True:
            try:
                client, address = self.server.accept()
                self.__total_player_count += 1

                self._establish_connection(address, time.time())
                client.send(pickle.dumps(str(self.__total_player_count)))

                conn_thread = threading.Thread(target=self._handler, args=(client, self.status))
                conn_thread.start()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            except BaseException as error:
                print(f'[SERVER EXCEPTION] {error}')
                self.socket.close()
                sys.exit()

    def _handler(self, conn: socket.socket, status: Dict[str, Any]) -> None:
        while True:
            ready_sockets, _, _ = select.select([conn], [], [], SERVER_TIMEOUT)

            if not ready_sockets:
                conn.send(pickle.dumps(status))
                continue
            
            # response format:
            # for commands: {'action': 'commands', 'value': {'commands': ...}}
            # for errors: {'action': 'error', 'value': {'error': ...}}
            try:
                response = pickle.loads(conn.recv(self.HEADER))
                handler = getattr(self.response_handler, f'handle_{response["action"]}', None)
                
                if callable(handler):
                    # print('old status:')
                    # pprint(status)
                    # print('received:')
                    # pprint(response)
                    status = handler(status, response['value'])
                    conn.send(pickle.dumps(status))
                else:
                    print(f'No handler for {response["action"]}')
                    
            except Exception as e:
                # traceback.print_exc()
                break

    def _establish_connection(self, address: str, time_connected: float) -> None:
        print(f'Connection has been established with: {address} at {time_connected}. Welcome :)')

        self.status['players'].append({
            'id': str(self.__total_player_count),
            'pos': (WIDTH/2, HEIGHT/2), 
            'dir': RIGHT, 
            'stats': INIT_STATS()
        })

    @property
    def total_player_count(self) -> int:
        return self.__total_player_count

    @property
    def active_player_count(self) -> int:
        return threading.activeCount() - 1  # Subtract 1 to exclude the main thread


def main() -> None:
    server = PyMMOServer('127.0.0.1', SERVER_PORT, ResponseHandler())
    server.run()


if __name__ == '__main__':
    main()
