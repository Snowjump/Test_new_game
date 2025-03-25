## Among Myth and Wonder
## common_search_funs

import math
import random

from Resources import game_stats
from Resources import game_battle

from Content import movement_catalog


def find_shootings_targets(b, acting_unit, enemy_units):
    own_position = acting_unit.position
    closest_distance = None
    destination = None

    for e in enemy_units:
        if not e.deserted:
            print(e.name + " position " + str(e.position) + " has deserted - " + str(e.deserted))
            distance = (math.sqrt(((e.position[0] - own_position[0]) ** 2) + (
                    (e.position[1] - own_position[1]) ** 2)))

            if distance > b.cur_range_limit:
                # Too far to hit
                pass

            else:
                # Target unit could be hit
                if closest_distance is None:
                    closest_distance = float(distance)
                    destination = [int(e.position[0]), int(e.position[1])]
                elif distance < closest_distance:
                    # Found target closer to shooting regiment
                    closest_distance = float(distance)
                    destination = [int(e.position[0]), int(e.position[1])]
                else:
                    pass

    return destination


def find_closest_enemy(b, enemy_units, acting_unit):
    enemy_position = None
    distance_to_enemy = None
    for e in enemy_units:
        if not e.deserted:
            distance = (math.sqrt(((e.position[0] - acting_unit.position[0]) ** 2) + (
                    (e.position[1] - acting_unit.position[1]) ** 2)))

            if distance_to_enemy is None:
                enemy_position = list(e.position)
                distance_to_enemy = float(distance)

            elif distance < distance_to_enemy:
                enemy_position = list(e.position)
                distance_to_enemy = float(distance)

    return enemy_position


def find_closest_position_to_shoot(b, closest_enemy):
    shooting_distance = None
    optimal_position = None
    for xy in b.movement_grid:
        distance = (math.sqrt(((closest_enemy[0] - xy[0]) ** 2) + (
                (closest_enemy[1] - xy[1]) ** 2)))

        if distance < b.cur_range_limit:
            if shooting_distance is None:
                shooting_distance = float(distance)
                optimal_position = list(xy)
            elif distance > shooting_distance:
                shooting_distance = float(distance)
                optimal_position = list(xy)
            else:
                pass
    return optimal_position


def find_nearby_enemies(b, enemy_army_id):
    # Enemies are within the reach of one turn moving
    ignore_targets = []
    enemy_positions = surrounding_enemies(b, enemy_army_id, b.queue[0].position)
    # First step - add enemy targets that directly surround this regiment

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
                                                    approach_direction = game_battle.change_direction(temp_pathway[0],
                                                                                                      temp_pathway[1])
                                                    name = b.battle_map[ApproachTile].map_object.obj_name
                                                    if approach_direction not in movement_catalog.waste_movement_dict[
                                                        name]:
                                                        permitted_attack = True

                                                    # Check if attack blocked by a defensive structure like a wall
                                                    # on a tile of approach
                                                    attack_direction = game_battle.change_direction(new_xy,
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
                                                    attack_direction = game_battle.change_direction(temp_pathway[-1],
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


def surrounding_enemies(b, enemy_army_id, unit_position):
    enemy_positions = []
    for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
        new_xy = [unit_position[0] + xy[0], unit_position[1] + xy[1]]
        if 0 < new_xy[0] <= game_stats.battle_width:
            if 0 < new_xy[1] <= game_stats.battle_height:
                TileNum = (new_xy[1] - 1) * game_stats.battle_width + new_xy[0] - 1
                OwnTileNum = (b.queue[0].position[1] - 1) * game_stats.battle_width + b.queue[0].position[0] - 1
                if b.battle_map[TileNum].army_id == enemy_army_id:
                    permitted_attack = True

                    # Check if attack blocked by a defensive structure like a wall
                    if b.battle_map[TileNum].map_object is not None:
                        if b.battle_map[TileNum].map_object.obj_type == "Structure":
                            direction = game_battle.change_direction(b.queue[0].position, new_xy)
                            name = b.battle_map[TileNum].map_object.obj_name
                            if direction in movement_catalog.block_movement_dict[name]:
                                if not b.battle_map[OwnTileNum].siege_tower_deployed:
                                    # Siege tower is not deployed there
                                    permitted_attack = False

                    if b.battle_map[OwnTileNum].map_object is not None:
                        if b.battle_map[OwnTileNum].map_object.obj_type == "Structure":
                            direction = game_battle.change_direction(new_xy, b.queue[0].position)
                            name = b.battle_map[OwnTileNum].map_object.obj_name
                            if direction in movement_catalog.block_movement_dict[name]:
                                if not b.battle_map[TileNum].siege_tower_deployed:
                                    # Siege tower is not deployed there
                                    permitted_attack = False

                    if permitted_attack:
                        enemy_positions.append(new_xy)

    return enemy_positions


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
                direction = game_battle.change_direction(new_xy, chosen_enemy)
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
                            approach_direction = game_battle.change_direction(temp_pathway[0],
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
