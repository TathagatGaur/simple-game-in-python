import pygame
import os
pygame.font.init()

#the main game surface
width,hieght=900,500
WIN=pygame.display.set_mode((width,hieght))#display the main screen using display.set_mode(())
pygame.display.set_caption("Airship")

WHITE=(255,255,255)
BLACK=(0,0,0)

Health_font=pygame.font.SysFont('comicsans',40)
Winner_font=pygame.font.SysFont('comicsans',100)

BORDER=pygame.Rect(width//2-5,0,10,hieght)
FPS=60
vel=5
bullet_vel=7
max_bullets=2

yellow_hit=pygame.USEREVENT+1
red_hit=pygame.USEREVENT+2

red_bullets=[]
yellow_bullets=[]

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(45,50)),-90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(45,50)),90)

SPACE=pygame.image.load(os.path.join('Assets','space.png'))
space_background=pygame.transform.scale(SPACE,(width,hieght))

def draw_window(RED,YELLOW,red_bullets,yellow_bullets,yellow_health,red_health):
    WIN.fill(WHITE)#to fill the window with white colour
    WIN.blit(space_background,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    red_health_txt=Health_font.render("Health:"+str(red_health),1,WHITE)
    yellow_health_txt=Health_font.render("Health:"+str(yellow_health),1,WHITE)
    WIN.blit(yellow_health_txt,(width-yellow_health_txt.get_width()-10,10))
    WIN.blit(red_health_txt,(10,10))
             
    WIN.blit(YELLOW_SPACESHIP,(YELLOW.x,YELLOW.y))
    WIN.blit(RED_SPACESHIP,(RED.x,RED.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, (255,0,0), bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, (255,255,0), bullet)
    pygame.display.update()# to update the window display

def yellow_movement(keys_pressed,yellow):
        if keys_pressed[pygame.K_LEFT] and yellow.x-vel>BORDER.x+BORDER.width:
            yellow.x-=vel
        if keys_pressed[pygame.K_RIGHT] and yellow.x+vel+yellow.width< width:
            yellow.x+=vel
        if keys_pressed[pygame.K_UP] and yellow.x-vel>0:
            yellow.y-=vel
        if keys_pressed[pygame.K_DOWN] and yellow.y+vel+yellow.height< hieght-15:
            yellow.y+=vel

def red_movement(keys_pressed,red):
        if keys_pressed[pygame.K_a]and red.x-vel>0:
            red.x-=vel
        if keys_pressed[pygame.K_d]and red.x+vel+red.width< BORDER.x:
            red.x+=vel
        if keys_pressed[pygame.K_w]and red.y-vel>0:
            red.y-=vel
        if keys_pressed[pygame.K_s]and red.y+vel+red.height< hieght-15:
            red.y+=vel

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in red_bullets:
        bullet.x+=bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x > width:
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x-=bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x <0:
            yellow_bullets.remove(bullet)
            
def draw_winner_txt(text):
    draw_txt=Winner_font.render(text,1,WHITE)
    WIN.blit(draw_txt,(width//2-draw_txt.get_width()//2,hieght//2-draw_txt.get_width()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red=pygame.Rect(100,300,45,50)
    yellow=pygame.Rect(700,300,45,50)
    clock=pygame.time.Clock()

    red_health=10
    yellow_health=10
    
    # To check the event in the game
    run=True
    while run==True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:# To close the game 
                run=False
            #event for shooting bullets
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RCTRL and len(yellow_bullets) < max_bullets:
                    bullet=pygame.Rect(yellow.x,yellow.y+yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet)
                if event.key==pygame.K_LCTRL and len(red_bullets)<max_bullets:
                    bullet=pygame.Rect(red.x+red.width,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
            print(red_bullets,yellow_bullets)

            # to check the health of the players
            if event.type==red_hit:
                red_health-=1
            if event.type==yellow_hit:
                yellow_health-=1

        # to print the winner
        winner_txt=""
        if red_health<=0:
            winner_txt="Yellow Wins!"
        if yellow_health<=0:
            winner_txt="Red Win!"
        if winner_txt!="":
            draw_winner_txt(winner_txt)
            break
        
        keys_pressed=pygame.key.get_pressed()
        red_movement(keys_pressed,red)
        yellow_movement(keys_pressed,yellow)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        draw_window(red,yellow,red_bullets,yellow_bullets,yellow_health,red_health)
    pygame.quit()   
if __name__=='__main__':# to call the game
    main()
