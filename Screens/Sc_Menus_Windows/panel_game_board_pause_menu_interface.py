## Among Myth and Wonder
## panel_game_board_pause_menu_interface

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources import graphics_classes
from Resources import game_stats
from Resources import graphics_basic
from Resources import update_gf_menus


class Game_Board_Pause_Menu_Interface_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        x = 21
        y = 251
        self.add_return_button(x, y)
        y += 50
        self.add_exit_to_main_menu_button(x, y)

    def add_return_button(self, x, y):
        new_button = graphics_classes.Text_Button("Return", return_to_game_board,
                                                  "Return", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 118, 2, 3)
        self.buttons.append(new_button)

    def add_exit_to_main_menu_button(self, x, y):
        new_button = graphics_classes.Text_Button("Exit to Main Menu", exit_to_main_menu,
                                                  "Exit to Main Menu", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 48, 2, 3)
        self.buttons.append(new_button)

    def draw_panel(self, screen):
        self.draw_elements(screen)

    def draw_elements(self, screen):
        yVar = game_stats.game_window_height - 800
        pygame.draw.line(screen, LineMainMenuColor1, [342, 51], [342, 751 + yVar], 2)


def return_to_game_board():
    game_stats.current_screen = "Game Board"
    game_stats.screen_to_draw = "game_board_screen"
    game_stats.pause_status = bool(game_stats.pause_last_status)
    game_stats.strategy_mode = True


def exit_to_main_menu():
    game_stats.current_screen = "Entrance Menu"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "main_menu_screen"
    game_stats.right_window = ""
    game_stats.selected_tile = []
    graphics_basic.init_entrance_menu_graphics()
    update_gf_menus.update_menus_art()

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()
