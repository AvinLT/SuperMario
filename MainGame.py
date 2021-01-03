# Made by Avin Lanson

import sys, copy, random
from pygame.locals import *
from ImageImport import *


clock = pygame.time.Clock() # initialize clock
pygame.init() # initialize pygame

WINDOW_SIZE = (640,384) #window size
display = pygame.Surface((320,192)) # what we display images on. later print 'display' on screen
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initialize window


True_cameraMove = [0,0]
global cameraMove
cameraMove = [0,0]



# load map from GameMap.txt
def loadMap(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    gameMap = []
    for row in data:
        gameMap.append(list(row))
    return gameMap

gameMap = loadMap('GameMap')# the map. 1 represents ground block. 2 represents brick. 0 is nothing. each block is 16
gameMapCopy = copy.deepcopy(gameMap) #To not duplicate mysteryBlock object.if value is 1000, shows mBlock position.

# used to find time for projectile to reach a y value. Applies only to projectiles with gravity effect
def checktime(yPos,acel,yVel,yTarg):
    tot = 0
    count = 0
    lock = True
    stop = False
    yVelMark = copy.deepcopy(yVel)
    
    if yTarg < yPos: # if target y value is lower that the initial y value
        while yPos + tot > yTarg:
            tot += yVel
            yVel += acel
            count += 1
    else: # if target y value is higher that the initial y value
        while not(stop):
            count += 1
            tot += yVel
            yVel += acel
            if yPos + tot >= yTarg: # since proj passes the targ y value twice (going up and then down), only second is counted.
                lock = False
            if not(lock):
                if yPos + tot + yVel <= yTarg and yVel < 0:
                    stop = True

            if count > 100: # if inital y vel isnt enough, to reach targ y value, make y vel bigger
                return checktime(yPos, acel, yVelMark + 3, yTarg)

    return count,-yVelMark


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
def enemyCollide(playerRect,movement,enemyRect,velY):
    temp = copy.deepcopy(playerRect)
    temp.y += movement[1]
    didHit = temp.colliderect(enemyRect)
    squashed = False

    if didHit:
        if movement[1] >= 1.5:
            velY = -3
            squashed = True

    return velY, squashed

#checks to see player hit mBlock
def mBlockCollide(playerRect,movement,mBlockRect):
    temp = copy.deepcopy(playerRect)
    temp.y += movement[1]
    didHit = temp.colliderect(mBlockRect)

    if movement[1] <= 0 and didHit:
        return True
    return False


# Without delay class ,subsequent code would execute every game loop
class delay():
    def __init__(self,delay):
        self.count = 0
        self.delay = delay

    def __bool__(self):
        self.count += 1
        if self.count % self.delay == 0:
            return True
        else:
            return False

class player():
    def __init__(self,x,y,playerImages,runImages,firePlayerImages,fireRunImages):
        
        self.playerImages = playerImages # standing sprite
        self.runImages = runImages # the sprites for runnning
        self.firePlayerImages = firePlayerImages
        self.fireRunImages = fireRunImages # the sprites when in fire power up state.
        self.playerRect = pygame.Rect(x,y, playerImages[0].get_width(), playerImages[0].get_height()) # creates a rect for the player
        self.playerRunCount = 999 # 999 signifies that player is not moving. if moving will be between 0 and 7
        self.runImagesDelay = 9 # how slow you want transitions from each running sprite
        self.velY = 0 # player y velocity
        self.grav = 0.2
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
        self.grav = 0.2 # y acceleration
        self.hit = False # whether fireball has hit a something other than the floor
        self.images = fireBallImages # images for fireball
        self.bounceSpeed = -2 # the y vel when fireball bounces
        self.delay = delay(8) # list of delay obj

    def move(self):

        hitDirection = {"top": False, "bottom": False, "left": False, "right": False} # the direction of the collison of fireball

        if not(self.hit):

            # first move by x vel
            self.rect.x += self.velX
            hitRect = collideRects(tileRects, self.rect)
            if len(hitRect) > 0:
                if self.facing == [0,1]:
                    hitDirection["right"] = True
                elif self.facing == [1, 0]:
                    hitDirection["left"] = True

            # move by y vel
            self.rect.y += self.velY
            hitRect = collideRects(tileRects, self.rect)
            if len(hitRect) > 0:
                if self.velY > 0:
                    hitDirection["bottom"] = True
                    self.rect.bottom = hitRect[0].top # so that the fireball isn't inside floor tile.
                else:
                    hitDirection["top"] = True

        if hitDirection["right"]:
            self.hit = True
        elif hitDirection["left"]:
            self.hit = True
        elif hitDirection["bottom"]:
            self.velY = self.bounceSpeed # bouncing effect
        elif hitDirection["top"]:
            self.velY = -self.velY # bounce off ceiling

        self.velY += self.grav

    def draw(self):
        if not(self.hit):
            if self.delay:
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
            self.rect = pygame.Rect((boss.rect.x + boss.rect.width), (boss.rect.y + boss.rect.height/5), self.length, self.length )
        elif boss.facing == [1,0]:
            self.rect = pygame.Rect((boss.rect.x - self.length), (boss.rect.y + boss.rect.height/5), self.length, self.length )
        xdif = (self.playerCentre[0] - self.rect.x)
        ydif = (self.playerCentre[1] - self.rect.y)
        self.speed = 1.1
        self.vel = [xdif/max(abs(xdif),abs(ydif))*self.speed, ydif/max(abs(xdif),abs(ydif))*self.speed] # [x vel, y vel]
        self.xTemp = 0 # since vel may be smaller than 1, vel added to xTemp until bigger than 1. then substracts 1
        self.yTemp = 0# since vel may be smaller than 1, vel added to yTemp until bigger than 1. then substracts 1

        self.hit = False

    def move(self):
        self.xTemp += self.vel[0]
        if abs(self.xTemp) >= 1:
            self.rect.x += self.xTemp
            self.xTemp = self.xTemp-1 if self.xTemp>=0 else self.xTemp+1

        self.yTemp += self.vel[1]
        if abs(self.yTemp) >= 1:
            self.rect.y += self.yTemp
            self.yTemp = self.yTemp - 1 if self.yTemp >= 0 else self.yTemp + 1

        if len(collideRects(tileRects,self.rect))>0 or self.rect.colliderect(player.playerRect):
            self.hit = True

    def draw(self):
        if not(self.hit):
            display.blit(self.image,(self.rect.x - cameraMove[0], self.rect.y - cameraMove[1]))



class bossHammer():
    def __init__(self,player,boss,image):

        self.player = player
        self.boss = boss
        self.playerCentre = [player.playerRect.centerx, player.playerRect.centery]
        self.image = image
        self.length = image[0].get_height()
        self.grav = 0.2
        self.animeCount = 0
        if boss.facing == [0, 1]:
            self.rect = pygame.Rect((boss.rect.x + boss.rect.width), (boss.rect.y + boss.rect.height / 3), self.length,
                                    self.length)
        else:
            self.rect = pygame.Rect((boss.rect.x - self.length), (boss.rect.y + boss.rect.height / 3), self.length,
                                    self.length)
        self.velY = -3
        # checktime give appropriate time and velY for hammer to go close/hit player
        self.time, self.velY = checktime(self.playerCentre[1],-self.grav,-self.velY,self.rect.y)
        self.velX = (self.playerCentre[0]-self.rect.x)/self.time
        self.hit = False
        self.delays = [delay(6)]

    def move(self):

        self.rect.x += self.velX
        self.rect.y += self.velY
        self.velY = self.velY + self.grav

        if len(collideRects(tileRects,self.rect))>0 or self.rect.colliderect(player.playerRect):
            self.hit = True

    def draw(self):

        if not(self.hit):
            if self.delays[0]:
                self.animeCount = (self.animeCount + 1) % len(self.image)

            display.blit(self.image[self.animeCount], (self.rect.x - cameraMove[0], self.rect.y - cameraMove[1]))


class boss():
    def __init__(self,x,y,player,sightRange,meleeRange,standImages,runImages,throwableImages):

        self.standImages = standImages
        self.runImages = runImages
        self.throwableImages = throwableImages
        self.player = player
        self.rect = pygame.Rect(x,y,standImages[0].get_width(), standImages[0].get_height())
        self.rangeRect = pygame.Rect(int(x-sightRange/2 + self.rect.width/2),int(y-sightRange/2 + self.rect.height/2),sightRange,sightRange)
        self.meleeRect = pygame.Rect(int(x-meleeRange/2 + self.rect.width/2),int(y-meleeRange/2 + self.rect.height/2),meleeRange,meleeRange)
        self.inRangeRect = False
        self.grav = 0.2
        self.moving = "left"
        self.runCount = 0
        self.runImagesDelay = 10  # how slow you want transitions from each running sprite
        self.hitDirection = {"top": False, "bottom": False, "left": False, "right": False}  # gives the direction of the collison
        self.facing = [1, 0]  # if [1,0], standing and facing left. if [0,1], standing and facing right
        self.fireBallList = [] # list of all fireball obj
        self.hammerThrowList = [] # list of all hammer obj
        self.moveCountMark = 40 # how long boss walks in each interval
        self.pauseCountMark = 60 # how long boss pauses
        self.powerThrowsMark = 3 # how many times boss throws in each burst
        self.moveCount = self.moveCountMark
        self.pauseCount = self.pauseCountMark
        self.powerThrows = 0
        self.velX = 1
        self.velY = 0
        self.powerFreq = 10 # time frame between each power use. the smaller,the burst is quicker
        self.currentPower = "" # power that is being used in the burst
        self.delays = [delay(self.runImagesDelay), delay(2), delay(self.powerFreq)]


    def scan(self,player): # checks to see if player in range rect. Boss will attack and follow player when in range

        self.rangeRect.x = self.rect.x - self.rangeRect.width/2 + self.standImages[0].get_width()/2
        self.rangeRect.y = self.rect.y - self.rangeRect.height/2 + self.standImages[0].get_height()/2
        if self.rangeRect.colliderect(player.playerRect):
            self.inRangeRect = True
            if self.meleeRect.colliderect(player.playerRect):
                pass
        else:
            self.inRangeRect = False

    def power(self,rand,currentPower = ""):

        # probability of each attack. If you want no attacks, make nothing equal to True.
        hammer = 50
        fire = 50
        nothing = False

        if currentPower == "":
            if not (nothing):
                if rand in range(0, hammer):
                    self.hammerThrowList.append(bossHammer(self.player, self, self.throwableImages[1]))
                    self.currentPower = "hammer"
                if rand in range(hammer, hammer + fire):
                    self.fireBallList.append(bossFireBall(self.player, self, self.throwableImages[0]))
                    self.currentPower = "fire"
        else:
            if self.currentPower == "hammer":
                self.hammerThrowList.append(bossHammer(self.player, self, self.throwableImages[1]))
            else:
                self.fireBallList.append(bossFireBall(self.player, self, self.throwableImages[0]))

    def move(self):

        self.scan(self.player)

        for fireball in self.fireBallList:
            fireball.move()
        for hammer in self.hammerThrowList:
            hammer.move()

        self.rect, self.hitDirection = move(self.rect, [0, self.velY], tileRects)
        self.velY += self.grav

        if self.velY > 4:
            self.velY = 4
        if self.moveCount > 0:

            if self.delays[0]:
                self.runCount = (self.runCount + 1) % 4
            if self.facing == [1,0]:
                self.moving = "left"
            else:
                self.moving = "rigth"

            if self.delays[1]:
                movement = [(-1 if self.facing == [1,0] else 1) * self.velX,0 ]
                self.rect, self.hitDirection = move(self.rect, movement, tileRects)
                self.moveCount -= 1
        else:

            self.moving = "standing"
            rand = random.randint(0, 100)

            if self.powerThrows > 0:
                if self.delays[2]:
                    self.power(rand,self.currentPower)
                    self.powerThrows -= 1

            if self.pauseCount > 0:
                self.pauseCount -= 1
            else:
                self.moveCount = self.moveCountMark
                self.pauseCount = self.pauseCountMark

                if self.inRangeRect:
                    if self.rect.centerx > player.playerRect.centerx:
                        rand = random.randint(51, 99)
                    else:
                        rand = random.randint(0, 49)

                if rand < 50:
                    self.facing = [0, 1]
                else:
                    self.facing = [1, 0]

                if self.inRangeRect:
                    self.powerThrows = self.powerThrowsMark
                    self.currentPower = ""

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
        self.tempCount = 0 # used to slow down animation.
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()) # rect for mBlock
        self.powerRect = pygame.Rect(self.x, self.y, 16, 16) # rect for power up

    def draw(self):

        if self.powerUp == "coin":
            self.tempCount += 1
            if self.hit and not(self.powerHit):
                if self.powerRect.y - 3> self.startY - 16:
                    display.blit(self.powerImage[(self.tempCount // 8) % 6], (self.powerRect.x-cameraMove[0], self.powerRect.y-cameraMove[1] - 3))
                    self.powerRect.y -= self.powerVelY
                else:
                    display.blit(self.powerImage[(self.tempCount // 8) % 6], (self.powerRect.x-cameraMove[0], self.powerRect.y-cameraMove[1] - 3))

        elif self.powerUp == "fireFlower":
            if self.hit and not(self.powerHit):
                if self.powerRect.y - 3> self.startY - 16:
                    display.blit(self.powerImage[(self.tempCount // 8) % 1], (self.powerRect.x-cameraMove[0], self.powerRect.y-cameraMove[1] - 3))
                    self.powerRect.y -= self.powerVelY
                else:
                    display.blit(self.powerImage[(self.tempCount // 8) % 1], (self.powerRect.x-cameraMove[0], self.powerRect.y-cameraMove[1] - 3))


        equ = lambda x: -(0.5*x**2-4)

        if self.hit and self.funcX > -1000:
            display.blit(self.image, (self.x -cameraMove[0], self.y - equ(self.funcX)-cameraMove[1]))

            if equ(self.funcX) < 0:
                self.funcX = -1001
            else:
                self.funcX += 0.2
        else:
            display.blit(self.image, (self.x-cameraMove[0], self.y-cameraMove[1] ))




player = player(30,44,playerImages,runImages,firePlayerImages,fireRunImages)
bowser = boss(450,40,player,250,25,bowserImages,bowserRunImages,bowserPowers)
enemyList = [enemies(92,112,90,220,1,goombaImages),
             enemies(128,192,112,175,1,goombaImages),
            enemies(250,32,235,285,1,goombaImages)]



fireBallList = [] # list of fireball objects
mBlockList = [] # list of mysteryBlock objects

delays = [delay(player.runImagesDelay)]
titletimer = 350 # amount of time controls at start are visible
monospace = pygame.font.SysFont("monospace", 8) # font type

global tileRects
tileRects = []



while True: #Main game loop

    display.fill((0,0,0)) # makes screen white

    # camera movements
    True_cameraMove[0] += (player.playerRect.x - cameraMove[0] - 148)/10
    True_cameraMove[1] += (player.playerRect.y - cameraMove[1] - 94)/10
    cameraMove = True_cameraMove.copy()
    cameraMove[0] = int(cameraMove[0])
    cameraMove[1] = int(cameraMove[1])

    if titletimer > 0: # controls appear at the start
        text = "use WASD to move. SPACE to use fireball when in firemode"
        label = monospace.render(text, 1, (0,0,0))
        display.blit(label, (30-cameraMove[0],  150-cameraMove[1]))
        titletimer -= 1


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
        #allow the animation to occur. Might fix this later on. Right now, its not a big bug.
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
                velY= -5
                
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

         # only transitions to next sprite when tempCount is 0.
        if delays[0]:
            player.playerRunCount += 1
            player.playerRunCount = player.playerRunCount % 4 # loops between 0 and 3, which have correspondin sprites in runImages list.
        player.facing = [0,1]  # signifies player is standing

    elif keys[K_a]:# when a is pressed, moves left
        player.movingLeft = True

         # only transitions to next sprite when tempCount is 0.
        if delays[0]:
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
            player.velY = -6 # makes the player move up.


    tileRects = []
    y = 0
    for row in gameMap: # builds the map
        x = 0
        for tile in row:
            if tile == '1': # ground block
                display.blit(groundBlock, (x * blockSize - cameraMove[0],y * blockSize - cameraMove[1]))
            if tile == '2': # brick block
                display.blit(brick, (x * blockSize - cameraMove[0], y * blockSize - cameraMove[1]))
            if tile == '3': # fire flower mystery block
                if gameMapCopy[y][x] != 1000:
                    mBlockList.append(mysteryB(x * blockSize , y * blockSize, mysteryBlock,"fireFlower",fireFlowerImages))
                gameMapCopy[y][x] = 1000
            if tile == '4': # coin mystery block
                if gameMapCopy[y][x] != 1000:
                    mBlockList.append(mysteryB(x * blockSize , y * blockSize, mysteryBlock,"coin",coinImages))
                gameMapCopy[y][x] = 1000
            if tile != '0': # empty space
                tileRects.append(pygame.Rect(x * blockSize , y * blockSize , blockSize, blockSize))
            x += 1
        y += 1


    # playerMovement is the intended movement
    playerMovement = [0, 0]

    # x direction movement
    if player.movingRight:
        playerMovement[0] += 2
    if player.movingLeft:
        playerMovement[0] -= 2


    playerMovement[1] += player.velY # y direction movement7y
    player.velY += player.grav # decreases the y velocity. when velY is +ive, player goes up. whe -ive, player goes down.

    #sets the y velocity to max 3.
    if player.velY > 4:
        player.velY = 4

    player.playerRect, player.hitDirection= move(player.playerRect, playerMovement, tileRects) # updates the player position and the collision direction

    #playerRect, enemyHit = move(playerRect, playerMovement, [goomba.rect])
    for enemy in enemyList:
        if enemy.squashed != True:
            player.velY, enemy.squashed = enemyCollide(player.playerRect, playerMovement, enemy.rect, player.velY)
        enemy.move()

    # moves all the fireball
    for fireball in fireBallList:
        fireball.move()
        for enemy in enemyList:
            if fireball.rect.colliderect(enemy.rect):
                enemy.squashed = True
                fireball.hit = True
                enemyList.remove(enemy)


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
        player.velY = 0
    if player.hitDirection['top']:
        player.velY = 0

    bowser.move()
    bowser.draw()
    player.draw(player.powerUp)

    for enemy in enemyList:
        enemy.draw()
    for mBlock in mBlockList:
        mBlock.draw()
    for ball in fireBallList:
        ball.draw()

    display.blit(test, (40 - cameraMove[0], 100 - cameraMove[1]))

    # makes boss range rect visible
    pygame.draw.rect(display,(255,0,0),pygame.Rect(bowser.rangeRect.x-cameraMove[0], bowser.rangeRect.y-cameraMove[1], bowser.rangeRect.width, bowser.rangeRect.width),1)

    # displays onto mainDisplay
    mainDisplay = pygame.transform.scale(display,WINDOW_SIZE)
    screen.blit(mainDisplay, (0,0))

    pygame.display.update() # update display
    clock.tick(60) # set frame rate


# Made by Avin Lanson