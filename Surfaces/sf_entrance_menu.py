## Among Myth and Wonder
## sf_entrance_menu

import sys, pygame, glob

from Resources import game_stats
from Resources import start_new_level
from Resources.game_assets import resource_path

button_zone = [[270, 413, 570, 445],
               [270, 213, 570, 245],
               [270, 263, 570, 295],
               [270, 313, 570, 345],
               [270, 363, 570, 395]]


def entrance_menu_keys(key_action):
    pass


def entrance_menu_surface_m1(position):
    print("entrance_menu_surface_m1")
    button_numb = 0
    for square in button_zone:
        button_numb += 1
        # print("Entrance menu surface button " + str(button_numb))
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_funs[button_numb]()
            break


def entrance_menu_surface_m3(position):
    print("entrance_menu_surface_m3")


def exit_but():
    pygame.quit()
    sys.exit()


def skirmish_menu_but():
    game_stats.selected_character = None

    game_stats.current_screen = "Skirmish"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "skirmish_menu_screen"

    game_stats.level_index = 0
    game_stats.levels_list = glob.glob("Levels/Skirmish/*.dat")
    # print("1 level_list: " + str(game_stats.levels_list))
    # for line in game_stats.levels_list:
        # print(str(line))
        # line = str(line[16:-4])
        # print(str(line))
    # print("2/vel_list: " + str(game_stats.levels_list))
    game_stats.levels_list = [w.replace(w, w[16:-4]) for w in game_stats.levels_list]
    # print("3 level_list: " + str(game_stats.levels_list))
    # for line in game_stats.levels_list:
        # print(str(line))

    start_new_level.gather_level_information("Skirmish", game_stats.levels_list[game_stats.level_index])

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def create_level_but():
    game_stats.selected_character = None

    game_stats.current_screen = "Create Level"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "create_level_screen"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def settings_but():
    game_stats.current_screen = "Settings"
    game_stats.screen_to_draw = "settings_screen"

    # click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    # click_sound.play()

    asset_url = resource_path('Sound/Interface/Abstract1.ogg')
    click_sound = pygame.mixer.Sound(asset_url)
    click_sound.play()


def credits_but():
    game_stats.current_screen = "Credits"
    game_stats.screen_to_draw = "credits_screen"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


button_funs = {1 : exit_but,
               2 : skirmish_menu_but,
               3 : create_level_but,
               4 : settings_but,
               5 : credits_but}
