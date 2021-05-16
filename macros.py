
WIDTH = 480
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

NORMAL_ATTACK = 0

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12346
SERVER_TIMEOUT = 0.1
CLIENT_TIMEOUT = 0.01


def CALCULATE_DAMAGE(attacker_stats, attacked_stats, kind=NORMAL_ATTACK):

    if kind == NORMAL_ATTACK:
        damage = max(attacker_stats['attack'] * attacked_stats['defense'], 0)
    else:
        damage = 9999

    return damage


def INIT_STATS(**kwargs):

    stats= {'move_speed': 8,
            'attack_speed': 5,
            'attack': 100,
            'defense': 0.3,
            'hp': 100,
            'max_hp': 100,
            'attacking': False}
    
    for arg in kwargs:
        stats[arg] = kwargs[arg]
        
    return stats
