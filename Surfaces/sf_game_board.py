## Miracle battles
## sf_game_board

import math
import pygame
import random
import sys
import copy

from Content import building_drafts
from Resources import game_basic
from Resources import game_classes
from Resources import game_obj
from Resources import game_pathfinding
from Resources import game_stats
from Resources import level_save
from Resources import algo_building
from Resources import skill_classes
from Resources import ability_classes
from Resources import update_gf_game_board
from Resources import update_gf_battle
from Resources import algo_path_arrows
from Resources import game_diplomacy
from Resources import diplomacy_classes
from Resources import game_autobattle


from Resources.Battle_Preparation import battle_map_generation
from Resources.Battle_Preparation import siege_map_generation

from Storage import create_unit

from Content import new_heroes_catalog
from Content import hero_names
from Content import starting_skills
from Content import hero_skill_catalog
from Content import rw_click_scripts
from Content import building_rw_det_cat

from Content.Quests import knight_lords_quest_messages
from Content.Quests import knight_lords_dilemma_messages
from Content.Quests import knight_lords_quest_det
from Content.Quests import knight_lords_dilemma_det
from Content import diplomatic_messages_text
from Content import diplomatic_messages_det

yVar = game_stats.game_window_height - 800

button_zone = [[1150, 10, 1250, 32],
               [1040, 10, 1140, 32],
               [1005, 5, 1030, 54],
               [3, 3, 27, 27],
               [3, 28, 27, 47],
               [3, 53, 27, 72],
               [1, 761 + yVar, 14, 793 + yVar],
               [186, 761 + yVar, 218, 793 + yVar]]

begin_battle_panel_zone = [[590, 138, 690, 160],
                           [590, 168, 690, 190]]

settlement_panel_zone = [[615, 85, 634, 104],
                         [5, 85, 110, 104],
                         [120, 85, 225, 104],
                         [235, 85, 340, 104],
                         [350, 85, 455, 104],
                         [465, 85, 570, 104]]

building_upgrade_panel_zone = [[1254, 85, 1273, 104]]

building_panel_zone = [[1254, 85, 1273, 104]]

new_regiment_information_panel_zone = [[1254, 85, 1273, 104]]

new_hero_skill_tree_panel_zone = [[1254, 85, 1273, 104],
                                  [646, 117, 665, 136],
                                  [1254, 117, 1273, 136]]

hero_window_panel_zone = [[1254, 85, 1273, 104],
                          [864, 112, 960, 132],
                          [864, 137, 960, 157],
                          [864, 162, 960, 182]]

settlement_building_zone = [[615, 112, 634, 132],
                            [615, 517, 634, 536]]

settlement_recruitment_zone = [[286, 112, 396, 132],
                               [406, 112, 516, 132]]

settlement_heroes_zone = [[286, 112, 396, 132],
                          [406, 112, 516, 132],
                          [615, 196, 634, 214],
                          [615, 216, 634, 234]]

settlement_economy_zone = [[5, 114, 110, 133],
                           [120, 114, 225, 133],
                           [235, 114, 340, 133],
                           [350, 114, 455, 133]]

settlement_factions_zone = [[221, 303, 240, 322],
                            [221, 517, 240, 534]]

settlement_economy_population_zone = [[206, 143, 225, 162],
                                      [206, 517, 225, 536]]

facility_lower_panel_zone = []

settlement_lower_panel_zone = [[303, 684 + yVar, 393, 706 + yVar],
                               [203, 776 + yVar, 253, 794 + yVar]]

army_lower_panel_zone = [[203, 776 + yVar, 253, 794 + yVar]]

army_exchange_panel_zone = [[203, 595 + yVar, 290, 617 + yVar]]

quest_log_panel_zone = [[655, 85, 674, 104],
                        [37, 85, 179, 104],
                        [187, 85, 329, 104]]

realm_panel_zone = [[655, 85, 674, 104]]

diplomacy_panel_zone = [[655, 85, 674, 104],
                        [421, 108, 437, 124],
                        [421, 298, 437, 314]]

diplomacy_action_zone = [[41, 321, 141, 338],
                         [41, 340, 141, 357]]

diplomacy_declaration_of_war_zone = [[117, 520, 216, 535],
                                     [457, 520, 556, 535]]

diplomacy_sue_for_peace_zone = [[400, 338, 516, 354],
                                [400, 358, 516, 374]]

diplomacy_draft_a_peace_offer_zone = [[117, 520, 216, 535],
                                      [255, 520, 367, 535],
                                      [406, 520, 557, 535]]

diplomacy_threaten_zone = [[117, 520, 216, 535],
                           [457, 520, 556, 535]]

war_panel_zone = [[655, 85, 674, 104],
                  [280, 243, 395, 261]]

settlement_blockade_panel_zone = [[128, 139, 238, 161],
                                  [128, 169, 238, 191],
                                  [128, 199, 238, 221],
                                  [128, 229, 238, 251],
                                  [1135, 75, 1154, 94]]

settlement_blockade_panel_rb_zone = [[734, 153, 9],
                                     [714, 153, 9],
                                     [734, 197, 9],
                                     [714, 197, 9],
                                     [734, 241, 9],
                                     [714, 241, 9]
                                     ]

autobattle_conclusion_panel_zone = [[590, 135, 690, 157]]


def game_board_keys(key_action):
    if key_action == 119:
        game_stats.pov_pos[1] -= 1
        update_gf_game_board.update_sprites()
    elif key_action == 115:
        game_stats.pov_pos[1] += 1
        update_gf_game_board.update_sprites()
    elif key_action == 97:
        game_stats.pov_pos[0] -= 1
        update_gf_game_board.update_sprites()
    elif key_action == 100:
        game_stats.pov_pos[0] += 1
        update_gf_game_board.update_sprites()

    elif key_action == 32:  # key - space
        if not game_stats.pause_status:
            game_stats.pause_status = True
            game_stats.passed_time = game_stats.passed_time + game_stats.temp_time_passed
        else:
            game_stats.pause_status = False
            game_stats.last_start = pygame.time.get_ticks()
        print("Pause is " + str(game_stats.pause_status))
        if not game_stats.count_started:
            game_stats.count_started = True
            game_stats.start_time = pygame.time.get_ticks()

    elif key_action == 122:  # key - Z
        print("game_stats.show_time - " + str(game_stats.show_time))
        if game_stats.show_time:
            game_stats.show_time = False
        else:
            game_stats.show_time = True

    elif key_action == 120:  # key - X
        print("game_stats.fps_status - " + str(game_stats.fps_status))
        if game_stats.fps_status:
            game_stats.fps_status = False
        else:
            game_stats.fps_status = True


