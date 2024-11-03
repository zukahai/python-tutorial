import pygame
import random 
import time
import math

from settings import *
from Person import Person
from Gobin import Gobin
from Shaman import Shaman
from Tower import Tower
from Player import Player


# Khởi tạo Pygame
pygame.init()
font = pygame.font.SysFont('sans', 50)

# Cài đặt màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Defender Tower Map")
clock = pygame.time.Clock()
# Màu sắc
# Tọa độ các điểm mốc (waypoints) trên bản đồ
WAYPOINTS1 = [(379, 2), (383, 86), (359, 176), (310, 237), (227, 272), (189, 350), (213, 405), (290, 428), (372, 427), (477, 433), (550, 435), (629, 416), (694, 371), (748, 359), (798, 361)]
WAYPOINTS2= [(791, 205), (685, 205), (627, 191), (573, 129), (561, 90), (500, 77), (436, 116), (428, 160), (401, 206), (335, 219), (255, 216), (191, 248), (187, 282), (223, 311), (294, 342), (342, 330), (422, 320), (485, 329), (531, 361), (529, 410), (487, 437), (424, 450), (359, 478), (349, 528), (355, 570), (350, 599)]
WAYPOINTS3=[(5, 372), (223, 378), (331, 397), (433, 443), (538, 445), (607, 412), (583, 349), (485, 321), (415, 273), (465, 230), (572, 228), (649, 239), (709, 260), (775, 270), (796, 276)]
WAYPOINTS3_1= [(1, 371), (120, 368), (204, 374), (285, 390), (357, 431), (459, 443), (545, 446), (588, 422), (595, 375), (508, 327), (410, 290), (348, 266), (285, 214), (306, 163), (403, 147), (481, 137), (591, 138), (670, 138), (749, 138), (797, 144)]
WAYPOINTS4=[(338, 586), (338, 465), (315, 428), (236, 387), (155, 294), (128, 209), (164, 133), (249, 95), (306, 81), (386, 76), (431, 79), (462, 10), (468, 1)]
WAYPOINTS4_1=[(347, 594), (354, 486), (364, 451), (480, 452), (562, 453), (631, 437), (702, 388), (736, 313), (698, 222), (632, 163), (595, 127), (541, 92), (470, 69), (460, 4)]
WAYPOINTS5=[(445, 594), (423, 514), (385, 439), (292, 420), (180, 409), (114, 349), (118, 273), (200, 206), (285, 166), (425, 143), (505, 126), (555, 87), (573, 16), (572, 5)]
WAYPOINTS5_1=[(451, 594), (432, 493), (373, 447), (307, 420), (295, 329), (346, 277), (442, 266), (524, 249), (537, 173), (553, 78), (569, 17), (575, 6)]
WAYPOINTS5_2=[(799, 475), (731, 479), (681, 460), (632, 406), (635, 328), (632, 291), (572, 261), (531, 207), (527, 151), (558, 68), (580, 24), (586, 3)]
WAYPOINTS6=[(406, 591), (404, 446), (401, 413), (479, 414), (546, 407), (570, 405), (580, 345), (579, 293), (637, 277), (699, 249), (702, 206), (661, 178), (544, 182), (476, 177), (420, 174), 
(399, 123), (402, 72), (396, 14)]
WAYPOINTS6_1=[(405, 595), (403, 503), (398, 426), (347, 415), (257, 411), (222, 395), (206, 338), (203, 304), (157, 284), (127, 257), (125, 210), (168, 181), (265, 176), (350, 172), (386, 172), 
(406, 92), (398, 30), (397, 3)]
WAYPOINTS6_2=[(3, 415), (111, 406), (194, 409), (216, 371), (218, 327), (285, 284), (329, 290), (408, 280), (407, 226), (412, 171), (411, 105), (408, 76), (405, 6)]
WAYPOINTS6_3=[(796, 412), (673, 419), (615, 421), (582, 385), (568, 332), (582, 300), (505, 281), (444, 282), (400, 284), (400, 212), (404, 150), (407, 92), (404, 50), (403, 22), (403, 11)]


WAYPOINT_LIST = {}

