## Among Myth and Wonder
## sf_skirmish_menu

from Resources.Game_Graphics import graphics_obj
from Resources.Game_Graphics import graphics_funs


def skirmish_menu_keys(key_action):
    print("skirmish_menu_keys")


def skirmish_menu_surface_m1(position):
    # print("skirmish_menu_surface_m1")
    graphics_funs.m1_single_click(graphics_obj.menus_objects, position)


def skirmish_menu_surface_m3(position):
    print("skirmish_menu_surface_m3")
