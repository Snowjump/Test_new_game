## Among Myth and Wonder
## sf_battle

import math
import pygame
import random
import sys

from Resources import game_obj
from Resources import game_stats
from Resources import game_battle
from Resources import game_classes
from Resources import game_basic
from Resources import graphics_basic
from Resources import algo_movement_range
from Resources import battle_abilities_hero
from Resources import battle_abilities_regiment
from Resources import update_gf_game_board
from Resources import update_gf_battle
from Resources import game_pathfinding

from Content import ability_catalog
from Content import ability_desc_cat_hero
from Content import ability_desc_cat_regiment
from Content import battle_result_scripts
from Content import exploration_catalog
from Content import reward_catalog
from Content import siege_warfare_catalog

from Content.Quests import knight_lords_quest_result_scripts

from Strategy_AI import strategy_logic

yVar = game_stats.game_window_height - 800

formation_button_zone = [[580, 10, 700, 32],
                         [1, 677 + yVar, 90, 736 + yVar],
                         [1, 739 + yVar, 90, 798 + yVar]]

fighting_button_zone = [[235, 740 + yVar, 357, 765 + yVar],
                        [235, 770 + yVar, 357, 795 + yVar],
                        [923, 740 + yVar, 1100, 795 + yVar],
                        [1103, 740 + yVar, 1195, 795 + yVar],
                        [74, 740 + yVar, 231, 795 + yVar]]

waiting_list_panel_zone = [[360, 740 + yVar, 380, 800 + yVar],
                           [900, 740 + yVar, 920, 800 + yVar]]

battle_end_window_zone = [[590, 135, 690, 157]]

ability_menu_window_zone = [[1076, 106, 1095, 125],
                            [970, 106, 1070, 125]]

regiment_info_window_zone = [[1254, 85, 1273, 104],
                             [646, 365, 665, 365 + 19],
                             [786, 365, 805, 365 + 19],
                             [1020, 205, 1039, 205 + 19],
                             [1160, 205, 1179, 205 + 19],
                             [1020, 365, 1039, 365 + 19],
                             [1160, 365, 1179, 365 + 19],
                             [1020, 505, 1039, 505 + 19],
                             [1160, 505, 1179, 505 + 19]]

