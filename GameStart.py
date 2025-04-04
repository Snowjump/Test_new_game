## Among Myth and Wonder
## GameStart

# import sys
import pygame
# import os
import math
# from pygame.locals import *

from Resources import game_stats
from Resources import update_gf_menus
from Resources.Game_Graphics import graphics_basic
from Resources.Game_Start import game_controls, display_graphics
from Resources.Game_Start import game_time


fpsClock = pygame.time.Clock()

# display constants
game_stats.screen_to_draw = "main_menu_screen"
screen = (0, 0)


def init_window():
    # Sound module, must be executed before pygame.init()
    # Source: https://proproprogs.ru/modules/dobavlyaem-zvuk-v-igrovoy-process-moduli-mixer-i-music
    pygame.mixer.pre_init(44100, -16, 1, 512)

    pygame.init()
    ##    game_stats.start_time = pygame.time.get_ticks()

    global screen

    screen = pygame.display.set_mode((game_stats.game_window_width, game_stats.game_window_height))
    pygame.display.set_caption('Among Myth and Wonder videogame')

    graphics_basic.init_entrance_menu_graphics()

    # print("End of init_window()")
    # print(screen)


def main_action():
    global screen

    while 1:
        # all events happen below
        game_controls.control_input()

        game_time.time_update()

        game_stats.mouse_position = pygame.mouse.get_pos()

        # all graphics perform below
        display_graphics.drawing(screen, game_stats.screen_to_draw)

        # frames per second
        fpsClock.tick(60)

        # FPS
        if game_stats.fps_status:
            game_stats.fps = math.ceil(fpsClock.get_fps() * 100) / 100


# game start
def main():
    init_window()
    main_action()


# prepare art pictures for menu screens
update_gf_menus.update_menus_art()


# start everything
if __name__ == '__main__':
    main()
