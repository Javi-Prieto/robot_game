from robots.models.potion import WaterPotion, Potion
from robots.models.wall import Wall
from robots.models.water import Water
import pygame

sprite = pygame.image.load("assets/PlayerSprites/PlayerFrontStay.png")
sprite_front = pygame.image.load("assets/PlayerSprites/PlayerFrontWalking.png")
sprite_back = pygame.image.load("assets/PlayerSprites/PlayerBackWalking.png")
sprite_right = pygame.image.load("assets/PlayerSprites/PlayerRightWalking.png")
sprite_left = pygame.image.load("assets/PlayerSprites/PlayerLeftWalking.png")
sprite_front_waterproof = pygame.image.load("assets/PlayerSprites/PlayerFrontWalkingWaterproof.png")
sprite_back_waterproof = pygame.image.load("assets/PlayerSprites/PlayerBackWalkingWaterproof.png")
sprite_left_waterproof = pygame.image.load("assets/PlayerSprites/PlayerLeftWalkingWaterproof.png")
sprite_right_waterproof = pygame.image.load("assets/PlayerSprites/PlayerRightWalkingWaterproof.png")


class Player:
    def __init__(self):
        self.position = [100, 60]
        self.speed = 1
        self.size = [50, 50]
        self.sprite = sprite
        self.life = 10
        self.isWaterproof = False

    def move_right(self):
        if self.isWaterproof:
            self.sprite = sprite_right_waterproof
        else:
            self.sprite = sprite_right
        self.position[0] += self.speed

    def move_left(self):
        if self.isWaterproof:
            self.sprite = sprite_left_waterproof
        else:
            self.sprite = sprite_left
        self.position[0] -= self.speed

    def move_up(self):
        if self.isWaterproof:
            self.sprite = sprite_back_waterproof
        else:
            self.sprite = sprite_back
        self.position[1] -= self.speed

    def move_down(self):
        if self.isWaterproof:
            self.sprite = sprite_front_waterproof
        else:
            self.sprite = sprite_front

        self.position[1] += self.speed

    def wall_collision(self, wall: Wall):
        match wall.looking_at:
            case 0:
                if self.position[1] <= wall.position[1] + wall.size[1]:
                    return True
            case 1:
                if self.position[1] >= wall.position[1] - wall.size[1]:
                    return True
            case 2:
                if self.position[0] <= wall.position[0] + wall.size[0]:
                    return True
            case 3:
                if self.position[0] >= wall.position[0] - wall.size[0]:
                    return True
            case _:
                return False
        return False

    def water_collision(self, water: Water):
        if self.isWaterproof:
            return False
        if water.position[0] <= self.position[0] <= water.position[0] + water.size[1] / 2 and water.position[1] - \
                water.size[1] / 2 <= self.position[1] <= water.position[1] + water.size[1] / 2:
            return True

    def collectable_collision(self, potion):
        if issubclass(potion.__class__, Potion):
            if potion.position[0] <= self.position[0] <= potion.position[0] + potion.size[1] / 2 and potion.position[
                1] - \
                    potion.size[1] / 2 <= self.position[1] <= potion.position[1] + potion.size[1] / 2:
                if isinstance(potion, WaterPotion):
                    potion.recollected = True
