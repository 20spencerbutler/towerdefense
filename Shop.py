import pygame, sys
from pygame.locals import *
from ShopButton import ShopButton

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

class Shop():
    def __init__(self, _buttons):

        self.buttons = _buttons
        self.surface = pygame.Surface((200, 600))
        self.mainButtons = []
        self.mainButtonsPos = []
        self.otherButtons = []
        self.otherButtonsPos = []

        for i in self.buttons:
            if i.getType()[0] == "Buy":
                self.mainButtons.append(i)
            elif i.getType()[0] == "Upgrade":
                self.mainButtons.append(i)
            else:
                self.otherButtons.append(i)

        self.surface.fill(GRAY)
        yPos = 0
        odd = True

        for x in self.mainButtons:
            if odd:
                self.surface.blit(x.getIcon(), (35, yPos))
                odd = False
                coordinate = [35, yPos]
                self.mainButtonsPos.append(coordinate)
            else:
                self.surface.blit(x.getIcon(), (105, yPos))
                yPos += 65
                odd = True
                coordinate = [105, yPos]
                self.mainButtonsPos.append(coordinate)

        odd = True
        yPos = 540

        for y in self.otherButtons:
            if odd:
                self.surface.blit(y.getIcon(), (35, yPos))
                odd = False
                coordinate = [35, yPos]
                self.otherButtonsPos.append(coordinate)
            else:
                self.surface.blit(y.getIcon(), (105, yPos))
                yPos -= 65
                odd = True
                coordinate = [105, yPos]
                self.otherButtonsPos.append(coordinate)

    def click(self, coordinates):
        for x in self.mainButtonsPos:
            if coordinates[0] >= x[0] and coordinates[0] < x[0] + 60 and coordinates[1] >= x[1] and coordinates[1] < x[1] + 60:
                return self.mainButtons[x]
        for y in self.otherButtonsPos:
            if coordinates[0] >= y[0] and coordiantes[0] < y[0] + 60 and coordinates[1] >= y[1] and coordinates[1] < y[1] + 60:
                return self.otherButtons[y]
        return False

    def getSurface(self):
        return self.surface

buttonOne = ShopButton(255, "Blaster", "The blaster blasts things.", ["Buy", "Attack Tower"])
buttonTwo = ShopButton(255, "Gun", "The gun shoots things.", ["Buy", "Attack Tower"])
buttonThree = ShopButton(255, "Upgrade Blaster", "This upgrades the blaster.", ["Upgrade", "Tower Upgrade"])
buttonFour = ShopButton(255, "Upgrade Gun", "This upgrades the gun.", ["Upgrade", "Tower Upgrade"])
buttonFive = ShopButton(255, "Sell Blaster", "This sells the blaster.", ["Sell", "Tower Sell"])
buttonSix = ShopButton(255, "Sell Gun", "This sells the gun.", ["Sell", "Tower Sell"])
buttons = [buttonOne, buttonTwo, buttonThree, buttonFour, buttonFive, buttonSix]
winco = Shop(buttons)
print(winco.click((40, 10)))
print(winco.click((40, 200)))

