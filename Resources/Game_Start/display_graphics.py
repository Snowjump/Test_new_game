## Among Myth and Wonder
## display_graphics

import pygame.draw
import pygame.font

# screens
from Screens.sc_create_level import *
from Screens.sc_entrance_menu import *
from Screens.sc_load_game_menu import *
from Screens.sc_game_board import *
from Screens.sc_game_board_pause_menu import *
from Screens.sc_level_editor import *
from Screens.sc_skirmish_menu import *
from Screens.sc_settings import *
from Screens.sc_battle import *
from Screens.sc_credits import *
from Screens.sc_load_level_into_editor import *


#  import GameStart
# print("display_graphics test1")

# screen functions
screen_funs = {"main_menu_screen" : main_menu_screen,
               "skirmish_menu_screen" : skirmish_menu_screen,
               "load_game_menu_screen" : load_game_menu_screen,
               "game_board_screen" : game_board_screen,
               "game_board_pause_menu_screen" : game_board_pause_menu_screen,
               "create_level_screen" : create_level_screen,
               "level_editor_screen" : level_editor_screen,
               "settings_screen" : settings_screen,
               "battle_screen" : battle_screen,
               "credits_screen" : credits_screen,
               "load_level_edit_screen" : load_level_edit_screen}

# constants
OldLace = [0xFD, 0xF5, 0xE6]


def drawing(screen, screen_to_draw):
##    print("Attempt to process screen")
##    print(screen)
    screen.fill(OldLace)  # background

##    print(screen_to_draw)

    screen_funs[screen_to_draw](screen)

    pygame.display.flip()
