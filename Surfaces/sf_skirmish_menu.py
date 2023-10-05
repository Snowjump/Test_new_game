## Miracle battles
## sf_skirmish_menu

import sys, pygame
import math

from Resources import game_stats
from Resources import start_new_level

button_zone = [[250, 513, 550, 545],
               [250, 443, 550, 475],
               [800, 109, 819, 128],
               [821, 109, 840, 128]]


def skirmish_menu_keys(key_action):
    pass


def skirmish_menu_surface_m1(position):
    # print("skirmish_menu_surface_m1")
    pressed_button = False
    button_numb = 0
    for square in button_zone:
        button_numb += 1
        # print("Skirmish surface button " + str(button_numb))
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_funs[button_numb]()
            pressed_button = True
            break

    if not pressed_button:
        # Skirmish scenarios list
        square = [77, 82, 304, 404]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            pressed_button = True
            y_axis = position[1]
            y_axis -= 82
            # print(str(y_axis))
            y_axis = math.ceil(y_axis / 24)
            # print(str(y_axis))
            # print("len(game_stats.levels_list) - " + str(len(game_stats.levels_list)))
            if y_axis - 1 != game_stats.level_index and y_axis <= len(game_stats.levels_list):
                game_stats.level_index = int(y_axis - 1)
                start_new_level.gather_level_information("Skirmish", game_stats.levels_list[game_stats.level_index])


def skirmish_menu_surface_m3(position):
    print("skirmish_menu_surface_m3")


def return_to_main_menu_but():
    game_stats.current_screen = "Entrance Menu"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "main_menu_screen"
    game_stats.levels_list = []

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def start_but():
    start_new_level.begin_new_level("Skirmish", game_stats.levels_list[game_stats.level_index])

    game_stats.current_screen = "Game Board"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "game_board_screen"
    game_stats.start_level_selected_realm = None

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()

    game_stats.gf_menus_art = {}


def previous_realm_but():
    start_new_level.skirmish_previous_realm()

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def next_realm_but():
    start_new_level.skirmish_next_realm()

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


button_funs = {1 : return_to_main_menu_but,
               2 : start_but,
               3 : previous_realm_but,
               4 : next_realm_but}
