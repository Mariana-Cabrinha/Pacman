import time
from ghost import Ghost
from blinky import Blinky
import random
from settings import WIDTH
from AI import a_star

class Inky(Blinky):
    def __init__(self, row, col, color='blue'):
        super().__init__(row, col, color)
        self.last_random_time = time.time()  # Inicializa o tempo da última mudança aleatória
        self.random_interval = 2  # Intervalo de 2 segundos
        self.p = False

    def update(self, walls_collide_list, pacman_rect):
        inky_pos = (self.rect.x // self.rect.width, self.rect.y // self.rect.height)  # Posição do Inky
        pacman_pos = (pacman_rect.x // pacman_rect.width, pacman_rect.y // pacman_rect.height)  # Posição do PacMan
        walls_positions = [(wall.left // self.rect.width, wall.top // self.rect.height) for wall in walls_collide_list]

        # Verifica se o intervalo de tempo passou (2 segundos)
        if time.time() - self.last_random_time > self.random_interval:
            # Atualiza o tempo da última mudança de alvo
            self.last_random_time = time.time()

            # Determina aleatoriamente o comportamento de Inky
            if random.random() < 0.5:  # 50% de chance de ir para o PacMan ou para uma casa próxima
                # Inky vai atrás do PacMan
                new_target = pacman_pos
            else:
                # Inky vai para uma casa próxima ao PacMan
                # Definindo as 4 posições adjacentes possíveis
                adjacent_positions = [
                    (pacman_pos[0] + 4, pacman_pos[1]),  # direita
                    (pacman_pos[0] - 4, pacman_pos[1]),  # esquerda
                    (pacman_pos[0], pacman_pos[1] + 4),  # abaixo
                    (pacman_pos[0], pacman_pos[1] - 4)   # acima
                ]
                
                # Filtra as posições válidas (não colidindo com paredes)
                valid_positions = [pos for pos in adjacent_positions if pos not in walls_positions]
                
                # Se existirem posições válidas, escolhe a mais próxima do PacMan
                if valid_positions:
                    # Calcula a distância para cada posição válida
                    distances = [self._calculate_distance(pacman_pos, pos) for pos in valid_positions]
                    # Escolhe a posição com a menor distância
                    new_target = valid_positions[distances.index(min(distances))]
                else:
                    # Se não houver posições válidas, escolhe a posição do PacMan
                    new_target = pacman_pos

            # Calcula o caminho para o novo alvo
            self.path = a_star(inky_pos, new_target, walls_positions)

        # Segue o caminho calculado, se houver um
        if self.path:
            if self.current_target is None or self.is_at_center_of_cell():
                if inky_pos == self.path[0]:
                    self.path.pop(0)
                self.current_target = self.path[0] if self.path else None
            if self.current_target is not None:
                self.move_to_next_position(self.current_target, walls_collide_list)
        else:
            print("Nenhum caminho encontrado ou o caminho está vazio")

        # Verifica se o Inky saiu dos limites da tela e ajusta a posição
        if self.rect.right <= 0:
            self.rect.x = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.x = 0

        self._animate()

    def _calculate_distance(self, pos1, pos2):
        """Calcula a distância entre duas posições."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])  # Distância Manhattan
