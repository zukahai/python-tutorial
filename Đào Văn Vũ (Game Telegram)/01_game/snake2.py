import pygame
import random
import math

# Khởi tạo Pygame
pygame.init()

# Cài đặt thông số màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple RPG Game")

# Định nghĩa màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Thiết lập đồng hồ để điều chỉnh tốc độ game
clock = pygame.time.Clock()

# Tạo lớp cho nhân vật chính (Player)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.level = 1
        self.hp = 100
        self.xp = 0
        self.xp_needed = 100  # Số XP cần để lên cấp

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def gain_xp(self, xp):
        self.xp += xp
        if self.xp >= self.xp_needed:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.speed += 1  # Tăng tốc độ khi lên cấp
        self.hp += 50  # Tăng HP khi lên cấp
        self.xp = 0  # Reset XP sau khi lên cấp
        self.xp_needed += 50  # Tăng số XP cần để lên cấp sau
        print(f"Leveled up to {self.level}! Speed and HP increased!")

    # Phương thức tấn công
    def attack(self, enemy):
        damage = random.randint(10, 20)  # Sát thương ngẫu nhiên
        enemy.hp -= damage
        print(f"Attacked enemy! Dealt {damage} damage!")
        if enemy.hp <= 0:
            print("Enemy defeated!")
            self.gain_xp(50)  # Nhận XP khi tiêu diệt quái vật
            enemy.kill()  # Xóa quái vật

# Lớp Bullet cho tấn công từ xa bằng chuột
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

        # Tính toán hướng từ vị trí người chơi đến vị trí chuột
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Xóa đạn khi ra khỏi màn hình
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

# Tạo lớp cho quái vật (Enemy)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = random.randint(1, 3)
        self.hp = 50  # Thêm HP cho quái vật

    def update(self):
        # Di chuyển quái vật về phía người chơi
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed

# Kiểm tra va chạm và tấn công bằng đạn
def check_bullet_hit(bullets, enemies):
    for bullet in bullets:
        hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
        if hit_enemy:
            player.attack(hit_enemy)  # Gây sát thương cho quái vật
            bullet.kill()  # Xóa đạn sau khi va chạm
def respawn_enemies(enemies, number):
    for _ in range(number):
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)
# Tạo nhóm các đối tượng nhân vật, quái vật, và đạn
player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()  # Nhóm đạn

#Tạo quái vật ban đầu
for i in range(5):
    enemy = Enemy()
    enemies.add(enemy)

# Tạo nhóm chính cho người chơi
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)

# Vòng lặp game chính
running = True
while running:
    # Đặt tốc độ game (frame per second)
    clock.tick(60)

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Lấy vị trí của chuột khi nhấp
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Tạo đạn bắn về hướng vị trí chuột
            bullet = Bullet(player.rect.centerx, player.rect.centery, mouse_x, mouse_y)
            bullets.add(bullet)
            all_sprites.add(bullet)

    # Cập nhật vị trí nhân vật, quái vật và đạn
    all_sprites.update()

    # Kiểm tra va chạm giữa đạn và quái vật
    check_bullet_hit(bullets, enemies)
    if len(enemies) == 0:
        print("All enemies defeated! Respawning enemies...")
        respawn_enemies(enemies, 5)
        

    # Kiểm tra va chạm giữa người chơi và quái vật
    if pygame.sprite.spritecollideany(player, enemies):
        player.hp -= 1  # Giảm HP khi chạm vào quái vật
        if player.hp <= 0:
            print("Game Over")
            running = False

    # Làm mới màn hình
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Hiển thị điểm HP, XP và Cấp độ
    font = pygame.font.Font(None, 36)
    hp_text = font.render(f"HP: {player.hp}", True, WHITE)
    xp_text = font.render(f"XP: {player.xp}/{player.xp_needed}", True, WHITE)
    level_text = font.render(f"Level: {player.level}", True, WHITE)
    screen.blit(hp_text, (10, 10))
    screen.blit(xp_text, (10, 50))
    screen.blit(level_text, (10, 90))

    # Cập nhật màn hình
    pygame.display.flip()

pygame.quit()
