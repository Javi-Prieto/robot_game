import pygame
import time
from robots.models.player import Player
from robots.models.potion import WaterPotion
from robots.models.wall import Wall
from robots.models.water import Water

pygame.init()
screen_height = 650
surface_width = 800
surface_height = 600
bg = pygame.image.load("assets/background.jpg")

wall = pygame.image.load("assets/wall.png")
bw_top = pygame.image.load("assets/big_wall_top.png")
bw_bt = pygame.image.load("assets/big_wall_bottom.png")
bw_lft = pygame.image.load("assets/big_wall_left.png")
bw_rght = pygame.image.load("assets/big_wall_right.png")
heart_png = pygame.image.load("assets/heart.png")
clock_png = pygame.image.load("assets/clock.png")

clock = pygame.time.Clock()
player = Player()
big_wall_top = Wall(bw_top, [0, 0], [800, 20], 0)
big_wall_bottom = Wall(bw_bt, [0, 550], [800, 20], 1)
big_wall_left = Wall(bw_lft, [0, 0], [30, 800], 2)
big_wall_right = Wall(bw_rght, [750, 0], [0, 800], 3)
water_block1 = Water([500, 400], [62, 62])
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
        if not player.wall_collision(big_wall_top):
            player.move_up()
            if player.water_collision(water_block1):
                time.sleep(0.1)
                player.life -= 1
        else:
            time.sleep(0.1)
            player.life -= 1
    elif is_moving_down:
        if not player.wall_collision(big_wall_bottom):
            player.move_down()
            if player.water_collision(water_block1):
                time.sleep(0.1)
                player.life -= 1
        else:
            time.sleep(0.1)
            player.life -= 1
    elif is_moving_left:
        if not player.wall_collision(big_wall_left):
            player.move_left()
            if player.water_collision(water_block1):
                time.sleep(0.1)
                player.life -= 1
        else:
            time.sleep(0.1)
            player.life -= 1
    elif is_moving_right:
        if not player.wall_collision(big_wall_right):
            player.move_right()
            if player.water_collision(water_block1):
                time.sleep(0.1)
                player.life -= 1
        else:
            time.sleep(0.1)
            player.life -= 1
    player.collectable_collision(water_potion)
    check_player_life()

    print(player.isWaterproof)
    life_text = font.render('------------', True, (0, 0, 0), (0, 0, 0))
    screen.blit(life_text, (40, 7))
    life_text = font.render('x ' + str(player.life), False, (255, 255, 255))
    screen.blit(life_text, (40, 7))
    screen.blit(heart_png, (5, 10))
    screen.blit(surface, (0, 50))
    surface.blit(bg, (0, 0))
    surface.blit(water_potion.sprite, tuple(water_potion.position))
    surface.blit(water_block1.sprite, tuple(water_block1.position))
    surface.blit(big_wall_top.sprite, tuple(big_wall_top.position))
    surface.blit(big_wall_bottom.sprite, tuple(big_wall_bottom.position))
    surface.blit(big_wall_left.sprite, tuple(big_wall_left.position))
    surface.blit(big_wall_right.sprite, tuple(big_wall_right.position))
    surface.blit(player.sprite, (player.position[0], player.position[1]))

    pygame.display.flip()

pygame.quit()
