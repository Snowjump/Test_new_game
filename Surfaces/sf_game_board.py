## Miracle battles


import math
import pygame
import random
import sys

from Content import building_drafts
from Resources import game_basic
from Resources import game_classes
from Resources import game_obj
from Resources import game_pathfinding
from Resources import game_stats
from Resources import level_save

yVar = game_stats.game_window_height - 800

button_zone = [[1150, 10, 1250, 32],
               [1040, 10, 1140, 32],
               [1005, 5, 1030, 54],
               [1150, 40, 1250, 62],
               [1040, 40, 1140, 62]]

begin_battle_panel_zone = [[590, 138, 690, 160],
                          [590, 168, 690, 190]]

mining_panel_zone = [[1044, 74, 1150, 96],
                     [1160, 74, 1240, 96],
                     [1044, 104, 1150, 126],
                     [1160, 104, 1240, 126]]

character_panel_zone = []

terrain_panel_zone = [[210, 754 + yVar, 310, 776 + yVar]]

building_panel_zone = [[210, 754 + yVar, 310, 776 + yVar]]  # placeholder

build_panel_zone = [[1044, 74, 1200, 96],
                    [1044, 164, 1265, 186]]


def game_board_keys(key_action):
    if key_action == 119:
        game_stats.pov_pos[1] -= 1
    elif key_action == 115:
        game_stats.pov_pos[1] += 1
    elif key_action == 97:
        game_stats.pov_pos[0] -= 1
    elif key_action == 100:
        game_stats.pov_pos[0] += 1

    elif key_action == 32:
        if game_stats.pause_status == False:
            game_stats.pause_status = True
            game_stats.passed_time = game_stats.passed_time + game_stats.temp_time_passed
        else:
            game_stats.pause_status = False
            game_stats.last_start = pygame.time.get_ticks()
        print("Pause is " + str(game_stats.pause_status))
        if game_stats.count_started == False:
            game_stats.count_started = True
            game_stats.start_time = pygame.time.get_ticks()

    elif key_action == 122:  # key - Z
        print("game_stats.show_time - " + str(game_stats.show_time))
        if game_stats.show_time:
            game_stats.show_time = False
        else:
            game_stats.show_time = True


def game_board_surface_m1(position):
    button_pressed = False
    ##    print("Success")

    button_numb = 0
    for square in button_zone:
        button_numb += 1
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_funs[button_numb]()
            button_pressed = True
            break

    # Panels' zone
    if game_stats.game_board_panel != "":
        p_funs = panel_buttons[game_stats.game_board_panel]
        p_button_zone = panel_zone[game_stats.game_board_panel]

        button_numb = 0
        for square in p_button_zone:
            button_numb += 1
            ##            print("Level editor panel button " + str(button_numb))
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                p_funs[button_numb]()
                button_pressed = True
                break

    # Window panel
    if game_stats.game_board_panel != "":
        square = click_zone[game_stats.game_board_panel]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_pressed = True

            if position[1] >= 194 and game_stats.game_board_panel == "information panel":
                game_stats.white_index = math.floor((position[1] - 194) / 50)
                print("Position in information panel - " + str(game_stats.white_index))

                # Index of selected tile in map list
                x2 = int(game_stats.selected_tile[0])
                y2 = int(game_stats.selected_tile[1])
                TileNum = (y2 - 1) * game_stats.cur_level_width + x2

                game_stats.pop_in_location = []
                for fac in game_obj.game_factions:
                    if fac.name == game_stats.location_factions[game_stats.faction_num]:
                        if len(fac.population) > 0:
                            for pop in fac.population:
                                if pop.location == TileNum:
                                    game_stats.pop_in_location.append(pop.personal_id)
                                    game_stats.details_panel_mode = "character"

    # Lower panel
    if game_stats.details_panel_mode != "":
        yVar = game_stats.game_window_height - 800

        print("game_stats.details_panel_mode - " + str(game_stats.details_panel_mode))
        lp_funs = lower_panel_buttons[game_stats.details_panel_mode]
        lp_button_zone = lower_panel_zone[game_stats.details_panel_mode]

        button_numb = 0

        for square in lp_button_zone:
            button_numb += 1

            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                lp_funs[button_numb]()
                button_pressed = True
                break

        square = [200, 600 + yVar, 1080, 800 + yVar]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_pressed = True

    # Click on game map
    if not button_pressed:
        game_stats.selected_tile = []

        x = math.ceil(position[0] / 48)
        y = math.ceil(position[1] / 48)
        x = int(x) + int(game_stats.pov_pos[0])
        y = int(y) + int(game_stats.pov_pos[1])
        print("Coordinates - x " + str(x) + " y " + str(y))
        game_stats.selected_tile = [int(x), int(y)]

        # Index of selected tile in map list
        x2 = int(game_stats.selected_tile[0])
        y2 = int(game_stats.selected_tile[1])
        TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1
        print("TileNum is " + str(TileNum))

        # game_stats.game_board_panel = ""

        if 0 < x2 <= game_stats.cur_level_width:
            if 0 < y2 <= game_stats.cur_level_height:

                # print("Army_id - " + str(game_obj.game_map[TileNum].army_id))

                if game_stats.selected_object == "":
                    if game_obj.game_map[TileNum].army_id is not None:
                        print("There is an army")
                        game_stats.selected_object = "Army"
                        game_stats.selected_army = int(game_obj.game_map[TileNum].army_id)

                # Movement command on map display
                elif game_stats.selected_object == "Army":
                    for army in game_obj.game_armies:
                        if army.army_id == game_stats.selected_army:
                            if army.owner == game_stats.player_power:
                                if len(army.route) > 0 and [x2, y2] == army.route[-1]:
                                    if army.action == "Stand":
                                        print('army.movement = "Move"')
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


