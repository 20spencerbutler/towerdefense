from pygame.sprite import *
import math


class Projectile(pygame.sprite.Sprite):
    def __init__(self, _posX, _posY, _damage, _appearance, _movementSpeed, _effects):
        # "posX" and "posY" represent the position of the projectile
        # "effects" is a dictionary
        super().__init__()
        self.posX = _posX
        self.posY = _posY
        self.damage = _damage
        self.movementSpeed = _movementSpeed
        self.effects = _effects
        self.existenceTime = 0
        self.timeExisted = 0
        self.movement = [0, 0]

        #pygame.sprite.Sprite.__init__(_appearance)
        image = _appearance[0]
        imageSized = pygame.transform.scale(image, (10, 10))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(_posX, _posY))
        self.rect[0], self.rect[1] = self.posX, self.posY

    # def __del__(self):
    #     # deletes self
    #     print("object deleted")

    def update(self):
        #print(self.rect)
        # "vectorToMag" is a tuple containing the x and y components of the vector leading from tower sprite to enemy
        # "despawn" is a boolean that determines if the projectile should stop existing
        # sprite (top left coordinate)

        self.timeExisted += 1
        if self.timeExisted == self.existenceTime: return True
        #print(self.timeExisted, self.existenceTime)

        self.posX += self.movement[0]
        self.posY += self.movement[1]
        self.rect[0], self.rect[1] = self.posX, self.posY
        #print(self.rect)

        return False

    def retarget(self, vecToEnemy, towerRange):
        #print(self.rect, 'reeeet')
        # intended to designate where a projectile will go (motionVector), and for how long it must exist to get
        # there (extent of towerRange) called ONCE per projectile
        retProj = Projectile(self.posX, self.posY, self.damage, [self.image], self.movementSpeed, self.effects)
        retProj.timeExisted = 0
        retProj.existenceTime = math.ceil(towerRange / self.movementSpeed)

        unitMotion = self.makeMotionVector(vecToEnemy)
        retProj.movement = [unitMotion[0] * self.movementSpeed, unitMotion[1] * self.movementSpeed]
        return retProj

    def makeMotionVector(self, vectorToMag):
        # Makes a unit motion vector vectorToMag is a tuple containing the x and y components of the vector leading
        # from tower sprite to enemy sprite (top left coordinate)
        # for example, [2, 2] represents a vector 2 in x direction, 2 in y direction
        #print(vectorToMag)

        partialSum = 0
        for i in vectorToMag:
            partialSum += math.pow(i, 2)

        magnitude = math.sqrt(partialSum)
        return ((vectorToMag[0]/magnitude), (vectorToMag[1]/magnitude))
