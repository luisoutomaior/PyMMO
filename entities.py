import pygame
from macros import *
from copy import deepcopy

class Entity:
    def __init__(self, sprite_type, pos):
        self.sprite_type = sprite_type
        self.params = {'pos': pos}

    def update(self):
        pass


class EntitySprite(pygame.sprite.Sprite):
    def __init__(self, entity, color=GREEN):
        self.entity = entity
        self.name = self.entity['id']
        self.pos = self.entity['pos']
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def update(self):
        pass


class HealthBarSprite(EntitySprite):
    def __init__(self, entity_sprite):
        entity = deepcopy(entity_sprite.entity)
        entity['id'] =  str(entity['id']) + '_HealthBar'
        super(HealthBarSprite, self).__init__(entity)
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


class PlayerSprite(EntitySprite):
    def __init__(self, entity, color=BLUE):
        super(PlayerSprite, self).__init__(entity=entity,
                                           color=color)

        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.speed = (0, 0)

        self.log = {'attacking': False}
        self.stats = {'move_speed': 8,
                      'attack_speed': 5,
                      'attack': 100,
                      'hp': 100,
                      'max_hp': 100}

        self.anim_counter = 0

    def update(self):
        super(PlayerSprite, self).update()

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


class EnemySprite(EntitySprite):
    def __init__(self, entity, color=YELLOW, init_pos=(0, 0)):
        super(EnemySprite, self).__init__(entity=entity,
                                          color=color)

        self.rect.centerx = self.pos[0] + WIDTH / 2
        self.rect.bottom = self.pos[1] + HEIGHT - 100
        self.speed = (0, 0)

        self.log = {'attacking': False}
        self.stats = {'attack_speed': 5,
                      'hp': 1000,
                      'max_hp': 1000,
                      'defense': 0.3}

        self.anim_counter = 0

    def update(self):
        super(EnemySprite, self).update()

        if self.stats['hp'] <= 0:
            self.die()

    def receive_damage(self, damage):
        hp = self.stats['hp']
        print(f'{self} got {damage} of damage. current hp: {hp}')
        self.stats['hp'] -= damage

    def die(self):
        print(self, 'is DEAD')
        self.kill()
