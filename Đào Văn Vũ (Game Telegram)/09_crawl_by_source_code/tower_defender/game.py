import pygame
import sys
import time
from browser import window, document
import math
import random

# Initialize Pygame
pygame.init()

# Get the canvas
canvas = document.getElementById('gameCanvas')
context = canvas.getContext('2d')

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TOWER_COST = 20
TOWER_RANGE = 150
ENEMY_HEALTH = 100
GOBLIN_HEALTH = 80
ENEMY_SPEED = 3
GOBLIN_SPEED = 4

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Game state
gold = 60
towers = []
enemies = []
bullets = []
time1 = 0  # Time for Player
time2 = 0  # Time for Goblin
game_start_time = time.time()

# Waypoints
WAYPOINTS = [
    (379, 2), (383, 86), (359, 176),
    (310, 237), (227, 272), (189, 350),
    (191, 427), (250, 492), (369, 552),
    (489, 552), (573, 493)
]

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = TOWER_RANGE
        self.last_shot = 0
        self.cooldown = 1.0

    def draw(self, context):
        # Draw tower
        pygame.draw.circle(context, YELLOW, (self.x, self.y), 20)
        # Draw range
        pygame.draw.circle(context, YELLOW, (self.x, self.y), self.range, 1)

    def update(self, current_time):
        if current_time - self.last_shot < self.cooldown:
            return

        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance <= self.range:
                bullets.append(Bullet(self.x, self.y, enemy))
                self.last_shot = current_time
                break

class Enemy:
    def __init__(self, enemy_type='player'):
        self.waypoint_index = 0
        self.x, self.y = WAYPOINTS[0]
        self.type = enemy_type
        self.health = ENEMY_HEALTH if enemy_type == 'player' else GOBLIN_HEALTH
        self.speed = ENEMY_SPEED if enemy_type == 'player' else GOBLIN_SPEED
        self.max_health = self.health

    def update(self):
        if self.waypoint_index >= len(WAYPOINTS) - 1:
            return True

        target_x, target_y = WAYPOINTS[self.waypoint_index + 1]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 5:
            self.waypoint_index += 1
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

        return False

    def draw(self, context):
        # Draw enemy
        color = RED if self.type == 'player' else GREEN
        pygame.draw.circle(context, color, (int(self.x), int(self.y)), 15)
        
        # Draw health bar
        health_width = 30 * (self.health / self.max_health)
        pygame.draw.rect(context, RED, (self.x - 15, self.y - 25, 30, 5))
        pygame.draw.rect(context, GREEN, (self.x - 15, self.y - 25, health_width, 5))

        # Draw enemy type
        font = pygame.font.Font(None, 20)
        text = font.render(self.type.upper(), True, WHITE)
        text_rect = text.get_rect(center=(self.x, self.y - 30))
        context.blit(text, text_rect)

class Bullet:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.damage = 20

    def update(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 5:
            self.target.health -= self.damage
            if self.target.health <= 0:
                global gold
                gold += 10
                enemies.remove(self.target)
            return True

        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed
        return False

    def draw(self, context):
        pygame.draw.circle(context, YELLOW, (int(self.x), int(self.y)), 3)

def spawn_enemies():
    global time1, time2
    current_time = time.time()
    elapsed_time = current_time - game_start_time
    
    # Update times
    time1 = int(elapsed_time)
    time2 = int(elapsed_time)
    
    # Spawn Player in time1
    if time1 > 0 and random.random() < 0.02:  # 2% chance per frame
        enemies.append(Enemy('player'))
    
    # Spawn Goblin in time2
    if time2 > 0 and random.random() < 0.01:  # 1% chance per frame
        enemies.append(Enemy('goblin'))

def update():
    current_time = time.time()
    
    # Spawn enemies
    spawn_enemies()
    
    # Update towers
    for tower in towers:
        tower.update(current_time)
    
    # Update enemies
    for enemy in list(enemies):
        if enemy.update():
            enemies.remove(enemy)
    
    # Update bullets
    for bullet in list(bullets):
        if bullet.update():
            bullets.remove(bullet)

def draw():
    # Clear screen
    context.fillStyle = 'black'
    context.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Draw game objects
    for tower in towers:
        tower.draw(context)
    for enemy in enemies:
        enemy.draw(context)
    for bullet in bullets:
        bullet.draw(context)
    
    # Draw UI
    context.fillStyle = 'white'
    context.font = '20px Arial'
    context.fillText(f'Time1: {time1}s', 10, 30)
    context.fillText(f'Time2: {time2}s', 10, 60)
    context.fillText(f'Gold: {gold}', SCREEN_WIDTH - 100, 30)

def handle_click(event):
    if gold >= TOWER_COST:
        rect = canvas.getBoundingClientRect()
        x = event.clientX - rect.left
        y = event.clientY - rect.top
        towers.append(Tower(x, y))
        global gold
        gold -= TOWER_COST

def game_loop():
    update()
    draw()
    window.requestAnimationFrame(game_loop)

# Set up event listeners
canvas.addEventListener('click', handle_click)

# Start game loop
game_loop()