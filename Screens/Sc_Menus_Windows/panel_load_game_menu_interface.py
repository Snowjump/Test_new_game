## Among Myth and Wonder
## panel_load_game_menu_interface

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources.Game_Graphics import graphics_classes
from Resources.Game_Graphics import graphics_funs

from Resources import game_stats


class Load_Game_Menu_Interface_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        x = 21
        y = 351
        self.add_return_to_main_menu_button(x, y)

        x = 361
        y = 298
        self.add_load_files_list(x, y)
        y += 322
        self.add_load_button(x, y)

    def add_return_to_main_menu_button(self, x, y):
        new_button = graphics_classes.Text_Button("Return to Main Menu", graphics_funs.return_to_main_menu,
                                                  "Return to Main Menu", "tnr_font26", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 300, 32, 40, 2, 3)
        self.buttons.append(new_button)

    def add_load_files_list(self, x, y):
        new_list = graphics_classes.Text_List("Load files list", graphics_funs.select_load_file,
                                              game_stats.levels_list,
                                              [x, y, x + 400, y + 319],
                                              tnr_font20, TitleText, NewGameColor, 1, WhiteBorder,
                                              game_stats.level_index, x + 2, y, 396, 24, 22)
        self.lists.append(new_list)

    def add_load_button(self, x, y):
        new_button = graphics_classes.Text_Button("Load", graphics_funs.confirm_loading,
                                                  "Load Game", "tnr_font20", "TitleText", None,
                                                  "BorderMainMenuColor", x, y, 200, 28, 51, 3, 3)
        self.buttons.append(new_button)


    def draw_panel(self, screen):
        self.draw_save_files_list_background(screen)
        self.draw_selected_save_file_info(screen)


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



