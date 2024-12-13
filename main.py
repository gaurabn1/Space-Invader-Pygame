import pygame, math, random 
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(pygame.image.load('spaceship.png'))

# Initital Score
score_value = 0

#Font
font = pygame.font.Font('freesansbold.ttf', 32)

#Game Over frozenset
game_over_text = font.render("GAME OVER", True, (255, 255, 255))

textX = 10
textY = 10

def show_score(textX, textY):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (textX, textY))

#Spawn Enemy Randomly
def enemy_random_spawn():
    enemyX = random.randint(0, 735)
    enemyY = random.randint(50, 150)
    return enemyX, enemyY


#Player Imageeeeeeee
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    x, y = enemy_random_spawn()
    enemyX.append(x)
    enemyY.append(y)
    enemyX_change.append(5)
    enemyY_change.append(25)

#Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 15
# Ready state - Bullet cannot be seen and is not moving
# Fire state - Bullet is currently moving
bullet_state = "ready"

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False

#Reset game
def reset_game():
    global playerX, playerY, bulletY, bullet_state, score_value
    bullet_state = "ready"
    playerX = 370
    playerY = 480
    score_value = 0
    bulletY = 480
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)



#Game Loop
running = True
game_over = False
while running:
    # RGB
    screen.fill((0, 0, 0))
    #Background Image
    screen.blit(background, (0, 0))

    #Event 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736;

    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            game_over = True
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                screen.blit(game_over_text, (300, 250))
                mixer.music.stop()
                game_over_sound = mixer.Sound('game_over.wav')
                game_over_sound.play()  


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        #Collision Detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i], enemyY[i] = enemy_random_spawn()
            score_value += 1

        enemy(enemyX[i], enemyY[i], i)


    #Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #Reset Bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if not game_over:
        playerX += playerX_change
        player(playerX, playerY)
        show_score(textX, textY)
    
    #Update the display
    pygame.display.update()

    if game_over:
        game_over = False
        pygame.time.wait(2000)
        reset_game()
        mixer.music.load('background.wav')
        mixer.music.play(-1)

