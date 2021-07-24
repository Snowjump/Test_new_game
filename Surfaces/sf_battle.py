## Miracle battles


import math
import pygame
import random
import sys

from Resources import game_obj
from Resources import game_stats
from Resources import game_battle

yVar = game_stats.game_window_height - 800

formation_button_zone = [[580, 10, 700, 32]]

fighting_button_zone = [[235, 740 + yVar, 357, 765 + yVar],
                        [235, 770 + yVar, 357, 795 + yVar],
                        [923, 740 + yVar, 1100, 795 + yVar]]

waiting_list_panel_zone = [[360, 740 + yVar, 380, 800 + yVar],
                           [900, 740 + yVar, 920, 800 + yVar]]


def battle_keys(key_action):
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:

            if key_action == 119:  # W
                battle.battle_pov[1] -= 1
            elif key_action == 115:  # S
                battle.battle_pov[1] += 1
            elif key_action == 97:  # A
                battle.battle_pov[0] -= 1
            elif key_action == 100:  # D
                battle.battle_pov[0] += 1
            elif key_action == 113:  # Q
                wait_but()
            elif key_action == 101:  # E
                defend_but()
            elif key_action == 114:  # R
                change_attack_method_but()


def battle_surface_m1(position):
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    if b.attacker_realm == game_stats.player_power:
        player_id = int(b.attacker_id)
    else:
        player_id = int(b.defender_id)

    for army in game_obj.game_armies:
        if army.army_id == player_id:
            a = army

    button_pressed = False

    if b.stage == "Formation":
        # Buttons
        button_numb = 0
        for square in formation_button_zone:
            button_numb += 1
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                formation_button_funs[button_numb]()
                button_pressed = True
                break

        # Lower panel
        if len(b.waiting_list) > 0:
            yVar = game_stats.game_window_height - 800

            lp_funs = lower_panel_buttons["Waiting list"]
            lp_button_zone = lower_panel_zone["Waiting list"]

            button_numb = 0

            for square in lp_button_zone:
                button_numb += 1

                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    lp_funs[button_numb]()
                    button_pressed = True
                    break

            square = [380, 740 + yVar, 900, 800 + yVar]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                index = int(int((position[0] - 380) / 52) + b.waiting_index)
                if index < len(b.waiting_list):
                    b.unit_card = int(index)
                    print("b.unit_card - " + str(b.unit_card) + " pos[0] - " + str(position[0]))

                    b.selected_unit = -1
                    b.selected_unit_alt = ()

                    button_pressed = True

    elif b.stage == "Fighting":
        # Buttons
        button_numb = 0
        for square in fighting_button_zone:
            button_numb += 1
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                fighting_button_funs[button_numb]()
                button_pressed = True
                break

    # Click on game map
    if not button_pressed:
        b.selected_tile = []

        x = math.ceil(position[0] / 96)
        y = math.ceil(position[1] / 96)
        x = int(x) + int(b.battle_pov[0])
        y = int(y) + int(b.battle_pov[1])
        print("Coordinates - x " + str(x) + " y " + str(y))
        b.selected_tile = [int(x), int(y)]

        # Index of selected tile in map list
        x2 = int(b.selected_tile[0])
        y2 = int(b.selected_tile[1])
        TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1
        print("TileNum is " + str(TileNum) + " [x2, y2] = " + str([x2, y2]))

        # game_stats.game_board_panel = ""

        if 0 < x2 <= game_stats.battle_width:
            if 0 < y2 <= game_stats.battle_height:

                if b.stage == "Formation":
                    if b.attacker_realm == game_stats.player_power:
                        starting_positions = list(b.starting_attacking_positions)
                        player_id = int(b.attacker_id)
                    else:
                        starting_positions = list(b.starting_defending_positions)
                        player_id = int(b.defender_id)

                    if b.selected_unit == -1 and b.selected_tile in starting_positions and b.unit_card == -1:
                        if b.battle_map[TileNum].army_id is not None:
                            # Select unit on battlefield
                            b.selected_unit = int(TileNum)
                            b.selected_unit_alt = (int(x2), int(y2))
                            print("selected_unit - " + str(b.selected_unit)
                                  + " selected_unit_alt " + str(b.selected_unit_alt))

                    elif b.selected_unit != -1 and b.selected_tile in starting_positions and b.unit_card == -1:
                        # Select tile, while already selected a unit on battlefield
                        if b.battle_map[TileNum].army_id is None:  # Empty tile
                            unit_num = int(b.battle_map[b.selected_unit].unit_index)  # Previous tile
                            b.battle_map[b.selected_unit].unit_index = None
                            b.battle_map[b.selected_unit].army_id = None

                            for army in game_obj.game_armies:
                                if army.army_id == player_id:
                                    army.units[unit_num].position = [int(x2), int(y2)]  # Unit

                                    b.battle_map[TileNum].unit_index = int(unit_num)  # New selected tile
                                    b.battle_map[TileNum].army_id = int(army.army_id)

                                    b.selected_unit = int(TileNum)
                                    b.selected_unit_alt = (int(x2), int(y2))

                        elif TileNum != b.selected_unit:  # Tile with unit that is not the same as already selected one
                            unit_num = int(b.battle_map[b.selected_unit].unit_index)  # Previous tile
                            b.battle_map[b.selected_unit].unit_index = None
                            b.battle_map[b.selected_unit].army_id = None

                            for army in game_obj.game_armies:
                                if army.army_id == player_id:
                                    army.units[unit_num].position = [int(x2), int(y2)]  # Moving unit
                                    army.units[b.battle_map[TileNum].unit_index].position = []  # Standing unit
                                    b.waiting_list.append(b.battle_map[TileNum].unit_index)  # Change waiting list

                                    b.battle_map[TileNum].unit_index = int(unit_num)  # New selected tile
                                    b.battle_map[TileNum].army_id = int(army.army_id)

                                    b.selected_unit = int(TileNum)
                                    b.selected_unit_alt = (int(x2), int(y2))

                    elif b.selected_unit == -1 and b.selected_tile in starting_positions and b.unit_card != -1:
                        # Select tile, while already selected a unit in waiting list
                        if b.battle_map[TileNum].army_id is None:  # Empty tile
                            for army in game_obj.game_armies:
                                if army.army_id == player_id:
                                    army.units[b.waiting_list[b.unit_card]].position = [int(x2), int(y2)]  # Unit

                                    # New selected tile
                                    b.battle_map[TileNum].unit_index = int(b.waiting_list[b.unit_card])
                                    b.battle_map[TileNum].army_id = int(army.army_id)

                                    del b.waiting_list[b.unit_card]
                                    b.selected_unit = int(TileNum)
                                    b.selected_unit_alt = (int(x2), int(y2))
                                    b.unit_card = -1

                        else:  # Tile already occupied
                            for army in game_obj.game_armies:
                                if army.army_id == player_id:
                                    # Putting unit from waiting list
                                    army.units[b.waiting_list[b.unit_card]].position = [int(x2), int(y2)]
                                    army.units[b.battle_map[TileNum].unit_index].position = []  # Standing unit
                                    b.waiting_list.append(b.battle_map[TileNum].unit_index)  # Change waiting list

                                    # New selected tile
                                    b.battle_map[TileNum].unit_index = int(b.waiting_list[b.unit_card])
                                    b.battle_map[TileNum].army_id = int(army.army_id)

                                    del b.waiting_list[b.unit_card]
                                    b.selected_unit = int(TileNum)
                                    b.selected_unit_alt = (int(x2), int(y2))
                                    b.unit_card = -1

                elif b.stage == "Fighting":
                    if b.realm_in_control == game_stats.player_power:
                        if b.attacker_realm == b.realm_in_control:
                            enemy = b.defender_id
                        else:
                            enemy = b.attacker_id

                        if [x2, y2] in b.movement_grid:
                            print("It's in - " + str([x2, y2]))
                            b.move_destination = [int(x2), int(y2)]
                            game_battle.action_order(b, "Move", None)

                        elif b.battle_map[TileNum].army_id == enemy:
                            if b.attack_type_in_use == "Melee":
                                game_battle.melee_attack_preparation(b, TileNum, position, x2, y2)

                            elif b.attack_type_in_use == "Ranged":
                                if not game_battle.surrounded_by_enemy(b):
                                    game_battle.ranged_attack_preparation(b, TileNum, x2, y2)


