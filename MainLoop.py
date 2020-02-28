import pygame, sys, random, time
from pygame.locals import *
pygame.init()


def main():
    global WINDOWWIDTH, WINDOWHEIGHT, DISPLAYSURF, ISGAME
    WINDOWWIDTH = 1000
    WINDOWHEIGHT = 1000
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
    ISGAME = False
    mousepos = None
    runningGame = None
    gameMenu = Menu()
    isClick = False
    while True:
        isClick = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                WINDOWWIDTH = event.w
                WINDOWHEIGHT = event.h
                DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
                DISPLAYSURF.fill(BLACK)
            elif event.type == MOUSEBUTTONUP:
                isClick = True
            mousepos = pygame.mouse.get_pos()
        if ISGAME:
            mousepos = gameClick(mousepos)
            runningGame.gameTick(mousepos)
            if mousepos[0] >= 0 and mousepos[0] <= 1000 and mousepos[1] >= 0 and mousepos[1] <= 1000 and isClick:
                runningGame.handleClick(mousepos)
            drawSurface(runningGame.display)
        else:
            mousepos = gameClick(mousepos)
            if mousepos[0] >= 0 and mousepos[0] <= 1000 and mousepos[1] >= 0 and mousepos[1] <= 1000 and isClick:
                if gameMenu.mapSelected(mousepos):
                    runningGame = Game(gameMenu.mapSelected(mousepos), 10, 100, Shop("intitalization inputs"))
                    ISGAME = True
            drawSurface(gameMenu.display)







def drawSurface(drawSurf):

    global DISPLAYSURF
    if WINDOWWIDTH > WINDOWHEIGHT:
        blitsurf = pygame.transform.scale(drawSurf, (WINDOWHEIGHT, WINDOWHEIGHT))
        DISPLAYSURF.blit(blitsurf, (WINDOWWIDTH/2 - WINDOWHEIGHT/2, 0))
    else:
        blitsurf = pygame.transform.scale(drawSurf, (WINDOWWIDTH, WINDOWWIDTH))
        DISPLAYSURF.blit(blitsurf, (0, WINDOWHEIGHT / 2 - WINDOWWIDTH / 2))


def gameClick(_click):
    global WINDOWWIDTH, WINDOWHEIGHT
    if WINDOWWIDTH > WINDOWHEIGHT:
        return ((_click[0] - (WINDOWWIDTH/2 - WINDOWHEIGHT/2)) * (1000 / WINDOWHEIGHT), _click[1] * (1000 / WINDOWHEIGHT))
    else:
        return (_click[0] * (1000/WINDOWWIDTH), (_click[1] - (WINDOWHEIGHT / 2 - WINDOWWIDTH / 2)) * (1000/WINDOWWIDTH))


