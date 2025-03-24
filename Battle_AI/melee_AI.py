## Among Myth and Wonder
## melee_AI

import copy
import random


from Resources import game_obj
from Resources import game_stats
from Resources import game_battle
from Resources import algo_b_astar

from Content import movement_catalog


def manage_melee(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee, enemy_ranged,
                 enemy_units, acting_hero, enemy_hero):
    base_MP = game_battle.calculate_speed(acting_unit, acting_hero)

    mode = "March"
    for skill in acting_unit.skills:
        if skill.application == "Movement":
            if skill.quality == "Can fly":
                mode = "Flight"
                break

    # Important, firstly, need to be sure, that regiment is using melee attack
    # Seems unnecessary
    melee_attacks_list = []
    num = 0
    for s in acting_unit.attacks:
        if s.attack_type == "Melee":
            melee_attacks_list.append(num)
        num += 1

    b.attack_type_index = random.choice(melee_attacks_list)
    b.attack_type_in_use = acting_unit.attacks[b.attack_type_index].attack_type

    # mode = "March"
    # for skill in acting_unit.skills:
    #     if skill.application == "Movement":
    #         if skill.quality == "Can fly":
    #             mode = "Flight"
    #             break

    if len(b.movement_grid) == 0:
        print("Regiment has nowhere to go")

        old_position = acting_unit.position
        enemy_nearby = []

        # Let's look at tiles surrounding this regiment, searching for enemies
        for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
            if 0 < old_position[0] + xy[0] <= game_stats.battle_width:
                if 0 < old_position[1] + xy[1] <= game_stats.battle_height:
                    new_position = [old_position[0] + xy[0], old_position[1] + xy[1]]
                    TileNum = (new_position[1] - 1) * game_stats.battle_width + new_position[0] - 1

                    if b.battle_map[TileNum].army_id == enemy_army_id:
                        enemy_nearby.append(new_position)

        if len(enemy_nearby) > 0:
            # Regiment has an enemy in nearby tile
            # For now let's choose enemy at random

            chosen_enemy = random.choice(enemy_nearby)

            pos = game_battle.direction_of_hit(chosen_enemy, old_position)

            b.AI_ready = False
            game_battle.melee_attack_preparation(b, TileNum, pos, chosen_enemy[0], chosen_enemy[1])

        else:
            # Regiment can't move nowhere, however it's not surrounded by enemies
            # Regiment will defend itself
            b.AI_ready = False
            game_battle.action_order(b, "Defend", None)

    else:
        print("Let's look if enemies are within the reach of one turn moving")
        enemy_positions = []

        enemy_positions = find_nearby_enemies(b, enemy_army_id, enemy_positions)
        # for old_xy in b.movement_grid:
        #     for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0], [0, 0]]:
        #         new_xy = [old_xy[0] + xy[0], old_xy[1] + xy[1]]
        #         if 0 < new_xy[0] <= game_stats.battle_width:
        #             if 0 < new_xy[1] <= game_stats.battle_height:
        #                 if new_xy not in enemy_positions:
        #                     TileNum = (new_xy[1] - 1) * game_stats.battle_width + new_xy[0] - 1
        #                     if b.battle_map[TileNum].army_id == enemy_army_id:
        #                         enemy_positions.append(new_xy)

        if len(enemy_positions) > 0:
            # Regiment has an enemy in his reach
            # For now let's choose enemy at random
            print("Charge enemy")

            chosen_enemy = random.choice(enemy_positions)
            print("chosen_enemy - " + str(chosen_enemy))

            # Next let's choose tile to approach at random too (for now)
            approach_tile = choose_approach(chosen_enemy, b)
            print("approach_tile - " + str(approach_tile))

            pos = game_battle.direction_of_hit(chosen_enemy, approach_tile)
            TileNum = (chosen_enemy[1] - 1) * game_stats.battle_width + chosen_enemy[0] - 1

            b.AI_ready = False
            game_battle.melee_attack_preparation(b, TileNum, pos, chosen_enemy[0], chosen_enemy[1])

        else:
            # There is no enemy that regiment could reach in one move
            # First let's check how many ranged units have both sides

            if own_ranged > enemy_ranged:
                # Our side has advantage in number of ranged units
                # Therefore let them shoot enemies, while this melee regiment will defend itself
                print("Hold positions")
                b.AI_ready = False
                game_battle.action_order(b, "Defend", None)

            else:
                # Our side has disadvantage in number of ranged units
                # Melee regiment must be more proactive and move to find enemy
                print("Melee regiment moves toward enemy")

                # First step - gather list of enemy positions
                enemy_positions = []
                for unit in enemy_units:
                    if empty_space(b, unit) and len(unit.crew) > 0:
                        enemy_positions.append(unit.position)

                print("Enemy units - " + str(len(enemy_units)) + ": " + str(enemy_positions))

                if len(enemy_positions) > 0:
                    chosen_route = None
                    chosen_node = None
                    for enemy in enemy_positions:
                        print("Searching for path toward enemy at " + str(enemy))
                        node, a_path = algo_b_astar.b_astar(None, acting_unit.position, enemy, None, base_MP, b, mode)
                        if a_path is None:
                            print("No path for " + str(enemy))
                            # enemy_positions.remove(enemy)

                        else:
                            a_path.pop(0)
                            a_path.pop(-1)
                            if chosen_route is None:
                                chosen_route = a_path
                                chosen_node = node
                                print("New path toward enemy - " + str(enemy) + " is " + str(a_path))
                            elif len(chosen_route) > len(a_path):
                                chosen_route = a_path
                                chosen_node = node
                                print("Better path toward enemy - " + str(enemy) + " is " + str(a_path))

                    print("")
                    print("New path - " + str(chosen_route))
                    # if chosen_node is not None:
                    #     print("Final node - " + str(chosen_node.position))
                    #     b.AI_ready = False
                    #     game_battle.action_order(b, "Move", None)
                    if chosen_route is not None:
                        # b.path, b.movement_grid = [chosen_node], chosen_route
                        current = chosen_node
                        while current is not None:
                            # print("current.position - " + str(current.position))
                            if current.position in b.movement_grid:
                                b.path = [copy.deepcopy(current)]
                                b.move_destination = [int(current.position[0]), int(current.position[1])]
                                current = None
                            else:
                                # print("current.parent.position - " + str(current.parent.position))
                                current = current.parent

                        b.AI_ready = False
                        game_battle.action_order(b, "Move", None)
                    else:
                        b.AI_ready = False
                        game_battle.action_order(b, "Defend", None)

                else:
                    b.AI_ready = False
                    game_battle.action_order(b, "Defend", None)


