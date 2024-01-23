import pygame

from robots.models.player import Player
pygame.init()
screen_width = 800
screen_height = 600
bg = pygame.image.load("assets/background.jpg")
sprite = pygame.image.load("assets/player.png")

player = Player(sprite)

running = True


screen = pygame.display.set_mode((screen_width, screen_height))
screen.blit(bg, (0, 0))


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

        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg, (0, 0))
    screen.blit(player.sprite, (player.position[0], player.position[1]))

    pygame.display.flip()



pygame.quit()
