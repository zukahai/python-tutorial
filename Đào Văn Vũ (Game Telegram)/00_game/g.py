import pygame
import hashlib
import json
import random
import time

# Khởi tạo Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Breaker")

# Màu sắc và thiết lập
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
FPS = 60
FONT = pygame.font.SysFont("comicsans", 30)
block_size = 50
energy_cost = 1  # Năng lượng tiêu tốn cho mỗi lần phá khối

# Lớp Blockchain và Block
class Block:
    def __init__(self, data, prev_hash="", nonce=0):
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = json.dumps(self.data) + self.prev_hash + str(self.nonce)
        data = data.encode("utf-8")
        return hashlib.sha256(data).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block")

    def add_block(self, data):
        new_block = Block(data, self.chain[-1].hash)
        while not new_block.hash.startswith("0"):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print(f"Hash: {block.hash}")
            print(f"Data: {block.data}")
            print(f"Nonce: {block.nonce}")
            print(f"Prev Hash: {block.prev_hash}")
            print("------------------------")
            time.sleep(1)

# Khởi tạo blockchain
blockchain = Blockchain()

# Lớp Player
class Player:
    def __init__(self, name, x, y):
        self.rect = pygame.Rect(x, y, block_size, block_size)
        self.name = name
        self.speed = 5
        self.coin_balance = 0
        self.energy = 10  # Khởi tạo năng lượng cho người chơi
        self.max_energy = 10
        self.energy_regen_time = 3  # Thời gian hồi năng lượng (3 giây)
        self.last_energy_regen = time.time()
        self.transaction_history = []

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(SCREEN, GREEN, self.rect)

    def regenerate_energy(self):
        # Hồi phục năng lượng theo thời gian
        if self.energy < self.max_energy and time.time() - self.last_energy_regen > self.energy_regen_time:
            self.energy += 1
            self.last_energy_regen = time.time()

    def hit_block(self, blocks, special_blocks, obstacles):
        if self.energy >= energy_cost:  # Kiểm tra nếu đủ năng lượng để phá khối
            for block in blocks:
                if self.rect.colliderect(block):
                    self.energy -= energy_cost  # Tiêu hao năng lượng khi phá khối
                    self.add_coin(1)  # Thưởng 1 coin khi phá khối
                    blocks.remove(block)
                    break
            for s_block in special_blocks:
                if self.rect.colliderect(s_block):
                    self.energy -= energy_cost
                    self.coin_balance += 5  # Khối đặc biệt thưởng nhiều coin
                    special_blocks.remove(s_block)
                    break
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle):
                    self.energy -= 2  # Chướng ngại vật tiêu hao nhiều năng lượng hơn
                    print(f"{self.name} đã va phải chướng ngại vật!")
                    obstacles.remove(obstacle)
                    break
        else:
            print("Không đủ năng lượng để phá khối!")

    def add_coin(self, amount):
        self.coin_balance += amount
        transaction = {"from": "system", "to": self.name, "amount": amount}
        blockchain.add_block(transaction)
        self.transaction_history.append(transaction)

    def spend_coin(self, amount):
        if self.coin_balance >= amount:
            self.coin_balance -= amount
            return True
        else:
            print("Không đủ coin!")
            return False

class Quest:
    def __init__(self):
        self.daily_quests = {"break_20_blocks": 20, "earn_5_coins": 5}
        self.progress = {"break_20_blocks": 0, "earn_10_coins": 0}

    def update_progress(self, quest_name):
        if quest_name in self.progress:
            self.progress[quest_name] += 1

    def check_quests(self):
        for quest, goal in self.daily_quests.items():
            if self.progress[quest] >= goal:
                print(f"Nhiệm vụ '{quest}' hoàn thành!")
                self.progress[quest] = 0
class Achievement:
    def __init__(self):
        self.achievements = []

    def check_achievement(self, player):
        if player.coin_balance >= 50 and "Coin Collector" not in self.achievements:
            print("Chúc mừng! Bạn đã đạt thành tích Coin Collector!")
            self.achievements.append("Coin Collector")

