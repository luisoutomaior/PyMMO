from ..helpers import SERVER_IP, SERVER_PORT, TIMEOUT, INIT, RUN, KILL, LOG, SEND_MESSAGE, RECEIVE_MESSAGE
import socket
import select


class Client:
    """Client class that implements instantiation of new world in the
    client side, and also communication and synchronization with server.
    """

    def __init__(self, id=None, socket=None, ip=SERVER_IP, port=SERVER_PORT):
        self.id = id
        self.socket = socket
        self.valid = False

        self.server_ip = ip
        self.server_port = port

        self.world = None

    def __str__(self):
        return str(f"PyMMO Client # {self.id}. Valid: {self.valid}. Socket: {self.socket}")

    def connect(self):
        """Connects to a server socket and validate by 
        exchanging messages with server.

        Returns:
            bool: True if connected and validated correctly
        """
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

    def disconnect(self):
        """Disconnects client from server and sends message to server 
        to kill server-side client instance.
        """
        LOG.info(f'Closing Client {self} sockets...')
        SEND_MESSAGE(self.socket, KILL)
        self.socket.close()

    def run(self, game):
        """Runs world on client side, including handling of kill commands, and 
        running the game's main loop.
        """
        while self.valid:
            ready_sockets, _, _ = select.select([self.socket], [], [], TIMEOUT)

            if ready_sockets:
                received_message = RECEIVE_MESSAGE(self.socket)
                if received_message == KILL:
                    self.valid = False
                    LOG.info('Received kill request. Killing client...')
                else:
                    LOG.info(
                        'Received world message from server. Running main loop:')
                    received_message.name = 'HELLO-'+str(self.id)
                    self.world.main_loop(received_message, game)

        else:
            LOG.exception('Client lost validity!')
            self.disconnect()
            exit()

    def update_world(self, message):
        """Updates client-side World according to message

        Args:
            message (World): message (object inherited from World) to be used to update the client World

        Returns:
            bool: True if World updated successfully
        """
        LOG.info('Updating client world...')
        self.world.update(message)
        LOG.info('World has been updated. Summary:')
        LOG.info(self.world)
        return True
