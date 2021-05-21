
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12346
SERVER_TIMEOUT = 1
CLIENT_TIMEOUT = 1

PACKET_SIZE = 1024 * 8
DEFAULT_CHAT_TIME = 5000

WIDTH = 64*4
HEIGHT = 64*4
FPS = 60

WHITE = (255, 255, 255)
LIGHTBLACK = (200, 200, 200)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
DARKGREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 255)
BACKGROUND = (254, 254, 254)

NORMAL_ATTACK = 0
RIGHT = 1
LEFT = 0

def CALCULATE_DAMAGE(attacker_stats, attacked_stats, kind=NORMAL_ATTACK):

    if kind == NORMAL_ATTACK:
        damage = max(attacker_stats['attack'] * attacked_stats['defense'], 0)
    else:
        damage = 9999

    return damage


def INIT_STATS(**kwargs):

    stats= {'alive': True,
            'move_speed': 8,
            'attack_speed': 5,
            'attack': 5,
            'defense': 0.3,
            'hp': 100,
            'max_hp': 100,
            'attacking': False,
            'moving': False,
            'speaking': False,
            'speaking_time': DEFAULT_CHAT_TIME,
            'text': '',
            'animating': False,
            'foreground_loc': {'default': [(0,0)]},
            'foreground_idx': -1}
    
    for arg in kwargs:
        stats[arg] = kwargs[arg]
        
    return stats


class Entity:
    def __init__(self, id, kind, pos, dir=RIGHT, stats=INIT_STATS(), sprite_name=None):
        self.id = id
        self.kind = kind
        self.pos = pos
        self.dir = dir
        self.stats = stats
        self.sprite_name = sprite_name
        
    def update_position(self, entity):
        self.pos = entity.pos
        self.dir = entity.dir

    def update_animation(self, entity):
        self.stats['animating'] = entity.stats['animating']
        self.stats['foreground_loc'] = entity.stats['foreground_loc']
        self.stats['foreground_idx'] = entity.stats['foreground_idx']
        
    def update_speech(self, entity):
        self.stats['text'] = entity.stats['text']
        self.stats['speaking'] = entity.stats['speaking']
        self.stats['speaking_time'] = entity.stats['speaking_time']

        if self.stats['speaking_time'] <= 0:
            self.stats['speaking_time'] = DEFAULT_CHAT_TIME

        if self.stats['speaking']:
            self.stats['text'] = ''
            self.stats['speaking'] = False
            
    def update_stats(self, entity):
        self.stats['hp'] = entity.stats['hp']
        

    def __repr__(self):
        from pprint import pformat
        return 'Entity\n' + pformat(vars(self), indent=4, width=1)