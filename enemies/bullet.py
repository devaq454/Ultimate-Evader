import os
import random

import pygame

from enemies import enemy

WIDTH, HEIGHT = 800, 600
FPS = 60


class Bullet(enemy.Enemy):
    """Класс пули"""

    def __init__(self, screen):
        super().__init__(screen, "data/bullet.png", (80, 30))
        # Где появится пуля. Справа (0), слева (1)
        self.side = random.randrange(0, 2)

        if self.side == 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.generate_position()

        # Скорость пули
        self.speed = 10

    def generate_position(self):
        if self.side == 0:
            # Справа.

            self.rect.x = WIDTH
            self.rect.y = random.randrange(self.floor- 250, self.floor - 35)
        elif self.side == 1:
            # Слева.

            self.rect.x = 0 - self.rect.size[0]
            self.rect.y = random.randrange(self.floor - 250, self.floor - 35)

    def can_move(self) -> bool:
        if self.side == 0:
            # Справа налево.
            return self.rect.x > (0 - self.rect.size[0])
        elif self.side == 1:
            # Слева направо.
            return self.rect.x < WIDTH

    def move(self) -> None:
        if self.side == 0:
            # Справа налево.
            self.rect.x -= self.speed
        elif self.side == 1:
            # Слева направо
            self.rect.x += self.speed
