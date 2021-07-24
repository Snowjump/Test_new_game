## Miracle battles!


import sys, pygame

from Resources import game_stats

button_zone = [[270, 413, 570, 445],
               [270, 213, 570, 245],
               [270, 263, 570, 295],
               [270, 313, 570, 345]]


def entrance_menu_keys(key_action):
    pass


def entrance_menu_surface_m1(position):
    print("Success")
    button_numb = 0
    for square in button_zone:
        button_numb += 1
        print("Entrance menu surface button " + str(button_numb))
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_funs[button_numb]()
            break


def entrance_menu_surface_m3(position):
    print("Success")


def exit_but():
    pygame.quit()
    sys.exit()


def new_game_but():
    game_stats.selected_character = None

    game_stats.current_screen = "New Game"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "new_game_screen"


def create_level_but():
    game_stats.selected_character = None

    game_stats.current_screen = "Create Level"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "create_level_screen"


def settings_but():
    game_stats.current_screen = "Settings"
    game_stats.screen_to_draw = "settings_screen"


button_funs = {1 : exit_but,
               2 : new_game_but,
               3 : create_level_but,
               4 : settings_but}