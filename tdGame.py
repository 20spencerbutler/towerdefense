import pygame, re, random
from Map import Map
from Projectile import Projectile
from Tower import Tower


aNumber = re.compile(r'\d+')

towerProps = (
    {
        'range': 100,
        'appearance': pygame.image.load('Tiles/A.png'),
        'fireRate': 20,
        'projectile': {
            'damage': 10,
            'appearance': [pygame.image.load('Tiles/B.png')],
            'speed': 30,
            'effects': False
        },
        'shop': False
    }
)

enemyProps = (
    {
        'appearance': pygame.image.load('Tiles/B.png'),
        'animTime': 0,
        'speed': 10,
        'hp': 10
    }
)

class writerMine:
    def __init__(self, fonter = 't'):
        self.fonts = []
        for i in range(0, 100):
            self.fonts.append(i)
            #print(i)
        self.fontuse = fonter

    def addFont(self, size):
        self.fonts[size - 1] = pygame.font.SysFont(self.fontuse, size)

    def write(self, size, text):
        #print(str(size) + ', ' + text)
        text = str(text)
        if self.fonts[size - 1] == size - 1: self.addFont(size)
        disper = self.fonts[size - 1].render(text, True, (255, 255 , 255))
        return disper

def isBounded(low, val, hi,):
    return val >= low and val <= hi

class Game():
    def __init__(self, mapUse, startingLives, startingMoney, shopDefault):
        self.menuBoundary = 800
        self.money = startingMoney
        self.lives = startingLives
        self.map = mapUse
        self.towers = []
        self.towerCanFire = []
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.display = pygame.Surface(1000, 1000)
        self.display.blit(pygame.transform.scale(self.map.getSurface(), self.menuBoundary, self.menuBoundary), (0, 0))
        self.shopNormal = shopDefault
        self.shop = self.shopNormal
        self.towerShopOpen = -1
        self.buyingTower = False
        self.printer = writerMine('')
        rawNodes = self.map.nodes
        self.useNodes = []
        for i in rawNodes:
            vals = aNumber.findall(i)
            if len(vals) < 2:
                next()
            self.useNodes.append((vals[0], vals[1]))


    def bottomMenu(self, hoverSurface = False):
        menuSurf = pygame.Surface(1000 - self.menuBoundary, self.menuBoundary)
        menuSurf.blit(self.printer.write(self.money, 20), (50, 50))
        menuSurf.blit(self.printer.write(self.lives, 20), (550, 50))
        if(hoverSurface): menuSurf.blit(pygame.scalehoverSurface, (600, 0))
        return menuSurf


    def gameTick(self, mousePos):
        mx, my = mousePos[0], mousePos[1]
        dispNow = pygame.Surface(1000, 1000)
        dispNow.blit(self.display, (0, 0))
        for tower in range(0, len(self.towers)):
            dispNow.blit(tower.appearance, (tower.location[0], tower.location[1]))
            enemiesInRange = []
            if(self.towerCanFire[tower]):
                rangeSprite = pygame.sprite.Sprite()
                rangeSprite.rect = (self.towers[tower].location[0], self.towers[tower].location[1], 1, 1)
                rangeSprite.radius = self.towers[tower].range
                enemiesInRange = pygame.sprite.spritecollide(rangeSprite, self.enemies,
                                                             False, pygame.sprite.collide_circle()
                                                             ).sprites()
            retNow = self.towers[tower].update(enemiesInRange, False)
            self.towerCanFire[tower] = retNow['canFire']
            if retNow['shotFired']:
                self.projectiles.add(retNow['shotFired'])

        for enemy in self.enemies:
            hasCompleted = enemy.update()
            if hasCompleted:
                print('enemy got through')
                self.lives -= 1
            else:
                dispNow.blit(enemy.appearance, (enemy.rect[0], enemy.rect[1]))

        for projectile in self.projectiles:
            projectile.update()
            enemyHit = pygame.sprite.spritecollide(projectile, self.enemies)
            if enemyHit:
                enemyHit[0].takeDamage(projectile.damage, projectile.effects)
                if('aoe' in projectile.effects):
                    for a in range(1, len(enemyHit)):
                        enemyHit[a].takeDamage(projectile.damage, projectile.effects)

                self.projectiles.remove(projectile)
            else:
                dispNow.blit(projectile.appearance, (projectile.rect[0], projectile.rect[1]))

        if self.buyingTower:
            r = self.rangeOfBuying
            rangeSurf = pygame.Surface((2 * r, 2 * r), pygame.SRCALPHA)
            rangeSurf.fill((0, 0, 0, 0))
            pygame.draw.circle(rangeSurf, (200, 0, 0, .5), (r / 2, r / 2), r)
            dispNow.blit(rangeSurf, (mx + r, my + r))

        dispNow.blit(pygame.transform.scale(self.shop.getSurface(), (1000 - self.menuBoundary, 1000)), (self.menuBoundary, 0))
        if(mx > self.menuBoundary):
            buttonHovered = self.shop.click((mx - self.menuBoundary, y))
            if(buttonHovered):
                currentHoverSurface = buttonHovered.description
        dispNow.blit(self.bottomMenu(currentHoverSurface), (0, self.menuBoundary))
        inter = random.randint(0, 10)
        if inter == 0:
            self.spawnEnemy(0)

        return dispNow

    def handleClick(self, position):
        x, y = position[0], position[1]
        for tower in range(0, len(self.towers)):
            if isBounded(tower.position[0], x, tower.position[0] + 50) and isBounded(tower.position[1], y, tower.position[1] + 50):
                self.shop = self.towers[tower].shop
                self.towerShopOpen = tower
                return

        if isBounded(self.menuBoundary, x, self.display.get_width()):
            buttonClicked = self.shop.click((x - self.menuBoundary, y))
            if buttonClicked:
                type = buttonClicked.onClick()
                if not type:
                    return
                if type[0] == 'sell':
                    self.towers.pop(self.towerShopOpen)
                    self.shop = self.shopNormal
                    self.towerShopOpen = -1
                    self.money += 1

                if type[0] == 'upgrade':
                    self.towers[self.towerShopOpen].upgrade()

                if type[0] == 'buyTower':
                    s = towerProps[type[1]]
                    self.buyingTower = True
                    self.rangeOfBuying = s['range']
                    self.towerBuying = type[1]

        if self.buyingTower:
            self.buildTower(self.towerBuying, (x, y))

        self.buyingTower = False
        self.shop = self.shopNormal
        self.towerShopOpen = -1

    def buildTower(self, tower, loc):
        s = towerProps[tower]
        t = s['projectile']
        self.towers.append(
            Tower(s['range'], s['appearance'], s['fireRate'],
                  Projectile(loc[0], loc[1], t['damage'], t['appearance'], t['speed'], t['effects']),
                  (loc[0], loc[1]), s['shop']))

    def spawnEnemy(self, eI):
        en = enemyProps[eI]
        self.enemies.add(en['appearance'], en['animTime'], en['speed'], en['hp'], (self.useNodes[0][0], self.useNodes[0][1]), self.useNodes)

