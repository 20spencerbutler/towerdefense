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

        display = Surface((1000, 1000))
        display.fill(BLACK)
        displayWidth = 1000

        BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

        mapText = "Please select the map you'd like to play on."
        theMapText = BASICFONT.render(mapText, True, WHITE)
        display.blit(theMapText, ((displayWidth / 10), (displayWidth / 10)))

        for a in range(0, 3):
            for b in range(0, 4):
                menuRect = pygame.draw.rect(display, LIGHTGRAY, ((10 + (b * 200), 10 + (a * 200), 200, 200)))
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
                    print(self.mapArr[counter], '//////////')
                    miniMap = Map(self.mapArr[counter], self.nodeArr[counter])
                    miniMapSurf = miniMap.getSurface()
                    miniMapSurfResized = pygame.transform.scale(miniMapSurf, (200, 200))
                    display.blit(miniMapSurfResized, (10 + (b * 200), 10 + (a * 200), 200, 200))
                    counter += 1

    def mapSelected(self, mousePos):
        # mousePos represents the location of a mouse click
        theMap = None

        for a in range(len(self.mapArr)):
            if self.board[a].collidepoint(
                    mousePos):
                theMap = Map.__init__(self, self.mapArr[a], self.nodeArr[a])

        return theMap