siege_equipment_menu_window_zone = [[816, 206, 835, 225]]


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
                prepare_change_attack_method()

            elif key_action == 120:  # key - X
                print("game_stats.fps_status - " + str(game_stats.fps_status))
                if game_stats.fps_status:
                    game_stats.fps_status = False
                else:
                    game_stats.fps_status = True


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

    b.button_pressed = False

    if b.stage == "Formation":
        # Buttons
        button_numb = 0
        for square in formation_button_zone:
            button_numb += 1
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                b.button_pressed = True  # Important to stay here before next function
                formation_button_funs[button_numb]()
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
                    b.button_pressed = True  # Important to stay here before next function
                    lp_funs[button_numb]()
                    break

            square = [380, 740 + yVar, 900, 800 + yVar]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                index = int(int((position[0] - 380) / 52) + b.waiting_index)
                if index < len(b.waiting_list):
                    b.unit_card = int(index)
                    print("b.unit_card - " + str(b.unit_card) + " pos[0] - " + str(position[0]))

                    b.selected_unit = -1
                    b.selected_unit_alt = ()
                    b.preparation_siege_machine = None

                    b.button_pressed = True

    elif b.stage == "Fighting":
        # Buttons
        # print(b.stage == "Fighting")
        button_numb = 0
        for square in fighting_button_zone:
            button_numb += 1
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                b.button_pressed = True  # Important to stay here before next function
                fighting_button_funs[button_numb]()
                break

        print("After fighting_button_zone")
        # Window
        if b.battle_window is not None:
            print("b.battle_window is not None, it's " + str(b.battle_window))
            square = click_window_zone[b.battle_window]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                # print("square[0] < position[0] < square[2] and square[1] < position[1] < square[3]")
                b.button_pressed = True

                w_funs = window_buttons[b.battle_window]
                w_button_zone = window_zone[b.battle_window]

                button_numb = 0
                for square in w_button_zone:
                    # print("square from w_button_zone - " + str(square))
                    button_numb += 1

                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        w_funs[button_numb]()

                        break

                if b.battle_window == "Ability menu":
                    square = [455, 127, 699, 600]  # Ability selection
                    square1 = [187, 127, 431, 600]  # Ability school selection
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        # Select ability
                        y_axis = position[1]
                        y_axis -= 127
                        print("y_axis - " + str(y_axis))
                        if y_axis % 44 <= 40:
                            y_axis = math.ceil(y_axis / 44)
                            print("index - " + str(y_axis))
                            hero = None
                            the_unit = None
                            for army in game_obj.game_armies:
                                if army.army_id == b.queue[0].army_id:
                                    if b.queue[0].obj_type == "Regiment":
                                        the_unit = army.units[b.queue[0].number]
                                    elif b.queue[0].obj_type == "Hero":
                                        hero = army.hero
                                    break
                            # if y_axis <= len(hero.abilities):
                            if y_axis <= len(b.list_of_abilities):
                                b.selected_ability = str(b.list_of_abilities[y_axis - 1])
                                # b.selected_ability = str(hero.abilities[y_axis - 1])
                                if b.queue[0].obj_type == "Hero":
                                    b.ability_description = ability_desc_cat_hero.script_cat[b.selected_ability](hero)
                                elif b.queue[0].obj_type == "Regiment":
                                    b.ability_description = ability_desc_cat_regiment.script_cat[b.selected_ability](the_unit)

                    elif square1[0] < position[0] < square1[2] and square1[1] < position[1] < square1[3]:
                        # Select ability school
                        y_axis = position[1]
                        y_axis -= 127
                        print("y_axis - " + str(y_axis))
                        if y_axis % 44 <= 40:
                            y_axis = math.ceil(y_axis / 44)
                            print("index - " + str(y_axis))
                            hero = None
                            the_unit = None
                            for army in game_obj.game_armies:
                                if army.army_id == b.queue[0].army_id:
                                    if b.queue[0].obj_type == "Regiment":
                                        the_unit = army.units[b.queue[0].number]
                                    elif b.queue[0].obj_type == "Hero":
                                        hero = army.hero
                                    break

                            b.list_of_abilities = []

                            if y_axis <= len(b.list_of_schools):
                                b.selected_school = str(b.list_of_schools[y_axis - 1])
                                if b.queue[0].obj_type == "Hero":
                                    for ability in hero.abilities:
                                        if b.selected_school == "Overall":
                                            b.list_of_abilities.append(str(ability))
                                            # Update visuals
                                            update_gf_battle.add_ability_misc_sprites(ability)
                                        elif ability_catalog.ability_cat[ability].school == b.selected_school:
                                            b.list_of_abilities.append(str(ability))
                                            # Update visuals
                                            update_gf_battle.add_school_misc_sprites(b.selected_school)
                                            update_gf_battle.add_ability_misc_sprites(ability)

                                    # Abilities from artifacts
                                    if len(hero.inventory) > 0:
                                        for artifact in hero.inventory:
                                            for effect in artifact.effects:
                                                if effect.application == "Cast spells":
                                                    if b.selected_school == "Overall":
                                                        for ability in effect.application_tags:
                                                            b.list_of_abilities.append(str(ability))
                                                            # Update visuals
                                                            update_gf_battle.add_ability_misc_sprites(ability)
                                                    else:
                                                        for ability in effect.application_tags:
                                                            if ability_catalog.ability_cat[ability].school == b.selected_school:
                                                                b.list_of_abilities.append(str(ability))
                                                                # Update visuals
                                                                update_gf_battle.add_school_misc_sprites(b.selected_school)
                                                                update_gf_battle.add_ability_misc_sprites(ability)

                                    b.selected_ability = str(b.list_of_abilities[0])
                                    b.ability_description = ability_desc_cat_hero.script_cat[b.selected_ability](hero)

                                elif b.queue[0].obj_type == "Regiment":
                                    for ability in the_unit.abilities:
                                        if b.selected_school == "Overall":
                                            b.list_of_abilities.append(str(ability))
                                        elif ability_catalog.ability_cat[ability].school == b.selected_school:
                                            b.list_of_abilities.append(str(ability))

                                    b.selected_ability = str(b.list_of_abilities[0])
                                    b.ability_description = ability_desc_cat_regiment.script_cat[b.selected_ability](the_unit)

                elif b.battle_window == "Siege equipment menu":
                    square = [755, 204, 814, 500]  # Ability selection
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        pick_up_siege_equipment(b, position)

    # Click on game map
    if not b.button_pressed and b.battle_window is None:
        b.selected_tile = []

        x = math.ceil((position[0] + 1) / 96)
        y = math.ceil((position[1] + 1) / 96)
        print("Intermediate - x " + str(x) + ", y " + str(y) +
              "; battle_pov - x " + str(b.battle_pov[0]) + ", y " + str(b.battle_pov[1]))
        x = int(x) + int(b.battle_pov[0])
        y = int(y) + int(b.battle_pov[1])
        print("Coordinates - x " + str(x) + ", y " + str(y))
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
                    # print("player_id - " + str(player_id))

                    if b.preparation_siege_machine is not None and b.selected_tile in starting_positions:
                        if b.battle_map[TileNum].army_id is not None:
                            # Equip regiment with siege machine
                            equip_regiment(b, TileNum)

                    elif b.selected_unit == -1 and b.selected_tile in starting_positions and b.unit_card == -1:
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
                                    break

                        elif TileNum != b.selected_unit:  # Tile with unit that is not the same as already selected one
                            # print("Tile with unit that is not the same as already selected one")
                            unit_num = int(b.battle_map[b.selected_unit].unit_index)  # Previous tile
                            b.battle_map[b.selected_unit].unit_index = None
                            b.battle_map[b.selected_unit].army_id = None

                            # print("len(game_obj.game_armies) - " + str(len(game_obj.game_armies)))
                            for army in game_obj.game_armies:
                                # print("army.owner - " + str(army.owner)
                                #       + "; army.army_id - " + str(army.army_id))
                                if army.army_id == player_id:
                                    army.units[unit_num].position = [int(x2), int(y2)]  # Moving unit
                                    army.units[b.battle_map[TileNum].unit_index].position = []  # Standing unit
                                    b.waiting_list.append(b.battle_map[TileNum].unit_index)  # Change waiting list
                                    # print("waiting_list: " + str(b.waiting_list))
                                    if army.units[b.battle_map[TileNum].unit_index].siege_engine is not None:
                                        if army.units[b.battle_map[TileNum].unit_index].siege_engine == "Siege tower":
                                            b.available_siege_towers += 1
                                        elif army.units[b.battle_map[TileNum].unit_index].siege_engine == "Battering ram":
                                            b.available_battering_rams += 1
                                        army.units[b.battle_map[TileNum].unit_index].siege_engine = None

                                    b.battle_map[TileNum].unit_index = int(unit_num)  # New selected tile
                                    b.battle_map[TileNum].army_id = int(army.army_id)

                                    b.selected_unit = int(TileNum)
                                    b.selected_unit_alt = (int(x2), int(y2))
                                    break

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
                                    break

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
                    if b.cursor_function is None:
                        if b.realm_in_control == game_stats.player_power and b.ready_to_act:
                            if b.attacker_realm == b.realm_in_control:
                                enemy = b.defender_id
                            else:
                                enemy = b.attacker_id

                            # print("b.movement_grid - " + str(b.movement_grid))
                            # if b.movement_grid:
                            if [x2, y2] in b.movement_grid:
                                print("It's in movement grid - " + str([x2, y2]))
                                b.move_destination = [int(x2), int(y2)]
                                b.ready_to_act = False

                                # game_battle.prepare_takeoff(b)  # For flyers

                                game_battle.action_order(b, "Move", None)

                            elif m1_click_structure(b, TileNum, x2, y2):
                                pass

                            elif b.battle_map[TileNum].army_id == enemy:
                                if b.attack_type_in_use == "Melee":
                                    game_battle.melee_attack_preparation(b, TileNum, position, x2, y2)

                                elif b.attack_type_in_use == "Ranged":
                                    if not game_battle.surrounded_by_enemy(b):
                                        distance = (math.sqrt(
                                            ((b.battle_map[TileNum].posxy[0] - b.queue[0].position[0]) ** 2) + (
                                                    (b.battle_map[TileNum].posxy[1] - b.queue[0].position[1]) ** 2)))
                                        if distance <= b.cur_range_limit:
                                            b.ready_to_act = False
                                            game_battle.ranged_attack_preparation(b, TileNum, x2, y2)
                    elif b.cursor_function == "Execute ability":
                        print("Execute ability")
                        print(b.selected_ability)
                        for action in ability_catalog.ability_cat[b.selected_ability].action:
                            hero = None
                            the_unit = None
                            for army in game_obj.game_armies:
                                if army.army_id == b.queue[0].army_id:
                                    hero = army.hero
                                    if b.queue[0].obj_type == "Regiment":
                                        the_unit = army.units[b.queue[0].number]
                                    break

                            if b.queue[0].obj_type == "Regiment":
                                battle_abilities_regiment.script_cat[action.script](b, TileNum, hero, the_unit)
                            elif b.queue[0].obj_type == "Hero":
                                battle_abilities_hero.script_cat[action.script](b, TileNum, hero)
                            # b.list_of_schools = []
                            # b.list_of_abilities = []
                            # b.ability_index = 0
                            # b.school_index = 0
                            # b.selected_school = None
                            # b.selected_ability = None
                        b.ready_to_act = False
                        game_battle.action_order(b, "Pass", None)


