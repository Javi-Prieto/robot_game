from robots.models.collectable import WaterPotion, Collectable, Life1Potion, Life3Potion, Life5Potion, WinnerObject
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
    def __init__(self, position):
        self.position = position
        self.speed = 2
        self.size = [28, 38]
        self.sprite = sprite
        self.life = 10
        self.isWaterproof = False
        self.objects_recollected = 0
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])

    def move_right(self):
        if self.isWaterproof:
            self.sprite = sprite_right_waterproof
        else:
            self.sprite = sprite_right
        self.position[0] += self.speed
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])

    def move_left(self):
        if self.isWaterproof:
            self.sprite = sprite_left_waterproof
        else:
            self.sprite = sprite_left
        self.position[0] -= self.speed
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])

    def move_up(self):
        if self.isWaterproof:
            self.sprite = sprite_back_waterproof
        else:
            self.sprite = sprite_back
        self.position[1] -= self.speed
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])

    def move_down(self):
        if self.isWaterproof:
            self.sprite = sprite_front_waterproof
        else:
            self.sprite = sprite_front
        self.position[1] += self.speed
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])

    def water_collision(self, water: Water):
        player_rect = pygame.Rect(self.hitbox)
        water_rect = pygame.Rect(water.hitbox)
        if self.isWaterproof:
            return False
        return player_rect.colliderect(water_rect)

    def wall_collision(self, wall: Wall):
        player_rect = pygame.Rect(self.hitbox)
        wall_rect = pygame.Rect(wall.hitbox)
        return player_rect.colliderect(wall_rect)

    def wall_water_collision(self, collision_object):
        player_rect = pygame.Rect(self.hitbox)
        if isinstance(collision_object, Wall):
            object_rect = pygame.Rect(collision_object.hitbox)
            return [True, False] if player_rect.colliderect(object_rect) else [False, False]
        elif isinstance(collision_object, Water):
            object_rect = pygame.Rect(collision_object.hitbox)
            if self.isWaterproof: return [False, True]
            return [True, True] if player_rect.colliderect(object_rect) else [False, True]

    def collectable_collision(self, collectable):
        if issubclass(collectable.__class__, Collectable):
            player_rect = pygame.Rect(self.hitbox)
            collectable_rect = pygame.Rect(collectable.hitbox)
            if player_rect.colliderect(collectable_rect):
                if isinstance(collectable, Life1Potion):
                    self.life += 1
                elif isinstance(collectable, Life3Potion):
                    self.life += 3
                elif isinstance(collectable, Life5Potion):
                    self.life += 5
                elif isinstance(collectable, WinnerObject):
                    self.objects_recollected += 1
                collectable.recollected = True
