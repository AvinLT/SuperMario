import pygame, sys
import copy
from pygame.locals import * #import modules


clock = pygame.time.Clock() #initialize clock

pygame.init() #initialize pygame

WINDOW_SIZE = (600,400) #window size

display = pygame.Surface((320,192))


screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initialize window

playerSize = 28
playerImage = pygame.transform.scale(pygame.image.load("sprites\marioset\stand.png"), (playerSize, playerSize)) # standing sprite

# the sprites for runnning
runImages = [
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1right.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3right.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1left.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3left.png"), (playerSize, playerSize)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (playerSize, playerSize))
]

goombaSize = 16

#enemy sprite
goombaImages = [pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaL.png"), (goombaSize, goombaSize)),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaR.png"), (goombaSize, goombaSize)),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaSqa.png"), (goombaSize, goombaSize))]


blockSize = 16 #size of the blocks on map
groundBlock = pygame.transform.scale(pygame.image.load(r"sprites\blocks\groundBlock.png"), (blockSize, blockSize))
brick = pygame.transform.scale(pygame.image.load(r"sprites\blocks\brick.png"), (blockSize, blockSize))





playersize = playerImage.get_height()# size of player image

playerRect = pygame.Rect(10,144-100, playerSize, playerSize) # creates a rect for the player

playerRunCount = 999 # 999 signifies that player is not moving. if moving will be between 0 and 7
runImagesDelay = 9 # how slow you want transitions from each running sprite
tempCount = 0


hitDirection = {"top": False, "bottom": False, "left":False, "right":False} # gives the direction of the collison
enemeyHit = {"top": False, "bottom": False, "left":False, "right":False}

#the map. 1 represents ground block. 2 represents brick. 0 is nothing. each block is 16
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


