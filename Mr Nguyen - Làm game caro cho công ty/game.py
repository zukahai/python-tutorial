import pygame
import sys

# Khởi tạo pygame
pygame.init()

# Lấy chiều cao màn hình
screen_info = pygame.display.Info()
screen_height = screen_info.current_h


N = 10

data = [[0 for i in range(N)] for j in range(N)]

# Chiều dài của game
game_length = screen_height - 100

# Kích thước mỗi ô trong mạng lưới 10x10
size = game_length / 10

# Thiết lập kích thước màn hình
screen = pygame.display.set_mode((game_length, game_length))
pygame.display.set_caption("Game")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# sáng hơn màu đen 1 chút
GRAY = (80, 80, 80)

images = [0]
images.append(pygame.image.load("./assets/1.png"))
images.append(pygame.image.load("./assets/2.png"))
images.append(pygame.image.load("./assets/3.png"))

for i in range(1, 4):
    images[i] = pygame.transform.scale(images[i], (size, size))

def next_taget(taget):
    res = taget.copy()
    if res["row"] == N:
        return res
    res["column"] += 1
    if res["column"] == N:
        res["column"] = 0
        res["row"] += 1
    return res
    

def reset_game():
    global data
    global taget
    global next
    data = [[0 for i in range(N)] for j in range(N)]
    taget = {"row": 0, "column": 0}
    next = next_taget(taget)

taget = {"row": 0, "column": 0}
next = next_taget(taget)



# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Bấm phím 1, 2, 3
        if event.type == pygame.KEYDOWN:
            if taget["row"] != N and (event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3):
                data[taget["row"]][taget["column"]] = event.key - 48
                taget = next
                next = next_taget(taget)
            # Bấm phím r
            if event.key == pygame.K_r:
                reset_game()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = (int)(y // size)
            column = (int)(x // size)
            if data[row][column] != 0:
                if taget["row"] != N and data[taget["row"]][taget["column"]] == 0:
                    next = taget.copy()
                taget = {"row": row, "column": column}
    # Đặt nền màn hình
    screen.fill(BLACK)

    # Vẽ mạng lưới 10x10
    for i in range(N):
        pygame.draw.line(screen, WHITE, (0, i * size), (game_length, i * size), 1)
        pygame.draw.line(screen, WHITE, (i * size, 0), (i * size, game_length), 1)

    # Vẽ ô target màu xám
    pygame.draw.rect(screen, GRAY, (taget["column"] * size + 1, taget["row"] * size + 1, size - 2, size - 2))

    # Vẽ dữ liệu
    for row in range(N):
        for column in range(N):
            if data[row][column] != 0:
                screen.blit(images[data[row][column]], (column * size, row * size))

    
    
    # Cập nhật màn hình
    pygame.display.flip()
# Thoát pygame
pygame.quit()
sys.exit()
