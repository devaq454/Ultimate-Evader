import random

import pygame

import enemies.bullet
from player import Player

from enemies import *

NUMBER_ENEMIES = 1


def change_background() -> None:
    """Устанавливает заданный задний фон, зависящий от уровня"""
    ...


def random_enemy() -> enemies.enemy.Enemy:
    choose = random.randrange(0, NUMBER_ENEMIES)
    if choose == 0:
        return enemies.bullet.Bullet(screen)


pygame.init()
size = w, h = 800, 600
screen = pygame.display.set_mode(size)

fps = 60
tick = 0
clock = pygame.time.Clock()
running = True
score = 0
last_score = 0
level = 0

# максимальное время респавна снарядов
respawn_ticks = 4 * fps

# сколько осталось до респавна
ticks_to_spawn = 0
player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while running:
    # пока игра работает
    tick += 1

    # каждые 60 * 2 - уровень кадров увеличивать очки на единицу
    if tick % (fps * 2 - level) <= 0:
        score += 1

    respawn_ticks = max(4 * 60 - score, 120)

    if level % 2 == 0:
        # каждые 2 уровня изменять задний фон
        change_background()

    level = score // 10

    if ticks_to_spawn == 0:
        # если пришло время респавна
        all_sprites.add(random_enemy())
        ticks_to_spawn = random.randrange(60, respawn_ticks)
    else:
        ticks_to_spawn -= 1

    if tick % 60 == 0:
        print(f"{score=} {tick=} {ticks_to_spawn=} {respawn_ticks=} {level=}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.key_left()
            if event.key == pygame.K_RIGHT:
                player.key_right()
            if event.key == pygame.K_UP:
                player.key_jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left = False
            if event.key == pygame.K_RIGHT:
                player.right = False
    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
