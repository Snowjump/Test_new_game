## Among Myth and Wonder
## sc_game_board_pause_menu

from Screens.colors_catalog import *

from Resources import graphics_obj


def game_board_pause_menu_screen(screen):
    screen.fill(NewGameColor)  # background

    for obj in graphics_obj.menus_objects:
        obj.draw_panel(screen)
        for button in obj.buttons:
            button.draw_button(screen)
