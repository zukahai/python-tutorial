import pygame
import math

from Bullet import Bullet


# Lớp tháp (Tower)
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./assets/images/towermage.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.range = 150  # Phạm vi tấn công
        self.cooldown = 1000  # Thời gian chờ giữa các lần bắn (ms)
        self.last_shot = pygame.time.get_ticks()  # Lần bắn cuối

    def shoot(self, enemies, bullets):
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.cooldown:
            for enemy in enemies:
                dx = enemy.x - self.rect.x
                dy = enemy.y - self.rect.y
                distance = math.hypot(dx, dy)
                if distance < self.range:
                    # Bắn đạn về phía kẻ thù trong phạm vi
                    bullet = Bullet(self.rect.centerx, self.rect.centery, enemy)
                    bullets.add(bullet)
                    self.last_shot = current_time
                    break