## Among Myth and Wonder
## sf_game_board_pause_menu

from Resources.Game_Graphics import graphics_obj
from Resources.Game_Graphics import graphics_funs


def game_board_pause_menu_keys(key_action):
    graphics_funs.key_action_panel(graphics_obj.menus_objects, key_action)


def game_board_pause_menu_m1(position):
    # print("game_board_pause_menu_m1")
    graphics_funs.m1_single_click(graphics_obj.menus_objects, position)


def game_board_pause_menu_m3(position):
    print("game_board_pause_menu_m3")
