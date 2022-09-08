import pygame
import os

expansionFrames = 7
dissipationFrames = 3

class SonicCharge(pygame.sprite.Sprite):
    def __init__(self,x,y, bornTime):
        super().__init__()

        self.images = []
        for num in range(0,expansionFrames):
            image = pygame.transform.scale(pygame.image.load(os.path.join("Assets","SonicCharge",(f"SonicCharge{num}.png"))),(40+16*num,40+4*num))
            self.images.append(image)
        
        for num in range(expansionFrames, expansionFrames+dissipationFrames):
            image = pygame.transform.scale(pygame.image.load(os.path.join("Assets","SonicCharge",(f"SonicCharge{num}.png"))),((40+16*num -12*num),(40+4*num-3*num-12)))
            self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.x = x 
        self.y = y
        self.bornTime = bornTime
        self.counter = 0
    
    def update(self):
        explosion_speed = 8
        self.counter += 1
        
        if self.counter >= explosion_speed and self.index < len(self.images) - dissipationFrames - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [self.x,self.y]

        if self.index >= len(self.images) - dissipationFrames - 1 and self.counter >= explosion_speed:
            if pygame.time.get_ticks() > 2000 + self.bornTime and self.index < len(self.images) - 1:
                self.counter = 0
                self.index += 1
                self.image = self.images[self.index]
                self.rect = self.image.get_rect()
                self.rect.center = [self.x,self.y]
            
            if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
                    self.kill()
            else:
                return None
