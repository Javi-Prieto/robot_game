from robots.models.collectable import WaterPotion, Collectable
from robots.models.wall import Wall, Side_wall
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
        self.size = [28, 38]
        self.sprite = sprite
        self.life = 10
        self.isWaterproof = False
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])

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

    def side_wall_collision(self, wall: Side_wall):
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
        player_rect = pygame.Rect(self.hitbox)
        water_rect = pygame.Rect(water.hitbox)
        if self.isWaterproof:
            return False
        return player_rect.colliderect(water_rect)

    def wall_collision(self, wall: Wall):
        player_rect = pygame.Rect(self.hitbox)
        wall_rect = pygame.Rect(wall.hitbox)
        return player_rect.colliderect(wall_rect)

    def collectable_collision(self, collectable):
        if issubclass(collectable.__class__, Collectable):
            player_rect = pygame.Rect(self.hitbox)
            collectable_rect = pygame.Rect(collectable.hitbox)
            if player_rect.colliderect(collectable_rect):
                if isinstance(collectable, WaterPotion):
                    collectable.recollected = True
