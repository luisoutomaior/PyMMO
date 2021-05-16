import pygame
from macros import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, name="Entity", color=GREEN, init_pos=(WIDTH / 2, HEIGHT / 2)):
        self.name = name
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        print(color)
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.centerx = init_pos[0]
        self.rect.bottom = init_pos[1]

    def update(self):
        pass

class HealthBar(Entity):
    def __init__(self, entity):
        super(HealthBar, self).__init__(name='HealthBar')
        self.entity = entity
        
        self.image = pygame.Surface((32, 4))
        self.image.fill(GREY)
        self.prev_hp = -1
        
    def update(self):
        if self.entity.alive():
            hp_percentage = self.entity.stats['hp'] / self.entity.stats['max_hp']
            if hp_percentage != self.prev_hp:
                self.prev_hp = hp_percentage
                healthbar = pygame.Surface((32 * hp_percentage, 4))
                healthbar.fill(GREEN)
                self.image.fill(GREY)
                self.image.blit(healthbar, (0,0))

            self.rect = self.image.get_rect()
            self.rect.centerx = self.entity.rect.centerx
            self.rect.bottom = self.entity.rect.bottom - 38
        else:
            self.kill()


class Player(Entity):
    def __init__(self, name='Player', color=BLUE, init_pos=(0, 0)):
        super(Player, self).__init__(name=name,
                                     color=color, 
                                     init_pos=init_pos)

        self.rect.centerx = init_pos[0] + WIDTH / 2
        self.rect.bottom = init_pos[1] + HEIGHT - 10
        self.speed = (0, 0)

        self.log = {'attacking': False}
        self.stats = {'attack_speed': 5,
                      'attack': 100,
                      'hp': 100,
                      'max_hp': 100} 

        self.anim_counter = 0

    def update(self):
        super(Player, self).update()

        self.speed = (0, 0)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed = (-8, 0)
        if keystate[pygame.K_RIGHT]:
            self.speed = (8, 0)
        if keystate[pygame.K_UP]:
            self.speed = (0, -8)
        if keystate[pygame.K_DOWN]:
            self.speed = (0, 8)

        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

        if keystate[pygame.K_RETURN]:
            self.attack()

        if self.log['attacking']:
            self.image.fill(RED)
            self.anim_counter -= self.stats['attack_speed']
            if self.anim_counter <= 0:
                self.log['attacking'] = False
        else:
            self.image.fill(BLUE)

    def attack(self):
        self.anim_counter = 30
        self.log['attacking'] = True


class Enemy(Entity):
    def __init__(self, name='Enemy', color=YELLOW, init_pos=(0, 0)):
        super(Enemy, self).__init__(name=name,
                                    color=color, 
                                    init_pos=init_pos)

        self.rect.centerx = init_pos[0] + WIDTH / 2
        self.rect.bottom = init_pos[1] + HEIGHT - 100
        self.speed = (0, 0)

        self.log = {'attacking': False}
        self.stats = {'attack_speed': 5,
                      'hp': 1000,
                      'max_hp': 1000,
                      'defense': 0.3} 

        self.anim_counter = 0

    def update(self):
        super(Enemy, self).update()

        if self.stats['hp'] <= 0:
            self.die()

    def receive_damage(self, damage):
        hp = self.stats['hp']
        print(f'{self} got {damage} of damage. current hp: {hp}')
        self.stats['hp'] -= damage

    def die(self):
        print(self, 'is DEAD')
        self.kill()