def battle_surface_m3(position):
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    b.button_pressed = False

    if b.stage == "Fighting":
        # Window
        if b.battle_window is not None:
            square = [640, 70, 1270, 600]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                b.button_pressed = True

    # Click on game map
    if not b.button_pressed:
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

                elif b.stage == "Fighting":
                    if b.realm_in_control == game_stats.player_power and b.ready_to_act:
                        if b.battle_map[TileNum].army_id is not None:
                            fill_regiment_information(b, TileNum)
                        else:
                            b.unit_info = None
                            b.attack_info = None
                            b.battle_window = None


def m1_click_structure(b, TileNum, x2, y2):
    result = False
    if b.battle_type == "Siege":
        if b.realm_in_control == game_stats.player_power:
            if b.queue[0].obj_type == "Regiment" and b.ready_to_act:
                # print("Regiment attacking the gates")
                for army in game_obj.game_armies:
                    if army.army_id == b.queue[0].army_id:
                        unit = army.units[b.queue[0].number]
                        if unit.siege_engine is not None:
                            if unit.siege_engine == "Battering ram":
                                if b.battle_map[TileNum].map_object is not None:
                                    print(b.battle_map[TileNum].map_object.obj_name)
                                    if b.battle_map[TileNum].map_object.obj_name in ["Palisade_gates"]:
                                        approach = [x2 - 1, y2]

                                        if approach in b.movement_grid:
                                            game_battle.disengage(b, b.queue[0].position)
                                            b.ready_to_act = False
                                            b.attacking_rotate.append(b.queue[0].number)
                                            b.move_destination = [int(approach[0]), int(approach[1])]
                                            b.target_destination = [int(x2), int(y2)]
                                            game_battle.action_order(b, "Move", "Break the gates")
                                            result = True

                                        elif approach == b.queue[0].position:
                                            game_battle.disengage(b, b.queue[0].position)
                                            b.ready_to_act = False
                                            b.attacking_rotate.append(b.queue[0].number)
                                            b.target_destination = [int(x2), int(y2)]
                                            game_battle.action_order(b, "Rotate", "Break the gates")
                                            result = True

                            elif unit.siege_engine == "Siege tower":
                                if b.battle_map[TileNum].map_object is not None:
                                    print(b.battle_map[TileNum].map_object.obj_name)
                                    if b.battle_map[TileNum].map_object.obj_name in ["Palisade_bottom", "Palisade"]:
                                        approach = [x2 - 1, y2]

                                        if approach in b.movement_grid:
                                            game_battle.disengage(b, b.queue[0].position)
                                            b.ready_to_act = False
                                            b.attacking_rotate.append(b.queue[0].number)
                                            b.move_destination = [int(approach[0]), int(approach[1])]
                                            b.target_destination = [int(x2), int(y2)]
                                            game_battle.action_order(b, "Move", "Dock the wall")
                                            result = True

                                        elif approach == b.queue[0].position:
                                            game_battle.disengage(b, b.queue[0].position)
                                            b.ready_to_act = False
                                            b.attacking_rotate.append(b.queue[0].number)
                                            b.target_destination = [int(x2), int(y2)]
                                            game_battle.action_order(b, "Rotate", "Dock the wall")
                                            result = True
                        break

    # print("m1_click_structure: result - " + str(result))
    return result


def find_battle_and_unit():
    b = None
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    # Index of selected tile in map list
    x2 = int(b.selected_tile[0])
    y2 = int(b.selected_tile[1])
    TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1

    unit = None

    for army in game_obj.game_armies:
        if army.army_id == b.battle_map[TileNum].army_id:
            unit = army.units[b.battle_map[TileNum].unit_index]
            break

    return b, unit


def fill_regiment_information(b, TileNum):
    b.regiment_attack_type_index = 0
    b.regiment_skills_index = 0
    b.regiment_effects_index = 0
    # b.effect_status_index = 0
    b.regiment_abilities_index = 0
    b.skill_info = None
    b.effect_info = None
    b.ability_info = None

    unit = None
    f_color = None
    s_color = None
    attack = None
    skill = None
    effect = None

    for army in game_obj.game_armies:
        if army.army_id == b.battle_map[TileNum].army_id:
            unit = army.units[b.battle_map[TileNum].unit_index]
            attack = unit.attacks[b.regiment_attack_type_index]
            if len(unit.skills) > 0:
                skill = unit.skills[b.regiment_skills_index]
            if len(unit.effects) > 0:
                effect = unit.effects[b.regiment_effects_index]

            if army.owner != "Neutral":
                for realm in game_obj.game_powers:
                    if realm.name == army.owner:
                        f_color = realm.f_color
                        s_color = realm.s_color

            break

    total_HP = 0
    for creature in unit.crew:
        total_HP += creature.HP

    b.unit_info = game_classes.Regiment_Info_Card(unit.name, f_color, s_color, len(unit.crew), total_HP, unit.morale,
                                                  unit.max_HP, unit.experience, unit.speed, unit.leadership,
                                                  unit.engaged, unit.deserted, len(unit.attacks), unit.armour,
                                                  unit.defence, unit.reg_tags, unit.magic_power, unit.mana_reserve,
                                                  unit.max_mana_reserve, unit.abilities)

    b.attack_info = game_classes.Attack_Info_Card(attack.name, attack.attack_type, attack.min_dmg, attack.max_dmg,
                                                  attack.mastery, attack.effective_range, attack.range_limit,
                                                  attack.tags)

    if len(unit.skills) > 0:
        value_text = ""
        if skill is not None:
            value_text = str(skill.quantity)
        else:
            value_text = str(skill.quality)
        b.skill_info = game_classes.Skill_Info_Card(skill.name, skill.application, value_text, skill.skill_tags)

    if len(unit.effects) > 0:
        time_text = ""
        if effect.until_next_turn:
            time_text = "Until next turn"
        else:
            # time_text = "Time left: " + str(effect.time_left)
            time_text = "Time left: " + str(effect.end_time - b.queue[0].time_act)
        b.effect_info = game_classes.Effect_Info_Card(effect.name, time_text, effect.buffs)

    if len(unit.abilities) > 0:
        b.ability_info = unit.abilities[b.regiment_abilities_index]
        b.ability_description = ability_desc_cat_regiment.script_cat[b.ability_info](unit)

    b.battle_window = "Regiment info"


