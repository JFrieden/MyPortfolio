import pygame
import os
import map

pygame.mixer.init()

laserHitSound = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
leftPlayerMovementList = {"UP": pygame.K_w, "DOWN": pygame.K_s, "LEFT": pygame.K_a, "RIGHT": pygame.K_d}
rightPlayerMovementList = {"UP": pygame.K_i, "DOWN": pygame.K_k, "LEFT": pygame.K_j, "RIGHT": pygame.K_l}

yellowPlayerImage = pygame.transform.rotate(
                        pygame.transform.scale(
                            pygame.image.load(
                                os.path.join('Assets','spaceship_yellow.png')),
                        (55,40))
                    , 90)

redPlayerImage = pygame.transform.rotate(
                        pygame.transform.scale(
                            pygame.image.load(
                                os.path.join('Assets','spaceship_red.png')),
                        (55,40))
                    , 270)


class Player(pygame.sprite.Sprite):
    def __init__(self, LeftPlayer = True):
        super().__init__()
        if LeftPlayer:
            self.image = yellowPlayerImage
        else:
            self.image = redPlayerImage
        
        if LeftPlayer:
            self.movement = leftPlayerMovementList
        else:
            self.movement = rightPlayerMovementList
        
        self.rect = self.image.get_rect()

        if LeftPlayer:
            self.rect.x = round(map.X/4,None)
            self.rect.y = round(map.Y/2, None)
        else: 
            self.rect.x = round(3*map.X/4, None)
            self.rect.y = round(map.Y/2)

        self.width = 40
        self.height = 55
        self.VEL = 5
        self.health = 5
        self.LeftPlayer = LeftPlayer
        
        

    def handleMovement(self, keysPressed):
        if self.LeftPlayer: #Left player bounds (left edge and divider)
            if keysPressed[self.movement["LEFT"]] and self.rect.x > 0: #LEFT
                self.rect.x -= self.VEL
            if keysPressed[self.movement["RIGHT"]] and self.rect.x < map.X/2 -self.width - 2.5: #RIGHT
                self.rect.x += self.VEL
        else: #Right player bounds (right edge and divider)
            if keysPressed[self.movement["LEFT"]] and self.rect.x > map.X/2 + 2.5: #LEFT
                self.rect.x -= self.VEL
            if keysPressed[self.movement["RIGHT"]] and self.rect.x < map.X - self.width:
                self.rect.x += self.VEL

        if keysPressed[self.movement["UP"]] and self.rect.y > 0: #UP
            self.rect.y -= self.VEL
        if keysPressed[self.movement["DOWN"]] and self.rect.y < map.Y - self.height: #DOWN
            self.rect.y += self.VEL


    def collide(self, damage = 1):
        self.health -= damage
        laserHitSound.play()
    