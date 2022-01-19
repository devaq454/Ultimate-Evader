import random

import pygame

from enemies import enemy

WIDTH, HEIGHT = 800, 600
FPS = 60


class Meteor(enemy.Enemy):
    """Класс метеора"""

    def __init__(self, screen):
        super().__init__(screen, "data/bullet.png", (80, 30))

        self.generate_position()

        # Скорость пули
        self.speed = 10

    def generate_position(self):
        self.rect.x = random.randrange(10, WIDTH - self.rect.size[0] - 10)
        self.rect.y = HEIGHT - self.rect.size[1]

    def can_move(self) -> bool:
        return self.rect.y <= self.floor - self.rect.size[1]

    def move(self) -> None:
        self.rect.y += self.speed