def game_board_surface_m1(position):
    global yVar
    game_stats.button_pressed = False
    ##    print("Success")
    print("")

    button_numb = 0
    for square in button_zone:
        button_numb += 1
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_funs[button_numb]()
            game_stats.button_pressed = True
            click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
            click_sound.play()
            break

    square = [14, 749 + yVar, 184, 795 + yVar]
    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
        select_war_notification(position)

    # Panels' zone
    if game_stats.game_board_panel != "":
        p_round_button_zone = []
        p_script_zone = None
        if game_stats.game_board_panel not in panel_buttons:
            p_funs = game_stats.event_panel_det.obj_funs
            p_button_zone = game_stats.event_panel_det.obj_button_zone
            p_script_zone = game_stats.event_panel_det.click_scripts
            square = game_stats.event_panel_det.square
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                game_stats.button_pressed = True
        else:
            p_funs = panel_buttons[game_stats.game_board_panel]
            p_button_zone = panel_zone[game_stats.game_board_panel]
            if game_stats.game_board_panel in panel_round_buttons:
                # print(game_stats.game_board_panel + " is in panel_round_buttons")
                p_round_button_funs = panel_round_buttons[game_stats.game_board_panel]
                p_round_button_zone = panel_rb_zone[game_stats.game_board_panel]

        if p_script_zone is not None:
            p_script_zone(position)

        button_numb = 0
        for square in p_button_zone:
            button_numb += 1
            ##            print("Level editor panel button " + str(button_numb))
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                print("p_funs[button_numb] - " + str(p_funs[button_numb]))
                p_funs[button_numb]()
                game_stats.button_pressed = True
                break

        if not game_stats.button_pressed and p_round_button_zone != []:
            button_numb = 0
            for point_radius in p_round_button_zone:
                print("point_radius - " + str(point_radius))
                button_numb += 1
                distance = math.sqrt(((point_radius[0] - position[0]) ** 2) + ((point_radius[1] - position[1]) ** 2))
                print("distance - " + str(distance))
                if distance <= point_radius[2]:
                    p_round_button_funs[button_numb]()
                    game_stats.button_pressed = True
                    break

        if game_stats.game_board_panel == "settlement panel" and game_stats.settlement_area == "Building":
            button_numb = 0
            for square in settlement_building_zone:
                button_numb += 1
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    settlement_building_funs[button_numb]()
                    game_stats.button_pressed = True
                    break

            square = [1, 112, 639, 540]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                game_stats.button_pressed = True
                # print(str(position[0]) + ", " + str(position[1]))
                x_axis, y_axis = position[0], position[1]
                x_axis -= 5
                # x_axis = x_axis % 153
                y_axis -= 112
                # y_axis = y_axis % 130
                if 0 < x_axis % 153 < 143 and 0 < y_axis % 108 < 100:
                    if 73 < y_axis % 108:
                        if x_axis % 153 < 35:
                            print("Building - build a new structure: " + str(x_axis) + ", " + str(y_axis))
                            x_axis = math.ceil(x_axis / 153)
                            y_axis = math.ceil(y_axis / 108)
                            print("Building - build a new structure: " + str(x_axis) + ", " + str(y_axis))
                            build_new_structure(x_axis, y_axis)

                        else:
                            print("Building - upgrade information: " + str(x_axis) + ", " + str(y_axis))
                            x_axis = math.ceil(x_axis / 153)
                            y_axis = math.ceil(y_axis / 108)
                            print("Building - upgrade information: " + str(x_axis) + ", " + str(y_axis))

                            show_building_upgrade_information(x_axis, y_axis)

                    else:
                        # Building information
                        print("Building - information: " + str(x_axis) + ", " + str(y_axis))
                        x_axis = math.ceil(x_axis / 153)
                        y_axis = math.ceil(y_axis / 108)
                        print("Building - information: " + str(x_axis) + ", " + str(y_axis))

                        the_plot = None
                        for city in game_obj.game_cities:
                            if city.city_id == game_stats.selected_settlement:
                                for plot in city.buildings:
                                    if plot.structure is not None:
                                        if plot.screen_position == [x_axis, y_axis + game_stats.building_row_index]:
                                            the_plot = plot
                                            print("Position - " + str(plot.screen_position))
                                            break
                                break

                        if the_plot is not None:
                            print('game_stats.right_window = "Building information"')
                            game_stats.right_window = "Building information"
                            game_stats.rw_object = the_plot.structure
                            print("game_stats.rw_object.name - " + str(game_stats.rw_object.name))
                            game_stats.selected_artifact_info = None
                            if the_plot.structure.name in building_rw_det_cat.building_catalog:
                                building_rw_det_cat.building_catalog[the_plot.structure.name]()
                            # Update visuals
                            update_gf_game_board.add_settlement_building_sprites(the_plot.structure.name,
                                                                                 the_plot.structure.img)

        elif game_stats.game_board_panel == "settlement panel" and game_stats.settlement_area == "Recruiting":
            button_numb = 0
            for square in settlement_recruitment_zone:
                button_numb += 1
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    settlement_recruitment_funs[button_numb]()
                    button_pressed = True
                    break

            square = [1, 115, 257, 540]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                game_stats.button_pressed = True
                y_axis = position[1]
                y_axis -= 115
                print(str(y_axis))
                y_axis = math.ceil(y_axis / 52)
                print(str(y_axis))

                the_settlement = None
                for city in game_obj.game_cities:
                    if city.city_id == game_stats.selected_settlement:
                        the_settlement = city

                number = 0
                for plot in the_settlement.buildings:
                    if plot.structure is not None:
                        if len(plot.structure.recruitment) > 0 and plot.status == "Built":
                            for unit_card in plot.structure.recruitment:
                                number += 1
                                if number == y_axis:
                                    game_stats.unit_for_hire = unit_card
                                    break

                for unit_card in create_unit.LE_units_dict_by_alignment[the_settlement.alignment]:
                    if unit_card.name == game_stats.unit_for_hire.unit_name:
                        game_stats.rw_object = unit_card
                        break

                game_stats.enough_resources_to_pay = game_basic.enough_resources_to_hire(game_stats.unit_for_hire.unit_name,
                                                                                         the_settlement)

        elif game_stats.game_board_panel == "settlement panel" and game_stats.settlement_area == "Heroes":
            button_numb = 0
            for square in settlement_heroes_zone:
                button_numb += 1
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    settlement_heroes_funs[button_numb]()
                    game_stats.button_pressed = True
                    break

            square = [1, 141, 257, 540]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                game_stats.button_pressed = True
                y_axis = position[1]
                y_axis -= 141
                print(str(y_axis))
                y_axis = math.ceil(y_axis / 52)
                print(str(y_axis))

                the_settlement = None
                alignment = None
                for city in game_obj.game_cities:
                    if city.city_id == game_stats.selected_settlement:
                        the_settlement = city
                        alignment = the_settlement.alignment

                if y_axis <= len(new_heroes_catalog.heroes_classes_dict_by_alignment[alignment]):
                    hero_class = new_heroes_catalog.heroes_classes_dict_by_alignment[alignment][y_axis - 1]
                    game_stats.hero_for_hire = new_heroes_catalog.basic_heroes_dict_by_alignment[alignment][hero_class]
                    game_stats.enough_resources_to_pay = game_basic.enough_resources_to_hire_hero(game_stats.hero_for_hire)
                    game_basic.form_starting_skills_pool(hero_class, "Player")

        elif game_stats.game_board_panel == "settlement panel" and game_stats.settlement_area == "Economy":
            button_numb = 0
            for square in settlement_economy_zone:
                button_numb += 1
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    settlement_economy_funs[button_numb]()
                    game_stats.button_pressed = True
                    break

            if game_stats.settlement_subsection == "Population":
                button_numb = 0
                for square in settlement_economy_population_zone:
                    button_numb += 1
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        settlement_economy_population_funs[button_numb]()
                        game_stats.button_pressed = True
                        break

                square = [2, 142, 201, 540]
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    game_stats.button_pressed = True
                    select_pops(position)

        elif game_stats.game_board_panel == "settlement panel" and game_stats.settlement_area == "Factions":
            button_numb = 0
            for square in settlement_factions_zone:
                button_numb += 1
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    settlement_factions_funs[button_numb]()
                    game_stats.button_pressed = True
                    break

            square = [4, 169, 240, 299]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                game_stats.button_pressed = True
                y_axis = position[1]
                y_axis -= 169
                print(str(y_axis))
                y_axis = math.ceil(y_axis / 20)
                print(str(y_axis))

                the_settlement = None
                for city in game_obj.game_cities:
                    if city.city_id == game_stats.selected_settlement:
                        the_settlement = city
                        break

                if y_axis <= len(the_settlement.factions):
                    game_stats.faction_screen_index = int(y_axis - 1)

        elif game_stats.game_board_panel == "army exchange panel":

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
                print("number - " + str(number))
                approaching_army = None
                standing_army = None
                for army in game_obj.game_armies:
                    if army.army_id == game_stats.selected_army:
                        approaching_army = army
                    elif army.army_id == game_stats.selected_second_army:
                        standing_army = army

                if number not in game_stats.second_army_exchange_list:
                    if len(approaching_army.units) - len(game_stats.first_army_exchange_list) + \
                            len(game_stats.second_army_exchange_list) < 20:
                        game_stats.second_army_exchange_list.append(number)
                        game_stats.second_army_exchange_list = sorted(game_stats.second_army_exchange_list,
                                                                      reverse=True)
                        print("second_army_exchange_list: " + str(game_stats.second_army_exchange_list))
                else:
                    game_stats.second_army_exchange_list.remove(number)

        elif game_stats.game_board_panel == "quest log panel":
            if game_stats.event_panel_det is not None:
                p_funs = game_stats.event_panel_det.obj_funs
                p_button_zone = game_stats.event_panel_det.obj_button_zone
                square = game_stats.event_panel_det.square
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    game_stats.button_pressed = True

                button_numb = 0
                for square in p_button_zone:
                    button_numb += 1
                    ##            print("Level editor panel button " + str(button_numb))
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        p_funs[button_numb]()
                        game_stats.button_pressed = True
                        break

            square = [4, 169, 240, 538]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                game_stats.button_pressed = True
                y_axis = position[1]
                y_axis -= 169
                print(str(y_axis))
                y_axis = math.ceil(y_axis / 20)
                print(str(y_axis))

                if game_stats.quest_area == "Quest messages":
                    select_quest_message(y_axis)
                elif game_stats.quest_area == "Diplomatic messages":
                    select_diplomatic_message(y_axis)

        elif game_stats.game_board_panel == "diplomacy panel":
            square = [260, 109, 396, 316]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                game_stats.button_pressed = True
                select_contact(position)

            if game_stats.diplomacy_area == "Diplomatic actions":
                # Important additional condition
                # Requires to select counterpart for diplomatic interaction
                if game_stats.contact_inspection is not None:
                    button_numb = 0
                    for square in diplomacy_action_zone:
                        button_numb += 1
                        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                            diplomacy_actions_funs[button_numb]()
                            game_stats.button_pressed = True
                            break

            elif game_stats.diplomacy_area == "Declaration of war":
                button_numb = 0
                for square in diplomacy_declaration_of_war_zone:
                    button_numb += 1
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        diplomacy_declaration_of_war_funs[button_numb]()
                        game_stats.button_pressed = True
                        break

                square = [40, 338, 161, 520]
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    game_stats.button_pressed = True
                    select_cb(position)

                if game_stats.cb_details:
                    square = [170, 338, 185, 520]
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        game_stats.button_pressed = True
                        select_cb_item(position)

                if game_stats.war_goals:
                    square = [300, 338, 315, 520]
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        game_stats.button_pressed = True
                        select_war_goal(position)

            elif game_stats.diplomacy_area == "Sue for peace":
                button_numb = 0
                for square in diplomacy_sue_for_peace_zone:
                    button_numb += 1
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        diplomacy_sue_for_peace_funs[button_numb]()
                        game_stats.button_pressed = True
                        break

            elif game_stats.diplomacy_area == "Draft a peace offer":
                button_numb = 0
                for square in diplomacy_draft_a_peace_offer_zone:
                    button_numb += 1
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        diplomacy_draft_a_peace_offer_funs[button_numb]()
                        game_stats.button_pressed = True
                        break

                square = [40, 338, 161, 520]
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    game_stats.button_pressed = True
                    select_demand(position)

                if game_stats.demand_details:
                    square = [170, 338, 185, 520]
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        game_stats.button_pressed = True
                        select_demand_item(position)

                if game_stats.claimed_demands:
                    square = [340, 338, 355, 520]
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        game_stats.button_pressed = True
                        select_pressed_demand(position)

            elif game_stats.diplomacy_area == "Threaten":
                button_numb = 0
                for square in diplomacy_threaten_zone:
                    button_numb += 1
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        diplomacy_threaten_funs[button_numb]()
                        game_stats.button_pressed = True
                        break

                square = [40, 338, 161, 520]
                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    game_stats.button_pressed = True
                    select_threat(position)

                if game_stats.cb_details:
                    square = [170, 338, 185, 520]
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        game_stats.button_pressed = True
                        select_threat_item(position)

                if game_stats.war_goals:
                    square = [300, 338, 315, 520]
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        game_stats.button_pressed = True
                        select_threat_demand(position)

    # Right Panels' zone
    if game_stats.right_window != "":
        print("game_stats.right_window - " + str(game_stats.right_window))
        rp_funs = right_panel_buttons[game_stats.right_window]
        rp_button_zone = right_panel_zone[game_stats.right_window]

        button_numb = 0
        for square in rp_button_zone:
            button_numb += 1
            ##            print("Level editor panel button " + str(button_numb))
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                rp_funs[button_numb]()
                game_stats.button_pressed = True
                break

        if game_stats.rw_panel_det is not None and not game_stats.button_pressed:
            rp_funs = game_stats.rw_panel_det.obj_funs
            rp_button_zone = game_stats.rw_panel_det.obj_button_zone

            button_numb = 0
            for square in rp_button_zone:
                button_numb += 1

                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    rp_funs[button_numb]()
                    game_stats.button_pressed = True
                    break

            if game_stats.rw_panel_det is not None:
                if game_stats.rw_panel_det.click_scripts is not None:
                    game_stats.rw_panel_det.click_scripts(position)

    # Window panel
    if game_stats.game_board_panel != "":
        if game_stats.game_board_panel not in click_zone:
            pass
        else:
            square = click_zone[game_stats.game_board_panel]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                game_stats.button_pressed = True

    # Right window panel
    if game_stats.right_window != "":
        square = right_click_zone[game_stats.right_window]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            game_stats.button_pressed = True

    # Lower panel
    if game_stats.details_panel_mode != "":
        xVarDic = {"facility lower panel": 200,
                   "settlement lower panel": 0,
                   "army lower panel": 0}
        yVar = game_stats.game_window_height - 800
        xVar = xVarDic[game_stats.details_panel_mode]

        # print("game_stats.details_panel_mode - " + str(game_stats.details_panel_mode))
        lp_funs = lower_panel_buttons[game_stats.details_panel_mode]
        lp_button_zone = lower_panel_zone[game_stats.details_panel_mode]

        button_numb = 0

        for square in lp_button_zone:
            button_numb += 1
            # print("square - " + str(square))

            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                lp_funs[button_numb]()
                game_stats.button_pressed = True
                break

        square = [200 + xVar, 650 + yVar, 1080, 800 + yVar]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            game_stats.button_pressed = True

        if game_stats.details_panel_mode == "facility lower panel":
            if position[1] >= 684 + yVar and 405 <= position[0] <= 520:
                x2 = int(game_stats.info_tile[0])
                y2 = int(game_stats.info_tile[1])
                x2 -= int(game_stats.pov_pos[0])
                y2 -= int(game_stats.pov_pos[1])
                TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1
                TileObj = game_obj.game_map[TileNum]

                index_number = math.floor((position[1] - (684 + yVar)) / 30)
                if TileObj.lot == "City":  # Settlement
                    for city in game_obj.game_cities:
                        if city.city_id == game_stats.right_click_city:
                            if index_number < len(city.residency):
                                game_stats.i_p_index = int(index_number)
                else:  # Facility
                    if index_number < len(TileObj.lot.residency):
                        game_stats.i_p_index = int(index_number)

        elif game_stats.details_panel_mode == "army lower panel" \
                and game_stats.game_board_panel == "army exchange panel":
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
                print("number - " + str(number))
                approaching_army = None
                standing_army = None
                for army in game_obj.game_armies:
                    if army.army_id == game_stats.selected_army:
                        approaching_army = army
                    elif army.army_id == game_stats.selected_second_army:
                        standing_army = army

                if number not in game_stats.first_army_exchange_list:
                    if len(standing_army.units) - len(game_stats.second_army_exchange_list) + \
                            len(game_stats.first_army_exchange_list) < 20:
                        game_stats.first_army_exchange_list.append(number)
                        game_stats.first_army_exchange_list = sorted(game_stats.first_army_exchange_list,
                                                                     reverse=True)
                        print("first_army_exchange_list: " + str(game_stats.first_army_exchange_list))
                else:
                    game_stats.first_army_exchange_list.remove(number)

    # Click on game map
    if not game_stats.button_pressed:
        game_stats.selected_tile = []

        x = math.ceil((position[0] + 1) / 48)
        y = math.ceil((position[1] + 1) / 48)
        x = int(x) + int(game_stats.pov_pos[0])
        y = int(y) + int(game_stats.pov_pos[1])
        print("Coordinates - x " + str(x) + " y " + str(y))
        game_stats.selected_tile = [int(x), int(y)]

        # Index of selected tile in map list
        x2 = int(game_stats.selected_tile[0])
        y2 = int(game_stats.selected_tile[1])
        TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1
        print("TileNum is " + str(TileNum))

        # if game_obj.game_map[TileNum].army_id is not None:
        # print("army_id is " + str(game_obj.game_map[TileNum].army_id))

        # game_stats.game_board_panel = ""

        # Within map borders
        if 0 < x2 <= game_stats.cur_level_width:
            if 0 < y2 <= game_stats.cur_level_height:

                TileObj = game_obj.game_map[TileNum]

                # print("Army_id - " + str(game_obj.game_map[TileNum].army_id))
                if game_stats.selected_object == "":
                    # Select settlement
                    if TileObj.lot is not None and TileObj.lot == "City":
                        # print("Click on a settlement")
                        game_stats.selected_settlement = int(game_obj.game_map[TileNum].city_id)
                        # print("Settlement ID is " + str(game_obj.game_map[TileNum].city_id))
                        select_settlement()

                    # Select army
                    elif game_obj.game_map[TileNum].army_id is not None:
                        print("Select army - gf_misc_img_dict: " + str(game_stats.gf_misc_img_dict))
                        print("There is an army")
                        game_stats.selected_object = "Army"
                        game_stats.selected_army = int(game_obj.game_map[TileNum].army_id)
                        game_stats.details_panel_mode = "army lower panel"

                        for army in game_obj.game_armies:
                            if army.army_id == game_stats.selected_army:
                                if army.owner == game_stats.player_power:
                                    if len(army.route) > 0:
                                        route = list(army.route)
                                        route.insert(0, list(army.posxy))
                                        algo_path_arrows.construct_path(army.army_id, route)

                                    if army.action == "Besieging":
                                        game_stats.attacker_army_id = int(army.army_id)
                                        game_stats.attacker_realm = str(army.owner)

                                        settlement, defender = game_basic.find_siege(army)

                                        if defender is not None:
                                            game_stats.defender_army_id = int(defender.army_id)
                                            game_stats.defender_realm = str(defender.owner)

                                        game_stats.assault_allowed = True
                                        for defensive_structure in settlement.defences:
                                            if defensive_structure.provide_wall:
                                                game_stats.assault_allowed = False
                                                for def_object in defensive_structure.def_objects:
                                                    if def_object.state in ["Broken", "Opened"]:
                                                        game_stats.assault_allowed = True
                                                        break

                                        # Check available siege equipment
                                        if not game_stats.assault_allowed:
                                            if settlement.siege.siege_towers_ready + \
                                                    settlement.siege.battering_rams_ready > 0:
                                                game_stats.assault_allowed = True

                                        game_stats.blockaded_settlement_name = str(settlement.name)
                                        game_stats.selected_settlement = settlement.city_id

                                        game_stats.game_board_panel = "settlement blockade panel"

                                        # Update visuals
                                        print("Update visuals - gf_misc_img_dict: " + str(game_stats.gf_misc_img_dict))
                                        update_gf_game_board.update_regiment_sprites()
                                        update_gf_game_board.open_settlement_building_sprites()

                                    break

                        # Update visuals
                        update_gf_game_board.update_regiment_sprites()

                # Movement command on map display
                elif game_stats.selected_object == "Army":
                    for army in game_obj.game_armies:
                        if army.army_id == game_stats.selected_army:
                            if army.owner == game_stats.player_power:
                                if len(army.route) > 0 and [x2, y2] == army.route[-1]:
                                    if army.action == "Stand":
                                        print('army.action = "Ready to move"')
                                        army.action = "Ready to move"
                                else:
                                    if army.action == "Stand":
                                        print("Appoint destination")
                                        game_pathfinding.search_army_movement("Player",
                                                                              int(game_stats.selected_army),
                                                                              str(game_stats.player_power),
                                                                              [x2, y2])
                                    else:
                                        print("Stop march")
                                        army.route = army.route[0:1]
                                        army.path_arrows = army.path_arrows[0:1]

                                break


