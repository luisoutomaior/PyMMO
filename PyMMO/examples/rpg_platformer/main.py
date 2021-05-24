from PyMMO import Server, Client, World
import time
import pygame
from .macros import BLACK, GREEN, WIDTH, HEIGHT, FPS
from .sprites import PlayerSprite, HealthBarSprite, EntityNameSprite

class HelloWorld(World):
    def __init__(self, name='HelloWorld'):
        super().__init__(name=name)
        
        self.prev_time = time.time()
        
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED)
        screen.fill(GREEN)
        pygame.display.set_caption("PyMMO HelloWorld")
        
        self.font = pygame.font.SysFont('arial',  10)
        self.clock = pygame.time.Clock()
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def main_loop(self, new_world):
        print(f'{self} time difference: {time.time() - self.prev_time} seconds')
        
        for entity_id in new_world.entities:
            entity = new_world.entities[entity_id]
            sprite = None
            if 'player-' in entity_id:
                sprite = PlayerSprite(entity)
                sprite.main = True

                self.players.add(sprite)
                
                self.ui.add(HealthBarSprite(sprite))
                self.ui.add(EntityNameSprite(sprite, self.font, 'Player'))
            
            if sprite is not None:
                self.all_sprites.add(sprite)
                
        self.clock.tick(FPS)
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        
        # time.sleep(1)
        # input('Press any key to update world...')
        self.prev_time = time.time()
        return new_world
        

if __name__ == '__main__':
    try:
        client = Client()
        client.connect()
        client.run()

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
          
