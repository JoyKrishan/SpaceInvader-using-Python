import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Initialize the screen (width, height)
screen = pygame.display.set_mode((800, 400))

# adding the background
background = pygame.transform.scale(pygame.image.load("1847.jpg"), (800, 400))
brighten = 128
background.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)

# adding background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Change the title of the window
pygame.display.set_caption("Space INVADER")
# displaying a icon
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playering = pygame.transform.scale(pygame.image.load("player.png"), (50, 30))
playerX = 370
playerY = 360
player_change = 0

# Opponent
enemies = []
enemiesX = []
enemiesY = []
enemiesX_change = []
enemiesY_change = []
num_enemies = 5
enemy_speed = 0.5
enemy_drop = 50
for i in range(num_enemies):  # num_enemies is the number of enemies
    enemies.append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("alien.png"), (50, 30)), 180))
    enemiesX.append(random.randint(0, 750))
    enemiesY.append(random.randint(10, 200))
    enemiesX_change.append(enemy_speed)
    enemiesY_change.append(enemy_drop)

# Bullet
# "ready" = not fired
# "fire" = fired
bullet_speed = 1
bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 340
bulletX_change = bullet_speed
bulletY_change = bullet_speed
bullet_state = "ready"


def player(x, y):
    screen.blit(playering, (x, y))


def opponent(x, y, i):
    screen.blit(enemies[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 10, y + 10))


def collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distance < 27:
        return True
    return False


score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10


def show_score(x, y):
    global score
    score_val = font.render("Score :" + str(score), True, (0, 0, 0))
    screen.blit(score_val, (x, y))


font2 = pygame.font.Font("freesansbold.ttf", 64)


def game_over():
    game_over_text = font2.render("GAME OVER", True, (0, 0, 0))
    screen.blit(game_over_text, (300, 250))


# Game Loop
running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if a keystroke is pressed check if its right or left
    if event.type == pygame.KEYDOWN:  # check if any key is pressed
        if event.key == pygame.K_LEFT:
            player_change -= 0.05
        if event.key == pygame.K_RIGHT:
            player_change += 0.05
        if event.key == pygame.K_RETURN:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                fire_bullet(playerX, bulletY)
                bulletX = playerX
    if event.type == pygame.KEYUP:
        player_change = 0

    playerX += player_change
    # make the boundary
    if playerX >= 750:
        playerX = 750
    elif playerX <= 0:
        playerX = 0

    for i in range(num_enemies):

        if enemiesY[i] > 300:
            for j in range(num_enemies):
                enemiesY[j] = 2000
            game_over()
            break
        enemiesX[i] += enemiesX_change[i]
        # make the boundary
        if enemiesX[i] >= 750:
            enemiesX_change[i] = -enemy_speed
            enemiesY[i] += enemiesY_change[i]
        elif enemiesX[i] <= 0:
            enemiesX_change[i] = enemy_speed
            enemiesY[i] += enemiesY_change[i]
        # collision
        if collision(enemiesX[i], enemiesY[i], bulletX, bulletY):
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 340
            bullet_state = "ready"
            score += 1
            print(score)
            enemiesX[i] = random.randint(0, 750)
            enemiesY[i] = random.randint(10, 200)
        opponent(enemiesX[i], enemiesY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 340
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
