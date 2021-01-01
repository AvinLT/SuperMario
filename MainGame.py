import pygame, sys
import copy
import cmath
import random
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
bowserWidth = 40
bowserHeight = 50

firePlayerImages = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireStand.png"), True, False), (playerWidth, playerHeight)),
                    pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireStand.png"), (playerWidth, playerHeight)),
                ]

bowserImages = [
                    pygame.transform.scale(pygame.image.load(r"sprites\enemies\bowserstandleft.PNG"), (bowserWidth, bowserHeight)),
                    pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\bowserstandleft.PNG"), True, False), (bowserWidth, bowserHeight))
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
bowserRunImages = [pygame.transform.scale(pygame.image.load(r"sprites\enemies\runleft1.PNG"), (bowserWidth, bowserHeight)),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\runleft2.PNG"), (bowserWidth, bowserHeight)),
                 pygame.transform.scale(pygame.image.load(r"sprites\enemies\runleft3.PNG"), (bowserWidth, bowserHeight)),
                 pygame.transform.scale(pygame.image.load(r"sprites\enemies\runleft4.PNG"),(bowserWidth, bowserHeight)),

                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\runleft1.PNG"), True, False),(bowserWidth, bowserHeight)),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\runleft2.PNG"), True, False),(bowserWidth, bowserHeight)),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\runleft3.PNG"), True, False),(bowserWidth, bowserHeight)),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\runleft4.PNG"), True, False),(bowserWidth, bowserHeight))
                 ]

