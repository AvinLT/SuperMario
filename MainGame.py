import pygame, sys
import copy
from pygame.locals import * #import modules


clock = pygame.time.Clock() #initialize clock

pygame.init() #initialize pygame

WINDOW_SIZE = (640,384) #window size

display = pygame.Surface((320,192)) # what we display images on. later print 'display' on screen


screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initialize window

playerSize = 28# size of player image
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

coinImages = [
pygame.image.load(r"sprites\interactables\c1.png"),
pygame.image.load(r"sprites\interactables\c2.png"),
pygame.image.load(r"sprites\interactables\c3.png"),
pygame.image.load(r"sprites\interactables\c4.png"),
pygame.image.load(r"sprites\interactables\c5.png"),
pygame.image.load(r"sprites\interactables\c6.png")
]

fireBallImages = pygame.image.load(r"sprites\interactables\fireBall.png")

goombaSize = 16

#enemy sprite
goombaImages = [pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaL.png"), (goombaSize, goombaSize)),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaR.png"), (goombaSize, goombaSize)),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaSqa.png"), (goombaSize, goombaSize))]

fireFlowerImages = [pygame.image.load(r"sprites\interactables\fireflower.png")]

blockSize = 16 #size of the blocks on map
groundBlock = pygame.transform.scale(pygame.image.load(r"sprites\blocks\groundBlock.png"), (blockSize, blockSize))
mysteryBlock = pygame.transform.scale(pygame.image.load(r"sprites\blocks\mysterybox.png"), (blockSize, blockSize))
brick = pygame.transform.scale(pygame.image.load(r"sprites\blocks\brick.png"), (blockSize, blockSize))


tempCount = 0


# the map. 1 represents ground block. 2 represents brick. 0 is nothing. each block is 16
gameMap = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,3,2,2,2,4,2,2,2,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

gameMapCopy = copy.deepcopy(gameMap) #To not duplicate mBlock object.if value is 1000, shows mBlock position.

"""class blocks():
    def __init__(self,x,y,blockType,hit,images):
        self.x = x
        self.y = y
        self.blockType = blockType
        self.hit = hit
        self.fixedYPos = self.y
        self.images = images
        self.velY = 0
        self.finished = False

    def hitanime(self):

        self.velY += 0.2
        self.y += self.velY

        if self.y > self.fixedYPos:
            self.y = self.fixedYpos
            self.hit = False
            self.finished = True

    def draw(self):
        self.animeCount += 1

        if not self.hit:
            display.blit(self.images[(self.animeCount // 6) % 3], (self.x, self.y))
        else:
            display.blit(self.images[3], (self.x, self.y))"""

class player():
    def __init__(self,x,y,playerImages,runImages):
        self.x = x#x cords
        self.y = y#y cords
        self.playerImage = playerImages# standing sprite
        self.runImages = runImages# the sprites for runnning
        self.playerSize = playerImage.get_height()
        self.playerRect = pygame.Rect(x,y, self.playerSize, self.playerSize)# creates a rect for the player
        self.playerRunCount = 999# 999 signifies that player is not moving. if moving will be between 0 and 7
        self.runImagesDelay = 9# how slow you want transitions from each running sprite
        self.playerVelY = 0#player y velocity
        self.hitDirection = {"top": False, "bottom": False, "left":False, "right":False} # gives the direction of the collison
        self.movingRight =False#shows if player is moving left or right
        self.movingLeft = False
        self.jumping = False#shows whether player is jumping
        self.powerUp = ""#shows is player has any power up

    def draw(self):
        if self.playerRunCount == 999:  # if standing
            display.blit(self.playerImage, [self.playerRect.x, self.playerRect.y])
        else:  # if running
            display.blit(self.runImages[self.playerRunCount], [self.playerRect.x, self.playerRect.y])


