import pygame_menu
import pygame

from robots.models.game import Game


class Menu:
    def __init__(self):
        self.game = Game()

    def generate_menu(self):
        pygame.init()
        surface = pygame.display.set_mode((800, 600))
        menu = pygame_menu.Menu('Welcome', 800, 600,
                                theme=pygame_menu.themes.THEME_BLUE)

        menu.add.button('Play', self.start_game())
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(surface)

    def start_game(self):
        self.game.game()