def close_information_window():
    b, unit = find_battle_and_unit()

    b.unit_info = None
    b.attack_info = None
    b.battle_window = None


def previous_attack_info():
    b, unit = find_battle_and_unit()

    if b.regiment_attack_type_index == 0:
        b.regiment_attack_type_index = len(unit.attacks) - 1
    else:
        b.regiment_attack_type_index -= 1

    attack = unit.attacks[b.regiment_attack_type_index]

    b.attack_info = game_classes.Attack_Info_Card(attack.name, attack.attack_type, attack.min_dmg, attack.max_dmg,
                                                  attack.mastery, attack.effective_range, attack.range_limit,
                                                  attack.tags)


def next_attack_info():
    b, unit = find_battle_and_unit()

    if b.regiment_attack_type_index == len(unit.attacks) - 1:
        b.regiment_attack_type_index = 0
    else:
        b.regiment_attack_type_index += 1

    attack = unit.attacks[b.regiment_attack_type_index]

    b.attack_info = game_classes.Attack_Info_Card(attack.name, attack.attack_type, attack.min_dmg, attack.max_dmg,
                                                  attack.mastery, attack.effective_range, attack.range_limit,
                                                  attack.tags)


def previous_skill_info():
    b, unit = find_battle_and_unit()

    if len(unit.skills) > 0:
        if b.regiment_skills_index == 0:
            b.regiment_skills_index = len(unit.skills) - 1
        else:
            b.regiment_skills_index -= 1

        skill = unit.skills[b.regiment_skills_index]

        value_text = ""
        if skill is not None:
            value_text = str(skill.quantity)
        else:
            value_text = str(skill.quality)

        b.skill_info = game_classes.Skill_Info_Card(skill.name, skill.application, value_text, skill.skill_tags)


def next_skill_info():
    print("next_skill_info")
    b, unit = find_battle_and_unit()

    if len(unit.skills) > 0:
        if b.regiment_skills_index == len(unit.skills) - 1:
            b.regiment_skills_index = 0
        else:
            b.regiment_skills_index += 1

        skill = unit.skills[b.regiment_skills_index]

        value_text = ""
        if skill is not None:
            value_text = str(skill.quantity)
        else:
            value_text = str(skill.quality)

        b.skill_info = game_classes.Skill_Info_Card(skill.name, skill.application, value_text, skill.skill_tags)


def previous_effect_info():
    b, unit = find_battle_and_unit()

    if len(unit.effects) > 0:
        if b.regiment_effects_index == 0:
            b.regiment_effects_index = len(unit.effects) - 1
        else:
            b.regiment_effects_index -= 1

        effect = unit.effects[b.regiment_effects_index]

        time_text = ""
        if effect.until_next_turn:
            time_text = "Until next turn"
        else:
            time_text = "Time left: " + str(effect.time_left)
        b.effect_info = game_classes.Effect_Info_Card(effect.name, time_text, effect.buffs)


def next_effect_info():
    b, unit = find_battle_and_unit()

    if len(unit.effects) > 0:
        if b.regiment_effects_index == len(unit.effects) - 1:
            b.regiment_effects_index = 0
        else:
            b.regiment_effects_index += 1

        effect = unit.effects[b.regiment_effects_index]

        time_text = ""
        if effect.until_next_turn:
            time_text = "Until next turn"
        else:
            time_text = "Time left: " + str(effect.time_left)
        b.effect_info = game_classes.Effect_Info_Card(effect.name, time_text, effect.buffs)


def previous_ability_info():
    b, unit = find_battle_and_unit()

    if len(unit.abilities) > 0:
        if b.regiment_abilities_index == 0:
            b.regiment_abilities_index = len(unit.abilities) - 1
        else:
            b.regiment_abilities_index -= 1

        b.ability_info = unit.abilities[b.regiment_abilities_index]
        b.ability_description = ability_desc_cat_regiment.script_cat[b.ability_info](unit)


def next_ability_info():
    b, unit = find_battle_and_unit()

    if len(unit.abilities) > 0:
        if b.regiment_abilities_index == len(unit.abilities) - 1:
            b.regiment_abilities_index = 0
        else:
            b.regiment_abilities_index += 1

        b.ability_info = unit.abilities[b.regiment_abilities_index]
        b.ability_description = ability_desc_cat_regiment.script_cat[b.ability_info](unit)


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
    b = None
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle
            break

    if len(b.waiting_list) == 0:
        b.stage = "Fighting"
        print("stage - " + str(b.stage))
        b.selected_tile = []
        b.selected_unit = -1
        b.selected_unit_alt = ()
        b.preparation_siege_machine = None

        fill_morale(b)
        fill_max_HP(b)
        fill_mana_reserve(b)
        fill_magic_power(b)
        fill_counterattacks(b)

        # Form queue
        game_battle.form_queue(b)

        for army in game_obj.game_armies:
            if army.army_id == b.attacker_id or army.army_id == b.defender_id:
                for unit in army.units:
                    game_battle.apply_aura(unit, b, army.army_id)

        game_battle.advance_queue(b)

        click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
        click_sound.play()


