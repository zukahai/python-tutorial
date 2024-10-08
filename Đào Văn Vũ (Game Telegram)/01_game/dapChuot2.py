import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình game
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Đập Chuột")

# Màu sắc
WHITE = (255, 255, 255)

# Tải ảnh con chuột
mouse_img = pygame.image.load('mouse.png')  # Đảm bảo 'mouse.png' nằm cùng thư mục với tệp code
mouse_size = mouse_img.get_rect().size  # Lấy kích thước của ảnh con chuột
# Giảm kích thước ảnh con chuột thành 100x100
mouse_img = pygame.transform.scale(mouse_img, (100, 100))
mouse_width, mouse_height = mouse_size

# Tạo vị trí ngẫu nhiên cho con chuột
mouse_pos = [random.randint(0, screen_width - mouse_width), random.randint(0, screen_height - mouse_height)]

# Thiết lập font để hiển thị điểm số
font = pygame.font.SysFont(None, 55)

# Biến để lưu điểm số
score = 0

# Tốc độ khung hình (FPS)
clock = pygame.time.Clock()

# Vòng lặp game
running = True
while running:
    # Xử lý các sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Lấy vị trí click chuột
            mouse_click_pos = event.pos
            # Kiểm tra nếu click trúng con chuột
            if mouse_pos[0] <= mouse_click_pos[0] <= mouse_pos[0] + mouse_width and \
               mouse_pos[1] <= mouse_click_pos[1] <= mouse_pos[1] + mouse_height:
                # Cộng điểm
                score += 1
                # Đổi vị trí con chuột ngẫu nhiên
                mouse_pos = [random.randint(0, screen_width - mouse_width), random.randint(0, screen_height - mouse_height)]

    # Vẽ màn hình trắng
    screen.fill(WHITE)

    # Vẽ con chuột (hình ảnh)
    screen.blit(mouse_img, mouse_pos)

    # Hiển thị điểm số
    score_text = font.render("Score: {0}".format(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Cập nhật màn hình
    pygame.display.flip()

    # Giới hạn tốc độ khung hình
    clock.tick(30)

# Thoát khỏi Pygame
pygame.quit()
