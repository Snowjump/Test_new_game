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
            button.draw_button(screen)

    # Art picture
    picture_img = game_stats.gf_menus_art["Arts/sinister_figure_in_the_woods"]
    picture_img = pygame.transform.scale(picture_img,
                                         (306, 546))
    screen.blit(picture_img, (901, 61))
