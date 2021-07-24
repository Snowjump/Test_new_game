## Miracle battles!

import sys, pygame

from Resources import game_stats
from Resources import game_start

button_zone = [[250, 513, 550, 545],
               [250, 131, 320, 163],
               [330, 131, 362, 163],
               [370, 131, 402, 163],
               [250, 232, 320, 264],
               [330, 232, 362, 264],
               [370, 232, 402, 264],
               [250, 333, 470, 365],
               [480, 333, 512, 365],
               [520, 333, 552, 365],
               [250, 458, 550, 490],
               [570, 131, 640, 163],
               [650, 131, 682, 163],
               [690, 131, 722, 163]]


def create_level_keys(key_action):
    pass


def create_level_surface_m1(position):
    # print("Success")
    button_numb = 0
    for square in button_zone:
        button_numb += 1
##        print("Create level surface button " + str(button_numb))
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_funs[button_numb]()
            break


def create_level_surface_m3(position):
    print("Success")


def return_to_main_menu_but():
    game_stats.active_width_field = False
    game_stats.active_height_field = False
    game_stats.active_name_field = False
    game_stats.active_starting_month_field = False

    game_stats.current_screen = "Entrance Menu"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "main_menu_screen"


def width_field_enter():

    print("type width")
    game_stats.active_width_field = True
    game_stats.active_height_field = False
    game_stats.active_name_field = False
    game_stats.active_starting_month_field = False


def approve_width_but():
    game_stats.new_level_width = int(game_stats.level_width)
    game_stats.level_width = ""
    game_stats.input_text = ""
    game_stats.active_width_field = False


def cancel_width_but():
    game_stats.level_width = ""
    game_stats.input_text = ""
    game_stats.active_width_field = False


def height_field_enter():

    print("type height")
    game_stats.active_height_field = True
    game_stats.active_width_field = False
    game_stats.active_name_field = False
    game_stats.active_starting_month_field = False


def approve_height_but():
    game_stats.new_level_height = int(game_stats.level_height)
    game_stats.level_height = ""
    game_stats.input_text = ""
    game_stats.active_height_field = False


def cancel_height_but():
    game_stats.level_height = ""
    game_stats.input_text = ""
    game_stats.active_height_field = False


def name_field_enter():

    print("type name")
    game_stats.active_name_field = True
    game_stats.active_width_field = False
    game_stats.active_height_field = False
    game_stats.active_starting_month_field = False


def approve_name_but():
    game_stats.new_level_name = game_stats.level_name
    game_stats.level_name = ""
    game_stats.input_text = ""
    game_stats.active_name_field = False


def cancel_name_but():
    game_stats.level_name = ""
    game_stats.input_text = ""
    game_stats.active_name_field = False


def start_editor_but():
    game_stats.active_width_field = False
    game_stats.active_height_field = False
    game_stats.active_name_field = False
    game_stats.active_starting_month_field = False

    game_start.new_game()

    game_stats.current_screen = "Level Editor"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "level_editor_screen"


def starting_month_field_enter():

    print("type starting month")
    game_stats.active_starting_month_field = True
    game_stats.active_width_field = False
    game_stats.active_height_field = False
    game_stats.active_name_field = False


def approve_starting_month_but():
    game_stats.LE_month = int(game_stats.type_LE_month)
    game_stats.type_LE_month = ""
    game_stats.input_text = ""
    game_stats.active_starting_month_field = False


def cancel_starting_month_but():
    game_stats.type_LE_month = ""
    game_stats.input_text = ""
    game_stats.active_starting_month_field = False


button_funs = {1 : return_to_main_menu_but,
               2 : width_field_enter,
               3 : approve_width_but,
               4 : cancel_width_but,
               5 : height_field_enter,
               6 : approve_height_but,
               7 : cancel_height_but,
               8 : name_field_enter,
               9 : approve_name_but,
               10 : cancel_name_but,
               11 : start_editor_but,
               12 : starting_month_field_enter,
               13 : approve_starting_month_but,
               14 : cancel_starting_month_but}
