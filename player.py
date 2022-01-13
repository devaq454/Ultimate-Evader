import pygame

WIDTH, HEIGHT = 800, 600

# Координата Y у платформы
FLOOR = 500


class Player(pygame.sprite.Sprite):
    """Класс игрока"""

    def __init__(self) -> None:
        """Инициализация класса"""

        pygame.sprite.Sprite.__init__(self)
        self.side = 60
        self.image = pygame.image.load("data/ball.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.side, self.side))
        self.rect = self.image.get_rect()
        self.rect.size = (self.side, self.side)
        print(self.rect.size)
        self.tick = 0
        self.rect.center = 400, 300
        self.speed_fall = 8
        self.left = False
        self.right = False
        self.is_jump = False
        self.speed = 10
        self.jump_ticks = 30

        self.direction = [0, 0]

    def key_left(self) -> None:
        """Установка флага, что игрок двигается влево"""

        self.left = True

    def key_right(self) -> None:
        """Установка флага, что игрок двигается вправо"""

        self.right = True

    def key_jump(self) -> None:
        """Прыжок"""

        if self.check_in_floor():
            # Если игрок на полу, то совершить прыжок
            self.is_jump = True
            self.jump_ticks = 44

    def move_left(self) -> None:
        """Изменение координаты x при движении влево"""

        self.rect.x = max(self.rect.x - self.speed, 0)

    def move_right(self) -> None:
        """Изменение координаты x при движении вправо"""

        self.rect.x = min(self.rect.x + self.speed, WIDTH - self.side)

    def check_in_floor(self) -> bool:
        """Находится ли игрок на платформе"""

        if self.rect.y >= FLOOR - self.side:
            return True
        return False

    def update(self) -> None:
        """Вызывается каждый кадр группой спрайтов"""

        self.tick += 1
        # каждый второй кадр пропускать
        if self.tick % 2 == 0:
            return

        if self.left:
            self.move_left()
        if self.right:
            self.move_right()

        # Прыжок
        if self.is_jump:
            if self.jump_ticks == 0:
                self.is_jump = False
            else:
                self.rect.y -= self.jump_ticks
                self.jump_ticks -= 1

        # Гравитация
        if not self.check_in_floor():
            self.rect.y += self.speed_fall
            self.speed_fall += 2
            if self.check_in_floor():
                # Если Y ниже платформы, то установить игрока на платформу
                self.speed_fall = 2
                self.rect.y = FLOOR - self.side
