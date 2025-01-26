## Among Myth and Wonder
## army_exchange

import math

from Resources import game_stats
from Resources import game_obj
from Resources import game_basic
from Resources import common_selects
from Resources import update_gf_game_board
from Resources.Game_Basic import objs_selects


def army_exchange_panel(position, yVar):
    square = [380, 380 + yVar, 639, 607 + yVar]
    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
        game_stats.button_pressed = True
        # print(str(position[0]) + ", " + str(position[1]))
        x_axis, y_axis = position[0], position[1]
        x_axis -= 380
        y_axis -= (380 + yVar)
        print(str(x_axis) + ", " + str(y_axis))
        x_axis = math.ceil(x_axis / 52)
        y_axis = math.ceil(y_axis / 57)
        print(str(x_axis) + ", " + str(y_axis))

        # Add new units to exchange list
        number = int(y_axis - 1) * 5 + int(x_axis) - 1
        print("army_exchange_panel(): number - " + str(number))
        approaching_army = common_selects.select_army_by_id(game_stats.selected_army)

        if number not in game_stats.second_army_exchange_list:
            if len(approaching_army.units) - len(game_stats.first_army_exchange_list) + \
                    len(game_stats.second_army_exchange_list) < 20:
                game_stats.second_army_exchange_list.append(number)
                game_stats.second_army_exchange_list = sorted(game_stats.second_army_exchange_list,
                                                              reverse=True)
                print("second_army_exchange_list: " + str(game_stats.second_army_exchange_list))
        else:
            game_stats.second_army_exchange_list.remove(number)


def army_exchange_lower_panel(position, yVar):
    if 654 + yVar <= position[1] < 768 + yVar and 430 <= position[0] < 949:

        x_axis, y_axis = position[0], position[1]
        x_axis -= 430
        y_axis -= (654 + yVar)
        print(str(x_axis) + ", " + str(y_axis))
        x_axis = math.ceil(x_axis / 52)
        y_axis = math.ceil(y_axis / 57)
        print(str(x_axis) + ", " + str(y_axis))

        # Add new units to exchange list
        number = int(y_axis - 1) * 10 + int(x_axis) - 1
        print("army_exchange_lower_panel(): number - " + str(number))
        standing_army = common_selects.select_army_by_id(game_stats.selected_second_army)

        if number not in game_stats.first_army_exchange_list:
            if len(standing_army.units) - len(game_stats.second_army_exchange_list) + \
                    len(game_stats.first_army_exchange_list) < 20:
                game_stats.first_army_exchange_list.append(number)
                game_stats.first_army_exchange_list = sorted(game_stats.first_army_exchange_list,
                                                             reverse=True)
                print("first_army_exchange_list: " + str(game_stats.first_army_exchange_list))
        else:
            game_stats.first_army_exchange_list.remove(number)


def complete_army_exchange_but():
    game_stats.game_board_panel = ""

    approaching_army = common_selects.select_army_by_id(game_stats.selected_army)
    approaching_army.action = "Stand"
    approaching_army_ID = int(approaching_army.army_id)
    standing_army = common_selects.select_army_by_id(game_stats.selected_second_army)
    standing_army.action = "Stand"
    standing_army_ID = int(standing_army.army_id)

    for number in game_stats.first_army_exchange_list:
        standing_army.units.append(approaching_army.units.pop(number))

    for number in game_stats.second_army_exchange_list:
        approaching_army.units.append(standing_army.units.pop(number))

    # game_stats.selected_army = -1
    game_stats.selected_second_army = -1
    game_stats.first_army_exchange_list = []
    game_stats.second_army_exchange_list = []
    # game_stats.selected_object = ""
    # game_stats.details_panel_mode = ""

    remove_list = []

    if approaching_army.units:
        game_basic.establish_leader(approaching_army_ID, "Game")
    else:
        # No units left in army
        game_obj.game_map[approaching_army.location].army_id = None
        remove_list.append(approaching_army_ID)
        objs_selects.deselect_army()
        # Update visuals
        update_gf_game_board.remove_regiment_sprites()
        update_gf_game_board.remove_hero_sprites()

    if standing_army.units:
        game_basic.establish_leader(standing_army_ID, "Game")
    else:
        # No units left in army
        game_obj.game_map[standing_army.location].army_id = None
        remove_list.append(standing_army_ID)

    if remove_list:
        game_basic.remove_army(remove_list)
