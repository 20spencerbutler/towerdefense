import pygame, sys, random, time
from pygame.locals import *
from ShopButton import ShopButton
from Shop import Shop
from tdGame import Game
from Menu import Menu
from Map import Map
#pygame.init()

basicTowerShop = Shop([
    ShopButton(0, 'Sell', 'Sells Tower', ('Sell')),
    ShopButton(0, 'Target First', 'Targets First Enemy', ('retarget', 0)),
    ShopButton(0, 'Target Last', 'Targets Last Enemy', ('retarget', 1)),
    ShopButton(0, 'Target Closest', 'Targets Closest Enemy', ('retarget', 2))
])

towerProps = (
    {
        'cost': 20,
        'name': 'Tower Chungus',
        'desc': 'Chungus Tower',
        'range': 100,
        'appearance': pygame.image.load('Tiles/firsttower.png'),
        'fireRate': 20,
        'projectile': {
            'damage': 10,
            'appearance': [pygame.image.load('Tiles/hadouken.png')],
            'speed': 30,
            'effects': {'slow': 30, 'aoe': 5}
        },
        'shop': basicTowerShop
    },
    {
        'cost': 20,
        'name': 'Tower Chungus',
        'desc': 'Chungus Tower',
        'range': 100,
        'appearance': pygame.image.load('Tiles/firsttower.png'),
        'fireRate': 20,
        'projectile': {
            'damage': 10,
            'appearance': [pygame.image.load('Tiles/hadouken.png')],
            'speed': 30,
            'effects': False
        },
        'shop': basicTowerShop
    }
)

enemyProps = (
    {
        'appearance': pygame.image.load('Tiles/antsprite 1.png'),
        'animTime': 0,
        'speed': 10,
        'hp': 10,
        'bounty': 5
    },
    {
        'appearance': pygame.image.load('Tiles/spidersprite.png'),
        'animTime': 0,
        'speed': 10,
        'hp': 50,
        'bounty': 20
    }
)

shopButtons = []
for i in range(0, len(towerProps)):
    #print(towerProps)
    t = towerProps[i]
    shopButtons.append(ShopButton(t['cost'], t['name'], t['desc'], ('Buy', i)))

mainShop = Shop(shopButtons)

def main():
    global WINDOWWIDTH, WINDOWHEIGHT, DISPLAYSURF, ISGAME
    WINDOWWIDTH = 1000
    WINDOWHEIGHT = 1000
    FPS = 8
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
    ISGAME = False
    mousepos = None
    runningGame = None
    gameMenu = Menu()
    isClick = False

    counterPostA = 0

    while True:
        if runningGame is not None:
            counterPostA += 1
        FPSCLOCK.tick(FPS)
        pygame.display.update()
        isClick = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                WINDOWWIDTH = event.w
                WINDOWHEIGHT = event.h
                DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
                DISPLAYSURF.fill(pygame.Color('BLACK'))
            elif event.type == MOUSEBUTTONUP:
                isClick = True
            mousepos = pygame.mouse.get_pos()
        if ISGAME:
            mousepos = gameClick(mousepos)
            dispLastTick = runningGame.gameTick(mousepos)
            if mousepos[0] >= 0 and mousepos[0] <= 1000 and mousepos[1] >= 0 and mousepos[1] <= 1000 and isClick:
                runningGame.handleClick(mousepos)
            drawSurface(dispLastTick)
        else:
            mousepos = gameClick(mousepos)
            if mousepos[0] >= 0 and mousepos[0] <= 1000 and mousepos[1] >= 0 and mousepos[1] <= 1000 and isClick:
                #print('ooy')
                if gameMenu.mapSelected(mousepos):
                    #print('HYEYEEY')
                    runningGame = Game(gameMenu.mapSelected(mousepos), 10, 100, mainShop, towerProps, enemyProps)
                    ISGAME = True
            drawSurface(gameMenu.display)

        # STUFF DEALING WITH ENEMY WAVES
        # 50 tick gaps of no enemies
        # With each new wave, wave lasts 20 ticks longer
        # With each new wave, gap between waves lasts 20 ticks longer
        # Enemies spawn faster and stronger at various intervals
        if runningGame is not None:
            enemyList = [0, 1]

            if counterPostA % 10 == 0 and counterPostA <= 30: # 30, 50
                runningGame.spawnEnemy(enemyList[0])

            if counterPostA % 10 == 0 and 80 < counterPostA <= 130: # 50, 70
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 2:
                    temp2 = enemyList[0]
                elif temp < 2:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            if counterPostA % 10 == 0 and 200 < counterPostA <= 270: # 70, 90
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 5:
                    temp2 = enemyList[0]
                elif temp < 5:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            if counterPostA % 5 == 0 and 360 < counterPostA: # 90, 110
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 2:
                    temp2 = enemyList[0]
                elif temp < 2:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)


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

main()
