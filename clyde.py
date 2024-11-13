import math

import settings
from AI import a_star
from ghost import Ghost

class Clyde(Ghost):
    SPEED = 4
    SCARED_DISTANCE = 8  # Distância em células que faz o Clyde fugir

    def __init__(self, row, col, color='orange'):
        super().__init__(row, col, color)
        self.path = []
        self.current_target = None
        # Define o canto inferior esquerdo como ponto de fuga
        self.scatter_corner = (1, settings.HEIGHT // self.rect.height - 2)

    def update(self, walls_collide_list, pacman_rect):
        clyde_pos = (self.rect.x // self.rect.width, self.rect.y // self.rect.height)
        pacman_pos = (pacman_rect.x // pacman_rect.width, pacman_rect.y // pacman_rect.height)
        walls_positions = [(wall.left // self.rect.width, wall.top // self.rect.height) for wall in walls_collide_list]

        # Calcula a distância até o Pacman (em células)
        distance_to_pacman = math.sqrt(
            (clyde_pos[0] - pacman_pos[0]) ** 2 +
            (clyde_pos[1] - pacman_pos[1]) ** 2
        )

        # Define o alvo com base na distância
        target_pos = self.scatter_corner if distance_to_pacman < self.SCARED_DISTANCE else pacman_pos

        # Calcula um novo caminho se necessário
        if not self.path or clyde_pos == self.path[0]:
            self.path = a_star(clyde_pos, target_pos, walls_positions)

        # Segue o caminho calculado, se houver um
        if self.path:
            if self.current_target is None or self.is_at_center_of_cell():
                if clyde_pos == self.path[0]:
                    self.path.pop(0)
                self.current_target = self.path[0] if self.path else None
            if self.current_target is not None:
                self.move_to_next_position(self.current_target, walls_collide_list)

        # Verifica se o Clyde saiu dos limites da tela e ajusta a posição
        if self.rect.right <= 0:
            self.rect.x = settings.WIDTH
        elif self.rect.left >= settings.WIDTH:
            self.rect.x = 0

        self._animate()

    # Os métodos move_to_next_position e is_at_center_of_cell são idênticos aos do Blinky
    def move_to_next_position(self, next_move, walls_collide_list):
        target_center = (next_move[0] * self.rect.width + self.rect.width // 2,
                        next_move[1] * self.rect.height + self.rect.height // 2)

        self.direction = (target_center[0] - self.rect.centerx, target_center[1] - self.rect.centery)

        if self.direction[0] > 0:
            self.moving_dir = "right"
        elif self.direction[0] < 0:
            self.moving_dir = "left"
        elif self.direction[1] > 0:
            self.moving_dir = "down"
        elif self.direction[1] < 0:
            self.moving_dir = "up"

        next_rect = self.rect.move(
            self.direction[0] // abs(self.direction[0]) * self.SPEED if self.direction[0] != 0 else 0,
            self.direction[1] // abs(self.direction[1]) * self.SPEED if self.direction[1] != 0 else 0
        )

        if not any(next_rect.colliderect(wall) for wall in walls_collide_list):
            self.rect = next_rect
        else:
            self.path = []
            self.current_target = None

    def is_at_center_of_cell(self):
        cell_center_x = (self.rect.x // self.rect.width) * self.rect.width + self.rect.width // 2
        cell_center_y = (self.rect.y // self.rect.height) * self.rect.height + self.rect.height // 2
        return self.rect.centerx == cell_center_x and self.rect.centery == cell_center_y