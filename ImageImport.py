import pygame

def setColourKey(imagesList):
    for images in imagesList:
        if type(images) == list:
            for image in images:
                if type(image) == list:
                    for subImage in image:
                        subImage.set_colorkey((255, 255, 255))
                else:
                    image.set_colorkey((255,255,255))
        else:
            images.set_colorkey((255,255,255))



# size of player image
playerSize = [20,35]
bowserSize = [40,50]

# standing player sprite
playerImages = [pygame.transform.scale(pygame.image.load("sprites\marioset\standleft.png"), (playerSize[0], playerSize[0])),
                pygame.transform.scale(pygame.image.load("sprites\marioset\stand.png"), (playerSize[0], playerSize[0]))]
goombaSize = 13
test = pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaL.png"), (goombaSize, goombaSize))
test.set_colorkey((255,255,255))

# the player sprites for running
runImages = [
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1right.png"), (playerSize[0], playerSize[0])),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (playerSize[0], playerSize[0])),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3right.png"), (playerSize[0], playerSize[0])),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2right.png"), (playerSize[0], playerSize[0])),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run1left.png"), (playerSize[0], playerSize[0])),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (playerSize[0], playerSize[0])),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run3left.png"), (playerSize[0], playerSize[0])),
pygame.transform.scale(pygame.image.load(r"sprites\marioset\run2left.png"), (playerSize[0], playerSize[0]))
]



firePlayerImages = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireStand.png"), True, False), (playerSize[0], playerSize[1])),
                    pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireStand.png"), (playerSize[0], playerSize[1])),
                ]

bowserImages = [
                    pygame.transform.scale(pygame.image.load(r"sprites\enemies\bowserstandleft.PNG"), (bowserSize[0], bowserSize[1])),
                    pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\bowserstandleft.PNG"), True, False), (bowserSize[0], bowserSize[1]))
                ]

fireRunImages = [pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireRunRight1.PNG"), (playerSize[0], playerSize[1])),
                pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireRunRight2.PNG"), (playerSize[0], playerSize[1])),
                pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireRunRight1.PNG"), (playerSize[0], playerSize[1])),
                 pygame.transform.scale(pygame.image.load(r"sprites\marioset\fireRunRight3.PNG"), (playerSize[0], playerSize[1])),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireRunRight1.PNG"), True, False),(playerSize[0], playerSize[1])),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireRunRight2.PNG"), True, False),(playerSize[0], playerSize[1])),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireRunRight1.PNG"), True, False),(playerSize[0], playerSize[1])),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\marioset\fireRunRight3.PNG"), True, False),(playerSize[0], playerSize[1]))
                 ]
bowserRunImages = [pygame.transform.scale(pygame.image.load(r"sprites\enemies\runleft1.PNG"), (bowserSize[0], bowserSize[1])),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\runleft2.PNG"), (bowserSize[0], bowserSize[1])),
                 pygame.transform.scale(pygame.image.load(r"sprites\enemies\runleft3.PNG"), (bowserSize[0], bowserSize[1])),
                 pygame.transform.scale(pygame.image.load(r"sprites\enemies\runleft4.PNG"),(bowserSize[0], bowserSize[1])),

                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\runleft1.PNG"), True, False),(bowserSize[0], bowserSize[1])),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\runleft2.PNG"), True, False),(bowserSize[0], bowserSize[1])),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\runleft3.PNG"), True, False),(bowserSize[0], bowserSize[1])),
                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(r"sprites\enemies\runleft4.PNG"), True, False),(bowserSize[0], bowserSize[1]))
                 ]

bowserPowerSize = 14
bowserPowers = [pygame.transform.scale(pygame.image.load(r"sprites\interactables\Fire.PNG"), (bowserPowerSize, bowserPowerSize)),
                [pygame.transform.scale(pygame.image.load(r"sprites\interactables\bowserHammer1.PNG"), (bowserPowerSize, bowserPowerSize)),
                 pygame.transform.scale(pygame.image.load(r"sprites\interactables\bowserHammer2.PNG"), (bowserPowerSize, bowserPowerSize)),
                 pygame.transform.scale(pygame.image.load(r"sprites\interactables\bowserHammer3.PNG"), (bowserPowerSize, bowserPowerSize)),
                 pygame.transform.scale(pygame.image.load(r"sprites\interactables\bowserHammer4.PNG"), (bowserPowerSize, bowserPowerSize))]
                ]

coinImages = [
pygame.transform.scale(pygame.image.load(r"sprites\interactables\c1.png"),(16,16)),
pygame.transform.scale(pygame.image.load(r"sprites\interactables\c2.png"),(16,16)),
pygame.transform.scale(pygame.image.load(r"sprites\interactables\c3.png"),(16,16)),
pygame.transform.scale(pygame.image.load(r"sprites\interactables\c4.png"),(16,16)),
pygame.transform.scale(pygame.image.load(r"sprites\interactables\c5.png"),(16,16)),
pygame.transform.scale(pygame.image.load(r"sprites\interactables\c6.png"),(16,16))
]

goombaSize = 16
goombaImages = [pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaL.png"), (goombaSize, goombaSize)),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaR.png"), (goombaSize, goombaSize)),
                pygame.transform.scale(pygame.image.load(r"sprites\enemies\goombaSqa.png"), (goombaSize, goombaSize))]

fireFlowerImages = [pygame.transform.scale(pygame.image.load(r"sprites\interactables\fireflower.png"),(16,16))]

fireBallImages = pygame.image.load(r"sprites\interactables\fireBall.png")



blockSize = 16 #size of the blocks on map
groundBlock = pygame.transform.scale(pygame.image.load(r"sprites\blocks\groundBlock.png"), (blockSize, blockSize))
mysteryBlock = pygame.transform.scale(pygame.image.load(r"sprites\blocks\mysterybox.png"), (blockSize, blockSize))
brick = pygame.transform.scale(pygame.image.load(r"sprites\blocks\brick.png"), (blockSize, blockSize))

background = pygame.transform.scale(pygame.image.load(r"sprites\blocks\background.png"), (320, 192))

# removes most of the white in the background of images. but its not perfect
setColourKey([playerImages,runImages,firePlayerImages,bowserImages,
              fireRunImages,bowserRunImages,bowserPowers,coinImages,
              goombaImages,fireFlowerImages,fireBallImages,groundBlock,
              mysteryBlock,brick])