import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Đào Vàng')

clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GOLD = (255, 223, 0)
BLACK = (0 , 0 , 0)
hook_x , hook_y = WIDTH // 2, HEIGHT // 4
hook_angle = 0
hook_length = 100
hook_speed = 2
hook_grab = False
hook_velocity = 2

#đối tượng vàng 
class Gold:
    def __init__(self, x, y, size, value):
        self.x = x
        self.y = y
        self.size = size
        self.value = value
        self.is_collected = False

    def draw(self):
        pygame.draw.circle(screen, GOLD, (self.x, self.y), self.size )

gold_list = []
for i in range(5):
    gold_size = random.randint(10, 20)
    gold_value = gold_size * 10
    gold_x = random.randint(gold_size, WIDTH - gold_size)
    gold_y = random.randint(HEIGHT // 2, HEIGHT - gold_size)
    gold = Gold(gold_x, gold_y, gold_size, gold_value)
    gold_list.append(gold)

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

score = 0

running = True

while running:
    screen.fill(WHITE)

    end_x = hook_x + hook_length * math.cos(math.radians(hook_angle))
    end_y = hook_y + hook_length * math.sin(math.radians(hook_angle))
    pygame.draw.line(screen, BLACK, (hook_x, hook_y), (end_x, end_y), 5)

    if not hook_grab:
        # hook_x = hook_x + hook_speed * math.cos(hook_angle)
        # hook_y = hook_y + hook_speed * math.sin(hook_angle)
        hook_angle = hook_angle + hook_velocity
        if hook_angle > 180 or hook_angle < 0:
            hook_velocity = -hook_velocity
        # hook_x = min(max(hook_x, 0), WIDTH)
        # hook_x = min(max(hook_x, hook_length), WIDTH - hook_length)
        end_x = hook_x + hook_length * math.cos(math.radians(hook_angle))
        end_y = hook_y + hook_length * math.sin(math.radians(hook_angle))
       
        
    elif hook_angle > 90 or hook_angle < -90:
        hook_speed = -hook_speed
    else:
        hook_x = pygame.mouse.get_pos()[0]
        hook_y = pygame.mouse.get_pos()[1]
        hook_length += hook_velocity
    

    for gold in gold_list:
        gold.draw()
        if distance(hook_x, hook_y, gold.x, gold.y) < gold.size // 2: 
            gold.is_collected = True
            score += gold.value
            break
    #kéo vàng về
    if gold.is_collected:
        score += gold.value
        gold_list.remove(gold)
        gold.is_collected = False
        hook_length += 10
        hook_velocity += 0.1 
    #choi game
    
    # In chữ chữ Hello World
    # font = pygame.font.Font(None, 36)
    text = font.render('Hello World', True, BLACK)
    screen.blit(text, (10, 10))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                hook_grab = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                hook_grab = False
                hook_velocity = 0
    
    # In ra chữ Hello World
    # font = pygame.font.Font(None, 36)
    text = font.render('Hello World', True, BLACK)
    screen.blit(text, (10, 10))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    font = pygame.font.Font(None, 36)
    text = font.render('Score: ' + str(score), True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()