def game_board_surface_m3(position):
    game_stats.button_pressed = False
    print("game_board_surface_m3")
    # Next few steps make sure, that user didn't click on any buttons

    button_numb = 0
    for square in button_zone:
        button_numb += 1
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            game_stats.button_pressed = True
            break

    # Panels' zone
    if game_stats.game_board_panel != "":
        if game_stats.game_board_panel == "settlement panel" and game_stats.settlement_area == "Building":
            square = [1, 112, 639, 540]
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                game_stats.button_pressed = True

    # Lower panel
    if game_stats.details_panel_mode != "":
        yVar = game_stats.game_window_height - 800
        print("game_stats.details_panel_mode - " + str(game_stats.details_panel_mode))

        button_numb = 0

        square = [200, 600 + yVar, 1080, 800 + yVar]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            game_stats.button_pressed = True

    # Click on game map
    if not game_stats.button_pressed:
        game_stats.selected_tile = []

        x = math.ceil(position[0] / 48)
        y = math.ceil(position[1] / 48)
        x = int(x) + int(game_stats.pov_pos[0])
        y = int(y) + int(game_stats.pov_pos[1])
        print("RC: Coordinates - x " + str(x) + " y " + str(y))
        game_stats.selected_tile = [int(x), int(y)]

        # Index of selected tile in map list
        x2 = int(game_stats.selected_tile[0])
        y2 = int(game_stats.selected_tile[1])
        TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1
        print("RC: TileNum is " + str(TileNum))

        # If player has had selected an army, then it get deselected
        if game_stats.selected_object == "Army":
            game_stats.selected_object = ""
            game_stats.selected_army = -1
            game_stats.selected_second_army = -1
            game_stats.details_panel_mode = ""
            game_stats.game_board_panel = ""
            game_stats.first_army_exchange_list = []
            game_stats.second_army_exchange_list = []

            # Update visuals
            update_gf_game_board.remove_regiment_sprites()
            update_gf_game_board.remove_hero_sprites()

        # Or player has had selected a settlement, then it get deselected
        elif game_stats.selected_object == "Settlement":
            game_stats.selected_object = ""
            game_stats.selected_settlement = -1
            game_stats.details_panel_mode = ""

        # If no army selected, then pop up window will appear with information about selected tile
        # NOTE: maybe I need to rebuild this if segment
        elif not game_stats.info_tile or game_stats.info_tile != [int(x), int(y)]:
            game_stats.selected_object = "Tile"
            game_stats.info_tile = [int(x), int(y)]
            game_stats.right_click_pos = [int(position[0]), int(position[1])]
            game_stats.i_p_index = 0

            if game_obj.game_map[TileNum].lot is not None:
                # print("obj_typ " + str(game_obj.game_map[TileNum].lot))
                if game_obj.game_map[TileNum].lot == "City":
                    game_stats.details_panel_mode = "facility lower panel"
                    game_stats.right_click_city = int(game_obj.game_map[TileNum].city_id)
                elif game_obj.game_map[TileNum].lot.obj_typ == "Facility":
                    game_stats.details_panel_mode = "facility lower panel"

            # Check if territory belongs to anyone
            if game_obj.game_map[TileNum].city_id is None:
                # It belongs to nobody
                game_stats.tile_ownership = "Wild lands"
                game_stats.tile_flag_colors = []
            else:
                for settlement in game_obj.game_cities:
                    if settlement.city_id == game_obj.game_map[TileNum].city_id:
                        if settlement.owner == "Neutral":
                            # This tile belongs to a nearby neutral settlement
                            game_stats.tile_ownership = "Neutral lands"
                        else:
                            # Someone own this land
                            game_stats.tile_ownership = str(settlement.owner)
                            for realm in game_obj.game_powers:
                                if realm.name == settlement.owner:
                                    game_stats.tile_flag_colors = [str(realm.f_color), str(realm.s_color)]
        else:
            # Right click on the same tile, therefore information screen should be closed
            game_stats.tile_ownership = "Wild lands"
            game_stats.tile_flag_colors = []
            game_stats.info_tile = []
            game_stats.right_click_pos = []
            game_stats.selected_object = ""
            game_stats.i_p_index = 0
            game_stats.details_panel_mode = ""
            game_stats.right_click_city = -1


def exit_but():
    game_stats.current_screen = "Entrance Menu"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "main_menu_screen"
    game_stats.edit_instrument = ""
    game_stats.selected_tile = []
    game_stats.level_editor_panel = ""


def save_but():
    ##    level_save.save_game()
    print("To be done")


def realm_but():
    game_stats.game_board_panel = "realm panel"
    for power in game_obj.game_powers:
        if power.name == game_stats.player_power:
            game_stats.realm_inspection = power
            break


def quest_log_but():
    if game_stats.game_board_panel == "settlement blockade panel":
        game_stats.attacker_army_id = 0
        game_stats.attacker_realm = ""
        game_stats.defender_army_id = 0
        game_stats.defender_realm = ""

        game_stats.selected_settlement = -1
        game_stats.game_board_panel = ""

        game_stats.selected_object = ""
        game_stats.selected_army = -1
        game_stats.selected_second_army = -1
        game_stats.details_panel_mode = ""
        game_stats.first_army_exchange_list = []
        game_stats.second_army_exchange_list = []

        # Update visuals
        update_gf_game_board.update_settlement_misc_sprites()

    if game_stats.game_board_panel == "settlement panel":
        img_list = ["Icons/building_icon", "Icons/recruiting_icon", "Icons/heroes_icon",
                    "Icons/economy_icon", "Icons/factions_icon", "Icons/duration_icon", "Icons/paper_3_square_48",
                    "Icons/good_loyalty_icon", "Icons/bad_loyalty_icon"]
        update_gf_game_board.remove_settlement_misc_sprites(img_list)
        game_stats.gf_building_dict = {}

        game_stats.selected_object = ""
        game_stats.selected_settlement = -1
        game_stats.settlement_area = ""
        game_stats.game_board_panel = ""
        game_stats.details_panel_mode = ""
        game_stats.right_window = ""
        game_stats.rw_object = None
        game_stats.unit_for_hire = None
        game_stats.first_starting_skill = None
        game_stats.second_starting_skill = None
        game_stats.province_records = None
        game_stats.allocated_gains_records = None
        game_stats.allocated_sold_records = None
        game_stats.allocated_bought_records = None
        game_stats.allocated_requested_goods_records = None
        game_stats.pops_details = None

    for realm in game_obj.game_powers:
        # print(str(realm.name))
        # print(str(game_stats.player_power))
        if realm.name == game_stats.player_power:
            # print(str(treasury))
            game_stats.selected_quest_messages = realm.quests_messages
            break

    game_stats.game_board_panel = "quest log panel"
    game_stats.quest_area = "Quest messages"
    game_stats.selected_diplomatic_notifications = None
    game_stats.diplomatic_message_index = None
    game_stats.diplomatic_message_panel = None

    # Update visuals
    img_list = ["Icons/scales_icon", "Icons/wind_rose_icon"]
    update_gf_game_board.add_misc_sprites(img_list)


def diplomacy_but():
    if game_stats.game_board_panel == "war panel":
        close_war_panel_but()

    game_stats.game_board_panel = "diplomacy panel"
    game_stats.contact_index = 0
    game_stats.diplomacy_area = "Diplomatic actions"
    game_stats.casus_bellis = []
    game_stats.cb_details = []
    game_stats.war_goals = []
    game_stats.dip_summary = None
    game_stats.war_summary = None
    game_stats.peace_demands = []
    game_stats.demand_details = []
    game_stats.claimed_demands = []
    game_stats.calculated_pa_cost = 0
    game_stats.peace_offer_text = []
    game_stats.explored_contacts = []
    game_stats.summary_text = []
    game_stats.war_inspection = None
    game_stats.contact_inspection = None

    # print("dip_summary - " + str(game_stats.dip_summary))

    for power in game_obj.game_powers:
        if power.name == game_stats.player_power:
            game_stats.realm_inspection = power
            break

    for power in game_obj.game_powers:
        if power.name in game_stats.realm_inspection.contacts:
            # print(str(game_stats.realm_inspection.name) + " Contact - " + str(power.name))
            game_stats.explored_contacts.append([str(power.f_color), str(power.s_color), str(power.name)])