def siege_tower_reserve_but():
    b = None
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle
            break

    if b.battle_type != "Siege":
        # Wrong battle type, should ignore clicking this button
        b.button_pressed = True
    else:
        if b.selected_unit == -1:
            if b.preparation_siege_machine == "Siege tower":
                b.preparation_siege_machine = None
            elif b.available_siege_towers > 0:
                if b.unit_card != -1:
                    b.unit_card = -1
                b.preparation_siege_machine = "Siege tower"
        else:
            the_army = None
            for army in game_obj.game_armies:
                if army.army_id == b.battle_map[b.selected_unit].army_id:
                    the_army = army
                    break

            the_unit = the_army.units[b.battle_map[b.selected_unit].unit_index]
            if the_unit.siege_engine is not None:
                if the_unit.siege_engine == "Siege tower":
                    the_unit.siege_engine = None
                    b.available_siege_towers += 1


def battering_ram_reserve_but():
    b = None
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle
            break

    # print("selected_unit: " + str(b.selected_unit))
    # print("battle_type: " + str(b.battle_type))
    # print("available_battering_rams: " + str(b.available_battering_rams))

    if b.battle_type != "Siege":
        # Wrong battle type, should ignore clicking this button
        b.button_pressed = True
    else:
        if b.selected_unit == -1:
            if b.preparation_siege_machine == "Battering ram":
                b.preparation_siege_machine = None
            elif b.available_battering_rams > 0:
                if b.unit_card != -1:
                    b.unit_card = -1
                b.preparation_siege_machine = "Battering ram"
        else:
            the_army = None
            for army in game_obj.game_armies:
                if army.army_id == b.battle_map[b.selected_unit].army_id:
                    the_army = army
                    break

            the_unit = the_army.units[b.battle_map[b.selected_unit].unit_index]
            if the_unit.siege_engine is not None:
                if the_unit.siege_engine == "Battering ram":
                    the_unit.siege_engine = None
                    b.available_battering_rams += 1


def equip_regiment(b, TileNum):
    the_army = None
    for army in game_obj.game_armies:
        if army.army_id == b.battle_map[TileNum].army_id:
            the_army = army
            break

    the_unit = the_army.units[b.battle_map[TileNum].unit_index]

    if the_unit.siege_engine is not None:
        pass
    else:
        if b.preparation_siege_machine == "Siege tower":
            b.available_siege_towers -= 1
            the_unit.siege_engine = "Siege tower"

        elif b.preparation_siege_machine == "Battering ram":
            b.available_battering_rams -= 1
            the_unit.siege_engine = "Battering ram"

        b.preparation_siege_machine = None


def handle_siege_equipment():
    b = None
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle
            break

    if b.battle_type != "Siege":
        # Wrong battle type, should ignore clicking this button
        b.button_pressed = True
    else:
        if b.queue[0].obj_type == "Regiment" and b.ready_to_act:
            the_unit = None
            for army in game_obj.game_armies:
                if army.army_id == b.queue[0].army_id:
                    the_unit = army.units[b.queue[0].number]
                    break

            if the_unit.siege_engine is not None:
                # Drop siege equipment
                TileNum = (b.queue[0].position[1] - 1) * game_stats.battle_width + b.queue[0].position[0] - 1
                img_width = siege_warfare_catalog.siege_machine_img_width[the_unit.siege_engine]
                img_height = siege_warfare_catalog.siege_machine_img_height[the_unit.siege_engine]
                print("img_width - " + str(img_width) + ", img_height - " + str(img_height)
                      + ", type - " + str(type(img_height)))
                coordinates = [random.randint(1, 95 - img_width),
                               random.randint(1, 95 - img_height)]
                b.battle_map[TileNum].siege_machines.append([str(the_unit.siege_engine), coordinates,
                                                             the_unit.right_side])
                the_unit.siege_engine = None

            else:
                TileNum = (b.queue[0].position[1] - 1) * game_stats.battle_width + b.queue[0].position[0] - 1
                if len(b.battle_map[TileNum].siege_machines) > 0:
                    print("Pick up equipment")
                    b.available_equipment = b.battle_map[TileNum].siege_machines
                    b.battle_window = "Siege equipment menu"


def fill_morale(b):
    for army in game_obj.game_armies:
        if army.army_id == b.attacker_id or army.army_id == b.defender_id:
            bonus_leadership = 0.0
            if army.hero is not None:
                # Skills
                for skill in army.hero.skills:
                    for effect in skill.effects:
                        if effect.application == "Bonus leadership":
                            if effect.method == "addition":
                                bonus_leadership += float(effect.quantity)

                # Artifacts
                if len(army.hero.inventory) > 0:
                    for artifact in army.hero.inventory:
                        for effect in artifact.effects:
                            if effect.application == "Bonus leadership":
                                if effect.method == "addition":
                                    bonus_leadership += float(effect.quantity)
                                elif effect.method == "subtraction":
                                    bonus_leadership -= float(effect.quantity)

            for unit in army.units:
                unit.leadership = float(unit.base_leadership) + float(bonus_leadership)
                # print(unit.name + ": base_leadership - " + str(unit.base_leadership) + ", bonus_leadership - " +
                #       str(bonus_leadership) + ", unit.leadership - " + str(unit.leadership))
                if unit.leadership < 1.0:
                    unit.leadership = 1.0
                unit.morale = float(unit.leadership)


def fill_max_HP(b):
    for army in game_obj.game_armies:
        if army.army_id == b.attacker_id or army.army_id == b.defender_id:
            bonus_HP = 0
            if army.hero is not None:
                for skill in army.hero.skills:
                    for effect in skill.effects:
                        if effect.application == "Bonus fortitude":
                            if effect.method == "addition":
                                bonus_HP += int(effect.quantity)
            for unit in army.units:
                unit.max_HP = int(unit.base_HP) + int(bonus_HP)
                for creature in unit.crew:
                    creature.HP = int(unit.max_HP)


