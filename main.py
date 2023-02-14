import pygame
from sys import exit
from random import randint

def display_score(endScore):
    loser_score_text = loser_screen_score_font.render("Score: " + "{:.2f}".format(endScore), False, "black")
    loser_score_rect = loser_score_text.get_rect(midtop = (500, 30))
    screen.blit(loser_score_text, loser_score_rect)

def display_play_again():
    play_again_text = play_again_font.render("Press SPACE to play again!", False, "black")
    play_again_rect = play_again_text.get_rect(midbottom = (500, 550))
    screen.blit(play_again_text, play_again_rect)

def display_high_score(high_score):
    high_score_text = time_font.render("Your High Score is: " + "{:.2f}".format(high_score), False, "black")
    high_score_rect = high_score_text.get_rect(midtop = (500, 120))
    screen.blit(high_score_text, high_score_rect)

def get_score(score):
    time = pygame.time.get_ticks()
    score = time/1000
    return score


def enemy_movement(enemy_list):
    if enemy_list:
        for rect_list in enemy_list:
            if(rect_list.bottom == 400):
                rect_list.x -= 6
            if(rect_list.bottom != 400):
                rect_list.x -= 8

            if rect_list.bottom == 400:
                screen.blit(crab, rect_list)
            else:
                screen.blit(fly, rect_list)

        enemy_list = [enemy for enemy in enemy_list if enemy.x > -125]

        return enemy_list

    else : return []

def collision(player, enemy): #if the player and a enemy collide, game_active == False
    if enemy:
        for enemy_rect in enemy:
            if player.colliderect(enemy_rect):
                return False
    return True


pygame.init()
pygame.display.set_caption("Beach Jump Game")

screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock() #used for FPS
game_active = True

#images and rectangles
background = pygame.image.load("pics/Background.jpg").convert_alpha()
water = pygame.image.load("pics/Water.jpg").convert_alpha()
sky = pygame.image.load("pics/sky.png").convert_alpha()
logo = pygame.image.load("pics/beachjump.png").convert_alpha()
logo_rect = logo.get_rect(midbottom=(500, 390))

player_stand = pygame.image.load("pics/Player/player_stand.png").convert_alpha()
player_rect = player_stand.get_rect(midbottom = (120, 400))
player_gravity = 0

crab = pygame.image.load("pics/Crab/crab_walk_1.png").convert_alpha()

fly = pygame.image.load("Pics/fly/fly_1.png").convert_alpha()

enemy_rect_list = []

#text
font = pygame.font.Font("font/font.TTF", 50)
time_font = pygame.font.Font("font/font.TTF", 35)
loser_screen_score_font = pygame.font.Font("font/font.TTF", 60)
play_again_font = pygame.font.Font("font/Water Galon.ttf", 25)

#timer

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer,1500)

score = 0
roundTime = 0
high_score = 0

while True:
    score = get_score(score) - (roundTime/1000)
    score_text = font.render("Score: " + "{:.2f}".format(score), False, "white")#if this is declared outside the while loop score does not update
    score_text_rect = score_text.get_rect(center=(500, 120))

    for event in pygame.event.get(): #checks for player input
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.y == 290:
                   player_gravity = -25
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0

                #makes sure the clock resets each round
                roundTime = pygame.time.get_ticks()
                game_active = True

        if event.type == enemy_timer and game_active:
            if randint(0, 2):#if it's one a crab will spwan, else a fly will
                enemy_rect_list.append(crab.get_rect(bottomleft = (1024, 400)))
            else:
                enemy_rect_list.append(fly.get_rect(bottomleft = (1024, randint(200, 280))))

    if game_active:
        #displays images
        screen.blit(background,(0,400))
        screen.blit(water, (0,310))
        screen.blit(sky, (0,0))
        screen.blit(score_text, score_text_rect)

        #player values
        player_gravity += 1
        player_rect.y += player_gravity
        if (player_rect.y >= 290):
            player_rect.y = 290
        screen.blit(player_stand, player_rect)

        #enemy movement fucntion
        enemy_rect_list = enemy_movement(enemy_rect_list)


        #collisions
        game_active = collision(player_rect,enemy_rect_list)

        #gets the score when the game stops so I can display it on the end screen
        endScore = score

    else: #loser screen
        if endScore > high_score:
            high_score = endScore

        enemy_rect_list.clear()
        screen.fill("tan1")
        display_score(endScore)
        display_play_again()
        display_high_score(high_score)
        screen.blit(logo, logo_rect)

    pygame.display.update()
    clock.tick(60)
