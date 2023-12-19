## Among Myth and Wonder
## sf_create_level

import sys, pygame

from Resources import game_stats
from Resources import game_start
from Resources import update_gf_level_editor

button_zone = [[250, 513, 550, 545],  # return_to_main_menu_but
               [50, 131, 120, 163],
               [130, 131, 162, 163],
               [170, 131, 202, 163],
               [50, 232, 120, 264],
               [130, 232, 162, 264],
               [170, 232, 202, 264],
               [50, 333, 270, 365],
               [280, 333, 312, 365],
               [320, 333, 352, 365],
               [250, 458, 550, 490],  # start_editor_but
               [370, 131, 440, 163],
               [450, 131, 482, 163],
               [490, 131, 522, 163]]


def create_level_keys(key_action):
    print("key_action")
    print("input_text: " + str(game_stats.input_text))

    if len(game_stats.input_text) > 0:
        # Check if input is a number
        if game_stats.active_width_field or game_stats.active_height_field or game_stats.active_starting_month_field:
            print("Is it a number?  " + str(game_stats.input_text[-1]))
            new_character = str(game_stats.input_text[-1])
            if new_character.replace('.', '', 1).isdigit():
                if not (game_stats.input_text[-1] == "0" and len(game_stats.create_level_input_text) == 0):
                    game_stats.create_level_input_text += str(game_stats.input_text[-1])

        # Check if input is a number or a letter
        elif game_stats.active_name_field:
            print(str(game_stats.input_text))
            print("Is it a number or a letter?  " + str(game_stats.input_text[-1]))
            new_character = str(game_stats.input_text[-1])
            if new_character.isalnum() or new_character.isspace():
                game_stats.create_level_input_text += str(game_stats.input_text[-1])
            # game_stats.create_level_input_text += str(game_stats.input_text[-1])



            # print(str(new_character.replace('.', '', 1).isdigit()))
            # print(str(new_character))

    print("")


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

    game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def width_field_enter():
    print("type width")
    game_stats.input_text = ""
    game_stats.create_level_input_text = ""
    game_stats.active_width_field = True
    game_stats.active_height_field = False
    game_stats.active_name_field = False
    game_stats.active_starting_month_field = False
    game_stats.record_text = True


def approve_width_but():
    if len(game_stats.level_width) > 0:
        game_stats.new_level_width = int(game_stats.level_width)
        game_stats.level_width = ""
        game_stats.input_text = ""
        game_stats.create_level_input_text = ""
        game_stats.active_width_field = False
        game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def cancel_width_but():
    game_stats.level_width = ""
    game_stats.input_text = ""
    game_stats.create_level_input_text = ""
    game_stats.active_width_field = False
    game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def height_field_enter():
    print("type height")
    game_stats.input_text = ""
    game_stats.create_level_input_text = ""
    game_stats.active_height_field = True
    game_stats.active_width_field = False
    game_stats.active_name_field = False
    game_stats.active_starting_month_field = False
    game_stats.record_text = True


def approve_height_but():
    if len(game_stats.level_height) > 0:
        game_stats.new_level_height = int(game_stats.level_height)
        game_stats.level_height = ""
        game_stats.input_text = ""
        game_stats.create_level_input_text = ""
        game_stats.active_height_field = False
        game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def cancel_height_but():
    game_stats.level_height = ""
    game_stats.input_text = ""
    game_stats.create_level_input_text = ""
    game_stats.active_height_field = False
    game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def name_field_enter():
    print("type name")
    game_stats.input_text = ""
    game_stats.create_level_input_text = ""
    game_stats.active_name_field = True
    game_stats.active_width_field = False
    game_stats.active_height_field = False
    game_stats.active_starting_month_field = False
    game_stats.record_text = True


def approve_name_but():
    if len(game_stats.level_name) > 0:
        game_stats.new_level_name = game_stats.level_name
        game_stats.level_name = ""
        game_stats.input_text = ""
        game_stats.create_level_input_text = ""
        game_stats.active_name_field = False
        game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def cancel_name_but():
    game_stats.level_name = ""
    game_stats.input_text = ""
    game_stats.create_level_input_text = ""
    game_stats.active_name_field = False
    game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def start_editor_but():
    game_stats.active_width_field = False
    game_stats.active_height_field = False
    game_stats.active_name_field = False
    game_stats.active_starting_month_field = False

    game_start.new_game()

    game_stats.current_screen = "Level Editor"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "level_editor_screen"

    game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()

    # Update visuals
    game_stats.gf_menus_art = {}
    update_gf_level_editor.update_sprites()


def starting_month_field_enter():
    print("type starting month")
    game_stats.input_text = ""
    game_stats.create_level_input_text = ""
    game_stats.active_starting_month_field = True
    game_stats.active_width_field = False
    game_stats.active_height_field = False
    game_stats.active_name_field = False
    game_stats.record_text = True


def approve_starting_month_but():
    if len(game_stats.type_LE_month) > 0:
        game_stats.LE_month = int(game_stats.type_LE_month)
        game_stats.type_LE_month = ""
        game_stats.input_text = ""
        game_stats.create_level_input_text = ""
        game_stats.active_starting_month_field = False
        game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def cancel_starting_month_but():
    game_stats.type_LE_month = ""
    game_stats.input_text = ""
    game_stats.create_level_input_text = ""
    game_stats.active_starting_month_field = False
    game_stats.record_text = False

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


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
