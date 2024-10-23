import pygame
import random

class Player:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.width = 514 / 6
        self.height = 486 / 4
        self.x = x
        self.y = y
        self.sprite_sheet = pygame.image.load("a.png").convert_alpha()
        self.current_frame = 0
        self.num_frames = self.sprite_sheet.get_width() // self.width

    def get_sprite(self):
        x = self.current_frame * self.width
        y = 2 * self.height
        width = self.width
        height = self.height

        sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
        return sprite

    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.num_frames:
            self.current_frame = 0
        # self.x += 7
        # self.y -= 3
        if self.x > 800:
            self.x = -100

    def draw(self):
        sprite = self.get_sprite()
        self.screen.blit(sprite, (self.x, self.y))



pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# SPRITE_WIDTH = 93.71
# SPRITE_HEIGHT = 155
clock = pygame.time.Clock()


players = []
for i in range(1):
    x = 50
    y =  i * 100
    player = Player(screen, x, y)
    players.append(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    
    for player in players:
        player.update()
        player.draw()


    pygame.display.flip() # Update màn hình

    clock.tick(10)  # 10 frames per second

# Thoát Pygame
pygame.quit()