WAYPOINT_LIST[1] = [WAYPOINTS1]
WAYPOINT_LIST[2] = [WAYPOINTS2]
WAYPOINT_LIST[3] = [WAYPOINTS3, WAYPOINTS3_1]
WAYPOINT_LIST[4] = [WAYPOINTS4, WAYPOINTS4_1]
WAYPOINT_LIST[5] = [WAYPOINTS5, WAYPOINTS5_1, WAYPOINTS5_2]
WAYPOINT_LIST[6] = [WAYPOINTS6, WAYPOINTS6_1, WAYPOINTS6_2, WAYPOINTS6_3]


tower_cost = 20
tower_radius = 50

def is_valid_build(x, y,towers, min_distance):
        for tower in towers:
            distance = math.sqrt((tower.rect.centerx - x) ** 2 + (tower.rect.centery - y) ** 2)
            if distance < min_distance * 2:
                return False
        return True
   
# Lớp Map để quản lý cấp độ
class Map:
    def __init__(self, screen):
        self.maps = ["map1.png", "map2.png", "map3.png", "map4.png", "map5.png", "map6.png"]
        self.level = 1
        self.screen = screen

    def draw_map(self):
        background_image = pygame.image.load("./assets/images/" + self.maps[self.level - 1])
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, [0, 0])

    def next_map(self):
        self.level += 1
        if self.level > len(self.maps):
            self.level = 1  # Quay lại bản đồ đầu tiên nếu vượt qua số lượng bản đồ

    def get_level(self):
        return self.level

player = Player(screen)

# Vòng lặp chính
running = True
map = Map(screen)
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64
enemies = []
currentime = 0

# Tạo nhóm cho tháp và đạn
towers = pygame.sprite.Group()
bullets = pygame.sprite.Group()

time = [60, 180, 300, 420, 1000, 1020, 1040, 1700, 1760, 1820, 1880]
time2 =[280,340,400,460,1520,1580,1640,1700]
time3 =[420,440,460,480,500,520,540,600]
time4 =[620,640,660,680,700,720,740,760]
time5 =[300, 320,  1200, 1300, 1400, 1500, 1800, 1810, 1820]


display_text = False 
pausing = False
while running:
    fps = clock.tick(60)
    map.draw_map()
    currentime += 1
    
    if currentime in time :
        enemy = Person(screen, map.get_level(), WAYPOINT_LIST)
        enemies.append(enemy)
    if currentime in time2:
        enemy = Gobin(screen, map.get_level(), WAYPOINT_LIST)
        enemies.append(enemy)
    if currentime in time5:
        enemy = Shaman(screen, map.get_level(), WAYPOINT_LIST)
        enemies.append(enemy)
    if currentime >= time[-1] and len(enemies) == 0:
        map.next_map()
        towers.empty()
        enemies = []
        player.set_gold(60)
        # player.set_hp(100)
        print("Next map", map.get_level())
        currentime = 0   
    for enemy in enemies:
        if enemy.is_at_end():
            player.remove_hp(10)
            enemies.remove(enemy)
            if player.is_dead():
                pausing = True

                
                
            
   
    # Bắn đạn từ các tháp
    for tower in towers:
        tower.shoot(enemies, bullets)

    # Cập nhật vị trí đạn
    bullets.update(enemies, player)

    bullets.draw(screen)
    towers.update()
    towers.draw(screen)
    player.draw(currentime)
    if pausing == False:
        for enemy in enemies:
            enemy.update()
            enemy.draw()
    # Đặt tháp khi nhấn chuột
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if player.get_gold() >= tower_cost and is_valid_build(mouse_x, mouse_y, towers, tower_radius):
                tower = Tower(mouse_x, mouse_y)
                player.remove_gold(tower_cost)
                towers.add(tower)
                text = font.render("Tower bought", True, BLACK)
                screen.blit(text, (300, 300))
            else:
                text = font.render("Not enough gold", True, BLACK)
                screen.blit(text, (300, 300))
            
    if pausing:
        textgameover = font.render("Game Over", True, BLACK)
        screen.blit(textgameover, (300, 300))

    pygame.display.flip()

pygame.quit()