def previous_war_notification_but():
    if len(game_stats.ongoing_wars) <= 4:
        # Nothing happens
        game_stats.button_pressed = False
    else:
        if game_stats.war_notifications_index > 0:
            game_stats.war_notifications_index -= 1
        else:
            game_stats.war_notifications_index = len(game_stats.ongoing_wars) - 4


def next_war_notification_but():
    if len(game_stats.ongoing_wars) <= 4:
        # Nothing happens
        game_stats.button_pressed = False
    else:
        if game_stats.war_notifications_index < len(game_stats.ongoing_wars) - 4:
            game_stats.war_notifications_index += 1
        else:
            game_stats.war_notifications_index = 0


def select_war_notification(position):
    x_axis = position[0]
    x_axis -= 14
    print("select_war_notification - " + str(x_axis))
    if x_axis % 43 < 40:
        x_axis = math.ceil(x_axis / 43)
        print(str(x_axis))
        if x_axis <= len(game_stats.ongoing_wars):
            game_stats.button_pressed = True

            if game_stats.game_board_panel == "diplomacy panel":
                close_diplomacy_panel_but()

            opponent = game_stats.ongoing_wars[x_axis - 1 + game_stats.war_notifications_index]
            game_stats.game_board_panel = "war panel"
            for war in game_obj.game_wars:
                if war.initiator == game_stats.player_power \
                        or war.respondent == game_stats.player_power:
                    if war.initiator == opponent[2] \
                            or war.respondent == opponent[2]:
                        game_stats.war_inspection = war

                        for realm in game_obj.game_powers:
                            if realm.name == war.initiator:
                                game_stats.realm_inspection = realm
                                break

                        for realm in game_obj.game_powers:
                            if realm.name == war.respondent:
                                game_stats.contact_inspection = realm
                                break

                        game_diplomacy.prepare_war_summary()
                        break


def play_battle_but():
    battle_map_generation.create_battle_map()

    # New visuals
    game_stats.gf_settlement_dict = {}
    game_stats.gf_facility_dict = {}
    game_stats.gf_exploration_dict = {}
    game_stats.gf_misc_img_dict = {}

    # Update visuals for battle
    update_gf_battle.battle_update_sprites()
    update_gf_battle.update_misc_sprites()
    game_stats.gf_battle_effects_dict = {}

    click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
    click_sound.play()


def autobattle_but():
    attacker = None
    defender = None
    for army in game_obj.game_armies:
        if army.army_id == game_stats.attacker_army_id:
            attacker = army
        elif army.army_id == game_stats.defender_army_id:
            defender = army

    battle_result_script = None
    if attacker.action == "Besieging":
        game_stats.battle_type = "Siege"
    # print("game_stats.battle_type - " + str(game_stats.battle_type))
    # print("game_stats.attacker_army_id - " + str(game_stats.attacker_army_id))
    # print("game_stats.defender_army_id - " + str(game_stats.defender_army_id))

    game_autobattle.begin_battle(attacker, defender, game_stats.battle_type, battle_result_script)

    game_stats.attacker_realm = attacker.owner
    game_stats.defender_realm = defender.owner

    # game_stats.game_board_panel = ""

    click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
    click_sound.play()


def close_autobattle_results():
    print("close_autobattle_results()")
    attacker_realm = None
    defender_realm = None

    for realm in game_obj.game_powers:
        if realm.name == game_stats.attacker_army.owner:
            attacker_realm = realm
            break

    for realm in game_obj.game_powers:
        if realm.name == game_stats.defender_army.owner:
            defender_realm = realm
            break

    # game_board_panel is set to default before after_battle_processing()
    # in case this is special battle thus after_battle_processing() could launch battle_result_scripts
    game_stats.game_board_panel = ""

    game_autobattle.after_battle_processing(game_stats.attacker_army, game_stats.defender_army,
                                            game_stats.attacker_troops_power_level_list,
                                            game_stats.defender_troops_power_level_list,
                                            attacker_realm, defender_realm,
                                            game_stats.battle_type,
                                            game_stats.attacker_no_troops_left, game_stats.defender_no_troops_left,
                                            game_stats.battle_result, None)

    print("Set default values in game_stats")

    game_stats.battle_result = ""
    game_stats.result_statement = ""
    game_stats.earned_experience = 0
    game_stats.attacker_army = None
    game_stats.defender_army = None
    game_stats.attacker_troops_power_level_list = []
    game_stats.defender_troops_power_level_list = []
    game_stats.attacker_no_troops_left = False
    game_stats.defender_no_troops_left = False


def play_siege_but():
    attacker = None
    defender = None
    for army in game_obj.game_armies:
        if army.army_id == game_stats.attacker_army_id:
            army.action = "Fighting"
            attacker = army
        elif army.army_id == game_stats.defender_army_id:
            army.action = "Fighting"
            defender = army
            TileNum = int(army.location)
            TileObj = game_obj.game_map[TileNum]
            game_stats.battle_terrain = str(TileObj.terrain)
            game_stats.battle_conditions = str(TileObj.conditions)

    can_assault = True

    # settlement = None
    # for city in game_obj.game_cities:
    #     if city.city_id == game_stats.selected_settlement:
    #         settlement = city
    #         break

    if game_stats.assault_allowed:
        # game_stats.battle_type = "Siege"
        game_stats.game_board_panel = ""

        if game_stats.game_type == "singleplayer":
            game_stats.strategy_mode = False

        game_stats.current_screen = "Battle"
        print(game_stats.current_screen)
        game_stats.screen_to_draw = "battle_screen"

        siege_map_generation.generate_map(attacker, defender)

    click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
    click_sound.play()


def encircle_but():
    game_stats.selected_object = ""
    game_stats.selected_army = -1
    game_stats.details_panel_mode = ""
    game_stats.attacker_army_id = 0
    game_stats.attacker_realm = ""

    if game_stats.defender_army_id != 0:
        game_stats.defender_army_id = 0
        game_stats.defender_realm = ""

    game_stats.blockaded_settlement_name = ""
    game_stats.selected_settlement = -1
    game_stats.game_board_panel = ""

    # Update visuals
    game_stats.gf_building_dict = {}
    if "Icons/paper_2_square_50_x_40" in game_stats.gf_misc_img_dict:
        del game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"]

    click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
    click_sound.play()


def retreat_but():
    for army in game_obj.game_armies:
        if army.army_id == game_stats.attacker_army_id:
            army.action = "Stand"
            break

    if game_stats.defender_army_id != 0:
        for army in game_obj.game_armies:
            if army.army_id == game_stats.defender_army_id:
                army.action = "Stand"
                break

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_stats.selected_settlement:
            settlement.siege = None
            break

    game_stats.attacker_army_id = 0
    game_stats.attacker_realm = ""
    game_stats.defender_army_id = 0
    game_stats.defender_realm = ""

    game_stats.blockaded_settlement_name = ""
    game_stats.selected_settlement = -1
    game_stats.game_board_panel = ""

    # Update visuals
    game_stats.gf_building_dict = {}
    del game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"]

    click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
    click_sound.play()


def build_trebuchet():
    print("build_trebuchet()")
    the_siege = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            the_siege = city.siege
            break

    print("trebuchets_max_quantity - " + str(the_siege.trebuchets_max_quantity))

    if the_siege.trebuchets_ordered + the_siege.trebuchets_ready < the_siege.trebuchets_max_quantity:
        the_siege.trebuchets_ordered += 1
        the_siege.construction_orders.append(["Trebuchet", 0])

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()
    else:
        click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
        click_sound.play()

    print("trebuchets_ordered - " + str(the_siege.trebuchets_ordered))


def cancel_building_trebuchet():
    print("cancel_building_trebuchet()")
    the_siege = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            the_siege = city.siege
            break

    if the_siege.trebuchets_ordered > 0:
        the_siege.trebuchets_ordered -= 1
        index = -1
        condition = True
        while condition:
            if the_siege.construction_orders[index][0] == "Trebuchet":
                condition = False
                del the_siege.construction_orders[index]
                print("Construction orders: " + str(the_siege.construction_orders))
            else:
                index -= 1
                if abs(index) > len(the_siege.construction_orders):
                    condition = False

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
        click_sound.play()

    print("trebuchets_ordered - " + str(the_siege.trebuchets_ordered))


def build_siege_tower():
    print("build_siege_tower()")
    the_siege = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            the_siege = city.siege
            break

    print("siege_towers_max_quantity - " + str(the_siege.siege_towers_max_quantity))

    if the_siege.siege_towers_ordered + the_siege.siege_towers_ready < the_siege.siege_towers_max_quantity:
        the_siege.siege_towers_ordered += 1
        the_siege.battering_rams_max_quantity -= 1
        the_siege.construction_orders.append(["Siege tower", 0])

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()
    else:
        click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
        click_sound.play()

    print("siege_towers_ordered - " + str(the_siege.siege_towers_ordered))


def cancel_building_siege_tower():
    print("cancel_building_siege_tower()")
    the_siege = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            the_siege = city.siege
            break

    if the_siege.siege_towers_ordered > 0:
        the_siege.siege_towers_ordered -= 1
        the_siege.battering_rams_max_quantity += 1
        index = -1
        condition = True
        while condition:
            if the_siege.construction_orders[index][0] == "Siege tower":
                condition = False
                del the_siege.construction_orders[index]
                print("Construction orders: " + str(the_siege.construction_orders))
            else:
                index -= 1
                if abs(index) > len(the_siege.construction_orders):
                    condition = False

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
        click_sound.play()

    print("siege_towers_ordered - " + str(the_siege.siege_towers_ordered))


def build_battering_ram():
    print("build_battering_ram()")
    the_siege = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            the_siege = city.siege
            break

    print("battering_rams_max_quantity - " + str(the_siege.battering_rams_max_quantity))

    if the_siege.battering_rams_ordered + the_siege.battering_rams_ready < the_siege.battering_rams_max_quantity:
        the_siege.battering_rams_ordered += 1
        the_siege.siege_towers_max_quantity -= 1
        the_siege.construction_orders.append(["Battering ram", 0])

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()
    else:
        click_sound = pygame.mixer.Sound("Sound/Interface/Minimalist2.ogg")
        click_sound.play()

    print("battering_rams_ordered - " + str(the_siege.battering_rams_ordered))


def cancel_building_battering_ram():
    print("cancel_building_battering_ram()")
    the_siege = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            the_siege = city.siege
            break

    if the_siege.battering_rams_ordered > 0:
        the_siege.battering_rams_ordered -= 1
        the_siege.siege_towers_max_quantity += 1
        index = -1
        condition = True
        while condition:
            if the_siege.construction_orders[index][0] == "Battering ram":
                condition = False
                del the_siege.construction_orders[index]
                print("Construction orders: " + str(the_siege.construction_orders))
            else:
                index -= 1
                if abs(index) > len(the_siege.construction_orders):
                    condition = False

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
        click_sound.play()

    print("battering_rams_ordered - " + str(the_siege.battering_rams_ordered))


def select_settlement():
    game_stats.selected_object = "Settlement"
    game_stats.game_board_panel = "settlement panel"
    game_stats.details_panel_mode = "settlement lower panel"
    algo_building.check_requirements()

    game_stats.settlement_area = "Building"
    game_stats.building_row_index = 0

    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    list_of_rows = []
    for plot in settlement.buildings:
        if int(plot.screen_position[1]) not in list_of_rows:
            list_of_rows.append(int(plot.screen_position[1]))

    game_stats.building_rows_amount = max(list_of_rows)
    # print("list_of_rows - " + str(list_of_rows))

    # Update visuals
    update_gf_game_board.update_regiment_sprites()
    update_gf_game_board.update_settlement_misc_sprites()
    update_gf_game_board.open_settlement_building_sprites()


