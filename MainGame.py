import pygame, sys
from pygame.locals import * #import modules
clock = pygame.time.Clock() #initialize clock

pygame.init() #initialize pygame

WINDOW_SIZE = (600,400) #window size

display = pygame.Surface((320,192))


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


#playerPos = [100,144-28] #position of main character
playerRect = pygame.Rect(100,144-28, playerSize, playerSize)

playerRunCount = 999 # 999 signifies that player is not moving. if moving will be between 0 and 7
runImagesDelay = 9 # how slow you want transitions from each running sprite
tempCount = 0

movement = [0,0]

hitDirection = {"top": False, "bottom": False, "left":False, "right":False}



gameMap = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,2,2,2,2,2,2,2,2,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

jumping = False
#velY = 10 # acts as velocity
def colliderects(tileRects, playerRect):
    hitRects = []
    for tile in tileRects:
        if playerRect.colliderect(tile):
            hitRects.append(tile)
    return hitRects


def move(playerRect, movement, tileRects, jumping):
    hitDirection = {"top": False, "bottom": False, "left": False, "right": False}
    hitRect = colliderects(tileRects, playerRect)

    playerRect.x += movement[0]

    for tile in hitRect:
        if movement[0] > 0:
            playerRect.right = tile.left
            hitDirection["right"] = True
        elif movement[0] < 0:
            playerRect.left = tile.right
            hitDirection["left"] = True

    hitRect = colliderects(tileRects, playerRect)

    playerRect.y += movement[1]

    for tile in hitRect:
        if movement[1] < 0:
            playerRect.top = tile.bottom
            hitDirection["top"] = True
        elif movement[1] > 0:
            playerRect.bottom = tile.top
            hitDirection["bottom"] = True
            jumping = False
            movement[1] = 0

    return playerRect, hitDirection, jumping


def colliderects2(tileRects, playerRect):
    hitRects = []
    for tile in tileRects:
        tile.y = tile.y - 1
        if playerRect.colliderect(tile):
            hitRects.append(tile)
    return hitRects

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
        movingright = True
        movement[0] = 2
        tempCount = (tempCount +1)  % runImagesDelay # only transitions to next sprite when tempCount is 0.
        if tempCount==0:
            playerRunCount += 1
            playerRunCount = playerRunCount % 4 # loops between 0 and 3, which have correspondin sprites in runImages list.

    elif keys[K_a]:
        movingleft = True
        movement[0] = -2

        tempCount = (tempCount + 1) % runImagesDelay # only transitions to next sprite when tempCount is 0.
        if tempCount == 0:
            playerRunCount += 1
            playerRunCount = (playerRunCount % 4) + 4 # loops between 4 and 7, which have correspondin sprites in runImages list.

    else:
        playerRunCount = 999 # signifies player is standing
        movingleft = False
        movingright = False
        movement[0] = 0

    if not jumping :
        if keys[K_w]:
            jumping = True
            movement[1] = -10






    tileRects = []
    y = 0
    for row in gameMap:
        x = 0
        for tile in row:
            if tile == 1:
                display.blit(groundBlock, (x * blockSize,y * blockSize ))
            if tile == 2:
                display.blit(brick, (x * blockSize, y * blockSize))
            if tile != 0:
                tileRects.append(pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize))
            x += 1
        y += 1






    playerRect, hitDirection, jumping = move(playerRect, movement, tileRects, jumping)


    """for tile in tileRects:
        if movingright == True:
            if playerRect.x + movement[0] >"""




    if jumping == True: # is player above ground and jumping
        movement[1] += 0.5 # velY = 0 when at top of jump.
    """else:
        movement[1] = 0""" # set to 10 so that the start of next jump will start at fastest speed.


    """playerRect.x += movement[0]
    playerRect.y += movement[1]"""









    if playerRunCount == 999: # if standing
        display.blit(playerImage,[playerRect.x,playerRect.y])
    else: # if running
        display.blit(runImages[playerRunCount],[playerRect.x,playerRect.y])


    surf = pygame.transform.scale(display,WINDOW_SIZE)
    screen.blit(surf, (0,0))

    pygame.display.update() # update display
    clock.tick(60) # set frame rate