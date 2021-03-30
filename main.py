import pygame
import os
pygame.font.init()
pygame.mixer.init()
import time
from pygame.locals import * 
import random
import json
import math


class Ship:
    def __init__(self,rect,color,shield,shield_enabled,back_shield,bottom_shield,top_shield):
        self.rect = rect
        self.color = color
        self.shield = shield
        self.shield_enabled = shield_enabled
        self.back_shield = back_shield
        self.bottom_shield = bottom_shield
        self.top_shield = top_shield

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carter's Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GAMEMUSIC = pygame.mixer.Sound('Assets/gamemusic.mp3')

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')



HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 70)

FPS = 60
VEL = 5
BULLET_VEL = 7
POWERUP_VEL = 1
OBSTACLE_VEL = 1
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 57, 40
POWERUP_WIDTH, POWERUP_HEIGHT = 46,45
BOMB_WIDTH, BOMB_HEIGHT = 80,40
SIDE_SHIELD_HEIGHT,SIDE_SHIELD_WIDTH = 45,7
FIRE_WIDTH, FIRE_HEIGHT = 80,50

BOUNCESHIELD = pygame.mixer.Sound('Assets/bounce_shield.mp3')
BOMB_ANN_AUDIO = pygame.mixer.Sound('Assets/bomb_announcement.mp3')
SHIELD_ANN_AUDIO = pygame.mixer.Sound('Assets/shield_announcement.mp3')


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_POWERUP = pygame.USEREVENT + 3
RED_POWERUP = pygame.USEREVENT + 4
YELLOW_HIT_BOMB = pygame.USEREVENT + 5
RED_HIT_BOMB = pygame.USEREVENT + 6
YELLOW_SHOT_BOMB = pygame.USEREVENT = 7
RED_SHOT_BOMB = pygame.USEREVENT + 8
YELLOW_HIT_FIRE = pygame.USEREVENT + 9
RED_HIT_FIRE = pygame.USEREVENT + 10

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

PLUSONEHEALTH_IMAGE = pygame.image.load(os.path.join('Assets', 'plusonehealth.png'))
PLUSONEHEALTH = pygame.transform.rotate(pygame.transform.scale(PLUSONEHEALTH_IMAGE,(POWERUP_WIDTH,POWERUP_HEIGHT)),0)
BOMB_IMAGE = pygame.image.load(os.path.join('Assets','bomb.png'))
BOMB = pygame.transform.rotate(pygame.transform.scale(BOMB_IMAGE,(BOMB_WIDTH,BOMB_HEIGHT)),0)

FIRE_IMG = pygame.image.load(os.path.join("Assets","fire.png"))
FIRE = pygame.transform.rotate(pygame.transform.scale(FIRE_IMG, (FIRE_WIDTH,FIRE_HEIGHT)),0)

BUZZER_AUDIO = pygame.mixer.Sound('Assets/buzzer.mp3')

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

YELLOW_INVISIBLE = False

FIRE_ANN = pygame.mixer.Sound('Assets/fire_ann.mp3')
FIRE_HIT = pygame.mixer.Sound('Assets/fire_hit.mp3')

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
DING_AUDIO = pygame.mixer.Sound('Assets/ding.mp3')
BOMB_AUDIO = pygame.mixer.Sound('Assets/explosion.mp3')
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
print("Pygame Init")





