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
YELLOW = (255, 255, 0)
PINK = (255,192,203)
BROWN = (139,69,19)

# Thiết lập đồng hồ để điều chỉnh tốc độ game
clock = pygame.time.Clock()
# Tạo lớp cho item
background_image = pygame.image.load('backgrounddark.png')
hero_image = pygame.image.load('heros.png')

class Item(pygame.sprite.Sprite):
    def __init__(self,item_type):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        if item_type == "health":
            self.image.fill(GREEN)
        elif item_type == "speed":
            self.image.fill(WHITE)
        elif item_type == "sword":
            self.image.fill(YELLOW)
        elif item_type == "gun":
            self.image.fill(BLACK)
        elif item_type == "rocket":
            self.image = pygame.image.load('rocket.png')
        elif item_type == "update weapon":
            self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.type = item_type
    def collect_item(self, item):
        if item.type == "health":
            player.hp += 30
        elif item.type == "speed":
            player.speed += 1
        elif item.type == "sword":
            player.has_sword = True
            player.attack_power += 10
        elif item.type == "gun":
            player.has_gun = True
        elif item.type == "rocket":
            player.has_rocket = True
        elif item.type == "update weapon":
            player.attack_power += 10
        item.kill()
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.image.load('rocket.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7
        self.explosion_radius = 50
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()
    def explode(self):
        for enemy in enemies:
            distance = math.hypot(enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)
            if distance < self.explosion_radius:
                enemy.hp -= 50
                if enemy.hp <= 0:
                    enemy.kill()
                    player.gain_xp(50)
                    self.kill()
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        hit_enemies = pygame.sprite.spritecollide(self, enemies, True)
        hit_remote_enemies = pygame.sprite.spritecollide(self, remote_enemies, True)
        if hit_enemies:
            self.explode()
            self.kill()
        if hit_remote_enemies:
            self.explode()
            self.kill()
# Tạo lớp cho nhân vật chính (Player)d
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('heros.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.level = 1
        self.attack_power = 10
        self.has_gun = False
        self.has_rocket = False
        self.has_sword = False
        self.hp = 100
        self.xp = 0
        self.xp_needed = 100  # Số XP cần để lên cấp
    def sword_attack(self, enemy):
        if self.has_sword:
            for enemy in enemies:
                distance = math.hypot(enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)
                if distance < 50:
                    damage = self.attack_power + 10
                    enemy.hp -= damage
                    if enemy.hp <= 0:
                        self.gain_xp(50)
                        enemy.kill()
    def shoot(self, target_x, target_y):
        bullet = Bullet(self.rect.x, self.rect.y, target_x, target_y)
        all_sprites.add(bullet)
        bullets.add(bullet) 
        print("Shoot!")
    def shoot_rocket(self, target_x, target_y):
        rocket = Rocket(self.rect.x, self.rect.y, target_x, target_y)
        rockets.add(rocket)
        all_sprites.add(rocket)
        print("Shoot Rocket!")
     

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
# Tạo lớp cho quái vật tấn công từ xa
class RemoteEnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
        self.shoot_cooldown = 2000
        self.last_shot = pygame.time.get_ticks()
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()
class RemoteEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('range.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = random.randint(1, 3)
        self.hp = 50

    def update(self):
        if random.randint(1,20) == 1:
            if self.rect.x < player.rect.x:
                self.rect.x += self.speed
            if self.rect.x > player.rect.x:
                self.rect.x -= self.speed
            if self.rect.y < player.rect.y:
                self.rect.y += self.speed
            if self.rect.y > player.rect.y:
                self.rect.y -= self.speed
            remote_bullet = RemoteEnemyBullet(self.rect.x, self.rect.y, player.rect.x, player.rect.y)
            remote_bullets.add(remote_bullet)
            all_sprites.add(remote_bullet)
def check_remote_bullet_hit(remote_bullets, player):
    hit_player = pygame.sprite.spritecollideany(player, remote_bullets)
    if hit_player:
        player.hp -= 2
        hit_player.kill()
def respawn_remote_enemies(remote_enemies, number):
    for _ in range(number):
        enemy = RemoteEnemy()
        remote_enemies.add(enemy)
        all_sprites.add(enemy)
# Tạo lớp cho quái vật (Enemy)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = random.randint(1, 3)
        self.hp = 50  # Thêm HP cho quái vật
        self.damage = 1

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
    def check_distance(self, player):
        distance = math.hypot(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        if distance < 5:
            return True
        else:
            return False
    

# Kiểm tra va chạm và tấn công bằng đạn
def check_bullet_hit(bullets, enemies, rockets, sword, gun):
    for bullet in bullets:
        hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
        hit_remote_enemy = pygame.sprite.spritecollideany(bullet, remote_enemies)
        
        if hit_enemy:
            player.attack(hit_enemy)  # Gây sát thương cho quái vật
            bullet.kill()  # Xóa đạn sau khi va chạm
        if hit_remote_enemy:
            player.attack(hit_remote_enemy)  # Gây sát thuong cho quái vật
            bullet.kill()
    for rocket in rockets:
        hit_enemy = pygame.sprite.spritecollideany(rocket, enemies)
        hit_remote_enemy = pygame.sprite.spritecollideany(rocket, remote_enemies)
        if hit_enemy:
            player.attack(hit_enemy)  # Gây sát thương cho quái vật
            rocket.kill()
        if hit_remote_enemy:
            player.attack(hit_remote_enemy)  # Gây sát thuong cho quái vật
            rocket.kill()
    if sword:
        hit_enemy = pygame.sprite.spritecollideany(player, enemies)
        hit_remote_enemy = pygame.sprite.spritecollideany(player, remote_enemies)
        if hit_enemy:
            player.sword_attack(hit_enemy)  # Gây sát thương cho quái vật
        if hit_remote_enemy:
            player.sword_attack(hit_remote_enemy)  # Gây sát thương cho quái vật
    if gun:
        hit_enemy = pygame.sprite.spritecollideany(player, enemies)
        hit_remote_enemy = pygame.sprite.spritecollideany(player, remote_enemies)
        if hit_enemy:
            player.attack(hit_enemy)  # Gây sát thương cho quái vật
            bullet.kill()
        if hit_remote_enemy:
            player.attack(hit_remote_enemy)  # Gây sát thương cho quái vật
            bullet.kill()

# Tạo nhóm chính cho người chơi
def respawn_enemies(enemies, number):
    for _ in range(number):
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)
# Tạo nhóm các đối tượng nhân vật, quái vật, và đạn
player = Player()
enemies = pygame.sprite.Group()
remote_enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()  # Nhóm đạn
remote_bullets = pygame.sprite.Group()

#Tạo quái vật ban đầu
for i in range(5):
    enemy = Enemy()
    enemies.add(enemy)

# Tạo nhóm chính cho người chơi
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)
all_sprites.add(remote_enemies)

# Vòng lặp game chính
running = True
items = pygame.sprite.Group()
for i in range(5):
    item_type = random.choice(["health", "speed", "sword", "gun", "rocket", "update weapon"])
    item = Item(item_type)
    items.add(item)
    all_sprites.add(item)

while running:
    # Đặt tốc độ game (frame per second)
    clock.tick(60)
    rockets = pygame.sprite.Group()
    swords = pygame.sprite.Group()
    guns = pygame.sprite.Group()
     
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Lấy vị trí của chuột khi nhấp
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Tạo đạn bắn về hướng vị trí chuột
            if player.has_gun:
                player.shoot(mouse_x, mouse_y)
            if player.has_rocket:
                player.shoot_rocket(mouse_x, mouse_y)
            if player.has_sword:
                player.sword_attack(enemies)
            
    
    # Cập nhật vị trí nhân vật, quái vật và đạn
    all_sprites.update()
    item_hit = pygame.sprite.spritecollideany(player, items)
    if item_hit:
        item_hit.collect_item(item_hit)

   
    
    # Kiểm tra va chạm giữa đạn và quái vật
    check_bullet_hit(bullets, enemies, rockets, swords, guns)
    if len(enemies) == 0:
        print("All enemies defeated! Respawning enemies...")
        respawn_enemies(enemies,5 + player.level) 
    check_remote_bullet_hit(remote_bullets, player)
    if len(remote_enemies) == 0:
        print("All enemies defeated! Respawning enemies...")
        respawn_remote_enemies(remote_enemies,3 + player.level) 
        

    # Kiểm tra va chạm giữa người chơi và quái vật
    if pygame.sprite.spritecollideany(player, enemies):
        player.hp -= 1  # Giảm HP khi chạm vào quái vật
        if player.hp <= 0:
            print("Game Over")
            running = False

    # Làm mới màn hình
    screen.fill(BLACK)
    rockets.draw(screen)
    screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))  
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
