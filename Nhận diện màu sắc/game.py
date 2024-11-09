import pygame
import sys
import cv2
from detech import *
from scanScreen import ScreenCapture
from API import *

class Game:
    def check_api(self):
        if not API_check():
            print("API key is invalid!")
            sys.exit()

    def __init__(self, image_path, N=10):
        self.check_api()
        
        self.cap = True
        if self.cap:
            self.capturer = ScreenCapture()
            self.capturer.select_region()

        pygame.init()
        self.image_path = image_path
        self.N = N
        self.mode = 0

        # Screen and game dimensions
        screen_info = pygame.display.Info()
        self.screen_height = screen_info.current_h
        self.game_length = self.screen_height - 100
        self.size = self.game_length / self.N

        # Setup screen and colors
        self.screen = pygame.display.set_mode((self.game_length, self.game_length), pygame.RESIZABLE)
        pygame.display.set_caption("Game")
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (80, 80, 80)
        self.BLUE = (29, 160, 230)

        # Load images and scale them
        self.images = [0]
        for i in range(1, 4):
            img = pygame.image.load(f"./assets/game_images/1_{i}.png")
            self.images.append(pygame.transform.scale(img, (self.size, self.size)))
        for i in range(1, 4):
            img = pygame.image.load(f"./assets/game_images/2_{i}.png")
            self.images.append(pygame.transform.scale(img, (self.size, self.size)))

        # Initialize game data and target positions
        self.data = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.target = {"row": 0, "column": 0}
        self.next = self.next_target(self.target)

        self.count = 0

    def update_screen_size(self, new_length):
        self.game_length = new_length
        self.size = self.game_length / self.N
        self.screen = pygame.display.set_mode((self.game_length, self.game_length), pygame.RESIZABLE)


        # Rescale images to new size
        self.images = [0]
        for i in range(1, 4):
            img = pygame.image.load(f"./assets/game_images/1_{i}.png")
            self.images.append(pygame.transform.scale(img, (self.size, self.size)))
        for i in range(1, 4):
            img = pygame.image.load(f"./assets/game_images/2_{i}.png")
            self.images.append(pygame.transform.scale(img, (self.size, self.size)))

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
        self.data = get_data(self.data, image)

    def draw_grid(self):
        for i in range(self.N):
            pygame.draw.line(self.screen, self.BLUE, (0, i * self.size), (self.game_length, i * self.size), 2)
            pygame.draw.line(self.screen, self.BLUE, (i * self.size, 0), (i * self.size, self.game_length), 2)

    def draw_data(self):
        for row in range(self.N):
            for column in range(self.N):
                if self.data[row][column] != 0:
                    self.screen.blit(self.images[self.mode + self.data[row][column]], (column * self.size, row * self.size))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.count += 1
            time_check = 30 * 12 * 60
            if self.count >= time_check:
                print("Checking API key...")
                self.count = 0
                self.check_api()

            if self.cap:
                self.capturer.start_capturing()
            self.load_data()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    # Update screen size on resize
                    self.update_screen_size(max(event.w, event.h))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.mode = 3 - self.mode

            # Fill the screen and draw data and grid
            self.screen.fill(self.WHITE)
            self.draw_data()
            self.draw_grid()
            
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game("./assets/images/image.png")
    game.run()
