import pygame
import random

class Player:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.sprite_sheet = pygame.image.load("idleR.png").convert_alpha()
        self.current_frame = 0
        self.num_frames = self.sprite_sheet.get_width() // 64

    def get_sprite(self):
        sprite = self.sprite_sheet.subsurface(pygame.Rect(self.current_frame * 64, 0, 64, 64))
        return sprite

    def update(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self):
        sprite = self.get_sprite()
        self.screen.blit(sprite, (self.x, self.y))



pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")

WHITE = (255, 255, 255)

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64
clock = pygame.time.Clock()


players = []
for i in range(10):
    player = Player(screen, random.randint(0, 800 - SPRITE_WIDTH), random.randint(0, 600 - SPRITE_HEIGHT))
    players.append(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    
    for player in players:
        player.update()
        player.draw()


    pygame.display.flip() # Update màn hình

    clock.tick(10)  # 10 frames per second

# Thoát Pygame
pygame.quit()
