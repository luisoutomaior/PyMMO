import pygame
from macros import *
from entities import *



pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hysteresis")
clock = pygame.time.Clock()



players = pygame.sprite.Group()
players.add(Player(BLUE))

enemies = pygame.sprite.Group()
enemies.add(Enemy())

ui = pygame.sprite.Group()

for entity in players:
    ui.add(HealthBar(entity))

for entity in enemies:
    ui.add(HealthBar(entity))

all_sprites = pygame.sprite.Group()
all_sprites.add(players)
all_sprites.add(enemies)
all_sprites.add(ui)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    hits = pygame.sprite.groupcollide(players, enemies, False, False)
    
    if hits:
        for hitting in hits:
            if isinstance(hitting, Player) and hitting.log['attacking']:
                for hitted in hits[hitting]:
                    hitted.receive_damage(CALCULATE_DAMAGE(hitting.stats, 
                                                           hitted.stats,
                                                           NORMAL_ATTACK))

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()