import heapq
import time

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

MAX_CALCULATION_TIME = 0.1  # Limite de tempo para cálculo do A*

def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def a_star(start, goal, walls_collide_list, ):
    start_time = time.time()
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}
    walls_set = set(walls_collide_list)

    while open_set and time.time() - start_time < MAX_CALCULATION_TIME:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            return reconstruct_path(came_from, current)

        for move in DIRECTIONS.values():
            neighbor = (current[0] + move[0], current[1] + move[1])

            if neighbor in walls_set or neighbor[0] < 0 or neighbor[1] < 0:
                continue

            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Retorna uma lista vazia se nenhum caminho for encontrado

def is_collide_with_wall(self, position, walls_collide_list):
    test_rect = self.rect.copy()
    test_rect.topleft = (position[0] * self.rect.width, position[1] * self.rect.height)
    return any(test_rect.colliderect(wall) for wall in walls_collide_list)

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    return path[::-1]  # Inverte o caminho para que ele comece do início

def is_valid_move(position, walls_collide_list):
    # Verifique se a posição não colide com as paredes
    return position not in walls_collide_list