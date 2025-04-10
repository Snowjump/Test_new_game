## Among Myth and Wonder
## panel_skirmish_menu_interface

import math

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources.Game_Graphics import graphics_classes, graphics_basic, graphics_obj
from Resources.Game_Graphics import graphics_funs
from Resources import game_stats
from Resources import start_new_level


class Skirmish_Menu_Interface_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        # Create new button
        x = 250
        y = 443
        self.add_start_new_game_button(x, y)
        y += 70
        self.add_return_to_main_menu_button(x, y)

        # Create new object list
        x = 80
        y = 85
        self.add_levels_list(x, y)

    def add_start_new_game_button(self, x, y):
        new_button = graphics_classes.Text_Button("Start new game", start_new_game,
                                                  "Start", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 124, 2, 3)
        self.buttons.append(new_button)

    def add_return_to_main_menu_button(self, x, y):
        new_button = graphics_classes.Text_Button("Return to Main Menu", graphics_funs.return_to_main_menu,
                                                  "Return to Main Menu", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 40, 2, 3)
        self.buttons.append(new_button)

    def add_previous_realm_button(self, x, y):
        new_button = graphics_classes.Arrow_Button("Switch to previous realm", switch_to_previous_realm,
                                                   "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                                   x, y, 19, 19, 1, 2)
        self.buttons.append(new_button)

    def add_next_realm_button(self, x, y):
        new_button = graphics_classes.Arrow_Button("Switch to next realm", switch_to_previous_realm,
                                                   "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                                   x, y, 19, 19, 1, 2)
        self.buttons.append(new_button)

    def add_levels_list(self, x, y):
        new_list = graphics_classes.Text_List("Levels list", select_level, game_stats.levels_list, [77, 82, 304, 404],
                                              tnr_font20, TitleText, NewGameColor, 1, WhiteBorder,
                                              game_stats.level_index, x, y, 220, 24, 22)
        self.lists.append(new_list)

    def draw_panel(self, screen):
        ## Level information
        self.draw_details(screen)
        self.draw_realm_selection(screen)
        self.draw_levels_list_background(screen)

    def draw_details(self, screen):
        if game_stats.level_index is not None:
            x = 400
            y = 85
            text_NewGame2 = tnr_font20.render(game_stats.levels_list[game_stats.level_index], True, TitleText)
            screen.blit(text_NewGame2, [x, y])

            y += 24
            text_NewGame2 = tnr_font18.render("Objectives:", True, TitleText)
            screen.blit(text_NewGame2, [x, y])

            y += 22
            text_NewGame2 = tnr_font18.render("Neither lords, nor their servants", True, TitleText)
            screen.blit(text_NewGame2, [x, y])

            y += 22
            text_NewGame2 = tnr_font18.render("shall know your mercy", True, TitleText)
            screen.blit(text_NewGame2, [x, y])

            y += 22
            text_NewGame2 = tnr_font18.render("Conquer all other realms", True, TitleText)
            screen.blit(text_NewGame2, [x, y])

    def draw_realm_selection(self, screen):
        if game_stats.level_index is not None:
            x = 800
            y = 85
            text_skirmish = str(game_stats.start_level_playable_realms) + " playable realms out of " + \
                str(game_stats.start_level_total_realms) + " realms total"

            text_NewGame2 = tnr_font18.render(text_skirmish, True, TitleText)
            screen.blit(text_NewGame2, [x, y])

            # Flag
            x += 46
            y += 24
            pygame.draw.polygon(screen, FlagColors[game_stats.start_level_selected_realm.f_color],
                                [[x, y], [x + 22, y],
                                 [x + 22, y + 8], [x, y + 8]])
            pygame.draw.polygon(screen, FlagColors[game_stats.start_level_selected_realm.s_color],
                                [[x, y + 9], [x + 22, y + 9],
                                 [x + 22, y + 16], [x, y + 16]])

            x += 27
            y -= 1
            text_skirmish = game_stats.start_level_selected_realm.name
            text_NewGame2 = tnr_font18.render(text_skirmish, True, TitleText)
            screen.blit(text_NewGame2, [x, y])

            x -= 27
            y += 22
            text_skirmish = game_stats.start_level_selected_realm.alignment
            text_NewGame2 = tnr_font18.render(text_skirmish, True, TitleText)
            screen.blit(text_NewGame2, [x, y])

    def draw_levels_list_background(self, screen):
        x = 78
        y = 83
        pygame.draw.polygon(screen, MainMenuColor, [[x, y], [x + 224, y], [x + 224, y + 320], [x, y + 320]])


def start_new_game():
    start_new_level.begin_new_level("Skirmish", game_stats.levels_list[game_stats.level_index])

    game_stats.current_screen = "Game Board"
    # print(game_stats.current_screen)
    game_stats.screen_to_draw = "game_board_screen"
    game_stats.start_level_selected_realm = None
    graphics_basic.init_game_board_graphics()
    graphics_obj.menus_objects = []

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()

    game_stats.gf_menus_art = {}


def switch_to_previous_realm():
    if game_stats.level_index is not None:
        start_new_level.skirmish_previous_realm()

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()


def switch_to_next_realm():
    if game_stats.level_index is not None:
        start_new_level.skirmish_next_realm()

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()


def select_level(self, position):
    y_axis = position[1]
    y_axis -= 82
    # print(str(y_axis))
    y_axis = math.ceil(y_axis / 24)
    # print(str(y_axis))
    # print("len(game_stats.levels_list) - " + str(len(game_stats.levels_list)))
    if y_axis - 1 != self.item_index and y_axis <= len(self.obj_list):
        self.item_index = int(y_axis - 1)
        start_new_level.gather_level_information("Skirmish", self.obj_list[self.item_index])
        game_stats.level_index = self.item_index
        # print("item_index - " + str(self.item_index))

    if self.item_index is not None:
        panel = graphics_funs.find_graphics_object("Skirmish menu", graphics_obj.menus_objects)
        button = graphics_funs.find_graphics_object("Switch to previous realm", panel.buttons)
        if not button:
            x = 800
            y = 109
            panel.add_previous_realm_button(x, y)
            x += 21
            panel.add_next_realm_button(x, y)
