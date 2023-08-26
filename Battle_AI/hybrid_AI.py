## Miracle battles!
import math
import copy
import random


from Resources import game_obj
from Resources import game_stats
from Resources import game_battle
from Resources import algo_b_astar


def manage_hybrid(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee, enemy_ranged,
                  enemy_units):
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

        old_position = acting_unit.position
        enemy_nearby = []
        melee_enemy_nearby = False

        # Let's look at tiles surrounding this regiment, searching for enemies
        for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
            if 0 < old_position[0] + xy[0] <= game_stats.battle_width:
                if 0 < old_position[1] + xy[1] <= game_stats.battle_height:
                    new_position = [old_position[0] + xy[0], old_position[1] + xy[1]]
                    TileNum = (new_position[1] - 1) * game_stats.battle_width + new_position[0] - 1

                    if b.battle_map[TileNum].army_id == enemy_army_id:
                        enemy_nearby.append(new_position)

                        for army in game_obj.game_armies:
                            if army.army_id == enemy_army_id:
                                if "melee" in army.units[b.battle_map[TileNum].unit_index].reg_tags:
                                    melee_enemy_nearby = True
                                break

        if len(enemy_nearby) > 0:
            # Regiment has an enemy in nearby tile
            # If melee enemy is nearby, than this hybrid regiment should attack it
            # Let's choose enemy at random
            # And switch to melee attack
            melee_attacks_list = []
            num = 0
            for s in acting_unit.attacks:
                if s.attack_type == "Melee":
                    melee_attacks_list.append(num)
                num += 1

            b.attack_type_index = random.choice(melee_attacks_list)
            b.attack_type_in_use = acting_unit.attacks[b.attack_type_index].attack_type

            print("Hit nearby enemy")
            chosen_enemy = random.choice(enemy_nearby)

            pos = direction_of_hit(chosen_enemy, old_position)

            b.AI_ready = False
            game_battle.melee_attack_preparation(b, TileNum, pos, chosen_enemy[0], chosen_enemy[1])

        else:
            # Regiment can't move nowhere, however it's not surrounded by enemies
            # Regiment will use ranged attack
            target = find_shootings_targets(b, acting_unit, enemy_units)

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
        # Let's check if enemy stands nearby

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
            # Let's look for enemies without counterattack

            target_without_counterattack = None
            defence_strength = None
            e_index = None
            num = 0

            for e in enemy_units:
                if e.position in enemy_nearby:
                    if e.counterattack == 0:
                        target_without_counterattack = True
                        if defence_strength is None:
                            defence_strength = int(e.defence) + int(armor) + game_battle.defence_effect(e)
                            e_index = int(num)
                        elif int(e.defence) + int(armor) + game_battle.defence_effect(e) < defence_strength:
                            defence_strength = int(e.defence) + int(armor) + game_battle.defence_effect(e)
                            e_index = int(num)
                        else:
                            pass
                num += 1

            if target_without_counterattack:
                print("Opportunity to hit an enemy without counterattack")

                # And switch to melee attack
                melee_attacks_list = []
                num = 0
                for s in acting_unit.attacks:
                    if s.attack_type == "Melee":
                        melee_attacks_list.append(num)
                    num += 1

                b.attack_type_index = random.choice(melee_attacks_list)
                b.attack_type_in_use = acting_unit.attacks[b.attack_type_index].attack_type

                chosen_enemy = enemy_nearby[e_index]

                pos = direction_of_hit(chosen_enemy, old_position)

                b.AI_ready = False
                game_battle.melee_attack_preparation(b, TileNum, pos, chosen_enemy[0], chosen_enemy[1])
            else:
                print("No opportunity to hit an enemy without counterattack, therefore hybrid regiment shall "
                      "attack at random")
                # And switch to melee attack
                melee_attacks_list = []
                num = 0
                for s in acting_unit.attacks:
                    if s.attack_type == "Melee":
                        melee_attacks_list.append(num)
                    num += 1

                b.attack_type_index = random.choice(melee_attacks_list)
                b.attack_type_in_use = acting_unit.attacks[b.attack_type_index].attack_type

                print("Hit nearby enemy")
                chosen_enemy = random.choice(enemy_nearby)

                pos = direction_of_hit(chosen_enemy, old_position)

                b.AI_ready = False
                game_battle.melee_attack_preparation(b, TileNum, pos, chosen_enemy[0], chosen_enemy[1])

        else:
            # No enemy nearby
            # Let's find targets for ranged attack

            target = find_shootings_targets(b, acting_unit, enemy_units)

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
                closest_enemy = find_closest_enemy(b, enemy_units, acting_unit)

                if closest_enemy is not None:
                    # Search for suitable position to shoot
                    shooting_position = find_closest_position_to_shoot(b, closest_enemy)
                    if shooting_position is None:
                        print("Unit can't reach position in move where it can shoot enemy")
                        node, a_path = algo_b_astar.b_astar(None, acting_unit.position, closest_enemy, None, b)
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
                        print("Moving to shooting position")
                        b.move_destination = [int(shooting_position[0]), int(shooting_position[1])]
                        b.AI_ready = False
                        game_battle.action_order(b, "Move", None)
                else:
                    # Run out of options
                    print("Run out of options")
                    b.AI_ready = False
                    game_battle.action_order(b, "Wait", None)


        # b.AI_ready = False
        # game_battle.action_order(b, "Wait", None)


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


def find_shootings_targets(b, acting_unit, enemy_units):
    own_position = acting_unit.position
    closest_distance = None
    destination = None

    for e in enemy_units:
        if len(e.crew) > 0:
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
        else:
            pass
    return destination


def find_closest_enemy(b, enemy_units, acting_unit):
    enemy_position = None
    distance_to_enemy = None
    for e in enemy_units:
        if len(e.crew) > 0:
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
