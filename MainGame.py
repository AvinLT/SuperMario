import pygame, sys
from pygame.locals import * #import modules
clock = pygame.time.Clock() #initialize clock

pygame.init() #initialize pygame

WINDOW_SIZE = (500,500) #window size
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initialize window


playerPos = [250,350] #position of main character
#playerImage = pygame.image.load("sprites\marioset\stand.png")
picture = pygame.image.load("sprites\marioset\stand.png")
picture = pygame.transform.scale(picture, (64, 64))
playersize = picture.get_height()

#pygame.draw.rect(screen,(255,255,255),(0,450,500,10))

jumpPower = 10
jumpCount = 10
jumping = False
while True: #Main game loop

    screen.fill((0,0,0))

    for event in pygame.event.get(): #event loop
        if event.type == QUIT: # checks if window is closed
            pygame.quit() #stops pygame
            sys.exit() # stops script



    keys = pygame.key.get_pressed()
    if keys[K_d]:
        playerPos[0] += 2
    if keys[K_a]:
        playerPos[0] -= 2

    if not(jumping):
        if keys[K_w]:
            jumping = True
    else:
        if jumpPower > -10 and playerPos[1] < WINDOW_SIZE[1]-playersize:
            neg = 1
            if jumpCount < 0:
                neg = -1
            playerPos[1] -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            jumping = False
            jumpCount = jumpPower











    screen.blit(picture,playerPos)

    pygame.display.update() # update display
    clock.tick(60) # set frame rate