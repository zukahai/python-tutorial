import pygame
from time import sleep
from random import randint

pygame.init()
screen = pygame.display.set_mode((601, 601))
pygame.display.set_caption('Snake')
running = True
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

clock = pygame.time.Clock()

# Snake position
# tail - head
snakes = [[5,10], [6, 10]]
direction = "right"

apple = [randint(0,19), randint(0,19)]
font_small = pygame.font.SysFont('sans', 20)
font_big = pygame.font.SysFont('sans', 50)
font = pygame.font.SysFont(None, 36)
score = 0
level = 1
level_up_score = 10 

pausing = False
target = 5




	
while running:		
	clock.tick(level * 2)
	screen.fill(BLACK)

	tail_x = snakes[0][0]
	tail_y = snakes[0][1]

	# Draw grid
	# for i in range(21):
	# 	pygame.draw.line(screen, WHITE,(0,i*30),(600,i*30))
	# 	pygame.draw.line(screen, WHITE,(i*30,0),(i*30,600))

	# Draw snake
	for snake in snakes:
		pygame.draw.rect(screen, GREEN, (snake[0]*30, snake[1]*30, 30, 30))
	# draw head
	pygame.draw.rect(screen, (255, 255, 255), (snakes[-1][0]*30, snakes[-1][1]*30, 30, 30))

	# Draw apple
	pygame.draw.rect(screen, RED, (apple[0]*30, apple[1]*30, 30, 30))

	# check crash with edge
	if snakes[-1][0] < 0 or snakes[-1][0] > 19 or snakes[-1][1] < 0 or snakes[-1][1] > 19:
		pausing = True

	# Draw score
	score_txt = font_small.render("Score: " + str(score), True, WHITE)
	screen.blit(score_txt, (5,5))

	# Draw target
	target_txt = font_small.render("Target: " + str(target), True, WHITE)
	screen.blit(target_txt, (5,25))
	
	# check crash with body
	for i in range(len(snakes)-1):
		if snakes[-1][0] == snakes[i][0] and snakes[-1][1] == snakes[i][1]:
			pausing = True
	# snake = sleep(0.1)
	# Draw game over
	if pausing:
		game_over_txt = font_big.render("Game over, score: " + str(score), True, WHITE)
		press_space_txt = font_big.render("Press Space to continue", True, WHITE)
		screen.blit(game_over_txt, (50,200))
		screen.blit(press_space_txt, (50,300))
	level_text = font.render(f"Level: {level}", True, WHITE)
	screen.blit(level_text, (235, 25))
	if score > level_up_score:
		level += 1
		level_up_score += 10
		apple = [randint(0,19), randint(0,19)]
		snake -= snake
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and direction != "down":
				direction = "up"
			if event.key == pygame.K_DOWN and direction != "up":
				direction = "down"
			if event.key == pygame.K_LEFT and direction != "right":
				direction = "left"
			if event.key == pygame.K_RIGHT and direction != "left":
				direction = "right"
			if event.key == pygame.K_SPACE and pausing == True:
				pausing = False
				snakes = [[5,10], [6, 10]]
				apple = [randint(0,19), randint(0,19)]
				score = 0
				direction = "right"
				level = 1

    # Snake move
	if pausing == False:
		if direction == "right":
			snakes.append([snakes[-1][0]+1, snakes[-1][1]])
			snakes.pop(0)
		if direction == "left":
			snakes.append([snakes[-1][0]-1, snakes[-1][1]])
			snakes.pop(0)
		if direction == "up":
			snakes.append([snakes[-1][0], snakes[-1][1]-1])
			snakes.pop(0)
		if direction == "down":
			snakes.append([snakes[-1][0], snakes[-1][1]+1])
			snakes.pop(0)
	
	# point
	if snakes[-1][0] == apple[0] and snakes[-1][1] == apple[1]:
		snakes.insert(0,[tail_x,tail_y])
		apple = [randint(0,19), randint(0,19)]
		score += 1
		print(score)

	# Next level
	if score == target:
		level += 1
		target += 5
		apple = [randint(0,19), randint(0,19)]
		snakes = [[5,10], [6, 10]]
		direction = "right"

	pygame.display.flip()

pygame.quit()