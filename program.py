import random

import pygame

import enemies.bullet
from enemies import enemy
from player import Player

NUMBER_ENEMIES = 1


class GameScene:
    """Статичный класс игровой сцены"""

    @staticmethod
    def change_background() -> pygame.Surface:
        """Устанавливает заданный задний фон, зависящий от уровня"""
        background = pygame.image.load('data/background.png')
        background = pygame.transform.scale(background, (w, h))
        return background

    @staticmethod
    def game_over() -> None:
        """Стирает все, кроме заднего фона и спрайтов"""
        GameScene.draw_background()
        group_enemies.draw(screen)
        group_player.draw(screen)
        font = pygame.font.Font(None, 80)
        text_game_over = font.render("Game over", True, (50, 50, 200))
        text_score = font.render(f"Score: {final_score}", True, (50, 50, 200))
        screen.blit(text_game_over, (250, 200))
        screen.blit(text_score, (300, 300))

    @staticmethod
    def draw_background() -> None:
        """Каждый кадр рисует задний фон"""
        screen.blit(background, (0, 0))

    @staticmethod
    def random_enemy() -> enemy.Enemy:
        """Возвращает случайного противника"""
        choose = random.randrange(0, min(NUMBER_ENEMIES, level))
        if choose == 0:
            return enemies.bullet.Bullet(screen)


pygame.init()
size = w, h = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ultimate Evader")

fps = 60
tick = 0
clock = pygame.time.Clock()
background = GameScene.change_background()
running = True
score = 0
final_score = -1
level = 1
# последний лвл, когда изменялся задний фон
last_level = -1
is_game_over = False

# максимальное время респавна снарядов
respawn_ticks = 4 * fps

# сколько осталось до респавна
ticks_to_spawn = 0
player = Player()

group_player = pygame.sprite.Group()
group_player.add(player)
group_enemies = pygame.sprite.Group()

while running:
    # пока игра работает
    if not is_game_over:
        tick += 1

        # каждые (60 * 2 - уровень) кадров увеличивать очки на единицу
        if tick % (fps * 2 - level) <= 0:
            score += 1

        if level % 2 == 0 and last_level != level:
            # каждые 2 уровня изменять задний фон
            last_level = level
            GameScene.change_background()

        level = score // 10 + 1

        if ticks_to_spawn == 0:
            # если пришло время респавна
            respawn_ticks = max(4 * 60 - score, 120)
            group_enemies.add(GameScene.random_enemy())
            ticks_to_spawn = random.randrange(respawn_ticks // 4, respawn_ticks)
        else:
            ticks_to_spawn -= 1

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
        # остановить все спрайты,
        # вывести на экран количество очков и надпись: "Game over"
        if final_score == -1:
            final_score = score
        GameScene.game_over()

    else:
        # Задний фон
        GameScene.draw_background()
        # Отображение очков
        font = pygame.font.Font(None, 35)
        text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (50, 50))

        group_enemies.update()
        group_player.update()
        group_player.draw(screen)
        group_enemies.draw(screen)

        if pygame.sprite.spritecollide(player, group_enemies, False):
            is_game_over = True
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
