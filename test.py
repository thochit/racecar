import time
import pygame
import random

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Race car')

clock = pygame.time.Clock()
BLACK = (0,0,0)
WHITE = (255,255,255)

RED = (200,0,0)
GREEN = (0,200,0)
BLUE = (0,0,255)

BRIGHT_GREEN = (0,255,0)
BRIGHT_RED = (255,0,0)

car_width = 73

crash_sound = pygame.mixer.Sound('crash_sound.mp3')
pygame.mixer.music.load('playing.mp3')

racecar = pygame.image.load('racecar.png')
gameIcon = pygame.image.load('carIcon.png')

pygame.display.set_icon(gameIcon)

def quitgame():
    pygame.quit()
    quit()

def show_image(x, y):
    gameDisplay.blit(racecar, (x, y))

def thing_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('DODGE:' + str(count), True, BLACK)
    gameDisplay.blit(text, (0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def text_object(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

Pause = True

def crash():

    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    Crash = True

    while Crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_object('YOU CRASHED', largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button('REPLAY', 150, 450, 100, 50, GREEN, BRIGHT_GREEN, 20, game_loop)

        button('QUIT', 550, 450, 100, 50, RED, BRIGHT_RED, 20, quitgame)

        pygame.display.update()
        clock.tick(30)

def button(msg, x, y, w, h, ic, ac, size, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

    smallText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_object(msg, smallText)
    TextRect.center = (x + w/2, y + h/2)
    gameDisplay.blit(TextSurf, TextRect)

def unpause():
    global Pause
    pygame.mixer.music.unpause()
    Pause = False

def pause():

    pygame.mixer.music.pause()

    while Pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        gameDisplay.fill(WHITE)
        largeText = pygame.font.Font('freesansbold.ttf', 100)
        TextSurf, TextRect = text_object('PAUSE', largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button('CONTINUE', 150, 450, 100, 50, GREEN, BRIGHT_GREEN, 20, unpause)

        button('QUIT', 550, 450, 100, 50, RED, BRIGHT_RED, 20, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        gameDisplay.fill(WHITE)
        largeText = pygame.font.Font('freesansbold.ttf', 100)
        TextSurf, TextRect = text_object('A BIT RACEY', largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button('GO!', 150, 450, 100, 50, GREEN, BRIGHT_GREEN, 20, game_loop)

        button('QUIT', 550, 450, 100, 50, RED, BRIGHT_RED, 20, quitgame)

        pygame.display.update()
        clock.tick(30)

def game_loop():
    global Pause

    pygame.mixer.music.load('playing.mp3')
    pygame.mixer.music.play(-1)

    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0
    y_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    thingCount = 1
    dodged = 0

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            ############################
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -20
                elif event.key == pygame.K_RIGHT:
                    x_change = 20

                if event.key == pygame.K_p:
                    Pause = True
                    pause()
                # if event.key == pygame.K_UP:
                #     y_change = -5
                # elif event.key == pygame.K_DOWN:
                #     y_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            ######################
        ##
        if 0 < x + x_change and x + x_change + car_width < display_width:
            x += x_change
        ##
        gameDisplay.fill(WHITE)

        things(thing_startx, thing_starty, thing_width, thing_height, BLACK)
        thing_starty += thing_speed

        show_image(x, y)

        thing_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

            ####
        if y < thing_starty + thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                print('x crossover')
                crash()
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
quitgame()


