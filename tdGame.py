import pygame

class Game():
    def __init__(self, mapUse, startingLives, startingMoney):
        self.money = startingMoney
        self.lives = startingLives
        self.map = mapUse
        self.towers = []
        self.towerCanFire = []
        self.enemies = []
        self.projectiles = []
        self.display = pygame.Surface(1000, 1000)

    def gameTick(self):
        for tower in range(0, len(self.towers)):
            retNow = self.towers[tower].update([])
            self.towerCanFire[tower] = retNow['canFire']
            if retNow['shotFired']:
                self.projectiles.add(retNow['shotFired'])

        for enemy in self.enemies:
            enemy.update()

        for projectile in self.projectiles:
            projectile.update()

