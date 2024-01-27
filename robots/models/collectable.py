import pygame

water_png = pygame.image.load("assets/Collectable/water_proof_potion.png")
life_5_png = pygame.image.load("assets/Collectable/life_5_potion.png")
life_3_png = pygame.image.load("assets/Collectable/life_3_potion.png")
life_1_png = pygame.image.load("assets/Collectable/life_1_potion.png")


class Collectable:
    def __init__(self, sprite, position, size):
        self.sprite = sprite
        self.position = position
        self.size = size
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])


class WaterPotion(Collectable):
    def __init__(self, position):
        super().__init__(water_png, position, [42, 48])
        self.recollected = False


class LifePotion(Collectable):
    def __init__(self, sprite, position, size, healing):
        super().__init__(sprite, position, size)
        self.healing = healing


class Life5Potion(LifePotion):
    def __init__(self, position):
        super().__init__(life_5_png, position, [42, 48], 5)


class Life3Potion(LifePotion):
    def __init__(self, position):
        super().__init__(life_3_png, position, [42, 39], 3)


class Life1Potion(LifePotion):
    def __init__(self, position):
        super().__init__(life_1_png, position, [24, 36], 1)
