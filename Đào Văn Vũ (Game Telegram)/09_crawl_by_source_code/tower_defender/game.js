- index.html
- game.py
- map1.png
- towermage.png
- idleR.png
- goblin.png// Game canvas
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const goldDisplay = document.getElementById('gold');

// Game constants
const TOWER_COST = 20;
const TOWER_RANGE = 150;
const ENEMY_HEALTH = 100;
const BULLET_SPEED = 5;
const ENEMY_SPEED = 3;
const GOBLIN_HEALTH = 80;
const GOBLIN_SPEED = 4;

// Game state
let gold = 60;
let towers = [];
let enemies = [];
let bullets = [];
let time1 = 0;
let time2 = 0;
let gameStartTime = Date.now();

// Waypoints for enemies
const WAYPOINTS = [
    {x: 379, y: 2}, {x: 383, y: 86}, {x: 359, y: 176},
    {x: 310, y: 237}, {x: 227, y: 272}, {x: 189, y: 350},
    {x: 191, y: 427}, {x: 250, y: 492}, {x: 369, y: 552},
    {x: 489, y: 552}, {x: 573, y: 493}
];

// Load images
const mapImage = new Image();
mapImage.src = 'map1.png';
const towerImage = new Image();
towerImage.src = 'towermage.png';
const enemyImage = new Image();
enemyImage.src = 'idleR.png';
const goblinImage = new Image();
goblinImage.src = 'goblin.png';

class Tower {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.lastShot = 0;
        this.cooldown = 1000; // 1 second cooldown
    }

    draw() {
        // Draw tower
        ctx.drawImage(towerImage, this.x - 32, this.y - 32, 64, 64);
        
        // Draw range circle
        ctx.beginPath();
        ctx.arc(this.x, this.y, TOWER_RANGE, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 0, 0.1)';
        ctx.fill();
        ctx.strokeStyle = 'rgba(255, 255, 0, 0.3)';
        ctx.stroke();
    }

    update() {
        const now = Date.now();
        if (now - this.lastShot < this.cooldown) return;

        for (let enemy of enemies) {
            const dx = enemy.x - this.x;
            const dy = enemy.y - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance <= TOWER_RANGE) {
                bullets.push(new Bullet(this.x, this.y, enemy));
                this.lastShot = now;
                break;
            }
        }
    }
}

class Enemy {
    constructor(type = 'player') {
        this.waypointIndex = 0;
        this.x = WAYPOINTS[0].x;
        this.y = WAYPOINTS[0].y;
        this.type = type;
        this.health = type === 'player' ? ENEMY_HEALTH : GOBLIN_HEALTH;
        this.speed = type === 'player' ? ENEMY_SPEED : GOBLIN_SPEED;
        this.maxHealth = this.health;
        this.frameWidth = 64;
        this.frameHeight = 64;
        this.currentFrame = 0;
        this.frameCount = 6;
        this.frameTimer = 0;
    }

    update() {
        if (this.waypointIndex >= WAYPOINTS.length - 1) return true;

        const target = WAYPOINTS[this.waypointIndex + 1];
        const dx = target.x - this.x;
        const dy = target.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 5) {
            this.waypointIndex++;
        } else {
            this.x += (dx / distance) * this.speed;
            this.y += (dy / distance) * this.speed;
        }

        // Update animation
        this.frameTimer++;
        if (this.frameTimer > 5) {
            this.currentFrame = (this.currentFrame + 1) % this.frameCount;
            this.frameTimer = 0;
        }

