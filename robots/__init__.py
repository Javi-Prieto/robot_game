import pygame
import time
from robots.models.player import Player
from robots.models.collectable import WaterPotion
from robots.models.wall import Wall, Side_wall
from robots.models.water import Water

number_potion_water = 0
number_bomb = 0
number_potion_l1 = 0
number_potion_l3 = 0
number_potion_l5 = 0
number_diamond = 0


pygame.init()
screen_height = 650
surface_width = 800
surface_height = 600


bg = pygame.image.load("assets/background.jpg")


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
                        number_bomb = save_dict[1]
                    case 'PW':
                        number_potion_water = save_dict[1]
                    case 'P1':
                        number_potion_l1 = save_dict[1]
                    case 'P3':
                        number_potion_l3 = save_dict[1]
                    case 'P5':
                        number_potion_l5 = save_dict[1]
                    case 'D':
                        number_diamond = save_dict[1]
        else:
            result_line = line.split('|')
            result_line.pop(-1)
            print(result_line)
            x_point = 0
            for chac in result_line:
                match chac:
                    case 'M':
                        object_list.append(Wall(mid_wall, [x_point, y_point], [50, 50]))
                    case 'A':
                        object_list.append(Water([x_point, y_point], [50, 50]))
                x_point += 50
            y_point += 50


clock = pygame.time.Clock()
player = Player()
water_potion = WaterPotion([300, 200])
font = pygame.font.Font(None, 50)

running = True
surface = pygame.Surface((surface_width, surface_height))
screen = pygame.display.set_mode((surface_width, screen_height))
is_moving_up = False
is_moving_down = False
is_moving_left = False
is_moving_right = False


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
                    if water_potion.recollected:
                        if player.isWaterproof:
                            player.isWaterproof = False
                        else:
                            player.isWaterproof = True
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

    if is_moving_up:
        if not player.wall_water_collision(object_list)[0]:
            player.move_up()
        else:
            if player.wall_water_collision(object_list)[1]:
                time.sleep(0.1)
                player.life -= 1
            elif player.wall_water_collision(object_list)[1]:
                player.move_down()
                player.move_down()
                time.sleep(0.1)
                player.life -= 1
    elif is_moving_down:
        if not player.wall_water_collision(object_list)[0]:
            player.move_down()
        else:
            if player.wall_water_collision(object_list)[1]:
                time.sleep(0.1)
                player.life -= 1
            elif player.wall_water_collision(object_list)[1]:
                player.move_down()
                player.move_down()
                time.sleep(0.1)
                player.life -= 1
    elif is_moving_left:
        if not player.wall_water_collision(object_list)[0]:
            player.move_left()
        else:
            if player.wall_water_collision(object_list)[1]:
                time.sleep(0.1)
                player.life -= 1
            elif player.wall_water_collision(object_list)[1]:
                player.move_down()
                player.move_down()
                time.sleep(0.1)
                player.life -= 1
    elif is_moving_right:
        if not player.wall_water_collision(object_list)[0]:
            player.move_right()
        else:
            if player.wall_water_collision(object_list)[1]:
                time.sleep(0.1)
                player.life -= 1
            elif player.wall_water_collision(object_list)[1]:
                player.move_down()
                player.move_down()
                time.sleep(0.1)
                player.life -= 1

    player.collectable_collision(water_potion)
    check_player_life()

    pygame.draw.rect(surface, (0,0,0), player.hitbox, 2)
    life_text = font.render('------------', True, (0, 0, 0), (0, 0, 0))
    screen.blit(life_text, (40, 7))
    life_text = font.render('x ' + str(player.life), False, (255, 255, 255))
    screen.blit(life_text, (40, 7))
    screen.blit(quick_inventory_png, (surface_width-96, 0))
    screen.blit(heart_png, (5, 10))
    screen.blit(surface, (0, 50))
    surface.blit(bg, (0, 0))
    for print_object in object_list:
        surface.blit(print_object.sprite, tuple(print_object.position))
    if not water_potion.recollected:
        surface.blit(water_potion.sprite, tuple(water_potion.position))
    else:
        water_potion_png = pygame.transform.scale(water_potion.sprite, (21, 24))
        screen.blit(water_potion_png, (surface_width-35, 13))

    surface.blit(player.sprite, (player.position[0], player.position[1]))

    pygame.display.flip()

pygame.quit()
