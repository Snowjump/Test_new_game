## Among Myth and Wonder
## sc_entrance_menu

import pygame.draw, pygame.font

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources import game_stats
from Resources import graphics_obj

pygame.init()


def main_menu_screen(screen):
    screen.fill(MainMenuColor)  # background

    # Software version annotation
    text_MainMenu1 = arial_font10.render(str(game_stats.version_major) + "." + str(game_stats.version_minor)
                                         + "." + str(game_stats.version_micro), True, TitleText)
    screen.blit(text_MainMenu1, [3, 3])

    # Decorative lines
    pygame.draw.line(screen, LineMainMenuColor1, [30, 120], [240, 120], 10)
    pygame.draw.line(screen, LineMainMenuColor2, [30, 124], [240, 124], 3)

    pygame.draw.line(screen, LineMainMenuColor1, [600, 120], [810, 120], 10)
    pygame.draw.line(screen, LineMainMenuColor2, [600, 124], [810, 124], 3)

    pygame.draw.line(screen, LineMainMenuColor1, [30, 220], [180, 220], 6)

    pygame.draw.line(screen, LineMainMenuColor1, [660, 220], [810, 220], 6)

    # Title
    text_MainMenu1 = tnr_font26.render("Among Myth and Wonder", True, TitleText)
    screen.blit(text_MainMenu1, [290, 100])

    ## Buttons
    for obj in graphics_obj.menus_objects:
        for button in obj.buttons:
            button.draw_text_button(screen)
    # # New Game
    # text_MainMenu2 = tnr_font26.render("Skirmish", True, TitleText)
    # screen.blit(text_MainMenu2, [371, 215])
    #
    # pygame.draw.polygon(screen, BorderMainMenuColor, [[270, 213], [570, 213], [570, 245], [270, 245]], 3)
    #
    # # Create level
    # text_MainMenu2 = tnr_font26.render("Create level", True, TitleText)
    # screen.blit(text_MainMenu2, [353, 265])
    #
    # pygame.draw.polygon(screen, BorderMainMenuColor, [[270, 263], [570, 263], [570, 295], [270, 295]], 3)
    #
    # # Settings
    # text_MainMenu4 = tnr_font26.render("Settings", True, TitleText)
    # screen.blit(text_MainMenu4, [373, 315])
    #
    # pygame.draw.polygon(screen, BorderMainMenuColor, [[270, 313], [570, 313], [570, 345], [270, 345]], 3)
    #
    # # Credits
    # text_MainMenu4 = tnr_font26.render("Credits", True, TitleText)
    # screen.blit(text_MainMenu4, [376, 365])
    #
    # pygame.draw.polygon(screen, BorderMainMenuColor, [[270, 363], [570, 363], [570, 395], [270, 395]], 3)

    # # Exit
    # text_MainMenu3 = tnr_font26.render("Exit", True, TitleText)
    # screen.blit(text_MainMenu3, [395, 415])
    #
    # pygame.draw.polygon(screen, BorderMainMenuColor, [[270, 413], [570, 413], [570, 445], [270, 445]], 3)

    # Art picture
    picture_img = game_stats.gf_menus_art["Arts/sinister_figure_in_the_woods"]
    picture_img = pygame.transform.scale(picture_img,
                                         (306, 546))
    screen.blit(picture_img, (901, 61))
