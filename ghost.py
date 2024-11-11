import pygame
import random
import time
from settings import WIDTH, CHAR_SIZE, GHOST_SPEED

class Ghost(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super().__init__()
        self.abs_x = (row * CHAR_SIZE)
        self.abs_y = (col * CHAR_SIZE)

        self.rect = pygame.Rect(self.abs_x, self.abs_y, CHAR_SIZE, CHAR_SIZE)
        self.move_speed = GHOST_SPEED
        self.color = pygame.Color(color)
        self.move_directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        self.moving_dir = "up"
        self.img_path = f'assets/ghosts/{color}/'
        self.img_name = f'{self.moving_dir}.png'
        self.image = pygame.image.load(self.img_path + self.img_name)
        self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft=(self.abs_x, self.abs_y))
        self.mask = pygame.mask.from_surface(self.image)

        self.directions = {'left': (-self.move_speed, 0), 'right': (self.move_speed, 0),
                           'up': (0, -self.move_speed), 'down': (0, self.move_speed)}
        self.keys = ['left', 'right', 'up', 'down']
        self.direction = (0, 0)

    def move_to_start_pos(self):
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y

    def is_collide(self, x, y, walls_collide_list):
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(walls_collide_list) == -1:
            return False
        return True

    def _animate(self):
        self.img_name = f'{self.moving_dir}.png'
        self.image = pygame.image.load(self.img_path + self.img_name)
        self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def update(self, walls_collide_list, pacman_rect):
        pass  # Este metodo será sobrescrito nas subclasses para lógica de movimento específica.

    def move_towards(self, target_x, target_y, walls_collide_list):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)
        dx, dy = (dx / distance) * self.move_speed, (dy / distance) * self.move_speed
        self.try_move(dx, dy, walls_collide_list)

    def move_away_from(self, target_x, target_y, walls_collide_list):
        dx = self.rect.centerx - target_x
        dy = self.rect.centery - target_y
        distance = max(1, (dx**2 + dy**2)**0.5)
        dx, dy = (dx / distance) * self.move_speed, (dy / distance) * self.move_speed
        self.try_move(dx, dy, walls_collide_list)

    def try_move(self, dx, dy, walls_collide_list):
        if not self.is_collide(dx, dy, walls_collide_list):
            self.rect.move_ip(dx, dy)
        else:
            self.direction = (0, 0)