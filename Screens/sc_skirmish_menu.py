## Among Myth and Wonder
## sc_skirmish_menu

import pygame.draw, pygame.font

from Screens.colors_catalog import *

from Resources import graphics_obj

pygame.init()

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)


def skirmish_menu_screen(screen):
    screen.fill(NewGameColor)  # background

    # Title
    text_NewGame1 = font26.render("SKIRMISH", True, TitleText)
    screen.blit(text_NewGame1, [335, 40])

    for obj in graphics_obj.menus_objects:
        obj.draw_panel(screen)
        for button in obj.buttons:
            button.draw_button(screen)
        for obj_list in obj.lists:
            obj_list.draw_list(screen)
