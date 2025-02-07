import pygame
import os
pygame.font.init()
pygame.mixer.init()

FPS=60
VEL=5   # velocity
BULLET_VEL=7 #BULLET VELOCTY
MAX_BULLETS=3
WIDTH,HEIGHT = 900 , 500 
SPACESHIP_HEIGHT,SPACESHIP_WIDTH=40,55


YELLOW_HIT=pygame.USEREVENT +1
RED_HIT=pygame.USEREVENT +2


WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("first game")


BORDER=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)# width/2 - 5 is because of width is 10

''' this sound is corrupted that is why this is not working
BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join('ASSECTS(pygame)','Assets_Greanade+1.mp3'))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join('ASSECTS(pygame)','Gun+Silencer.mp3'))
'''

HEALTH_FONT=pygame.font.SysFont('comicsans',40)
WINNER_FONT=pygame.font.SysFont('comicsans',100)
BLUE =(0,0,255)
WHITE=(255,255,255)
ROYAL_BLUE=(65,105,225)
FIRE_BRICK=(178,34,34)
BLACK=(0,0,0)
YELLOW_=(255,255,0)



YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join('ASSECTS(pygame)', 'spaceship_yellow.png'))
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(55,40)),90 )
RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join('ASSECTS(pygame)', 'spaceship_red.png'))
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(55,40)),270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('ASSECTS(pygame)', 'space.png')), (WIDTH, HEIGHT))

#SPACE=pygame.image.load(pygame.image.load(os.path.join('ASSECTS(pygame)','space.png')),(WIDTH,HEIGHT))

def draw_board(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
     WIN.blit(SPACE,(0,0))
     #WIN.fill(ROYAL_BLUE)
     pygame.draw.rect(WIN,BLACK,BORDER)# (A,B,C) a= on what are we drawing ,b=color,c=what are we drawing 
     
     red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
     yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
     WIN.blit(red_health_text,(WIDTH - red_health_text.get_width()-10,10))
     WIN.blit(yellow_health_text,(10,10))
     WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y))
     WIN.blit(RED_SPACESHIP,(red.x,red.y))
     
     
     for bullet in red_bullets:
       pygame.draw.rect(WIN,FIRE_BRICK,bullet)
     for bullet in yellow_bullets:
       pygame.draw.rect(WIN,YELLOW_,bullet)
     pygame.display.update()
     # this code pygame.display.update() is called without this the screen will not be updated 


def yellow_handel_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a]and yellow.x - VEL>0: #left
            yellow.x-=VEL
    if keys_pressed[pygame.K_d]and yellow.x + VEL + yellow.width < BORDER.x: #right
            yellow.x+=VEL
    if keys_pressed[pygame.K_w]and yellow.y - VEL > 0: #up
            yellow.y-=VEL
    if keys_pressed[pygame.K_s]and yellow.y + VEL + yellow.width < HEIGHT: #down# vaise to isme yellow.height ayega magar yellow.width se bhi kam ho gya
            yellow.y+=VEL

def red_handel_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT]and red.x - VEL >BORDER.x + BORDER.width: #left
            red.x-=VEL
    if keys_pressed[pygame.K_RIGHT]and red.x + VEL + red.width<WIDTH: #right
            red.x+=VEL
    if keys_pressed[pygame.K_UP]and red.y - VEL>0: #up
            red.y-=VEL
    if keys_pressed[pygame.K_DOWN]and red.y + VEL +red.width<HEIGHT: #down # vaise to isme red.height ayega magar rrd.width se bhi kam ho gya
            red.y+=VEL

 
def handel_bullets(yellow_bullets,red_bullets,yellow,red):
      for bullet in yellow_bullets:
            bullet.x+=BULLET_VEL
            if red.colliderect(bullet):
                  pygame.event.post(pygame.event.Event(RED_HIT))
                  yellow_bullets.remove(bullet)
            elif bullet.x>WIDTH:
                  yellow_bullets.remove(bullet)


      for bullet in red_bullets:
            bullet.x -=BULLET_VEL
            if yellow.colliderect(bullet):
                  pygame.event.post(pygame.event.Event(YELLOW_HIT))
                  red_bullets.remove(bullet)
            elif bullet.x<0:
                  red_bullets.remove(bullet)


def draw_winner(text):
      draw_text=WINNER_FONT.render(text,1,WHITE)
      WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2, HEIGHT/2 - draw_text.get_height()/2))
      pygame.display.update()
      pygame.time.delay(2000)



def main():
    red=pygame.Rect(700,300,SPACESHIP_HEIGHT,SPACESHIP_WIDTH)
    yellow=pygame.Rect(100,300,SPACESHIP_HEIGHT,SPACESHIP_WIDTH)
    
    
    red_bullets = []
    yellow_bullets =[]
    red_health=10
    yellow_health=10
    
    clock=pygame.time.Clock()
    run=True
    while run:
          clock.tick(FPS)
          for event in pygame.event.get():
               if event.type== pygame.QUIT:
                    run = False
                    pygame.quit()

               if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                     bullet=pygame.Rect( yellow.x+yellow.width , yellow.y+yellow.height//2-2 , 10 , 5)
                     yellow_bullets.append(bullet)   
                     #BULLET_FIRE_SOUND.PLAY()
                    
                    if event.key==pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:
                          bullet=pygame.Rect( red.x , red.y+red.height//2-2 , 10 , 5)
                          red_bullets.append(bullet)
                         # BULLET_FIRE_SOUND.PLAY()

               if event.type==RED_HIT:
                     red_health-=1
                    # BULLET_HIT_SOUND.PLAY()
               if event.type==YELLOW_HIT:
                     yellow_health-=1
                    # BULLET_HIT_SOUND.PLAY()
               winner_text=""      
          if red_health<=0:
                winner_text="YELLOW_WINS!"
          if yellow_health<=0:
                winner_text="RED_WINS!"

          if winner_text!="":
             draw_winner(winner_text)
             break


          keys_pressed=pygame.key.get_pressed()
          yellow_handel_movement(keys_pressed,yellow)
          red_handel_movement(keys_pressed,red)
          handel_bullets(yellow_bullets,red_bullets,yellow,red)

          
          
          
          
          draw_board(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health) # here this call the drawing function and fill the window with the color (you coded)
    #main()
#pygame.quit()


if __name__ =="__main__":
     main()
pygame.quit()   