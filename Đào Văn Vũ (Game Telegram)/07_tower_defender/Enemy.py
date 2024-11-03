import pygame
import math

from settings import *

class Enemy:
    def __init__(self):
        self.is_show_hp = 1000

    def get_sprite(self):
        x = self.current_frame * 64
        y = 0
        width = self.width
        height = self.height
        sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
        return sprite

    def update(self):
        # Di chuyển dọc theo waypoints
        if self.index_waypoints < len(self.waypoints) - 1:
            target_x, target_y = self.waypoints[self.index_waypoints]
            dx, dy = target_x - self.x, target_y - self.y
            distance = math.hypot(dx, dy)

            if distance > 0:
                self.x += dx / distance * self.speed
                self.y += dy / distance * self.speed

            # Khi đến gần waypoint hiện tại, chuyển sang waypoint tiếp theo
            if distance < 5:  
                self.index_waypoints += 1

        self.is_show_hp += 1


        self.current_frame += 1
        if self.current_frame >= self.num_frames:
            self.current_frame = 0

    def draw(self):
        if self.is_show_hp < 120:
            length_bar = 60
            pygame.draw.rect(self.screen, (GREEN), ((self.x -length_bar//2), self.y - self.height - 10, (self.health / self.max_health) * length_bar, 14))
            pygame.draw.rect(self.screen, (RED), ((self.x -length_bar//2), self.y - self.height - 10, length_bar, 14), 2)
        
        sprite = self.get_sprite()
        # Quay lại nếu đi qua trái
        if self.x > self.waypoints[self.index_waypoints][0]:
            sprite = pygame.transform.flip(sprite, True, False)
        self.screen.blit(sprite, (self.x - self.width // 2, self.y - self.height))

    def take_damage(self, damage):
        self.is_show_hp = 0
        self.health -= damage
        if self.health <= 0:
            # Xóa kẻ thù nếu hết máu
            return True
        return False
    
    # Kiểm tra đi tới waypoint cuối cùng
    def is_at_end(self):
        return self.index_waypoints == len(self.waypoints) - 1
    
