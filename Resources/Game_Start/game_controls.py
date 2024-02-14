## Among Myth and Wonder
## game_controls

import pygame
from pygame.locals import *

# Screens and surfaces
from Surfaces.sf_create_level import *
from Surfaces.sf_entrance_menu import *
from Surfaces.sf_game_board import *
from Surfaces.sf_level_editor import *
from Surfaces.sf_skirmish_menu import *
from Surfaces.sf_settings import *
from Surfaces.sf_battle import *
from Surfaces.sf_credits import *


from Resources import game_stats


# all events happen below
def control_input():
    # global mouse_button1_pressed, mouse_button3_pressed, Pause, key_pressed, time_counted
    for event in pygame.event.get():
        # Game exit
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        # Typing
        if event.type == KEYDOWN:
            # print("event.key: " + str(event.key) + "; key_pressed: " + str(game_stats.key_pressed))
            # game_stats.input_text += event.unicode
            # print(game_stats.input_text)
            # print("unicode: " + event.unicode + "; record_text: " + str(game_stats.record_text))
            if game_stats.record_text:
                game_stats.input_text += event.unicode

            # if not key_pressed or event.key in [304]:
            if not game_stats.key_pressed:
                # print("key_handler")
                if event.key not in [304]:
                    game_stats.key_pressed = True
                key_handler(event.key)
            # print(game_stats.input_text)  # For checking

        if event.type == KEYUP:
            if game_stats.key_pressed:
                # print("key is up " + str(event.key))
                game_stats.key_pressed = False

        # Mouse button used
        if event.type == MOUSEBUTTONDOWN and not game_stats.mouse_button1_pressed \
                and not game_stats.mouse_button3_pressed:
            # print("button " + str(event.button))
            # print(pygame.mouse.get_pos())
            mouse_button = event.button

            if mouse_button == 1:
                position = pygame.mouse.get_pos()
                print("Position is " + str(position))
                game_stats.mouse_button1_pressed = True
                mouse_handler1(position)

            elif mouse_button == 3:
                position = pygame.mouse.get_pos()
                print("Position is " + str(position))
                game_stats.mouse_button3_pressed = True
                mouse_handler3(position)

        if event.type == MOUSEBUTTONUP:
            # print("button is up " + str(event.button))
            mouse_button = event.button
            if mouse_button == 1:
                game_stats.mouse_button1_pressed = False
            elif mouse_button == 3:
                game_stats.mouse_button3_pressed = False

    # Timer
    ##        if game_stats.pause_status == False:
    ##            pass
    ##            game_stats.start_time = pygame.time.get_ticks()
    ##            game_stats.time_counted = pygame.time.get_ticks()


# mouse function, takes mouse position during click
# then check what screen at this moment
# and check buttons on this screen
# perform appropriate action
def mouse_handler1(position):  # for first mouse button
    # print("Mouse 1: current_screen is " + str(game_stats.current_screen))
    button_action_list = {"Entrance Menu": entrance_menu_surface_m1,
                          "Skirmish": skirmish_menu_surface_m1,
                          "Game Board": game_board_surface_m1,
                          "Create Level": create_level_surface_m1,
                          "Level Editor": level_editor_surface_m1,
                          "Settings": settings_surface_m1,
                          "Battle": battle_surface_m1,
                          "Credits": credits_surface_m1}

    button_action_list[game_stats.current_screen](position)


def mouse_handler3(position):  # for third (right) mouse button
    # print("Mouse 3: current_screen is " + str(game_stats.current_screen))
    button_action_list = {"Entrance Menu": entrance_menu_surface_m3,
                          "Skirmish": skirmish_menu_surface_m3,
                          "Game Board": game_board_surface_m3,
                          "Create Level": create_level_surface_m3,
                          "Level Editor": level_editor_surface_m3,
                          "Settings": settings_surface_m3,
                          "Battle": battle_surface_m3,
                          "Credits": credits_surface_m3}

    button_action_list[game_stats.current_screen](position)


def key_handler(key_action):  # for keyboard
    # print("Keyboard: current_screen is " + str(game_stats.current_screen))
    # print("Key action is " + str(key_action))
    key_action_list = {"Entrance Menu": entrance_menu_keys,
                       "Skirmish": skirmish_menu_keys,
                       "Game Board": game_board_keys,
                       "Create Level": create_level_keys,
                       "Level Editor": level_editor_keys,
                       "Settings": settings_keys,
                       "Battle": battle_keys,
                       "Credits": credits_keys}

    key_action_list[game_stats.current_screen](key_action)