def game_board_surface_m3(position):
    button_pressed = False
    print("game_board_surface_m3")
    # Next few steps make sure, that user didn't click on any buttons

    button_numb = 0
    for square in button_zone:
        button_numb += 1
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_pressed = True
            break

    # Lower panel
    if game_stats.details_panel_mode != "":
        yVar = game_stats.game_window_height - 800
        print("game_stats.details_panel_mode - " + str(game_stats.details_panel_mode))

        button_numb = 0

        square = [200, 600 + yVar, 1080, 800 + yVar]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_pressed = True

    # Click on game map
    if not button_pressed:
        game_stats.selected_tile = []

        x = math.ceil(position[0] / 48)
        y = math.ceil(position[1] / 48)
        x = int(x) + int(game_stats.pov_pos[0])
        y = int(y) + int(game_stats.pov_pos[1])
        print("Coordinates - x " + str(x) + " y " + str(y))
        game_stats.selected_tile = [int(x), int(y)]

        # Index of selected tile in map list
        x2 = int(game_stats.selected_tile[0])
        y2 = int(game_stats.selected_tile[1])
        TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1
        print("TileNum is " + str(TileNum))

        if game_stats.selected_object == "Army":
            game_stats.selected_object = ""
            game_stats.selected_army = -1


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


def play_battle_but():
    game_stats.game_board_panel = ""

    if game_stats.game_type == "singleplayer":
        game_stats.strategy_mode = False

    game_stats.current_screen = "Battle"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "battle_screen"

    # Create battle
    game_stats.battle_id_counter += 1

    # Preparing battle map
    new_battle_map = []
    for y in range(1, game_stats.battle_height + 1):
        for x in range(1, game_stats.battle_width + 1):
            new_battle_map.append(game_classes.Battle_Tile((x, y),
                                                           game_stats.battle_terrain,
                                                           game_stats.battle_conditions))
    # Adding obstacles on map
    grid_for_obstacle = []
    for y in range(1, game_stats.battle_height + 1):
        for x in range(3, game_stats.battle_width - 1):
            grid_for_obstacle.append([x, y])
    number_of_obstacles = 5
    while number_of_obstacles > 0:
        xy = grid_for_obstacle.pop(random.choice(range(0, len(grid_for_obstacle))))
        TileNum = (xy[1] - 1) * game_stats.battle_width + xy[0] - 1
        new_battle_map[TileNum].obstacle = game_classes.Battle_Map_Object("Oak", "Nature/Trees/", "Obstacle",
                                                                          [[1, 1], [36, 6], [68, 2],
                                                                           [15, 30], [43, 34], [62, 39],
                                                                           [6, 64], [40, 63], [70, 68]])
        number_of_obstacles -= 1

    starting_pov = [0, 0]
    cover_map = [3, 1, 16, 12]
    if game_stats.defender_army_id == game_stats.player_power:
        starting_pov = [6, 0]
        cover_map = [1, 1, 14, 12]

    attacking_positions = []
    for x in range(1, 3):
        for y in range(1, game_stats.battle_height + 1):
            attacking_positions.append([x, y])
            starting_attacking_positions = list(attacking_positions)
    defending_positions = []
    for x in range(game_stats.battle_width - 1, game_stats.battle_width + 1):
        for y in range(1, game_stats.battle_height + 1):
            defending_positions.append([x, y])
            starting_defending_positions = list(defending_positions)

    for army in game_obj.game_armies:
        if army.army_id == game_stats.attacker_army_id:
            unit_num = 0
            for unit in army.units:
                spot = list(random.choice(attacking_positions))
                attacking_positions.remove(spot)
                unit.position = list(spot)
                unit.direction = "E"  # E
                x2 = int(spot[0])
                y2 = int(spot[1])
                TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1
                new_battle_map[TileNum].unit_index = int(unit_num)
                new_battle_map[TileNum].army_id = int(game_stats.attacker_army_id)
                print("spot - " + str(spot) + " regiment - " + unit.name + " TileNum - " + str(TileNum))
                unit_num += 1
        elif army.army_id == game_stats.defender_army_id:
            unit_num = 0
            for unit in army.units:
                spot = list(random.choice(defending_positions))
                defending_positions.remove(spot)
                unit.position = list(spot)
                unit.direction = "W"  # W
                x2 = int(spot[0])
                y2 = int(spot[1])
                TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1
                new_battle_map[TileNum].unit_index = int(unit_num)
                new_battle_map[TileNum].army_id = int(game_stats.defender_army_id)
                print("spot - " + str(spot) + " regiment - " + unit.name + " TileNum - " + str(TileNum))
                unit_num += 1

    print("game_stats.battle_conditions " + game_stats.battle_conditions)
    game_obj.game_battles.append(game_classes.Land_Battle(game_stats.battle_id_counter,
                                                          game_stats.attacker_army_id,
                                                          game_stats.attacker_realm,
                                                          game_stats.defender_army_id,
                                                          game_stats.defender_realm,
                                                          game_stats.battle_terrain,
                                                          game_stats.battle_conditions,
                                                          new_battle_map,
                                                          starting_pov,
                                                          cover_map,
                                                          starting_attacking_positions,
                                                          starting_defending_positions))


