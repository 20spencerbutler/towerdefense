import math
from pygame import *
from pygame.sprite import *

class Projectile():
    def __init__(self, _posX, _posY, _damage, _appearance, _movementSpeed, _effects):
        # "posX" and "posY" represent the position of the projectile
        # "effects" is a dictionary

        self.posX = _posX
        self.posY = _posY
        self.damage = _damage
        self.movementSpeed = _movementSpeed
        self.effects = _effects
        self.existenceTime = 0
        self.timeExisted = 0

        pygame.sprite.Sprite.__init__(_appearance)
        image = pygame.image.load("sprite.png")
        imageSized = pygame.transform.scale(image, (100, 100))
        self.image = imageSized
        self.rect = self.image.get_rect(topleft=(_posX, _posY))

    def __del__(self):
        # deletes self
        print("object deleted")

    def update(self, vectorToMag, despawn):
        # "vectorToMag" is a tuple containing the x and y components of the vector leading from tower sprite to enemy
        # "despawn" is a boolean that determines if the projectile should stop existing
        # sprite (top left coordinate)

        if despawn is True:
            Projectile.__del__(self)

        moveX = vectorToMag[0]
        moveY = vectorToMag[1]

        Projectile.posX = moveX
        Projectile.posY = moveY

    def retarget(self, towerRange, movementSpeed):
        # intended to designate where a projectile will go (motionVector), and for how long it must exist to get
        # there (extent of towerRange) called ONCE per projectile

        Projectile.existenceTime = (towerRange / movementSpeed)

    def makeMotionVector(self, vectorToMag):
        # Makes a unit motion vector vectorToMag is a tuple containing the x and y components of the vector leading
        # from tower sprite to enemy sprite (top left coordinate)
        # for example, [2, 2] represents a vector 2 in x direction, 2 in y direction

        partialSum = 0
        for i in vectorToMag:
            partialSum += math.pow(i, 2)

        magnitude = math.sqrt(partialSum)
        return ((vectorToMag[0]/magnitude), (vectorToMag[1]/magnitude))
