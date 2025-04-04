## Among Myth and Wonder
## panel_entrance_menu_buttons

import sys
import glob

from Screens.fonts_catalog import *

from Resources.Game_Graphics import graphics_classes, graphics_basic
from Resources import game_stats
from Resources import start_new_level


class Entrance_Menu_Buttons_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        # Create new button
        x = 270
        y = 213
        self.add_skirmish_menu_button(x, y)
        y += 50
        self.add_create_level_button(x, y)
        y += 50
        self.add_settings_button(x, y)
        y += 50
        self.add_credits_button(x, y)
        y += 50
        self.add_exit_button(x, y)

    def add_skirmish_menu_button(self, x, y):
        new_button = graphics_classes.Text_Button("Skirmish button", open_new_game_skirmish,
                                                  "Skirmish", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 101, 2, 3)
        self.buttons.append(new_button)

    def add_create_level_button(self, x, y):
        new_button = graphics_classes.Text_Button("Create level button", open_create_level,
                                                  "Create level", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 85, 2, 3)
        self.buttons.append(new_button)

    def add_settings_button(self, x, y):
        new_button = graphics_classes.Text_Button("Settings button", open_settings,
                                                  "Settings", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 106, 2, 3)
        self.buttons.append(new_button)

    def add_credits_button(self, x, y):
        new_button = graphics_classes.Text_Button("Credits button", open_credits,
                                                  "Credits", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 109, 2, 3)
        self.buttons.append(new_button)

    def add_exit_button(self, x, y):
        new_button = graphics_classes.Text_Button("Exit button", exit_app,
                                                  "Exit", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 125, 2, 3)
        self.buttons.append(new_button)


def open_new_game_skirmish():
    game_stats.selected_character = None

    game_stats.current_screen = "Skirmish"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "skirmish_menu_screen"

    game_stats.level_index = 0
    game_stats.levels_list = glob.glob("Levels/Skirmish/*.dat")
    # print("1 level_list: " + str(game_stats.levels_list))
    # for line in game_stats.levels_list:
    # print(str(line))
    # line = str(line[16:-4])
    # print(str(line))
    # print("2/vel_list: " + str(game_stats.levels_list))
    game_stats.levels_list = [w.replace(w, w[16:-4]) for w in game_stats.levels_list]
    # print("3 level_list: " + str(game_stats.levels_list))
    # for line in game_stats.levels_list:
    # print(str(line))

    start_new_level.gather_level_information("Skirmish", game_stats.levels_list[game_stats.level_index])
    graphics_basic.init_skirmish_menu_graphics()

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def open_create_level():
    # game_stats.selected_character = None

    game_stats.current_screen = "Create Level"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "create_level_screen"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def open_settings():
    game_stats.current_screen = "Settings"
    game_stats.screen_to_draw = "settings_screen"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def open_credits():
    game_stats.current_screen = "Credits"
    game_stats.screen_to_draw = "credits_screen"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def exit_app():
    pygame.quit()
    sys.exit()
