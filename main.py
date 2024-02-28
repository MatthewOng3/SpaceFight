from cmath import inf
import pygame
import os
import random
import sys

pygame.font.init() #initialise pygame font library 
pygame.mixer.init() #initlaise sound library for pygame

WIDTH,HEIGHT = 900,500  #define dimensions of the game
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT)) #make a new window of this dimensions
pygame.display.set_caption("Space Duel!") #Set window name at the top

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

Ammo_increase = 45
Spd_increase = 6

FPS = 60 #define how many frames for the game to update at
DISTANCE = 5
BORDER = pygame.Rect(WIDTH//2 - 5,0, 10, HEIGHT) #dimensions of border

ship_width,ship_height = 55,40
power_width,power_height = 20,30
health_font = pygame.font.SysFont('arial',30) #Size of health display
winner_font = pygame.font.SysFont('arial',90) 

#sounds
bullet_hit = pygame.mixer.Sound(os.path.join(r'C:\Users\matth\OneDrive\Desktop\PersonalProjects\SpaceFight\Assets','Bullet_Impact_Metal_Hard_Clang.mp3')) 
bullet_fire = pygame.mixer.Sound(os.path.join(r'C:\Users\matth\OneDrive\Desktop\PersonalProjects\SpaceFight\Assets','Gun+Silencer.mp3'))


Yellow_hit = pygame.USEREVENT + 1 #represent number for a custom user event , Event ID essentially
Red_hit = pygame.USEREVENT + 2
Power = pygame.USEREVENT + 3
Red_Depower = pygame.USEREVENT + 4
Yellow_Depower = pygame.USEREVENT + 5

#Load images(surfaces)
yellow_ship_image = pygame.image.load(os.path.join(r'C:\Users\matth\OneDrive\Desktop\PersonalProjects\SpaceFight\Assets','spaceship_yellow.png'))
red_ship_image = pygame.image.load(os.path.join(r'C:\Users\matth\OneDrive\Desktop\PersonalProjects\SpaceFight\Assets', 'spaceship_red.png'))
background = pygame.transform.scale(pygame.image.load(os.path.join(r'C:\Users\matth\OneDrive\Desktop\PersonalProjects\SpaceFight\Assets','space.png')),(WIDTH,HEIGHT))
bolt = pygame.image.load(os.path.join(r'C:\Users\matth\OneDrive\Desktop\PersonalProjects\SpaceFight\Assets', 'bolt.png'))

#resize and rotate image
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_ship_image,(ship_width,ship_height)),90)
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_ship_image,(ship_width,ship_height)),270)
bullet_power = pygame.transform.scale(bolt,(power_width,power_height))

def display(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,spawn,power_up):
    #WIN.fill(WHITE) #fill the screen before drawing any image on it
    WINDOW.blit(background,(0,0))
    pygame.draw.rect(WINDOW, BLACK, BORDER) #draw rectangle on the window

    red_health_text = health_font.render("Health: " + str(red_health),1,WHITE) #always put 1 as a minimal argument
    yellow_health_text = health_font.render("Health: " + str(yellow_health),1,WHITE)

    WINDOW.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,5))
    WINDOW.blit(yellow_health_text,(10,5))
    WINDOW.blit(yellow_spaceship,(yellow.x,yellow.y)) #use blit to put any images on the screen, (0,0) is top left, refer to width, height variables
    WINDOW.blit(red_spaceship,(red.x,red.y))
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW,YELLOW,bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW,RED,bullet)
        

    if spawn == 1:
        WINDOW.blit(bullet_power,(power_up.x,power_up.y))
        
    pygame.display.update() #need to update display in order to show any changes made

def movement_yellow(pressed_keys,yellow):
    if pressed_keys[pygame.K_w] and yellow.y - DISTANCE > 0: 
        yellow.y -= DISTANCE
    if pressed_keys[pygame.K_a] and yellow.x - DISTANCE > 0: 
        yellow.x -= DISTANCE
    if pressed_keys[pygame.K_s] and yellow.y + DISTANCE + yellow.height < HEIGHT - 15: 
        yellow.y += DISTANCE
    if pressed_keys[pygame.K_d] and yellow.x + DISTANCE + yellow.width < BORDER.x: 
        yellow.x += DISTANCE

def movement_red(pressed_keys,red):
    if pressed_keys[pygame.K_UP] and red.y - DISTANCE > 0:
        red.y -= DISTANCE
    if pressed_keys[pygame.K_LEFT] and red.x - DISTANCE > BORDER.x + BORDER.width: 
        red.x -= DISTANCE
    if pressed_keys[pygame.K_DOWN] and red.y + DISTANCE + red.height < HEIGHT - 15: 
        red.y += DISTANCE
    if pressed_keys[pygame.K_RIGHT] and red.x + DISTANCE + red.width < WIDTH: 
        red.x += DISTANCE

