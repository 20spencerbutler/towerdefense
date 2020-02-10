import pygame, sys, random, time
from pygame.locals import *
pygame.init()


class Enemy:

    def __init__(self, _appearance, _animationTime, _speed, _health, _rect, _nodeArray):
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
        self.moveVector =[]


    def takeDamage(self, damageNum, effectArray):

        for effect in effectArray:
            haseffect = False
            for status in self.statusEffects:
                if effect == status:
                    haseffect = True
            if not haseffect:
                self.statusEffects.append(effect)

        self.health -= damageNum
        if self.health <= 0:
            return True
        return False

    def update(self):
        if self.distanceToNode - self.speed <= 0:
            if self.currentNodeIndex < len(self.nodeArray) - 1:
                self.rect.centerx = self.nodeArray[self.currentNodeIndex][0]
                self.rect.centery = self.nodeArray[self.currentNodeIndex][1]
                self.distanceToNode = (((self.nodeArray[self.currentNodeIndex][0] - self.nodeArray[self.currentNodeIndex + 1][0]) ** 2) + ((self.nodeArray[self.currentNodeIndex][1] - self.nodeArray[self.currentNodeIndex + 1][1]) ** 2)) ** 0.5
                self.moveVector = [(self.nodeArray[self.currentNodeIndex + 1][0] - self.nodeArray[self.currentNodeIndex][0]) / self.distanceToNode, (self.nodeArray[self.currentNodeIndex + 1][1] - self.nodeArray[self.currentNodeIndex][1]) / self.distanceToNode]
                self.currentNodeIndex += 1
                return False
            else:
                return True
        else:
            self.rect.move_ip(self.speed * self.moveVector[0], self.speed * self.moveVector[1])
            self.distanceToNode -= self.speed
            return False




