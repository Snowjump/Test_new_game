## Miracle battles!
## GameStart

import sys
import pygame
import os
from pygame.locals import *

from Resources import display_graphics
from Resources import game_stats
from Resources import game_basic
from Resources import game_battle
from Surfaces.sf_create_level import *

# Screens and surfaces
from Surfaces.sf_entrance_menu import *
from Surfaces.sf_game_board import *
from Surfaces.sf_level_editor import *
from Surfaces.sf_skirmish_menu import *
from Surfaces.sf_settings import *
from Surfaces.sf_battle import *
from Surfaces.sf_credits import *


fpsClock = pygame.time.Clock()
time_counted = 0
# font16 = pygame.font.SysFont('timesnewroman', 16)

# display constants
size = width, height = game_stats.game_window_width, game_stats.game_window_height

print("test1")
## screen_to_draw = "main_menu_screen"
game_stats.screen_to_draw = "main_menu_screen"
## screen = None
print("test2")

# mouse constants
mouse_button1_pressed = False
mouse_button3_pressed = False
key_pressed = False


def init_window():
    # Sound module, must be executed before pygame.init()
    # Source: https://proproprogs.ru/modules/dobavlyaem-zvuk-v-igrovoy-process-moduli-mixer-i-music
    pygame.mixer.pre_init(44100, -16, 1, 512)

    pygame.init()
    ##    game_stats.start_time = pygame.time.get_ticks()

    global screen

    # fonts
    global font10, font12, font14, font15, font16, font17, font18, font20, font26
    font10 = pygame.font.SysFont('timesnewroman', 10)
    font12 = pygame.font.SysFont('timesnewroman', 12)
    font14 = pygame.font.SysFont('timesnewroman', 14)
    font15 = pygame.font.SysFont('timesnewroman', 15)
    font16 = pygame.font.SysFont('timesnewroman', 16)
    font17 = pygame.font.SysFont('timesnewroman', 17)
    font18 = pygame.font.SysFont('timesnewroman', 18)
    font20 = pygame.font.SysFont('timesnewroman', 20)
    font26 = pygame.font.SysFont('timesnewroman', 26)

    size = width, height = game_stats.game_window_width, game_stats.game_window_height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Miracle battles game')

    print("End of init_window()")
    print(screen)


# game start
def main():
    init_window()
    main_action()


# very important function
def main_action():
    global screen

    while 1:
        # all events happen below
        control_input()

        game_stats.mouse_position = pygame.mouse.get_pos()
        ##        print("Screen variable")
        ##        print(screen)

        # all graphics perform below
        display_graphics.drawing(screen, game_stats.screen_to_draw)

        # frames per second
        fpsClock.tick(60)

        # # FPS
        # fps = fpsClock.get_fps()
        # text_panel = font16.render(str(fps), True, [0xFF, 0xFF, 0x99])
        # screen.blit(text_panel, [10, 44])
        if game_stats.fps_status:
            game_stats.fps = math.ceil(fpsClock.get_fps() * 100) / 100


# all events happen below
def control_input():
    global mouse_button1_pressed, mouse_button3_pressed, Pause, key_pressed, time_counted
    for event in pygame.event.get():
        # Game exit
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        # Typing
        if event.type == KEYDOWN:
            print("event.key: " + str(event.key) + "; key_pressed: " + str(key_pressed))
            # game_stats.input_text += event.unicode
            # print(game_stats.input_text)
            print("unicode: " + event.unicode + "; record_text: " + str(game_stats.record_text))
            if game_stats.record_text:
                game_stats.input_text += event.unicode

            # if not key_pressed or event.key in [304]:
            if not key_pressed:
                print("key_handler")
                if event.key not in [304]:
                    key_pressed = True
                key_handler(event.key)
            # print(game_stats.input_text)  # For checking

        if event.type == KEYUP:
            if key_pressed:
                # print("key is up " + str(event.key))
                key_pressed = False

        # Mouse button used
        if event.type == MOUSEBUTTONDOWN and mouse_button1_pressed == False and mouse_button3_pressed == False:
            # print("button " + str(event.button))
            # print(pygame.mouse.get_pos())
            mouse_button = event.button

            if mouse_button == 1:
                position = pygame.mouse.get_pos()
                print("Position is " + str(position))
                mouse_button1_pressed = True
                mouse_handler1(position)

            elif mouse_button == 3:
                position = pygame.mouse.get_pos()
                print("Position is " + str(position))
                mouse_button3_pressed = True
                mouse_handler3(position)

        if event.type == MOUSEBUTTONUP:
            # print("button is up " + str(event.button))
            mouse_button = event.button
            if mouse_button == 1:
                mouse_button1_pressed = False
            elif mouse_button == 3:
                mouse_button3_pressed = False

    # Timer
    ##        if game_stats.pause_status == False:
    ##            pass
    ##            game_stats.start_time = pygame.time.get_ticks()
    ##            time_counted = pygame.time.get_ticks()
    if game_stats.pause_status == False:
        time_counted = pygame.time.get_ticks()
        game_stats.temp_time_passed = time_counted - game_stats.last_start
        game_stats.display_time = int(game_stats.passed_time + game_stats.temp_time_passed)
        # print("game_stats.display_time - " + str(game_stats.display_time))
        # print("math.floor(game_stats.display_time/1000) - " + str(math.floor(game_stats.display_time/1000)))

        # if game_stats.strategy_mode:
        #     game_basic.advance_time()  # Increase time - also characters complete actions from their tasks

        game_basic.advance_time()
        if not game_stats.strategy_mode:
            game_battle.advance_battle_time(time_counted)

        # print("Passed time - " + str(game_stats.passed_time) + " get_ticks - " + str(time_counted) + " start time -
        # " + str(game_stats.start_time))
    else:
        game_stats.display_time = int(game_stats.passed_time)


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


# start everything
if __name__ == '__main__':
    main()
