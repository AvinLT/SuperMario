import pygame, sys
import random
import copy
from fractions import Fraction
from pygame.locals import *

a = pygame.Rect(100,144-28, 10, 10)
c = pygame.image.load(r"sprites\interactables\c1.png")

"""import cmath

a = 1
b = 2
c = 1
d = (b**2) - (4*a*c)
sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)
rand = 1 if random.randint(0,100) < 50 else -1"""

def checktime(yPos,acel,yVel,yTarg):
    tot = 0
    count = 0
    if yTarg < yPos:
        while yPos + tot > yTarg:
            tot += yVel
            yVel += acel
            count += 1
    else:
        while yPos + tot < yTarg:
            tot += yVel
            yVel += acel
            count += 1
    return count

#print(checktime(0,-1,5,9))

def checktime2(yPos,acel,yVel,yTarg):
    tot = 0
    count = 0
    lock = True
    stop = False
    yVelMark = copy.deepcopy(yVel)
    if yTarg < yPos:
        while yPos + tot > yTarg:
            tot += yVel
            yVel += acel
            count += 1
    else:
        while not(stop):
            count += 1
            tot += yVel
            yVel += acel
            if yPos + tot >= yTarg:
                lock = False
            if not(lock):
                if yPos + tot + yVel <= yTarg and yVel < 0:
                    stop = True

            if count > 100:
                return checktime2(yPos, acel, yVelMark + 3, yTarg)

    return count,-yVelMark

#print(checktime2(0,-1,5,9))

class test():
    def __init__(self):
        self.t = 4
    def __bool__(self):
        if self.t % 2 == 0:
            return True
        else:
            return False

a = [1,2,3,4]
print(a)
a.remove(3)
print(a)
