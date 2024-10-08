import pygame
import random

pygame.init()

screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Đập Chuột")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

mouse_size = 50
mouse_pos = [random.randint(0, screen_width - mouse_size), random.randint(0, screen_height - mouse_size)]

font = pygame.font.SysFont(None, 55)

score = 0

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # Là khi anh bấm chuột xuống
            # Lấy vị trí click chuột
            mouse_click_pos = event.pos
            # mouse__pos[0] là tọa độ x của chuột
            # mouse__pos[1] là tọa độ y của chuột
            # mouse_size là kích thước của chuột
            # mouse_click_pos[0] là tọa độ x của click chuột của mình
            # mouse_click_pos[1] là tọa độ y của click chuột của mình

            # Đoạn này kiểm tra xem vị trí click chuột có nằm trong hình chữ nhật của con chuột không
            if mouse_pos[0] <= mouse_click_pos[0] <= mouse_pos[0] + mouse_size and \
               mouse_pos[1] <= mouse_click_pos[1] <= mouse_pos[1] + mouse_size:
                # Cộng điểm
                score += 1
                # Đổi vị trí con chuột ngẫu nhiên
                mouse_pos = [random.randint(0, screen_width - mouse_size), random.randint(0, screen_height - mouse_size)]

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, (*mouse_pos, mouse_size, mouse_size))

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
