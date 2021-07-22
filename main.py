#Imports
import pygame, sys
from pygame.locals import *
import random, time
 
#Initializing 
pygame.init()
 
#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
LIVES = 3
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("GAME OVER :(", True, BLACK)
 #background image
background = pygame.image.load("background.png")
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((800,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("GO GO GO")

 #enemy sprite/rect
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.jpg")
        self.rect = self.image.get_rect(center = (random.randint(40,SCREEN_WIDTH-400)
                                                 , 0))
 #adds to score, speed, and reset
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 400), 0)

class Enemy2(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.jpg")
        self.rect = self.image.get_rect(center = (random.randint(400,SCREEN_WIDTH-40)
                                                 , 0))
      
      #adds to score, speed, and reset
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(400, SCREEN_WIDTH - 40), 0)
 
 #player sprite and location
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("download.jpg")
        self.rect = self.image.get_rect(center = (350, 520))
      #movement  
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-10, 0)
                  
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(10, 0)
                  
                   
#Setting up Sprites        
P1 = Player()
E1 = Enemy()
E2 = Enemy2()
invince = 60
 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)
 
#Adding speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.load('crab-rave.wav') 
pygame.mixer.music.play(-1)

#Game Loop
while True:
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #sets background and score
    DISPLAYSURF.blit(background, (-5,0))
    scores = font_small.render(str(f"YOUR SCORE: {SCORE}"), True, GREEN)
    DISPLAYSURF.blit(scores, (10,10))
    lives = font_small.render(str(f"LIVES LEFT: {LIVES}"), True, RED)
    DISPLAYSURF.blit(lives, (10,30))
 
    #Moves and Re-draws all Sprites
    for i, entity in enumerate(all_sprites):
        render = True
        if(i == 0 and invince > 0):
            render = invince%4 == 0 # if even, render, otherwise skip, gives blinky blinky
            
        if render: DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies) and invince == 0:
          if LIVES > 0:
              LIVES -= 1
              invince = 60

          else:
            time.sleep(1)
                        
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (50,250))
            DISPLAYSURF.blit(scores, (50, 400))
            pygame.display.update()
            for entity in all_sprites:
                    entity.kill() 
            time.sleep(2)
            pygame.quit()
            sys.exit()        
         
    if(invince > 0):
        invince -= 1

    pygame.display.update()
    FramePerSec.tick(FPS)