        return false;
    }

    draw() {
        // Draw enemy sprite
        const sprite = this.type === 'player' ? enemyImage : goblinImage;
        ctx.drawImage(
            sprite,
            this.currentFrame * this.frameWidth, 0,
            this.frameWidth, this.frameHeight,
            this.x - 32, this.y - 32,
            this.frameWidth, this.frameHeight
        );

        // Draw health bar
        ctx.fillStyle = 'red';
        ctx.fillRect(this.x - 25, this.y - 40, 50, 5);
        ctx.fillStyle = 'green';
        ctx.fillRect(this.x - 25, this.y - 40, (this.health / this.maxHealth) * 50, 5);

        // Draw enemy type
        ctx.fillStyle = 'white';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(this.type.toUpperCase(), this.x, this.y - 45);
    }

    takeDamage(damage) {
        this.health -= damage;
        if (this.health <= 0) {
            gold += 10;
            goldDisplay.textContent = gold;
            return true;
        }
        return false;
    }
}

class Bullet {
    constructor(x, y, target) {
        this.x = x;
        this.y = y;
        this.target = target;
        this.damage = 20;
    }

    update() {
        const dx = this.target.x - this.x;
        const dy = this.target.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 5) {
            if (this.target.takeDamage(this.damage)) {
                const index = enemies.indexOf(this.target);
                if (index > -1) {
                    enemies.splice(index, 1);
                }
            }
            return true;
        }

        this.x += (dx / distance) * BULLET_SPEED;
        this.y += (dy / distance) * BULLET_SPEED;
        return false;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = 'yellow';
        ctx.fill();
    }
}

function spawnEnemy() {
    const currentTime = Date.now();
    const elapsedTime = currentTime - gameStartTime;
    
    // Update times
    time1 = Math.floor(elapsedTime / 1000);
    time2 = Math.floor(elapsedTime / 1000);
    
    // Spawn enemies
    if (time1 > 0 && Math.random() < 0.02) {
        enemies.push(new Enemy('player'));
    }
    if (time2 > 0 && Math.random() < 0.01) {
        enemies.push(new Enemy('goblin'));
    }
}

function updateGame() {
    // Update all game objects
    towers.forEach(tower => tower.update());
    
    // Update enemies
    for (let i = enemies.length - 1; i >= 0; i--) {
        if (enemies[i].update()) {
            enemies.splice(i, 1);
        }
    }
    
    // Update bullets
    for (let i = bullets.length - 1; i >= 0; i--) {
        if (bullets[i].update()) {
            bullets.splice(i, 1);
        }
    }
}

function drawGame() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw map
    ctx.drawImage(mapImage, 0, 0, canvas.width, canvas.height);
    
    // Draw path (for debugging)
    ctx.beginPath();
    ctx.moveTo(WAYPOINTS[0].x, WAYPOINTS[0].y);
    for (let i = 1; i < WAYPOINTS.length; i++) {
        ctx.lineTo(WAYPOINTS[i].x, WAYPOINTS[i].y);
    }
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.stroke();
    
    // Draw game objects
    towers.forEach(tower => tower.draw());
    enemies.forEach(enemy => enemy.draw());
    bullets.forEach(bullet => bullet.draw());
    
    // Draw UI
    ctx.fillStyle = 'white';
    ctx.font = '20px Arial';
    ctx.textAlign = 'left';
    ctx.fillText(`Time1: ${time1}s`, 10, 30);
    ctx.fillText(`Time2: ${time2}s`, 10, 60);
    ctx.fillText(`Gold: ${gold}`, canvas.width - 100, 30);
}

function gameLoop() {
    spawnEnemy();
    updateGame();
    drawGame();
    requestAnimationFrame(gameLoop);
}

// Handle tower placement
canvas.addEventListener('click', (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    if (gold >= TOWER_COST) {
        towers.push(new Tower(x, y));
        gold -= TOWER_COST;
        goldDisplay.textContent = gold;
    }
});

// Start game when all images are loaded
Promise.all([
    new Promise(resolve => mapImage.onload = resolve),
    new Promise(resolve => towerImage.onload = resolve),
    new Promise(resolve => enemyImage.onload = resolve),
    new Promise(resolve => goblinImage.onload = resolve)
]).then(() => {
    gameStartTime = Date.now();
    gameLoop();
});
