import pygame 

pygame.init()

screen = pygame.display.set_mode((400, 600))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       
    screen.fill((0, 0, 0))

    # Vẽ hình chữ nhật
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, 100, 100))

    pygame.display.flip()

    # Vẽ chữ hello
    font = pygame.font.Font(None, 36)
    text = font.render("Hello", True, (255, 255, 255))
    screen.blit(text, (200, 200))