def bullet_interaction(RED_BULLET_SPD, YELLOW_BULLET_SPD, yellow_bullet,red_bullet,yellow,red):
    for bullet in yellow_bullet:
        bullet.x += YELLOW_BULLET_SPD
        if red.colliderect(bullet): #check if both recs touch each other(only works with rects)
            pygame.event.post(pygame.event.Event(Red_hit))  #making a new event saying red player was hit
            yellow_bullet.remove(bullet)  
        elif bullet.x > WIDTH: #remove bullets if it goes outside the screen
            yellow_bullet.remove(bullet)
    
    for bullet in red_bullet:
        bullet.x -= RED_BULLET_SPD
        if yellow.colliderect(bullet): #check if both recs touch each other(only works with rects)
            pygame.event.post(pygame.event.Event(Yellow_hit))  #making a new event saying red player was hit adding it to event queue
            red_bullet.remove(bullet)  
        elif bullet.x < 0:
            red_bullet.remove(bullet)

def pow(indicator,spawn):
    num = random.randint(1,500)
    
    if num == indicator and spawn == 0: #to check if the random numbers match thus changing spawn variable to 1 which spawns the power up
        spawn = 1

    if spawn == 1:
        pygame.event.post(pygame.event.Event(Power)) #adds this event to the main function


def getcoord():
    
   
    red_1 = random.randint(40,350)
    red_2 = random.randint(550,840)
    pow_x = random.choice([red_1,red_2])
    pow_y = random.randint(50,450)

    return pow_x,pow_y

def output_winner(winner):
    output_text = winner_font.render(winner,1,WHITE) #render text
    WINDOW.blit(output_text,(WIDTH/2 - output_text.get_width()/2,HEIGHT/2 - output_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    RED_AMMO = 4
    YELLOW_AMMO = 4
    RED_BULLET_SPD = 9
    YELLOW_BULLET_SPD = 9
    pow_x,pow_y = 0,0
    inf_ammo = 0
    yellow = pygame.Rect(100,300,ship_width,ship_height) #define x and y coordinate,representing as rectangles
    red = pygame.Rect(700,300,ship_width,ship_height)
    
    yellow_bullet = []
    red_bullet = []

    yellow_health = 5
    red_health = 5
    spawn = 0
    check = 0
    check_1 = 0
    timer = 0
    clock = pygame.time.Clock() #for fps
    game = True
    while game == True:
        clock.tick(FPS) #run while loop 60 fps
        for event in pygame.event.get(): #for every main function , to call for events, essentially a queue of events
            if event.type == pygame.QUIT: #if quit event occurs, quit game
                game = False
                pygame.quit() #quit the game
                sys.exit(0)

            if event.type == pygame.KEYDOWN:  #check if a key is pressed down
                if event.key == pygame.K_SPACE and len(yellow_bullet) < RED_AMMO: #if key pressed down is space and len of the ammo array is lower than cap
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2,10,5)
                    yellow_bullet.append(bullet)
                    bullet_fire.play()
                if event.key == pygame.K_RCTRL and len(red_bullet) < YELLOW_AMMO:
                    bullet = pygame.Rect(red.x, red.y + red.height//2,10,5)
                    red_bullet.append(bullet)
                    bullet_fire.play()
            if event.type == Power :
                spawn = 1
                try:
                    if red.colliderect(inf_ammo):
                        spawn = 0
                        check = 0 
                        RED_AMMO += Ammo_increase
                        RED_BULLET_SPD += Spd_increase
                        check_1 = 1
                    elif yellow.colliderect(inf_ammo):
                        spawn = 0
                        check = 0
                        YELLOW_AMMO += Ammo_increase
                        YELLOW_BULLET_SPD += Spd_increase
                        check_1 = 2
                except:
                    pass
            if event.type == Red_hit:
                red_health -= 1
                bullet_hit.play() #play sound
            if event.type == Yellow_hit:
                yellow_health -= 1
                bullet_hit.play()
        winner = ""
        if yellow_health <= 0:
            winner = "Yellow Wins!"
        if red_health <= 0:
            winner = "Red Wins!"
        if winner != "":
            output_winner(winner)
            break

        if check_1 == 1:
            timer += 1
            if timer == 1000:
                check_1 = 0
                timer = 0
                RED_AMMO -= Ammo_increase
                RED_BULLET_SPD -= Spd_increase
        elif check_1 == 2:
            timer += 1
            if timer == 1000:
                check_1 = 0
                timer = 0
                YELLOW_AMMO -= Ammo_increase 
                YELLOW_BULLET_SPD -= Spd_increase

        indicator = random.randint(1,500)
        pressed_keys = pygame.key.get_pressed() #tells us what keys are currently being pressed down
        movement_yellow(pressed_keys,yellow) 
        movement_red(pressed_keys,red)
        bullet_interaction(RED_BULLET_SPD,YELLOW_BULLET_SPD,yellow_bullet,red_bullet,yellow,red)
        pow(indicator,spawn)


        if spawn == 1 and check == 0: # if statements to let the code know a power up has already been spawned
            pow_x,pow_y = getcoord()
            check = 1
            inf_ammo = pygame.Rect(pow_x,pow_y,power_width,power_height) 
        elif check == 1:
            inf_ammo = pygame.Rect(pow_x,pow_y,power_width,power_height) #so the info_ammo value stays the same after checking if a power up spawned
        else:
            inf_ammo = None

        
        
        display(red,yellow,red_bullet,yellow_bullet,red_health,yellow_health,spawn,inf_ammo) 
       
    
    main()

if __name__ == "__main__":  

    main()