def close_settlement_panel_but():
    game_stats.selected_object = ""
    game_stats.selected_settlement = -1
    game_stats.settlement_area = ""
    game_stats.game_board_panel = ""
    game_stats.details_panel_mode = ""
    game_stats.right_window = ""
    game_stats.rw_object = None
    game_stats.unit_for_hire = None
    game_stats.first_starting_skill = None
    game_stats.second_starting_skill = None
    game_stats.province_records = None
    game_stats.allocated_gains_records = None
    game_stats.allocated_sold_records = None
    game_stats.allocated_bought_records = None
    game_stats.allocated_requested_goods_records = None
    game_stats.pops_details = None
    game_stats.building_rows_amount = 0
    game_stats.building_row_index = 0

    # Update visuals
    update_gf_game_board.remove_regiment_sprites()
    update_gf_game_board.remove_hero_sprites()
    img_list = ["Icons/building_icon", "Icons/recruiting_icon", "Icons/heroes_icon",
                "Icons/economy_icon", "Icons/factions_icon", "Icons/duration_icon", "Icons/paper_3_square_48",
                "Icons/good_loyalty_icon", "Icons/bad_loyalty_icon"]
    update_gf_game_board.remove_settlement_misc_sprites(img_list)
    game_stats.gf_building_dict = {}

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def next_turn_but():
    for realm in game_obj.game_powers:
        if realm.name == game_stats.player_power:
            # if not game_stats.new_tasks:
            #     print("game_stats.new_tasks: " + str(game_stats.new_tasks))
            # if realm.diplomatic_messages:
            #     print("diplomatic_messages: " + str(realm.diplomatic_messages))
            if not game_stats.new_tasks and not realm.diplomatic_messages:
                # Turn over hourglass icon
                game_stats.turn_hourglass = True

                realm.turn_completed = True
                print(str(realm.name) + "'s turn is " + str(realm.turn_completed))
            else:
                # print("-> quest_log_but")
                quest_log_but()
            break


def select_stationed_army_but():
    TileObj = None
    TileNum = None

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_stats.selected_settlement:
            x2 = int(settlement.posxy[0])
            y2 = int(settlement.posxy[1])
            # x2 -= int(game_stats.pov_pos[0])
            # y2 -= int(game_stats.pov_pos[1])

            TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1
            TileObj = game_obj.game_map[TileNum]
            break

    print("TileObj.army_id - " + str(TileObj.army_id))
    if TileObj.army_id is not None:
        # Stationed army
        army = None

        for army_obj in game_obj.game_armies:
            if army_obj.army_id == TileObj.army_id:
                army = army_obj
                break

        if len(army.units) < 5:
            print("There is less then 5 regiments in army, can't operate outside of settlement")
        else:
            print("Selected stationed army")
            game_stats.selected_object = "Army"
            game_stats.selected_army = int(game_obj.game_map[TileNum].army_id)

            game_stats.selected_settlement = -1
            game_stats.settlement_area = ""
            game_stats.game_board_panel = ""
            game_stats.details_panel_mode = "army lower panel"
            game_stats.right_window = ""
            game_stats.rw_object = None

            # Update visuals
            img_list = ["Icons/building_icon", "Icons/recruiting_icon", "Icons/heroes_icon",
                        "Icons/economy_icon", "Icons/factions_icon", "Icons/paper_3_square_48",
                        "Icons/good_loyalty_icon", "Icons/bad_loyalty_icon"]
            update_gf_game_board.remove_settlement_misc_sprites(img_list)
            game_stats.gf_building_dict = {}


def open_building_area():
    if game_stats.settlement_area == "Building":
        pass
    else:
        game_stats.settlement_area = "Building"
        game_stats.right_window = ""
        game_stats.rw_object = None
        algo_building.check_requirements()

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()


def open_recruiting_area():
    if game_stats.settlement_area == "Recruiting":
        pass
    else:
        game_stats.settlement_area = "Recruiting"
        game_stats.right_window = ""
        game_stats.rw_object = None
        game_stats.unit_for_hire = None

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()

        # Update visuals
        update_gf_game_board.update_regiment_sprites()
        img_list = ['Icons/duration_icon', 'Icons/paper_3_square_48']
        update_gf_game_board.add_misc_sprites(img_list)


def open_heroes_area():
    if game_stats.settlement_area == "Heroes":
        pass
    else:
        game_stats.settlement_area = "Heroes"
        game_stats.right_window = ""
        game_stats.rw_object = None
        game_stats.hero_for_hire = None

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()

        # Update visuals
        update_gf_game_board.update_regiment_sprites()
        img_list = ['Icons/duration_icon', 'Icons/paper_3_square_48']
        update_gf_game_board.add_misc_sprites(img_list)


def open_economy_area():
    if game_stats.settlement_area == "Economy":
        pass
    else:
        # print("game_stats.settlement_area = 'Economy'")
        game_stats.settlement_area = "Economy"
        game_stats.settlement_subsection = "Overview"
        game_stats.right_window = ""
        game_stats.rw_object = None
        game_stats.population_subsection_index = -1
        game_stats.pops_details = None
        # print("open_economy_area() - game_stats.allocated_gains_records - " + str(game_stats.allocated_gains_records))
        game_basic.gather_province_records()

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()


def open_factions_area():
    if game_stats.settlement_area == "Factions":
        pass
    else:
        game_stats.settlement_area = "Factions"
        game_stats.right_window = ""
        game_stats.rw_object = None
        game_stats.faction_screen_index = 0

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()

        # Update visuals
        img_list = ['Icons/good_loyalty_icon', 'Icons/bad_loyalty_icon']
        update_gf_game_board.add_misc_sprites(img_list)


def close_right_panel_but():
    game_stats.right_window = ""
    # game_stats.rw_object = None
    game_stats.rw_unit_info = None
    game_stats.rw_attack_info = None
    game_stats.rw_skill_info = None
    game_stats.skill_tree_level_index = 1
    game_stats.hero_information_option = None
    game_stats.rw_panel_det = None
    game_stats.selected_skill_info = None
    game_stats.hero_doesnt_know_this_skill = None
    game_stats.selected_new_attribute = None
    game_stats.selected_new_skill = None
    game_stats.selected_artifact_info = None
    game_stats.hero_in_settlement = None
    game_stats.inventory_is_full = None
    game_stats.hero_inventory = None
    game_stats.already_has_an_artifact = None
    game_stats.realm_artifact_collection = None
    game_stats.artifact_focus = None

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()

    # Update visuals
    img_list = ['Icons/paper_2_square_48', 'Icons/paper_square_40']
    update_gf_game_board.remove_settlement_misc_sprites(img_list)
    game_stats.gf_skills_dict = {}
    game_stats.gf_artifact_dict = {}


def complete_army_exchange_but():
    game_stats.game_board_panel = ""

    approaching_army = None
    standing_army = None
    approaching_army_ID = None
    standing_army_ID = None

    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:
            army.action = "Stand"
            approaching_army = army
            approaching_army_ID = int(army.army_id)
        elif army.army_id == game_stats.selected_second_army:
            army.action = "Stand"
            standing_army = army
            standing_army_ID = int(army.army_id)

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

    game_basic.establish_leader(approaching_army_ID, "Game")
    game_basic.establish_leader(standing_army_ID, "Game")


def plot_row_up():
    if game_stats.building_row_index > 0:
        game_stats.building_row_index -= 1

    click_sound = pygame.mixer.Sound("Sound/Interface/bookFlip3.ogg")
    click_sound.play()


def plot_row_down():
    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    list_of_rows = []
    for plot in settlement.buildings:
        if int(plot.screen_position[1]) not in list_of_rows:
            list_of_rows.append(int(plot.screen_position[1]))

    max_row = max(list_of_rows)
    # print("list_of_rows - " + str(list_of_rows))

    if game_stats.building_row_index < max_row - 4:
        game_stats.building_row_index += 1

    click_sound = pygame.mixer.Sound("Sound/Interface/bookFlip3.ogg")
    click_sound.play()


def build_new_structure(x_axis, y_axis):
    # Order to build a new structure
    power_name = None
    the_settlement = None
    cost = None
    the_plot = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            power_name = city.owner
            the_settlement = city
            for plot in city.buildings:
                if plot.upgrade is not None:
                    if plot.screen_position == [x_axis, y_axis + game_stats.building_row_index]:
                        the_plot = plot
                        cost = plot.upgrade.construction_cost
                        break
            break

    if cost is not None:
        treasury = None
        for realm in game_obj.game_powers:
            if realm.name == power_name:
                treasury = realm.coffers
                break
        print(str(power_name) + ", treasury " + str(treasury) + ", cost " + str(cost))
        if algo_building.check_available_resources(treasury, cost) \
                and the_plot.upgrade.fulfilled_conditions:
            algo_building.consume_constructions_materials(treasury, cost, the_settlement)
            algo_building.start_construction(the_plot)

            click_sound = pygame.mixer.Sound("Sound/Interface/mining.wav")
            click_sound.play()


def show_building_upgrade_information(x_axis, y_axis):
    the_plot = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            for plot in city.buildings:
                if plot.upgrade is not None:
                    if plot.screen_position == [x_axis, y_axis + game_stats.building_row_index]:
                        the_plot = plot
                        print("Position - " + str(plot.screen_position))
                        break
            break

    if the_plot is not None:
        game_stats.right_window = "Building upgrade information"
        game_stats.rw_object = the_plot.upgrade
        # Update visuals
        update_gf_game_board.add_settlement_building_sprites(the_plot.upgrade.name,
                                                             the_plot.upgrade.img)

        click_sound = pygame.mixer.Sound("Sound/Interface/bookFlip1.ogg")
        click_sound.play()


def settlement_regiment_information():
    if game_stats.unit_for_hire is not None:
        game_stats.right_window = "New regiment information"

    u = game_stats.rw_object
    settlement = None
    f_color = None
    s_color = None
    total_HP = int(len(u.crew) * u.base_HP)
    attack = u.attacks[0]

    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city

    for realm in game_obj.game_powers:
        if realm.name == settlement.owner:
            f_color = realm.f_color
            s_color = realm.s_color

    print("Morale - " + str(u.morale) + ", Leadership - " + str(u.leadership))
    game_stats.rw_unit_info = game_classes.Regiment_Info_Card(u.name, f_color, s_color, len(u.crew), total_HP, u.morale,
                                                              u.base_HP, u.experience, u.speed, u.base_leadership,
                                                              u.engaged, u.deserted, len(u.attacks), u.armour, u.defence,
                                                              u.reg_tags, u.magic_power, u.mana_reserve,
                                                              u.max_mana_reserve, u.abilities)

    game_stats.rw_attack_info = game_classes.Attack_Info_Card(attack.name, attack.attack_type, attack.min_dmg,
                                                              attack.max_dmg, attack.mastery, attack.effective_range,
                                                              attack.range_limit, attack.tags)

    game_stats.rw_skill_info = None

    s = None
    value_text = str(None)
    if len(u.skills) > 0:
        s = u.skills[0]
        if s.quantity is not None:
            value_text = str(s.quantity)
        elif s.quality is not None:
            value_text = str(s.quality)
        else:
            value_text = ""
        game_stats.rw_skill_info = game_classes.Skill_Info_Card(s.name, s.application, value_text, str(s.skill_tags))


def hire_regiment():
    permit_unit_creation = False
    if game_stats.unit_for_hire is not None:
        permit_unit_creation = True

    # Index of settlement's tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.cur_level_width + x - 1

    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    if game_obj.game_map[TileNum].army_id is None:
        owner = settlement.owner
        game_stats.army_id_counter += 1
        game_obj.game_map[TileNum].army_id = int(game_stats.army_id_counter)
        game_obj.game_armies.append(game_classes.Army([x, y], int(TileNum),
                                                      int(game_stats.army_id_counter),
                                                      str(owner),
                                                      random.choice([True, False])))
        print("Created new army, ID - " + str(game_stats.army_id_counter))

    # Check available recruitment
    if game_stats.unit_for_hire.ready_units == 0:
        permit_unit_creation = False

    if not game_stats.enough_resources_to_pay:
        permit_unit_creation = False

    if permit_unit_creation:
        for army in game_obj.game_armies:
            if army.army_id == game_obj.game_map[TileNum].army_id:
                if len(army.units) < 20:
                    units_list = list(create_unit.LE_units_dict_by_alignment[settlement.alignment])

                    for new_unit in units_list:
                        if new_unit.name == game_stats.unit_for_hire.unit_name:
                            army.units.append(copy.deepcopy(new_unit))
                            print("Added to army new unit - " + new_unit.name)
                            print("Img - " + new_unit.img)
                            game_basic.establish_leader(army.army_id, "Game")

                            game_stats.unit_for_hire.ready_units -= 1
                            game_basic.realm_payment_for_object(game_stats.rw_object.name, settlement)
                            game_stats.enough_resources_to_pay = game_basic.enough_resources_to_hire(game_stats.rw_object.name,
                                                                                                     settlement)
                            # game_basic.enough_resources_to_hire()
                            break
                break


