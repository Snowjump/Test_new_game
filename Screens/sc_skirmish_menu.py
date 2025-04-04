## Among Myth and Wonder
## sc_skirmish_menu

import pygame.font

from Screens.colors_catalog import *

from Resources.Game_Graphics import graphics_obj
from Resources.Game_Graphics import graphics_funs

pygame.init()

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)


def skirmish_menu_screen(screen):
    screen.fill(NewGameColor)  # background

    # Title
    text_NewGame1 = font26.render("SKIRMISH", True, TitleText)
    screen.blit(text_NewGame1, [335, 40])

    graphics_funs.draw_panel_objects(screen, graphics_obj.menus_objects)