def choose_approach(chosen_enemy, b):
    print("b.queue[0].position - " + str(b.queue[0].position))
    enemy_tile = (chosen_enemy[1] - 1) * game_stats.battle_width + chosen_enemy[0] - 1
    tiles_for_approach = []
    for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
        new_xy = [chosen_enemy[0] + xy[0], chosen_enemy[1] + xy[1]]
        ApproachTile = (new_xy[1] - 1) * game_stats.battle_width + new_xy[0] - 1

        permitted_attack = True

        if b.battle_map[enemy_tile].map_object is not None:
            if b.battle_map[enemy_tile].map_object.obj_type == "Structure":
                direction = simple_direction(new_xy, chosen_enemy)
                name = b.battle_map[enemy_tile].map_object.obj_name
                if direction in movement_catalog.block_movement_dict[name]:
                    if not b.battle_map[ApproachTile].siege_tower_deployed:
                        # Siege tower is not deployed there
                        permitted_attack = False

        if new_xy == b.queue[0].position:
            print("Standing still: new_xy - " + str(new_xy))
            if permitted_attack:
                tiles_for_approach.append(new_xy)
        elif new_xy in b.movement_grid:
            print("Looking to approach: new_xy - " + str(new_xy))
            if b.battle_map[ApproachTile].map_object is not None:
                if b.battle_map[ApproachTile].map_object.obj_type == "Structure":
                    for node in b.path:
                        if node.position == [new_xy[0], new_xy[1]]:
                            temp_pathway = []
                            current = node
                            while current is not None:
                                temp_pathway.append(current.position)
                                current = current.parent
                            temp_pathway = temp_pathway[::-1]
                            temp_pathway = temp_pathway[-2:]
                            approach_direction = simple_direction(temp_pathway[0],
                                                                  temp_pathway[1])
                            # print("From " + str(temp_pathway[0]) + " to " + str(temp_pathway[1]))
                            # print("Approach " + str(ApproachTile) + " from " + str(approach_direction))
                            name = b.battle_map[ApproachTile].map_object.obj_name
                            # print(name + " waste directions " + str(movement_catalog.waste_movement_dict[name]))
                            if approach_direction in movement_catalog.waste_movement_dict[name]:
                                permitted_attack = False
                            if approach_direction in movement_catalog.block_movement_dict[name]:
                                permitted_attack = False
                            break

            if permitted_attack:
                tiles_for_approach.append(new_xy)

    return random.choice(tiles_for_approach)


