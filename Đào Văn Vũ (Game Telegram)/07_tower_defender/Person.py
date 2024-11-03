import pygame
import math
import random

from Enemy import Enemy

# Lớp kẻ thù (Player chỉ là một ví dụ, bạn có thể đổi tên thành `Enemy`)
class Person(Enemy):
    def __init__(self, screen, level, waypoint_list):
        super().__init__()
        intdex_random = random.randint(0, len(waypoint_list[level]) - 1)
        self.waypoints = waypoint_list[level][intdex_random]
        self.screen = screen
        self.sprite_sheet = pygame.image.load("./assets/images/idleR.png").convert_alpha()
        self.current_frame = 0
        self.num_frames = self.sprite_sheet.get_width() // 64
        self.index_waypoints = 0
        self.speed = 0.5  # Tốc độ di chuyển
        self.x, self.y = self.waypoints[0]  # Bắt đầu tại điểm mốc đầu tiên
        self.health = self.max_health = 50
        self.width = 64
        self.height = 64

    def get_sprite(self):
        x = self.current_frame * 64
        y = 0
        width = self.width
        height = 64
        sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
        return sprite