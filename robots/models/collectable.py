import pygame
import random

from robots.models.wall import Wall

water_png = pygame.image.load("assets/Collectable/water_proof_potion.png")
life_5_png = pygame.image.load("assets/Collectable/life_5_potion.png")
life_3_png = pygame.image.load("assets/Collectable/life_3_potion.png")
life_1_png = pygame.image.load("assets/Collectable/life_1_potion.png")
katana = pygame.image.load("assets/Collectable/katana.png")
bazooka = pygame.image.load("assets/Collectable/Bazooka.png")
desert_eagle = pygame.image.load("assets/Collectable/desert_eagle.png")
shuriken = pygame.image.load("assets/Collectable/shurikken.png")
bomb = pygame.image.load("assets/Collectable/bomb.png")


class Collectable:
    def __init__(self, sprite, position, size):
        self.sprite = sprite
        self.position = position
        self.size = size
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])
        self.recollected = False


def select_sprite():
    number = random.randint(0, 3)
    match number:
        case 0:
            return katana
        case 1:
            return bazooka
        case 2:
            return shuriken
        case 3:
            return shuriken
        case _:
            return katana


class WinnerObject(Collectable):
    def __init__(self, position):
        super().__init__(select_sprite(), position, [50, 50])


class Bomb(Collectable):
    def __init__(self, position):
        super().__init__(bomb, position, [50, 50])
        self.radius_damage = (self.position[0] - 50, self.position[1] - 50, self.size[0] * 3, self.size[1] * 3)

    def destroy_wall(self, wall):
        if isinstance(wall, Wall):
            self.radius_damage = (self.position[0] - 50, self.position[1] - 50, self.size[0] * 3, self.size[1] * 3)
            bomb_damage_radius_rect = pygame.Rect(self.radius_damage)
            wall_rect = pygame.Rect(wall.hitbox)
            return bomb_damage_radius_rect.colliderect(wall_rect)


class WaterPotion(Collectable):
    def __init__(self, position):
        super().__init__(water_png, position, [42, 48])


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