def battle_surface_m3(position):
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    button_pressed = False

    # Click on game map
    if not button_pressed:
        b.selected_tile = []

        x = math.ceil(position[0] / 96)
        y = math.ceil(position[1] / 96)
        x = int(x) + int(b.battle_pov[0])
        y = int(y) + int(b.battle_pov[1])
        print("Coordinates - x " + str(x) + " y " + str(y))
        b.selected_tile = [int(x), int(y)]

        # Index of selected tile in map list
        x2 = int(b.selected_tile[0])
        y2 = int(b.selected_tile[1])
        TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1
        print("TileNum is " + str(TileNum))

        # game_stats.game_board_panel = ""

        if 0 < x2 <= game_stats.battle_width:
            if 0 < y2 <= game_stats.battle_height:

                if b.stage == "Formation":
                    if b.attacker_realm == game_stats.player_power:
                        starting_positions = list(b.starting_attacking_positions)
                        player_id = int(b.attacker_id)
                    else:
                        starting_positions = list(b.starting_defending_positions)
                        player_id = int(b.defender_id)

                    # Unselect unit
                    b.selected_unit = -1
                    b.selected_unit_alt = ()
                    b.unit_card = -1


def waiting_index_left():
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    if len(b.waiting_list) > 10:
        if b.waiting_index == 0:
            b.waiting_index = int(len(b.waiting_list) - 10)
        else:
            b.waiting_index -= 1

    print("waiting_index - " + str(b.waiting_index))


