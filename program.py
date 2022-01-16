import math

import pygame

import enemies.bullet
from player import Player

from enemies import *


def main():
    pygame.init()
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)

    fps = 60
    tick = 0
    clock = pygame.time.Clock()
    running = True
    player = Player()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    while running:
        tick += 1

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


if __name__ == '__main__':
    main()
