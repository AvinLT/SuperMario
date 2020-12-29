import pygame, sys
import copy
from pygame.locals import * #import modules


clock = pygame.time.Clock() #initialize clock
pygame.init() #initialize pygame

WINDOW_SIZE = (640,384) #window size
display = pygame.Surface((320,192)) # what we display images on. later print 'display' on screen
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initialize window

# size of player image
playerWidth = 20

# standing sprite
playerImages = [pygame.transform.scale(pygame.image.load("sprites\marioset\standleft.png"), (playerWidth, playerWidth)),
                pygame.transform.scale(pygame.image.load("sprites\marioset\stand.png"), (playerWidth, playerWidth))]

# the sprites for runnning
runImages = [
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1right.png"), (playerWidth, playerWidth)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (playerWidth, playerWidth)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3right.png"), (playerWidth, playerWidth)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (playerWidth, playerWidth)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1left.png"), (playerWidth, playerWidth)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (playerWidth, playerWidth)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3left.png"), (playerWidth, playerWidth)),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (playerWidth, playerWidth))
]

playerWidth = 20
playerHeight = 35

firePlayerImages = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireStand.png"), True, False), (playerWidth, playerHeight)),
                    pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireStand.png"), (playerWidth, playerHeight)),
                ]

fireRunImages = [pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireRunRight1.PNG"), (playerWidth, playerHeight)),
                pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireRunRight2.PNG"), (playerWidth, playerHeight)),
                pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireRunRight1.PNG"), (playerWidth, playerHeight)),
                 pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireRunRight3.PNG"), (playerWidth, playerHeight)),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireRunRight1.PNG"), True, False),(playerWidth, playerHeight)),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireRunRight2.PNG"), True, False),(playerWidth, playerHeight)),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireRunRight1.PNG"), True, False),(playerWidth, playerHeight)),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireRunRight3.PNG"), True, False),(playerWidth, playerHeight))
                 ]

coinImages = [
pygame.image.load(r"sprites\interactables\c1.png"),
pygame.image.load(r"sprites\interactables\c2.png"),
pygame.image.load(r"sprites\interactables\c3.png"),
pygame.image.load(r"sprites\interactables\c4.png"),
pygame.image.load(r"sprites\interactables\c5.png"),
pygame.image.load(r"sprites\interactables\c6.png")
]

goombaSize = 16
goombaImages = [pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaL.png"), (goombaSize, goombaSize)),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaR.png"), (goombaSize, goombaSize)),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaSqa.png"), (goombaSize, goombaSize))]

fireFlowerImages = [pygame.image.load(r"sprites\interactables\fireflower.png")]

fireBallImages = pygame.image.load(r"sprites\interactables\fireBall.png")

blockSize = 16 #size of the blocks on map
groundBlock = pygame.transform.scale(pygame.image.load(r"sprites\blocks\groundBlock.png"), (blockSize, blockSize))
mysteryBlock = pygame.transform.scale(pygame.image.load(r"sprites\blocks\mysterybox.png"), (blockSize, blockSize))
brick = pygame.transform.scale(pygame.image.load(r"sprites\blocks\brick.png"), (blockSize, blockSize))


tempCount = 0 # used for animation of player running

global cameraMove
cameraMove = [0,0]