def empty_space(b, unit):
    for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
        new_xy = [unit.position[0] + xy[0], unit.position[1] + xy[1]]
        if 0 < new_xy[0] <= game_stats.battle_width:
            if 0 < new_xy[1] <= game_stats.battle_height:
                TileNum = (new_xy[1] - 1) * game_stats.battle_width + new_xy[0] - 1
                if b.battle_map[TileNum].army_id is None and b.battle_map[TileNum].map_object is None:
                    # Empty space
                    return True

    return False


def find_nearby_enemies(b, enemy_army_id, enemy_positions):
    # Enemies are within the reach of one turn moving
    ignore_targets = []

    # First step - add enemy targets that directly surround this regiment
    for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
        new_xy = [int(b.queue[0].position[0]) + xy[0], int(b.queue[0].position[1]) + xy[1]]
        if 0 < new_xy[0] <= game_stats.battle_width:
            if 0 < new_xy[1] <= game_stats.battle_height:
                TileNum = (new_xy[1] - 1) * game_stats.battle_width + new_xy[0] - 1
                OwnTileNum = (b.queue[0].position[1] - 1) * game_stats.battle_width + b.queue[0].position[0] - 1
                if b.battle_map[TileNum].army_id == enemy_army_id:
                    permitted_attack = True

                    # Check if attack blocked by a defensive structure like a wall
                    if b.battle_map[TileNum].map_object is not None:
                        if b.battle_map[TileNum].map_object.obj_type == "Structure":
                            direction = simple_direction(b.queue[0].position, new_xy)
                            name = b.battle_map[TileNum].map_object.obj_name
                            if direction in movement_catalog.block_movement_dict[name]:
                                if not b.battle_map[OwnTileNum].siege_tower_deployed:
                                    # Siege tower is not deployed there
                                    permitted_attack = False

                    if b.battle_map[OwnTileNum].map_object is not None:
                        if b.battle_map[OwnTileNum].map_object.obj_type == "Structure":
                            direction = simple_direction(new_xy, b.queue[0].position)
                            name = b.battle_map[OwnTileNum].map_object.obj_name
                            if direction in movement_catalog.block_movement_dict[name]:
                                if not b.battle_map[TileNum].siege_tower_deployed:
                                    # Siege tower is not deployed there
                                    permitted_attack = False

                    if permitted_attack:
                        enemy_positions.append(new_xy)

    print("First step - add enemy targets that directly surround this regiment:")
    print(str(enemy_positions))
    print("")

    # Second step - add enemy targets farther away
    for old_xy in b.movement_grid:
        for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0], [0, 0]]:
            new_xy = [int(old_xy[0]) + xy[0], int(old_xy[1]) + xy[1]]
            if 0 < new_xy[0] <= game_stats.battle_width:
                if 0 < new_xy[1] <= game_stats.battle_height:
                    if new_xy not in enemy_positions and new_xy not in ignore_targets:
                        TileNum = (new_xy[1] - 1) * game_stats.battle_width + new_xy[0] - 1
                        if b.battle_map[TileNum].army_id == enemy_army_id:
                            permitted_attack = False

                            # Check limitations imposed by structures
                            for xy2 in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0], [0, 0]]:
                                approach_xy = [new_xy[0] + xy2[0], new_xy[1] + xy2[1]]
                                if approach_xy in b.movement_grid:
                                    ApproachTile = (approach_xy[1] - 1) * game_stats.battle_width + approach_xy[0] - 1
                                    print("ApproachTile - " + str(ApproachTile) + "; approach_xy - " + str(approach_xy)
                                          + "; enemy at - " + str(new_xy))
                                    if b.battle_map[ApproachTile].map_object is not None:
                                        if b.battle_map[ApproachTile].map_object.obj_type == "Structure":
                                            for node in b.path:
                                                if node.position == [int(approach_xy[0]), int(approach_xy[1])]:
                                                    temp_pathway = []
                                                    current = node
                                                    while current is not None:
                                                        temp_pathway.append(current.position)
                                                        current = current.parent
                                                    temp_pathway = temp_pathway[::-1]
                                                    temp_pathway = temp_pathway[-2:]
                                                    approach_direction = simple_direction(temp_pathway[0],
                                                                                          temp_pathway[1])
                                                    name = b.battle_map[ApproachTile].map_object.obj_name
                                                    if approach_direction not in movement_catalog.waste_movement_dict[
                                                        name]:
                                                        permitted_attack = True

                                                    # Check if attack blocked by a defensive structure like a wall
                                                    # on a tile of approach
                                                    attack_direction = simple_direction(new_xy,
                                                                                        temp_pathway[1])
                                                    if attack_direction in movement_catalog.block_movement_dict[name]:
                                                        if not b.battle_map[TileNum].siege_tower_deployed:
                                                            # Siege tower is not deployed there
                                                            permitted_attack = False

                                                    break

                                    else:
                                        permitted_attack = True

                                    # Check if attack blocked by a defensive structure like a wall
                                    # on a tile where enemy regiment positioned
                                    if b.battle_map[TileNum].map_object is not None:
                                        if b.battle_map[TileNum].map_object.obj_type == "Structure":
                                            for node in b.path:
                                                if node.position == [int(approach_xy[0]), int(approach_xy[1])]:
                                                    temp_pathway = []
                                                    current = node
                                                    while current is not None:
                                                        temp_pathway.append(current.position)
                                                        current = current.parent
                                                    temp_pathway = temp_pathway[::-1]
                                                    attack_direction = simple_direction(temp_pathway[-1],
                                                                                        new_xy)
                                                    name = b.battle_map[TileNum].map_object.obj_name
                                                    if attack_direction in movement_catalog.block_movement_dict[name]:
                                                        if not b.battle_map[ApproachTile].siege_tower_deployed:
                                                            # Siege tower is not deployed there
                                                            permitted_attack = False

                                                    break

                            if permitted_attack:
                                enemy_positions.append(new_xy)
                            else:
                                ignore_targets.append(new_xy)

    print("Second step - add enemy targets farther away:")
    print(str(enemy_positions))
    print("")

    return enemy_positions


def simple_direction(start_pos, finish_pos):
    relative_position = None
    if start_pos[0] < finish_pos[0]:
        if start_pos[1] < finish_pos[1]:
            relative_position = "NW"
        elif start_pos[1] == finish_pos[1]:
            relative_position = "W"
        elif start_pos[1] > finish_pos[1]:
            relative_position = "SW"

    elif start_pos[0] == finish_pos[0]:
        if start_pos[1] < finish_pos[1]:
            relative_position = "N"
        elif start_pos[1] > finish_pos[1]:
            relative_position = "S"

    elif start_pos[0] > finish_pos[0]:
        if start_pos[1] < finish_pos[1]:
            relative_position = "NE"
        elif start_pos[1] == finish_pos[1]:
            relative_position = "E"
        elif start_pos[1] > finish_pos[1]:
            relative_position = "SE"

    return relative_position
