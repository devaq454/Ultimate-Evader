from abc import ABC, abstractmethod

import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60


class Enemy(pygame.sprite.Sprite, ABC):
    """Класс родитель для снарядов."""

    # время предсказывания снаряда.
    time_prediction = 2 * FPS

    def __init__(self, screen: pygame.Surface, path_image: str,
                 size: tuple) -> None:
        """Инициализация."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.screen = screen

        # self.generate_position()

        # Кадров до появления
        self.ticks_to_show = 3 * FPS

    @abstractmethod
    def can_move(self) -> bool:
        """Возвращяет True, пока снаряд может двигаться."""

    @abstractmethod
    def generate_position(self) -> None:
        """Создание начального положения"""

    def get_prediction(self) -> tuple:
        """Возвращает место появления снаряда."""

        if self.rect.y <= (0 - self.rect.size[1]):
            # Сверху.
            x = self.rect.x
            y = 0
            length_x = self.rect.size[0]
            length_y = 5
        elif self.rect.x >= WIDTH + self.rect.size[0]:
            # Справа.
            x = WIDTH - 5
            y = self.rect.y
            length_x = 6
            length_y = self.rect.size[1]
        else:
            # Слева.
            # self.rect.x <= (0 - self.rect.size[0])
            x = 0
            y = self.rect.y
            length_x = 5
            length_y = self.rect.size[1]
        rect = (x, y, length_x, length_y)
        return rect

    def draw_prediction(self) -> None:
        """Рисует предсказание места появления."""
        rect = self.get_prediction()
        # TODO
        pygame.draw.rect(self.screen, (255, 0, 0), rect)

    @abstractmethod
    def move(self) -> None:
        """Двигает снаряд."""

    def update(self) -> None:
        """Вызывается каждый кадр группой спрайтов."""
        if self.ticks_to_show == 0:
            # если объект появился
            if self.can_move():
                self.move()
            else:
                self.kill()
        else:
            if self.ticks_to_show <= self.time_prediction:
                # создание предсказания место появления снаряда
                self.draw_prediction()
            self.ticks_to_show -= 1
