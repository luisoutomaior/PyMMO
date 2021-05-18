
from pprint import pprint as print
import socket
import pygame
import select
import pygame
from macros import *
from entities import *
import pickle
import traceback
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--enemies_only',
                    action='store_true',
                    # dest='accumulate',
                    # action='store_const',
                    # const=sum,
                    # default=max,
                    help='only add enemies')

args = parser.parse_args()
print(args)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVER_IP, SERVER_PORT))


pygame.init()

font = pygame.font.SysFont('arial',  10)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED)
screen.fill(GREEN)
pygame.display.set_caption("PyMMO")
clock = pygame.time.Clock()


id = None
all_sprites = None
main_player = None

running = True
while running:
    ready_sockets, _, _ = select.select([server], [], [],
                                        CLIENT_TIMEOUT)
    try:
        if ready_sockets:
            try:
                data = pickle.loads(server.recv(1024))
            except:
                continue

            if isinstance(data, str) and data == 'kill':
                print(data)
                exit('Killed by server')

            if id is None and not isinstance(data, str):
                print('still needs id')
                continue

            elif id is None and isinstance(data, str):
                id = data
                print('new id: ' + str(id))
                continue

            elif id is not None and not isinstance(data, dict):
                print('not dict')
                continue

            elif id is not None and isinstance(data, dict):
                enemies = pygame.sprite.Group()
                players = pygame.sprite.Group()
                ui = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()

                if not args.enemies_only:
                    for player_entity in data['players']:
                        if player_entity['id'] == id:
                            # print('player_entity: ')
                            # print(player_entity)
                            color = PURPLE
                        else:
                            color = BLUE

                        sprite = PlayerSprite(entity=player_entity,
                                              color=color)

                        ui.add(HealthBarSprite(sprite))
                        ui.add(EntityNameSprite(sprite, font, 'Player'))
                        

                        if player_entity['id'] == id and player_entity['stats']['speaking'] == 'writing':
                            ui.add(ChatBubbleSprite(sprite, font, color=DARKGREY))
                            
                        if player_entity['stats']['speaking'] == 'ready':
                            ui.add(ChatBubbleSprite(sprite, font, color=LIGHTBLACK))
  
                        players.add(sprite)

                        if player_entity['id'] == id:
                            main_player = sprite
                            main_player.main = True

                for enemy_entity in data['enemies']:
                    sprite = EnemySprite(entity=enemy_entity,
                                         color=YELLOW)
                    ui.add(HealthBarSprite(sprite))
                    ui.add(EntityNameSprite(sprite, font, 'Enemy'))
                    enemies.add(sprite)

                all_sprites.add(players)
                all_sprites.add(enemies)
                all_sprites.add(ui)
            else:
                print(data)
                exit('strange result:')

            if all_sprites is None:
                print('all_sprites is None')
                continue
            else:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                all_sprites.update()

                hits = pygame.sprite.groupcollide(
                    players, all_sprites, False, False)

                response = {'commands': [], 'id': id}
                if hits:
                    for hitting in hits:
                        if hitting.stats['attacking']:
                            for hitted in hits[hitting]:
                                if hitted is not hitting:
                                    if isinstance(hitted, EnemySprite):
                                        command = 'damage: player-to-enemy'
                                    elif isinstance(hitted, PlayerSprite):
                                        command = 'damage: player-to-player'
                                    else:
                                        continue

                                    damage = CALCULATE_DAMAGE(hitting.stats,
                                                            hitted.stats,
                                                            NORMAL_ATTACK)
                                    new_hp = hitted.stats['hp']
                                    hitted.receive_damage(damage)

                                    damage_command = {'type': command,
                                                    'hitting': hitting.entity,
                                                    'hitted': hitted.entity}
                                    response['commands'].append(
                                        {'damage': damage_command})

                if main_player is not None:
                    if main_player.stats['moving']:
                        response['commands'].append({'movement': main_player.entity})

                    if main_player.stats['animating']:
                        response['commands'].append({'animation': main_player.entity})

                    if main_player.stats['speaking']:
                        response['commands'].append({'speak': main_player.entity})
                        

                if len(response['commands']):
                    print('sending:')
                    print(response)
                    server.send(pickle.dumps(response))

                screen.fill(BLACK)
                all_sprites.draw(screen)
                pygame.display.flip()
                # input('lol')

    except Exception as e:
        print('global error: ' + str(e))
        server.send(pickle.dumps(e))
        traceback.print_exc()
        exit()

pygame.quit()
