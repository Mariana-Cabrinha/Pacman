import heapq

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star(start, goal, walls_collide_list, directions):
    # Implementação do algoritmo A* para encontrar o caminho do fantasma até o pacman
    open_list = []
    closed_list = set()
    came_from = {}

    # Iniciar o open list com a posição inicial
    heapq.heappush(open_list, (0 + manhattan_distance(start, goal), 0, start))  # (f, g, position)
    g_score = {start: 0}

    while open_list:
        _, current_g, current = heapq.heappop(open_list)

        if current == goal:
            # Reconstruir o caminho
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        closed_list.add(current)

        # Explorar os vizinhos
        for direction in directions.values():
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            # Ignorar se o vizinho for uma parede ou já foi visitado
            if neighbor in closed_list or not is_valid_move(neighbor, walls_collide_list):
                continue

            tentative_g_score = current_g + 1  # O custo é 1 para cada movimento

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                heapq.heappush(open_list, (
                    tentative_g_score + manhattan_distance(neighbor, goal), tentative_g_score, neighbor))

def is_valid_move(position, walls_collide_list):
    # Verifique se a posição não colide com as paredes
    return position not in walls_collide_list