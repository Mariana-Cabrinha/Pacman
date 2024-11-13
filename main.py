import pygame, sys
from settings import WIDTH, HEIGHT, NAV_HEIGHT, MAPS, CHAR_SIZE
from world import World

pygame.init()

class Main:
    def __init__(self):
        self.FPS = pygame.time.Clock()
        self.screen = None
        self.current_level = 0
        self.load_level(self.current_level)

    def load_level(self, level):
        map_data = MAPS[level]
        width = len(map_data[0]) * CHAR_SIZE
        height = len(map_data) * CHAR_SIZE
        self.screen = pygame.display.set_mode((width, height + NAV_HEIGHT))
        self.world = World(self.screen, level + 1)

    def main(self):
        while True:
            self.screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.world.update()

            # Verifica se deve passar para o próximo nível
            if self.world.next_level():
                self.current_level = (self.current_level + 1) % len(MAPS)
                self.load_level(self.current_level)

            pygame.display.update()
            self.FPS.tick(30)

if __name__ == "__main__":
    play = Main()
    play.main()