#creates an enemy object.
class enemies():

    def __init__(self,x,y,velX,startX,endX,images):
        self.x = x # x position
        self.y = y # y position
        self.velX = velX # velocity
        self.startX = startX # left edge of path
        self.endX = endX # right edge of path
        self.squashed = False # checks if enemy is squashed
        self.walkCount = 0 # used to render walking animation
        self.images = images # the png images used
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())

        self.deadTimer = 60
    def move(self):
        if not self.squashed:

            self.x += self.velX
            self.rect.x += self.velX
            self.walkCount += 1


            if self.x > self.endX:
                self.velX = -self.velX
                self.walkCount = 0
            if self.x < self.startX:
                self.velX = -self.velX
                self.walkCount = 0
        else:
            self.velX = 0
            self.deadTimer -= 1

    def draw(self):
        if not self.squashed:
            display.blit(self.images[(self.walkCount // 8) % 2], (self.x, self.y))
        else:
            if self.deadTimer > 0:
                display.blit(self.images[2], (self.x, self.y))



#checks to see if player is colliding with any blocks on map
def colliderects(tileRects, playerRect):
    hitRects = []
    for tile in tileRects:
        if playerRect.colliderect(tile):
            hitRects.append(tile)
    return hitRects

#if there is a collision, then set player position to right next to the colliding block.
#the function outputs the updated player positon and the direction of the collision.
def move(playerRect, movement, tileRects):
    hitDirection = {"top": False, "bottom": False, "left": False, "right": False}
    playerRect.x += movement[0]
    hitRect = colliderects(tileRects, playerRect)

    for tile in hitRect:
        if movement[0] > 0:
            playerRect.right = tile.left
            hitDirection["right"] = True
        elif movement[0] < 0:
            playerRect.left = tile.right
            hitDirection["left"] = True

    playerRect.y += movement[1]
    hitRect = colliderects(tileRects, playerRect)

    for tile in hitRect:
        if movement[1] > 0:
            playerRect.bottom = tile.top
            hitDirection["bottom"] = True
        elif movement[1] < 0:
            playerRect.top = tile.bottom
            hitDirection["top"] = True

    return playerRect, hitDirection

def enemycollide(playerRect,movement,rectlist,playerVelY):
    temp = copy.deepcopy(playerRect)
    temp.y += movement[1]
    hitRect = colliderects(rectlist, temp)
    squashed = False

    for enemy in hitRect:
        if movement[1] >= 1.5:
            playerVelY = -3
            squashed = True

    return playerVelY, squashed


#shows if player is moving left or right
movingRight = False
movingLeft = False

#player velocity
playerVelY = 0

#initialising goomba
goomba = enemies(66,128,1,64,256,goombaImages)

while True: #Main game loop

    display.fill((255,255,255)) # makes screen white



    for event in pygame.event.get(): #event loop
        if event.type == QUIT: # checks if window is closed
            pygame.quit() #stops pygame
            sys.exit() # stops script

        #although this code for controls fixes the bug that occurs when changing x direction quickly, it doesnt
        #allow the animation to occur. Hopefully I can fix this later on. Right now, its not a big bug.
        """if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                movingRight = True

                tempCount = (tempCount + 1) % runImagesDelay  # only transitions to next sprite when tempCount is 0.
                if tempCount == 0:
                    playerRunCount += 1
                    playerRunCount = playerRunCount % 4  # loops between 0 and 3, which have correspondin sprites in runImages list.

            if event.key == K_LEFT:
                movingLeft = True

                tempCount = (tempCount + 1) % runImagesDelay  # only transitions to next sprite when tempCount is 0.
                if tempCount == 0:
                    playerRunCount += 1
                    playerRunCount = (playerRunCount % 4) + 4  # loops between 4 and 7, which have correspondin sprites in runImages list.

            if event.key == K_UP:
                playerVelY= -5
                
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                movingRight = False
                playerRunCount = 999
            if event.key == K_LEFT:
                movingLeft = False
                playerRunCount = 999"""


    keys = pygame.key.get_pressed()

    if keys[K_d]: # when d is pressed, moves right
        movingRight = True

        tempCount = (tempCount +1)  % runImagesDelay # only transitions to next sprite when tempCount is 0.
        if tempCount==0:
            playerRunCount += 1
            playerRunCount = playerRunCount % 4 # loops between 0 and 3, which have correspondin sprites in runImages list.

    elif keys[K_a]:# when a is pressed, moves left
        movingLeft = True

        tempCount = (tempCount + 1) % runImagesDelay # only transitions to next sprite when tempCount is 0.
        if tempCount == 0:
            playerRunCount += 1
            playerRunCount = (playerRunCount % 4) + 4 # loops between 4 and 7, which have correspondin sprites in runImages list.

    else:
        playerRunCount = 999 # signifies player is standing
        movingLeft = False
        movingRight = False


    if hitDirection["bottom"]==True: # stops the jump key being pressed when still in air.

        if keys[K_w]:# when w is pressed, jumps
            jumping = True
            playerVelY = -6 # makes the player move up.






    tileRects = []
    y = 0
    for row in gameMap: # builds the map
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

    #playerMovement is the intended movement
    playerMovement = [0, 0]

    #x direction movement
    if movingRight:
        playerMovement[0] += 2
    if movingLeft:
        playerMovement[0] -= 2

    #y direction movement
    playerMovement[1] += playerVelY

    # decreases the y velocity. when playerVelY is +ive, player goes up. whe -ive, player goes down.
    playerVelY += 0.2

    #sets the y velocity to max 3.
    if playerVelY > 3:
        playerVelY = 3



    #updates the player position and the collision direction
    playerRect, hitDirection= move(playerRect, playerMovement, tileRects)


    #playerRect, enemyHit = move(playerRect, playerMovement, [goomba.rect])
    if goomba.squashed != True:
        playerVelY, goomba.squashed = enemycollide(playerRect, playerMovement, [goomba.rect], playerVelY)

    #updates goomba movements
    goomba.move()

    #if the player is standing, set the y velocity to 0
    if hitDirection['bottom']:
        playerVelY = 0
    if hitDirection['top']:
        playerVelY = 0









    if playerRunCount == 999: # if standing
        display.blit(playerImage,[playerRect.x,playerRect.y])
    else: # if running
        display.blit(runImages[playerRunCount],[playerRect.x,playerRect.y])
    goomba.draw()

    surf = pygame.transform.scale(display,WINDOW_SIZE)
    screen.blit(surf, (0,0))

    pygame.display.update() # update display
    clock.tick(60) # set frame rate