def loadMap(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    gameMap = []
    for row in data:
        gameMap.append(list(row))
    return gameMap

# the map. 1 represents ground block. 2 represents brick. 0 is nothing. each block is 16
gameMap = loadMap('GameMap')


gameMapCopy = copy.deepcopy(gameMap) #To not duplicate mBlock object.if value is 1000, shows mBlock position.



class player():
    def __init__(self,x,y,playerImages,runImages,firePlayerImages,fireRunImages):
        self.playerImages = playerImages # standing sprite
        self.runImages = runImages # the sprites for runnning
        self.firePlayerImages = firePlayerImages
        self.fireRunImages = fireRunImages # the sprites when in fire power up state.
        self.playerRect = pygame.Rect(x,y, playerImages[0].get_width(), playerImages[0].get_height()) # creates a rect for the player
        self.playerRunCount = 999 # 999 signifies that player is not moving. if moving will be between 0 and 7
        self.runImagesDelay = 9 # how slow you want transitions from each running sprite
        self.playerVelY = 0 # player y velocity
        self.hitDirection = {"top": False, "bottom": False, "left":False, "right":False} # gives the direction of the collison
        self.movingRight =False # shows if player is moving left or right
        self.movingLeft = False # shows if player is moving left or right
        self.facing = [0,1] # if [1,0], standing and facing left. if [0,1, standing and facing right
        self.jumping = False # shows whether player is jumping
        self.powerUp = "" # shows is player has any power up

    def draw(self,powerUp):
        if powerUp == "":

            if self.facing == [0,1] and self.playerRunCount == 999: # if standing and facing left
                display.blit(self.playerImages[1], [self.playerRect.x - cameraMove[0], self.playerRect.y - cameraMove[1]])
            elif self.facing == [1,0] and self.playerRunCount == 999:  # if standing and facing right
                display.blit(self.playerImages[0], [self.playerRect.x - cameraMove[0], self.playerRect.y- cameraMove[1]])
            else:  # if standing
                display.blit(self.runImages[self.playerRunCount], [self.playerRect.x - cameraMove[0],self.playerRect.y- cameraMove[1]])
        elif powerUp == "fireFlower":
            if self.facing == [0,1] and self.playerRunCount == 999: # if standing and facing left
                display.blit(self.firePlayerImages[1], [self.playerRect.x-cameraMove[0], self.playerRect.y-cameraMove[1]])
            elif self.facing == [1,0] and self.playerRunCount == 999:  # if standing and facing right
                display.blit(self.firePlayerImages[0], [self.playerRect.x-cameraMove[0], self.playerRect.y-cameraMove[1]])
            else:  # if standing
                display.blit(self.fireRunImages[self.playerRunCount], (self.playerRect.x-cameraMove[0],self.playerRect.y-cameraMove[1]))


class fireBall():
    def __init__(self,facingDirection,playerRect,fireBallImages):
        self.facing = facingDirection

        if facingDirection == [0, 1]:
            self.velX = 4
        elif facingDirection == [1, 0]:
            self.velX = -4
        if facingDirection == [0,1]:
            x = playerRect.x + playerRect.width
        else:
            x = playerRect.x - fireBallImages.get_width()

        y = playerRect.centery

        self.rect = pygame.Rect(x, y, fireBallImages.get_width(), fireBallImages.get_height())#rect for each fireball
        self.velY = 3 # starting y vel
        self.accel = 0.2 # y acceleration
        self.hit = False # whether fireball has hit a something other than the floor
        self.images = fireBallImages#images for fireball
        self.bounceSpeed = -2 # the y vel when fireball bounces
        self.animeCount = 0

    def move(self):
        hitDirection = {"top": False, "bottom": False, "left": False, "right": False}#the direction of the collison of fireball


        if not(self.hit):

            self.rect.x += self.velX
            hitRect = collideRects(tileRects, self.rect)
            if len(hitRect) > 0:
                if self.facing == [0,1]:
                    hitDirection["right"] = True
                elif self.facing == [1, 0]:
                    hitDirection["left"] = True

            self.rect.y += self.velY
            hitRect = collideRects(tileRects, self.rect)
            if len(hitRect) > 0:
                if self.velY > 0:
                    hitDirection["bottom"] = True
                    self.rect.bottom = hitRect[0].top # so that the fireball isn't inside floor tile.
                else:
                    hitDirection["top"] = True

        if hitDirection["right"] == True:
            self.hit = True
        elif hitDirection["left"] == True:
            self.hit = True
        elif hitDirection["bottom"] == True:
            self.velY = self.bounceSpeed #bouncing
        elif hitDirection["top"] == True :
            self.velY = -self.velY

        self.velY += self.accel

    def draw(self):
        if not(self.hit):
            self.animeCount += 1
            if self.animeCount % 8 == 0:
                self.images = pygame.transform.rotate(self.images,90)
            display.blit(self.images, [self.rect.x-cameraMove[0], self.rect.y-cameraMove[1]])


class boss():
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
        self.rect = pygame.Rect(x, y, self.images[0].get_width(), self.images[0].get_height())# rect for enemy
        self.deadTimer = 60 # how long image visible after death

    def move(self):
        if not self.squashed:
            self.x += self.velX
            self.rect.x += self.velX
            self.walkCount += 1
            
            if self.x > self.endX: #turn around when at the end of path
                self.velX = -self.velX
                self.walkCount = 0
            if self.x < self.startX: #turn around when at the end of path
                self.velX = -self.velX
                self.walkCount = 0
        else:
            self.velX = 0
            self.deadTimer -= 1

    def draw(self):
        if not self.squashed:
            display.blit(self.images[(self.walkCount // 8) % 2], (self.x-cameraMove[0], self.y-cameraMove[1]))
        else:
            if self.deadTimer > 0:
                display.blit(self.images[2], (self.x-cameraMove[0], self.y-cameraMove[1]))

class mysteryB:
    def __init__(self,x,y,image,powerUp,powerImage):
        self.x = x # x pos
        self.y = y # y pos
        self.startY = y # initial y pos, to drop back to initial position after animation 
        self.hit = False # whether block has been used
        self.powerUp = powerUp # power up in block
        self.image = image # image
        self.powerImage = powerImage # image of power up
        self.funcX = 0 # used as x for function, inputted in function to give y value
        self.powerVelY = 0.5 # speed of power animation
        self.powerHit = False # has the power up been used
        self.animeCount = 0 # used to slow down animation.
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()) # rect for mBlock
        self.powerRect = pygame.Rect(self.x, self.y, 16, 16) # rect for power up

    def draw(self):

        if self.powerUp == "coin":
            self.animeCount += 1
            if self.hit and not(self.powerHit):
                if self.powerRect.y - 3> self.startY - 16:
                    display.blit(self.powerImage[(self.animeCount // 8) % 6], (self.powerRect.x-cameraMove[0], self.powerRect.y-cameraMove[1] - 3))
                    self.powerRect.y -= self.powerVelY
                else:
                    display.blit(self.powerImage[(self.animeCount // 8) % 6], (self.powerRect.x-cameraMove[0], self.powerRect.y-cameraMove[1] - 3))

        elif self.powerUp == "fireFlower":
            if self.hit and not(self.powerHit):
                if self.powerRect.y - 3> self.startY - 16:
                    display.blit(self.powerImage[(self.animeCount // 8) % 1], (self.powerRect.x-cameraMove[0], self.powerRect.y-cameraMove[1] - 3))
                    self.powerRect.y -= self.powerVelY
                else:
                    display.blit(self.powerImage[(self.animeCount // 8) % 1], (self.powerRect.x-cameraMove[0], self.powerRect.y-cameraMove[1] - 3))


        equ = lambda x: -(0.5*x**2-4)

        if self.hit and self.funcX > -1000:
            display.blit(self.image, (self.x -cameraMove[0], self.y - equ(self.funcX)-cameraMove[1]))

            if equ(self.funcX) < 0:
                self.funcX = -1001
            else:
                self.funcX += 0.2
        else:
            display.blit(self.image, (self.x-cameraMove[0], self.y-cameraMove[1] ))











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

#checks to see if player squashed enemy
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

#checks to see player hit mBlock
def mBlockCollide(playerRect,movement,mBlockRect):
    temp = copy.deepcopy(playerRect)
    temp.y += movement[1]
    didHit = temp.colliderect(mBlockRect)

    if movement[1] <= 0 and didHit:
        return True
    return False



player = player(10,44,playerImages,runImages,firePlayerImages,fireRunImages)

#initialising goomba
enemyList = [enemies(66,128,64,256,1,goombaImages),
             enemies(128,48,112,175,1,goombaImages)]
fireBallList = [] # list of fireball objects
mBlockList = [] # list of mBlock objects


while True: #Main game loop

    display.fill((255,255,255)) # makes screen white

    cameraMove[0] += player.playerRect.x - cameraMove[0] - 148
    cameraMove[1] += player.playerRect.y - cameraMove[1] - 94


    for event in pygame.event.get(): #event loop
        if event.type == QUIT: # checks if window is closed
            pygame.quit() #stops pygame
            sys.exit() # stops script

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                fireBallList.append(fireBall(player.facing,player.playerRect,fireBallImages))


        #although this code for controls fixes the bug that occurs when changingd x direction quickly, it doesnt
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
        player.facing = [0,1]  # signifies player is standing

    elif keys[K_a]:# when a is pressed, moves left
        player.movingLeft = True

        tempCount = (tempCount + 1) % player.runImagesDelay # only transitions to next sprite when tempCount is 0.
        if tempCount == 0:
            player.playerRunCount += 1
            player.playerRunCount = (player.playerRunCount % 4) + 4 # loops between 4 and 7, which have correspondin sprites in runImages list.
        player.facing = [1,0]  # signifies player is standing

    else:
        player.movingLeft = False
        player.movingRight = False
        player.playerRunCount = 999


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
            if tile == '1':
                display.blit(groundBlock, (x * blockSize - cameraMove[0],y * blockSize - cameraMove[1]))
            if tile == '2':
                display.blit(brick, (x * blockSize - cameraMove[0], y * blockSize - cameraMove[1]))
            if tile == '3':
                if gameMapCopy[y][x] != 1000:
                    mBlockList.append(mysteryB(x * blockSize , y * blockSize, mysteryBlock,"fireFlower",fireFlowerImages))
                gameMapCopy[y][x] = 1000
            if tile == '4':
                if gameMapCopy[y][x] != 1000:
                    mBlockList.append(mysteryB(x * blockSize , y * blockSize, mysteryBlock,"coin",coinImages))
                gameMapCopy[y][x] = 1000
            if tile != '0':
                tileRects.append(pygame.Rect(x * blockSize , y * blockSize , blockSize, blockSize))
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
    if player.playerVelY > 4:
        player.playerVelY = 4



    #updates the player position and the collision direction
    player.playerRect, player.hitDirection= move(player.playerRect, playerMovement, tileRects)


    #playerRect, enemyHit = move(playerRect, playerMovement, [goomba.rect])
    for enemy in enemyList:
        if enemy.squashed != True:
            player.playerVelY, enemy.squashed = enemyCollide(player.playerRect, playerMovement, enemy.rect, player.playerVelY)

        enemy.move()

    # moves all the fireball
    for fireball in fireBallList:
        fireball.move()

    # checks to see is mBlock and power up have been hit
    for mBlock in mBlockList:
        if mBlockCollide(player.playerRect, playerMovement, mBlock.rect):
            mBlock.hit = True

        if mBlock.hit and player.playerRect.colliderect(mBlock.powerRect):
            mBlock.powerHit = True
            if mBlock.powerUp == "fireFlower":
                player.playerRect = pygame.Rect(player.playerRect.x, player.playerRect.y, player.firePlayerImages[0].get_width(), player.firePlayerImages[0].get_height())
                player.powerUp = "fireFlower"





    #if the player is standing, set the y velocity to 0
    if player.hitDirection['bottom']:
        player.playerVelY = 0
    if player.hitDirection['top']:
        player.playerVelY = 0



    player.draw(player.powerUp)

    for enemy in enemyList:
        enemy.draw()

    for mBlock in mBlockList:
        mBlock.draw()

    for ball in fireBallList:
        ball.draw()

    #pygame.draw.rect(display,(255,0,0),player.playerRect)

    surf = pygame.transform.scale(display,WINDOW_SIZE)
    screen.blit(surf, (0,0))

    pygame.display.update() # update display
    clock.tick(60) # set frame rate