def waiting_index_right():
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    if len(b.waiting_list) > 10:
        if b.waiting_index == len(b.waiting_list) - 10:
            b.waiting_index = 0
        else:
            b.waiting_index += 1

    print("waiting_index - " + str(b.waiting_index))


def start_battle_but():
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    if len(b.waiting_list) == 0:
        b.stage = "Fighting"
        print("stage - " + str(b.stage))
        b.selected_tile = []
        b.selected_unit = -1
        b.selected_unit_alt = ()

        fill_morale(b)

        # Form queue
        game_battle.form_queue(b)

        game_battle.advance_queue(b)


def fill_morale(b):
    for army in game_obj.game_armies:
        if army.army_id == b.attacker_id or army.army_id == b.defender_id:
            for unit in army.units:
                unit.leadership = float(unit.base_leadership)
                unit.morale = float(unit.leadership)


def wait_but():
    print("wait_but")
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    if b.realm_in_control == game_stats.player_power:
        game_battle.complete_turn(b, 0.5)


def defend_but():
    print("defend_but")
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    # TODO: Increase defence

    if b.realm_in_control == game_stats.player_power:
        game_battle.action_order(b, "Defend", None)
        # game_battle.complete_turn(b, 1.0)


def change_attack_method_but():
    print("wait_but")
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    if b.realm_in_control == game_stats.player_power:
        for army in game_obj.game_armies:
            if army.army_id == b.queue[0].army_id:
                if b.attack_type_index + 1 == len(army.units[b.queue[0].number].attacks):
                    b.attack_type_index = 0
                else:
                    b.attack_type_index += 1

                b.attack_type_in_use = army.units[b.queue[0].number].attacks[b.attack_type_index].attack_type
                b.cur_effective_range = army.units[b.queue[0].number].attacks[b.attack_type_index].effective_range
                b.cur_range_limit = army.units[b.queue[0].number].attacks[b.attack_type_index].range_limit


formation_button_funs = {1: start_battle_but}

fighting_button_funs = {1: wait_but,
                        2: defend_but,
                        3: change_attack_method_but}

waiting_list_panel_funs = {1: waiting_index_left,
                           2: waiting_index_right}


lower_panel_buttons = {"Waiting list": waiting_list_panel_funs}


lower_panel_zone = {"Waiting list": waiting_list_panel_zone}
