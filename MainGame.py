import pygame, sys
from pygame.locals import * #import modules
clock = pygame.time.Clock() #initialize clock

pygame.init() #initialize pygame

WINDOW_SIZE = (500,500) #window size
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initialize window


playerPos = [250,500 - 64 - 10] #position of main character

playerImage = pygame.transform.scale(pygame.image.load("sprites\marioset\stand.png"), (64, 64)) # standing sprite

runImages = [
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1right.png"), (64, 64)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (64, 64)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3right.png"), (64, 64)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (64, 64)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1left.png"), (64, 64)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (64, 64)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3left.png"), (64, 64)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (64, 64))
] # the sprites for runnning

playerRunCount = 999 # 999 signifies that player is not moving. if moving will be between 0 and 7
runImagesDelay = 9 # how slow you want transitions from each running sprite
tempCount = 0

playersize = playerImage.get_height()

#pygame.draw.rect(screen,(255,255,255),(0,450,500,10))

"""jumpPower = 10
jumpCount = 10"""

jumping = False
velY = 10 # acts as velocity

while True: #Main game loop

    screen.fill((255,255,255)) # makes screen white

    for event in pygame.event.get(): #event loop
        if event.type == QUIT: # checks if window is closed
            pygame.quit() #stops pygame
            sys.exit() # stops script

        """if event.type == KEYUP:
            if event.key == K_w:
                playerRunCount = 999"""



    keys = pygame.key.get_pressed()
    
    if keys[K_d]: # when d is pressed, moves right
        playerPos[0] += 2

        tempCount = (tempCount +1)  % runImagesDelay # only transitions to next sprite when tempCount is 0.
        if tempCount==0:
            playerRunCount += 1
            playerRunCount = playerRunCount % 4 # loops between 0 and 3, which have correspondin sprites in runImages list.

    elif keys[K_a]:
        playerPos[0] -= 2

        tempCount = (tempCount + 1) % runImagesDelay # only transitions to next sprite when tempCount is 0.
        if tempCount == 0:
            playerRunCount += 1
            playerRunCount = (playerRunCount % 4) + 4 # loops between 4 and 7, which have correspondin sprites in runImages list.

    else:
        playerRunCount = 999 # signifies player is standing


    if keys[K_w]:
        jumping = True

    """if not(jumping):
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
            jumpCount = jumpPower"""



    if playerPos[1] <= WINDOW_SIZE[1] - playersize + velY and jumping == True: # is player above ground and jumping
        playerPos[1] -= velY 
        velY -= 0.5 # velY = 0 when at top of jump.
    else:
        jumping = False
        velY = 10 # set to 10 so that the start of next jump will start at fastest speed.









    if playerRunCount == 999: # if standing
        screen.blit(playerImage,playerPos)
    else: # if running
        screen.blit(runImages[playerRunCount],playerPos)


    pygame.display.update() # update display
    clock.tick(60) # set frame rate