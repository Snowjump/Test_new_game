## Miracle battles!


import sys, pygame

from Resources import game_stats

button_zone = [[160, 100, 460, 132],
               [160, 230, 300, 256],
               [160, 270, 300, 296]]


def settings_keys(key_action):
    pass


def settings_surface_m1(position):
    button_numb = 0
    for square in button_zone:
        button_numb += 1
        print("Settings surface button " + str(button_numb))
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_funs[button_numb]()
            break


def settings_surface_m3(position):
    print("settings_surface_m3")


def return_settings_main_menu_but():
    game_stats.current_screen = "Entrance Menu"
    game_stats.screen_to_draw = "main_menu_screen"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def res_1280_800_but():
    game_stats.game_window_width = 1280
    game_stats.game_window_height = 800
    size = width, height = game_stats.game_window_width, game_stats.game_window_height
    screen = pygame.display.set_mode(size)

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def res_1280_700_but():
    print("res_1280_700_but")
    game_stats.game_window_width = 1280
    game_stats.game_window_height = 700
    size = width, height = game_stats.game_window_width, game_stats.game_window_height
    screen = pygame.display.set_mode(size)

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


button_funs = {1 : return_settings_main_menu_but,
               2 : res_1280_800_but,
               3 : res_1280_700_but}
