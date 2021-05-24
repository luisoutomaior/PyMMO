from ..helpers import SERVER_IP, SERVER_PORT, TIMEOUT, INIT, RUN, KILL, LOG, SEND_MESSAGE, RECEIVE_MESSAGE
import socket
import select


class Client:
    def __init__(self, id=None, socket=None, ip=SERVER_IP, port=SERVER_PORT):
        self.id = id
        self.socket = socket
        self.valid = False

        self.server_ip = ip
        self.server_port = port
        
        self.world = None

    def connect(self):
        LOG.info(
            f'Connecting to server {self.server_ip}:{self.server_port}  ...')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))

        LOG.info('SUCCESS. Now connected to server. Requesting entrance...')
        SEND_MESSAGE(self.socket, INIT)

        while not self.valid:
            ready_sockets, _, _ = select.select([self.socket], [], [], TIMEOUT)

            if ready_sockets:
                received_message = RECEIVE_MESSAGE(self.socket)

                if received_message == RUN:
                    self.valid = True
                    LOG.info(
                        f'SUCCESS. Entered server {self.server_ip}:{self.server_port} .')
                    received_world = RECEIVE_MESSAGE(self.socket)
                    self.world = received_world
                    
                    return True
                elif received_message:
                    LOG.info(f'Client Received: {received_message}')
        
        return True

    def disconnect(self):
        LOG.info('Closing sockets...')
        SEND_MESSAGE(self.socket, KILL)
        self.socket.close()

    def run(self):
        while self.valid:
            ready_sockets, _, _ = select.select([self.socket], [], [], TIMEOUT)

            if ready_sockets:
                received_message = RECEIVE_MESSAGE(self.socket)
                if received_message == KILL:
                    self.valid = False
                    LOG.info('Received kill request. Killing client...')
                    SEND_MESSAGE(self.socket, KILL)
                    
                else:
                    LOG.info('Received world message from server. Running main loop:')
                    received_message.name = 'HELLO-'+str(self.id)
                    self.world.main_loop(received_message)
                    
        else:
            LOG.exception('Client lost validity!')
            exit()

    def update_world(self, message):
        LOG.info('Updating client world...')
        self.world.update(message)
        LOG.info('World has been updated. Summary:')
        LOG.info(self.world)
        return True

    def __str__(self):
        return str(f"PyMMO Client # {self.id}. Valid: {self.valid}. Socket: {self.socket}")
