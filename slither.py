# Author: Javi Barranco
# Name: Slither Game

import sys
import os
import time
import random
import pygame

pygame.init()

# Display control:
displayWidth = 500
displayHeight = 500

gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Slither Game')

icon_path = os.path.join("assets","icon.png")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

# Sprite control:
img1_path = os.path.join("assets", "SnakeHead.png")
img2_path = os.path.join("assets", "Apple.png")
img1 = pygame.image.load(img1_path)
img2 = pygame.image.load(img2_path)

# Colors:
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# Frames control:
clock = pygame.time.Clock()
FPS = 20

# Font control:
smallfont = pygame.font.SysFont("comicsansms", 20)
mediumfont = pygame.font.SysFont("comicsansms", 40)
largefont = pygame.font.SysFont("comicsansms", 65)


def snake(block_size, snakeList, direction):
    # We paint green blocks for all the snake except the first block.
    # For the first block we blit the img1.
    if direction == "right":
        head = pygame.transform.rotate(img1, 270)
    if direction == "left":
        head = pygame.transform.rotate(img1, 90)
    if direction == "up":
        head = img1
    if direction == "down":
        head = pygame.transform.rotate(img1, 180)
    gameDisplay.blit(head,(snakeList[-1][0], snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])

def randAppleGen(AppleSize):
    randAppleX = random.randrange(0,displayWidth-AppleSize)
    randAppleY = random.randrange(0,displayHeight-AppleSize)
    return randAppleX, randAppleY

def pause():
    # Flags:
    paused = True
    message_to_screen("Paused", red, -50, "large")
    message_to_screen("Press Enter to continue or q to quit", white, 20, "medium")
    pygame.display.update()

    while paused == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    os._exit(0)

def score(score):
    text = mediumfont.render("Score: "+str(score), True, white)
    gameDisplay.blit(text, [0,0])

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = mediumfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen (msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (displayWidth/2),(displayHeight/2)+y_displace
    gameDisplay.blit(textSurf,textRect)

def game_intro():
    # Flags:
    intro = True

    while intro == True:
        gameDisplay.fill(black)
        message_to_screen("Welcome to Slither", green, y_displace=-50, size="large")
        message_to_screen("Press 'Enter' to start", (50,255,50),20,size="medium")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                    pygame.quit()
                    quit()
                    os._exit(0)

def gameLoop():
    # Flags:
    gameExit = False
    gameOver = False

    # Snake values:
    lead_x = displayWidth/2
    lead_y = displayHeight/2
    snakeList = []
    snakeLenght = 1
    block_size = 20
    mvm_speed = block_size
    lead_x_change = mvm_speed
    lead_y_change = 0
    direction = "right"

    # Apple values:
    AppleSize = block_size
    randAppleX, randAppleY = randAppleGen(AppleSize)

    # Loops:
    # GameExit Loop:
    while gameExit == False:
        # GameOver Loop:
        if gameOver == True:
            gameDisplay.fill(black)
            message_to_screen("GAME OVER", green, y_displace=-50, size="large")
            message_to_screen("Final Score: " + str(snakeLenght-1),green, y_displace=20,size="medium")
            message_to_screen("Press Enter to play or q to quit", white, y_displace=75, size="small")
            pygame.display.update()
        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                        os._exit(0)
                    if event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True
                    if event.key == pygame.K_RETURN:
                        gameLoop()

        for event in pygame.event.get():
            #print(event) # Uncomment to get event logs.
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                os._exit(0)
            # Check movement:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -mvm_speed
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = mvm_speed
                    lead_y_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = mvm_speed
                    lead_x_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -mvm_speed
                    lead_x_change = 0
                elif event.key == pygame.K_ESCAPE:
                    pause()
        # Logic:
        # Check collision with borders:
        if lead_x >= displayWidth or lead_x < 0 or lead_y >= displayHeight or lead_y < 0:
            gameOver = True
        # Check collision with snake body:
        for XnY in snakeList[:-1]:
            if XnY == snakeHead:
                gameOver = True
        # Check Snake-Apple collision:
        if lead_x >= randAppleX and lead_x < randAppleX+AppleSize or lead_x+block_size >= randAppleX and lead_x+block_size < randAppleX+AppleSize:
            if lead_y >= randAppleY and lead_y < randAppleY+AppleSize:
                randAppleX, randAppleY = randAppleGen(AppleSize)
                snakeLenght += 1
            elif lead_y+block_size >= randAppleY and lead_y+block_size < randAppleY+AppleSize:
                randAppleX, randAppleY = randAppleGen(AppleSize)
                snakeLenght += 1
        # Add movement:
        lead_x += lead_x_change
        lead_y += lead_y_change
        # Update Frame:
        gameDisplay.fill(black)
        # Update the snake:
        # Each frame we add the current head position to the end of the array.
        # If you dont eat an apple, we delete the first element of the array. This
        # way we create an illusion of the snake moving. If you eat an apple, the
        # snake size increases meaning no elements are deleted and the snake grows.
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeLenght:
            del snakeList[0]
        snake(block_size, snakeList, direction)
        # Update apple
        gameDisplay.blit(img2,(randAppleX,randAppleY))
        # Update Score:
        score(snakeLenght-1)
        # Render the frame:
        pygame.display.update()
        # Sets the amount of frames per second
        clock.tick(FPS)

game_intro()
