import pygame
import math

from settings import *


# Lớp đạn
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.target = target
        self.speed = 10

    def update(self, enemies, player):
        dx = self.target.x - self.rect.x
        dy = self.target.y - self.rect.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.rect.x += dx / distance * self.speed
            self.rect.y += dy / distance * self.speed

        # Kiểm tra va chạm với kẻ thù
        if pygame.Rect.colliderect(self.rect, pygame.Rect(self.target.x, self.target.y, 64, 64)):
            if self.target.take_damage(10):
                if self.target in enemies:
                    player.add_gold(10)
                    enemies.remove(self.target)  # Xóa kẻ thù nếu bị giết
            self.kill()  # Xóa đạn sau khi va chạm