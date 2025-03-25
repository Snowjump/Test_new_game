## Among Myth and Wonder
## melee_AI

import copy

from Battle_AI import common_search_funs
from Battle_AI import common_battle_funs

from Resources import game_battle
from Resources import algo_b_astar


def manage_melee(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee, enemy_ranged,
                 enemy_units, acting_hero, enemy_hero):
    base_MP = game_battle.calculate_speed(acting_unit, acting_hero)

    mode = "March"
    for skill in acting_unit.skills:
        if skill.application == "Movement":
            if skill.quality == "Can fly":
                mode = "Flight"
                break

    if len(b.movement_grid) == 0:
        print("Regiment has nowhere to go")
        old_position = acting_unit.position
        enemy_nearby = common_search_funs.surrounding_enemies(b, enemy_army_id, old_position)

        if enemy_nearby:
            # Regiment has an enemy in nearby tile
            # For now let's choose enemy at random
            common_battle_funs.set_melee_attack(b, acting_unit, enemy_nearby, old_position)

        else:
            # Regiment can't move nowhere, however it's not surrounded by enemies
            # Regiment will defend itself
            b.AI_ready = False
            game_battle.action_order(b, "Defend", None)

    else:
        print("Let's look if enemies are within the reach of one turn moving")
        enemy_positions = common_search_funs.find_nearby_enemies(b, enemy_army_id)

        if enemy_positions:
            # Regiment has an enemy in his reach
            # For now let's choose enemy at random
            print("Charge enemy")
            common_battle_funs.set_melee_attack(b, acting_unit, enemy_positions, acting_unit.position, True)

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
                    if common_search_funs.empty_space(b, unit) and len(unit.crew) > 0 and not unit.deserted:
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
