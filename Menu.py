from pygame import *
from pygame.sprite import *
from Map import Map

# Color setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGRAY = (160, 160, 160)


class Menu():
    def __init__(self):

        _board = []

        self.display = Surface((1000, 1000))
        self.display.fill(BLACK)
        self.displayWidth = 1000

        BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

        mapText = "Please select the map you'd like to play on."
        theMapText = BASICFONT.render(mapText, True, WHITE)
        self.display.blit(theMapText, ((self.displayWidth / 10), (self.displayWidth / 10)))

        for a in range(0, 3):
            for b in range(0, 4):
                menuRect = pygame.draw.rect(self.display, LIGHTGRAY, ((10 + (b * 200), 10 + (a * 200), 200, 200)))
                _board.append(menuRect)

        self.board = _board

        # draws in mini-versions of maps - MORE SHOULD BE ADDED LATER

        self.mapArr = []
        self.nodeArr = []

        map1 = "BloonsMapOne.txt"
        self.mapArr.append(map1)

        nodes1 = "BloonsNodesOne.txt"
        self.nodeArr.append(nodes1)

        counter = 0
        counter_limit = len(self.mapArr)
        for a in range(0, 3):
            for b in range(0, 4):
                if counter < counter_limit:
                    #print(self.mapArr[counter], '//////////')
                    miniMap = Map(self.mapArr[counter], self.nodeArr[counter])
                    miniMapSurf = miniMap.getSurface()
                    miniMapSurfResized = pygame.transform.scale(miniMapSurf, (200, 200))
                    self.display.blit(miniMapSurfResized, (10 + (b * 200), 10 + (a * 200), 200, 200))
                    counter += 1

    def mapSelected(self, mousePos):
        # mousePos represents the location of a mouse click
        theMap = None
        print(mousePos)
        for a in range(len(self.mapArr)):
            if self.board[a].collidepoint(
                    mousePos):
                theMap = Map(self.mapArr[a], self.nodeArr[a])
        print(theMap)
        return theMap
