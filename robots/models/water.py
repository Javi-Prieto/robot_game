import pygame
water_block = pygame.image.load("assets/Obstacles/water_block.png")

class Water:
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.sprite = water_block
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])