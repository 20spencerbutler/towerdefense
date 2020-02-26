import pygame, sys
from pygame.locals import *
from pygame.font import *

GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class ShopButton():
    def __init__(self, _cost, _name, _description, _type):

        pygame.font.init()
        self.cost = _cost
        self.name = _name
        self.description = _description
        self.type = _type
        self.display = pygame.Surface((800, 600))
        self.icon = pygame.Surface((60, 60))

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

        iconFont = pygame.font.Font('freesansbold.ttf', 10)
        self.icon.fill(BLACK)
        self.iconName = []
        start = 0
        for i in range (len(self.name)):
            if self.name[i] == " ":
                item = self.name[start:i]
                self.iconName.append(item)
                start = i + 1
            elif i == len(self.name) - 1:
                item = self.name[start:i + 1]
                self.iconName.append(item)
        yPos = 10
        for i in self.iconName:
            textSurf, textRect = makeText(i, WHITE, BLACK, 10, yPos, iconFont)
            yPos += 10
            self.icon.blit(textSurf, textRect)

    def onClick(self, bank):
        if bank < self.cost:
            return False
        else:
            return self.type[0]

    def getDescription(self):
        return self.display

    def getIcon(self):
        return self.icon
    
    def getType(self):
        return self.type

def makeText(text, color, bgcolor, top, left, font):
    textSurf = font.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)