def fill_mana_reserve(b):
    for army in game_obj.game_armies:
        if army.army_id == b.attacker_id or army.army_id == b.defender_id:

            for unit in army.units:
                bonus_mana_reserve = 0
                if army.hero is not None:
                    # Artifacts
                    if len(army.hero.inventory) > 0:
                        for artifact in army.hero.inventory:
                            for effect in artifact.effects:
                                if effect.application == "Bonus mana reserve":
                                    allowed = True
                                    if len(effect.other_tags) > 0:
                                        allowed = False
                                        for unit_tag in unit.reg_tags:
                                            if unit_tag in effect.other_tags:
                                                allowed = True

                                    if allowed:
                                        if effect.method == "addition":
                                            bonus_mana_reserve += int(effect.quantity)
                                        elif effect.method == "subtraction":
                                            bonus_mana_reserve -= int(effect.quantity)

                unit.mana_reserve = int(unit.max_mana_reserve) + int(bonus_mana_reserve)
                # print(unit.name + ": max_mana_reserve - " + str(unit.max_mana_reserve) + ", bonus_mana_reserve - " +
                #       str(bonus_mana_reserve) + ", unit.mana_reserve - " + str(unit.mana_reserve))
                if unit.mana_reserve < 0:
                    unit.mana_reserve = 0


def fill_magic_power(b):
    for army in game_obj.game_armies:
        if army.army_id == b.attacker_id or army.army_id == b.defender_id:

            for unit in army.units:
                bonus_MP = 0
                if army.hero is not None:
                    # Artifacts
                    if len(army.hero.inventory) > 0:
                        for artifact in army.hero.inventory:
                            for effect in artifact.effects:
                                if effect.application == "Bonus Magic Power":
                                    allowed = True
                                    if len(effect.other_tags) > 0:
                                        allowed = False
                                        for unit_tag in unit.reg_tags:
                                            if unit_tag in effect.other_tags:
                                                allowed = True

                                    if allowed:
                                        if effect.method == "addition":
                                            bonus_MP += int(effect.quantity)
                                        elif effect.method == "subtraction":
                                            bonus_MP -= int(effect.quantity)

                unit.magic_power = int(unit.base_magic_power) + int(bonus_MP)
                # print(unit.name + ": base_magic_power - " + str(unit.base_magic_power) + ", bonus_MP - " +
                #       str(bonus_MP) + ", unit.magic_power - " + str(unit.magic_power))
                if unit.magic_power < 0:
                    unit.magic_power = 0


def fill_counterattacks(b):
    for army in game_obj.game_armies:
        if army.army_id == b.attacker_id or army.army_id == b.defender_id:
            counter_attacks_value = 1
            if army.hero is not None:
                for skill in army.hero.skills:
                    for effect in skill.effects:
                        if effect.application == "Bonus counterattack":
                            if effect.method == "addition":
                                counter_attacks_value += effect.quantity

            for unit in army.units:
                unit.counterattack = int(counter_attacks_value)


def wait_but():
    print("wait_but")
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

        if b.queue[0].obj_type == "Regiment" or b.queue[0].obj_type == "Hero":

            if b.realm_in_control == game_stats.player_power and b.ready_to_act:
                b.ready_to_act = False
                game_battle.action_order(b, "Wait", None)
                # game_battle.complete_turn(b, 0.5)


def defend_but():
    print("defend_but")

    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

        if b.queue[0].obj_type == "Regiment":

            if b.realm_in_control == game_stats.player_power and b.ready_to_act:
                b.ready_to_act = False
                game_battle.action_order(b, "Defend", None)
                # game_battle.complete_turn(b, 1.0)


def prepare_opening_ability_menu():
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle
            if b.queue[0].obj_type == "Hero":
                open_hero_ability_menu_but(b)
            elif b.queue[0].obj_type == "Regiment":
                open_regiment_ability_menu_but(b)
            break


def prepare_change_attack_method():
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle
            if b.queue[0].obj_type == "Regiment":
                change_attack_method_but(b)

            break


# def choose_attack_method_or_hero_ability():
#     for battle in game_obj.game_battles:
#         if battle.attacker_realm == game_stats.player_power or \
#                 battle.defender_realm == game_stats.player_power:
#             b = battle
#
#             if b.queue[0].obj_type == "Regiment":
#                 change_attack_method_but(b)
#             elif b.queue[0].obj_type == "Hero":
#                 open_ability_menu_but(b)
#
#             break


def change_attack_method_but(b):
    print("change_attack_method_but")

    for army in game_obj.game_armies:
        if army.army_id == b.queue[0].army_id:
            if b.attack_type_index + 1 == len(army.units[b.queue[0].number].attacks):
                b.attack_type_index = 0
            else:
                b.attack_type_index += 1

            unit = army.units[b.queue[0].number]

            b.attack_type_in_use = unit.attacks[b.attack_type_index].attack_type
            b.attack_name = unit.attacks[b.attack_type_index].name
            b.cur_effective_range = unit.attacks[b.attack_type_index].effective_range
            # b.cur_range_limit = unit.attacks[b.attack_type_index].range_limit
            b.cur_range_limit = game_battle.attack_range_effect(army, unit,
                                                                unit.attacks[b.attack_type_index].range_limit)


def open_hero_ability_menu_but(b):
    print("open_hero_ability_menu_but")

    b.battle_window = "Ability menu"
    b.cursor_function = None
    b.ability_index = 0
    b.school_index = 0
    b.list_of_abilities = []
    b.list_of_schools = []

    for army in game_obj.game_armies:
        if army.army_id == b.queue[0].army_id:
            b.available_mana_reserve = int(army.hero.mana_reserve)
            b.list_of_schools.append("Overall")
            b.selected_school = "Overall"
            # Update visuals
            update_gf_battle.add_school_misc_sprites("Overall")
            for ability in army.hero.abilities:
                b.list_of_abilities.append(str(ability))

                school = ability_catalog.ability_cat[ability].school

                if school not in b.list_of_schools:
                    b.list_of_schools.append(str(school))

                # Update visuals
                update_gf_battle.add_school_misc_sprites(school)
                update_gf_battle.add_ability_misc_sprites(ability)

            # Abilities from artifacts
            if len(army.hero.inventory) > 0:
                for artifact in army.hero.inventory:
                    for effect in artifact.effects:
                        if effect.application == "Cast spells":
                            for ability in effect.application_tags:
                                b.list_of_abilities.append(str(ability))

                                school = ability_catalog.ability_cat[ability].school

                                if school not in b.list_of_schools:
                                    b.list_of_schools.append(str(school))

                                # Update visuals
                                update_gf_battle.add_school_misc_sprites(school)
                                update_gf_battle.add_ability_misc_sprites(ability)

            b.selected_ability = str(army.hero.abilities[0])
            b.ability_description = ability_desc_cat_hero.script_cat[b.selected_ability](army.hero)

            break


