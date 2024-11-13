import settings
from AI import a_star, is_collide_with_wall
from ghost import Ghost
from settings import WIDTH

class Blinky(Ghost):
    SPEED = 4  # Velocidade para Blinky

    def __init__(self, row, col, color='red'):
        super().__init__(row, col, color)
        self.path = []
        self.current_target = None

    def update(self, walls_collide_list, pacman_rect):
        blinky_pos = (self.rect.x // self.rect.width, self.rect.y // self.rect.height) # Posição do Blinky
        pacman_pos = (pacman_rect.x // pacman_rect.width, pacman_rect.y // pacman_rect.height) # Posição do PacMan
        walls_positions = [(wall.left // self.rect.width, wall.top // self.rect.height) for wall in walls_collide_list] # Posições das paredes

        # Calcula um novo caminho se o Blinky não tiver um ou se já chegou ao destino
        if not self.path or blinky_pos == self.path[0]:
            self.path = a_star(blinky_pos, pacman_pos, walls_positions)

        # Segue o caminho calculado, se houver um
        if self.path:
            if self.current_target is None or self.is_at_center_of_cell():
                if blinky_pos == self.path[0]:
                    self.path.pop(0)
                self.current_target = self.path[0] if self.path else None
            if self.current_target is not None:
                self.move_to_next_position(self.current_target, walls_collide_list)

        # Verifica se o Blinky saiu dos limites da tela e ajusta a posição
        if self.rect.right <= 0:
            self.rect.x = settings.WIDTH
        elif self.rect.left >= settings.WIDTH:
            self.rect.x = 0

        self._animate()

    def move_to_next_position(self, next_move, walls_collide_list):
        # Calcula o próximo centro do alvo
        target_center = (next_move[0] * self.rect.width + self.rect.width // 2, next_move[1] * self.rect.height + self.rect.height // 2)

        # Define a direção do movimento
        self.direction = (target_center[0] - self.rect.centerx, target_center[1] - self.rect.centery)

        if self.direction[0] > 0:
            self.moving_dir = "right"
        elif self.direction[0] < 0:
            self.moving_dir = "left"
        elif self.direction[1] > 0:
            self.moving_dir = "down"
        elif self.direction[1] < 0:
            self.moving_dir = "up"

        # Calcula o próximo retângulo de posição
        next_rect = self.rect.move(self.direction[0] // abs(self.direction[0]) * self.SPEED if self.direction[0] != 0 else 0,
                                   self.direction[1] // abs(self.direction[1]) * self.SPEED if self.direction[1] != 0 else 0)

        # Verifica se há colisão com a parede
        if not any(next_rect.colliderect(wall) for wall in walls_collide_list):
            self.rect = next_rect
        else:
            self.path = []  # Limpa o caminho em caso de colisão
            self.current_target = None  # Limpa o alvo em caso de colisão

    def is_at_center_of_cell(self):
        # Calcula o centro da célula atual
        cell_center_x = (self.rect.x // self.rect.width) * self.rect.width + self.rect.width // 2
        cell_center_y = (self.rect.y // self.rect.height) * self.rect.height + self.rect.height // 2
        return self.rect.centerx == cell_center_x and self.rect.centery == cell_center_y