def new_hero_skill_tree():
    if game_stats.hero_for_hire is not None:
        game_stats.right_window = "New hero skill tree"
        game_stats.skill_tree_level_index = 1


def skill_tree_level_prev():
    if game_stats.skill_tree_level_index == 1:
        pass
    else:
        game_stats.skill_tree_level_index -= 1


def skill_tree_level_next():
    print("Skill tree level - " + str(game_stats.skill_tree_level_index))
    cutoff = 5
    if game_stats.right_window == "Hero window":
        cutoff = 6
    if game_stats.skill_tree_level_index == cutoff:
        pass
    else:
        game_stats.skill_tree_level_index += 1


def remove_artifact_from_inventory():
    # print("remove_artifact_from_inventory")
    if game_stats.artifact_focus == "Hero's inventory":
        hero = game_stats.rw_object
        # print(str(game_stats.selected_artifact_info))
        # print(game_stats.selected_artifact_info.name)
        # print("len(hero.inventory) - " + str(len(hero.inventory)))
        # print("len(game_stats.realm_artifact_collection) - " + str(len(game_stats.realm_artifact_collection)))
        for artifact in hero.inventory:
            if artifact.name == game_stats.selected_artifact_info.name:
                artifact.blocked = 0
                game_stats.realm_artifact_collection.append(artifact)
                hero.inventory.remove(artifact)
                break

        game_stats.selected_artifact_info = None
        game_stats.artifact_focus = None
        # print("again len(hero.inventory) - " + str(len(hero.inventory)))
        # print("again len(game_stats.realm_artifact_collection) - " + str(len(game_stats.realm_artifact_collection)))
        # for element in game_stats.realm_artifact_collection:
        #     print(str(element))


def equip_artifact_from_collection():
    if game_stats.artifact_focus == "Realm's artifact collection":
        hero = game_stats.rw_object
        for artifact in game_stats.realm_artifact_collection:
            if artifact.name == game_stats.selected_artifact_info.name:
                artifact.blocked = 1
                hero.inventory.append(artifact)
                game_stats.realm_artifact_collection.remove(artifact)
                break

        game_stats.selected_artifact_info = None
        game_stats.artifact_focus = None


def hire_hero():
    permit_hero_creation = False
    if game_stats.hero_for_hire is not None:
        permit_hero_creation = True

    print("permit_hero_creation - " + str(permit_hero_creation))

    # Index of settlement's tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    # print("game_stats.new_level_width - " + str(game_stats.new_level_width))
    TileNum = (y - 1) * game_stats.cur_level_width + x - 1
    print("game_stats.selected_tile - " + str(game_stats.selected_tile) + "; TileNum - " + str(TileNum))

    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    treasury = None
    for realm in game_obj.game_powers:
        if realm.name == settlement.owner:
            treasury = realm.coffers
            break

    print("enough_resources_to_pay - " + str(game_stats.enough_resources_to_pay))
    if not game_stats.enough_resources_to_pay:
        permit_hero_creation = False

    print("permit_hero_creation - " + str(permit_hero_creation))
    print("selected_tile TileNum - " + str(TileNum))
    print("selected_tile posxy - " + str(game_obj.game_map[TileNum].posxy))
    print("game_map[TileNum].army_id - " + str(game_obj.game_map[TileNum].army_id))
    if game_obj.game_map[TileNum].army_id is not None:
        the_army = None
        for army in game_obj.game_armies:
            if army.army_id == game_obj.game_map[TileNum].army_id:
                the_army = army
                if army.hero is not None:
                    permit_hero_creation = False
                    break

        if permit_hero_creation:
            print("the_army.army_id - " + str(the_army.army_id))
            hero_class = game_stats.hero_for_hire[0]
            game_stats.hero_id_counter += 1
            if not starting_skills.locked_first_skill_check[hero_class]:
                first_skill_name = starting_skills.starting_skills_by_class[hero_class][game_stats.first_starting_skill]
            else:
                first_skill_name = starting_skills.locked_first_skill_by_class[hero_class]
            first_skill = hero_skill_catalog.hero_skill_data[first_skill_name]
            second_skill_name = starting_skills.starting_skills_by_class[hero_class][game_stats.second_starting_skill]
            second_skill = hero_skill_catalog.hero_skill_data[second_skill_name]

            the_army.hero = game_classes.Hero(int(game_stats.hero_id_counter),  # hero_id
                                              str(random.choice(hero_names.hero_classes_cat[hero_class])),
                                              str(game_stats.hero_for_hire[0]),  # hero_class
                                              int(game_stats.hero_for_hire[3]),  # level
                                              0,  # experience
                                              int(game_stats.hero_for_hire[1]),  # magic_power
                                              int(game_stats.hero_for_hire[2]),  # knowledge
                                              list(game_stats.hero_for_hire[8]),  # attributes_list
                                              str(game_stats.hero_for_hire[4]),  # img
                                              str(game_stats.hero_for_hire[5]),  # img_source
                                              int(game_stats.hero_for_hire[6]),  # x_offset
                                              int(game_stats.hero_for_hire[7]),  # y_offset
                                              [skill_classes.Hero_Skill(str(first_skill_name),
                                                                        str(first_skill[0]),
                                                                        str(first_skill[1]),
                                                                        str(first_skill[2]),
                                                                        str(first_skill[3]),
                                                                        str(first_skill[4]),
                                                                        list(first_skill[5]),
                                                                        list(first_skill[6]),
                                                                        first_skill[7],
                                                                        [0, 0]),
                                               skill_classes.Hero_Skill(str(second_skill_name),
                                                                        str(second_skill[0]),
                                                                        str(second_skill[1]),
                                                                        str(second_skill[2]),
                                                                        str(second_skill[3]),
                                                                        str(second_skill[4]),
                                                                        list(second_skill[5]),
                                                                        list(second_skill[6]),
                                                                        second_skill[7],
                                                                        [0, 1])],  # skills
                                              int(game_stats.hero_for_hire[2]) * 10,  # maximum mana reserve
                                              int(game_stats.hero_for_hire[2]) * 10)  # mana reserve

            # action1 = ability_classes.Ability_Action("Increase morale",
            #                                          "Direct order - increase morale",
            #                                          "Addition")
            # ability = ability_classes.Hero_Ability("Direct order",
            #                                        "Horn",
            #                                        "Abilities\Tactics",
            #                                        "Tactics",
            #                                        [action1, action2],
            #                                        [],
            #                                        "single_ally")
            the_army.hero.abilities.append("Direct order")
            game_basic.learn_new_abilities(first_skill_name, the_army.hero)
            game_basic.learn_new_abilities(second_skill_name, the_army.hero)

            new_experience, bonus_level = game_basic.increase_level_for_new_heroes(settlement)

            game_basic.hero_next_level(the_army.hero, new_experience)

            for res in treasury:
                depleted = False
                if "Florins" == res[0]:
                    res[1] -= 2000 + (game_stats.hero_for_hire[3] + bonus_level - 1) * 250
                    if res[1] == 0:
                        depleted = True

                if depleted:
                    for delete_res in treasury:
                        if res[0] == delete_res[0]:
                            treasury.remove(delete_res)

            # Update visuals
            update_gf_game_board.update_regiment_sprites()


def next_first_starting_skill():
    print("next_first_starting_skill")
    if game_stats.hero_for_hire[0] is not None:
        hero_class = game_stats.hero_for_hire[0]

        if not starting_skills.locked_first_skill_check[hero_class]:
            max_index = len(starting_skills.starting_skills_by_class[hero_class]) - 1
            if game_stats.first_starting_skill + 1 == game_stats.second_starting_skill:
                if game_stats.first_starting_skill + 2 > max_index:
                    game_stats.first_starting_skill = 0
                else:
                    game_stats.first_starting_skill += 2

            elif game_stats.first_starting_skill + 1 > max_index:
                if game_stats.second_starting_skill == 0:
                    game_stats.first_starting_skill = 1
                else:
                    game_stats.first_starting_skill = 0

            else:
                game_stats.first_starting_skill += 1

        else:
            pass


def next_second_starting_skill():
    print("next_second_starting_skill")
    if game_stats.hero_for_hire[0] is not None:
        hero_class = game_stats.hero_for_hire[0]

        max_index = len(starting_skills.starting_skills_by_class[hero_class]) - 1
        if game_stats.second_starting_skill + 1 == game_stats.first_starting_skill:
            if game_stats.second_starting_skill + 2 > max_index:
                game_stats.second_starting_skill = 0
            else:
                game_stats.second_starting_skill += 2

        elif game_stats.second_starting_skill + 1 > max_index:
            if game_stats.first_starting_skill == 0:
                game_stats.second_starting_skill = 1
            else:
                game_stats.second_starting_skill = 0

        else:
            game_stats.second_starting_skill += 1


def open_overview_section():
    if game_stats.settlement_subsection == "Overview":
        pass
    else:
        game_stats.settlement_subsection = "Overview"
        game_stats.right_window = ""
        game_stats.rw_object = None
        game_stats.population_subsection_index = -1
        game_stats.pops_details = None
        game_basic.gather_province_records()

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()


def open_population_section():
    if game_stats.settlement_subsection == "Population":
        pass
    else:
        game_stats.settlement_subsection = "Population"
        game_stats.right_window = ""
        game_stats.rw_object = None
        game_stats.population_subsection_index = -1
        game_stats.pops_card_index = 0
        game_stats.pops_details = None

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()


def up_pops_card_index():
    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    num = 0
    for pops in settlement.residency:
        # print(pops.name)
        num += 1

    for TileNum in settlement.property:
        TileObj = game_obj.game_map[TileNum]
        for pops in TileObj.lot.residency:
            # print(pops.name)
            num += 1

    if game_stats.pops_card_index == 0:
        if num <= 9:
            game_stats.pops_card_index = 0
        else:
            game_stats.pops_card_index = int(num - 9)
    else:
        game_stats.pops_card_index -= 1


def down_pops_card_index():
    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    num = 0
    for pops in settlement.residency:
        # print(pops.name)
        num += 1

    for TileNum in settlement.property:
        TileObj = game_obj.game_map[TileNum]
        for pops in TileObj.lot.residency:
            # print(pops.name)
            num += 1

    print("pops_card_index - " + str(game_stats.pops_card_index) + ", num - " + str(num))
    if game_stats.pops_card_index < num - 9:
        game_stats.pops_card_index += 1
    else:
        game_stats.pops_card_index = 0


def up_faction_pops_index():
    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    if game_stats.faction_pops_index > 0:
        game_stats.faction_pops_index -= 1
    else:
        if len(settlement.factions[game_stats.faction_screen_index].members) <= 6:
            game_stats.faction_pops_index = 0
        else:
            game_stats.faction_pops_index = int(len(settlement.factions[game_stats.faction_screen_index].members) - 6)


def down_faction_pops_index():
    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    if len(settlement.factions[game_stats.faction_screen_index].members) <= 6:
        game_stats.faction_pops_index = 0
    else:
        if game_stats.faction_pops_index < int(len(settlement.factions[game_stats.faction_screen_index].members) - 6):
            game_stats.faction_pops_index += 1
        else:
            game_stats.faction_pops_index = 0


def open_local_market_section():
    if game_stats.settlement_subsection == "Local market":
        pass
    else:
        # print("Local market")
        game_stats.settlement_subsection = "Local market"
        game_stats.right_window = ""
        game_stats.rw_object = None
        game_basic.snapshot_local_market()

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()


def open_trade_routes_section():
    if game_stats.settlement_subsection == "Trade routes":
        pass
    else:
        game_stats.settlement_subsection = "Trade routes"
        game_stats.right_window = ""
        game_stats.rw_object = None

        click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
        click_sound.play()


