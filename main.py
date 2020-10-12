from math import pow, sqrt
from random import randint

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# background - sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space lavender")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
nums_of_enemy = 5

for i in range(nums_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(randint(0, 736))
    enemyY.append(randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
# ready state mean you can't see the bullet, and fire the bullet is currently moving
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score - ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    # blit mean drawing !
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# bullet touch enemy
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = sqrt(pow(enemyX - bulletX, 2) + pow(enemyY - bulletY, 2))
    if distance < 27:
        return True


def reset_enemy(i):
    global score_value, bulletY, bullet_state, enemyX, enemyY
    bulletY = 480
    bullet_state = "ready"
    score_value += 1
    enemyX[i] = randint(0, 736)
    enemyY[i] = randint(50, 150)  # respawn again !


# Game loop
running = True
while running:
    # display color (R-G-B)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # if key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking boundaries !
    playerX += playerX_change

    if playerX > 736:
        playerX = 736
    elif playerX < 0:
        playerX = 0

    # enemy movement
    for i in range(nums_of_enemy):

        # game over
        if enemyY[i] > 440:  # came near to the ship
            for j in range(nums_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] < 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]

        if (is_collision(enemyX[i], enemyY[i], bulletX, bulletY)):
            exposition_sound = mixer.Sound('explosion.wav')
            exposition_sound.play()
            reset_enemy(i)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)

    # player, enemy and  bullet avatar load
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