class fireBall():
    def __init__(self,movingLeft,movingRight,playerRect,fireBallImages):
        x = playerRect.x + playerRect.width
        y = playerRect.centery
        self.rect = pygame.Rect(x,y, fireBallImages.get_width(), fireBallImages.get_height())
        self.movingLeft = movingLeft
        self.movingRight = movingRight
        self.velY = 3
        self.accel = 0.2
        if movingRight:
            self.velX = 3
        elif movingLeft:
            self.velX = -3
        else:
            self.velX = 3
        self.hit = False
        self.images = fireBallImages
        self.jumpheight = -2

    def move(self):
        global tileRects

        hitDirection = {"top": False, "bottom": False, "left": False, "right": False}

        if not(self.hit):

            self.rect.x += self.velX
            hitRect = collideRects(tileRects, self.rect)
            if len(hitRect) > 0:
                if self.movingRight:
                    hitDirection["right"] = True
                else:
                    hitDirection["left"] = True

            self.rect.y += self.velY
            hitRect = collideRects(tileRects, self.rect)
            if len(hitRect) > 0:
                if self.velY > 0:
                    hitDirection["bottom"] = True
                    self.velY = self.jumpheight
                    self.rect.bottom = hitRect[0].top

                else:
                    hitDirection["top"] = True

        if hitDirection["right"] == True and hitDirection["bottom"] == False:
            self.hit = True
        elif hitDirection["left"] == True and hitDirection["bottom"] == False:
            self.hit = True
        elif hitDirection["bottom"] == True:
            self.velY = self.jumpheight
        elif hitDirection["top"] == True :
            self.velY = -self.velY

        self.velY += self.accel

    def draw(self):
        if not(self.hit):
            display.blit(self.images, [self.rect.x, self.rect.y])
        else:
            pass







    #creates an enemy object.
class enemies():

    def __init__(self,x,y,startX,endX,velX,images):
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