def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health,yellow_shield,redship,yellowship,powerups,yellow_shields,red_shields,bombs,obstacles):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)


    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    red_shields_text = HEALTH_FONT.render("Shields: " + str(red_shields),1,WHITE)
    yellow_shields_text = HEALTH_FONT.render("Shields: " + str(yellow_shields),1,WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_shields_text, (WIDTH - red_shields_text.get_width() -10,40))
    WIN.blit(yellow_shields_text, (10, 40))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for powerup in powerups:
        WIN.blit(PLUSONEHEALTH, (powerup.x,powerup.y))

    for bomb in bombs:
        WIN.blit(BOMB, (bomb.x,bomb.y))

    for obstacle in obstacles:
        WIN.blit(FIRE,(obstacle.x,obstacle.y))

    if yellowship.shield_enabled == True:
        pygame.draw.rect(WIN,YELLOW,pygame.Rect(yellowship.shield))
        pygame.draw.rect(WIN,YELLOW,pygame.Rect(yellowship.back_shield))
        pygame.draw.rect(WIN,YELLOW,pygame.Rect(yellowship.bottom_shield))
        pygame.draw.rect(WIN,YELLOW,pygame.Rect(yellowship.top_shield))

    if redship.shield_enabled == True:
        pygame.draw.rect(WIN,RED,pygame.Rect(redship.shield))
        pygame.draw.rect(WIN,RED,pygame.Rect(redship.back_shield))
        pygame.draw.rect(WIN,RED,pygame.Rect(redship.bottom_shield))
        pygame.draw.rect(WIN,RED,pygame.Rect(redship.top_shield))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)



    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL
    





def get_dpad_pressed(keys_pressed,yellow):

    for key in keys_pressed: 
        if key == "dpad_center":
            keys_pressed = []
            return True
        if key == "dpad_up" and yellow.y - VEL > 0:
            yellow.y -= VEL
        if key == "dpad_right" and yellow.x + VEL + yellow.width < BORDER.x:
            yellow.x += VEL
        if key == "dpad_left" and  yellow.x - VEL > 0:
            yellow.x -= VEL
        if key == "dpad_down" and yellow.y + VEL + yellow.height < HEIGHT - 15:
            yellow.y += VEL
    return False



def red_get_dpad_pressed(key_pressed,red):
    for key in key_pressed:
        if key == "dpad_center":
            keys_pressed = []
            return True
        if key == "dpad_up" and red.y - VEL > 0:
            red.y -= VEL
        if key == "dpad_right" and red.x + VEL + red.width < WIDTH:
            red.x += VEL
        if key == "dpad_left" and red.x - VEL > BORDER.x + BORDER.width:
            red.x -= VEL
        if key == "dpad_down" and red.y + VEL + red.height < HEIGHT - 15:
            red.y += VEL
    return False



def handle_bullets(yellow_bullets, red_bullets, yellow, red,redship,yellowship):
    
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if redship.shield_enabled and (redship.shield.colliderect(bullet) or redship.back_shield.colliderect(bullet) or redship.top_shield.colliderect(bullet) or redship.bottom_shield.colliderect(bullet)):
            BOUNCESHIELD.play()
            yellow_bullets.remove(bullet)
        elif red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellowship.shield_enabled and (yellowship.shield.colliderect(bullet) or yellowship.back_shield.colliderect(bullet) or yellowship.top_shield.colliderect(bullet) or yellowship.bottom_shield.colliderect(bullet)):
            BOUNCESHIELD.play()
            red_bullets.remove(bullet)
        elif yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)



def handle_powerups(powerups,yellowship,redship,red_health,yellow_health):
    for powerup in powerups:
        if yellowship.rect.colliderect(powerup):
            pygame.event.post(pygame.event.Event(YELLOW_POWERUP))

        if redship.rect.colliderect(powerup):
            pygame.event.post(pygame.event.Event(RED_POWERUP))


def handle_bombs(bombs,yellowship,redship,red_health,yellow_health):
    for bomb in  bombs:
        if yellowship.rect.colliderect(bomb):
            pygame.event.post(pygame.event.Event(YELLOW_HIT_BOMB))

        if redship.rect.colliderect(bomb):
            pygame.event.post(pygame.event.Event(RED_HIT_BOMB))

