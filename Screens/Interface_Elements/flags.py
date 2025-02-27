## Among Myth and Wonder
## flags

import pygame.draw

# from Screens.colors_catalog import *


def adventure_flag(screen, x, y, c, xm, ym, flagpole_color, top_color, bottom_color):
    # x and y are coordinates
    # c is a distance by what flag should be lowered down the flagpole
    # xm and ym coordinates shift during movement animation
    pygame.draw.polygon(screen, flagpole_color,
                        ([x + 3 + xm, y + 33 + ym],
                         [x + 4 + xm, y + 33 + ym],
                         [x + 4 + xm, y + 47 + ym],
                         [x + 3 + xm, y + 47 + ym]))
    pygame.draw.polygon(screen, top_color,
                        ([x + 5 + xm, y + 33 + ym + c],
                         [x + 14 + xm, y + 33 + ym + c],
                         [x + 14 + xm, y + 36 + ym + c],
                         [x + 5 + xm, y + 36 + ym + c]))
    pygame.draw.polygon(screen, bottom_color,
                        ([x + 5 + xm, y + 37 + ym + c],
                         [x + 14 + xm, y + 37 + ym + c],
                         [x + 14 + xm, y + 40 + ym + c],
                         [x + 5 + xm, y + 40 + ym + c]))


def battlefield_flag(screen, x, y, xm, ym, flagpole_color, top_color, bottom_color):
    # x and y are coordinates
    # xm and ym coordinates shift during movement animation
    pygame.draw.polygon(screen, flagpole_color,
                        ([x + 3 + xm, y + 81 + ym],
                         [x + 4 + xm, y + 81 + ym],
                         [x + 4 + xm, y + 95 + ym],
                         [x + 3 + xm, y + 95 + ym]))
    pygame.draw.polygon(screen, top_color,
                        ([x + 5 + xm, y + 81 + ym],
                         [x + 14 + xm, y + 81 + ym],
                         [x + 14 + xm, y + 84 + ym],
                         [x + 5 + xm, y + 84 + ym]))
    pygame.draw.polygon(screen, bottom_color,
                        ([x + 5 + xm, y + 85 + ym],
                         [x + 14 + xm, y + 85 + ym],
                         [x + 14 + xm, y + 88 + ym],
                         [x + 5 + xm, y + 88 + ym]))


def card_flag(screen, x, y, flagpole_color, top_color, bottom_color):
    # x and y are coordinates
    pygame.draw.polygon(screen, flagpole_color,
                        ([x + 3, y + 44],
                         [x + 4, y + 44],
                         [x + 4, y + 60],
                         [x + 3, y + 60]))
    pygame.draw.polygon(screen, top_color,
                        ([x + 5, y + 44],
                         [x + 14, y + 44],
                         [x + 14, y + 47],
                         [x + 5, y + 47]))
    pygame.draw.polygon(screen, bottom_color,
                        ([x + 5, y + 48],
                         [x + 14, y + 48],
                         [x + 14, y + 51],
                         [x + 5, y + 51]))
