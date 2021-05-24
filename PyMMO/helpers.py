from copy import copy
import _pickle as pickle
from rich.traceback import install
install()

import logging
from rich.logging import RichHandler

logging.basicConfig(
    # level="ERROR",
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

LOG = logging.getLogger("rich")



# Server config
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
# TIMEOUT = 1/60 # time in seconds
# TIMEOUT = 0.001 # time in seconds
TIMEOUT = 1 # time in seconds
# BUFFER = 1024 # size in bytes
BUFFER = 1024*4 # size in bytes


# Default messages
INIT = 'INIT'
KILL = 'KILL'
RUN = 'RUN'

NEW_PLAYER_ENTITY = 'NEW_ENTITY'
KILL_PLAYER_ENTITY = 'KILL_ENTITY' 

def scramble(message):
    return message # TODO: Message scrambling

def descramble(message):
    return message # TODO: Message descrambling

def encode(message: dict):
    return pickle.dumps(scramble(message))

def decode(message):
    return pickle.loads(descramble(message))

def SEND_MESSAGE(to_socket, message):
    LOG.info(f'<<< sending...')
    status = to_socket.send(encode(message))
    LOG.info(f'<<< sent: {message}')
    return status

def RECEIVE_MESSAGE(from_socket):
    LOG.info(f'>>> receiving...')
    message = decode(from_socket.recv(BUFFER))
    LOG.info(f'>>> received: {message}')
    return message