def autobattle_but():
    pass


def tunels_but():
    game_stats.brush = "Tunels"


def remove_tunels_but():
    game_stats.brush = "Remove tunels"


def cave_but():
    game_stats.brush = "Cave"


def remove_cave_but():
    game_stats.brush = "Remove cave"


def cutting_but():
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.cur_level_width + x

    if game_obj.game_map[TileNum - 1].natural_feature is not None:
        if game_obj.game_map[TileNum - 1].natural_feature.name == "Mashroom garden":
            for fac in game_obj.game_factions:
                if fac.name == game_stats.player_faction:
                    # Make task to cut mashrooms repetetive
                    if [x, y] in fac.con_plans.cutting_plans:
                        fac.con_plans.cutting_plans.remove([x, y])
                        fac.con_plans.cutting_plans_inf.append([x, y])

                    # Remove task to cut mashrooms
                    elif [x, y] in fac.con_plans.cutting_plans_inf:
                        fac.con_plans.cutting_plans_inf.remove([x, y])
                        for task in game_obj.task_list:
                            if task.action == "Cut mashrooms" and task.position == [x,
                                                                                    y] and task.faction_name == fac.name:
                                # Search for character
                                for pop in fac.population:
                                    if pop.personal_id == task.performer:
                                        # Remove task from character's goals
                                        pop.goal = None
                                        pop.occupation = "not occupied"
                                # Remove task from task list
                                game_obj.task_list.remove(task)

                    # Add new task to cut mashrooms
                    else:
                        fac.con_plans.cutting_plans.append([x, y])
                        game_stats.task_id_counter += 1
                        another_task = game_classes.task_record("Cut mashrooms", [x, y], game_stats.player_faction,
                                                                game_stats.task_id_counter)
                        game_obj.task_list.append(another_task)
                        game_pathfinding.search_mashroom_cutting([x, y], game_stats.player_faction,
                                                                 game_stats.task_id_counter)


def next_turn_but():
    # Turn over hourglass icon
    game_stats.turn_hourglass = True

    for realm in game_obj.game_powers:
        if realm.name == game_stats.player_power:
            realm.turn_completed = True
            print(str(realm.name) + "'s turn is " + str(realm.turn_completed))


button_funs = {1: exit_but,
               2: save_but,
               3: next_turn_but}

click_zone = {"begin battle panel": [380, 100, 900, 400]}

begin_battle_panel_funs = {1: play_battle_but,
                           2: autobattle_but}

mining_panel_funs = {1: tunels_but,
                     2: remove_tunels_but,
                     3: cave_but,
                     4: remove_cave_but}


terrain_panel_funs = {1: cutting_but}

building_panel_funs = {1: cutting_but}  # placeholder

character_panel_funs = {}

panel_buttons = {"begin battle panel": begin_battle_panel_funs,
                 "mining panel": mining_panel_funs}

panel_zone = {"begin battle panel": begin_battle_panel_zone,
              "mining panel": mining_panel_zone,
              "build panel": build_panel_zone}

lower_panel_buttons = {"Terrain": terrain_panel_funs,
                       "character": character_panel_funs,
                       "Building": building_panel_funs}

lower_panel_zone = {"Terrain": terrain_panel_zone,
                    "character": character_panel_zone,
                    "Building": building_panel_zone}
