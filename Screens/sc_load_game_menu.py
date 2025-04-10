## Among Myth and Wonder
## sc_load_game_menu

import pygame.font

from Screens.colors_catalog import *

from Resources.Game_Graphics import graphics_obj
from Resources.Game_Graphics import graphics_funs

pygame.init()

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)


def load_game_menu_screen(screen):
    screen.fill(NewGameColor)  # background

    # Title
    text_NewGame1 = font26.render("LOAD GAME", True, TitleText)
    screen.blit(text_NewGame1, [334, 40])

    graphics_funs.draw_panel_objects(screen, graphics_obj.menus_objects)