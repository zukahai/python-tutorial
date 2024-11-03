import pygame
from settings import *

class Player:
    def __init__(self, screen):
        # đặt là private để tránh việc thay đổi giá  của gold
        self.__gold = 60 # Số vàng ban đầu
        self.screen = screen
        self.__hp = 100

    def draw(self, currentime,):
        font = pygame.font.Font("./assets/fonts/NVNPixelFJVerdana8pt.ttf", 30)
        pygame.draw.rect(self.screen, WHITE, (730, 0, 90, 50))
        text = font.render(str(currentime // 60), True, BLACK)
        textgold = font.render(str(self.get_gold()), True, YELLOW)
        self.screen.blit(textgold, (0, 30))
        self.screen.blit(text, (730 + (70 - text.get_width()) // 2, -5))

        # Vẽ thanh máu
        font = pygame.font.Font("./assets/fonts/NVNPixelFJVerdana8pt.ttf", 20)
        pygame.draw.rect(self.screen, RED, (0, 0, self.__hp * 2, 30))
        pygame.draw.rect(self.screen, BLACK, (0, 0, 200, 30), 3)
        text = font.render(str(self.__hp) + '/100', True, WHITE)
        # Vẽ số máu ở giữa thanh máu 
        self.screen.blit(text, (100 - text.get_width() // 2, -5))

    def add_gold(self, amount):
        self.__gold += amount
    
    def remove_gold(self, amount):
        self.__gold -= amount

    def get_gold(self):
        return self.__gold
    
    def set_gold(self, gold):
        self.__gold = gold
    
    def get_hp(self):
        return self.__hp
    
    def set_hp(self, hp):
        self.__hp = hp
    
    def remove_hp(self, amount):
        self.__hp -= amount
        if self.__hp <= 0:
            self.__hp = 0

    def is_dead(self):
        return self.__hp <= 0
    

    