def handle_obstacles(obstacles,yellowship,redship,red_health,yellow_health):
    for obstacle in obstacles:
        if yellowship.rect.colliderect(obstacle):
            pygame.event.post(pygame.event.Event(YELLOW_HIT_FIRE))

        if redship.rect.colliderect(obstacle):
            pygame.event.post(pygame.event.Event(RED_HIT_FIRE))



def destroy_powerups(powerups,red_bullets,yellow_bullets):
    for powerup in powerups:
        for bullet in red_bullets:
            if powerup.colliderect(bullet):
                if powerup.colliderect(bullet):
                    if powerup.x >= BORDER.x:
                        pass
                    elif powerup.x <= BORDER.x:
                        powerups.pop()
                        BOMB_AUDIO.play()
        for bullet in yellow_bullets:
            if powerup.colliderect(bullet):
                if powerup.x <= BORDER.x:
                    pass
                elif powerup.x > BORDER.x:
                    powerups.pop()
                    BOMB_AUDIO.play()






def destroy_bombs(bombs,red_bullets,yellow_bullets,yellowship,redship):
    for bomb in bombs:
        for bullet in red_bullets:
            if bomb.colliderect(bullet):
                if bomb.x >= BORDER.x:
                    pass
                elif bomb.x <= BORDER.x:
                    distanceX = pygame.Vector2(yellowship.rect.center).distance_to(pygame.Vector2(bomb.x)) 
                    distanceY = pygame.Vector2(yellowship.rect.center).distance_to(pygame.Vector2(bomb.y)) 
                    if distanceX <= 175:
                        pygame.event.post(pygame.event.Event(RED_SHOT_BOMB))
                    elif distanceY <= 175:
                        pygame.event.post(pygame.event.Event(RED_SHOT_BOMB))
                    else:
                        pass
  


        for bullet in yellow_bullets:
            if bomb.colliderect(bullet):
                if bomb.x <= BORDER.x:
                    distanceX = pygame.Vector2(redship.rect.center).distance_to(pygame.Vector2(bomb.x)) 
                    pass
                elif bomb.x >= BORDER.x:
                    distanceX = pygame.Vector2(redship.rect.center).distance_to(pygame.Vector2(bomb.x)) 
                    distanceY = pygame.Vector2(redship.rect.center).distance_to(pygame.Vector2(bomb.y)) 
                    if distanceX <= 250:
                        pygame.event.post(pygame.event.Event(YELLOW_SHOT_BOMB))
                    elif distanceY <= 250:
                        pygame.event.post(pygame.event.Event(YELLOW_SHOT_BOMB))
                    else:
                        pass


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    red_bullets = []
    yellow_bullets = []
    pygame.time.delay(5000)
    print("Pygame Time Delay complete")
    red_joystick_id = 1
    yellow_joystick_id = 0
    joysticks_enabled = False





