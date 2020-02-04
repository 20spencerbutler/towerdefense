import pygame

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

    def gameTick(self):
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
            enemyHit = pygame.sprite.spritecollideany(projectile, self.enemies)
            if enemyHit:
                enemyHit[0].takeDamage(projectile.damage, projectile.effects)
                self.projectiles.remove(projectile)
            else:
                dispNow.blit(projectile.appearance, (projectile.rect[0], projectile.rect[1]))



        return dispNow

    def handleClick(self, position):
        x, y = position[0], position[1]
        for tower in self.towers:
            if isBounded(tower.position[0], x, tower.position[0] + 50) and isBounded(tower.position[1], y, tower.position[1] + 50):
                self.shop = tower.shop
                return

        if isBounded(self.menuBoundary, x, self.display.get_width()):
            buttonClicked = self.shop.click((x - self.menuBoundary, y))
            if buttonClicked:
                type = buttonClicked.onClick()
                if not type:
                    return
                











