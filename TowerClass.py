import pygame, sys, random, time
from pygame.locals import *
pygame.init()


class BaseTower:

    def __init__(self, _range, _appearance, _fireRate, _projectile, _location , _shop):
        self.range = _range
        self.appearance = _appearance
        self.fireRate = _fireRate
        self.projectile = _projectile
        self.location = _location
        self.shop = _shop
        self.targetType = "FIRST"
        self.upgradetype = "RATE"

    def update(self, nearbyEnemies, targetingType):
        if len(nearbyEnemies) == 0:
            canfire = False
        else:
            canfire = True
            if not targetingType:
                self.targetType = targetingType
            mostCloseEnemy = None
            closeEnemyDistance = (self.location[0] - nearbyEnemies[0].rect.centerx)**2 + (self.location[1] - nearbyEnemies[0].rect.centery)
            orderedEnemyArray = []
            vectorToEnemy = []
            for enemy in nearbyEnemies:
                if self.targetType == "CLOSE" and (self.location[0] - enemy.rect.centerx)**2 + (self.location[1] - enemy.rect.centery) < closeEnemyDistance:
                    closeEnemyDistance = (self.location[0] - enemy.rect.centerx)**2 + (self.location[1] - enemy.rect.centery)
                    mostCloseEnemy = enemy
                if self.targetType == "FIRST" or self.targetType == "LAST":
                    if len(orderedEnemyArray) == 0:
                        orderedEnemyArray.append(enemy)
                    else:
                        for x in range(0, len(orderedEnemyArray)):
                            if enemy.currentNodeIndex < orderedEnemyArray[x].currentNodeIndex:
                                orderedEnemyArray.insert(x, enemy)
                                break
                            elif enemy.currentNodeIndex == orderedEnemyArray[x].currentNodeIndex and enemy.distanceToNode > orderedEnemyArray[x].distanceToNode:
                                orderedEnemyArray.insert(x, enemy)
                                break
                            elif x == len(orderedEnemyArray) - 1:
                                orderedEnemyArray.append(enemy)
            if self.targetType == "CLOSE":
                vectorToEnemy = [mostCloseEnemy.rect.centerx - self.location[0], mostCloseEnemy.rect.centery - self.location[1]]
            elif self.targetType == "FIRST":
                vectorToEnemy = [orderedEnemyArray[0].rect.centerx - self.location[0], orderedEnemyArray[0].rect.centery - self.location[1]]
            elif self.targetType == "LAST":
                vectorToEnemy = [orderedEnemyArray[len(orderedEnemyArray)-1].rect.centerx - self.location[0], orderedEnemyArray[len(orderedEnemyArray)-1].rect.centery - self.location[1]]

        if not canfire:
            returndict = {
                "canFire": False,
                "shotFired": None
            }
            return returndict
        returndict = {
            "canFire": True,
            "shotFired": self.projectile.retarget(vectorToEnemy, self.range)
        }
        return returndict

    def upgrade(self):
        if self.upgradetype == "RATE":
            self.fireRate = 0.9 * self.fireRate
            self.upgradetype = "DMG"
        elif self.upgradetype == "DMG":
            self.projectile.upgradeDamage()
            self.upgradetype = "RATE"