def main():
    

    print("Main Start ...")
    POWERUP_TIMER = FPS * 10
    BOMB_TIMER = FPS * 15
    OBSTACLE_TIMER = FPS * 12
    OBSTACLE_TIMEOUT = FPS * 8
    BOMB_TIMEOUT = FPS * 7
    POWERUP_TIMEOUT = FPS * 5
    GAMEMUSIC.play()
    pygame.event.clear()
    pygame.joystick.init()
    print("Pygame Joystick Init")
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    if len(joysticks) == 2:
        joysticks_enabled = True

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_shield = pygame.Rect(red.x+20,red.y,SPACESHIP_HEIGHT-30,SPACESHIP_WIDTH)
    red_back_shield = pygame.Rect(red.x+40,red.y-2,SPACESHIP_HEIGHT-30,SPACESHIP_WIDTH+2)
    red_bottom_shield = pygame.Rect(red.x-5,red.y+50,SIDE_SHIELD_HEIGHT,SIDE_SHIELD_WIDTH)
    red_top_shield = pygame.Rect(red.x-5,red.y-2,SIDE_SHIELD_HEIGHT,SIDE_SHIELD_WIDTH)
    redship = Ship(pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT),RED,red_shield,False,red_back_shield,red_bottom_shield,red_top_shield)

    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)    
    yellow_shield = pygame.Rect(yellow.x+40,yellow.y,SPACESHIP_HEIGHT-30,SPACESHIP_WIDTH)
    yellow_back_shield = pygame.Rect(yellow.x-15,yellow.y-2,SPACESHIP_HEIGHT-30,SPACESHIP_WIDTH+2)
    yellow_bottom_shield = pygame.Rect(yellow.x-5,yellow.y+50,SIDE_SHIELD_HEIGHT,SIDE_SHIELD_WIDTH)
    yellow_top_shield = pygame.Rect(yellow.x-5,yellow.y-2,SIDE_SHIELD_HEIGHT,SIDE_SHIELD_WIDTH)
    yellowship=Ship(pygame.Rect(100,300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT),YELLOW,yellow_shield,False,yellow_back_shield,yellow_bottom_shield,yellow_top_shield)



    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10
    yellow_shields = 5
    red_shields = 5

    joystick_keys = []
    red_joystick_keys = []
    powerups = []
    bombs = []
    obstacles = []
    POWERUP_TOGGLE = False
    BOMBS_TOGGLE = False
    OBSTACLE_TOGGLE = False
    clock = pygame.time.Clock()
    run = True
    yellowshieldcount = 0
    redshieldcount = 0
    while run:
        redship.shield = pygame.Rect(red.x-5,red.y,SPACESHIP_HEIGHT-30,SPACESHIP_WIDTH)
        yellowship.shield = pygame.Rect(yellow.x+40,yellow.y-2,SPACESHIP_HEIGHT-30,SPACESHIP_WIDTH+12)
        redship.back_shield = pygame.Rect(red.x+40,red.y-2,SPACESHIP_HEIGHT-30,SPACESHIP_WIDTH+2)
        redship.bottom_shield = pygame.Rect(red.x-5,red.y+50,SIDE_SHIELD_HEIGHT,SIDE_SHIELD_WIDTH)
        redship.top_shield = pygame.Rect(red.x-5,red.y-2,SIDE_SHIELD_HEIGHT,SIDE_SHIELD_WIDTH)
        yellowship.back_shield= pygame.Rect(yellow.x-15,yellow.y-2,SPACESHIP_HEIGHT-30,SPACESHIP_WIDTH+12)
        yellowship.bottom_shield = pygame.Rect(yellow.x-5,yellow.y+60,SIDE_SHIELD_HEIGHT,SIDE_SHIELD_WIDTH)
        yellowship.top_shield = pygame.Rect(yellow.x-5,yellow.y-2,SIDE_SHIELD_HEIGHT,SIDE_SHIELD_WIDTH)
        yellowship.rect = pygame.Rect(yellow)
        redship.rect = pygame.Rect(red)

        if len(powerups) == 0:
            if POWERUP_TIMER > 0:
                POWERUP_TIMER -= 1
            else:
                SHIELD_ANN_AUDIO.play()
                powerups.append(pygame.Rect(random.randint(100,800), random.randint(100,400),POWERUP_WIDTH,POWERUP_HEIGHT))
                POWERUP_TIMER = FPS * 10
                POWERUP_TOGGLE = not POWERUP_TOGGLE
        if len(bombs) == 0:
            if BOMB_TIMER > 0:
                BOMB_TIMER -=1
            else:
                BOMB_ANN_AUDIO.play()
                bombs.append(pygame.Rect(random.randint(100,800),random.randint(100,400),BOMB_WIDTH,BOMB_HEIGHT))
                BOMB_TIMER = FPS * 7
        if len(bombs) == 1:
            if BOMB_TIMEOUT > 0:
                BOMB_TIMEOUT -=1
            else:
                bombs.pop()
                BOMB_TIMEOUT = FPS * 7
        if len(powerups) == 1:
            if POWERUP_TIMEOUT > 0:
                POWERUP_TIMEOUT -=1
            else:
                powerups.pop()
                POWERUP_TIMEOUT = FPS * 10


        if len(powerups) == 1:
            if POWERUP_TOGGLE == False:
                powerups[0].x +=POWERUP_VEL*random.randint(0,3)
                powerups[0].y +=POWERUP_VEL*random.randint(0,3)                
            else:
                powerups[0].x -=POWERUP_VEL*random.randint(0,3)
                powerups[0].y -=POWERUP_VEL*random.randint(0,3)

        if len(bombs) == 1:
            if BOMBS_TOGGLE == False:
                bombs[0].x += POWERUP_VEL*random.randint(0,3)
                bombs[0].y += POWERUP_VEL*random.randint(0,3)
            else:
                bombs[0].x -= POWERUP_VEL*random.randint(0,3)
                bombs[0].y -= POWERUP_VEL*random.randint(0,3)

        if len(obstacles) == 0:
            if OBSTACLE_TIMER > 0:
                OBSTACLE_TIMER -=1
            else:
                FIRE_ANN.play()
                obstacles.append(pygame.Rect(random.randint(100,800),random.randint(100,400),FIRE_WIDTH,FIRE_HEIGHT))
                OBSTACLE_TIMER = FPS * 10

        if len(obstacles) == 1:
            if OBSTACLE_TIMEOUT > 0:
                OBSTACLE_TIMEOUT -=1
            else:
                obstacles.pop()
                OBSTACLE_TIMEOUT = FPS * 8
        if len(obstacles) == 1:
            if OBSTACLE_TOGGLE == False:
                obstacles[0].y += OBSTACLE_VEL*random.randint(0,3)
            else:
                obstacles[0].y -= OBSTACLE_VEL*random.randint(0,3)



        if yellowshieldcount < 1:
            yellowship.shield_enabled = False
        elif yellowshieldcount >= 1:
            yellowshieldcount -=1

        if redshieldcount < 1:
            redship.shield_enabled = False
        elif redshieldcount >= 1:
            redshieldcount -=1
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == JOYBUTTONDOWN:
                if event.joy == 0:
                    if event.button == 2:
                        bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2 -2,10,5)
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                    elif event.button == 0:
                        if yellow_shields <= 0:
                            BUZZER_AUDIO.play()
                        elif yellow_shields <= 5:
                            yellow_shields -=1
                            yellowship.shield_enabled = True
                            yellowshieldcount = 60
                elif event.joy == 1:
                    if event.button == 2:
                        bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                        print('add bullet')
                        red_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                    elif event.button == 0:
                        if red_shields <= 0:
                            BUZZER_AUDIO.play()
                        elif red_shields <= 5:
                            red_shields -=1
                            redship.shield_enabled = True
                            redshieldcount = 60                    
                    
            if event.type == JOYHATMOTION:
                if event.joy == 0:
                    if event.value == (0,1):
                        joystick_keys.append('dpad_up')
                    if event.value == (1,0):
                        joystick_keys.append('dpad_right')
                    if event.value == (0,0):
                        joystick_keys.append('dpad_center')
                    if event.value == (-1,0):
                        joystick_keys.append('dpad_left')
                    if event.value == (0,-1):
                        joystick_keys.append('dpad_down')
                elif event.joy == 1:
                    if event.value == (0,1):
                        red_joystick_keys.append('dpad_up')
                    if event.value == (1,0):
                        red_joystick_keys.append('dpad_right')
                    if event.value == (0,0):
                        red_joystick_keys.append('dpad_center')
                    if event.value == (-1,0):
                        red_joystick_keys.append('dpad_left')
                    if event.value == (0,-1):
                        red_joystick_keys.append('dpad_down')


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                     print("red bullets",len(red_bullets))
                     bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                     red_bullets.append(bullet)
                     BULLET_FIRE_SOUND.play()
                
                
                if event.key == pygame.K_q:
                    if yellow_shields <= 0:
                        BUZZER_AUDIO.play()
                    elif yellow_shields <= 5:
                        yellow_shields -=1
                        yellowship.shield_enabled = True
                        yellowshieldcount = 60

                if event.key == pygame.K_p:
                    if red_shields <= 0:
                        BUZZER_AUDIO.play()
                    elif red_shields <= 5:
                        red_shields -=1
                        redship.shield_enabled = True
                        redshieldcount = 60



            if event.type == RED_HIT:
                red_health -= 1
                if red.x + VEL + red.width < WIDTH:
                    red.x += VEL * 5
                BULLET_HIT_SOUND.play()


            if event.type == YELLOW_HIT:
                yellow_health -= 1
                if  yellow.x - VEL > 0:
                    yellow.x -= VEL * 5
 
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_POWERUP:
                yellow_health += 1
                DING_AUDIO.play()
                powerups.pop()

            if event.type == RED_POWERUP:
                red_health +=1
                DING_AUDIO.play()
                powerups.pop()

            if event.type == YELLOW_HIT_BOMB:
                yellow_health -=1
                BOMB_AUDIO.play()
                bombs.pop()

            if event.type == RED_HIT_BOMB:
                red_health -=1
                BOMB_AUDIO.play()
                bombs.pop()
            
            if event.type == RED_SHOT_BOMB:
                yellow_health -=2
                BOMB_AUDIO.play()
                bombs.pop()

            if event.type == YELLOW_SHOT_BOMB:
                red_health -=2
                BOMB_AUDIO.play()
                bombs.pop()

            if event.type == YELLOW_HIT_FIRE:
                yellow_health -= 1
                FIRE_HIT.play()
                obstacles.pop()

            if event.type == RED_HIT_FIRE:
                red_health -= 1
                FIRE_HIT.play()
                obstacles.pop()

        winner_text = ""
        if red_health <= 0:
            RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','explosion.png'))
            RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
            RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
            WIN.blit(RED_SPACESHIP, (red.x, red.y))
            with open("game_stats.json","r+") as f:
                data = json.load(f)
                numOfGames = data["Games Played: "]
                gamesPlayed = {"Games Played: ": numOfGames +1}
                data.update(gamesPlayed)
                f.seek(0)
                json.dump(data,f,indent=4)
                winner_text = "Yellow Wins! Games played: " + str(numOfGames)
                red_bullets = []
                yellow_bullets = []



        if yellow_health <= 0:
            YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','explosion.png'))
            YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
            YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
            WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
            with open("game_stats.json","r+") as f:
                data = json.load(f)
                numOfGames = data["Games Played: "]
                gamesPlayed = {"Games Played: ": numOfGames +1}
                data.update(gamesPlayed)
                f.seek(0)
                json.dump(data,f,indent=4)
                winner_text = "Red Wins! " + "Games played: " + str(numOfGames) 
                red_bullets = []
                yellow_bullets = []


        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        if (get_dpad_pressed(joystick_keys,yellow)) == True:
            print("Resetting yellow dpad")
            joystick_keys = []
        if (red_get_dpad_pressed(red_joystick_keys,red)) == True:
            red_joystick_keys = []
            print("Resetting red dpad")
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red,redship,yellowship)
        handle_powerups(powerups,yellowship,redship,red_health,yellow_health)
        handle_bombs(bombs,yellowship,redship,red_health,yellow_health)
        destroy_powerups(powerups,red_bullets,yellow_bullets)
        destroy_bombs(bombs,red_bullets,yellow_bullets,yellowship,redship)
        handle_obstacles(obstacles,yellowship,redship,red_health,yellow_health)


        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health,yellow_shield,redship,yellowship,powerups,yellow_shields,red_shields,bombs,obstacles)
        
    main()


if __name__ == "__main__":
    main()