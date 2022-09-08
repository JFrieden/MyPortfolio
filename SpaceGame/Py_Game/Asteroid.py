import pygame
import os
import random
#from pygame import sprite --for reference only

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, height=40, width=40, integrity=2):
        super().__init__()
        asteroidSelect = random.randint(1,3)
        self.image = pygame.transform.scale(
            pygame.image.load(
                os.path.join('Assets',('Asteroid%d.png' %(asteroidSelect)))
                )
                ,(width,height)
            )
        self.width = width
        self.height = height
        self.integrity = integrity
        self.rect = self.image.get_rect()
    
    def collide(self, damage = 1):
        self.integrity -= damage
    
       