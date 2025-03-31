## Among Myth and Wonder
## sf_skirmish_menu

import sys, pygame
import math

from Resources import game_stats
from Resources import start_new_level
from Resources import graphics_obj


def skirmish_menu_keys(key_action):
    pass


def skirmish_menu_surface_m1(position):
    # print("skirmish_menu_surface_m1")
    for obj in graphics_obj.menus_objects:
        for button in obj.buttons:
            button.press_button(position)
        for obj_list in obj.lists:
            obj_list.select_element(position)
    # pressed_button = False
    # button_numb = 0
    # for square in button_zone:
    #     button_numb += 1
    #     # print("Skirmish surface button " + str(button_numb))
    #     if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
    #         button_funs[button_numb]()
    #         pressed_button = True
    #         break

    # if not pressed_button:
    #     # Skirmish scenarios list
    #     square = [77, 82, 304, 404]
    #     if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
    #         pressed_button = True
    #         y_axis = position[1]
    #         y_axis -= 82
    #         # print(str(y_axis))
    #         y_axis = math.ceil(y_axis / 24)
    #         # print(str(y_axis))
    #         # print("len(game_stats.levels_list) - " + str(len(game_stats.levels_list)))
    #         if y_axis - 1 != game_stats.level_index and y_axis <= len(game_stats.levels_list):
    #             game_stats.level_index = int(y_axis - 1)
    #             start_new_level.gather_level_information("Skirmish", game_stats.levels_list[game_stats.level_index])


def skirmish_menu_surface_m3(position):
    print("skirmish_menu_surface_m3")