class mysteryB:
    def __init__(self,x,y,image,powerUp,powerImage):
        self.x = x
        self.y = y
        self.startY = y
        self.hit = False
        self.powerUp = powerUp
        self.image = image
        self.powerImage = powerImage
        self.current = 0
        self.powerVelY = 0.5
        self.powerHit = False
        self.animeCount = 0

        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.powerRect = pygame.Rect(self.x, self.y, 16, 16)

    def draw(self):
        if self.powerUp == "coin":

            self.animeCount += 1

            if self.hit and not(self.powerHit):
                if self.powerRect.y - 3> self.startY - 16:
                    display.blit(self.powerImage[(self.animeCount // 8) % 6], (self.powerRect.x, self.powerRect.y - 3))
                    self.powerRect.y -= self.powerVelY
                else:
                    display.blit(self.powerImage[(self.animeCount // 8) % 6], (self.powerRect.x, self.powerRect.y - 3))
        elif self.powerUp == "fireFlower":
            if self.hit and not(self.powerHit):
                if self.powerRect.y - 3> self.startY - 16:
                    display.blit(self.powerImage[(self.animeCount // 8) % 1], (self.powerRect.x, self.powerRect.y - 3))
                    self.powerRect.y -= self.powerVelY
                else:
                    display.blit(self.powerImage[(self.animeCount // 8) % 1], (self.powerRect.x, self.powerRect.y - 3))


        equ = lambda x: -(0.5*x**2-4)

        if self.hit and self.current > -1000:
            display.blit(self.image, (self.x , self.y - equ(self.current)))

            if equ(self.current) < 0:
                self.current = -1001
            else:
                self.current += 0.2
        else:
            display.blit(self.image, (self.x, self.y ))











#checks to see if player is colliding with any blocks on map
def collideRects(tileRects, playerRect):
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
    hitRect = collideRects(tileRects, playerRect)

    for tile in hitRect:
        if movement[0] > 0:
            playerRect.right = tile.left
            hitDirection["right"] = True
        elif movement[0] < 0:
            playerRect.left = tile.right
            hitDirection["left"] = True

    playerRect.y += movement[1]
    hitRect = collideRects(tileRects, playerRect)

    for tile in hitRect:
        if movement[1] > 0:
            playerRect.bottom = tile.top
            hitDirection["bottom"] = True
        elif movement[1] < 0:
            playerRect.top = tile.bottom
            hitDirection["top"] = True

    return playerRect, hitDirection

def enemyCollide(playerRect,movement,enemyRect,playerVelY):
    temp = copy.deepcopy(playerRect)
    temp.y += movement[1]
    didHit = temp.colliderect(enemyRect)
    squashed = False

    if didHit:
        if movement[1] >= 1.5:
            playerVelY = -3
            squashed = True

    return playerVelY, squashed

def mBlockCollide(playerRect,movement,mBlockRect):
    temp = copy.deepcopy(playerRect)
    temp.y += movement[1]
    didHit = temp.colliderect(mBlockRect)

    if movement[1] <= 0 and didHit:
        return True
    return False


#initialising goomba
enemyList = [enemies(66,128,64,256,1,goombaImages),
             enemies(128,48,112,175,1,goombaImages)]

player = player(10,44,playerImage,runImages)

fireBallList = []

mBlockList = []

while True: #Main game loop

    display.fill((255,255,255)) # makes screen white


    for event in pygame.event.get(): #event loop
        if event.type == QUIT: # checks if window is closed
            pygame.quit() #stops pygame
            sys.exit() # stops script

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                fireBallList.append(fireBall(player.movingLeft,player.movingRight,player.playerRect,fireBallImages))


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
        player.movingRight = True

        tempCount = (tempCount +1)  % player.runImagesDelay # only transitions to next sprite when tempCount is 0.
        if tempCount==0:
            player.playerRunCount += 1
            player.playerRunCount = player.playerRunCount % 4 # loops between 0 and 3, which have correspondin sprites in runImages list.

    elif keys[K_a]:# when a is pressed, moves left
        player.movingLeft = True

        tempCount = (tempCount + 1) % player.runImagesDelay # only transitions to next sprite when tempCount is 0.
        if tempCount == 0:
            player.playerRunCount += 1
            player.playerRunCount = (player.playerRunCount % 4) + 4 # loops between 4 and 7, which have correspondin sprites in runImages list.

    else:
        player.playerRunCount = 999 # signifies player is standing
        player.movingLeft = False
        player.movingRight = False


    if player.hitDirection["bottom"] == True: # stops the jump key being pressed when still in air.

        if keys[K_w]:# when w is pressed, jumps
            player.jumping = True
            player.playerVelY = -6 # makes the player move up.



    global tileRects
    tileRects = []
    y = 0
    for row in gameMap: # builds the map
        x = 0
        for tile in row:
            if tile == 1:
                display.blit(groundBlock, (x * blockSize,y * blockSize ))
            if tile == 2:
                display.blit(brick, (x * blockSize, y * blockSize))
            if tile == 3:
                if gameMapCopy[y][x] != 1000:
                    mBlockList.append(mysteryB(x * blockSize, y * blockSize, mysteryBlock,"fireFlower",fireFlowerImages))
                gameMapCopy[y][x] = 1000
            if tile == 4:
                if gameMapCopy[y][x] != 1000:
                    mBlockList.append(mysteryB(x * blockSize, y * blockSize, mysteryBlock,"coin",coinImages))
                gameMapCopy[y][x] = 1000
            if tile != 0:
                tileRects.append(pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize))
            x += 1
        y += 1

    #playerMovement is the intended movement
    playerMovement = [0, 0]

    #x direction movement
    if player.movingRight:
        playerMovement[0] += 2
    if player.movingLeft:
        playerMovement[0] -= 2

    #y direction movement7y
    playerMovement[1] += player.playerVelY

    # decreases the y velocity. when playerVelY is +ive, player goes up. whe -ive, player goes down.
    player.playerVelY += 0.2

    #sets the y velocity to max 3.
    if player.playerVelY > 3:
        player.playerVelY = 3



    #updates the player position and the collision direction
    player.playerRect, player.hitDirection= move(player.playerRect, playerMovement, tileRects)


    #playerRect, enemyHit = move(playerRect, playerMovement, [goomba.rect])
    for enemy in enemyList:
        if enemy.squashed != True:
            player.playerVelY, enemy.squashed = enemyCollide(player.playerRect, playerMovement, enemy.rect, player.playerVelY)

        # updates goomba movements
        enemy.move()

    for ball in fireBallList:
        ball.move()


    for mBlock in mBlockList:
        if mBlockCollide(player.playerRect, playerMovement, mBlock.rect):
            mBlock.hit = True

        if mBlock.hit and player.playerRect.colliderect(mBlock.powerRect):
            mBlock.powerHit = True





    #if the player is standing, set the y velocity to 0
    if player.hitDirection['bottom']:
        player.playerVelY = 0
    if player.hitDirection['top']:
        player.playerVelY = 0




    player.draw()

    for enemy in enemyList:
        enemy.draw()

    for mBlock in mBlockList:
        mBlock.draw()

    for ball in fireBallList:
        ball.draw()

    surf = pygame.transform.scale(display,WINDOW_SIZE)
    screen.blit(surf, (0,0))

    pygame.display.update() # update display
    clock.tick(60) # set frame rate