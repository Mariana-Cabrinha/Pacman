import settings
from ghost import Ghost
import random

class Clyde(Ghost):
    def __init__(self, row, col, color='orange'):
        super().__init__(row, col, color)

    def update(self, walls_collide_list, pacman_rect):
        # ghost movement
        available_moves = []
        for key in self.keys:
            if not self.is_collide(*self.directions[key], walls_collide_list):
                available_moves.append(key)

        randomizing = False if len(available_moves) <= 2 and self.direction != (0, 0) else True
        # 60% chance of randomizing ghost move
        if randomizing and random.randrange(0, 100) <= 60:
            self.moving_dir = random.choice(available_moves)
            self.direction = self.directions[self.moving_dir]

        if not self.is_collide(*self.direction, walls_collide_list):
            self.rect.move_ip(self.direction)
        else:
            self.direction = (0, 0)

        # teleporting to the other side of the map
        if self.rect.right <= 0:
            self.rect.x = settings.WIDTH
        elif self.rect.left >= settings.WIDTH:
            self.rect.x = 0

        self._animate()