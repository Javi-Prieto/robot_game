import pygame

from robots.models.player import Player
from robots.models.wall import Wall

pygame.init()
screen_height = 650
surface_width = 800
surface_height = 600
bg = pygame.image.load("assets/background.jpg")
sprite = pygame.image.load("assets/player.png")
wall = pygame.image.load("assets/wall.png")
bw_top = pygame.image.load("assets/big_wall_top.png")
bw_bt = pygame.image.load("assets/big_wall_bottom.png")
bw_lft = pygame.image.load("assets/big_wall_left.png")
bw_rght = pygame.image.load("assets/big_wall_right.png")
heart_png = pygame.image.load("assets/heart.png")
clock = pygame.image.load("assets/clock.png")

player = Player(sprite)
big_wall_top = Wall(bw_top, [0, 0], [800, 50])
big_wall_bottom = Wall(bw_bt, [0, 550], [800, 50])
big_wall_left = Wall(bw_lft, [0, 0], [50, 800])
big_wall_right = Wall(bw_rght, [750, 0], [50, 800])
font = pygame.font.Font(None, 50)

running = True
surface = pygame.Surface((surface_width, surface_height))
screen = pygame.display.set_mode((surface_width, screen_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_RIGHT:
                    player.move_right()
                case pygame.K_LEFT:
                    player.move_left()
                case pygame.K_UP:
                    player.move_up()
                case pygame.K_DOWN:
                    player.move_down()
        if player.wall_collision(big_wall_top.position, big_wall_top.size):
            player.life -= 1
        elif  player.wall_collision(big_wall_top.position, big_wall_top.size):
            player.life -= 1


    life_text = font.render('x '+str(player.life), True, (255, 255, 255))
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
