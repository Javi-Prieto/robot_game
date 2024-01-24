import pygame
import time
from robots.models.player import Player
from robots.models.wall import Wall

pygame.init()
screen_height = 650
surface_width = 800
surface_height = 600
bg = pygame.image.load("assets/background.jpg")
sprite = pygame.image.load("assets/PlayerSprites/PlayerFrontStay.png")
sprite_front = pygame.image.load("assets/PlayerSprites/PlayerFrontWalking.png")
sprite_back = pygame.image.load("assets/PlayerSprites/PlayerBackWalking.png")
sprite_right = pygame.image.load("assets/PlayerSprites/PlayerRightWalking.png")
sprite_left = pygame.image.load("assets/PlayerSprites/PlayerLeftWalking.png")
wall = pygame.image.load("assets/wall.png")
bw_top = pygame.image.load("assets/big_wall_top.png")
bw_bt = pygame.image.load("assets/big_wall_bottom.png")
bw_lft = pygame.image.load("assets/big_wall_left.png")
bw_rght = pygame.image.load("assets/big_wall_right.png")
heart_png = pygame.image.load("assets/heart.png")
clock = pygame.image.load("assets/clock.png")

player = Player(sprite)
big_wall_top = Wall(bw_top, [0, 0], [800, 50], 0)
big_wall_bottom = Wall(bw_bt, [0, 550], [800, 50], 1)
big_wall_left = Wall(bw_lft, [0, 0], [50, 800], 2)
big_wall_right = Wall(bw_rght, [750, 0], [50, 800], 3)
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
    for event in pygame.event.get():
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
        player.sprite = sprite_back
        if not player.wall_collision(big_wall_top):
            player.move_up()
        else:
            time.sleep(0.1)
            player.life -= 1
    elif is_moving_down:
        player.sprite = sprite_front
        if not player.wall_collision(big_wall_bottom):
            player.move_down()
        else:
            time.sleep(0.1)
            player.life -= 1
    elif is_moving_left:
        player.sprite = sprite_left
        if not player.wall_collision(big_wall_left):
            player.move_left()
        else:
            time.sleep(0.1)
            player.life -= 1
    elif is_moving_right:
        player.sprite = sprite_right
        if not player.wall_collision(big_wall_right):
            player.move_right()
        else:
            time.sleep(0.1)
            player.life -= 1

    check_player_life()

    life_text = font.render('------------', True, (0, 0, 0), (0, 0, 0))
    screen.blit(life_text, (40, 7))
    life_text = font.render('x ' + str(player.life), False, (255, 255, 255))
    screen.blit(life_text, (40, 7))
    screen.blit(heart_png, (5, 10))
    screen.blit(surface, (0, 50))
    surface.blit(bg, (0, 0))
    surface.blit(big_wall_top.sprite, tuple(big_wall_top.position))
    surface.blit(big_wall_bottom.sprite, tuple(big_wall_bottom.position))
    surface.blit(big_wall_left.sprite, tuple(big_wall_left.position))
    surface.blit(big_wall_right.sprite, tuple(big_wall_right.position))
    surface.blit(player.sprite, (player.position[0], player.position[1]))

    pygame.display.flip()

    if event.type == pygame.QUIT:
        running = False

pygame.quit()
