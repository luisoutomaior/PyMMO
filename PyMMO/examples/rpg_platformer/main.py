from PyMMO import Server, Client, World, Entity, NEW_PLAYER_ENTITY, KILL_PLAYER_ENTITY
from PyMMO.examples.rpg_platformer.macros import BLACK, GREEN, WIDTH, HEIGHT, FPS
from PyMMO.examples.rpg_platformer.sprites import PlayerSprite, HealthBarSprite, EntityNameSprite
import pygame
import time

# World is the object that is transferred between client and server.
# It needs to be pickle-able. 
# This class controls Game objects e.g. adds new sprites, refreshes screen, etc.

class RpgPlatformerWorld(World):
    def __init__(self, name='HelloWorld'):
        super().__init__(name=name)

    def update(self, message):
        if NEW_PLAYER_ENTITY in message:
            self.add_entity(id=message[NEW_PLAYER_ENTITY],
                            entity_class=RpgPlatformerEntity,
                            kind='player')
            
        elif KILL_PLAYER_ENTITY in message:
            self.kill_entity(id=message[KILL_PLAYER_ENTITY])
            

    def main_loop(self, new_world, game):

        game.clear()
        for entity_id in new_world.entities:
            entity = new_world.entities[entity_id]
            sprite = None
            print(entity)
            if entity['kind'] == 'player':
                sprite = PlayerSprite(entity)
                sprite.main = True

                game.players.add(sprite)

                game.ui.add(HealthBarSprite(sprite))
                game.ui.add(EntityNameSprite(sprite, game.font, 'Player'))

            if sprite is not None:
                game.all_sprites.add(sprite)
        game.tick()

        return new_world

# Game is the class that contains the main PyGame objects such as display, sprites, etc.
class RpgPlatformerGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED)
        self.screen.fill(GREEN)
        pygame.display.set_caption("PyMMO RPG Platformer")

        self.font = pygame.font.SysFont('arial',  10)
        self.clock = pygame.time.Clock()

        self.prev_time = time.time()
        
    def clear(self):
        print(f'Latency: {time.time() - self.prev_time:.5f} seconds')
        self.prev_time = time.time()
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def tick(self):
        self.clock.tick(FPS)
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


# Entities are objects that the World retains, i.e. are transferred beteween Client and Server
# These objects need to be pickle-able and serializable
# They describe in-game objects such as playable and non-playable characters, enemies, etc
class RpgPlatformerEntity(Entity):
    def __init__(self, id, **kwargs):
        super().__init__(id, entity_spec_or_gen=self.entity_spec_gen, **kwargs)
            
    def entity_spec_gen(self, id):
        stats = {
            'id': id,
            'kind': 'entity',
            'pos': (HEIGHT//2, WIDTH//2),
            'speed': (0, 0),
            'accel': (0, 0),
            'stats': {
                'alive': True,
                'move_speed': 5,
                'attack_speed': 5,
                'attack': 1,
                'defense': 0,
                'max_hp': 100,
                'hp': 100,
                'attacking': False,
                'moving': False,
                'speaking': False,
                'speaking_time': 50,
                'text': '',
                'animating': False,
                'foreground_loc': {'default': [(0, 0)]},
                'foreground_idx': -1
            }
        }
        return stats

if __name__ == '__main__':
    port = 12347
    try:
        client = Client(port=port)
        client.connect()
        
        game = RpgPlatformerGame()
        client.run(game)

    except KeyboardInterrupt:
        client.disconnect()
        exit('Client killed manually.')

    except ConnectionRefusedError:
        # input('No existing servers found. Press any button to start a new server.')
        try:
            server = Server(port=port)
            server.init_world(RpgPlatformerWorld)
            server.start()

        except KeyboardInterrupt:
            server.stop()
            exit('Server killed manually.')
