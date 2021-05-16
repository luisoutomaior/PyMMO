
import socket
import pygame
import select
import pygame
from macros import *
from entities import *
import pickle
import traceback
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVER_IP, SERVER_PORT))
from pprint import pprint as print


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
        if ready_sockets:
            try:
                data = pickle.loads(server.recv(1024))
            except:
                continue

            # print('curr id:', id, 'received:', data)

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

                for player in data['players']:
                    # print('id:' + player['id'] + ' vs ' + str(id))
                    if player['id'] == id:
                        color = PURPLE
                    else:
                        color = BLUE
                        
                    # print('color:' + str(color))
                        
                    sprite = Player(entity=player,
                                    color=color)

                    ui.add(HealthBar(sprite))
                    players.add(sprite)

                    if player['id'] == id:
                        main_player = sprite
                        main_player.main = True
                        

                for enemy in data['enemies']:
                    sprite = Enemy(entity=enemy,
                                   color=YELLOW)
                    ui.add(HealthBar(sprite))
                    enemies.add(sprite)

                all_sprites.add(players)
                all_sprites.add(enemies)
                all_sprites.add(ui)
            else:
                print(data)
                exit('strange result:')

        if all_sprites is None:
            continue
        else:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            all_sprites.update()

            hits = pygame.sprite.groupcollide(players, all_sprites, False, False)

            response = {'commands': []}
            if hits:
                for hitting in hits:
                    print(hits)
                    if hitting.stats['attacking']:
                        for hitted in hits[hitting]:
                            if hitted is not hitting:
                                if isinstance(hitted, Enemy):
                                    command = 'damage: player-to-enemy'
                                elif isinstance(hitted, Player):
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
                                response['commands'].append({'damage': damage_command})
                                
                                server.send(pickle.dumps(damage_command))

            if main_player.moving:
                response['commands'].append({'movement': main_player.entity})

            server.send(pickle.dumps(response))
            
            screen.fill(BLACK)
            all_sprites.draw(screen)
            pygame.display.flip()

    except Exception as e:
        print('global error: ' + str(e))
        server.send(pickle.dumps(e))
        traceback.print_exc()
        exit()
        
pygame.quit()
