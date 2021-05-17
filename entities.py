import pygame
from macros import *
from copy import deepcopy
from pprint import pprint as print
import numpy as np


class EntitySprite(pygame.sprite.Sprite):
    def __init__(self, entity, color=GREEN):
        pygame.sprite.Sprite.__init__(self)
        self.entity = entity
        self.id = self.entity['id']
        self.pos = self.entity['pos']
        self.speed = (0, 0)
        self.stats = self.entity['stats']

        self.image = pygame.Surface((32, 32))
        self.color = color
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def update(self):
        self.image.fill(self.color)
        self.rect.x = self.entity['pos'][0]
        self.rect.y = self.entity['pos'][1]

        if self.speed != (0, 0):
            self.stats['moving'] = True

            new_pos = (self.entity['pos'][0] + self.speed[0],
                       self.entity['pos'][1] + self.speed[1])

            self.entity['pos'] = new_pos

        else:
            self.stats['moving'] = False

    def receive_damage(self, damage):
        hp = self.stats['hp']
        self.stats['hp'] = hp - damage
        new_hp = self.stats['hp']
        id = self.entity['id']
        print(f'{id} got {damage} of damage. current hp: {hp}. new hp: {new_hp}')

        if self.stats['hp'] <= 0:
            self.stats['alive'] = False
            self.die()

    def die(self):
        print(str(self.entity['id']) + ' is DEAD')
        self.kill()

    def speak(self):
        print('=> SPEAK:\t' + self.id + ': ' + self.stats['text'])


class HealthBarSprite(EntitySprite):
    def __init__(self, entity_sprite):
        entity = deepcopy(entity_sprite.entity)
        entity['id'] = str(entity['id']) + '_HealthBar'
        super(HealthBarSprite, self).__init__(entity)
        self.entity = entity_sprite

        self.image = pygame.Surface((32, 4))
        self.image.fill(GREY)

        self.prev_hp = -1

    def update(self):
        if self.entity.entity['stats']['alive'] and self.entity.alive():
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


class EntityNameSprite(EntitySprite):
    def __init__(self, entity_sprite, font, name):
        entity = deepcopy(entity_sprite.entity)
        super(EntityNameSprite, self).__init__(entity)
        self.entity = entity_sprite

        self.image = pygame.Surface((32, 10))
        self.image.fill(GREY)

        self.text = font.render(name + entity['id'], False, WHITE)

    def update(self):
        if self.entity.entity['stats']['alive'] and self.entity.alive():
            self.image.fill(GREY)
            self.image.blit(self.text, (0, 0))

            self.rect = self.image.get_rect()
            self.rect.centerx = self.entity.rect.centerx
            self.rect.bottom = self.entity.rect.bottom - 40
        else:
            self.kill()


class ChatBubbleSprite(EntitySprite):
    def __init__(self, entity_sprite, font, color=BLACK):
        entity = deepcopy(entity_sprite.entity)
        super(ChatBubbleSprite, self).__init__(entity)
        self.entity = entity_sprite

        self.text = font.render(self.entity.stats['text'], False, WHITE)
        self.image = pygame.Surface((self.text.get_width(), 10))
        self.image.fill(color)

    def update(self):
        if self.entity.entity['stats']['alive'] and self.entity.alive():
            self.image.fill(GREY)
            self.image.blit(self.text, (0, 0))

            self.rect = self.image.get_rect()
            self.rect.centerx = self.entity.rect.centerx
            self.rect.bottom = self.entity.rect.bottom - 48
        else:
            self.kill()


class EnemySprite(EntitySprite):
    def __init__(self, entity, color=YELLOW, init_pos=(0, 0)):
        super(EnemySprite, self).__init__(entity=entity,
                                          color=color)

        self.rect.centerx = self.pos[0]
        self.rect.bottom = self.pos[1]
        self.speed = (0, 0)

    def update(self):
        super(EnemySprite, self).update()


class PlayerSprite(EntitySprite):
    def __init__(self, entity, color=BLUE):
        super(PlayerSprite, self).__init__(entity=entity,
                                           color=color)

        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.speed = (0, 0)

        self.anim_counter = 0
        self.speak_counter = 300
        self.main = False

    def update(self):

        if self.main:
            self.speed = (0, 0)

            keystate = pygame.key.get_pressed()
            char = np.argmax(list(keystate)) - 4
            possible_chars = 'abcdefghijklmnopqrstuvwxyz'
            if char >= 0 and char < len(possible_chars):
                char = possible_chars[char]
                self.stats['text'] += char
                self.stats['speaking'] = 'writing'

            if keystate[pygame.K_LEFT]:
                self.speed = (-8, 0)
            if keystate[pygame.K_RIGHT]:
                self.speed = (8, 0)
            if keystate[pygame.K_UP]:
                self.speed = (0, -8)
            if keystate[pygame.K_DOWN]:
                self.speed = (0, 8)

            if not self.stats['attacking'] and keystate[pygame.K_SPACE]:
                self.attack()

            elif self.stats['attacking']:
                self.image.fill(RED)
                self.anim_counter -= self.stats['attack_speed']
                if self.anim_counter <= 0:
                    self.stats['attacking'] = False
                    
            
            if keystate[pygame.K_RETURN]:
                print(self.stats['speaking'])
                if self.stats['speaking'] == 'writing':
                    self.stats['speaking'] = 'ready'
                print(self.stats['speaking'])
                
            if self.stats['speaking'] == 'ready':
                self.image.fill(GREY)
                self.speak()
                
                if self.stats['speaking_time'] > 0:
                    self.stats['speaking_time'] -= 200

            else:
                self.image.fill(self.color)

        super(PlayerSprite, self).update()

    def attack(self):
        self.anim_counter = 3000
        self.stats['attacking'] = True
