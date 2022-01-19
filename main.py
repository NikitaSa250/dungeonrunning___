import pygame
import sys
from parameters import *
from level_map import Level_map
from level import Level


class Game:
    def __init__(self):
        self.max_level = 2
        self.level_map = Level_map(1, self.max_level, screen, self.create_level)
        self.status = 'level map'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_level_map)
        self.status = 'level'

    def create_level_map(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.level_map = Level_map(current_level, self.max_level, screen, self.create_level)
        self.status = 'level map'

    def run(self):
        if self.status == 'level map':
            self.level_map.run()
        else:
            self.level.run()


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


