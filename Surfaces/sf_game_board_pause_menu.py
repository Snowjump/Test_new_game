## Among Myth and Wonder
## sf_game_board_pause_menu

from Resources import graphics_obj


def game_board_pause_menu_keys(key_action):
    pass


def game_board_pause_menu_m1(position):
    # print("game_board_pause_menu_m1")
    for obj in graphics_obj.menus_objects:
        for button in obj.buttons:
            button.press_button(position)


def game_board_pause_menu_m3(position):
    print("game_board_pause_menu_m3")
