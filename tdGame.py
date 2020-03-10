import pygame, re, random
from Map import Map
from Projectile import Projectile
from Shop import Shop
from ShopButton import ShopButton
from Tower import Tower
from EnemyClass import Enemy


aNumber = re.compile(r'\d+')

class writerMine:
    def __init__(self, fonter = 't'):
        self.fonts = []
        for i in range(0, 100):
            self.fonts.append(i)
            #print(i)
        self.fontuse = fonter

    def addFont(self, size):
        self.fonts[size - 1] = pygame.font.SysFont(self.fontuse, size)
        #print(size, '--------------')

    def write(self, size, text):
        #print(str(size) + ', ' + text)
        text = str(text)
        if self.fonts[size - 1] == size - 1: self.addFont(size)
        #print(self.fonts[size - 1], size, text)
        disper = self.fonts[size - 1].render(text, True, (255, 255 , 255))
        return disper

def isBounded(low, val, hi,):
    return val >= low and val <= hi

class Game():
    def __init__(self, mapUse, startingLives, startingMoney, shopDefault, tp, ep):
        self.menuBoundary = 800
        self.money = startingMoney
        self.lives = startingLives
        self.map = mapUse
        self.towers = []
        self.towerCanFire = []
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.display = pygame.Surface((1000, 1000))
        self.display.blit(pygame.transform.scale(self.map.getSurface(), (self.menuBoundary, self.menuBoundary)), (0, 0))
        self.shopNormal = shopDefault
        self.shop = self.shopNormal
        self.towerShopOpen = -1
        self.buyingTower = False
        self.printer = writerMine('')
        self.towerProps = tp
        self.enemyProps = ep
        rawNodes = self.map.nodes
        self.useNodes = []
        for i in rawNodes:
            teste = i[0] + i[1]
            #print(i)
            vals = aNumber.findall(teste)
            if len(vals) < 2:
                next()
            self.useNodes.append((int(vals[0]) * 30, int(vals[1]) * 30))


    def bottomMenu(self, hoverSurface = False):
        menuSurf = pygame.Surface((1000 - self.menuBoundary, self.menuBoundary))
        menuSurf.blit(self.printer.write(20, self.money), (50, 50))
        menuSurf.blit(self.printer.write(20, self.lives), (550, 50))
        if(hoverSurface): menuSurf.blit(hoverSurface, (600, 1000 - self.menuBoundary))
        return menuSurf


    def gameTick(self, mousePos):
        #print('heyyya! gametick!')
        mx, my = mousePos[0], mousePos[1]
        dispNow = pygame.Surface((1000, 1000))
        dispNow.blit(self.display, (0, 0))
        for tower in range(0, len(self.towers)):
            dispNow.blit(self.towers[tower].appearance, (self.towers[tower].location[0], self.towers[tower].location[1]))
            enemiesInRange = []
            if(self.towerCanFire[tower]):
                rangeSprite = pygame.sprite.Sprite()
                rangeSprite.rect = pygame.Rect(self.towers[tower].location[0], self.towers[tower].location[1], 1, 1)
                rangeSprite.radius = self.towers[tower].range
                enemiesInRange = pygame.sprite.spritecollide(rangeSprite, self.enemies,
                                                             False, pygame.sprite.collide_circle
                                                             )
            retNow = self.towers[tower].update(enemiesInRange, False)
            self.towerCanFire[tower] = retNow['canFire']
            if retNow['shotFired']:
                #print('heyyyy')
                self.projectiles.add(retNow['shotFired'])

        for enemy in self.enemies:
            hasCompleted = enemy.update()
            if hasCompleted:
                #print('enemy got through')
                self.lives -= 1
                self.enemies.remove(enemy)
            else:
                dispNow.blit(enemy.appearance, (enemy.rect[0], enemy.rect[1]))

        for projectile in self.projectiles:
            if projectile.update():
                projectile.kill()
            enemyHit = pygame.sprite.spritecollide(projectile, self.enemies, False)
            if enemyHit:
                wasHit = enemyHit[0].takeDamage(projectile.damage, projectile.effects)
                if(wasHit):
                    enemyHit[0].kill()
                    self.money += wasHit
                if(projectile.effects):
                    #print('t', projectile.effects)
                    if('aoe' in projectile.effects):
                        for a in range(1, len(enemyHit)):
                            wasHit = enemyHit[a].takeDamage(projectile.damage, projectile.effects)
                            if(wasHit):
                                enemyHit[a].kill()
                                self.money += wasHit

                self.projectiles.remove(projectile)
            else:
                dispNow.blit(projectile.image, (projectile.rect[0], projectile.rect[1]))

        if self.buyingTower:
            r = int(self.rangeOfBuying)
            #print(r)
            rangeSurf = pygame.Surface((2 * r, 2 * r), pygame.SRCALPHA)
            rangeSurf.fill((0, 0, 0, 0))
            pygame.draw.circle(rangeSurf, (200, 0, 0, .5), (int(r / 2), int(r / 2)), r)
            dispNow.blit(rangeSurf, (mx + r, my + r))

        #dispNow.blit(pygame.transform.scale(self.shop.getSurface(), (1000 - self.menuBoundary, 1000)), (self.menuBoundary, 0))
        dispNow.blit(self.shop.getSurface(), (self.menuBoundary, 0))

        currentHoverSurface = False
        if(mx > self.menuBoundary):
            buttonHovered = self.shop.click((mx - self.menuBoundary, my))
            if(buttonHovered):
                currentHoverSurface = buttonHovered.getDescription()
        dispNow.blit(self.bottomMenu(currentHoverSurface), (0, self.menuBoundary))
        inter = random.randint(0, 40)
        if inter == 0:
            self.spawnEnemy(0)

        #print(self.lives)
        if(self.lives < 1):
            return 'lost!'
        return dispNow

    def handleClick(self, position):
        x, y = position[0], position[1]
        for tower in range(0, len(self.towers)):
            if isBounded(self.towers[tower].location[0], x, self.towers[tower].location[0] + 50) and isBounded(self.towers[tower].location[1], y, self.towers[tower].location[1] + 50):
                self.shop = self.towers[tower].shop
                self.towerShopOpen = tower
                return

        if isBounded(self.menuBoundary, x, self.display.get_width()):
            #print(x - self.menuBoundary, y)
            buttonClicked = self.shop.click((x - self.menuBoundary, y))
            if buttonClicked:
                buttonClicked.switchClick()
                pygame.display.update()
                type = buttonClicked.onClick(self.money)
                #print('hey man', type)
                if not type:
                    return

                if type[0] == 'Sell':
                    self.towers.pop(self.towerShopOpen)
                    self.shop = self.shopNormal
                    self.towerShopOpen = -1
                    self.money += 1

                if type[0] == 'upgrade':
                    self.towers[self.towerShopOpen].upgrade()

                if type[0] == 'Buy':
                    #print('buyin')
                    s = self.towerProps[type[1]]
                    self.buyingTower = True
                    self.rangeOfBuying = s['range']
                    self.towerBuying = type[1]

                return

        if self.buyingTower and isBounded(0, x, self.menuBoundary) and isBounded(0, y, self.menuBoundary):
            print(x, self.menuBoundary, y)
            self.buildTower(self.towerBuying, (x, y))

        self.buyingTower = False
        self.shop = self.shopNormal
        self.towerShopOpen = -1

    def buildTower(self, tower, loc):
        s = self.towerProps[tower]
        t = s['projectile']
        self.towers.append(
            Tower(s['range'], s['appearance'], s['fireRate'],
                  Projectile(loc[0], loc[1], t['damage'], t['appearance'], t['speed'], t['effects']),
                  (loc[0], loc[1]), s['shop']))
        self.money -= s['cost']
        self.towerCanFire.append(False)

    def spawnEnemy(self, eI):
        #print('hey lol', self.useNodes)
        en = self.enemyProps[eI]
        self.enemies.add(Enemy(en['appearance'], en['animTime'], en['speed'], en['hp'], pygame.Rect(self.useNodes[0][0], self.useNodes[0][1], 50, 50), self.useNodes, en['bounty']))