def open_regiment_ability_menu_but(b):
    print("open_regiment_ability_menu_but")

    b.battle_window = "Ability menu"
    b.cursor_function = None
    b.ability_index = 0
    b.school_index = 0
    b.list_of_abilities = []
    b.list_of_schools = []

    for army in game_obj.game_armies:
        if army.army_id == b.queue[0].army_id:
            the_unit = army.units[b.queue[0].number]

            b.available_mana_reserve = int(the_unit.mana_reserve)
            b.list_of_schools.append("Overall")
            b.selected_school = "Overall"
            # Update visuals
            update_gf_battle.add_school_misc_sprites("Overall")
            for ability in the_unit.abilities:
                b.list_of_abilities.append(str(ability))

                school = ability_catalog.ability_cat[ability].school

                if school not in b.list_of_schools:
                    b.list_of_schools.append(str(school))

                # Update visuals
                update_gf_battle.add_school_misc_sprites(school)
                update_gf_battle.add_ability_misc_sprites(ability)

            b.selected_ability = str(the_unit.abilities[0])
            b.ability_description = ability_desc_cat_regiment.script_cat[b.selected_ability](the_unit)

            break


def close_ability_menu_window():
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

            b.list_of_schools = []
            b.list_of_abilities = []
            b.ability_index = 0
            b.school_index = 0
            b.selected_school = None
            b.selected_ability = None
            b.battle_window = None
            b.available_mana_reserve = None
            b.ability_description = None

            break


def execute_ability():
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

            if b.available_mana_reserve >= ability_catalog.ability_cat[b.selected_ability].mana_cost:
                b.cursor_function = "Execute ability"
                b.battle_window = None


def close_siege_equipment_menu_window():
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

            b.battle_window = None
            b.available_equipment = []

            break


def pick_up_siege_equipment(b, position):
    # Select siege machine
    y_axis = position[1]
    y_axis -= 204
    print("y_axis - " + str(y_axis))
    if y_axis % 60 <= 57:
        y_axis = math.ceil(y_axis / 60)
        print("index - " + str(y_axis))

        if y_axis <= len(b.available_equipment):
            the_unit = None
            for army in game_obj.game_armies:
                if army.army_id == b.queue[0].army_id:
                    the_unit = army.units[b.queue[0].number]
                    break

            the_unit.siege_engine = str(b.available_equipment[y_axis -1][0])
            del b.available_equipment[y_axis -1]

            b.battle_window = None
            b.available_equipment = []


