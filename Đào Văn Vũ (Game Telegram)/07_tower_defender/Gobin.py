import pygame
import math
import random

from Enemy import Enemy

class Gobin(Enemy):
    def __init__(self, screen, level, waypoint_list):
        super().__init__()
        self.screen = screen
        self.width = 112
        self.height = 112
       
        intdex_random = random.randint(0, len(waypoint_list[level]) - 1)
        self.waypoints = waypoint_list[level][intdex_random]
        self.screen = screen
        self.sprite_sheet = pygame.image.load("./assets/images/nubeIR.png").convert_alpha()
        self.current_frame = 0
        self.num_frames = self.sprite_sheet.get_width() // self.width
        self.index_waypoints = 0
        self.speed = 1  # Tốc độ di chuyển
        self.x, self.y = self.waypoints[0]  # Bắt đầu tại điểm mốc đầu tiên
        self.health = self.max_health = 30

    def get_sprite(self):
        x = self.current_frame * self.width
        y = 0 * self.height
        width = self.width
        height = self.height

        sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
        return sprite