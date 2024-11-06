import pygame
import sys
import cv2
from detech import *
from scanScreen import ScreenCapture

class Game:
    def __init__(self, image_path, N=10):
        # Initialize pygame and screen properties
        pygame.init()
        self.image_path = image_path
        self.N = N

        # Screen and game dimensions
        screen_info = pygame.display.Info()
        self.screen_height = screen_info.current_h
        self.game_length = self.screen_height - 100
        self.size = self.game_length / self.N

        # Setup screen and colors
        self.screen = pygame.display.set_mode((self.game_length, self.game_length))
        pygame.display.set_caption("Game")
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (80, 80, 80)

        # Load images and scale them
        self.images = [0]
        for i in range(1, 4):
            img = pygame.image.load(f"./assets/{i}.png")
            self.images.append(pygame.transform.scale(img, (self.size, self.size)))

        # Initialize game data and target positions
        self.data = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.target = {"row": 0, "column": 0}
        self.next = self.next_target(self.target)

        self.capturer = ScreenCapture()
        self.capturer.select_region()

    def next_target(self, target):
        res = target.copy()
        if res["row"] == self.N:
            return res
        res["column"] += 1
        if res["column"] == self.N:
            res["column"] = 0
            res["row"] += 1
        return res

    def reset_game(self):
        self.data = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.target = {"row": 0, "column": 0}
        self.next = self.next_target(self.target)

    def load_data(self):
        image = cv2.imread(self.image_path)
        self.data = get_color_image(image)
        print(self.data)

    def draw_grid(self):
        for i in range(self.N):
            pygame.draw.line(self.screen, self.BLACK, (0, i * self.size), (self.game_length, i * self.size), 1)
            pygame.draw.line(self.screen, self.BLACK, (i * self.size, 0), (i * self.size, self.game_length), 1)

    def draw_data(self):
        for row in range(self.N):
            for column in range(self.N):
                if self.data[row][column] != 0:
                    self.screen.blit(self.images[self.data[row][column]], (column * self.size, row * self.size))

    def run(self):
        running = True
        while running:
            self.capturer.start_capturing()
            self.load_data()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the screen and draw data and grid
            self.screen.fill(self.WHITE)
            self.draw_data()
            self.draw_grid()
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game("./assets/images/image.png")
    game.run()
