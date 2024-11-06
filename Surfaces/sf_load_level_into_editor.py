## Among Myth and Wonder
## sf_load_level_into_editor

import sys, pygame, math

from Resources import game_stats
from Resources import game_start
from Resources import update_gf_level_editor


button_zone = [[250, 513, 550, 545],  # return_to_main_menu_but
               [670, 131, 830, 163],  # new level level
               [250, 458, 550, 490]]  # start_editor_but


def load_level_edit_surface_keys(key_action):
    pass


def load_level_edit_surface_m1(position):
    pressed_button = False
    button_numb = 0
    for square in button_zone:
        button_numb += 1
        ##        print("Create level surface button " + str(button_numb))
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
            if y_axis - 1 != game_stats.level_index and y_axis <= len(game_stats.levels_list):
                game_stats.level_index = int(y_axis - 1)


def load_level_edit_surface_m3(position):
    print("load_level_edit_surface_m3()")


def return_to_main_menu_but():
    game_stats.current_screen = "Entrance Menu"
    game_stats.screen_to_draw = "main_menu_screen"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def new_level_but():
    print("new_level_but()")
    game_stats.current_screen = "Create Level"
    game_stats.screen_to_draw = "create_level_screen"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def start_editor_but():
    game_start.load_level_into_editor()

    game_stats.current_screen = "Level Editor"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "level_editor_screen"

    game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()

    # Update visuals
    game_stats.gf_menus_art = {}
    update_gf_level_editor.update_sprites()


button_funs = {1 : return_to_main_menu_but,
               2 : new_level_but,
               3 : start_editor_but}
