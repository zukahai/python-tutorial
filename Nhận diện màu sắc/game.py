import pygame
import sys
from detech import *

image_path = "./assets/images/image.png"


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
    image = cv2.imread(image_path)
    data = get_color_image(image)
    print(data)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
    screen.fill(WHITE)

    # Vẽ dữ liệu
    for row in range(N):
        for column in range(N):
            if data[row][column] != 0:
                screen.blit(images[data[row][column]], (column * size, row * size))

     # Vẽ mạng lưới 10x10
    for i in range(N):
        pygame.draw.line(screen, BLACK, (0, i * size), (game_length, i * size), 1)
        pygame.draw.line(screen, BLACK, (i * size, 0), (i * size, game_length), 1)
    
    # Cập nhật màn hình
    pygame.display.flip()
# Thoát pygame
pygame.quit()
sys.exit()
