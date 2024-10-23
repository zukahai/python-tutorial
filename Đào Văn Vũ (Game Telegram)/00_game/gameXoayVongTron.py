import pygame
import numpy as np
import math
import random
class Ball:
    def __init__(self, position, velocity):
      self.pos = np.array(position, dtype=np.float64) #vi tri
      self.v = np.array(velocity, dtype=np.float64) #van toc
      self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  
      self.is_in = True

def is_ball_in_arc(ball_pos,CIRCLE_CENTER, start_angle, end_angle ):
    dx = ball_pos[0] - CIRCLE_CENTER[0]
    dy = ball_pos[1] - CIRCLE_CENTER[1]
    ball_angle = math.atan2(dy,dx)
    start_angle = start_angle % (2 * math.pi)
    end_angle = end_angle % (2 * math.pi)
    if start_angle > end_angle:
        end_angle += 2 * math.pi

    if start_angle <= ball_angle <= end_angle or (start_angle <= ball_angle + 2 * math.pi <= end_angle):
        return True
    
def draw_arc(window, center, radius, start_angle, end_angle):
    p1 = center + (radius + 1000) * np.array([math.cos(start_angle),math.sin(start_angle)])
    p2 = center + (radius + 1000) * np.array([math.cos(end_angle),math.sin(end_angle)])
    pygame.draw.polygon(window,BLACK,[center,p1,p2],0)

pygame.init() #khởi tạo
WIDTH = 800 #biến chiều rộng
HEIGHT = 800 #biến chiều cao 
window = pygame.display.set_mode((WIDTH, HEIGHT)) #biến tạo cửa sổ với kích thước theo biến chiều cao chiều rộng
clock = pygame.time.Clock() 
BLACK = (0, 0, 0) #màu hiển thị
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
CIRCLE_CENTER = np.array([WIDTH/2, HEIGHT/2], dtype=np.float64)
CIRCLE_RADIUS = 150
BALL_RADIUS = 5
ball_pos = np.array([WIDTH/2, HEIGHT/2 - 120], dtype=np.float64)

running = True
GRAVITY = 0.2 # tạo biến trọng lực cho quả bóng rơi
ball_vel = np.array([0,0], dtype=np.float64) #vận tốc
arc_degrees = 60 #độ dây cung 60 độ
start_angle = math.radians(-arc_degrees / 2) #góc bắt đầu 
end_angle = math.radians(arc_degrees / 2) #góc kết thúc dây cung
spinning_speed = 0.01  #tốc độ quay
#is_ball_in = True #tình trạng quả bóng xem ở trong hay ko
balls = [Ball(ball_pos, ball_vel)]

while running: #vòng lặp hiển thị với những nút bấm
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Xử lý k

    start_angle += spinning_speed
    end_angle += spinning_speed
    for ball in balls :
        if ball.pos[1] > HEIGHT or ball_pos[0] < 0 or ball_pos[0] > WIDTH or ball_pos[1] < 0:
            balls.remove(ball)
            balls.append(Ball(position=[WIDTH // 2, HEIGHT // 2 - 120], velocity=[random.uniform(-4, 4), random.uniform(-1, 1)]))
            balls.append(Ball(position=[WIDTH // 2, HEIGHT // 2 - 120], velocity=[random.uniform(-4, 4), random.uniform(-1, 1)]))


        ball.v[1] += GRAVITY
        ball.pos += ball.v 
        dist = np.linalg.norm(ball.pos - CIRCLE_CENTER) #tính độ dài của vector
        if dist + BALL_RADIUS > CIRCLE_RADIUS:
            if is_ball_in_arc(ball.pos,CIRCLE_CENTER, start_angle, end_angle ):
                ball.is_in = False
            if ball.is_in:    
            #bước 1 tính vector d
                d = ball.pos - CIRCLE_CENTER
                d_unit = d/np.linalg.norm(d)
                ball.pos = CIRCLE_CENTER + (CIRCLE_RADIUS - BALL_RADIUS) * d_unit
                #bước 2 tính vector t
                t =np.array([-d[1],d[0]], dtype=np.float64)
                #bước 3
                proj_v_t = (np.dot(ball.v,t)/np.dot(t,t)) *t
                #bước 4
                ball.v = 2 * proj_v_t - ball.v
                ball.v += t * spinning_speed #r = r * w tính lực kéo


    window.fill(BLACK) # cho toàn bộ màn hình màu đen
    pygame.draw.circle(window, ORANGE, CIRCLE_CENTER, CIRCLE_RADIUS, 3) #tạo vòng tròn có độ dày là 3
    draw_arc(window, CIRCLE_CENTER, CIRCLE_RADIUS, start_angle, end_angle)
    for ball in balls:
         pygame.draw.circle(window, ball.color, ball.pos, BALL_RADIUS) #tạo quả bóng màu đỏ


    pygame.display.flip() #flip update thay đổi màn hình
    clock.tick(60) #cho phép 60s thay đổi 1 lần

pygame.quit()