import pygame
from macros import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, color=GREEN, init_pos=(WIDTH / 2, HEIGHT / 2)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = init_pos[0]
        self.rect.bottom = init_pos[1]

    def update(self):
        pass


class Player(Entity):
    def __init__(self, color=BLUE, init_pos=(0, 0)):
        super(Player, self).__init__(color, init_pos)

        self.rect.centerx = init_pos[0] + WIDTH / 2
        self.rect.bottom = init_pos[1] + HEIGHT - 10
        self.speed = (0, 0)

        self.log = {'attacking': False}
        self.stats = {'attack_speed': 5,
                      'attack': 100}  # min: 0, max: FPS

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
    def __init__(self, color=YELLOW, init_pos=(0, 0)):
        super(Enemy, self).__init__(color, init_pos)

        self.rect.centerx = init_pos[0] + WIDTH / 2
        self.rect.bottom = init_pos[1] + HEIGHT - 100
        self.speed = (0, 0)

        self.log = {'attacking': False}
        self.stats = {'attack_speed': 5,
                      'hp': 1000,
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
