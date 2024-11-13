import random, settings, time
from AI import a_star, manhattan_distance
from blinky import Blinky

class Inky(Blinky):
    def __init__(self, row, col, color='blue'):
        super().__init__(row, col, color)
        self.last_random_time = time.time()  # Inicializa o tempo da última mudança aleatória
        self.random_interval = 2  
        self.p = False

    def update(self, walls_collide_list, pacman_rect):
        inky_pos = (self.rect.x // self.rect.width, self.rect.y // self.rect.height)
        pacman_pos = (pacman_rect.x // pacman_rect.width, pacman_rect.y // pacman_rect.height)
        walls_positions = [(wall.left // self.rect.width, wall.top // self.rect.height) for wall in walls_collide_list]

       
        if time.time() - self.last_random_time > self.random_interval:
            # Atualiza o tempo da última mudança de alvo
            self.last_random_time = time.time()

            # Determina aleatoriamente o comportamento de Inky
        if random.random() < 0.5:
                
            self.p= True
        else:
            self.p= False
        if self.p:
            new_target = pacman_pos
            self.path = a_star(inky_pos, new_target, walls_positions)
        else:
            adjacent_positions = [
                (pacman_pos[0] + 2, pacman_pos[1]),  # Para a direita
                (pacman_pos[0] - 2, pacman_pos[1]),  # Para a esquerda
                (pacman_pos[0], pacman_pos[1] + 2),  # Para baixo
                (pacman_pos[0], pacman_pos[1] - 2)   # Para cima
                ]

                # Filtra as posições válidas (não colide com paredes)
            valid_positions = [pos for pos in adjacent_positions if pos not in walls_positions]

            if valid_positions:
                    # Calcula a distância para cada posição válida
                    distances = [manhattan_distance(inky_pos, pos) for pos in valid_positions]
                    # Escolhe a posição mais distante (para tentar cortar caminho do Pac-Man)
                    new_target = valid_positions[distances.index(max(distances))]
            else:
                    # Se não houver posições válidas, escolhe a posição do Pac-Man
                    new_target = pacman_pos

            # Calcula o caminho para o novo alvo
            self.path = a_star(inky_pos, new_target, walls_positions)

        # Se Inky tem um caminho para seguir
        if self.path:
            # Se ele atingiu a célula central ou ainda não tem alvo
            if self.current_target is None or self.is_at_center_of_cell():
                # Remove a célula atual do caminho
                if inky_pos == self.path[0]:
                    self.path.pop(0)
                # Atualiza o próximo alvo
                self.current_target = self.path[0] if self.path else None

            # Move para o próximo alvo
            if self.current_target is not None:
                self.move_to_next_position(self.current_target, walls_collide_list)

        # Ajusta a posição caso Inky saia dos limites da tela
        if self.rect.right <= 0:
            self.rect.x = settings.WIDTH
        elif self.rect.left >= settings.WIDTH:
            self.rect.x = 0

        # Atualiza a animação de Inky
        self._animate()
