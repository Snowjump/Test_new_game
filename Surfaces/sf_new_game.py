## Miracle battles

import sys, pygame

from Resources import game_stats
from Resources import start_new_level

button_zone = [[250, 513, 550, 545],
               [250, 443, 550, 475]]


def new_game_keys(key_action):
    pass


def new_game_surface_m1(position):
    print("Success")
    button_numb = 0
    for square in button_zone:
        button_numb += 1
        print("New game surface button " + str(button_numb))
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_funs[button_numb]()
            break


def new_game_surface_m3(position):
    print("Success")


def return_to_main_menu_but():
    game_stats.current_screen = "Entrance Menu"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "main_menu_screen"


def start_but():
    start_new_level.begin_new_level("Test level")

    game_stats.current_screen = "Game Board"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "game_board_screen"

###


button_funs = {1 : return_to_main_menu_but,
               2 : start_but}