## Among Myth and Wonder
## sc_game_board_pause_menu

from Screens.colors_catalog import *

from Resources.Game_Graphics import graphics_obj
from Resources.Game_Graphics import graphics_funs


def game_board_pause_menu_screen(screen):
    screen.fill(NewGameColor)  # background

    graphics_funs.draw_panel_objects(screen, graphics_obj.menus_objects)
