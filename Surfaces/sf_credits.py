## Among Myth and Wonder
## sf_credits

import pygame

from Resources import game_stats

button_zone = [[31, 31, 331, 63]]


def credits_keys(key_action):
    pass


def credits_surface_m1(position):
    print("credits_surface_m1")
    button_numb = 0
    for square in button_zone:
        button_numb += 1
        # print("Credits surface button " + str(button_numb))
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_funs[button_numb]()
            break


def credits_surface_m3(position):
    print("credits_surface_m3")


def return_to_main_menu_but():
    game_stats.current_screen = "Entrance Menu"
    game_stats.screen_to_draw = "main_menu_screen"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


button_funs = {1 : return_to_main_menu_but}
