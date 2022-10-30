import math
import random
import pygame
from pygame import mixer



pygame.init()

# creating screen
screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load("5465339.jpg")


# background
background_music = mixer.music.load("background.wav")
mixer.music.play(-1)


# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)

# adding player
playerIMG = pygame.image.load("in_game.png")
playerX = 370
playerY = 480
playerX_change = 0


# adding enemy
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)



#bullet


bulletIMG = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
 
def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG,(x + 16 , y + 10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

def player(x,y):
    screen.blit(playerIMG,(x,y))

def enemy(x,y , i):
    screen.blit(enemyIMG[i],(x,y))

def game_over_text():
    game_over = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(game_over, (200,250))


# game loop
running = True

while running:
    screen.fill((0,0,0))
    #background Image
    screen.blit(background,(0 , 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       
        # key pressed check
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if  event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound ('laser.wav')
                    bullet_sound.play()
                    # get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX,playerY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0




    # checking for boundaries of spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    # enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 480:
            game_over_sound = mixer.Sound("music_gameover.mp3")
            game_over_sound.play()
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        # collision
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)


        enemy(enemyX[i],enemyY[i] , i)


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    

    player(playerX,playerY)
    show_score(textX,textY)

    pygame.display.update()