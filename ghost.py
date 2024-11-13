import math, pygame, settings
from settings import CHAR_SIZE, GHOST_SPEED

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

class PinkGhost(Ghost):
    def __init__(self, row, col):
        super().__init__(row, col, "pink")
        self.target_offset = 4 * CHAR_SIZE  # 4 células à frente

    def calculate_target_position(self, pacman_rect, pacman_direction):
        """Calcula a posição alvo 4 células à frente do Pac-Man"""
        # Converte a direção do pacman em um offset
        direction_to_offset = {
            'up': (0, -self.target_offset),
            'down': (0, self.target_offset),
            'left': (-self.target_offset, 0),
            'right': (self.target_offset, 0)
        }

        offset_x, offset_y = direction_to_offset.get(pacman_direction, (0, 0))
        target_x = pacman_rect.centerx + offset_x
        target_y = pacman_rect.centery + offset_y

        # Garante que o alvo está dentro dos limites da tela
        target_x = max(0, min(target_x, settings.WIDTH - CHAR_SIZE))
        target_y = max(0, min(target_y, settings.WIDTH - CHAR_SIZE))

        return target_x, target_y

    def euclidean_distance(self, pos1, pos2):
        # Calcula a distância Euclidiana entre duas posições
        x1, y1 = pos1
        x2, y2 = pos2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def get_best_move(self, walls_collide_list, current_pos, target_pos):
        # Implementa a busca gulosa para encontrar o melhor movimento
        possible_moves = [
            ('left', (-self.move_speed, 0)),
            ('right', (self.move_speed, 0)),
            ('up', (0, -self.move_speed)),
            ('down', (0, self.move_speed))
        ]

        best_move = None
        best_distance = float('inf')

        for direction, (dx, dy) in possible_moves:
            if not self.is_collide(dx, dy, walls_collide_list):
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)
                distance = self.euclidean_distance(new_pos, target_pos)

                if distance < best_distance:
                    best_distance = distance
                    best_move = (dx, dy)
                    self.moving_dir = direction

        return best_move

    def update(self, walls_collide_list, pacman_rect, pacman_direction):
        # Atualiza a posição do fantasma usando busca gulosa
        current_pos = (self.rect.centerx, self.rect.centery)
        target_pos = self.calculate_target_position(pacman_rect, pacman_direction)

        best_move = self.get_best_move(walls_collide_list, current_pos, target_pos)

        if best_move:
            dx, dy = best_move
            self.try_move(dx, dy, walls_collide_list)
            self._animate()