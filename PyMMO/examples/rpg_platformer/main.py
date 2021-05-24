from PyMMO import Server, Client, World
from PyMMO.examples.rpg_platformer.macros import BLACK, GREEN, WIDTH, HEIGHT, FPS
from PyMMO.examples.rpg_platformer.sprites import PlayerSprite, HealthBarSprite, EntityNameSprite
import pygame
import time


class HelloWorld(World):
    def __init__(self, name='HelloWorld'):
        super().__init__(name=name)
        self.prev_time = time.time()

    def main_loop(self, new_world, game):
        print(f'{self} time difference: {time.time() - self.prev_time} seconds')

        for entity_id in new_world.entities:
            entity = new_world.entities[entity_id]
            sprite = None
            if 'player-' in entity_id:
                sprite = PlayerSprite(entity)
                sprite.main = True

                game.players.add(sprite)

                game.ui.add(HealthBarSprite(sprite))
                game.ui.add(EntityNameSprite(sprite, self.font, 'Player'))

            if sprite is not None:
                game.all_sprites.add(sprite)

        game.tick()

        self.prev_time = time.time()
        return new_world
    
    
class RpgPlatformerPyGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED)
        self.screen.fill(GREEN)
        pygame.display.set_caption("PyMMO RPG Platformer")

        self.font = pygame.font.SysFont('arial',  10)
        self.clock = pygame.time.Clock()

        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
    

    def tick(self):
        self.clock.tick(FPS)
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        

if __name__ == '__main__':
    try:
        client = Client()
        client.connect()
        client.run(RpgPlatformerPyGame())

    except KeyboardInterrupt:
        client.disconnect()
        exit('Client killed manually.')

    except ConnectionRefusedError:
        # input('No existing servers found. Press any button to start a new server.')
        try:
            server = Server()
            server.init_world(HelloWorld)
            server.start()

        except KeyboardInterrupt:
            server.stop()
            exit('Server killed manually.')
