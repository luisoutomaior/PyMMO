import pygame
from macros import *
from copy import deepcopy
from pprint import pprint as print

class Entity(pygame.sprite.Sprite):
    def __init__(self, entity, color=GREEN):
        self.entity = entity
        self.name = self.entity['id']
        self.pos = self.entity['pos']
        self.stats = self.entity['stats']
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.color = color
        self.image.fill(color)

        self.rect = self.image.get_rect()
        
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def update(self):
        if self.stats['hp'] <= 0:
            self.die()
        self.image.fill(self.color)

    def receive_damage(self, damage):
        hp = self.stats['hp']
        self.stats['hp'] =  hp - damage
        new_hp = self.stats['hp']
        id = self.entity['id']
        print(f'{id} got {damage} of damage. current hp: {hp}. new hp: {new_hp}')

    def die(self):
        print(str(self.entity['id']) + ' is DEAD')
        self.kill()

class HealthBar(Entity):
    def __init__(self, entity_sprite):
        entity = deepcopy(entity_sprite.entity)
        entity['id'] =  str(entity['id']) + '_HealthBar'
        super(HealthBar, self).__init__(entity)
        self.entity = entity_sprite

        self.image = pygame.Surface((32, 4))
        self.image.fill(GREY)

        self.prev_hp = -1

    def update(self):
        if self.entity.alive():
            hp_percentage = self.entity.stats['hp'] / \
                self.entity.stats['max_hp']
            if hp_percentage != self.prev_hp:
                self.prev_hp = hp_percentage
                healthbar = pygame.Surface((32 * hp_percentage, 4))
                healthbar.fill(GREEN)
                self.image.fill(GREY)
                self.image.blit(healthbar, (0, 0))

            self.rect = self.image.get_rect()
            self.rect.centerx = self.entity.rect.centerx
            self.rect.bottom = self.entity.rect.bottom - 38
        else:
            self.kill()


class Player(Entity):
    def __init__(self, entity, color=BLUE):
        super(Player, self).__init__(entity=entity,
                                           color=color)

        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.speed = (0, 0)

        self.anim_counter = 0
        self.main = False

    def update(self):
        super(Player, self).update()

        if self.main:
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

            new_pos = (self.entity['pos'][0] + self.speed[0], 
                    self.entity['pos'][1] + self.speed[1])
            
            self.entity['pos'] = new_pos
            
            self.rect.x = self.entity['pos'][0]
            self.rect.y = self.entity['pos'][1]

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

            if self.stats['attacking']:
                self.image.fill(RED)
                self.anim_counter -= self.stats['attack_speed']
                if self.anim_counter <= 0:
                    self.stats['attacking'] = False
            else:
                self.image.fill(self.color)

    def attack(self):
        self.anim_counter = 300
        self.stats['attacking'] = True


class Enemy(Entity):
    def __init__(self, entity, color=YELLOW, init_pos=(0, 0)):
        super(Enemy, self).__init__(entity=entity,
                                          color=color)

        self.rect.centerx = self.pos[0]
        self.rect.bottom = self.pos[1]
        self.speed = (0, 0)

    def update(self):
        super(Enemy, self).update()

