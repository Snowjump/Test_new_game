## Among Myth and Wonder
## graphics_funs

import pygame
import math

from Resources import game_stats
from Resources import update_gf_game_board

from Resources.Game_Graphics import graphics_basic
from Resources.Game_Graphics import graphics_obj
from Resources.Save_Load import save_game


def draw_panel_objects(screen, graphics_objects_list):
    for obj in graphics_objects_list:
        if hasattr(obj, 'draw_panel'):
            obj.draw_panel(screen)
        for button in obj.buttons:
            button.draw_button(screen)
        for obj_list in obj.lists:
            obj_list.draw_list(screen)
        for text_box in obj.text_boxes:
            text_box.draw_box(screen)


def find_graphics_object(obj_name, obj_list):
    for obj in obj_list:
        if obj.name == obj_name:
            return obj


def key_action_panel(graphics_objects_list, key_action):
    for obj in graphics_objects_list:
        for text_box in obj.text_boxes:
            if text_box.type_text:
                if key_action == 27:  # Escape
                    text_box.deselect_box()
                elif key_action == 8:  # Backspace
                    if text_box.text:  # Remove last character from text line
                        text_box.text = text_box.text[:-1]
                elif key_action == 13:  # Enter
                    text_box.deselect_box()
                else:  # Add a character to text line
                    if game_stats.input_text.isalnum() or game_stats.input_text.isspace():
                        print(str(game_stats.input_text))
                        text_box.text += game_stats.input_text


def m1_single_click(graphics_objects_list, position):
    for obj in graphics_objects_list:
        for button in obj.buttons:
            button.press_button(position)
        for obj_list in obj.lists:
            obj_list.select_element(position)
        for text_box in obj.text_boxes:
            text_box.press_box(position)


def return_to_main_menu():
    game_stats.current_screen = "Entrance Menu"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "main_menu_screen"
    game_stats.levels_list = []
    graphics_basic.init_entrance_menu_graphics()

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


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
        graphics_basic.init_game_board_graphics()
        graphics_obj.menus_objects = []

        # Update visuals
        update_gf_game_board.update_misc_sprites()
        update_gf_game_board.update_sprites()
