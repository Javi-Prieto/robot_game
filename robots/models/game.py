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
        self.collected_bombs_2 = []
        self.player = Player([100, 100])
        self.player_2 = Player([500, 500])
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
            self.generate_finish_game_1(False)

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
                self.generate_finish_game_1(True)
            pygame.display.flip()

        pygame.quit()
        exit(0)

    def load_ui_1v1(self, screen, surface):
        dp_face = pygame.image.load("assets/Screen/dp_face.png")
        font = pygame.font.Font(None, 50)
        heart_png = pygame.image.load("assets/heart.png")
        clock_png = pygame.image.load("assets/clock.png")
        bg = pygame.image.load("assets/background.jpg")
        quick_inventory_png = pygame.image.load("assets/Screen/quick_inventory.png")
        quick_inventory_png_2 = pygame.image.load("assets/Screen/quick_inventory_2.png")
        life_text = font.render('------------------------------------------------------', True, (0, 0, 0), (0, 0, 0))
        screen.blit(life_text, (40, 7))
        win_text = font.render('x ' + str(self.player.objects_recollected), False, (255, 255, 255))
        life_text = font.render('x ' + str(self.player.life), False, (255, 255, 255))
        win_text_2 = font.render('x ' + str(self.player_2.objects_recollected), False, (255, 255, 255))
        life_text_2 = font.render('x ' + str(self.player_2.life), False, (255, 255, 255))
        screen.blit(life_text, (40, 7))
        screen.blit(win_text, (170, 7))
        screen.blit(life_text_2, (435, 7))
        screen.blit(win_text_2, (565, 7))
        screen.blit(quick_inventory_png, (250, 0))
        screen.blit(quick_inventory_png_2, (645, 0))
        screen.blit(heart_png, (5, 10))
        screen.blit(heart_png, (400, 10))
        screen.blit(dp_face, (115, 2))
        screen.blit(dp_face, (510, 2))
        screen.blit(surface, (0, 50))
        surface.blit(bg, (0, 0))

    def print_collectable_1v1(self, surface, screen):
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
            surface.blit(bomb.sprite, tuple(bomb.position))
        for bomb in self.collected_bombs:
            bomb_png = pygame.transform.scale(bomb.sprite, (28, 28))
            screen.blit(bomb_png, (258, 11))
            bomb_number = bomb_font.render(str(len(self.collected_bombs)), False, (255, 255, 255))
            screen.blit(bomb_number, (258, 5))
        for bomb in self.collected_bombs_2:
            bomb_png = pygame.transform.scale(bomb.sprite, (28, 28))
            screen.blit(bomb_png, (653, 11))
            bomb_number = bomb_font.render(str(len(self.collected_bombs_2)), False, (255, 255, 255))
            screen.blit(bomb_number, (653, 5))

    def check_player_life_1v1(self):
        if not self.player.life > 0:
            self.generate_finish_game_1v1(2)
        if not self.player_2.life > 0:
            self.generate_finish_game_1v1(1)

    def game_1v1(self):
        self.generate_collectable()
        if self.number_diamond % 2 == 0:
            self.number_diamond += 1
        screen_height = 650
        surface_width = 800
        surface_height = 600
        clock = pygame.time.Clock()
        water_potion_png = self.water_potions[-1].sprite
        screen = pygame.display.set_mode((surface_width, screen_height))
        surface = pygame.Surface((surface_width, surface_height))
        collisioning = []
        collisioning_2 = []
        is_1_moving_up = False
        is_1_moving_down = False
        is_1_moving_left = False
        is_1_moving_right = False
        is_2_moving_up = False
        is_2_moving_down = False
        is_2_moving_left = False
        is_2_moving_right = False
        is_water_potion_collected_1 = False
        is_water_potion_collected_2 = False
        while self.running:
            clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_RIGHT:
                            is_1_moving_right = True
                        case pygame.K_LEFT:
                            is_1_moving_left = True
                        case pygame.K_UP:
                            is_1_moving_up = True
                        case pygame.K_DOWN:
                            is_1_moving_down = True
                        case pygame.K_w:
                            is_2_moving_up = True
                        case pygame.K_s:
                            is_2_moving_down = True
                        case pygame.K_d:
                            is_2_moving_right = True
                        case pygame.K_a:
                            is_2_moving_left = True
                        case pygame.K_t:
                            if is_water_potion_collected_1:
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
                        case pygame.K_q:
                            if not len(self.collected_bombs_2) == 0:
                                self.collected_bombs_2[-1].position = [
                                    self.player_2.position[0] - (self.player_2.position[0] % 50),
                                    self.player_2.position[1] - (self.player_2.position[1] % 50)]
                                surface.blit(self.collected_bombs_2[-1].sprite, tuple(self.player_2.position))
                                for collision_object in self.object_list:
                                    if self.collected_bombs_2[-1].destroy_wall(collision_object):
                                        self.object_list.remove(collision_object)
                                self.collected_bombs_2.remove(self.collected_bombs_2[-1])
                        case pygame.K_e:
                            if is_water_potion_collected_2:
                                if self.player_2.isWaterproof:
                                    self.player_2.isWaterproof = False
                                else:
                                    self.player_2.isWaterproof = True
                elif event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_RIGHT:
                            is_1_moving_right = False
                        case pygame.K_LEFT:
                            is_1_moving_left = False
                        case pygame.K_UP:
                            is_1_moving_up = False
                        case pygame.K_DOWN:
                            is_1_moving_down = False
                        case pygame.K_w:
                            is_2_moving_up = False
                        case pygame.K_s:
                            is_2_moving_down = False
                        case pygame.K_d:
                            is_2_moving_right = False
                        case pygame.K_a:
                            is_2_moving_left = False

            for collision_object in self.object_list:
                collisioning = self.player.wall_water_collision(collision_object)
                if collisioning[0]: break
            for collision_object in self.object_list:
                collisioning_2 = self.player_2.wall_water_collision(collision_object)
                if collisioning_2[0]: break
            for bomb in self.collectable_bombs:
                self.player.collectable_collision(bomb)
                if bomb.recollected:
                    self.collectable_bombs.remove(bomb)
                    self.collected_bombs.append(bomb)
            for bomb in self.collectable_bombs:
                self.player_2.collectable_collision(bomb)
                if bomb.recollected:
                    self.collectable_bombs.remove(bomb)
                    self.collected_bombs_2.append(bomb)
            for collectable_object in self.collectable_objects:
                self.player.collectable_collision(collectable_object)
            for collectable_object in self.collectable_objects:
                self.player_2.collectable_collision(collectable_object)

            for water_potion in self.water_potions:
                self.player.collectable_collision(water_potion)
                if water_potion.recollected:
                    self.water_potions.remove(water_potion)
                    is_water_potion_collected_1 = True
            for water_potion in self.water_potions:
                self.player_2.collectable_collision(water_potion)
                if water_potion.recollected:
                    self.water_potions.remove(water_potion)
                    is_water_potion_collected_2 = True
            if not collisioning[0]:
                if is_1_moving_up:
                    self.player.move_up()
                elif is_1_moving_down:
                    self.player.move_down()
                elif is_1_moving_right:
                    self.player.move_right()
                elif is_1_moving_left:
                    self.player.move_left()
            else:
                if collisioning[1]:
                    if is_1_moving_up:
                        self.player.move_up()
                    elif is_1_moving_down:
                        self.player.move_down()
                    elif is_1_moving_right:
                        self.player.move_right()
                    elif is_1_moving_left:
                        self.player.move_left()
                    time.sleep(0.1)
                    self.player.life -= 1
                else:
                    time.sleep(0.1)
                    self.player.life -= 1
                    if is_1_moving_up:
                        self.player.move_down()
                    elif is_1_moving_down:
                        self.player.move_up()
                    elif is_1_moving_right:
                        self.player.move_left()
                    elif is_1_moving_left:
                        self.player.move_right()
            self.player_2_move(collisioning_2, is_2_moving_up, is_2_moving_down, is_2_moving_right, is_2_moving_left)
            self.check_player_life_1v1()
            self.load_ui_1v1(screen, surface)

            for print_object in self.object_list:
                surface.blit(print_object.sprite, tuple(print_object.position))
            self.print_collectable_1v1(surface, screen)

            if is_water_potion_collected_1:
                water_potion_png = pygame.transform.scale(water_potion_png, (21, 24))
                screen.blit(water_potion_png, (310, 13))
            if is_water_potion_collected_2:
                water_potion_png = pygame.transform.scale(water_potion_png, (21, 24))
                screen.blit(water_potion_png, (705, 13))
            surface.blit(self.player.sprite, (self.player.position[0], self.player.position[1]))
            surface.blit(self.player_2.sprite, (self.player_2.position[0], self.player_2.position[1]))
            if self.player.objects_recollected + self.player_2.objects_recollected >= self.number_diamond:
                if self.player.objects_recollected > self.player_2.objects_recollected:
                    self.generate_finish_game_1v1(1)
                else:
                    self.generate_finish_game_1v1(2)
            pygame.display.flip()

        pygame.quit()
        exit(0)

    def player_2_move(self, collisioning, is_2_moving_up, is_2_moving_down, is_2_moving_right,
                      is_2_moving_left):
        if not collisioning[0]:
            if is_2_moving_up:
                self.player_2.move_up()
            elif is_2_moving_down:
                self.player_2.move_down()
            elif is_2_moving_right:
                self.player_2.move_right()
            elif is_2_moving_left:
                self.player_2.move_left()
        else:
            if collisioning[1]:
                if is_2_moving_up:
                    self.player_2.move_up()
                elif is_2_moving_down:
                    self.player_2.move_down()
                elif is_2_moving_right:
                    self.player_2.move_right()
                elif is_2_moving_left:
                    self.player_2.move_left()
                time.sleep(0.1)
                self.player_2.life -= 1
            else:
                time.sleep(0.1)
                self.player_2.life -= 1
                if is_2_moving_up:
                    self.player_2.move_down()
                elif is_2_moving_down:
                    self.player_2.move_up()
                elif is_2_moving_right:
                    self.player_2.move_left()
                elif is_2_moving_left:
                    self.player_2.move_right()

    def generate_finish_game_1(self, is_win: bool):
        pygame.init()
        game = Game()
        res = (800, 650)
        screen = pygame.display.set_mode(res)
        color = (255, 255, 255)
        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)
        width = screen.get_width()
        height = screen.get_height()
        smallfont = pygame.font.SysFont('impact', 35)
        bigfont = pygame.font.SysFont('impact', 70)
        win_text = bigfont.render('YOU WIN!!!', True, color) if is_win else bigfont.render('IM, SORRY YOU LOSE', True,
                                                                                           color)
        play_text = smallfont.render('Replay', True, color)
        play_1v1_text = smallfont.render('Play 1v1', True, color)
        text = smallfont.render('Quit', True, color)
        if is_win:
            screen.fill((0, 128, 0))
        else:
            screen.fill((255, 25, 25))
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 100 <= mouse[
                        1] <= height / 2 - 100 + 40:
                        self.collected_bombs = []
                        self.collected_bombs_2 = []
                        self.player = Player([100, 100])
                        self.player_2 = Player([500, 500])
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
                        self.game()
                    if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 50 <= mouse[
                        1] <= height / 2 - 50 + 40:
                        self.game_1v1()
                    if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 <= mouse[
                        1] <= height / 2 + 40:
                        pygame.quit()
            mouse = pygame.mouse.get_pos()
            if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 100 <= mouse[
                1] <= height / 2 - 100 + 40:
                pygame.draw.rect(screen, color_light, [width / 2 - 90, height / 2 - 100, 140, 40])
            else:
                pygame.draw.rect(screen, color_dark, [width / 2 - 90, height / 2 - 100, 140, 40])
            if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 50 <= mouse[
                1] <= height / 2 - 50 + 40:
                pygame.draw.rect(screen, color_light, [width / 2 - 90, height / 2 - 50, 140, 40])
            else:
                pygame.draw.rect(screen, color_dark, [width / 2 - 90, height / 2 - 50, 140, 40])
            if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.draw.rect(screen, color_light, [width / 2 - 90, height / 2, 140, 40])
            else:
                pygame.draw.rect(screen, color_dark, [width / 2 - 90, height / 2, 140, 40])
            screen.blit(win_text, (width / 2 - 200, 100))
            screen.blit(play_1v1_text, (width / 2 - 70, height / 2 - 50))
            screen.blit(play_text, (width / 2 - 60, height / 2 - 100))
            screen.blit(text, (width / 2 - 50, height / 2))
            pygame.display.update()

    def generate_finish_game_1v1(self, winner: int):
        pygame.init()
        game = Game()
        res = (800, 650)
        screen = pygame.display.set_mode(res)
        color = (255, 255, 255)
        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)
        width = screen.get_width()
        height = screen.get_height()
        smallfont = pygame.font.SysFont('impact', 35)
        bigfont = pygame.font.SysFont('impact', 70)
        win_text = bigfont.render('PLAYER 1 WINS!!!', True, color) if winner == 1 else bigfont.render(
            'PLAYER 2 WINS!!!', True, color)
        play_text = smallfont.render('Replay', True, color)
        play_1v1_text = smallfont.render('Play 1', True, color)
        text = smallfont.render('Quit', True, color)
        screen.fill((0, 128, 0))
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 100 <= mouse[
                        1] <= height / 2 - 100 + 40:
                        self.collected_bombs = []
                        self.collected_bombs_2 = []
                        self.player = Player([100, 100])
                        self.player_2 = Player([500, 500])
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
                        self.game_1v1()
                    if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 50 <= mouse[
                        1] <= height / 2 - 50 + 40:
                        self.game()
                    if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 <= mouse[
                        1] <= height / 2 + 40:
                        pygame.quit()
            mouse = pygame.mouse.get_pos()
            if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 100 <= mouse[
                1] <= height / 2 - 100 + 40:
                pygame.draw.rect(screen, color_light, [width / 2 - 90, height / 2 - 100, 140, 40])
            else:
                pygame.draw.rect(screen, color_dark, [width / 2 - 90, height / 2 - 100, 140, 40])
            if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 50 <= mouse[
                1] <= height / 2 - 50 + 40:
                pygame.draw.rect(screen, color_light, [width / 2 - 90, height / 2 - 50, 140, 40])
            else:
                pygame.draw.rect(screen, color_dark, [width / 2 - 90, height / 2 - 50, 140, 40])
            if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.draw.rect(screen, color_light, [width / 2 - 90, height / 2, 140, 40])
            else:
                pygame.draw.rect(screen, color_dark, [width / 2 - 90, height / 2, 140, 40])
            screen.blit(win_text, (width / 2 - 200, 100))
            screen.blit(play_1v1_text, (width / 2 - 70, height / 2 - 50))
            screen.blit(play_text, (width / 2 - 60, height / 2 - 100))
            screen.blit(text, (width / 2 - 50, height / 2))
            pygame.display.update()