def select_pops(position):
    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    y_axis = position[1]
    y_axis -= 142
    print("y_axis - " + str(y_axis))
    y_axis = math.ceil(y_axis / 44)
    print("math.ceil(y_axis / 44) - " + str(y_axis))
    game_stats.population_subsection_index = int(y_axis - 1 + game_stats.pops_card_index)
    num = 0
    proceed = True
    for pops in settlement.residency:
        print(pops.name)
        if num == y_axis - 1 + game_stats.pops_card_index:
            game_stats.pops_details = pops
            proceed = False
        num += 1

    if proceed:
        for TileNum in settlement.property:
            TileObj = game_obj.game_map[TileNum]
            for pops in TileObj.lot.residency:
                print(pops.name)
                if num == y_axis - 1 + game_stats.pops_card_index:
                    game_stats.pops_details = pops
                num += 1


def open_hero_information():
    game_stats.right_window = "Hero window"
    game_stats.hero_information_option = "Skills"
    game_stats.rw_panel_det = game_classes.Object_Surface({},
                                                          [],
                                                          None,
                                                          rw_click_scripts.hero_skills)

    # Selected army
    if game_stats.selected_army != -1:
        for army in game_obj.game_armies:
            if army.army_id == game_stats.selected_army:
                game_stats.rw_object = army.hero

                for realm in game_obj.game_powers:
                    if realm.name == army.owner:
                        game_stats.realm_artifact_collection = realm.artifact_collection
                        break

                break

    # Selected settlement
    elif game_stats.selected_settlement != -1:
        for settlement in game_obj.game_cities:
            if settlement.city_id == game_stats.selected_settlement:
                x2 = int(settlement.posxy[0])
                y2 = int(settlement.posxy[1])
                TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1
                print("[x2, y2] - [" + str(x2) + ", " + str(y2) + "], TileNim - " + str(TileNum))
                TileObj = game_obj.game_map[TileNum]
                print("army_id - " + str(TileObj.army_id))

                for army in game_obj.game_armies:
                    if army.army_id == TileObj.army_id:
                        game_stats.rw_object = army.hero
                        break

                for realm in game_obj.game_powers:
                    if realm.name == settlement.owner:
                        game_stats.realm_artifact_collection = realm.artifact_collection
                        break

                break

    # Update visuals
    img_list = ['Icons/paper_2_square_48', 'Icons/paper_square_40']
    update_gf_game_board.add_misc_sprites(img_list)
    update_gf_game_board.update_skills_sprites()


def hero_information_window_skills_option():
    game_stats.hero_information_option = "Skills"
    game_stats.rw_panel_det = game_classes.Object_Surface({},
                                                          [],
                                                          None,
                                                          rw_click_scripts.hero_skills)


def hero_information_window_attributes_tree_option():
    game_stats.hero_information_option = "Attributes tree"
    game_stats.skill_tree_level_index = game_stats.rw_object.attribute_points_used
    game_stats.rw_panel_det = game_classes.Object_Surface({1: skill_tree_level_prev,
                                                           2: skill_tree_level_next},
                                                          [[864, 271, 883, 290],
                                                           [1254, 271, 1273, 290]],
                                                          None,
                                                          rw_click_scripts.hero_attributes)


def hero_information_window_inventory_option():
    game_stats.hero_information_option = "Inventory"
    game_stats.rw_panel_det = game_classes.Object_Surface({1: remove_artifact_from_inventory,
                                                           2: equip_artifact_from_collection},
                                                          [[864, 491, 965, 511],
                                                           [864, 516, 965, 536]],
                                                          None,
                                                          rw_click_scripts.hero_inventory)

    # Update visuals
    update_gf_game_board.update_artifact_sprites()


def buy_artifact():
    if game_stats.enough_resources_to_pay:
        # Index of settlement's tile in map list
        x = int(game_stats.selected_tile[0])
        y = int(game_stats.selected_tile[1])
        TileNum = (y - 1) * game_stats.cur_level_width + x - 1

        if game_obj.game_map[TileNum].army_id is not None:
            for army in game_obj.game_armies:
                if army.army_id == game_obj.game_map[TileNum].army_id:
                    if army.hero is not None:
                        pass


def close_realm_panel_but():
    game_stats.game_board_panel = ""
    game_stats.realm_inspection = None

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def close_quest_log_panel_but():
    game_stats.game_board_panel = ""
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_stats.selected_quest_messages = None
    game_stats.selected_diplomatic_notifications = None
    game_stats.diplomatic_message_index = None
    game_stats.diplomatic_message_panel = None

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def open_quest_messages_area():
    game_stats.quest_area = "Quest messages"
    game_stats.selected_diplomatic_notifications = None
    game_stats.diplomatic_message_index = None
    game_stats.diplomatic_message_panel = None
    for realm in game_obj.game_powers:
        # print(str(realm.name))
        # print(str(game_stats.player_power))
        if realm.name == game_stats.player_power:
            game_stats.selected_quest_messages = realm.quests_messages
            break


def open_diplomatic_messages_area():
    game_stats.quest_area = "Diplomatic messages"
    game_stats.selected_quest_messages = None
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    for realm in game_obj.game_powers:
        if realm.name == game_stats.player_power:
            game_stats.selected_diplomatic_notifications = realm.diplomatic_messages
            break


def select_quest_message(index):
    realm_dilemma_message_dict = {"Knight Lords": knight_lords_dilemma_messages.message_dict}
    realm_quest_message_dict = {"Knight Lords": knight_lords_quest_messages.message_dict}
    realm_dilemma_panel_det = {"Knight Lords": knight_lords_dilemma_det.details_dict}
    realm_quest_panel_det = {"Knight Lords": knight_lords_quest_det.details_dict}

    quest_log = None
    # for realm in game_obj.game_powers:
    #     if realm.name == game_stats.player_power:
    #         quest_log = realm.quests_messages
    #         break

    quest_log = game_stats.selected_quest_messages

    if index <= len(quest_log):
        game_stats.quest_message_index = int(index - 1)

        alignment = quest_log[game_stats.quest_message_index].alignment
        quest_name = quest_log[game_stats.quest_message_index].name

        if quest_name in realm_quest_message_dict[alignment]:
            game_stats.quest_message_panel = realm_quest_message_dict[alignment][quest_name]
        elif quest_name in realm_dilemma_message_dict[alignment]:
            game_stats.quest_message_panel = realm_dilemma_message_dict[alignment][quest_name]

        if quest_name in realm_quest_panel_det[alignment]:
            realm_quest_panel_det[alignment][quest_name]()
        elif quest_name in realm_dilemma_panel_det[alignment]:
            realm_dilemma_panel_det[alignment][quest_name]()


def select_diplomatic_message(index):
    notification_log = game_stats.selected_diplomatic_notifications
    if index <= len(notification_log):
        game_stats.diplomatic_message_index = int(index - 1)
        message_subject = notification_log[game_stats.diplomatic_message_index].subject

        game_stats.diplomatic_message_panel = diplomatic_messages_text.text_dict[message_subject]
        diplomatic_messages_det.details_dict[message_subject]()


def close_diplomacy_panel_but():
    game_stats.game_board_panel = ""
    game_stats.realm_inspection = None
    game_stats.explored_contacts = []
    game_stats.contact_inspection = None
    game_stats.casus_bellis = []
    game_stats.cb_details = []
    game_stats.war_goals = []
    game_stats.dip_summary = None
    game_stats.war_summary = None
    game_stats.peace_demands = []
    game_stats.demand_details = []
    game_stats.claimed_demands = []
    game_stats.calculated_pa_cost = 0
    game_stats.peace_offer_text = []
    game_stats.explored_contacts = []
    game_stats.summary_text = []

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def previous_contact_but():
    if game_stats.contact_index > 0:
        game_stats.contact_index -= 1
    elif len(game_stats.explored_contacts) > 13:
        game_stats.contact_index = len(game_stats.explored_contacts) - 13


def next_contact_but():
    if len(game_stats.explored_contacts) > 13:
        if game_stats.contact_index < len(game_stats.explored_contacts) - 13:
            game_stats.contact_index += 1
        else:
            game_stats.contact_index = 0


def select_contact(position):
    y_axis = position[1]
    y_axis -= 109
    # print(str(y_axis))
    y_axis = math.ceil(y_axis / 16)
    # print(str(y_axis))

    if y_axis <= len(game_stats.explored_contacts):
        realm_name = game_stats.explored_contacts[y_axis + game_stats.contact_index - 1][2]
        # print(str(realm_name))

        for realm in game_obj.game_powers:
            if realm.name == realm_name:
                game_stats.contact_inspection = realm
                # print("Selected " + str(realm.name))
                # print(str(game_stats.contact_inspection.name))
                break

        # game_diplomacy.prepare_summary()
        return_to_diplomatic_actions_area_but()


def declare_war_or_sue_for_peace_action_but():
    if game_stats.dip_summary.ongoing_war:
        game_stats.diplomacy_area = "Sue for peace"
        game_diplomacy.prepare_war_summary()
    else:
        game_stats.diplomacy_area = "Declaration of war"
        game_diplomacy.prepare_casus_bellis()


def return_to_diplomatic_actions_area_but():
    # print("return_to_diplomatic_actions_area_but")
    game_stats.diplomacy_area = "Diplomatic actions"
    game_stats.casus_bellis = []
    game_stats.cb_details = []
    game_stats.war_goals = []
    game_stats.war_summary = None
    game_stats.summary_text = []
    game_diplomacy.prepare_summary()

    # print("")
    # print("return_to_diplomatic_actions_area_but")
    # for realm in game_stats.realm_inspection.relations.at_war:
    #     print("At war with " + str(realm[2]) + " " + str(realm[0]) + " " + str(realm[1]))


def declare_war_but():
    if game_stats.war_goals:
        game_diplomacy.declare_war()


def select_cb(position):
    y_axis = position[1]
    y_axis -= 338
    print(str(y_axis))
    y_axis = math.ceil(y_axis / 17)
    print(str(y_axis))

    if y_axis <= len(game_stats.casus_bellis):
        game_stats.cb_details = []
        game_diplomacy.cb_details_dict[game_stats.casus_bellis[y_axis - 1]]()


def select_cb_item(position):
    y_axis = position[1]
    y_axis -= 338
    print(str(y_axis))
    y_axis = math.ceil(y_axis / 17)
    print(str(y_axis))

    if y_axis <= len(game_stats.cb_details):
        game_diplomacy.add_war_goal(game_stats.cb_details.pop(y_axis - 1))


def select_war_goal(position):
    y_axis = position[1]
    y_axis -= 338
    print(str(y_axis))
    y_axis = math.ceil(y_axis / 17) - 1
    print(str(y_axis))

    num = 0
    cb = None
    wg_num = 0
    for goal in game_stats.war_goals:
        if cb is None:
            if num == y_axis:
                break
            else:
                cb = goal[2]
                num += 1

            if num == y_axis:
                print("select_war_goal - 1")
                game_diplomacy.remove_war_goal(wg_num)
            else:
                wg_num += 1
                num += 1

        elif cb != goal[2]:
            if num == y_axis:
                break
            else:
                cb = goal[2]
                num += 1

            if num == y_axis:
                print("select_war_goal - 2")
                game_diplomacy.remove_war_goal(wg_num)
            else:
                wg_num += 1
                num += 1

        else:
            if num == y_axis:
                print("select_war_goal - 3")
                game_diplomacy.remove_war_goal(wg_num)
            else:
                wg_num += 1
                num += 1


def draft_a_peace_offer_but():
    # print(game_stats.war_summary)
    print(game_stats.war_summary.war_goals)
    game_stats.claimed_demands = []
    game_stats.calculated_pa_cost = 0
    game_stats.peace_offer_text = []
    game_stats.summary_text = []
    game_stats.diplomacy_area = "Draft a peace offer"

    if game_stats.war_summary.own_realm_war_enthusiasm >= game_stats.war_summary.opponent_war_enthusiasm:
        game_stats.make_demands = True
    else:
        game_stats.make_demands = False

    game_diplomacy.prepare_peace_demands_summary()


