from js import document, window
from pyodide.ffi import create_proxy
import random
import time

# Game constants
GRID_SIZE = 20
CELL_SIZE = 20
GRID_WIDTH = 400 // CELL_SIZE
GRID_HEIGHT = 400 // CELL_SIZE

# Colors
SNAKE_COLOR = "#4CAF50"
FOOD_COLOR = "#FF5722"

# Initialize game variables
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
food = None
direction = "right"
score = 0
game_over = False

# Get canvas context
canvas = document.getElementById("gameCanvas")
ctx = canvas.getContext("2d")

# Set focus to canvas
canvas.focus()

def generate_food():
    global food
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            food = (x, y)
            break

def draw():
    # Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    # Draw snake
    for segment in snake:
        x, y = segment
        ctx.fillStyle = SNAKE_COLOR
        ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
    
    # Draw food
    if food:
        ctx.fillStyle = FOOD_COLOR
        ctx.fillRect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)

def move():
    global snake, food, score, game_over
    
    if game_over:
        return
    
    # Get current head position
    head_x, head_y = snake[0]
    
    # Calculate new head position
    if direction == "up":
        new_head = (head_x, head_y - 1)
    elif direction == "down":
        new_head = (head_x, head_y + 1)
    elif direction == "left":
        new_head = (head_x - 1, head_y)
    else:  # right
        new_head = (head_x + 1, head_y)
    
    # Check for collisions
    if (new_head in snake or 
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
        game_over = True
        return
    
    # Add new head
    snake.insert(0, new_head)
    
    # Check if food is eaten
    if new_head == food:
        score += 1
        document.getElementById("score-value").textContent = str(score)
        generate_food()
    else:
        snake.pop()

def handle_keydown(event):
    global direction
    key = event.key.lower()
    
    if (key == "arrowup" or key == "w") and direction != "down":
        direction = "up"
    elif (key == "arrowdown" or key == "s") and direction != "up":
        direction = "down"
    elif (key == "arrowleft" or key == "a") and direction != "right":
        direction = "left"
    elif (key == "arrowright" or key == "d") and direction != "left":
        direction = "right"

def game_loop():
    move()
    draw()
    if not game_over:
        proxy_game_loop = create_proxy(game_loop)
        window.setTimeout(proxy_game_loop, 150)
    else:
        ctx.fillStyle = "red"
        ctx.font = "30px Arial"
        ctx.fillText("Trò Chơi Kết Thúc!", canvas.width/2 - 100, canvas.height/2)

# Set up event listeners
proxy_handle_keydown = create_proxy(handle_keydown)
document.addEventListener("keydown", proxy_handle_keydown)

# Start the game
generate_food()
proxy_game_loop = create_proxy(game_loop)
game_loop()
