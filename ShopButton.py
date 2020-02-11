import pygame, sys
from pygame.locals import *
from pygame.font import *

GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

class ShopButton():
    def __init__(self, _cost, _name, _description, _type):

        pygame.font.init()
        self.cost = _cost
        self.name = _name
        self.description = _description
        self.type = _type
        self.display = pygame.Surface((800, 600))

        font = pygame.font.Font('freesansbold.ttf', 20)
        pygame.draw.rect(self.display, GRAY, (50, 200, 500, 200))
        pos = 220
        textSurfTitle, textRectTitle = makeText(self.name + ":", WHITE, GRAY, 50, 200, font)
        self.display.blit(textSurfTitle, textRectTitle)
        for line in self.description:
            textSurf, textRect = makeText(line, WHITE, GRAY, 50, pos, font)
            self.display.blit(textSurf, textRect)
            pos += 20
        if self.type[0] == "Buy":
            textSurfCost, textRectCost = makeText("Cost: " + (str)(self.cost), WHITE, GRAY, 50, 379, font)
            self.display.blit(textSurfCost, textRectCost)
        if self.type[0] == "Sell":
            textSurfSell, textRectSell = makeText("Sells For: " + (str)(self.cost), WHITE, GRAY, 50, 379, font)
            self.display.blit(textSurfSell, textRectSell)
        if self.type[0] == "Upgrade":
            textSurfUpgrade, textRectUpgrade = makeText("Upgrades For: " + (str)(self.cost), WHITE, GRAY, 50, 379, font)
            self.display.blit(textSurfUpgrade, textRectUpgrade)

def makeText(text, color, bgcolor, top, left, font):
    textSurf = font.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)
