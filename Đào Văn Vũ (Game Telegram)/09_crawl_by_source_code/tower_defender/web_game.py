import pygame
import random 
import math
import asyncio
from pyodide.ffi import create_proxy
from js import document, requestAnimationFrame

# Initialize Pygame for web
pygame.init()

# Setup for web canvas
canvas = document.getElementById('gameCanvas')
context = canvas.getContext('2d')
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defender Web")

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
GRAY = (105, 105, 105)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game waypoints (kept from original)
WAYPOINTS1 = [(379, 2), (383, 86), (359, 176), (310, 237), (227, 272), (189, 350), (213, 405), (290, 428), (372, 427), (477, 433), (550, 435), (629, 416), (694, 371), (748, 359), (798, 361)]

WAYPOINT_LIST = {
    1: [WAYPOINTS1]
}

class Bullet:
    def __init__(self, x, y, target):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.target = target
        self.speed = 5
        self.x = float(x)
        self.y = float(y)

    def update(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += (dx/dist) * self.speed
            self.y += (dy/dist) * self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

class Player:
    def __init__(self, screen, level, waypoint_list):
        intdex_random = random.randint(0, len(waypoint_list[level]) - 1)
        self.waypoints = waypoint_list[level][intdex_random]
        self.screen = screen
        self.sprite_sheet = pygame.image.load("idleR.png")
        self.current_frame = 0
        self.num_frames = self.sprite_sheet.get_width() // 64
        self.index_waypoints = 0
        self.speed = 3
        self.x, self.y = self.waypoints[0]
        self.health = 100

    def get_sprite(self):
        x = self.current_frame * 64
        y = 0
        width = 64
        height = 64
        sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
        return sprite

    def update(self):
        if self.index_waypoints < len(self.waypoints) - 1:
            target_x, target_y = self.waypoints[self.index_waypoints]
            dx, dy = target_x - self.x, target_y - self.y
            distance = math.hypot(dx, dy)

            if distance > 0:
                self.x += dx / distance * self.speed
                self.y += dy / distance * self.speed

            if distance < 5:
                self.index_waypoints += 1

        self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self):
        sprite = self.get_sprite()
        self.screen.blit(sprite, (self.x - 32, self.y - 32))

class Tower:
    def __init__(self, x, y):
        self.image = pygame.image.load('towermage.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.range = 150
        self.cooldown = 1000
        self.last_shot = pygame.time.get_ticks()

    def shoot(self, enemies, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            for enemy in enemies:
                dx = enemy.x - self.rect.centerx
                dy = enemy.y - self.rect.centery
                distance = math.hypot(dx, dy)
                if distance <= self.range:
                    bullets.append(Bullet(self.rect.centerx, self.rect.centery, enemy))
                    self.last_shot = now
                    break

class Game:
    def __init__(self):
        self.player_gold = 60
        self.tower_cost = 20
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.level = 1
        self.game_over = False
        
    def update(self):
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                self.player_gold += 10
                
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.target not in self.enemies:
                self.bullets.remove(bullet)
                
        for tower in self.towers:
            tower.shoot(self.enemies, self.bullets)
            
    def draw(self):
        screen.fill(WHITE)
        for tower in self.towers:
            screen.blit(tower.image, tower.rect)
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            pygame.draw.circle(screen, YELLOW, (int(bullet.rect.x), int(bullet.rect.y)), 5)
            
        # Draw UI
        font = pygame.font.Font(None, 36)
        gold_text = font.render(f'Gold: {self.player_gold}', True, BLACK)
        screen.blit(gold_text, (10, 10))
        
        # Convert Pygame surface to canvas
        data = pygame.image.tostring(screen, 'RGBA')
        img_data = context.createImageData(SCREEN_WIDTH, SCREEN_HEIGHT)
        img_data.data.set(data)
        context.putImageData(img_data, 0, 0)

# Main game loop
game = Game()
clock = pygame.time.Clock()

def handle_click(event):
    x = event.offsetX
    y = event.offsetY
    if game.player_gold >= game.tower_cost:
        game.towers.append(Tower(x, y))
        game.player_gold -= game.tower_cost

canvas.addEventListener('click', create_proxy(handle_click))

def game_loop(*args):
    if len(game.enemies) < 5:
        game.enemies.append(Player(screen, game.level, WAYPOINT_LIST))
        
    game.update()
    game.draw()
    clock.tick(60)
    
    requestAnimationFrame(create_proxy(game_loop))

# Start the game loop
game_loop()