# Lớp cửa hàng
class Shop:
    def __init__(self):
        self.items = {
            "double_coin": {"price": 10, "effect": "double_coin"},
            "extra_time": {"price": 15, "effect": "extra_time"},
            "energy_boost": {"price": 10, "effect": "energy_boost"}
        }

    def purchase(self, player, item_name):
        item = self.items.get(item_name)
        if item and player.spend_coin(item["price"]):
            if item_name == "energy_boost":
                player.energy = min(player.energy + 5, player.max_energy)  # Thêm 5 năng lượng
            return item["effect"]
        else:
            print("Không mua được vật phẩm.")
            return None

# Khởi tạo người chơi và cửa hàng
player = Player("Player1", WIDTH // 2, HEIGHT // 2)
quest = Quest()
achievement = Achievement()
shop = Shop()

# Lớp bảng xếp hạng
class Leaderboard:
    def __init__(self):
        self.scores = []

    def update(self, player):
        self.scores.append((player.name, player.coin_balance))
        self.scores = sorted(self.scores, key=lambda x: x[1], reverse=True)

    def display(self):
        print("Bảng xếp hạng:")
        for idx, (name, score) in enumerate(self.scores):
            print(f"{idx + 1}. {name} - {score} coins")

leaderboard = Leaderboard()
class Event:
    def __init__(self):
        self.active_event = None

    def activate_event(self, event_type):
        if event_type == "double_coin":
            print("Sự kiện Coin Frenzy: Nhận gấp đôi coin!")
            self.active_event = "double_coin"

    def apply_event(self, player):
        if self.active_event == "double_coin":
            player.coin_balance *= 2 
player1 = Player("Player1", WIDTH // 2, HEIGHT // 2)
player2 = Player("Player2", WIDTH // 2, HEIGHT // 2)
event_system = Event()
# Tạo các khối trong game
def create_blocks(num_block, num_special, num_obstacles):
    blocks = [pygame.Rect(random.randint(0, WIDTH - block_size), random.randint(0, HEIGHT - block_size), block_size, block_size) for _ in range(num_block)]
    special_blocks = [pygame.Rect(random.randint(0, WIDTH - block_size), random.randint(0, HEIGHT - block_size), block_size, block_size) for _ in range(num_special)]
    obstacles = [pygame.Rect(random.randint(0, WIDTH - block_size), random.randint(0, HEIGHT - block_size), block_size, block_size) for _ in range(num_obstacles)]
    return blocks, special_blocks, obstacles

# Khởi tạo khối
blocks,special_blocks,obstacles = create_blocks(10, 3, 2)

# Vòng lặp chính của trò chơi
clock = pygame.time.Clock()
running = True
while running:
    SCREEN.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Điều khiển người chơi và tương tác với khối
    keys = pygame.key.get_pressed()
    player1.move()
    player2.move()

    player1.regenerate_energy()
    player2.regenerate_energy()

    player1.hit_block(blocks, special_blocks, obstacles)
    player2.hit_block(blocks, special_blocks, obstacles)

    # Vẽ người chơi và khối lên màn hình
    player1.draw()
    player2.draw()
    for block in blocks:
        pygame.draw.rect(SCREEN, RED, block)
    for s_block in special_blocks:
        pygame.draw.rect(SCREEN, YELLOW, s_block)
    for obstacle in obstacles:
        pygame.draw.rect(SCREEN, ORANGE, obstacle)

    # Hiển thị thông tin điểm số và năng lượng của mỗi người chơi
    score_text1 = FONT.render(f"{player1.name} Coin: {player1.coin_balance} Energy: {player1.energy}", True, BLACK)
    score_text2 = FONT.render(f"{player2.name} Coin: {player2.coin_balance} Energy: {player2.energy}", True, BLACK)
    SCREEN.blit(score_text1, (10, 10))
    SCREEN.blit(score_text2, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

# Hiển thị bảng xếp hạng sau khi kết thúc PvP
print("Bảng xếp hạng PvP:")
if player1.coin_balance > player2.coin_balance:
    print(f"{player1.name} thắng với {player1.coin_balance} coins!")
elif player2.coin_balance > player1.coin_balance:
    print(f"{player2.name} thắng với {player2.coin_balance} coins!")
else:
    print("Hòa!")

# Cập nhật và hiển thị bảng xếp hạng
leaderboard.update(player)
leaderboard.display()

# In ra chuỗi blockchain sau khi kết thúc trò chơi
print("Blockchain:") 
blockchain.print_chain()
print("Bảng xếp hạng:")
leaderboard.display()

pygame.quit()
