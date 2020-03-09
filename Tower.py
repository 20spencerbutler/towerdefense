import copy

class Tower:

    def __init__(self, _range, _appearance, _fireRate, _projectile, _location , _shop):
        self.range = _range
        self.appearance = _appearance
        self.fireRate = _fireRate
        self.projectile = _projectile
        self.location = _location
        self.shop = _shop
        self.targetType = "FIRST"
        self.fireCooldown = 0

    def update(self, nearbyEnemies, targetingType):
        # if(len(nearbyEnemies) != 0):
        #     print(nearbyEnemies)
        canFire = False
        self.fireCooldown = max(self.fireCooldown - 1, 0)
        if self.fireCooldown == 0:
            #print('heyyyyy', nearbyEnemies)
            canFire = True
        if not len(nearbyEnemies) == 0:
            self.fireCooldown = self.fireRate
            if targetingType:
                self.targetType = targetingType
            mostCloseEnemy = None
            closeEnemyDistance = 1000000000
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
            elif self.targetType == "LAST":
                vectorToEnemy = [orderedEnemyArray[0].rect.centerx - self.location[0], orderedEnemyArray[0].rect.centery - self.location[1]]
            elif self.targetType == "FIRST":
                vectorToEnemy = [orderedEnemyArray[len(orderedEnemyArray)-1].rect.centerx - self.location[0], orderedEnemyArray[len(orderedEnemyArray)-1].rect.centery - self.location[1]]

            print(vectorToEnemy, '----', self.targetType)
            #vectorToEnemy = (500, 0)
            returndict = {
                "canFire": False,
                "shotFired": self.projectile.retarget(vectorToEnemy, self.range)
            }

            return returndict

        if not canFire:
            returndict = {
                "canFire": False,
                "shotFired": None
            }
            return returndict

        returndict = {
            'canFire': True,
            'shotFired': False
        }

        return returndict

    def upgrade(self):
        print("upgrade")