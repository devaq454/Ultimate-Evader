from abc import ABC, abstractmethod

import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60


class Enemy(pygame.sprite.Sprite, ABC):  # TODO мб поменять порядок
    """Класс родитель для снарядов."""

    # время предсказывания снаряда.
    time_prediction = 1 * FPS

    def __init__(self, screen, path_image: str = None) -> None:
        """Инициализация."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path_image)
        self.rect = self.image.get_rect()
        self.screen = screen

        # Кадров до появления
        self.ticks_to_show = 3 * FPS

    @abstractmethod
    def can_move(self) -> bool:
        """Возвращяет true, пока снаряд может двигаться."""
        ...

    def create_prediction(self):
        """Создает место появления снаряда"""
        pygame.draw.rect(self.screen, (255, 0, 0), (WIDTH - 5, self.rect.y,
                                                    6, self.rect.y))

    @abstractmethod
    def move(self) -> None:
        """Двигает снаряд."""
        ...

    def update(self):
        """Вызывается каждый кадр группой спрайтов."""

        if self.ticks_to_show == 0:
            # если объект появился
            if self.can_move():
                self.move()
            else:
                self.kill()
        else:
            if self.ticks_to_show <= self.time_prediction:
                # создания предсказания место появления снаряда
                self.create_prediction()
            self.ticks_to_show -= 1
