import pygame
import os
import random
from pygame import draw
from pygame.locals import *
from Player import Player
import pygameGlobals as pg
from Asteroid import Asteroid
from SonicCharge import SonicCharge

pygame.font.init()
pygame.mixer.init()
pygame.init()

screenInfo = pygame.display.Info()
X = screenInfo.current_w
Y = screenInfo.current_h

WINDOW = pygame.display.set_mode((X, Y), FULLSCREEN)
pygame.display.set_caption("My First Game!")

laserFireSound = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(X/2 - 2.5, 0 , 5, Y)

HEALTHFONT = pygame.font.SysFont('comicsans', 40)
WINFONT = pygame.font.SysFont('comicsans', 100)


FPS = 60
ASTEROID_SECONDS_ON_SCREEN = 10
ASTEROID_SIZE = 40
ASTEROID_VEL = round(Y / (FPS * ASTEROID_SECONDS_ON_SCREEN), None)
VEL = 5
MAX_AMMO = 5
LASER_VEL = 7

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')).convert(), (X, Y))


def draw_window(yellowPlayer, redPlayer, redLasers, yellowLasers, asteroids, SonicCharges):
    WINDOW.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    redHealthText = HEALTHFONT.render("Health: " + str(redPlayer.health), 1, WHITE)
    yellowHealthText = HEALTHFONT.render("Health: "+str(yellowPlayer.health), 1, WHITE)
    WINDOW.blit(redHealthText, (X - redHealthText.get_width()-10, 10))
    WINDOW.blit(yellowHealthText,(10, 10))

    WINDOW.blit(yellowPlayer.image, (yellowPlayer.rect.x, yellowPlayer.rect.y))
    WINDOW.blit(redPlayer.image, (redPlayer.rect.x, redPlayer.rect.y))
    

    for laser in redLasers:
        pygame.draw.rect(WINDOW, RED, laser)
    
    for laser in yellowLasers:
        pygame.draw.rect(WINDOW, YELLOW, laser)

    for asteroid in asteroids:
      WINDOW.blit(asteroid.image, (asteroid.rect.x,asteroid.rect.y))

    for SonicCharge in SonicCharges:
        SonicCharge.update()
        WINDOW.blit(SonicCharge.image, (SonicCharge.rect.x,SonicCharge.rect.y))
      
    pygame.display.update()


def drawVictory(text):
    if "Red" in text:
        victoryText = WINFONT.render(text,1, RED)
    elif "Yellow" in text: 
        victoryText = WINFONT.render(text, 1, YELLOW)
    
    WINDOW.blit(BACKGROUND, (0,0))
    WINDOW.blit(victoryText, (X/2 - victoryText.get_width()/2, Y/2 - victoryText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def handleCollisions(redLasers, yellowLasers, asteroids, redPlayer, yellowPlayer):
    for laser in yellowLasers:
        laser.x += LASER_VEL
        if redPlayer.rect.colliderect(laser):
            redPlayer.collide()
            yellowLasers.remove(laser)
        if laser.x > X:
            yellowLasers.remove(laser)

    for laser in redLasers:
        laser.x -= LASER_VEL
        if yellowPlayer.rect.colliderect(laser):
            yellowPlayer.collide()
            redLasers.remove(laser)
        if laser.x + laser.width < 0:
            redLasers.remove(laser)

    for asteroid in asteroids:
        asteroid.rect.y += ASTEROID_VEL
        if yellowPlayer.rect.colliderect(asteroid.rect):
            yellowPlayer.collide()
            asteroid.collide(2)
            if asteroid.integrity  <= 0:
                asteroids.remove(asteroid)
        elif redPlayer.rect.colliderect(asteroid.rect):
            redPlayer.collide()
            asteroid.collide(2)
            if asteroid.integrity  <= 0:
                asteroids.remove(asteroid)
        elif asteroid.rect.y > Y:
            asteroids.remove(asteroid)
       
        for laser in redLasers:
            if asteroid.rect.colliderect(laser):
                redLasers.remove(laser)
                asteroid.collide()
                if asteroid.integrity  <= 0:
                    asteroids.remove(asteroid)
        for laser in yellowLasers:
            if asteroid.rect.colliderect(laser):
                yellowLasers.remove(laser)
                asteroid.collide()
                if asteroid.integrity  <= 0:
                    asteroids.remove(asteroid)
                
                

def makeAsteroids(asteroids, prevTime):
    if len(asteroids) > 6: 
        return prevTime;
    else:
        rand1to5 = random.randrange(2000, 20000,1000)
        if pygame.time.get_ticks() > prevTime + rand1to5:
            prevTime = pygame.time.get_ticks()
            if(prevTime % 10 == 1):
                asteroid = Asteroid(width = 80, height = 80, integrity = 4)
            elif(prevTime % 10 == 2):
                asteroid = Asteroid(width = 56, height = 56, integrity = 3)
            else:
                asteroid = Asteroid()
            asteroid.rect.x = random.randrange(-asteroid.width, X - asteroid.width, asteroid.width) #randRange() is lower bound exclusive
            asteroid.rect.y = -asteroid.height
            asteroids.append(asteroid)
        return prevTime;


def main():
    
    pygame.key.start_text_input()
    redPlayer = Player(LeftPlayer = False)
    yellowPlayer = Player()
    
    yellowLasers = []
    redLasers = []
    SonicCharges = []

    SonicCharge1 = SonicCharge(300,300,pygame.time.get_ticks())

    SonicCharges.append(SonicCharge1)

    asteroids = []
    asteroidTime = 0

    clk = pygame.time.Clock()

    victoryText = ""

    run = True
    while run:
        clk.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellowLasers) < MAX_AMMO:
                    laser = pygame.Rect(yellowPlayer.rect.x + yellowPlayer.width, yellowPlayer.rect.centery - 2.5, 10,5)
                    yellowLasers.append(laser)
                    laserFireSound.play()

                if event.key == pygame.K_RCTRL and len(redLasers) < MAX_AMMO:
                    laser = pygame.Rect(redPlayer.rect.x, redPlayer.rect.centery - 2.5, 10,5)
                    redLasers.append(laser)
                    laserFireSound.play()

                if event.key == pygame.K_ESCAPE:
                    WINDOW = pygame.display.set_mode((X-100, Y-100))
                
        if redPlayer.health <= 0:
            victoryText = "Yellow Wins!"
        if yellowPlayer.health <= 0:  
            victoryText = "Red Wins!"

        if victoryText != "":
            drawVictory(victoryText)
            pygame.key.stop_text_input()
            break

        keysPressed = pygame.key.get_pressed()
        yellowPlayer.handleMovement(keysPressed)
        redPlayer.handleMovement(keysPressed)

        asteroidTime = makeAsteroids(asteroids, asteroidTime)

        handleCollisions(redLasers, yellowLasers, asteroids, redPlayer, yellowPlayer)

        draw_window(yellowPlayer, redPlayer, redLasers, yellowLasers, asteroids, SonicCharges)
        
    if(run):
        main()

    pygame.quit()

if __name__ == "__main__":
    main()
