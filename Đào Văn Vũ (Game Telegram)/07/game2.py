import pygame
import random 
import time
import math

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Defender Tower Map")
clock = pygame.time.Clock()
# Màu sắc
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
GRAY = (105, 105, 105)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
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

player_gold = 60
tower_cost = 20
tower_radius = 50

class Enemy:
    def get_sprite(self):
        x = self.current_frame * 64
        y = 0
        width = self.width
        height = 64
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

        self.current_frame += 1
        if self.current_frame >= self.num_frames:
            self.current_frame = 0

    def draw(self):
        pygame.draw.rect(self.screen, (GREEN), (self.x -30, self.y - 45, (self.health / self.max_health) * self.width, 14))
        sprite = self.get_sprite()

        # Quay lại nếu đi qua trái
        if self.x > self.waypoints[self.index_waypoints][0]:
            sprite = pygame.transform.flip(sprite, True, False)
        self.screen.blit(sprite, (self.x - 32, self.y - 32))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            # Xóa kẻ thù nếu hết máu
            return True
        return False
    
    # Kiểm tra đi tới waypoint cuối cùng
    def is_at_end(self):
        return self.index_waypoints == len(self.waypoints) - 1
    


# Lớp kẻ thù (Player chỉ là một ví dụ, bạn có thể đổi tên thành `Enemy`)
class Player(Enemy):
    def __init__(self, screen, level, waypoint_list):
        intdex_random = random.randint(0, len(waypoint_list[level]) - 1)
        self.waypoints = waypoint_list[level][intdex_random]
        self.screen = screen
        self.sprite_sheet = pygame.image.load("idleR.png").convert_alpha()
        self.current_frame = 0
        self.num_frames = self.sprite_sheet.get_width() // 64
        self.index_waypoints = 0
        self.speed = 3  # Tốc độ di chuyển
        self.x, self.y = self.waypoints[0]  # Bắt đầu tại điểm mốc đầu tiên
        self.health = 100
        self.max_health = 100
        self.width = 64

    def get_sprite(self):
        x = self.current_frame * 64
        y = 0
        width = self.width
        height = 64
        sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
        return sprite

    
class Gobin(Enemy):
    def __init__(self, screen, level, waypoint_list):
        self.screen = screen
        self.width = 514 / 6
        self.height = 486 / 4
       
        intdex_random = random.randint(0, len(waypoint_list[level]) - 1)
        self.waypoints = waypoint_list[level][intdex_random]
        self.screen = screen
        self.sprite_sheet = pygame.image.load("c.png").convert_alpha()
        self.current_frame = 0
        self.num_frames = self.sprite_sheet.get_width() // self.width
        self.index_waypoints = 0
        self.speed = 2  # Tốc độ di chuyển
        self.x, self.y = self.waypoints[0]  # Bắt đầu tại điểm mốc đầu tiên
        self.health = 10
        self.max_health = 10

    def get_sprite(self):
        x = self.current_frame * self.width
        y = 1 * self.height
        width = self.width
        height = self.height

        sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
        return sprite

# class Shaman:
#     def __init__(self, screen, level, waypoint_list):
#         self.screen = screen
#         self.width = 514 / 6
#         self.height = 486 / 4
       
#         intdex_random = random.randint(0, len(waypoint_list[level]) - 1)
#         self.waypoints = waypoint_list[level][intdex_random]
#         self.screen = screen
#         self.sprite_sheet = pygame.image.load("c.png").convert_alpha()
#         self.current_frame = 0
#         self.num_frames = self.sprite_sheet.get_width() // self.width
#         self.index_waypoints = 0
#         self.speed = 2  # Tốc độ di chuyển
#         self.x, self.y = self.waypoints[0]  # Bắt đầu tại điểm mốc đầu tiên
#         self.health = 10

#     def get_sprite(self):
#         x = self.current_frame * self.width
#         y = 3 * self.height
#         width = self.width
#         height = self.height

#         sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
#         return sprite


#     def update(self):
#         # Di chuyển dọc theo waypoints
#         if self.index_waypoints < len(self.waypoints) - 1:
#             target_x, target_y = self.waypoints[self.index_waypoints]
#             dx, dy = target_x - self.x, target_y - self.y
#             distance = math.hypot(dx, dy)

#             if distance > 0:
#                 self.x += dx / distance * self.speed
#                 self.y += dy / distance * self.speed

#             # Khi đến gần waypoint hiện tại, chuyển sang waypoint tiếp theo
#             if distance < 5:  
#                 self.index_waypoints += 1

#         self.current_frame += 1
#         if self.current_frame >= self.num_frames:
#             self.current_frame = 0

#     def draw(self):
#         pygame.draw.rect(self.screen, (GREEN), (self.x -30, self.y - 45, self.health // 2, 14))
#         sprite = self.get_sprite()
#         self.screen.blit(sprite, (self.x - self.width//2, self.y - self.height//2))

#     def take_damage(self, damage):
#         self.health -= damage
#         if self.health <= 0:
#             # Xóa kẻ thù nếu hết máu
#             return True
#         return False
    
#     # Kiểm tra đi tới waypoint cuối cùng
#     def is_at_end(self):
#         return self.index_waypoints == len(self.waypoints) - 1
# class Orc:
#     def __init__(self, screen, level, waypoint_list):
#         self.screen = screen
#         self.width = 514 / 6
#         self.height = 486 / 4
       
#         intdex_random = random.randint(0, len(waypoint_list[level]) - 1)
#         self.waypoints = waypoint_list[level][intdex_random]
#         self.screen = screen
#         self.sprite_sheet = pygame.image.load("c.png").convert_alpha()
#         self.current_frame = 0
#         self.num_frames = self.sprite_sheet.get_width() // self.width
#         self.index_waypoints = 0
#         self.speed = 2  # Tốc độ di chuyển
#         self.x, self.y = self.waypoints[0]  # Bắt đầu tại điểm mốc đầu tiên
#         self.health = 10

