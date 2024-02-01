import random
import pygame
import time

from robots.models.collectable import Bomb, WinnerObject, Life1Potion, WaterPotion, Life3Potion, Life5Potion
from robots.models.player import Player
from robots.models.wall import Wall
from robots.models.water import Water


class Game:
    def __init__(self):
        self.collected_bombs = []
        self.player = Player()
        self.object_list = []
        self.collectable_objects = []
        self.water_potions = []
        self.collectable_bombs = []
        self.number_bomb = 0
        self.number_potion_water = 0
        self.number_potion_l1 = 0
        self.number_potion_l3 = 0
        self.number_potion_l5 = 0
        self.number_diamond = 0
        self.running = True

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
                                self.number_bomb = int(save_dict[1])
                            case 'PW':
                                self.number_potion_water = int(save_dict[1])
                            case 'P1':
                                self.number_potion_l1 = int(save_dict[1])
                            case 'P3':
                                self.number_potion_l3 = int(save_dict[1])
                            case 'P5':
                                self.number_potion_l5 = int(save_dict[1])
                            case 'D':
                                self.number_diamond = int(save_dict[1])
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

    def get_nice_cords(self):
        x = random.randint(50, 750)
        y = random.randint(50, 550)
        x -= x % 50
        y -= y % 50
        for wall_water_object in self.object_list:
            while wall_water_object.position == [x, y]:
                x = random.randint(50, 750)
                y = random.randint(50, 550)
                x -= x % 50
                y -= y % 50
        return [x, y]

    def generate_collectable(self):
        self.load_map()
        for i in range(self.number_bomb + self.number_diamond + self.number_potion_l1 + self.number_potion_water
                       + self.number_potion_l3 + self.number_potion_l5):
            if i < self.number_bomb:
                self.collectable_bombs.append(Bomb(self.get_nice_cords()))
            elif i < self.number_bomb + self.number_diamond:
                self.collectable_objects.append(WinnerObject(self.get_nice_cords()))
            elif i < self.number_bomb + self.number_diamond + self.number_potion_l1:
                self.collectable_objects.append(Life1Potion(self.get_nice_cords()))
            elif i < self.number_bomb + self.number_diamond + self.number_potion_l1 + self.number_potion_water:
                self.water_potions.append(WaterPotion(self.get_nice_cords()))
            elif i < self.number_bomb + self.number_diamond + self.number_potion_l1 + self.number_potion_water + self.number_potion_l3:
                self.collectable_objects.append(Life3Potion(self.get_nice_cords()))
            else:
                self.collectable_objects.append(Life5Potion(self.get_nice_cords()))
        for collectable_object in self.collectable_objects:
            for i in self.collectable_objects:
                if not i == collectable_object:
                    while i.position == collectable_object.position:
                        collectable_object.position = self.get_nice_cords()
            for i in self.water_potions:
                while i.position == collectable_object.position:
                    collectable_object.position = self.get_nice_cords()
            for i in self.collectable_bombs:
                while i.position == collectable_object.position:
                    collectable_object.position = self.get_nice_cords()

    def check_player_life(self):
        if not self.player.life > 0:
            self.running = False

    def print_collectable(self, surface, screen):
        bomb_font = pygame.font.Font(None, 24)
        for collectable_object in self.collectable_objects:
            if not collectable_object.recollected:
                surface.blit(collectable_object.sprite, tuple(collectable_object.position))
            else:
                self.collectable_objects.remove(collectable_object)
        for water_potion in self.water_potions:
            if not water_potion.recollected:
                surface.blit(water_potion.sprite, tuple(water_potion.position))
        for bomb in self.collectable_bombs:
            if not bomb.recollected:
                surface.blit(bomb.sprite, tuple(bomb.position))
            else:
                self.collectable_bombs.remove(bomb)
                self.collected_bombs.append(bomb)
        for bomb in self.collected_bombs:
            bomb_png = water_potion_png = pygame.transform.scale(bomb.sprite, (28, 28))
            screen.blit(water_potion_png, (800 - 85, 11))
            bomb_number = bomb_font.render(str(len(self.collected_bombs)), False, (255, 255, 255))
            screen.blit(bomb_number, (800 - 90, 5))

    def load_ui(self, screen, surface):
        dp_face = pygame.image.load("assets/Screen/dp_face.png")
        font = pygame.font.Font(None, 50)
        heart_png = pygame.image.load("assets/heart.png")
        clock_png = pygame.image.load("assets/clock.png")
        bg = pygame.image.load("assets/background.jpg")
        quick_inventory_png = pygame.image.load("assets/Screen/quick_inventory.png")
        life_text = font.render('-----------------------', True, (0, 0, 0), (0, 0, 0))
        screen.blit(life_text, (40, 7))
        win_text = font.render('x ' + str(self.player.objects_recollected), False, (255, 255, 255))
        life_text = font.render('x ' + str(self.player.life), False, (255, 255, 255))
        screen.blit(life_text, (40, 7))
        screen.blit(win_text, (170, 7))
        screen.blit(quick_inventory_png, (800 - 96, 0))
        screen.blit(heart_png, (5, 10))
        screen.blit(dp_face, (115, 2))
        screen.blit(surface, (0, 50))
        surface.blit(bg, (0, 0))
    def game(self):
        self.generate_collectable()
        screen_height = 650
        surface_width = 800
        surface_height = 600
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((surface_width, screen_height))
        surface = pygame.Surface((surface_width, surface_height))
        collisioning = []
        is_moving_up = False
        is_moving_down = False
        is_moving_left = False
        is_moving_right = False
        is_water_potion_collected = False

        while self.running:
            clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_RIGHT:
                            is_moving_right = True
                        case pygame.K_LEFT:
                            is_moving_left = True
                        case pygame.K_UP:
                            is_moving_up = True
                        case pygame.K_DOWN:
                            is_moving_down = True
                        case pygame.K_t:
                            if is_water_potion_collected:
                                if self.player.isWaterproof:
                                    self.player.isWaterproof = False
                                else:
                                    self.player.isWaterproof = True
                        case pygame.K_b:
                            if not len(self.collected_bombs) == 0:
                                self.collected_bombs[-1].position = [
                                    self.player.position[0] - (self.player.position[0] % 50),
                                    self.player.position[1] - (self.player.position[1] % 50)]
                                surface.blit(self.collected_bombs[-1].sprite, tuple(self.player.position))
                                for collision_object in self.object_list:
                                    if self.collected_bombs[-1].destroy_wall(collision_object):
                                        self.object_list.remove(collision_object)
                                self.collected_bombs.remove(self.collected_bombs[-1])
                elif event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_RIGHT:
                            is_moving_right = False
                        case pygame.K_LEFT:
                            is_moving_left = False
                        case pygame.K_UP:
                            is_moving_up = False
                        case pygame.K_DOWN:
                            is_moving_down = False

            for collision_object in self.object_list:
                collisioning = self.player.wall_water_collision(collision_object)
                if collisioning[0]: break
            for bomb in self.collectable_bombs:
                self.player.collectable_collision(bomb)
            for collectable_object in self.collectable_objects:
                self.player.collectable_collision(collectable_object)
            if not is_water_potion_collected:
                for water_potion in self.water_potions:
                    self.player.collectable_collision(water_potion)
                    if water_potion.recollected:
                        is_water_potion_collected = True
            if not collisioning[0]:
                if is_moving_up:
                    self.player.move_up()
                elif is_moving_down:
                    self.player.move_down()
                elif is_moving_right:
                    self.player.move_right()
                elif is_moving_left:
                    self.player.move_left()
            else:
                if collisioning[1]:
                    if is_moving_up:
                        self.player.move_up()
                    elif is_moving_down:
                        self.player.move_down()
                    elif is_moving_right:
                        self.player.move_right()
                    elif is_moving_left:
                        self.player.move_left()
                    time.sleep(0.1)
                    self.player.life -= 1
                else:
                    time.sleep(0.1)
                    self.player.life -= 1
                    if is_moving_up:
                        self.player.move_down()
                    elif is_moving_down:
                        self.player.move_up()
                    elif is_moving_right:
                        self.player.move_left()
                    elif is_moving_left:
                        self.player.move_right()

            self.check_player_life()
            self.load_ui(screen, surface)

            for print_object in self.object_list:
                surface.blit(print_object.sprite, tuple(print_object.position))
            self.print_collectable(surface, screen)

            if is_water_potion_collected:
                water_potion_png = pygame.transform.scale(self.water_potions[-1].sprite, (21, 24))
                screen.blit(water_potion_png, (surface_width - 35, 13))
            surface.blit(self.player.sprite, (self.player.position[0], self.player.position[1]))
            if self.player.objects_recollected >= self.number_diamond:
                self.running = False
            pygame.display.flip()

        pygame.quit()
        exit(0)
