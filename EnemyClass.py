import pygame, math
from pygame.locals import *
#pygame.init()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, _appearance, _animationTime, _speed, _health, _rect, _nodeArray, _bounty):
        super().__init__()
        self.appearance = _appearance
        self.animationTime = _animationTime
        self.animationTicks = 0
        self.statusEffects = []
        self.speed = _speed
        self.health = _health
        self.rect = _rect
        self.nodeArray = _nodeArray
        self.currentNodeIndex = 0
        self.distanceToNode = 0
        self.moveVector = []
        self.bounty = _bounty
        self.partialSpeed = 0


    def takeDamage(self, damageNum, effectArray):
        if effectArray:
            for effect in effectArray:
                haseffect = False
                for status in self.statusEffects:
                    if effect == status:
                        haseffect = True
                if not haseffect:
                    self.statusEffects.append(effect)

        self.health -= damageNum
        if self.health <= 0:
            #print('enemy got zapped')
            return self.bounty
        return False

    def update(self):
        hasPartialed = 0
        if(self.partialSpeed >= 1):
            hasPartialed = math.floor(self.partialSpeed)
            self.speed += hasPartialed
            self.partialSpeed -= hasPartialed
            #print(hasPartialed, '))))')
        #print(hasPartialed, '(((((')
        if self.distanceToNode - self.speed <= 0:
            #print('t')
            if self.currentNodeIndex < len(self.nodeArray) - 1:
                self.rect.centerx = self.nodeArray[self.currentNodeIndex][0]
                self.rect.centery = self.nodeArray[self.currentNodeIndex][1]
                self.distanceToNode = (((self.nodeArray[self.currentNodeIndex][0] - self.nodeArray[self.currentNodeIndex + 1][0]) ** 2) + ((self.nodeArray[self.currentNodeIndex][1] - self.nodeArray[self.currentNodeIndex + 1][1]) ** 2)) ** 0.5
                self.moveVector = [(self.nodeArray[self.currentNodeIndex + 1][0] - self.nodeArray[self.currentNodeIndex][0]) / self.distanceToNode, (self.nodeArray[self.currentNodeIndex + 1][1] - self.nodeArray[self.currentNodeIndex][1]) / self.distanceToNode]
                self.currentNodeIndex += 1
                self.speed -= hasPartialed
                return False
            else:
                self.speed -= hasPartialed
                return True
        else:
            self.rect.move_ip(self.speed * self.moveVector[0], self.speed * self.moveVector[1])
            distMoved = math.sqrt(math.floor(self.speed * self.moveVector[0]) ** 2 + math.floor(self.speed * self.moveVector[1]) ** 2)
            self.distanceToNode -= distMoved
            self.partialSpeed += self.speed - distMoved
            #print(self.partialSpeed, self.speed)
            self.speed -= hasPartialed
            return False





