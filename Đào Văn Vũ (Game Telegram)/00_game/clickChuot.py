import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            print("Đang bấm xuống {0}, {1}".format(x, y))
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            print("Đã nhả chuột {0}, {1}".format(x, y))
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            print("Đang di chuyển chuột {0}, {1}".format(x, y))

    screen.fill((255, 255, 255))
    pygame.display.flip()

pygame.quit()
