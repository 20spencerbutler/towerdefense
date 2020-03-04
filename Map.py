import pygame

class Map():
    def __init__(self, _tileMap, _nodes):
        #print(_tileMap, '---------------')
        with open(_tileMap) as mapOne: 
            linesOne = [line.split() for line in mapOne]
        
        with open(_nodes) as nodesOne:
            linesTwo = [line.split() for line in nodesOne]
            
        self.display = pygame.Surface((800, 600))
        self.tileMap = []
        tileSize = 30
        for x in range(len(linesOne)):
            self.tileMap.append(linesOne[x])
        self.nodes = []
        for x in range(len(linesTwo)):
            self.nodes.append(linesTwo[x])
        drawX = 0
        for x in self.tileMap:
            drawY = 0
            for y in x:
                if y == "A":
                    windows = pygame.image.load('Tiles/GrassSprite.png')
                    self.display.blit(windows, [drawY, drawX])
                if y == "B":
                    windows = pygame.image.load('Tiles/water.png')
                    self.display.blit(windows, [drawY, drawX])
                drawY += tileSize
            drawX += tileSize

    def getSurface(self):
        return self.display


myMap = Map('BloonsMapOne.txt', 'BloonsNodesOne.txt')
surface = myMap.getSurface()
