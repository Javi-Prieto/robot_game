import pygame
from robots.models.player import Player
from robots.models.wall import Wall
from robots.models.water import Water


class Game():
    def __init__(self):
        self.player = Player()
        self.object_list = []
        self.collectable_objects = []
        self.water_potions = []
        self.bombs = []

    def load_map(self):
        mid_wall = pygame.image.load("assets/Obstacles/wall_block.png")
        with open('assets/MAP.txt', 'r') as file:
            x_point = 0
            y_point = 0
            result_line = []
            save_dict = []
            for line in file:
                if line[0] != 'M':
                    result_line = line.split(',')
                    for chac in result_line:
                        save_dict = chac.split(':')
                        match save_dict[0]:
                            case 'B':
                                number_bomb = int(save_dict[1])
                            case 'PW':
                                number_potion_water = int(save_dict[1])
                            case 'P1':
                                number_potion_l1 = int(save_dict[1])
                            case 'P3':
                                number_potion_l3 = int(save_dict[1])
                            case 'P5':
                                number_potion_l5 = int(save_dict[1])
                            case 'D':
                                number_diamond = int(save_dict[1])
                else:
                    result_line = line.split('|')
                    result_line.pop(-1)
                    x_point = 0
                    for chac in result_line:
                        match chac:
                            case 'M':
                                self.object_list.append(Wall(mid_wall, [x_point, y_point], [50, 50]))
                            case 'A':
                                self.object_list.append(Water([x_point, y_point], [50, 50]))
                        x_point += 50
                    y_point += 50
