## Among Myth and Wonder
## sf_load_game_menu

from Resources.Game_Graphics import graphics_obj
from Resources.Game_Graphics import graphics_funs


def load_game_menu_keys(key_action):
    print("load_game_menu_keys")


def load_game_menu_surface_m1(position):
    # print("load_game_menu_surface_m1")
    graphics_funs.m1_single_click(graphics_obj.menus_objects, position)


def load_game_menu_surface_m3(position):
    print("load_game_menu_surface_m3")
