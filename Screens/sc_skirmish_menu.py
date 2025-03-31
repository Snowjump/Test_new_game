## Among Myth and Wonder
## sc_skirmish_menu

import pygame.draw, pygame.font

from Screens.colors_catalog import *

from Resources import game_stats
from Resources import graphics_obj

pygame.init()

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)
font20 = pygame.font.SysFont('timesnewroman', 20)
font18 = pygame.font.SysFont('timesnewroman', 18)


def skirmish_menu_screen(screen):
    screen.fill(NewGameColor)  # background

    # Title
    text_NewGame1 = font26.render("SKIRMISH", True, TitleText)
    screen.blit(text_NewGame1, [335, 40])

    for obj in graphics_obj.menus_objects:
        obj.draw_panel(screen)
        for button in obj.buttons:
            button.draw_button(screen)
        for obj_list in obj.lists:
            obj_list.draw_list(screen)

    # # Levels list
    # x = 78
    # y = 83
    # pygame.draw.polygon(screen, MainMenuColor, [[x, y], [x + 224, y], [x + 224, y + 320], [x, y + 320]])
    #
    # # text_NewGame2 = font20.render("Test level", True, TitleText)
    # # screen.blit(text_NewGame2, [80, 85])
    # x = 80
    # y = 85
    # underline_number = 0
    # for level_title in game_stats.levels_list:
    #     text_NewGame2 = font20.render(level_title, True, TitleText)
    #     screen.blit(text_NewGame2, [x, y])
    #
    #     # Grey underlines
    #     pygame.draw.lines(screen, NewGameColor, False, [(x, y + underline_number * 24 + 22),
    #                                                     (x + 220, y + underline_number * 24 + 22)], 1)
    #     underline_number += 1
    #     y += 24
    #
    # # White line
    # pygame.draw.lines(screen, WhiteBorder, False, [(x, y + game_stats.level_index * 24 + 22),
    #                                                (x + 220, y + game_stats.level_index * 24 + 22)], 1)
