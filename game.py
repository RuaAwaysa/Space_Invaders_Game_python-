import pygame
import random
import math

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('assets/images/background1.jpg')

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-ship.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))  # Resize player
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
alien_shoot_delay = []
alien_last_shot_time = []  # Track the last time each alien fired
shoot_delay_duration = 3000  # Slower shoot delay (3 seconds between shots)

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (50, 50))  # Resize enemy
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)  # Slower movement
    enemyY_change.append(20)
    alien_last_shot_time.append(0)  # Initialize last shot time for each alien

# Alien Bullet
alien_bulletImg = pygame.image.load('bullet.png')
alien_bulletImg = pygame.transform.scale(alien_bulletImg, (16, 32))
alien_bulletX = []
alien_bulletY = []
alien_bulletY_change = 1.5  # Slower alien bullet speed
alien_bullet_state = []  # track state of bullets ("ready" or "fire")

# Initialize the alien bullets state for each enemy
for i in range(num_of_enemies):
    alien_bulletX.append(0)
    alien_bulletY.append(0)
    alien_bullet_state.append("ready")

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (16, 32))  # Resize bullet
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6  # Slower bullet speed
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Game Over Flag
game_over = False


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def fire_alien_bullet(x, y, i):
    global alien_bullet_state
    alien_bullet_state[i] = "fire"
    screen.blit(alien_bulletImg, (x + 16, y + 20))

def is_collision(obj1X, obj1Y, obj2X, obj2Y, threshold=27):
    distance = math.sqrt(math.pow(obj1X - obj2X, 2) + math.pow(obj1Y - obj2Y, 2))
    return distance < threshold

def restart_game():
    global playerX, playerY, playerX_change, bulletX, bulletY, bullet_state, score_value, game_over
    global enemyX, enemyY, enemyX_change, enemyY_change, alien_bulletY, alien_bullet_state

    # Reset player position and bullet state
    playerX = 370
    playerY = 480
    playerX_change = 0
    bulletY = 480
    bullet_state = "ready"

    # Reset enemies and alien bullets
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)
        alien_bulletY[i] = enemyY[i]
        alien_bullet_state[i] = "ready"
        alien_last_shot_time[i] = 0  # Reset the last shot time

    # Reset score and game_over flag
    score_value = 0
    game_over = False

# Game Loop
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3  # Slower player movement
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

            if event.key == pygame.K_RETURN and game_over:
                # Restart the game after game over
                restart_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not game_over:
        # Player Movement
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440 or is_collision(enemyX[i], enemyY[i], playerX, playerY, 50):
                game_over = True
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.5  # Slower enemy movement
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.5
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

            # Alien shooting logic (individual delay for each alien)
            current_time = pygame.time.get_ticks()
            if alien_bullet_state[i] == "ready" and current_time - alien_last_shot_time[i] > shoot_delay_duration:
                if random.randint(0, 100) < 5:  # 5% chance of firing
                    alien_bulletX[i] = enemyX[i]
                    alien_bulletY[i] = enemyY[i]
                    fire_alien_bullet(alien_bulletX[i], alien_bulletY[i], i)
                    alien_last_shot_time[i] = current_time

            if alien_bullet_state[i] == "fire":
                fire_alien_bullet(alien_bulletX[i], alien_bulletY[i], i)
                alien_bulletY[i] += alien_bulletY_change

            # If alien bullet hits the player
            if is_collision(alien_bulletX[i], alien_bulletY[i], playerX, playerY, 30):
                game_over = True
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            # Reset alien bullet when it leaves screen
            if alien_bulletY[i] > 600:
                alien_bullet_state[i] = "ready"

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    if game_over:
        game_over_text()

    pygame.display.update()
