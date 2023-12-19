## Among Myth and Wonder
## GameStart

import sys
import pygame
import os
import math
# from pygame.locals import *

from Resources import display_graphics
from Resources import game_stats
from Resources import update_gf_menus
from Resources.Game_Start import game_controls
from Resources.Game_Start import game_time


fpsClock = pygame.time.Clock()

# display constants
size = width, height = game_stats.game_window_width, game_stats.game_window_height

print("test1")
## screen_to_draw = "main_menu_screen"
game_stats.screen_to_draw = "main_menu_screen"
screen = (0, 0)
print("test2")

# # mouse constants
# mouse_button1_pressed = False
# mouse_button3_pressed = False
# key_pressed = False


def init_window():
    # Sound module, must be executed before pygame.init()
    # Source: https://proproprogs.ru/modules/dobavlyaem-zvuk-v-igrovoy-process-moduli-mixer-i-music
    pygame.mixer.pre_init(44100, -16, 1, 512)

    pygame.init()
    ##    game_stats.start_time = pygame.time.get_ticks()

    global screen

    # # fonts
    # global font10, font12, font14, font15, font16, font17, font18, font20, font26
    # font10 = pygame.font.SysFont('timesnewroman', 10)
    # font12 = pygame.font.SysFont('timesnewroman', 12)
    # font14 = pygame.font.SysFont('timesnewroman', 14)
    # font15 = pygame.font.SysFont('timesnewroman', 15)
    # font16 = pygame.font.SysFont('timesnewroman', 16)
    # font17 = pygame.font.SysFont('timesnewroman', 17)
    # font18 = pygame.font.SysFont('timesnewroman', 18)
    # font20 = pygame.font.SysFont('timesnewroman', 20)
    # font26 = pygame.font.SysFont('timesnewroman', 26)

    size = game_stats.game_window_width, game_stats.game_window_height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Among Myth and Wonder videogame')

    # print("End of init_window()")
    # print(screen)


# game start
def main():
    init_window()
    main_action()


# very important function
def main_action():
    global screen

    while 1:
        # all events happen below
        game_controls.control_input()

        game_time.time_update()

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


# prepare art pictures for menu screens
update_gf_menus.update_menus_art()


# start everything
if __name__ == '__main__':
    main()
