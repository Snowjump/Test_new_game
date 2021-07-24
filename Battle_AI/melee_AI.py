## Miracle battles!
import copy
import random

from Resources import game_obj


from Resources import game_obj
from Resources import game_stats
from Resources import game_battle
from Resources import algo_b_astar


def manage_melee(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee, enemy_ranged,
                 enemy_units):

    # Important, firstly, need to be sure, that regiment is using melee attack
    melee_attacks_list = []
    num = 0
    for s in acting_unit.attacks:
        if s.attack_type == "Melee":
            melee_attacks_list.append(num)
        num += 1

    b.attack_type_index = random.choice(melee_attacks_list)
    b.attack_type_in_use = acting_unit.attacks[b.attack_type_index].attack_type

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

            pos = direction_of_hit(chosen_enemy, old_position)

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

        for old_xy in b.movement_grid:
            for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0], [0, 0]]:
                new_xy = [old_xy[0] + xy[0], old_xy[1] + xy[1]]
                if 0 < new_xy[0] <= game_stats.battle_width:
                    if 0 < new_xy[1] <= game_stats.battle_height:
                        if new_xy not in enemy_positions:
                            TileNum = (new_xy[1] - 1) * game_stats.battle_width + new_xy[0] - 1
                            if b.battle_map[TileNum].army_id == enemy_army_id:
                                enemy_positions.append(new_xy)

        if len(enemy_positions) > 0:
            # Regiment has an enemy in his reach
            # For now let's choose enemy at random
            print("Charge enemy")

            chosen_enemy = random.choice(enemy_positions)
            print("chosen_enemy - " + str(chosen_enemy))

            # Next let's choose tile to approach at random too (for now)
            approach_tile = choose_approach(chosen_enemy, b)
            print("approach_tile - " + str(approach_tile))

            pos = direction_of_hit(chosen_enemy, approach_tile)

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

                # First step - gather list of enemy positions
                enemy_positions = []
                for unit in enemy_units:
                    if empty_space(b, unit) and len(unit.crew) > 0:
                        enemy_positions.append(unit.position)

                if len(enemy_units) > 0:
                    chosen_route = None
                    chosen_node = None
                    for enemy in enemy_positions:
                        node, a_path = algo_b_astar.b_astar(None, acting_unit.position, enemy, None, b)
                        if a_path is None:
                            print("No path for " + str(enemy))
                            enemy_positions.remove(enemy)

                        else:
                            a_path.pop(0)
                            a_path.pop(-1)
                            if chosen_route is None:
                                chosen_route = a_path
                                chosen_node = node
                                # print("New path - " + str(a_path))
                            elif len(chosen_route) > len(a_path):
                                chosen_route = a_path
                                chosen_node = node

                    print("New path - " + str(chosen_route))
                    print("Final node - " + str(chosen_node.position))
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


def direction_of_hit(chosen_enemy, old_position):

    if chosen_enemy[0] - old_position[0] == 1:
        if chosen_enemy[1] - old_position[1] == 1:
            # NW from target
            pos = [20, 20]
        elif chosen_enemy[1] - old_position[1] == 0:
            # W from target
            pos = [20, 50]
        elif chosen_enemy[1] - old_position[1] == -1:
            # SW from target
            pos = [20, 80]
    elif chosen_enemy[0] - old_position[0] == 0:
        if chosen_enemy[1] - old_position[1] == 1:
            # N from target
            pos = [50, 20]
        elif chosen_enemy[1] - old_position[1] == -1:
            # S from target
            pos = [50, 80]
    elif chosen_enemy[0] - old_position[0] == -1:
        if chosen_enemy[1] - old_position[1] == 1:
            # NE from target
            pos = [80, 20]
        elif chosen_enemy[1] - old_position[1] == 0:
            # E from target
            pos = [80, 50]
        elif chosen_enemy[1] - old_position[1] == -1:
            # SE from target
            pos = [80, 80]

    return pos


def choose_approach(chosen_enemy, b):
    tiles_for_approach = []
    for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
        new_xy = [chosen_enemy[0] + xy[0], chosen_enemy[1] + xy[1]]
        if new_xy in b.movement_grid:
            tiles_for_approach.append(new_xy)

    return random.choice(tiles_for_approach)


def empty_space(b, unit):
    for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
        new_xy = [unit.position[0] + xy[0], unit.position[1] + xy[1]]
        if 0 < new_xy[0] <= game_stats.battle_width:
            if 0 < new_xy[1] <= game_stats.battle_height:
                TileNum = (new_xy[1] - 1) * game_stats.battle_width + new_xy[0] - 1
                if b.battle_map[TileNum].army_id is None and b.battle_map[TileNum].obstacle is None:
                    # Empty space
                    return True

    return False