#     def get_sprite(self):
#         x = self.current_frame * self.width
#         y = 2 * self.height
#         width = self.width
#         height = self.height

#         sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
#         return sprite


#     def update(self):
#         # Di chuyển dọc theo waypoints
#         if self.index_waypoints < len(self.waypoints) - 1:
#             target_x, target_y = self.waypoints[self.index_waypoints]
#             dx, dy = target_x - self.x, target_y - self.y
#             distance = math.hypot(dx, dy)

#             if distance > 0:
#                 self.x += dx / distance * self.speed
#                 self.y += dy / distance * self.speed

#             # Khi đến gần waypoint hiện tại, chuyển sang waypoint tiếp theo
#             if distance < 5:  
#                 self.index_waypoints += 1

#         self.current_frame += 1
#         if self.current_frame >= self.num_frames:
#             self.current_frame = 0

#     def draw(self):
#         pygame.draw.rect(self.screen, (GREEN), (self.x -30, self.y - 45, self.health // 2, 14))
#         sprite = self.get_sprite()
#         self.screen.blit(sprite, (self.x - self.width//2, self.y - self.height//2))

#     def take_damage(self, damage):
#         self.health -= damage
#         if self.health <= 0:
#             # Xóa kẻ thù nếu hết máu
#             return True
#         return False
    
#     # Kiểm tra đi tới waypoint cuối cùng
#     def is_at_end(self):
#         return self.index_waypoints == len(self.waypoints) - 1


# Lớp đạn
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.target = target
        self.speed = 5

    def update(self):
        dx = self.target.x - self.rect.x
        dy = self.target.y - self.rect.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.rect.x += dx / distance * self.speed
            self.rect.y += dy / distance * self.speed

        # Kiểm tra va chạm với kẻ thù
        if pygame.Rect.colliderect(self.rect, pygame.Rect(self.target.x, self.target.y, 64, 64)):
            global player_gold
            if self.target.take_damage(10):
                
                if self.target in players:
                    player_gold += 10 
                    players.remove(self.target)  # Xóa kẻ thù nếu bị giết
            self.kill()  # Xóa đạn sau khi va chạm
def is_valid_build(x, y,towers, min_distance):
        for tower in towers:
            distance = math.sqrt((tower.rect.centerx - x) ** 2 + (tower.rect.centery - y) ** 2)
            if distance < min_distance * 2:
                return False
        return True
# Lớp tháp (Tower)
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('towermage.png')
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
   
# Lớp Map để quản lý cấp độ
class Map:
    def __init__(self, screen):
        self.maps = ["map1.png", "map2.png", "map3.png", "map4.png", "map5.png", "map6.png"]
        self.level = 1
        self.screen = screen

    def draw_map(self):
        background_image = pygame.image.load(self.maps[self.level - 1])
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, [0, 0])

    def next_map(self):
        self.level += 1
        if self.level > len(self.maps):
            self.level = 1  # Quay lại bản đồ đầu tiên nếu vượt qua số lượng bản đồ

    def get_level(self):
        return self.level

# Vòng lặp chính
running = True
map = Map(screen)
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64
player = Player(screen, 1, WAYPOINT_LIST)
players = [player]
currentime = 0

# Tạo nhóm cho tháp và đạn
towers = pygame.sprite.Group()
bullets = pygame.sprite.Group()
font = pygame.font.SysFont('sans', 50)
time = [120,140,160,180,200,220]
time2 =[80,100,120,140,190,240,300,360,380,400,420,440]
time3 =[420,440,460,480,500,520,540,600]
time4 =[620,640,660,680,700,720,740,760]

hp = 100

  
display_text = False 
pausing = False
while running:
    fps = clock.tick(60)
   
       
        
    
    map.draw_map()
    currentime += 1
    pygame.draw.rect(screen, WHITE, (730, 0, 90, 50))
    text = font.render(str(currentime // 60), True, BLACK)
    texthp = font.render(str(hp), True, RED)
    textgold = font.render(str(player_gold), True, YELLOW)
    screen.blit(textgold, (0, 0))
    screen.blit(texthp, (0, 50))
    screen.blit(text, (730, 0))
    if currentime in time :
        player = Player(screen, map.get_level(), WAYPOINT_LIST)
        players.append(player)
    if currentime in time2:
        player = Gobin(screen, map.get_level(), WAYPOINT_LIST)
        players.append(player)
    # if currentime in time3:
    #     player = Shaman(screen, map.get_level(), WAYPOINT_LIST)
    #     players.append(player)
    # if currentime in time4:
    #     player = Orc(screen, map.get_level(), WAYPOINT_LIST)
    #     players.append(player)
    if pausing == False:
        for player in players:
            player.update()
            player.draw()
    if currentime >= time[-1] and len(players) == 0:
        map.next_map()
        towers.empty()
        players = []
        player_gold = 60
        hp = 100
        print("Next map", map.get_level())
        currentime = 0   
    for player in players:
        if player.is_at_end():
            hp -= 10
            players.remove(player)
            if hp <= 0:
                pausing = True

                
                
            
   
    # Bắn đạn từ các tháp
    for tower in towers:
        tower.shoot(players, bullets)

    # Cập nhật vị trí đạn
    bullets.update()
    bullets.draw(screen)
    towers.update()
    towers.draw(screen)
    # Đặt tháp khi nhấn chuột
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if player_gold >= tower_cost and is_valid_build(mouse_x, mouse_y, towers, tower_radius):
                tower = Tower(mouse_x, mouse_y)
                player_gold -= tower_cost
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