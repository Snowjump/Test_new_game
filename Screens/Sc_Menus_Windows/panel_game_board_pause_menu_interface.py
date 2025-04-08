## Among Myth and Wonder
    ## panel_game_board_pause_menu_interface

import glob
import math

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources.Game_Graphics import graphics_classes, graphics_basic, graphics_obj
from Resources.Game_Graphics import graphics_funs

from Resources.Save_Load import save_game

from Resources import game_stats
from Resources import update_gf_menus
from Resources import update_gf_game_board


class Game_Board_Pause_Menu_Interface_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        x = 21
        y = 251
        self.add_return_button(x, y)
        y += 50
        self.add_save_game(x, y)
        y += 50
        self.add_load_game(x, y)
        y += 50
        self.add_exit_to_main_menu_button(x, y)

    def add_return_button(self, x, y):
        new_button = graphics_classes.Text_Button("Return", return_to_game_board,
                                                  "Return", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 118, 2, 3)
        self.buttons.append(new_button)

    def add_save_game(self, x, y):
        new_button = graphics_classes.Text_Button("Save Game", save_game_submenu,
                                                  "Save Game", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 91, 2, 3)
        self.buttons.append(new_button)

    def add_load_game(self, x, y):
        new_button = graphics_classes.Text_Button("Load Game", load_game_submenu,
                                                  "Load Game", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 91, 2, 3)
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
    game_stats.level_info = None
    game_stats.pause_status = bool(game_stats.pause_last_status)
    game_stats.strategy_mode = True
    graphics_obj.menus_objects = []


def save_game_submenu():
    panel = graphics_funs.find_graphics_object("Game board pause menu", graphics_obj.menus_objects)
    save_button = graphics_funs.find_graphics_object("Save Game", panel.buttons)
    save_button.border_color = "HighlightOption"
    load_button = graphics_funs.find_graphics_object("Load Game", panel.buttons)
    load_button.border_color = "BorderMainMenuColor"

    graphics_basic.remove_specific_objects(["Load game submenu"], graphics_obj.menus_objects)

    game_stats.level_index = 0
    game_stats.levels_list = glob.glob("*.svfl")
    game_stats.level_info = None
    graphics_basic.prepare_save_game_submenu_interface()


def load_game_submenu():
    panel = graphics_funs.find_graphics_object("Game board pause menu", graphics_obj.menus_objects)
    load_button = graphics_funs.find_graphics_object("Load Game", panel.buttons)
    load_button.border_color = "HighlightOption"
    save_button = graphics_funs.find_graphics_object("Save Game", panel.buttons)
    save_button.border_color = "BorderMainMenuColor"

    graphics_basic.remove_specific_objects(["Save game submenu"], graphics_obj.menus_objects)

    game_stats.level_index = 0
    game_stats.levels_list = glob.glob("*.svfl")
    game_stats.level_info = None
    graphics_basic.prepare_load_game_submenu_interface()


def exit_to_main_menu():
    game_stats.current_screen = "Entrance Menu"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "main_menu_screen"
    game_stats.level_info = None
    game_stats.right_window = ""
    game_stats.selected_tile = []
    graphics_basic.init_entrance_menu_graphics()
    update_gf_menus.update_menus_art()

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


