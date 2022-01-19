import pygame
import sys
from parameters import *
from level_map import Level_map


class Game:
    def __init__(self):
        self.max_level = 2
        self.level_map = Level_map(1, self.max_level, screen)

    def run(self):
        self.level_map.run()


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('black')
    game.run()

    pygame.display.update()
    clock.tick(60)


