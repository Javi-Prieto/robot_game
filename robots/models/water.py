import pygame
water_block = pygame.image.load("assets/Obstacles/water_block.png")

class Water:
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.sprite = water_block