import random

import pygame

from enemies import enemy, bullet, meteor
from player import Player

NUMBER_ENEMIES = 2


class GameScene:
    """Статичный класс игровой сцены"""

    width, height = 800, 600
    @classmethod
    def change_background(cls) -> pygame.Surface:
        """Устанавливает заданный задний фон, зависящий от уровня"""
        global background
        background = pygame.image.load('data/background.png')
        background = pygame.transform.scale(background, (w, h))
        return background

    @classmethod
    def game_over(cls) -> None:
        """Стирает все, кроме заднего фона и спрайтов"""
        global status_pause
        status_pause = True
        font = pygame.font.Font(None, 80)
        color = (50, 50, 200)
        text_game_over = font.render("Game over", True, color)
        text_score = font.render(f"Score: {final_score}", True, color)
        font = pygame.font.Font(None, 50)
        text_key_restart = font.render("Press R to restart", True, color)
        screen.blit(text_game_over, (250, 100))
        screen.blit(text_score, (300, 200))
        screen.blit(text_key_restart, (20, cls.height - 80))

    @classmethod
    def draw_background(cls) -> None:
        """Каждый кадр рисует задний фон"""
        screen.blit(background, (0, 0))

    @classmethod
    def random_enemy(cls) -> enemy.Enemy:
        """Возвращает случайного противника"""
        choose = random.randrange(0, min(NUMBER_ENEMIES, level))
        if choose == 0:
            return bullet.Bullet(screen)
        if choose == 1:
            return meteor.Meteor(screen)

    @classmethod
    def draw_sprites(cls) -> None:
        """Рисует все спрайты"""
        global status_pause
        if not status_pause:
            group_enemies.update()
        group_enemies.draw(screen)
        group_player.draw(screen)

    @classmethod
    def switch_pause(cls) -> None:
        """Ставит или снимает с паузы"""
        global status_pause
        status_pause = not status_pause

    @classmethod
    def start(cls) -> None:
        """Все настройки устанавливает в значения по умолчанию"""
        global tick, background, running, score, status_pause, final_score, level, last_level, is_game_over, respawn_ticks, ticks_to_spawn, player, group_enemies, group_player
        tick = 0
        running = True
        # Статус паузы
        status_pause = True
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
        background = GameScene.change_background()


pygame.init()
size = w, h = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ultimate Evader")

fps = 60
clock = pygame.time.Clock()

# значения по умолчанию
tick = 0
background = GameScene.change_background()
running = True
# Статус паузы
status_pause = True
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
    if not status_pause:
        tick += 1

        # каждые (60 * 2 - уровень) кадров увеличивать очки на единицу
        if tick % (fps * 2 - level) <= 0:
            score += 1

        if level % 2 == 0 and last_level != level:
            # каждые 2 уровня изменять задний фон
            last_level = level
            GameScene.change_background()

        level = score // 10 + 1

        enemy.Enemy.time_prediction = max(30, 2 * fps - level * 5)

        if ticks_to_spawn == 0:
            # если пришло время респавна
            respawn_ticks = max(4 * 60 - score, 120)
            group_enemies.add(GameScene.random_enemy())
            ticks_to_spawn = random.randrange(respawn_ticks // 8,
                                              respawn_ticks // 2)
            print(ticks_to_spawn)
        else:
            ticks_to_spawn -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if status_pause is True and is_game_over is False:
                # Снятие паузы вначале игры
                status_pause = False
            if is_game_over and event.key == pygame.K_r:
                # Рестарт игры
                GameScene.start()
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

    GameScene.draw_background()
    if is_game_over:
        # остановить все спрайты,
        # вывести на экран количество очков и надпись: "Game over"
        if final_score == -1:
            final_score = score
        GameScene.game_over()
    if not status_pause:
        group_player.update()
    if not is_game_over:
        # Отображение очков
        font = pygame.font.Font(None, 35)
        text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (50, 50))

        if pygame.sprite.spritecollide(player, group_enemies, False):
            is_game_over = True
    # Вывод на экран всех спрайтов и задний фон
    GameScene.draw_sprites()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
