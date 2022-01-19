import pygame
from data1 import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, dot_speed):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == 'available':
            self.image.fill('red')
        else:
            self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx - (dot_speed / 2), self.rect.centery - (dot_speed / 2), dot_speed, dot_speed)

class Dot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos


class Level_map:
    def __init__(self, start_level, max_level, surface, create_level):

        self.display_surface = surface
        self.max_level =  max_level
        self.current_level = start_level
        self.create_level = create_level

        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8

        self.setup_nodes()
        self.setup_dot()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed)
            else:
                node_sprite = Node(node_data['node_pos'], 'unavailable', self.speed)
            self.nodes.add(node_sprite)

    def draw_the_paths(self):
        points = [node['node_pos']for index, node in enumerate(levels.values()) if index <= self.max_level]
        pygame.draw.lines(self.display_surface, 'red', False, points, 6)

    def setup_dot(self):
        self.dot = pygame.sprite.GroupSingle()
        dot_sprite = Dot(self.nodes.sprites()[self.current_level].rect.center)
        self.dot.add(dot_sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def update_dot_pos(self):
        if self.moving and self.move_direction:
            self.dot.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.dot.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        self.input()
        self.update_dot_pos()
        self.dot.update()
        self.draw_the_paths()
        self.nodes.draw(self.display_surface)
        self.dot.draw(self.display_surface)
