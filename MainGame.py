import pygame, sys
from pygame.locals import * #import modules
clock = pygame.time.Clock() #initialize clock

pygame.init() #initialize pygame

WINDOW_SIZE = (600,400) #window size

display = pygame.Surface((300,192))


screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initialize window

playerSize = 28
playerImage = pygame.transform.scale(pygame.image.load("sprites\marioset\stand.png"), (playerSize, playerSize)) # standing sprite

runImages = [
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1right.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3right.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1left.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3left.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (playerSize, playerSize))
] # the sprites for runnning

blockSize = 16
groundBlock = pygame.transform.scale(pygame.image.load(r"sprites\blocks\groundBlock.png"), (blockSize, blockSize))
brick = pygame.transform.scale(pygame.image.load(r"sprites\blocks\brick.png"), (blockSize, blockSize))


#playerImage.set_colorkey((255,255,255))
"""for image in range(len(runImages)):
    image.set_colorkey((255,255,255))"""



playersize = playerImage.get_height()


playerPos = [100,144-28] #position of main character

playerRunCount = 999 # 999 signifies that player is not moving. if moving will be between 0 and 7
runImagesDelay = 9 # how slow you want transitions from each running sprite
tempCount = 0



gameMap = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,2,2,2,2,2,2,2,2,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

jumping = False
velY = 10 # acts as velocity

while True: #Main game loop

    display.fill((255,255,255)) # makes screen white

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

    tile_rects = []
    y = 0
    for row in gameMap:
        x = 0
        for tile in row:
            if tile == 1:
                display.blit(groundBlock, (x * blockSize,y * blockSize ))
            if tile == 2:
                display.blit(brick, (x * blockSize, y * blockSize))
            if tile != 0:
                tile_rects.append(pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize))
            x += 1
        y += 1



    if playerPos[1] <= WINDOW_SIZE[1] - playersize + velY and jumping == True: # is player above ground and jumping
        playerPos[1] -= velY 
        velY -= 0.5 # velY = 0 when at top of jump.
    else:
        jumping = False
        velY = 10 # set to 10 so that the start of next jump will start at fastest speed.









    if playerRunCount == 999: # if standing
        display.blit(playerImage,playerPos)
    else: # if running
        display.blit(runImages[playerRunCount],playerPos)


    surf = pygame.transform.scale(display,WINDOW_SIZE)
    screen.blit(surf, (0,0))

    pygame.display.update() # update display
    clock.tick(60) # set frame rate