bowserPowers = [pygame.transform.scale(pygame.image.load(r"sprites\interactables\boswerFire.PNG"), (10, 10)),
pygame.transform.scale(pygame.image.load(r"sprites\interactables\bowserHammer.PNG"), (10, 10))
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
True_cameraMove = [0,0]
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
            else:  # if running
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


class bossFireBall():
    def __init__(self,player,boss,image):
        self.player = player
        self.boss = boss
        self.playerCentre = [player.playerRect.centerx, player.playerRect.centery]
        self.image = image
        self.length = image.get_height()
        if boss.facing == [0,1]:
            self.rect = pygame.Rect((boss.rect.x + boss.rect.width), (boss.rect.y - boss.rect.height/4), self.length, self.length )
        else:
            self.rect = pygame.Rect((boss.rect.x + self.length), (boss.rect.y - boss.rect.height/4), self.length, self.length )
        xdif = (self.playerCentre[0] - self.rect.x)
        ydif = (self.playerCentre[1] - self.rect.y)
        self.grad = [xdif/max(abs(xdif),abs(ydif)),ydif/max(abs(xdif),abs(ydif))]
        self.xTemp = 0
        self.yTemp = 0

        self.hit = False

    def move(self):
        self.xTemp += self.grad[0]
        if abs(self.xTemp) >= 1:
            self.rect.x += self.xTemp
            self.xTemp = self.xTemp-1 if self.xTemp>=0 else self.xTemp+1

        self.yTemp += self.grad[1]
        if abs(self.yTemp) >= 1:
            self.rect.y += self.yTemp
            self.yTemp = self.yTemp - 1 if self.yTemp >= 0 else self.yTemp + 1

        if len(collideRects(tileRects,self.rect))>0 or self.rect.colliderect(player.playerRect):
            self.hit = True

    def draw(self):
        if not(self.hit):
            display.blit(self.image,(self.rect.x - cameraMove[0], self.rect.y - cameraMove[1]))

def checktime(yPos,acel,yVel,yTarg):
    tot = 0
    count = 0
    if yTarg < yPos:
        while yPos + tot > yTarg:
            tot += yVel
            yVel += acel
            count += 1
    else:
        acel *= -1
        while yPos + tot < yTarg:
            tot += yVel
            yVel += acel
            count += 1
    return count

class bossHammer():
    def __init__(self,player,boss,image):
        self.player = player
        self.boss = boss
        self.playerCentre = [player.playerRect.centerx, player.playerRect.centery]
        self.image = image
        self.length = image.get_height()
        self.accel = 0.2
        self.velY = -2
        if boss.facing == [0, 1]:
            self.rect = pygame.Rect((boss.rect.x + boss.rect.width), (boss.rect.y - boss.rect.height / 4), self.length,
                                    self.length)
        else:
            self.rect = pygame.Rect((boss.rect.x + self.length), (boss.rect.y - boss.rect.height / 4), self.length,
                                    self.length)

        self.time = 10
        u = ((self.rect.y - self.playerCentre[1]) - 0.5*-self.accel*self.time**2)/self.time
        self.velY = u/3

        """a = 0.5*-self.accel
        b = -self.velY
        c = -(self.rect.y - self.playerCentre[1])
        d = (b ** 2) - (4 * a * c)
        sol1 = (-b - cmath.sqrt(d)) / (2 * a)
        sol2 = (-b + cmath.sqrt(d)) / (2 * a)
        if sol1.imag == 0 and sol1.real > 0:
            self.time = sol1.real/60
        elif sol2.imag == 0 and sol2.real > 0:
            self.time = sol2.real/60
        else:
            print("TIME WRONG")"""

        self.velX = (self.playerCentre[0]-self.rect.x)/checktime(self.playerCentre[1],-self.accel,-self.velY,self.rect.y)
        self.hit = False

    def move(self):
        self.rect.x += self.velX
        self.rect.y += self.velY
        self.velY = self.velY + self.accel

        if len(collideRects(tileRects,self.rect))>0 or self.rect.colliderect(player.playerRect):
            self.hit = True

    def draw(self):
        if not(self.hit):
            display.blit(self.image, (self.rect.x - cameraMove[0], self.rect.y - cameraMove[1]))



class boss():
    def __init__(self,x,y,player,sightRange,meleeRange,standImages,runImages,throwableImages):

        self.player = player
        self.rect = pygame.Rect(x,y,standImages[0].get_width(), standImages[0].get_height())
        self.rangeRect = pygame.Rect(int(x-sightRange/2 + self.rect.width/2),int(y-sightRange/2 + self.rect.height/2),sightRange,sightRange)
        self.meleeRect = pygame.Rect(int(x-meleeRange/2 + self.rect.width/2),int(y-meleeRange/2 + self.rect.height/2),meleeRange,meleeRange)
        self.standImages = standImages
        self.runImages = runImages
        self.throwableImages = throwableImages
        self.accel = 0.2
        self.moving = "left"
        self.runCount = 0 # 999 signifies that player is not moving. if moving will be between 0 and 7
        self.runImagesDelay = 10  # how slow you want transitions from each running sprite
        self.hitDirection = {"top": False, "bottom": False, "left": False, "right": False}  # gives the direction of the collison
        self.facing = [1, 0]  # if [1,0], standing and facing left. if [0,1], standing and facing right
        self.fireBallList = []
        self.hammerThrowList = []
        self.moveCountMark = 40
        self.pauseCountMark = 60
        self.moveCount = self.moveCountMark
        self.pauseCount = self.pauseCountMark
        self.velX = 1
        self.velY = 0
        self.sign = -1
        self.tempCount = 0


    def scan(self,player):
        if self.rangeRect.colliderect(player.playerRect):
            if self.meleeRect.colliderect(player.playerRect):
                pass

    def move(self):

        for fireball in self.fireBallList:
            fireball.move()
        for hammer in self.hammerThrowList:
            hammer.move()

        self.rect, self.hitDirection = move(self.rect, [0, self.velY], tileRects)
        self.velY += self.accel
        if self.velY > 4:
            self.velY = 4

        if self.moveCount > 0:


            self.tempCount += 1
            if self.tempCount % self.runImagesDelay == 0:
                self.runCount = (self.runCount + 1) % 4

            if self.sign == -1:
                self.moving = "left"
            else:
                self.moving = "rigth"
            if self.tempCount % 2 == 0:

                self.rect.x += self.sign * self.velX
                movement = [self.sign * self.velX,0 ]


                self.rect, self.hitDirection = move(self.rect, movement, tileRects)


                self.moveCount -= 1
        else:
            self.moving = "standing"
            if self.pauseCount > 0:
                self.pauseCount -= 1
            else:
                self.moveCount = self.moveCountMark
                self.pauseCount = self.pauseCountMark
                rand = random.randint(0, 100)

                if rand < 50:
                    self.sign = 1
                    self.facing = [0, 1]
                else:
                    self.sign = -1
                    self.facing = [1, 0]

                if rand > 50:
                    self.fireBallList.append(bossFireBall(self.player,self,self.throwableImages[0]))
                elif rand > 1:
                    self.hammerThrowList.append(bossHammer(self.player, self, self.throwableImages[1]))
                else:
                    pass

    def draw(self):
        for fireball in self.fireBallList:
            fireball.draw()
        for hammer in self.hammerThrowList:
            hammer.draw()

        if self.facing == [0, 1] and self.moving == "standing":  # if standing and facing rigth
            display.blit(self.standImages[1], [self.rect.x - cameraMove[0], self.rect.y - cameraMove[1]])
        elif self.facing == [1, 0] and self.moving == "standing":  # if standing and facing left
            display.blit(self.standImages[0], [self.rect.x - cameraMove[0], self.rect.y - cameraMove[1]])
        else:  # if running
            if self.facing == [1, 0] and self.moving != "standing":
                display.blit(self.runImages[self.runCount], [self.rect.x - cameraMove[0], self.rect.y - cameraMove[1]])
            else:
                display.blit(self.runImages[self.runCount+4], [self.rect.x - cameraMove[0], self.rect.y - cameraMove[1]])






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
def collideRects(tileRects, Rect):
    hitRects = []
    for tile in tileRects:
        if Rect.colliderect(tile):
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

bowser = boss(80,40,player,100,25,bowserImages,bowserRunImages,bowserPowers)

#initialising goomba
enemyList = [enemies(66,128,64,256,1,goombaImages),
             enemies(128,48,112,175,1,goombaImages)]
fireBallList = [] # list of fireball objects
mBlockList = [] # list of mBlock objects


while True: #Main game loop

    display.fill((255,255,255)) # makes screen white

    True_cameraMove[0] += (player.playerRect.x - cameraMove[0] - 148)/10
    True_cameraMove[1] += (player.playerRect.y - cameraMove[1] - 94)/10
    cameraMove = True_cameraMove.copy()
    cameraMove[0] = int(cameraMove[0])
    cameraMove[1] = int(cameraMove[1])


    for event in pygame.event.get(): #event loop
        if event.type == QUIT: # checks if window is closed
            pygame.quit() #stops pygame
            sys.exit() # stops script

        if event.type == KEYDOWN:
            if event.key == K_SPACE and player.powerUp == "fireFlower":
                fireBallList.append(fireBall(player.facing,player.playerRect,fireBallImages))
            if event.key == K_j:
                bowser.velY = -4


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

    bowser.move()


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


    bowser.draw()
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