def end_battle_but():
    print("end_battle_but()")
    b = None
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle
            break

    # print("battle_type - " + b.battle_type)
    loser = None
    winner = None
    settlement = None
    settlement_captured = False
    remove_army_id = []

    for army in game_obj.game_armies:
        if army.army_id in [b.attacker_id, b.defender_id]:
            print("army_id - " + str(army.army_id) + " owner - " + str(army.owner))
            # Remove armies, if they had been wiped out
            for unit in army.units:
                if len(unit.crew) > 0:
                    unit.position = None
                    unit.direction = None
                    unit.engaged = False
                    unit.counterattack = 1
                    unit.effects = []
                    unit.deserted = False

                    for creature in unit.crew:
                        creature.HP = int(unit.max_HP)
                    unit.max_HP = None
                else:
                    army.units.remove(unit)

            if army.owner == b.defeated_side:
                loser = army
                loser_alive = True
                if b.battle_type == "Siege" and army.army_id == b.defender_id:
                    loser_alive = False
                    remove_army_id.append(army.army_id)
                    game_obj.game_map[army.location].army_id = None
                    settlement_captured = True
            else:
                print("Winner is " + str(army.owner))
                winner = army
                winner_alive = True

            if army.army_id == b.defender_id:
                if game_obj.game_map[army.location].lot is not None:
                    if game_obj.game_map[army.location].lot == "City":
                        for city in game_obj.game_cities:
                            if city.city_id == game_obj.game_map[army.location].city_id:
                                settlement = city
                                print(settlement.name + " - siege settlement")
                                break
            # if b.battle_type == "Siege" and settlement is None:
            #     if game_obj.game_map[army.location].lot is not None:
            #         if game_obj.game_map[army.location].lot == "City":
            #             for city in game_obj.game_cities:
            #                 if city.city_id == game_obj.game_map[army.location].city_id:
            #                     if city.siege is not None:
            #                         settlement = city
            #                         print(settlement.name + " - siege settlement")
            #                     break

            if len(army.units) == 0 or (army.owner == b.defeated_side and army.owner == "Neutral"):
                if army.owner == "Neutral":
                    # Neutral armies can't retreat, they get removed instead
                    print("Neutral army " + str(army.army_id) + " is defeated")
                print("Army " + str(army.army_id) + " is wiped out")

                # Removing army ID from location if it was neutral roaming army
                if game_obj.game_map[army.location].army_id == army.army_id:
                    game_obj.game_map[army.location].army_id = None

                if game_obj.game_map[army.location].lot is not None:
                    # print(game_obj.game_map[army.location].lot)
                    if game_obj.game_map[army.location].lot != "City":
                        # Removing army ID from exploration object if it was an event battle
                        if game_obj.game_map[
                                army.location].lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                            if game_obj.game_map[army.location].lot.properties.army_id == army.army_id:
                                game_obj.game_map[army.location].lot.properties.army_id = None
                    else:
                        # Captured neutral settlement
                        settlement_captured = True

                if army.army_id not in remove_army_id:  # Could have been added before
                    remove_army_id.append(army.army_id)

                if army.owner == b.defeated_side:
                    loser_alive = False
                else:
                    winner_alive = False

            print("b.defeated_side - " + str(b.defeated_side))
            print("")
            # # Neutral armies can't retreat, they get removed instead
            # if army.owner == b.defeated_side:
            #     if army.owner == "Neutral":
            #         print("Neutral army " + str(army.army_id) + " is defeated")
            #         game_obj.game_map[army.location].army_id = None
            #         game_obj.game_armies.remove(army)
            #         loser_alive = False

            if army.owner == b.defeated_side:
                if loser_alive:
                    army.action = "Stand"
            else:
                if winner_alive:
                    army.action = "Stand"
                    # Gain experience
                    if army.hero is not None:
                        army.hero.experience += int(b.earned_experience)

            if army.army_id not in remove_army_id:
                if army.owner != "Neutral":
                    for realm in game_obj.game_powers:
                        if realm.name == army.owner:
                            strategy_logic.complete_war_order(army, realm)
                            break

    # Removing destroyed armies
    game_basic.remove_army(remove_army_id)

    # Capture settlement
    if b.battle_type == "Siege":
        if settlement_captured:
            game_basic.capture_settlement(settlement, b.attacker_realm, winner_alive, winner)

    # In case there is a besieged settlement, its siege should be lifted
    if settlement:
        if settlement.siege:
            settlement.siege = None

    # Check shattered status
    if loser.shattered == "Stable":
        loser.shattered = "Shattered"
    else:
        game_obj.game_armies.remove(loser)
        loser_alive = False

    # Defeated army should route
    if loser_alive:
        loser_realm = None
        friendly_cities = []
        hostile_cities = []
        at_war_list = []
        known_map = []

        if loser.owner != "Neutral":
            for realm in game_obj.game_powers:
                if realm.name == loser.owner:
                    loser_realm = realm
                    break

            known_map = loser_realm.known_map
            friendly_cities, hostile_cities, at_war_list = game_pathfinding.find_friendly_cities(loser_realm.name)
        else:
            known_map = game_stats.map_positions

        routing_path, routing_grid = algo_movement_range.range_astar(None, loser.posxy, 600.0, friendly_cities,
                                                                     hostile_cities, known_map, True, [])

        if len(routing_grid) > 0:
            farthest_tile = None
            biggest_distance = 0.0
            for tile in routing_grid:
                distance = math.sqrt(((tile[0] - winner.posxy[0]) ** 2) + ((tile[1] - winner.posxy[1]) ** 2))
                if farthest_tile is None:
                    farthest_tile = list(tile)
                    biggest_distance = float(distance)

                elif distance > biggest_distance:
                    farthest_tile = list(tile)
                    biggest_distance = float(distance)

            print("farthest_tile - " + str(farthest_tile) + " biggest_distance - " + str(biggest_distance))

            for node in routing_path:
                if node.position == farthest_tile:
                    print("node.position - " + str(node.position) + " and farthest_tile - " + str(farthest_tile))
                    pathway = []
                    current = node
                    while current is not None:
                        pathway.append(current.position)
                        current = current.parent

                    print("Final unreversed path is " + str(pathway))
                    loser.route = list(pathway[::-1])
                    loser.route = loser.route[1:]
                    print("Final reversed path is " + str(loser.route))
                    loser.action = "Routing"

                    # algo_path_arrows.construct_path(loser.army_id, loser.route)
        else:
            loser.action = "Stand"

    game_stats.current_screen = "Game Board"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "game_board_screen"
    game_stats.strategy_mode = True

    # Result script
    if b.result_script is not None:
        if b.attacker_realm == game_stats.player_power:
            winner_army = None
            for army in game_obj.game_armies:
                if army.army_id == b.attacker_id:
                    winner_army = army
                    break

            game_stats.reward_id_counter += 1
            game_obj.game_rewards.append(reward_catalog.reward_scripts[b.result_script](winner_army))
            for reward in game_obj.game_rewards:
                if reward[0] == game_stats.reward_id_counter:
                    game_stats.reward_for_demonstration = list(reward[1])
                    break
            for realm in game_obj.game_powers:
                if realm.name == winner_army.owner:
                    realm.reward_IDs.append(int(game_stats.reward_id_counter))
                    break
            battle_result_scripts.result_scripts[b.result_script](winner_army)

    elif loser.event is not None:
        attacker_realm = None
        for realm in game_obj.game_powers:
            if realm.name == winner.owner:
                attacker_realm = realm
                break

        print("end_battle_but: Event name - " + loser.event.name)
        if loser.event.name in knight_lords_quest_result_scripts.result_scripts:
            knight_lords_quest_result_scripts.result_scripts[loser.event.name](winner, attacker_realm, loser.event)

    game_obj.game_battles.remove(b)

    game_stats.attacker_army_id = 0
    game_stats.defender_army_id = 0

    graphics_basic.prepare_resource_ribbon()

    # Update visuals
    print("end_battle_but - update_visuals")
    game_stats.gf_misc_img_dict = {}
    game_stats.gf_battle_effects_dict = {}
    update_gf_game_board.update_misc_sprites()
    update_gf_game_board.update_sprites()
    update_gf_game_board.update_regiment_sprites()

    click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
    click_sound.play()


formation_button_funs = {1: start_battle_but,
                         2: siege_tower_reserve_but,
                         3: battering_ram_reserve_but}

fighting_button_funs = {1: wait_but,
                        2: defend_but,
                        3: prepare_opening_ability_menu,
                        4: prepare_change_attack_method,
                        5: handle_siege_equipment}

waiting_list_panel_funs = {1: waiting_index_left,
                           2: waiting_index_right}

battle_end_window_funs = {1: end_battle_but}

ability_menu_window_funs = {1: close_ability_menu_window,
                            2: execute_ability}

siege_equipment_menu_window_funs = {1: close_siege_equipment_menu_window}

regiment_info_window_funs = {1 : close_information_window,
                             2 : previous_attack_info,
                             3 : next_attack_info,
                             4 : previous_skill_info,
                             5 : next_skill_info,
                             6 : previous_effect_info,
                             7 : next_effect_info,
                             8 : previous_ability_info,
                             9 : next_ability_info}

window_buttons = {"Battle end window": battle_end_window_funs,
                  "Ability menu": ability_menu_window_funs,
                  "Regiment info": regiment_info_window_funs,
                  "Siege equipment menu": siege_equipment_menu_window_funs}

lower_panel_buttons = {"Waiting list": waiting_list_panel_funs}

lower_panel_zone = {"Waiting list": waiting_list_panel_zone}

window_zone = {"Battle end window": battle_end_window_zone,
               "Ability menu": ability_menu_window_zone,
               "Regiment info": regiment_info_window_zone,
               "Siege equipment menu": siege_equipment_menu_window_zone}

click_window_zone = {"Regiment info": [642, 70, 1278, 600],
                     "Battle end window": [130, 100, 1150, 400],
                     "Ability menu": [180, 100, 1100, 600],
                     "Siege equipment menu": [441, 201, 840, 500]}
