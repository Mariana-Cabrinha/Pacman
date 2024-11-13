import settings
from ghost import Ghost
import math
from settings import CHAR_SIZE

class Pinky(Ghost):
    def __init__(self, row, col, color='pink'):
        super().__init__(row, col, color)
        self.target_offset = 4 * CHAR_SIZE
        self.last_move = None
        self.stuck_counter = 0  # Contador para detectar quando está preso

    def calculate_target_position(self, pacman_rect, pacman_status):
        # Se estiver no respawn ou parado por muito tempo, mira diretamente no Pac-Man
        if (self.rect.x == self.abs_x and self.rect.y == self.abs_y) or self.stuck_counter > 10:
            return pacman_rect.centerx, pacman_rect.centery

        direction_to_offset = {
            'up': (0, -self.target_offset),
            'down': (0, self.target_offset),
            'left': (-self.target_offset, 0),
            'right': (self.target_offset, 0),
            'idle': (0, 0)
        }

        # Se o Pac-Man estiver parado, calcula um offset baseado na posição relativa
        if pacman_status == 'idle':
            dx = pacman_rect.centerx - self.rect.centerx
            dy = pacman_rect.centery - self.rect.centery
            if abs(dx) > abs(dy):
                pacman_status = 'right' if dx > 0 else 'left'
            else:
                pacman_status = 'down' if dy > 0 else 'up'

        offset_x, offset_y = direction_to_offset.get(pacman_status, (0, 0))
        target_x = pacman_rect.centerx + offset_x
        target_y = pacman_rect.centery + offset_y

        target_x = max(CHAR_SIZE, min(target_x, settings.WIDTH - CHAR_SIZE))
        target_y = max(CHAR_SIZE, min(target_y, settings.HEIGHT - CHAR_SIZE))

        return target_x, target_y

    def get_available_moves(self, walls_collide_list):
        available_moves = []
        for key, direction in self.directions.items():
            if not self.is_collide(*direction, walls_collide_list):
                available_moves.append(key)
        return available_moves

    def update(self, walls_collide_list, pacman_rect):
        pacman_status = getattr(pacman_rect, 'status', 'idle')

        # Verifica se está na posição inicial
        is_at_spawn = (self.rect.x == self.abs_x and self.rect.y == self.abs_y)

        # Calcula o ponto alvo
        target_x, target_y = self.calculate_target_position(pacman_rect, pacman_status)

        # Obtém movimentos disponíveis
        available_moves = self.get_available_moves(walls_collide_list)

        if not available_moves:
            self.direction = (0, 0)
            self.stuck_counter += 1
            return

        # Se estiver no spawn, prioriza movimento para cima
        if is_at_spawn and 'up' in available_moves:
            best_move = 'up'
        else:
            # Encontra o melhor movimento usando busca gulosa
            best_move = None
            best_distance = float('inf')

            for move in available_moves:
                direction = self.directions[move]
                new_x = self.rect.centerx + direction[0]
                new_y = self.rect.centery + direction[1]

                distance = math.sqrt((target_x - new_x)**2 + (target_y - new_y)**2)

                # Evita reverter direção a menos que seja necessário
                if self.last_move:
                    opposite_moves = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
                    if move == opposite_moves.get(self.last_move) and len(available_moves) > 1:
                        continue

                if distance < best_distance:
                    best_distance = distance
                    best_move = move

        # Executa o movimento
        if best_move:
            self.moving_dir = best_move
            self.direction = self.directions[best_move]
            self.rect.move_ip(self.direction)
            self.last_move = best_move
            self.stuck_counter = 0  # Reset do contador quando se move
        else:
            # Se não encontrou movimento válido, escolhe qualquer um disponível
            move = available_moves[0]
            self.moving_dir = move
            self.direction = self.directions[move]
            self.rect.move_ip(self.direction)
            self.last_move = move
            self.stuck_counter = 0

        # Teleporting to the other side of the map
        if self.rect.right <= 0:
            self.rect.x = settings.WIDTH
        elif self.rect.left >= settings.WIDTH:
            self.rect.x = 0

        self._animate()