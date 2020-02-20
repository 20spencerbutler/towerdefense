import pygame, sys
from pygame.locals import *
from ShopButton import ShopButton

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

class Shop():
    def __init__(self, _buttons):

        self.buttons = _buttons
        self.surface = pygame.display.set_mode((200, 600))
        self.mainButtons = []

        for i in self.buttons:
            if i.getType() == "Buy":
                self.mainButtons.append(i)
            elif i.getType() == "Upgrade":
                self.mainButtons.append(i)

        surface.fill(GRAY)
