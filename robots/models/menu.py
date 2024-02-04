import pygame

from robots.models.game import Game


class Menu:

    @staticmethod
    def generate_menu():
        pygame.init()
        res = (800, 650)
        game = Game()
        screen = pygame.display.set_mode(res)
        color = (255, 255, 255)
        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)
        menu_bg = pygame.image.load("assets/menu_bg.jpg")
        menu_bg = pygame.transform.scale(menu_bg, (800, 650))
        width = screen.get_width()
        height = screen.get_height()
        smallfont = pygame.font.SysFont('impact', 35)
        play_text = smallfont.render('Play', True, color)
        play_1v1_text = smallfont.render('Play 1v1', True, color)
        text = smallfont.render('Quit', True, color)
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 100 <= mouse[
                        1] <= height / 2 - 100 + 40:
                        game.game()
                    if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 - 50 <= mouse[
                        1] <= height / 2 - 50 + 40:
                        game.game_1v1()
                    if width / 2 - 90 <= mouse[0] <= width / 2 - 90 + 140 and height / 2 <= mouse[
                        1] <= height / 2 + 40:
                        pygame.quit()
            screen.blit(menu_bg, (0, 0))
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
            screen.blit(play_text, (width / 2 - 50, height / 2 - 100))
            screen.blit(play_1v1_text, (width / 2 - 70, height / 2 - 50))
            screen.blit(text, (width / 2 - 50, height / 2))
            pygame.display.update()


