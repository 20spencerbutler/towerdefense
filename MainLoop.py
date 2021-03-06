import pygame, sys, random, time
from pygame.locals import *
from ShopButton import ShopButton
from Shop import Shop
from tdGame import Game
from Menu import Menu
from Map import Map
#pygame.init()

basicTowerShop = Shop([
    ShopButton(0, 'Sell', 'Sells Tower', ('Sell', False)),
    ShopButton(0, 'Target First', 'Targets First Enemy', ('retarget', 0)),
    ShopButton(0, 'Target Last', 'Targets Last Enemy', ('retarget', 1)),
    ShopButton(0, 'Target Closest', 'Targets Closest Enemy', ('retarget', 2))
])

towerProps = (
    {
        'cost': 20,
        'name': 'Cannon Tower',
        'desc': 'Cannon Tower',
        'range': 100,
        'appearance': pygame.image.load('Tiles/cannon.png'),
        'fireRate': 100,
        'projectile': {
            'damage': 10,
            'appearance': [pygame.image.load('Tiles/hadouken.png')],
            'speed': 6,
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
        'fireRate': 100,
        'projectile': {
            'damage': 10,
            'appearance': [pygame.image.load('Tiles/hadouken.png')],
            'speed': 6,
            'effects': False
        },
        'shop': basicTowerShop
    }
)

enemyProps = (
    {
        'appearance': pygame.image.load('Tiles/antsprite 1.png'),
        'animTime': 0,
        'speed': 2,
        'hp': 10,
        'bounty': 5
    },
    {
        'appearance': pygame.image.load('Tiles/spidersprite.png'),
        'animTime': 0,
        'speed': 2,
        'hp': 50,
        'bounty': 20
    },
    {
        'appearance': pygame.image.load('Tiles/waspsprite.png'),
        'animTime': 0,
        'speed': 6,
        'hp': 30,
        'bounty': 50
    },
    {
        'appearance': pygame.image.load('Tiles/pixil-frame-0.png'),
        'animTime': 0,
        'speed': 0.5,
        'hp': 1500,
        'bounty': 100
    }


)

shopButtons = []
for i in range(0, len(towerProps)):
    #print(towerProps)
    t = towerProps[i]
    shopButtons.append(ShopButton(t['cost'], t['name'], t['desc'], ('Buy', i)))

mainShop = Shop(shopButtons)

bigFont = pygame.font.SysFont('Comic Sans MS', 50)

def main():
    global WINDOWWIDTH, WINDOWHEIGHT, DISPLAYSURF, ISGAME, BIGFONT
    WINDOWWIDTH = 1000
    WINDOWHEIGHT = 1000
    FPS = 40
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
    ISGAME = False
    hasLost = False
    mousepos = None
    runningGame = None
    gameMenu = Menu()
    isClick = False

    counterPostA = 0

    while True:
        if runningGame is not None:
            counterPostA += 1
        #print(counterPostA)
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
            if dispLastTick == 'lost!':
                drawSurface(bigFont.render('You lose!!', True, (255, 255, 255)))
                ISGAME = False
                hasLost = True
            else:
                drawSurface(dispLastTick)
        elif (hasLost):
            drawSurface(bigFont.render('You lose!!', True, (255, 255, 255)))
            if isClick:
                hasLost = False
            #drawSurface(dispLastTick)
        else:
            mousepos = gameClick(mousepos)
            if mousepos[0] >= 0 and mousepos[0] <= 1000 and mousepos[1] >= 0 and mousepos[1] <= 1000 and isClick:
                #print('ooy')
                if gameMenu.mapSelected(mousepos):
                    #print('HYEYEEY')
                    runningGame = Game(gameMenu.mapSelected(mousepos), 1000, 100, mainShop, towerProps, enemyProps)
                    ISGAME = True
            drawSurface(gameMenu.display)

        # STUFF DEALING WITH ENEMY WAVES
        # 50 tick gaps of no enemies
        # With each new wave, wave lasts 20 ticks longer
        # With each new wave, gap between waves lasts 20 ticks longer
        # Enemies spawn faster and stronger at various intervals
        if runningGame is not None:
            enemyList = [0, 1]

            # WAVE 1
            if counterPostA % 20 == 0 and counterPostA <= 30: # 300, 50 - (wave duration, time between waves)
                runningGame.spawnEnemy(enemyList[0])

            # WAVE 2
            if counterPostA % 20 == 0 and 330 < counterPostA <= 380: # 320, 70
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 2:
                    temp2 = enemyList[0]
                elif temp < 2:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            # WAVE 3
            if counterPostA % 20 == 0 and 700 < counterPostA <= 770: # 340, 90
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 5:
                    temp2 = enemyList[0]
                elif temp < 5:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            # WAVE 4
            if counterPostA % 10 == 0 and 1040 < counterPostA <= 1130: # 360, 110
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 2:
                    temp2 = enemyList[0]
                elif temp < 2:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            # WAVE 5
            if counterPostA % 10 == 0 and 1400 < counterPostA <= 1510: # 380, 130
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 5:
                    temp2 = enemyList[0]
                elif temp < 5:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            # WAVE 6
            if counterPostA % 10 == 0 and 1890 < counterPostA <= 2020: # 400, 150
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 8:
                    temp2 = enemyList[0]
                elif temp < 8:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            # WAVE 7
            if counterPostA % 10 == 0 and 2420 < counterPostA <= 2570: # 420, 170
                temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            # WAVE 8
            if counterPostA % 5 == 0 and 2990 < counterPostA <= 3160: # 440, 190
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 5:
                    temp2 = enemyList[0]
                elif temp < 5:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            # WAVE 9
            if counterPostA % 5 == 0 and 3600 < counterPostA <= 3790: # 460, 210
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 8:
                    temp2 = enemyList[0]
                elif temp < 8:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            # WAVE 10
            if counterPostA % 5 == 0 and 4250 < counterPostA <= 4460:  # 480, 230
                temp2 = None
                temp = random.randint(0, 10)
                if temp >= 8:
                        temp2 = enemyList[0]
                elif temp < 8:
                    temp2 = enemyList[1]
                runningGame.spawnEnemy(temp2)

            # WAVE 11
            if counterPostA % 1 == 0 and 4940 < counterPostA:  # 480, 230
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
