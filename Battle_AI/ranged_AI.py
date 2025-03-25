## Among Myth and Wonder
## ranged_AI

import copy
import random

from Battle_AI import common_search_funs
from Battle_AI import common_battle_funs

from Resources import game_stats
from Resources import game_battle
from Resources import algo_b_astar


def manage_ranged(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee, enemy_ranged,
                  enemy_units, acting_hero, enemy_hero):
    base_MP = game_battle.calculate_speed(acting_unit, acting_hero)

    mode = "March"
    for skill in acting_unit.skills:
        if skill.application == "Movement":
            if skill.quality == "Can fly":
                mode = "Flight"
                break

    # Important, firstly, need to be sure, that regiment is using ranged attack
    ranged_attacks_list = []
    num = 0
    for s in acting_unit.attacks:
        if s.attack_type == "Ranged":
            ranged_attacks_list.append(num)
        num += 1

    b.attack_type_index = random.choice(ranged_attacks_list)
    b.attack_type_in_use = acting_unit.attacks[b.attack_type_index].attack_type
    b.cur_effective_range = acting_unit.attacks[b.attack_type_index].effective_range
    b.cur_range_limit = acting_unit.attacks[b.attack_type_index].range_limit

    if len(b.movement_grid) == 0:
        print("Regiment has nowhere to go")
        # Let's look at tiles surrounding this regiment, searching for enemies
        old_position = acting_unit.position
        enemy_nearby = common_search_funs.surrounding_enemies(b, enemy_army_id, old_position)

        if enemy_nearby:
            # Regiment has an enemy in nearby tile
            # Let's look for enemies without counterattack
            targets_without_counterattack = []

            for e in enemy_units:
                if e.position in enemy_nearby:
                    if e.counterattack == 0:
                        targets_without_counterattack.append(e.position)

            if targets_without_counterattack:
                print("enemy_nearby :" + str(enemy_nearby))
                print("Opportunity to hit an enemy without counterattack")
                common_battle_funs.set_melee_attack(b, acting_unit, targets_without_counterattack, old_position)

            else:
                # Otherwise let's choose enemy at random
                print("Too dangerous to attack")
                b.AI_ready = False
                game_battle.action_order(b, "Defend", None)

        else:
            # Regiment can't move nowhere, however it's not surrounded by enemies
            # Regiment will use ranged attack
            target = common_search_funs.find_shootings_targets(b, acting_unit, enemy_units)

            if target is None:
                # There is no enemies in regiment's shooting range
                # Let's wait a little for better opportunity
                print("No target, wait")
                b.AI_ready = False
                game_battle.action_order(b, "Wait", None)
            else:
                TileNum = (target[1] - 1) * game_stats.battle_width + target[0] - 1
                b.AI_ready = False
                game_battle.ranged_attack_preparation(b, TileNum, target[0], target[1])
    else:
        # Let's look at tiles surrounding this regiment, searching for enemies
        old_position = acting_unit.position
        enemy_nearby = common_search_funs.surrounding_enemies(b, enemy_army_id, old_position)

        if enemy_nearby:
            # Regiment has an enemy in nearby tile
            # Let's look for enemies without counterattack
            targets_without_counterattack = []

            for e in enemy_units:
                if e.position in enemy_nearby:
                    if e.counterattack == 0:
                        targets_without_counterattack.append(e.position)

            if targets_without_counterattack:
                print("targets_without_counterattack: " + str(targets_without_counterattack))
                print("Opportunity to hit an enemy without counterattack")
                common_battle_funs.set_melee_attack(b, acting_unit, targets_without_counterattack, old_position)
            else:
                print("No opportunity to hit an enemy without counterattack, therefore regiment shall defend itself")
                b.AI_ready = False
                game_battle.action_order(b, "Defend", None)

        else:
            # No enemy nearby
            # Let's find targets for ranged attack

            target = common_search_funs.find_shootings_targets(b, acting_unit, enemy_units)

            if target is not None:
                TileNum = (target[1] - 1) * game_stats.battle_width + target[0] - 1
                b.AI_ready = False
                game_battle.ranged_attack_preparation(b, TileNum, target[0], target[1])
            # No target in range limit
            elif enemy_ranged == 0:
                # Since there is no enemy ranged units, than it's better wait for enemy to come closer
                print("Waiting for enemy to advance")
                b.AI_ready = False
                game_battle.action_order(b, "Wait", None)
            else:
                # Look for closest enemy
                closest_enemy = common_search_funs.find_closest_enemy(b, enemy_units, acting_unit)

                if closest_enemy is not None:
                    # Search for suitable position to shoot
                    shooting_position = common_search_funs.find_closest_position_to_shoot(b, closest_enemy)
                    if shooting_position is None:
                        print("Unit can't reach position in move where it can shoot enemy")
                        print("closest_enemy - " + str(closest_enemy))
                        node, a_path = algo_b_astar.b_astar(None, acting_unit.position, closest_enemy, None, base_MP, b, mode)
                        if a_path is not None:
                            # Trying to come closer toward enemy
                            a_path.pop(0)
                            a_path.pop(-1)
                            current = node
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
                            # Regiment is blocked off from reaching enemies, should wait instead
                            b.AI_ready = False
                            game_battle.action_order(b, "Wait", None)
                    else:
                        print("Moving to shooting position")
                        b.move_destination = [int(shooting_position[0]), int(shooting_position[1])]
                        b.AI_ready = False
                        game_battle.action_order(b, "Move", None)
                else:
                    # Run out of options
                    print("Run out of options")
                    b.AI_ready = False
                    game_battle.action_order(b, "Wait", None)