class Save_Game_Interface_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        x = 361
        y = 263
        self.add_save_file_name_text_box(x, y)
        y += 35
        self.add_save_files_list(x, y)
        y += 322
        self.add_save_button(x, y)

    def add_save_file_name_text_box(self, x, y):
        new_button = graphics_classes.Text_Box("Save filename text box", "tnr_font20", "TitleText", "FieldColor",
                                               "BorderMainMenuColor", x, y, 400, 28, 4, 4, 2)
        self.text_boxes.append(new_button)

    def add_save_files_list(self, x, y):
        new_list = graphics_classes.Text_List("Save files list", select_save_file, game_stats.levels_list,
                                              [x, y, x + 400, y + 319],
                                              tnr_font20, TitleText, NewGameColor, 1, WhiteBorder,
                                              game_stats.level_index, x + 2, y, 396, 24, 22)
        self.lists.append(new_list)

    def add_save_button(self, x, y):
        new_button = graphics_classes.Text_Button("Save", confirm_saving,
                                                  "Save Game", "tnr_font20", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 200, 28, 51, 3, 3)
        self.buttons.append(new_button)

    def draw_panel(self, screen):
        self.draw_subtitle(screen)
        self.draw_save_files_list_background(screen)
        self.draw_selected_save_file_info(screen)

    def draw_subtitle(self, screen):
        text_NewGame1 = tnr_font26.render("Save Game", True, TitleText)
        screen.blit(text_NewGame1, [735, 51])

    def draw_save_files_list_background(self, screen):
        x = 361
        y = 295
        pygame.draw.polygon(screen, MainMenuColor, [[x, y], [x + 400, y], [x + 400, y + 320], [x, y + 320]])

    def draw_selected_save_file_info(self, screen):
        if game_stats.level_info:
            x = 767
            y = 295
            pygame.draw.polygon(screen, MainMenuColor, [[x, y], [x + 400, y], [x + 400, y + 320], [x, y + 320]])
            x += 3
            y += 3
            text_line = tnr_font20.render(game_stats.level_info.level_name, True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text_line = tnr_font20.render(str(game_stats.level_info.timestamp), True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text_line = tnr_font20.render(game_stats.level_info.level_type, True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text = "Year " + str(game_stats.level_info.game_year) + " | Month " + str(game_stats.level_info.game_month)
            text_line = tnr_font20.render(text, True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text = "Map size " + str(game_stats.level_info.cur_level_width) +\
                   "x" + str(game_stats.level_info.cur_level_height)
            text_line = tnr_font20.render(text, True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text = "Game version " + str(game_stats.level_info.game_version_major) + "." +\
                   str(game_stats.level_info.game_version_minor) + "." + str(game_stats.level_info.game_version_micro)
            text_line = tnr_font20.render(text, True, DarkText)
            screen.blit(text_line, [x, y])


def select_save_file(self, position):
    y_axis = position[1]
    y_axis -= 295
    # print(str(y_axis))
    y_axis = math.ceil(y_axis / 24)
    # print(str(y_axis))
    # print("len(game_stats.levels_list) - " + str(len(game_stats.levels_list)))
    # print("game_stats.level_index - " + str(game_stats.level_index))
    if (y_axis - 1 != self.item_index and y_axis <= len(self.obj_list)) \
            or (y_axis - 1 == 0 and len(self.obj_list) == 1):
        self.item_index = int(y_axis - 1)
        game_stats.level_index = self.item_index
        # print("game_stats.level_index = " + str(game_stats.level_index))
        panel = graphics_funs.find_graphics_object("Save game submenu", graphics_obj.menus_objects)
        filename_text_box = graphics_funs.find_graphics_object("Save filename text box", panel.text_boxes)
        filename_text_box.text = str(self.obj_list[self.item_index][:-5])
        save_game.get_save_info(filename_text_box.text + ".svfl")
        print("item_index - " + str(self.item_index))


def confirm_saving():
    panel = graphics_funs.find_graphics_object("Save game submenu", graphics_obj.menus_objects)
    filename_text_box = graphics_funs.find_graphics_object("Save filename text box", panel.text_boxes)
    save_game.save_current_game(filename_text_box.text)
    filename_text_box.text = ""
    # Update save files list
    game_stats.levels_list = glob.glob("*.svfl")
    save_files_list = graphics_funs.find_graphics_object("Save files list", panel.lists)
    save_files_list.update_objects(game_stats.levels_list)


class Load_Game_Interface_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        x = 361
        y = 263
        y += 35
        self.add_load_files_list(x, y)
        y += 322
        self.add_load_button(x, y)

    def add_load_files_list(self, x, y):
        new_list = graphics_classes.Text_List("Load files list", select_load_file, game_stats.levels_list,
                                              [x, y, x + 400, y + 319],
                                              tnr_font20, TitleText, NewGameColor, 1, WhiteBorder,
                                              game_stats.level_index, x + 2, y, 396, 24, 22)
        self.lists.append(new_list)

    def add_load_button(self, x, y):
        new_button = graphics_classes.Text_Button("Load", confirm_loading,
                                                  "Load Game", "tnr_font20", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 200, 28, 51, 3, 3)
        self.buttons.append(new_button)


    def draw_panel(self, screen):
        self.draw_subtitle(screen)
        self.draw_save_files_list_background(screen)
        self.draw_selected_save_file_info(screen)


    def draw_subtitle(self, screen):
        text_NewGame1 = tnr_font26.render("Load Game", True, TitleText)
        screen.blit(text_NewGame1, [735, 51])


    def draw_save_files_list_background(self, screen):
        x = 361
        y = 295
        pygame.draw.polygon(screen, MainMenuColor, [[x, y], [x + 400, y], [x + 400, y + 320], [x, y + 320]])


    def draw_selected_save_file_info(self, screen):
        if game_stats.level_info:
            x = 767
            y = 295
            pygame.draw.polygon(screen, MainMenuColor, [[x, y], [x + 400, y], [x + 400, y + 320], [x, y + 320]])
            x += 3
            y += 3
            text_line = tnr_font20.render(game_stats.level_info.level_name, True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text_line = tnr_font20.render(str(game_stats.level_info.timestamp), True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text_line = tnr_font20.render(game_stats.level_info.level_type, True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text = "Year " + str(game_stats.level_info.game_year) + " | Month " + str(game_stats.level_info.game_month)
            text_line = tnr_font20.render(text, True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text = "Map size " + str(game_stats.level_info.cur_level_width) +\
                   "x" + str(game_stats.level_info.cur_level_height)
            text_line = tnr_font20.render(text, True, DarkText)
            screen.blit(text_line, [x, y])
            y += 24
            text = "Game version " + str(game_stats.level_info.game_version_major) + "." +\
                   str(game_stats.level_info.game_version_minor) + "." + str(game_stats.level_info.game_version_micro)
            text_line = tnr_font20.render(text, True, DarkText)
            screen.blit(text_line, [x, y])


def select_load_file(self, position):
    y_axis = position[1]
    y_axis -= 295
    # print(str(y_axis))
    y_axis = math.ceil(y_axis / 24)
    # print(str(y_axis))
    # print("len(game_stats.levels_list) - " + str(len(game_stats.levels_list)))
    # print("game_stats.level_index - " + str(game_stats.level_index))
    if (y_axis - 1 != self.item_index and y_axis <= len(self.obj_list)) \
            or (y_axis - 1 == 0 and len(self.obj_list) == 1):
        self.item_index = int(y_axis - 1)
        game_stats.level_index = self.item_index
        # print("game_stats.level_index = " + str(game_stats.level_index))
        save_file = str(self.obj_list[self.item_index])
        save_game.get_save_info(save_file)


def confirm_loading():
    if game_stats.level_info:
        save_game.load_game(game_stats.level_info)

        game_stats.current_screen = "Game Board"
        game_stats.screen_to_draw = "game_board_screen"
        game_stats.level_info = None
        game_stats.strategy_mode = True
        graphics_obj.menus_objects = []

        # Update visuals
        update_gf_game_board.update_misc_sprites()
        update_gf_game_board.update_sprites()
