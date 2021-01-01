import pygame, sys
import random
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

print(checktime(0,-2,10,25))
