
from os import read
import socket
from numpy.lib.arraysetops import isin
import pygame
import select
import pygame
from macros import *
from entities import *
import pickle
import traceback
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVER_IP, SERVER_PORT))


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hysteresis")
clock = pygame.time.Clock()



id = None
all_sprites = None
main_player = None

running = True
while running:
    ready_sockets, _, _ = select.select([server], [], [],
                                        CLIENT_TIMEOUT)
    try:
        print(ready_sockets)
        if ready_sockets:
            try:
                data = pickle.loads(server.recv(1024))
            except:
                continue

            print('curr id:', id, 'received:', data)

            if id is None and not isinstance(data, str):
                print('still needs id')
                continue
            
            elif id is None and isinstance(data, str):
                id = data
                print('new id', id)
                continue
            
            elif id is not None and not isinstance(data, dict):
                print('not dict')
                continue
                
            elif id is not None and isinstance(data, dict):
                players = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                ui = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()
                
                for player in data['players']:
                    sprite = PlayerSprite(entity=player,
                                        color=BLUE)
                    ui.add(HealthBarSprite(sprite))
                    players.add(sprite)
                    
                    print(player['id'], id)
                    if player['id'] == id:
                        main_player = sprite

                for enemy in data['enemies']:
                    sprite = EnemySprite(entity=enemy,
                                            color=YELLOW)
                    ui.add(HealthBarSprite(sprite))
                    enemies.add(sprite)

                all_sprites.add(players)
                all_sprites.add(enemies)
                all_sprites.add(ui)
            else:
                print(data)
                exit('strange result:')

        print(id, 'all sprites', all_sprites)
        if all_sprites is None:
            continue
        else:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            all_sprites.update()

            hits = pygame.sprite.groupcollide(players, enemies, False, False)

            if hits:
                for hitting in hits:
                    if isinstance(hitting, PlayerSprite) and hitting.log['attacking']:
                        for hitted in hits[hitting]:
                            damage = CALCULATE_DAMAGE(hitting.stats,
                                                    hitted.stats,
                                                    NORMAL_ATTACK)
                            new_hp = hitted.stats['hp']
                            hitted.receive_damage(damage)
                            message = bytes(
                                f'{hitting.name} attacked {hitted.name}, damage: {damage} {new_hp}', "utf-8")
                            # server.send(pickle.dumps(message))

            server.send(pickle.dumps(main_player.entity))
            screen.fill(BLACK)
            all_sprites.draw(screen)
            pygame.display.flip()

    except Exception as e:
        print('global error:',e)
        server.send(pickle.dumps(e))
        traceback.print_exc()
        exit()
pygame.quit()
