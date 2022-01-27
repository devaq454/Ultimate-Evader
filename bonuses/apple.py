import random

import pygame

WIDTH, HEIGHT = 800, 600
FLOOR = 513
FPS = 60


class Apple(pygame.sprite.Sprite):
    """Класс бонуса яблока"""
    # время продложительности показа яблока

    def __init__(self, screen: pygame.Surface) -> None:
        """Инициализация"""
        self.ticks_show = 120
        pygame.sprite.Sprite.__init__(self)
        self.size = 50
        self.image = pygame.image.load("data/apple.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.screen = screen

        self.generate_position()

    def generate_position(self) -> None:
        """Генерирует позицию у пола"""
        self.rect.x = random.randrange(self.size, WIDTH - self.size)
        self.rect.y = FLOOR - self.size - 3

    def update(self) -> None:
        if self.ticks_show <= 0:
            self.kill()
        self.ticks_show -= 1
