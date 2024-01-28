import pygame
import time
from robots.models.player import Player
from robots.models.collectable import WaterPotion, WinnerObject, Life1Potion, Life3Potion, Life5Potion, Bomb
from robots.models.wall import Wall
from robots.models.water import Water
import random

number_potion_water = 0
number_bomb = 0
number_potion_l1 = 0
number_potion_l3 = 0
number_potion_l5 = 0
number_diamond = 0
total_collectable = 0

pygame.init()
screen_height = 650
surface_width = 800
surface_height = 600

bg = pygame.image.load("assets/background.jpg")
dp_face = pygame.image.load("assets/Screen/dp_face.png")
heart_png = pygame.image.load("assets/heart.png")
clock_png = pygame.image.load("assets/clock.png")
quick_inventory_png = pygame.image.load("assets/Screen/quick_inventory.png")
mid_wall = pygame.image.load("assets/Obstacles/wall_block.png")
object_list = []

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
                        object_list.append(Wall(mid_wall, [x_point, y_point], [50, 50]))
                    case 'A':
                        object_list.append(Water([x_point, y_point], [50, 50]))
                x_point += 50
            y_point += 50

collectable_objects = []
water_potions = []
collectable_bombs = []
collected_bombs = []


def get_nice_cords():
    x = random.randint(50, 750)
    y = random.randint(50, 550)
    x -= x % 50
    y -= y % 50
    for wall_water_object in object_list:
        while wall_water_object.position == [x, y]:
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            x -= x % 50
            y -= y % 50

    return [x, y]


total_collectable = (number_bomb + number_diamond + number_potion_l1 + number_potion_water + number_potion_l3 +
                     number_potion_l5)
for i in range(total_collectable):
    if i <= number_bomb:
        collectable_bombs.append(Bomb(get_nice_cords()))
    elif i <= number_bomb + number_diamond:
        collectable_objects.append(WinnerObject(get_nice_cords()))
    elif i <= number_bomb + number_diamond + number_potion_l1:
        collectable_objects.append(Life1Potion(get_nice_cords()))
    elif i <= number_bomb + number_diamond + number_potion_l1 + number_potion_water:
        water_potions.append(WaterPotion(get_nice_cords()))
    elif i <= number_bomb + number_diamond + number_potion_l1 + number_potion_water + number_potion_l3:
        collectable_objects.append(Life3Potion(get_nice_cords()))
    else:
        collectable_objects.append(Life5Potion(get_nice_cords()))

for collectable_object in collectable_objects:
    for i in collectable_objects:
        if not i == collectable_object:
            while i.position == collectable_object.position:
                collectable_object.position = get_nice_cords()
    for i in water_potions:
        while i.position == collectable_object.position:
            collectable_object.position = get_nice_cords()
    for i in collectable_bombs:
        while i.position == collectable_object.position:
            collectable_object.position = get_nice_cords()
clock = pygame.time.Clock()
player = Player()
font = pygame.font.Font(None, 50)
bomb_font = pygame.font.Font(None, 24)
water_potion_for_inventory = WaterPotion([0, 0])
running = True
surface = pygame.Surface((surface_width, surface_height))
screen = pygame.display.set_mode((surface_width, screen_height))
is_moving_up = False
is_moving_down = False
is_moving_left = False
is_moving_right = False
is_water_potion_collected = False


def check_player_life():
    if not player.life > 0:
        global running
        running = False


while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
                        if player.isWaterproof:
                            player.isWaterproof = False
                        else:
                            player.isWaterproof = True
                case pygame.K_b:
                    if not len(collected_bombs) == 0:
                        collected_bombs[-1].position = [player.position[0] - (player.position[0] % 50),
                                                        player.position[1] - (player.position[1] % 50)]
                        surface.blit(collected_bombs[-1].sprite, tuple(player.position))
                        for collision_object in object_list:
                            if collected_bombs[-1].destroy_wall(collision_object):
                                object_list.remove(collision_object)
                        collected_bombs.remove(collected_bombs[-1])
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
    collisioning = []
    for collision_object in object_list:
        collisioning = player.wall_water_collision(collision_object)
        if collisioning[0]: break
    for bomb in collectable_bombs:
        player.collectable_collision(bomb)
    for collectable_object in collectable_objects:
        player.collectable_collision(collectable_object)
    if not is_water_potion_collected:
        for water_potion in water_potions:
            player.collectable_collision(water_potion)
            if water_potion.recollected:
                is_water_potion_collected = True
    if not collisioning[0]:
        if is_moving_up:
            player.move_up()
        elif is_moving_down:
            player.move_down()
        elif is_moving_right:
            player.move_right()
        elif is_moving_left:
            player.move_left()
    else:
        if collisioning[1]:
            if is_moving_up:
                player.move_up()
            elif is_moving_down:
                player.move_down()
            elif is_moving_right:
                player.move_right()
            elif is_moving_left:
                player.move_left()
            time.sleep(0.1)
            player.life -= 1
        else:
            time.sleep(0.1)
            player.life -= 1
            if is_moving_up:
                player.move_down()
            elif is_moving_down:
                player.move_up()
            elif is_moving_right:
                player.move_left()
            elif is_moving_left:
                player.move_right()

    check_player_life()
    life_text = font.render('-----------------------', True, (0, 0, 0), (0, 0, 0))
    screen.blit(life_text, (40, 7))
    win_text = font.render('x ' + str(player.objects_recollected), False, (255, 255, 255))
    life_text = font.render('x ' + str(player.life), False, (255, 255, 255))
    screen.blit(life_text, (40, 7))
    screen.blit(win_text, (170, 7))
    screen.blit(quick_inventory_png, (surface_width - 96, 0))
    screen.blit(heart_png, (5, 10))
    screen.blit(dp_face, (115, 2))
    screen.blit(surface, (0, 50))
    surface.blit(bg, (0, 0))

    for print_object in object_list:
        surface.blit(print_object.sprite, tuple(print_object.position))
    for collectable_object in collectable_objects:
        if not collectable_object.recollected:
            surface.blit(collectable_object.sprite, tuple(collectable_object.position))
        else:
            collectable_objects.remove(collectable_object)
    for water_potion in water_potions:
        if not water_potion.recollected:
            surface.blit(water_potion.sprite, tuple(water_potion.position))
    for bomb in collectable_bombs:
        if not bomb.recollected:
            surface.blit(bomb.sprite, tuple(bomb.position))
        else:
            collectable_bombs.remove(bomb)
            collected_bombs.append(bomb)
    for bomb in collected_bombs:
        bomb_png = water_potion_png = pygame.transform.scale(bomb.sprite, (28, 28))
        screen.blit(water_potion_png, (surface_width - 85, 11))
        bomb_number = bomb_font.render(str(len(collected_bombs)), False, (255, 255, 255))
        screen.blit(bomb_number, (surface_width - 90, 5))
    if is_water_potion_collected:
        water_potion_png = pygame.transform.scale(water_potion_for_inventory.sprite, (21, 24))
        screen.blit(water_potion_png, (surface_width - 35, 13))

    surface.blit(player.sprite, (player.position[0], player.position[1]))
    if player.objects_recollected >= number_diamond:
        running = False
    pygame.display.flip()

pygame.quit()