def return_to_sue_for_peace_area_but():
    game_stats.claimed_demands = []
    game_stats.calculated_pa_cost = 0
    game_stats.peace_offer_text = []
    game_stats.summary_text = []
    game_stats.diplomacy_area = "Sue for peace"
    game_diplomacy.prepare_war_summary()


def change_between_demands_and_concessions_but():
    if game_stats.make_demands:
        game_stats.make_demands = False
        game_stats.demand_details = []
        game_stats.claimed_demands = []
        game_diplomacy.prepare_peace_demands_summary()
    else:
        game_stats.make_demands = True
        game_stats.demand_details = []
        game_stats.claimed_demands = []
        game_diplomacy.prepare_peace_demands_summary()


def propose_peace_offer_but():
    if game_stats.claimed_demands:
        if game_stats.will_accept_peace_agreement:
            game_diplomacy.propose_peace_agreement()
            return_to_sue_for_peace_area_but()
    else:
        if game_stats.will_accept_white_peace:
            game_diplomacy.propose_white_peace()
            return_to_sue_for_peace_area_but()


def select_demand(position):
    y_axis = position[1]
    y_axis -= 338
    print(str(y_axis))
    y_axis = math.ceil(y_axis / 17)
    print(str(y_axis))

    if y_axis <= len(game_stats.peace_demands):
        game_stats.demand_details = []
        game_diplomacy.demands_details_dict[game_stats.peace_demands[y_axis - 1]]()


def select_demand_item(position):
    y_axis = position[1]
    y_axis -= 338
    print(str(y_axis))
    y_axis = math.ceil(y_axis / 17)
    print(str(y_axis))

    if y_axis <= len(game_stats.demand_details):
        game_diplomacy.add_demand(game_stats.demand_details.pop(y_axis - 1))


def select_pressed_demand(position):
    y_axis = position[1]
    y_axis -= 338
    print(str(y_axis))
    y_axis = math.ceil(y_axis / 17) - 1
    print(str(y_axis))

    num = 0
    cb = None
    wg_num = 0
    for demand in game_stats.claimed_demands:
        if cb is None:
            if num == y_axis:
                break
            else:
                cb = demand[0]
                num += 1

            if num == y_axis:
                game_diplomacy.remove_pressed_demand(wg_num)
            else:
                wg_num += 1
                num += 1

        elif cb != demand[0]:
            if num == y_axis:
                break
            else:
                cb = demand[0]
                num += 1

            if num == y_axis:
                game_diplomacy.remove_pressed_demand(wg_num)
            else:
                wg_num += 1
                num += 1

        else:
            if num == y_axis:
                game_diplomacy.remove_pressed_demand(wg_num)
            else:
                wg_num += 1
                num += 1


def threaten_but():
    if not game_stats.dip_summary.ongoing_war:
        game_stats.diplomacy_area = "Threaten"
        game_diplomacy.prepare_threats()


def select_threat(position):
    # print("select_threat")
    y_axis = position[1]
    y_axis -= 338
    # print(str(y_axis))
    y_axis = math.ceil(y_axis / 17)
    # print(str(y_axis))

    if y_axis <= len(game_stats.casus_bellis):
        game_stats.cb_details = []
        game_diplomacy.threats_details_dict[game_stats.casus_bellis[y_axis - 1]]()


def select_threat_item(position):
    y_axis = position[1]
    y_axis -= 338
    # print(str(y_axis))
    y_axis = math.ceil(y_axis / 17)
    # print(str(y_axis))

    if y_axis <= len(game_stats.cb_details):
        game_diplomacy.add_threat_demand(game_stats.cb_details.pop(y_axis - 1))


def select_threat_demand(position):
    y_axis = position[1]
    y_axis -= 338
    # print(str(y_axis))
    y_axis = math.ceil(y_axis / 17) - 1
    # print(str(y_axis))

    num = 0
    threat = None
    wg_num = 0
    for demand in game_stats.war_goals:
        if threat is None:
            if num == y_axis:
                break
            else:
                threat = demand[2]
                num += 1

            if num == y_axis:
                print("select_threat_demand - 1")
                game_diplomacy.remove_threat_demand(wg_num)
            else:
                wg_num += 1
                num += 1

        elif threat != demand[2]:
            if num == y_axis:
                break
            else:
                threat = demand[2]
                num += 1

            if num == y_axis:
                print("select_threat_demand - 2")
                game_diplomacy.remove_threat_demand(wg_num)
            else:
                wg_num += 1
                num += 1

        else:
            if num == y_axis:
                print("select_threat_demand - 3")
                game_diplomacy.remove_threat_demand(wg_num)
            else:
                wg_num += 1
                num += 1


def send_threat_but():
    if game_stats.war_goals:
        game_diplomacy.send_threat()
        return_to_diplomatic_actions_area_but()


def close_war_panel_but():
    game_stats.game_board_panel = ""
    game_stats.war_inspection = None
    game_stats.realm_inspection = None
    game_stats.contact_inspection = None


def war_sue_for_peace_but():
    if game_stats.realm_inspection.name == game_stats.player_power \
            or game_stats.contact_inspection.name == game_stats.player_power:
        realm_name = None
        if game_stats.realm_inspection.name != game_stats.player_power:
            realm_name = str(game_stats.realm_inspection.name)
        else:
            realm_name = str(game_stats.contact_inspection.name)
        close_war_panel_but()
        diplomacy_but()

        for realm in game_obj.game_powers:
            if realm.name == realm_name:
                game_stats.contact_inspection = realm
                break

        # print("1. game_stats.dip_summary - " + str(game_stats.dip_summary))
        return_to_diplomatic_actions_area_but()
        # print("2. game_stats.dip_summary - " + str(game_stats.dip_summary))
        declare_war_or_sue_for_peace_action_but()


button_funs = {1: exit_but,
               2: save_but,
               3: next_turn_but,
               4: realm_but,
               5: quest_log_but,
               6: diplomacy_but,
               7: previous_war_notification_but,
               8: next_war_notification_but}

click_zone = {"begin battle panel": [380, 100, 900, 440],
              "settlement panel": [1, 80, 639, 540],
              "army exchange panel": [200, 380 + yVar, 639, 619 + yVar],
              "settlement blockade panel": [121, 70, 1159, 500],
              "quest log panel": [34, 80, 679, 540],
              "realm panel": [34, 80, 679, 540],
              "diplomacy panel": [34, 80, 679, 540],
              "war panel": [34, 80, 679, 540]}

right_click_zone = {"Building upgrade information": [642, 80, 1278, 540],
                    "Building information": [642, 80, 1278, 540],
                    "New regiment information": [642, 80, 1278, 540],
                    "New hero skill tree": [642, 80, 1278, 540],
                    "Hero window": [642, 80, 1278, 540]}

begin_battle_panel_funs = {1: play_battle_but,
                           2: autobattle_but}

building_upgrade_panel_funs = {1: close_right_panel_but}

building_panel_funs = {1: close_right_panel_but}

new_regiment_information_panel_funs = {1: close_right_panel_but}

new_hero_skill_tree_panel_funs = {1: close_right_panel_but,
                                  2: skill_tree_level_prev,
                                  3: skill_tree_level_next}

hero_window_panel_funs = {1: close_right_panel_but,
                          2: hero_information_window_skills_option,
                          3: hero_information_window_attributes_tree_option,
                          4: hero_information_window_inventory_option}

settlement_funs = {1: close_settlement_panel_but,
                   2: open_building_area,
                   3: open_recruiting_area,
                   4: open_heroes_area,
                   5: open_economy_area,
                   6: open_factions_area}

facility_lower_panel_funs = {}

settlement_lower_panel_funs = {1: select_stationed_army_but,
                               2: open_hero_information}

army_lower_panel_funs = {1: open_hero_information}

army_exchange_funs = {1: complete_army_exchange_but}

quest_log_funs = {1: close_quest_log_panel_but,
                  2: open_quest_messages_area,
                  3: open_diplomatic_messages_area}

realm_panel_funs = {1: close_realm_panel_but}

diplomacy_panel_funs = {1: close_diplomacy_panel_but,
                        2: previous_contact_but,
                        3: next_contact_but}

diplomacy_actions_funs = {1: declare_war_or_sue_for_peace_action_but,
                          2: threaten_but}

diplomacy_declaration_of_war_funs = {1: return_to_diplomatic_actions_area_but,
                                     2: declare_war_but}

diplomacy_sue_for_peace_funs = {1: return_to_diplomatic_actions_area_but,
                                2: draft_a_peace_offer_but}

diplomacy_draft_a_peace_offer_funs = {1: return_to_sue_for_peace_area_but,
                                      2: change_between_demands_and_concessions_but,
                                      3: propose_peace_offer_but}

diplomacy_threaten_funs = {1: return_to_diplomatic_actions_area_but,
                           2: send_threat_but}

war_panel_funs = {1: close_war_panel_but,
                  2: war_sue_for_peace_but}

settlement_blockade_panel_funs = {1: play_siege_but,
                                  2: autobattle_but,
                                  3: encircle_but,
                                  4: retreat_but,
                                  5: encircle_but}

settlement_blockade_panel_rb_funs = {1: build_trebuchet,
                                     2: cancel_building_trebuchet,
                                     3: build_siege_tower,
                                     4: cancel_building_siege_tower,
                                     5: build_battering_ram,
                                     6: cancel_building_battering_ram
                                     }

autobattle_conclusion_panel_funs = {1: close_autobattle_results}

settlement_building_funs = {1: plot_row_up,
                            2: plot_row_down}

settlement_recruitment_funs = {1: settlement_regiment_information,
                               2: hire_regiment}

settlement_heroes_funs = {1: new_hero_skill_tree,
                          2: hire_hero,
                          3: next_first_starting_skill,
                          4: next_second_starting_skill}

settlement_economy_funs = {1: open_overview_section,
                           2: open_population_section,
                           3: open_local_market_section,
                           4: open_trade_routes_section}

settlement_economy_population_funs = {1: up_pops_card_index,
                                      2: down_pops_card_index}

settlement_factions_funs = {1: up_faction_pops_index,
                            2: down_faction_pops_index}

panel_buttons = {"begin battle panel": begin_battle_panel_funs,
                 "settlement panel": settlement_funs,
                 "army exchange panel": army_exchange_funs,
                 "quest log panel": quest_log_funs,
                 "settlement blockade panel": settlement_blockade_panel_funs,
                 "realm panel": realm_panel_funs,
                 "diplomacy panel": diplomacy_panel_funs,
                 "war panel": war_panel_funs,
                 "autobattle conclusion panel": autobattle_conclusion_panel_funs}

panel_round_buttons = {"settlement blockade panel": settlement_blockade_panel_rb_funs}

panel_zone = {"begin battle panel": begin_battle_panel_zone,
              "settlement panel": settlement_panel_zone,
              "army exchange panel": army_exchange_panel_zone,
              "quest log panel": quest_log_panel_zone,
              "settlement blockade panel": settlement_blockade_panel_zone,
              "realm panel": realm_panel_zone,
              "diplomacy panel": diplomacy_panel_zone,
              "war panel": war_panel_zone,
              "autobattle conclusion panel": autobattle_conclusion_panel_zone}

panel_rb_zone = {"settlement blockade panel": settlement_blockade_panel_rb_zone}

right_panel_buttons = {"Building upgrade information": building_upgrade_panel_funs,
                       "Building information": building_panel_funs,
                       "New regiment information": new_regiment_information_panel_funs,
                       "New hero skill tree": new_hero_skill_tree_panel_funs,
                       "Hero window": hero_window_panel_funs}

right_panel_zone = {"Building upgrade information": building_upgrade_panel_zone,
                    "Building information": building_panel_zone,
                    "New regiment information": new_regiment_information_panel_zone,
                    "New hero skill tree": new_hero_skill_tree_panel_zone,
                    "Hero window": hero_window_panel_zone}

lower_panel_buttons = {"facility lower panel": facility_lower_panel_funs,
                       "settlement lower panel": settlement_lower_panel_funs,
                       "army lower panel": army_lower_panel_funs}

lower_panel_zone = {"facility lower panel": facility_lower_panel_zone,
                    "settlement lower panel": settlement_lower_panel_zone,
                    "army lower panel": army_lower_panel_zone}
