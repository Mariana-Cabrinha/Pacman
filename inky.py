from ghost import Ghost
import random
from settings import WIDTH

class Inky(Ghost):
    def __init__(self, row, col, color='blue', blinky=None):
        super().__init__(row, col, color)
        self.blinky = blinky  # Armazena uma referência ao objeto Blinky

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
            self.rect.x = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.x = 0

        self._animate()