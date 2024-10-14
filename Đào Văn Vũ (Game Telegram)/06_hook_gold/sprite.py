import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hiển thị nhiều nhân vật từ Sprite Sheet")

WHITE = (255, 255, 255)

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64

sprite_sheet = pygame.image.load("idleR.png").convert_alpha()

def get_sprite(frame):
    sprite = sprite_sheet.subsurface(pygame.Rect(frame * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT))
    return sprite

current_frame = 0
num_frames = sprite_sheet.get_width() // SPRITE_WIDTH 
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    sprite = get_sprite(current_frame)
    screen.blit(sprite, (400, 300)) 

    current_frame = (current_frame + 1) % num_frames

    pygame.display.flip()

    clock.tick(10)  # 10 frames per second

# Thoát Pygame
pygame.quit()
