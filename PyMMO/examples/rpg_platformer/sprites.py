import pygame
from .macros import *
from copy import deepcopy
from pprint import pprint as print
import numpy as np



CHAR_STANDING_SPRITESHEET = pygame.image.load(ASSETS_PATH + 'Char Standing.png')
CHAR_ATTACKING_SPRITESHEET = pygame.image.load(ASSETS_PATH + 'Char Attacking.png')


class EntitySprite(pygame.sprite.Sprite):
    def __init__(self, entity, color=GREEN):
        pygame.sprite.Sprite.__init__(self)
        self.entity = entity
        
        # Position and Movement
        self.pos = self.entity['pos']
        self.speed = self.entity['speed']
        self.accel = self.entity['accel']
        
        self.stats = self.entity['stats']

        # Appearance
        self.image = pygame.Surface((64, 64))
        self.foreground = None
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def update(self):
        # Movement
        if self.speed != (0, 0):
            self.stats['moving'] = True

            new_pos = (self.entity['pos'][0] + self.speed[0],
                       self.entity['pos'][1] + self.speed[1])

            self.entity['pos'] = new_pos
            
            if self.speed[0] > 0:
                self.entity['dir'] = RIGHT
            elif self.speed[0] < 0:
                self.entity['dir'] = LEFT
            
        else:
            self.stats['moving'] = False

        self.rect.x = self.entity['pos'][0]
        self.rect.y = self.entity['pos'][1]
            
        # Animation
        if self.foreground is not None:
            animation = 'attacking' if self.stats['attacking'] else 'default'
            
            if self.stats['foreground_idx'] >= len(self.stats['foreground_loc'][animation]) - 1:
                self.stats['foreground_idx'] = 0
            else:
                self.stats['foreground_idx'] += 1

            curr_loc = self.stats['foreground_loc'][animation][self.stats['foreground_idx']]
            
            self.image.fill(BACKGROUND)
            self.image.blit(self.foreground[animation], curr_loc)
            self.image.set_colorkey(BACKGROUND)
            if self.entity['dir'] != RIGHT:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image.fill(self.color)

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
        print('=> SPEAK:\t' + self.entity['id'] + ': ' + self.stats['text'])


class HealthBarSprite(EntitySprite):
    def __init__(self, entity_sprite):
        entity = deepcopy(entity_sprite.entity)
        super(HealthBarSprite, self).__init__(entity)
        self.entity = entity_sprite

        self.image = pygame.Surface((32, 6))
        self.image.fill(DARKGREY)

        self.prev_hp = -1

    def update(self):
        if self.entity.entity['stats']['alive'] and self.entity.alive():
            hp_percentage = self.entity.stats['hp'] / \
                self.entity.stats['max_hp']
            if hp_percentage != self.prev_hp:
                self.prev_hp = hp_percentage
                healthbar = pygame.Surface((30 * hp_percentage, 4))
                healthbar.fill(GREEN)
                self.image.fill(DARKGREY)
                self.image.blit(healthbar, (1, 1))

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

        self.text = font.render(name + str(entity['id']), False, WHITE)
        self.image = pygame.Surface((self.text.get_rect().width, 10))
        self.image.fill(DARKGREY)

    def update(self):
        if self.entity.entity['stats']['alive'] and self.entity.alive():
            self.image.fill(DARKGREY)
            self.image.blit(self.text, (0, 0))

            self.rect = self.image.get_rect()
            self.rect.centerx = self.entity.rect.centerx
            self.rect.bottom = self.entity.rect.bottom - 44
        else:
            self.kill()


class ChatBubbleSprite(EntitySprite):
    def __init__(self, entity_sprite, font, color=BLACK):
        entity = deepcopy(entity_sprite.entity)
        super(ChatBubbleSprite, self).__init__(entity)
        self.entity = entity_sprite
        self.color = color

        text_color = (255 - color[0], 255 - color[1], 255 - color[2])

        self.text = font.render(self.entity.stats['text'], False, text_color)
        self.image = pygame.Surface((self.text.get_width(), 12))
        self.image.fill(color)

    def update(self):
        if self.entity.entity['stats']['alive'] and self.entity.alive():
            self.image.fill(self.color)
            self.image.blit(self.text, (0, 0))

            self.rect = self.image.get_rect()
            self.rect.centerx = self.entity.rect.centerx
            self.rect.bottom = self.entity.rect.bottom - 56
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

        self.foreground = {'default': CHAR_STANDING_SPRITESHEET,
                           'attacking': CHAR_ATTACKING_SPRITESHEET}
        self.stats['foreground_loc'] = {
            'default': [
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
                (0, -64),
                (0, -64),
                (0, -64),
                (0, -64),
            ],
            'attacking': [
                (0, 0),
                (0, 0),
                (0, -64),
                (0, -64),
                (0, -64*2),
                (0, -64*2),
                (0, -64*3),
                (0, -64*3),
                (0, -64*4),
                (0, -64*4),
            ]}

        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.speed = (0, 0)

        self.main = False
        self.stats['animating'] = True

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

            if keystate[pygame.K_RETURN]:
                if self.stats['speaking'] == 'writing':
                    self.stats['speaking'] = 'ready'

            if self.stats['speaking'] == 'ready':
                # self.image.fill(DARKGREY)
                self.speak()

                if self.stats['speaking_time'] > 0:
                    self.stats['speaking_time'] -= 50

        super(PlayerSprite, self).update()

    def attack(self):
        self.stats['attacking'] = True
