import random

import pygame

import enemies.bullet
from enemies import enemy
from enemies import bullet
from player import Player

NUMBER_ENEMIES = 1


def change_background() -> None:
    """Устанавливает заданный задний фон, зависящий от уровня"""
    ...


def game_over(score) -> None:
    """Надпись Game Over и количество очков"""
    ...


def random_enemy() -> enemy.Enemy:
    choose = random.randrange(0, min(NUMBER_ENEMIES, level))
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
final_score = -1
last_score = 0
level = 1
is_game_over = False

# максимальное время респавна снарядов
respawn_ticks = 4 * fps

# сколько осталось до респавна
ticks_to_spawn = 0
player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while running:
    # пока игра работает
    if not is_game_over:
        tick += 1

        # каждые 60 * 2 - уровень кадров увеличивать очки на единицу
        if tick % (fps * 2 - level) <= 0:
            score += 1

        respawn_ticks = max(4 * 60 - score, 120)

        if level % 2 == 0:
            # каждые 2 уровня изменять задний фон
            change_background()

        level = score // 10 + 1

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

    if is_game_over:
        # остановить все спрайты; вывести на экран количество очков и надпись: "Game over"
        if final_score == -1:
            final_score = score

    else:
        screen.fill((0, 0, 0))
        # Отображение очков
        font = pygame.font.Font(None, 35)
        text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (50, 50))

        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
    clock.tick(fps)
pygame.quit()
