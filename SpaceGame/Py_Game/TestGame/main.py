import pygame
import os

pygame.init()

screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Explosion Test")

bg = (0,0,0)

def drawBackground():
    screen.fill(bg)

class SonicCharge(pygame.sprite.Sprite):
    def __init__(self,x,y, bornTime):
        super().__init__()

        self.images = []
        for num in range(0,7):
            image = pygame.transform.scale(pygame.image.load(os.path.join("Assets","SonicCharge",(f"SonicCharge{num}.png"))),(40+16*num,40+4*num))
            self.images.append(image)
        
        for num in range(7, 11):
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
        
        if self.counter >= explosion_speed and self.index < len(self.images) - 5:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [self.x,self.y]

        if self.index >= len(self.images) - 5 and self.counter >= explosion_speed:
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

   



SonicChargeGroup = pygame.sprite.Group()

run = True 
clock = pygame.time.Clock()

while run:
    clock.tick(60)
    drawBackground()

    SonicChargeGroup.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            sonic_charge = SonicCharge(pos[0], pos[1], pygame.time.get_ticks())
            SonicChargeGroup.add(sonic_charge)

    SonicChargeGroup.update()

    pygame.display.update()

pygame.quit()