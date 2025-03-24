## Among Myth and Wonder
## game_battle

import copy
import math
import random
import pygame.math

from Resources import game_classes
from Resources import game_obj
from Resources import game_stats
from Resources import algo_b_movement_range
from Resources import algo_b_astar
from Battle_AI import battle_logic
from Resources import battle_skills
from Resources import update_gf_battle
from Resources import common_selects
from Resources import common_lists

from Resources.Game_Battle import execute_order_funs
from Resources.Game_Battle import hit_funs

from Resources.Game_Regiment import regiment_classes

from Content import movement_catalog
from Content import siege_warfare_catalog


# Battle queue keeps record in what order will act regiments, heroes and effects
def form_queue(b):  # b - stands for Battle
    print("")
    print("form_queue()")
    blank = []

    for army in game_obj.game_armies:
        if army.army_id in [b.attacker_id, b.defender_id]:
            a = army
            first_color = None
            second_color = None
            if a.owner != "Neutral":
                power = common_selects.select_realm_by_name(a.owner)
                first_color = str(power.f_color)
                second_color = str(power.s_color)

            index = 0
            for unit in a.units:
                print(unit.name + " unit.position - " + str(unit.position))
                blank.append([a.army_id, a.owner, index, unit.position, unit.img_source, unit.img, first_color,
                              second_color, unit.x_offset, unit.y_offset, unit.crew[0].img_width,
                              unit.crew[0].img_height, "Regiment"])
                index += 1

            if a.hero:
                print("Add " + str(a.hero.name) + " to queue")
                blank.append([a.army_id, a.owner, None, None, a.hero.img_source, a.hero.img, first_color,
                              second_color, a.hero.x_offset, a.hero.y_offset, 0, 0, "Hero"])

    random.shuffle(blank)

    for item in blank:
        b.queue.append(game_classes.Queue_Card(0.0, item[12], item[0], item[1], item[2], item[3], item[4],
                                               item[5], item[6], item[7], item[8], item[9], item[10], item[11], ""))

    print("Queue length is " + str(len(b.queue)))


# Check next queue card and prepare battle state
def advance_queue(b):  # b - stands for Battle
    print("")
    print("advance_queue(b)")
    list_of_effect_cards = []
    index = 0
    for q_card in b.queue:
        if q_card.obj_type == "Regiment" or q_card.obj_type == "Hero":
            break
        else:
            print(str(index) + ") " + str(q_card.title))
            list_of_effect_cards.append(int(index))
            index += 1

    if len(list_of_effect_cards) > 0:
        list_of_effect_cards = sorted(list_of_effect_cards, reverse=True)
        index_list = []
        for element in list_of_effect_cards:
            army = common_selects.select_army_by_id(b.queue[element].army_id)
            for effect in army.units[b.queue[element].number].effects:
                if effect.name == b.queue[element].title:
                    army.units[b.queue[element].number].effects.remove(effect)
            index_list.append(element)

        common_lists.reversed_list_cleaning(b.queue, index_list)

    # Resetting
    b.attacking_rotate = []
    b.defending_rotate = []
    b.ready_to_act = False
    b.ability_targets = []
    b.total_targets = 0
    b.ability_mana_cost = 0
    b.initiative_cost = 0

    b.realm_in_control = str(b.queue[0].owner)

    if b.realm_in_control == b.attacker_realm:
        b.enemy = b.defender_realm
    else:
        b.enemy = b.attacker_realm

    print("b.realm_in_control - " + str(b.realm_in_control) + " b.attacker_realm - " + str(b.attacker_realm) +
          " b.defender_realm - " + str(b.defender_realm) + " b.enemy - " + str(b.enemy))

    if b.attacker_id == b.queue[0].army_id:
        b.enemy_army_id = b.defender_id
    else:
        b.enemy_army_id = b.attacker_id

    if b.realm_in_control == game_stats.player_power:
        b.ready_to_act = True
    else:
        b.AI_ready = True

    if b.queue[0].obj_type != "Hero":
        print(str(b.queue[0].owner) + " " + str(b.queue[0].obj_type) + " " + str(b.queue[0].number) + " "
              + str(b.queue[0].position))
        # Move screen
        x = int(b.queue[0].position[0])
        y = int(b.queue[0].position[1])
        x -= int(b.battle_pov[0])
        y -= int(b.battle_pov[1])

        if 0 < x <= 14 and 0 < y <= 8:
            pass
        else:
            if x <= 0:
                b.battle_pov[0] -= int(b.battle_pov[0] - b.queue[0].position[0] + 2)
            elif x > 14:
                b.battle_pov[0] += int(b.queue[0].position[0] - 16 + 5)
            if y <= 0:
                b.battle_pov[1] -= int(b.battle_pov[1] - b.queue[0].position[1] + 3)
            elif y > 7:
                b.battle_pov[1] += int(b.queue[0].position[1] - 7 + 1)

    else:
        battle_ending(b)

    b.movement_grid = []
    if b.queue[0].obj_type == "Regiment":
        army = common_selects.select_army_by_id(b.queue[0].army_id)
        morale_restoration_bonus = 0.0
        if army.hero:
            for skill in army.hero.skills:
                for effect in skill.effects:
                    if effect.application == "Bonus morale restoration":
                        if effect.method == "addition":
                            morale_restoration_bonus += float(effect.quantity)
        unit = army.units[b.queue[0].number]
        print("Regiment - " + unit.name + "; " + str(unit.position))

        b.attack_type_index = 0
        list_of_attacks = []
        for attack in unit.attacks:
            list_of_attacks.append(str(attack.attack_type))
        if "Abilities" in list_of_attacks:
            b.attack_type_index = int(list_of_attacks.index("Abilities"))
        elif "Ranged" in list_of_attacks:
            b.attack_type_index = int(list_of_attacks.index("Ranged"))
        b.attack_type_in_use = unit.attacks[b.attack_type_index].attack_type
        b.attack_name = unit.attacks[b.attack_type_index].name
        b.cur_effective_range = unit.attacks[b.attack_type_index].effective_range
        # b.cur_range_limit = unit.attacks[b.attack_type_index].range_limit
        b.cur_range_limit = attack_range_effect(army, unit, unit.attacks[b.attack_type_index].range_limit)

        # Reset engage status
        unit.engaged = False

        # Reset counterattack counter
        unit.counterattack = 1
        if army.hero:
            for skill in army.hero.skills:
                for effect in skill.effects:
                    if effect.application == "Bonus counterattack":
                        if effect.method == "addition":
                            unit.counterattack += effect.quantity

        # Restore some morale
        unit.simple_change_morale(game_stats.battle_morale_base_restoration + morale_restoration_bonus)

        # Check duration of effects
        num_list = []
        num = 0
        for e in unit.effects:
            if e.until_next_turn:
                print(str(e.name) + " effect has ended")
                num_list.append(num)
                # unit.effects.remove(e)
            num += 1

        # common_lists
        if num_list:
            num_list = sorted(num_list, reverse=True)
            for index in num_list:
                del unit.effects[index]

        # Movement path
        # MP = unit.speed
        # acting_hero = None
        # for army in game_obj.game_armies:
        #     if army.army_id == b.queue[0].army_id:
        acting_hero = army.hero

        mode = "March"
        for skill in unit.skills:
            if skill.application == "Movement":
                if skill.quality == "Can fly":
                    mode = "Flight"
                    break

        MP = calculate_speed(unit, acting_hero)
        start = b.queue[0].position

        b.path, b.movement_grid = algo_b_movement_range.pseudo_astar(None, start, MP, b, mode)

        # Check if unit should route due to low morale
        if unit.morale <= 0.0:
            print("advance_queue() -> routing_path()")
            # b.primary = "Move"
            b.secondary = "Route"
            routing_path(b, unit, acting_hero)


def complete_turn(b, add_time):
    print("complete_turn")
    # b.queue[0].time_act += add_time
    # print("time_act - " + str(b.queue[0].time_act) + ", add_time - " + str(add_time))
    new_time = float(b.queue[0].time_act + add_time)
    new_index = len(b.queue)
    index = 0
    for card in b.queue:

        if new_time < card.time_act and new_index > index:
            new_index = int(index)

        # print("new_time " + str(new_time) + " card.time_act " + str(card.time_act) + " new_index " + str(new_index))
        index += 1

    # print("army_id - " + str(b.queue[0].army_id) + " owner - " + str(b.queue[0].owner) + " number - "
    #       + str(b.queue[0].number))
    # print("b.queue[0].time_act - " + str(b.queue[0].time_act) + " + add_time - " + str(add_time) + " = new_time - "
    #       + str(new_time))
    b.queue[0].time_act = float(new_time)
    # print("updated b.queue[0].time_act - " + str(b.queue[0].time_act) + " new_index - " + str(new_index - 1))
    b.queue.insert(new_index - 1, b.queue.pop(0))

    b.path = None
    b.movement_grid = None
    b.positions_list = []
    advance_queue(b)


def action_order(b, first_action, second_action):
    b.cursor_function = None  # Important in case player choose to execute an ability, but instead gave other order
    b.primary = first_action
    b.secondary = second_action
    print("game_battle .. action_order()")
    print("First action - " + str(b.primary) + ", secondary action - " + str(b.secondary))

    if first_action == "Move":
        remove_aura_effects(b.queue[0].position, b)
        # print("length of b.path - " + str(len(b.path)))
        # print("b.move_destination - " + str(b.move_destination))
        # print("b.target_destination - " + str(b.target_destination))
        for node in b.path:
            # print("node position - " + str(node.position))
            if node.position == b.move_destination:
                # print("node.position - " + str(node.position) + " and b.move_destination - " + str(b.move_destination))
                pathway = []
                current = node
                while current is not None:
                    pathway.append(current.position)
                    current = current.parent
                # print("Final unreversed path is " + str(pathway))
                b.tile_trail = list(pathway[::-1])
                b.tile_trail = b.tile_trail[1:]
                print("Final reversed path is " + str(b.tile_trail))

        # b.move_destination = None
        b.movement_grid = None
        b.path = None

        prepare_takeoff(b)  # For flyers

        # Disengaging surrounding units
        disengage(b, b.queue[0].position)
        print("")


def execute_order(b):
    print("execute_order()")
    print("b.primary - " + str(b.primary) + "; b.secondary - " + str(b.secondary))
    acting_unit = None
    acting_army = common_selects.select_army_by_id(b.queue[0].army_id)
    acting_hero = acting_army.hero
    enemy_army = None
    enemy_hero = None
    if b.enemy_army_id:
        enemy_army = common_selects.select_army_by_id(b.enemy_army_id)
        enemy_hero = enemy_army.hero
    # print("b.enemy_army_id - " + str(b.enemy_army_id))
    # print("Execution for " + str(b.queue[0].obj_type))
    if b.queue[0].obj_type != "Hero":
        acting_unit = acting_army.units[b.queue[0].number]
        print(str(b.queue[0].position) + " " + acting_unit.name + " - not a hero")
        if b.primary in ["Rotate", "Move", "Route"]:
            if b.tile_trail:
                change_side_direction(acting_unit, b, acting_army, enemy_army)
            elif b.secondary == "Route":
                print("Nowhere to go - " + str(b.secondary))
                b.primary = "Wait"
                b.secondary = None

    if b.primary == "Move":
        execute_order_funs.primary_move(b, acting_unit, acting_army, enemy_army)

    elif b.primary == "Wait":
        execute_order_funs.primary_wait(b, acting_unit)
    elif b.primary == "Wait message":
        execute_order_funs.primary_wait_message(b)
    elif b.primary == "Wait message1":
        execute_order_funs.primary_wait_message1(b)

    elif b.primary == "Defend":
        execute_order_funs.primary_defend(b, acting_unit, acting_hero)
    elif b.primary == "Defend message":
        execute_order_funs.primary_defend_message(b)
    elif b.primary == "Defend message1":
        execute_order_funs.primary_defend_message1(b)

    elif b.primary == "Pass":
        execute_order_funs.primary_pass(b)
    elif b.primary == "Pass1":
        execute_order_funs.primary_pass1(b, acting_army, acting_hero)

    elif b.primary == "Rotate":
        execute_order_funs.primary_rotate(b, acting_army, acting_unit, enemy_army)

    elif b.primary == "Melee attack":
        execute_order_funs.primary_melee_attack(b, acting_hero, acting_unit, enemy_hero, enemy_army)

    elif b.primary == "Hit from above":
        execute_order_funs.primary_hit_from_above(b, acting_hero, acting_unit, enemy_army, enemy_hero)

    elif b.primary == "Break the gates":
        execute_order_funs.primary_break_the_gates(b)
    elif b.primary == "Dock the wall":
        execute_order_funs.primary_dock_the_wall(b)

    elif b.primary == "Damage message":
        execute_order_funs.primary_damage_message(b)
    elif b.primary == "Damage message1":
        execute_order_funs.primary_damage_message1(b, acting_army, acting_unit, enemy_army)

    elif b.primary == "Counterattack":
        execute_order_funs.primary_counterattack(b, acting_army, acting_hero, enemy_army, enemy_hero)
    elif b.primary == "Counterattack damage message":
        execute_order_funs.primary_counterattack_damage_message(b)
    elif b.primary == "Counterattack damage message1":
        execute_order_funs.primary_counterattack_damage_message1(b)

    elif b.primary == "Ranged attack":
        execute_order_funs.primary_ranged_attack(b, acting_hero, acting_unit, enemy_army, enemy_hero)


def change_direction(position1, position2):
    # In what direction the regiment turned to
    new_direction = ""
    if position1[0] == position2[0]:
        if position1[1] > position2[1]:
            new_direction = "N"
        elif position1[1] < position2[1]:
            new_direction = "S"
    elif position1[0] > position2[0]:
        if position1[1] > position2[1]:
            new_direction = "NW"
        elif position1[1] < position2[1]:
            new_direction = "SW"
        elif position1[1] == position2[1]:
            new_direction = "W"
    elif position1[0] < position2[0]:
        if position1[1] > position2[1]:
            new_direction = "NE"
        elif position1[1] < position2[1]:
            new_direction = "SE"
        elif position1[1] == position2[1]:
            new_direction = "E"

    return new_direction


def attack_angle(unit_at, unit_df):
    dir_code = {"NE": 1,
                "E": 2,
                "SE": 3,
                "S": 4,
                "SW": 5,
                "W": 6,
                "NW": 7,
                "N": 8}

    attacker = dir_code[unit_at]
    defender = dir_code[unit_df]

    step1 = (int(attacker) + 4) % 8
    step2 = int(defender) - step1
    step3 = 8 - step2
    step4 = step3 % 8

    if step4 == 0:
        step4 = 8

    angle_code = {1: "Front right",
                  2: "Right flank",
                  3: "Rear right",
                  4: "Rear",
                  5: "Rear left",
                  6: "Left flank",
                  7: "Front left",
                  8: "Front"}

    direction_angle = angle_code[step4]
    print("Directions: unit_at - " + str(unit_at) + ", unit_df - " + str(unit_df))
    print("attacker - " + str(attacker) + ", defender - " + str(defender))
    print("step1 - " + str(step1) + ", step2 - " + str(step2) + ", step3 - " + str(step3) + ", step4 - " + str(step4))
    print("attack_angle - " + str(direction_angle))

    return direction_angle


def form_list_of_attackers(b, unit):
    if b.primary == "Melee attack" or b.primary == "Counterattack":
        index_list = []
        index_count = 0
        while index_count <= len(unit.crew) - 1 and index_count <= unit.number - 1:
            index_list.append(index_count)
            index_count += 1

        # print("index_list - " + str(index_list))
        return index_list

    elif b.primary == "Hit from above":
        index_list = []
        index_count = 0
        # All creatures strike in attack from above
        while index_count <= len(unit.crew) - 1:
            index_list.append(index_count)
            index_count += 1

            # print("index_list - " + str(index_list))
        return index_list


def complete_melee_attack(b, unit, primary_target, angle, acting_hero, enemy_hero):
    print("complete_melee_attack(): " + unit.name + " hitting " + primary_target.name)
    # Total HP among all creatures in targeted regiment
    # Needed to calculate morale hit
    before_HP = 0
    for creature in primary_target.crew:
        before_HP += creature.HP

    # Reset damage counter
    b.dealt_damage = 0
    b.killed_creatures = 0

    # Check attack type parameters
    target_option = "Single target"
    for tag in unit.attacks[b.attack_type_index].tags:
        if tag in ["Dragon breath", "Drake breath"]:
            target_option = str(tag)
        elif b.attack_name == "Hit and fly":
            target_option = "Random target"

    for at_creature in b.perform_attack:
        if len(primary_target.crew) > 0:
            if target_option == "Single target":
                target = choose_melee_target(b, at_creature, primary_target, angle, b.perform_attack)
                hit_funs.melee_hit(b, at_creature, unit, primary_target, target, acting_hero, enemy_hero)

            elif target_option in ["Dragon breath", "Drake breath"]:
                # Maximum 5 attacks for "Dragon breath"
                # Maximum 2 attacks for "Drake breath"
                limit_dic = {"Dragon breath": 5,
                             "Drake breath": 2}
                attacks = []
                limit = limit_dic[target_option]
                print(target_option + ": limit - " + str(limit))

                if len(primary_target.crew) < limit:
                    limit = int(len(primary_target.crew))
                for attack_index in range(limit):
                    attacks.append(attack_index)

                for attack_index in attacks:
                    target = choose_melee_target(b, attack_index, primary_target, angle, attacks)
                    hit_funs.melee_hit(b, at_creature, unit, primary_target, target, acting_hero, enemy_hero)

            elif target_option == "Random target":
                # Angle doesn't matter since attacking regiment is striking from above
                # Target chosen at random
                target = random.randint(0, len(primary_target.crew) - 1)
                hit_funs.melee_hit(b, at_creature, unit, primary_target, target, acting_hero, enemy_hero)

    # if b.attack_name != "Hit and fly":
    #     print("complete_melee_attack(): b.attack_name - " + str(b.attack_name))
    battle_skills.charge_track(unit, primary_target, b.queue)

    # Reduce morale
    primary_target.reduce_morale(b, before_HP, angle)

    # Set initiative after performed action
    if b.primary != "Counterattack":
        set_initiative(unit, acting_hero, "Melee")

    b.damage_dealt_positions.append(tuple(primary_target.position))
    print("b.damage_dealt_positions: " + str(b.damage_dealt_positions))

    check_if_no_one_left_alive(b)

    b.anim_message.append(game_classes.Battle_Message(["Damage " + str(b.dealt_damage),
                                                       "Killed " + str(b.killed_creatures)],
                                                      "Regiment",
                                                      (primary_target.position[0], primary_target.position[1])))


def choose_melee_target(b, at_creature, primary_target, angle, perform_attack):
    enemy_list = []  # List of creature indexes

    if angle == "Front":
        # How many enemies this creature face
        if len(primary_target.crew) < primary_target.number:
            limit = len(primary_target.crew)
        else:
            limit = primary_target.number
        for i in range(0, limit):
            enemy_list.append(i)

        # print("enemy_list - " + str(enemy_list))
        target = enemy_list[math.ceil((len(enemy_list) / len(perform_attack) * (at_creature + 1)) * -1)]
        # print("target - " + str(target) + " for creature - " + str(at_creature))
        return target
    elif angle == "Rear":
        if len(primary_target.crew) % primary_target.number == 0:
            rows_left = int(len(primary_target.crew) / primary_target.number)
            for i in range((rows_left - 1) * primary_target.number, rows_left * primary_target.number):
                enemy_list.append(i)

        else:
            full_rows_left = int(len(primary_target.crew) / primary_target.number)
            for i in range(full_rows_left * primary_target.number, len(primary_target.crew)):
                enemy_list.append(i)

            if full_rows_left > 0:
                for i in range(len(primary_target.crew) - primary_target.number,
                               full_rows_left * primary_target.number - 1):
                    enemy_list.append(i)

        print("enemy_list - " + str(enemy_list) + " from crew - " + str(len(primary_target.crew)))
        target = enemy_list[math.ceil(len(enemy_list) / len(perform_attack) * (at_creature + 1)) - 1]
        print("target - " + str(target) + " for creature - " + str(at_creature))
        return target

    elif angle == "Left flank":
        rows_left = math.ceil(len(primary_target.crew) / primary_target.number)
        for i in range(0, rows_left):
            enemy_list.append(i * primary_target.number)

        # print("enemy_list - " + str(enemy_list))
        target = enemy_list[math.ceil(len(enemy_list) / len(perform_attack) * (at_creature + 1)) - 1]
        # print("target - " + str(target) + " for creature - " + str(at_creature))
        return target

    elif angle == "Right flank":
        if len(primary_target.crew) % primary_target.number == 0:
            rows_left = int(len(primary_target.crew) / primary_target.number)
            for i in range(0, rows_left):
                enemy_list.append(i * primary_target.number + primary_target.number - 1)

        else:
            full_rows_left = int(len(primary_target.crew) / primary_target.number)
            for i in range(full_rows_left - 1, full_rows_left):
                enemy_list.append(i * primary_target.number + primary_target.number - 1)

            enemy_list.append(len(primary_target.crew) - 1)

        # print("enemy_list - " + str(enemy_list))
        target = enemy_list[math.ceil((len(enemy_list) / len(perform_attack) * (at_creature + 1)) * -1)]
        # print("target - " + str(target) + " for creature - " + str(at_creature))
        return target

    elif angle == "Front left":
        # Front side
        if len(primary_target.crew) < primary_target.number:
            limit = len(primary_target.crew)
        else:
            limit = primary_target.number
        for i in range(0, limit):
            enemy_list.append(i)
            enemy_list.reverse()

        # Left flank side
        if len(primary_target.crew) > primary_target.number:
            rows_left = math.ceil(len(primary_target.crew) / primary_target.number)
            for i in range(1, rows_left):
                enemy_list.append(i * primary_target.number)

        # print("enemy_list - " + str(enemy_list))
        target = enemy_list[math.ceil(len(enemy_list) / len(perform_attack) * (at_creature + 1)) - 1]
        # print("target - " + str(target) + " for creature - " + str(at_creature))
        return target

    elif angle == "Front right":
        # Front side
        if len(primary_target.crew) < primary_target.number:
            limit = len(primary_target.crew)
        else:
            limit = primary_target.number
        for i in range(0, limit):
            enemy_list.append(i)

        # Right flank side
        full_rows_left = int(len(primary_target.crew) / primary_target.number)
        if full_rows_left > 0:
            for i in range(1, full_rows_left):  # 1 - because first row already appended
                enemy_list.append(i * primary_target.number + primary_target.number - 1)

        enemy_list.reverse()
        # print("enemy_list - " + str(enemy_list))
        target = enemy_list[math.ceil(len(enemy_list) / len(perform_attack) * (at_creature + 1)) - 1]
        # print("target - " + str(target) + " for creature - " + str(at_creature))
        return target

    elif angle == "Rear right":
        if len(primary_target.crew) % primary_target.number == 0:
            enemy_list_part = []
            # Right flank side
            full_rows_left = int(len(primary_target.crew) / primary_target.number)
            for i in range(full_rows_left - 1, full_rows_left):
                enemy_list_part.append(i * primary_target.number + primary_target.number - 1)

            enemy_list_part.reverse()

            # Rear side without the farthest right creature
            for i in range(0, len(primary_target.crew) - full_rows_left * primary_target.number - 1):
                enemy_list.append(full_rows_left * primary_target.number + i)

            enemy_list = enemy_list + enemy_list_part

        else:
            enemy_list_part = []
            # Right flank side
            full_rows_left = int(len(primary_target.crew) / primary_target.number)
            for i in range(full_rows_left - 1, full_rows_left):
                enemy_list_part.append(i * primary_target.number + primary_target.number - 1)

            enemy_list_part.reverse()

            # Rear side
            for i in range(0, len(primary_target.crew) - full_rows_left * primary_target.number):
                enemy_list.append(full_rows_left * primary_target.number + i)

            enemy_list = enemy_list + enemy_list_part

        # print("enemy_list - " + str(enemy_list))
        target = enemy_list[math.ceil(len(enemy_list) / len(perform_attack) * (at_creature + 1)) - 1]
        # print("target - " + str(target) + " for creature - " + str(at_creature))
        return target

    elif angle == "Rear left":
        # Left flank side without last row
        rows_left = math.ceil(len(primary_target.crew) / primary_target.number)
        if rows_left > 0:
            for i in range(0, rows_left):  # Without last row
                enemy_list.append(i * primary_target.number)

        # Rear side
        for i in range(0, len(primary_target.crew) - (rows_left - 1) * primary_target.number):
            enemy_list.append((rows_left - 1) * primary_target.number + i)

        print("enemy_list - " + str(enemy_list) + " from crew - " + str(len(primary_target.crew)))
        target = enemy_list[math.ceil(len(enemy_list) / len(perform_attack) * (at_creature + 1)) - 1]
        print("target - " + str(target) + " for creature - " + str(at_creature))
        return target


def kill_unit(b, primary_target):
    print("kill_unit()")
    x = int(primary_target.position[0])
    y = int(primary_target.position[1])
    TileNum = (y - 1) * game_stats.battle_width + x - 1

    # Remove regiment's card in battle queue
    for card in b.queue:
        if card.army_id == b.battle_map[TileNum].army_id and card.number == b.battle_map[TileNum].unit_index:
            b.queue.remove(card)
            b.queue_index = 0
            break

    # Making new grave in tile's graveyard for killed regiment
    b.battle_map[TileNum].graveyard.append(game_classes.Grave(b.battle_map[TileNum].unit_index,
                                                              b.battle_map[TileNum].army_id))

    # Clearing tile information about regiment
    b.battle_map[TileNum].unit_index = None
    b.battle_map[TileNum].army_id = None

    # Disengaging surrounding units
    disengage(b, b.battle_map[TileNum].posxy)

    # # Check if battle supposed to end
    # battle_ending(b)


def complete_ranged_attack(b, unit, primary_target, acting_hero, enemy_hero):
    print("complete_ranged_attack(): " + unit.name + " hitting " + primary_target.name)
    # print("First time - " + str(unit))
    # print(unit.name)
    # Total HP among all creatures in targeted regiment
    # Needed to calculate morale hit
    before_HP = 0
    for creature in primary_target.crew:
        before_HP += creature.HP

    # Reset damage counter
    b.dealt_damage = 0
    b.killed_creatures = 0

    # print(str(unit))
    # print("len(unit.crew) - " + str(len(unit.crew)))
    for at_creature in range(0, len(unit.crew)):
        if len(primary_target.crew) > 0:
            target = choose_ranged_target(b, primary_target)
            hit_funs.ranged_hit(b, unit, primary_target, target, acting_hero, enemy_hero)

    # Let's check who died in unit
    # long_msg = ""
    number = 1
    perished_list = []
    index = 0
    for df_creature in primary_target.crew:
        # long_msg += str(number) + ". HP - " + str(df_creature.HP) + " "
        number += 1

        if df_creature.HP == 0:
            perished_list.append(index)
            # # Remove killed creature
            # primary_target.cemetery.append(df_creature)
            # primary_target.crew.remove(df_creature)

        index += 1

    perished_list.reverse()
    # print("perished_list - " + str(perished_list))
    for perished in perished_list:
        # Remove killed creature
        primary_target.cemetery.append(primary_target.crew[perished])
        del primary_target.crew[perished]

    # print(long_msg)

    # If no alive creatures left, kill this unit
    if len(primary_target.crew) == 0:
        kill_unit(b, primary_target)

    # Reduce morale
    primary_target.reduce_morale(b, before_HP, "Ranged")

    # Set initiative after performed action
    set_initiative(unit, acting_hero, "Ranged")

    check_if_no_one_left_alive(b)

    b.anim_message.append(game_classes.Battle_Message(["Damage " + str(b.dealt_damage),
                                                       "Killed " + str(b.killed_creatures)],
                                                      "Regiment",
                                                      (primary_target.position[0], primary_target.position[1])))


def choose_ranged_target(b, primary_target):
    return random.randint(0, len(primary_target.crew) - 1)


def perform_battle_actions(b):
    print("perform_battle_actions")
    # b = game_stats.present_battle
    acting_army = common_selects.select_army_by_id(b.queue[0].army_id)
    acting_hero = acting_army.hero
    acting_unit = None
    if b.queue[0].obj_type != "Hero":
        acting_unit = acting_army.units[b.queue[0].number]
    enemy_army_id = b.attacker_id
    if b.attacker_id == b.queue[0].army_id:
        enemy_army_id = b.defender_id
    enemy_army = common_selects.select_army_by_id(enemy_army_id)

    if not b.battle_stop:
        # print("if not b.battle_stop")
        if b.realm_in_control != game_stats.player_power and b.AI_ready:
            print("perform_battle_actions -> AI manage_unit")
            battle_logic.manage_unit(b, acting_army, enemy_army, acting_unit, acting_hero)

        if b.secondary == "Route" and b.realm_in_control == game_stats.player_power and b.primary is None:
            print('action_order(b, "Move", "Route")')
            action_order(b, "Move", "Route")

        execute_order(b)


def advance_battle_time(time_counted):
    b = game_stats.present_battle

    if b.stage == "Fighting":

        b.battle_temp_time_passed = time_counted - b.battle_last_start
        b.battle_display_time = int(b.battle_passed_time + b.battle_temp_time_passed)

        # print("It works - " + str(math.floor(game_stats.display_time/1000) % 5))
        if math.floor(b.battle_display_time / 1000) % 1 == 0:
            # print("math.floor(game_stats.display_time/1000) % 5 == 0")
            # print("game_stats.last_change - " + str(game_stats.last_change))
            # print("math.floor(game_stats.display_time/1000) - "
            # + str(math.floor(game_stats.display_time/1000)))
            if math.floor(b.battle_display_time / 1000) != b.battle_last_change:
                # print("math.floor(game_stats.display_time/1000) != game_stats.last_change")
                b.battle_last_change = math.floor(b.battle_display_time / 1000)

                # print("game_stats.current_screen - " + str(game_stats.current_screen))
                perform_battle_actions(b)


def melee_attack_preparation(b, TileNum, position, x2, y2):
    # x, y - coordinates of target
    x = (position[0] + 1) % 96
    y = (position[1] + 1) % 96
    print("melee_attack_preparation: TileNum - " + str(TileNum) + ", position [x2, y2] - " + str([x2, y2]))
    print("x, y - " + str([x, y]))

    approach = []

    check = True

    if x < 32:
        if y < 32:
            word = "NW"
            approach = [x2 - 1, y2 - 1]
        elif 32 <= y < 64:
            word = "W"
            approach = [x2 - 1, y2]
        elif 64 <= y:
            word = "SW"
            approach = [x2 - 1, y2 + 1]
    elif 32 <= x < 64:
        if y < 32:
            word = "N"
            approach = [x2, y2 - 1]
        elif 32 <= y < 64:
            check = False
        elif 64 <= y:
            word = "S"
            approach = [x2, y2 + 1]
    elif 64 <= x < 96:
        if y < 32:
            word = "NE"
            approach = [x2 + 1, y2 - 1]
        elif 32 <= y < 64:
            word = "E"
            approach = [x2 + 1, y2]
        elif 64 <= y:
            word = "SE"
            approach = [x2 + 1, y2 + 1]

    if not approach:  # Clicked on a center of square
        check = False
    elif (approach[0] < 0 or game_stats.battle_width < approach[0]) \
            or (approach[1] < 0 or game_stats.battle_height < approach[1]):
        # Approach tile is out of bounds
        check = False
    else:
        print(word + ": TileNum position [x2, y2] - " + str([x2, y2]) + "; approach position - " + str(approach))
        ApproachTile = (approach[1] - 1) * game_stats.battle_width + approach[0] - 1
        print("ApproachTile is " + str(ApproachTile) + ", position [x2, y2] - " + str(approach))

        if b.battle_map[TileNum].map_object is not None:
            if b.battle_map[TileNum].map_object.obj_type == "Structure":
                name = b.battle_map[TileNum].map_object.obj_name
                print(name + " - " + (str([x2, y2])))
                if word in movement_catalog.block_movement_dict[name]:
                    if not b.battle_map[ApproachTile].siege_tower_deployed:
                        # Siege tower is not deployed there
                        check = False

        if b.battle_map[ApproachTile].map_object:
            if b.battle_map[ApproachTile].map_object.obj_type == "Structure":
                attack_direction = simple_direction([x2, y2], approach)
                name = b.battle_map[ApproachTile].map_object.obj_name
                print(name + " - " + (str(approach)))
                if attack_direction in movement_catalog.block_movement_dict[name]:
                    if not b.battle_map[TileNum].siege_tower_deployed:
                        # Siege tower is not deployed there
                        check = False

    print("b.attack_name - " + str(b.attack_name))
    # Standard melee attack
    if check and b.attack_name in ["Melee assault", "Dragon breath", "Drake breath"]:
        acting_army = common_selects.select_army_by_id(b.queue[0].army_id)
        enemy_army = common_selects.select_army_by_id(b.battle_map[TileNum].army_id)
        if approach in b.movement_grid:
            permitted_attack = True
            # Lets check if attack forbidden by moving onto object
            if b.battle_map[ApproachTile].map_object:
                if b.battle_map[ApproachTile].map_object.obj_type == "Structure":
                    for node in b.path:
                        if node.position == [int(approach[0]), int(approach[1])]:
                            temp_pathway = []
                            current = node
                            while current is not None:
                                temp_pathway.append(current.position)
                                current = current.parent
                            temp_pathway = temp_pathway[::-1]
                            temp_pathway = temp_pathway[-2:]
                            # print("Final temp_pathway is " + str(temp_pathway))
                            approach_direction = simple_direction(temp_pathway[0], temp_pathway[1])
                            print("approach_direction is " + str(approach_direction))
                            name = b.battle_map[ApproachTile].map_object.obj_name
                            if approach_direction in movement_catalog.waste_movement_dict[name]:
                                permitted_attack = False
                            break

            if permitted_attack:
                disengage(b, b.queue[0].position)
                b.ready_to_act = False

                b.attacking_rotate.append(game_classes.Rotation_Data(b.battle_map[ApproachTile].posxy,
                                                                     b.queue[0].number,
                                                                     b.queue[0].army_id))

                # TileNum2 = (y2 - 1) * game_stats.battle_width + x2 - 1
                b.enemy_army_id = enemy_army.army_id
                enemy_unit = enemy_army.units[b.battle_map[TileNum].unit_index]
                print("After approach defending regiment is found")
                print("unit_index is " + str(b.battle_map[TileNum].unit_index) +
                      " at TileNum " + str(TileNum) + " position " + str(b.battle_map[TileNum].posxy) +
                      " and engaged is " + str(enemy_unit.engaged))
                if not enemy_unit.engaged:
                    print(enemy_unit.name + " is going to rotate")
                    enemy_unit.engaged = True
                    b.defending_rotate.append(game_classes.Rotation_Data(tuple(enemy_unit.position),
                                                                         b.battle_map[TileNum].unit_index,
                                                                         b.battle_map[TileNum].army_id))

                if not acting_army.units[b.queue[0].number].engaged:
                    acting_army.units[b.queue[0].number].engaged = True

                print("It's possible to approach from - " + str(approach))
                b.move_destination = [int(approach[0]), int(approach[1])]
                b.target_destination = [int(x2), int(y2)]
                # prepare_takeoff(b)
                print_rotating_units(b)

                action_order(b, "Move", "Melee attack")

        elif approach == b.queue[0].position:
            disengage(b, b.queue[0].position)
            b.ready_to_act = False

            b.attacking_rotate.append(game_classes.Rotation_Data(tuple(b.queue[0].position),
                                                                 b.queue[0].number,
                                                                 b.queue[0].army_id))

            # TileNum2 = (y2 - 1) * game_stats.battle_width + x2 - 1
            b.enemy_army_id = enemy_army.army_id
            enemy_unit = enemy_army.units[b.battle_map[TileNum].unit_index]
            print("Standing next to enemy before attack ")
            if not enemy_unit.engaged:
                print(enemy_unit.name + " is going to rotate")
                enemy_unit.engaged = True
                b.defending_rotate.append(game_classes.Rotation_Data(tuple(enemy_unit.position),
                                                                     b.battle_map[TileNum].unit_index,
                                                                     b.battle_map[TileNum].army_id))

            if not acting_army.units[b.queue[0].number].engaged:
                acting_army.units[b.queue[0].number].engaged = True

            print("attacking_rotate set to - " + str(len(b.attacking_rotate)))
            print("defending_rotate set to - " + str(len(b.defending_rotate)))
            print("Standing in same position - " + str(approach))
            b.target_destination = [int(x2), int(y2)]
            action_order(b, "Rotate", "Melee attack")
            rotation_direction(b, acting_army, enemy_army)

    # Hit and fly melee attack
    elif b.attack_name == "Hit and fly":
        acting_army = common_selects.select_army_by_id(b.queue[0].army_id)
        enemy_army = common_selects.select_army_by_id(b.battle_map[TileNum].army_id)
        distance = acting_army.units[b.queue[0].number].attacks[b.attack_type_index].range_limit
        square_distance = ((x2 - b.queue[0].position[0]) ** 2) + ((y2 - b.queue[0].position[1]) ** 2)
        print("distance - " + str(distance) + "; b.queue[0].position - " + str(b.queue[0].position) +
              "; x2, y2 - " + str(x2) + ", " + str(y2) + "; square distance - " + str(square_distance))
        root_distance = square_distance ** (1 / 2)
        print("root distance - " + str(root_distance))
        if distance ** 2 >= ((x2 - b.queue[0].position[0]) ** 2) + ((y2 - b.queue[0].position[1]) ** 2) \
                and root_distance > 1.5:
            b.enemy_army_id = enemy_army.army_id
            disengage(b, b.queue[0].position)
            b.ready_to_act = False
            b.move_destination = [int(x2), int(y2)]
            b.target_destination = [int(x2), int(y2)]
            b.move_back_destination = [int(b.queue[0].position[0]), int(b.queue[0].position[1])]

            action_order(b, "Move", "Hit and fly")


def ranged_attack_preparation(b, TileNum, x2, y2):
    distance = (math.sqrt(((b.battle_map[TileNum].posxy[0] - b.queue[0].position[0]) ** 2) + (
            (b.battle_map[TileNum].posxy[1] - b.queue[0].position[1]) ** 2)))

    if distance > b.cur_range_limit:
        # Too far to hit
        pass
    else:
        x_delta = int(x2 - b.queue[0].position[0])
        y_delta = int(y2 - b.queue[0].position[1])
        facing_angle = pygame.math.Vector2(x_delta, y_delta).angle_to((1, 0))
        print("Angle - " + str(facing_angle) + "; (x2, y2) - (" + str(x2) + ", " + str(y2) + "); position - " +
              str(b.queue[0].position))

        new_direction = None
        if -22.5 <= facing_angle < 22.5:
            new_direction = "E"
        elif 22.5 <= facing_angle < 67.5:
            new_direction = "NE"
        elif 67.5 <= facing_angle < 112.5:
            new_direction = "N"
        elif 122.5 <= facing_angle < 167.5:
            new_direction = "NW"
        elif -67.5 <= facing_angle < -22.5:
            new_direction = "SE"
        elif -112.5 <= facing_angle < -67.5:
            new_direction = "S"
        elif -167.5 <= facing_angle < -112.5:
            new_direction = "SW"
        else:
            new_direction = "W"

        b.changed_direction = str(new_direction)

        TileNum2 = (y2 - 1) * game_stats.battle_width + x2 - 1
        print("TileNum2 - " + str(TileNum2))
        army = common_selects.select_army_by_id(b.battle_map[TileNum2].army_id)
        b.enemy_army_id = army.army_id

        b.target_destination = [int(x2), int(y2)]
        b.secondary = "Ranged attack"
        b.primary = "Rotate"


def damage_value(attack, acting_hero, unit):
    dmg_bonus = 0
    max_dmg_bonus = 0
    if acting_hero:
        for skill in acting_hero.skills:
            for effect in skill.effects:
                if effect.application == "Bonus damage":
                    if attack.attack_type in effect.skill_tags:
                        if effect.method == "addition":
                            dmg_bonus += int(effect.quantity)

                elif effect.application == "Bonus max damage":
                    if attack.attack_type in effect.skill_tags:
                        approved_unit_type = False
                        for tag in effect.other_tags:
                            if tag in unit.reg_tags:
                                approved_unit_type = True
                        if approved_unit_type:
                            if effect.method == "addition":
                                max_dmg_bonus += int(effect.quantity)

    new_min_dmg = int(attack.min_dmg) + dmg_bonus
    new_max_dmg = int(attack.max_dmg) + dmg_bonus + max_dmg_bonus

    # Check bless spell
    if len(unit.effects) > 0:
        for effect in unit.effects:
            if effect.name == "Bless":
                new_min_dmg = int(new_max_dmg)
    return new_min_dmg, new_max_dmg


def surrounded_by_enemy(b):
    for army in game_obj.game_armies:
        if army.army_id in [b.attacker_id, b.defender_id]:
            if army.owner == b.enemy:
                enemy_army_id = army.army_id
                break

    center = b.queue[0].position
    surrounded = False

    for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
        new_position = [center[0] + xy[0], center[1] + xy[1]]
        if 0 < new_position[0] <= game_stats.battle_width:
            if 0 < new_position[1] <= game_stats.battle_height:
                TileNum = (new_position[1] - 1) * game_stats.battle_width + new_position[0] - 1

                if b.battle_map[TileNum].army_id == enemy_army_id:
                    # Found an enemy in nearby tile
                    surrounded = True

    if surrounded:
        print("Your ranged unit ability blocked by nearby enemy unit")
    return surrounded


def disengage(b, position):
    print("game_battle .. disengage() .. Position - " + str(position))
    # If unit has died or left its position than all other units who were engaged in battle with it should disengage
    for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
        new_position = [position[0] + xy[0], position[1] + xy[1]]
        if 0 < new_position[0] <= game_stats.battle_width:
            if 0 < new_position[1] <= game_stats.battle_height:
                TileNum = (new_position[1] - 1) * game_stats.battle_width + new_position[0] - 1

                if b.battle_map[TileNum].army_id is not None:
                    # Only those enemies should be disengaged whose direction has been pointing towards this regiment
                    expected_direction = ""
                    if xy[0] == 1:
                        if xy[1] == 1:
                            expected_direction = "NW"
                        elif xy[1] == 0:
                            expected_direction = "W"
                        elif xy[1] == -1:
                            expected_direction = "SW"
                    elif xy[0] == 0:
                        if xy[1] == 1:
                            expected_direction = "N"
                        elif xy[1] == -1:
                            expected_direction = "S"
                    elif xy[0] == -1:
                        if xy[1] == 1:
                            expected_direction = "NE"
                        elif xy[1] == 0:
                            expected_direction = "E"
                        elif xy[1] == -1:
                            expected_direction = "SE"

                    army = common_selects.select_army_by_id(b.battle_map[TileNum].army_id)
                    if army.units[b.battle_map[TileNum].unit_index].direction == expected_direction:
                        army.units[b.battle_map[TileNum].unit_index].engaged = False


def routing_path(b, routing_unit, acting_hero):
    mode = "March"
    for skill in routing_unit.skills:
        if skill.application == "Movement":
            if skill.quality == "Can fly":
                mode = "Flight"
                break

    # First step - gather list of positions beyond the edge of battlefield
    exit_positions = []
    if b.queue[0].owner == b.attacker_realm:
        for i in range(1, 13):
            exit_positions.append([0, i])
    elif b.queue[0].owner == b.defender_realm:
        for i in range(1, 13):
            exit_positions.append([17, i])

    print("exit_positions: " + str(exit_positions))
    chosen_route = None
    chosen_node = None
    for exit_pos in exit_positions:
        # print("exit_pos - " + str(exit_pos))
        base_MP = calculate_speed(routing_unit, acting_hero)
        node, a_path = algo_b_astar.b_astar(None, routing_unit.position, exit_pos, None, base_MP, b, mode)
        if a_path is None:
            # print("No path for " + str(exit_pos))
            # exit_positions.remove(exit_pos)
            pass
        else:
            a_path.pop(0)
            # a_path.pop(-1)
            if chosen_route is None:
                chosen_route = a_path
                chosen_node = node
                # print("New path - " + str(a_path))
            elif len(chosen_route) > len(a_path):
                chosen_route = a_path
                chosen_node = node

    print("New path - " + str(chosen_route))
    if chosen_node:
        print("Final node - " + str(chosen_node.position))

    if chosen_route is not None:
        # b.path, b.movement_grid = [chosen_node], chosen_route
        current = chosen_node
        while current is not None:
            # print("current.position - " + str(current.position))
            # print("b.movement_grid " + str(b.movement_grid))
            if current.position in b.movement_grid:
                b.path = [copy.deepcopy(current)]
                b.move_destination = [int(current.position[0]), int(current.position[1])]
                current = None
            else:
                # print("current.parent.position - " + str(current.parent.position))
                current = current.parent


def battle_ending(b):
    functioning_attacker_army = False
    functioning_defender_army = False

    for army in game_obj.game_armies:
        if army.army_id == b.attacker_id:
            for unit in army.units:
                if unit.morale > 0.0 and len(unit.crew) > 0:
                    functioning_attacker_army = True
                    break

        elif army.army_id == b.defender_id:
            for unit in army.units:
                if unit.morale > 0.0 and len(unit.crew) > 0:
                    functioning_defender_army = True
                    break

    if not functioning_attacker_army or not functioning_defender_army:
        print("One army has lost: Attackers are standing - " + str(functioning_attacker_army) +
              " Defenders are standing - " + str(functioning_defender_army))

        if b.attacker_realm == game_stats.player_power:
            if functioning_attacker_army:
                b.battle_end_message = "Victory"
            else:
                b.battle_end_message = "Defeat"
        else:
            if functioning_defender_army:
                b.battle_end_message = "Victory"
            else:
                b.battle_end_message = "Defeat"

        if not functioning_attacker_army:
            b.defeated_side = b.attacker_realm
            if functioning_defender_army:
                for war in game_obj.game_wars:
                    if war.initiator in [b.attacker_realm, b.defender_realm]:
                        if war.respondent in [b.attacker_realm, b.defender_realm]:
                            if war.initiator == b.defender_realm:
                                war.initiator_battle_victories += 1
                            else:
                                war.respondent_battle_victories += 1
                            break
        elif not functioning_defender_army:
            b.defeated_side = b.defender_realm
            if functioning_attacker_army:
                for war in game_obj.game_wars:
                    if war.initiator in [b.attacker_realm, b.defender_realm]:
                        if war.respondent in [b.attacker_realm, b.defender_realm]:
                            if war.initiator == b.attacker_realm:
                                war.initiator_battle_victories += 1
                            else:
                                war.respondent_battle_victories += 1
                            break

        b.battle_window = "Battle end window"
        b.battle_stop = True
        b.ready_to_act = False
        b.AI_ready = False

        for army in game_obj.game_armies:
            if (army.army_id == b.attacker_id or army.army_id == b.defender_id) and army.owner == b.defeated_side:
                for unit in army.units:
                    print(unit.name + " crew size is " + str(len(unit.crew))
                          + " cemetery size is " + str(len(unit.cemetery)))
                    if len(unit.crew) > 0:
                        for creature in unit.crew:
                            b.earned_experience += int(unit.rank)
                            # print("Routing " + creature.name + " gives " + str(unit.rank)
                            #       + " experience, accumulating to " + str(b.earned_experience))

                    if len(unit.cemetery) > 0:
                        # number = 1
                        for perished in unit.cemetery:
                            # print(perished)
                            b.earned_experience += int(unit.rank)
                            # print("Perished " + perished.name + " gives " + str(unit.rank)
                            #       + " experience, accumulating to " + str(b.earned_experience)
                            #       + ", alive - " + str(perished.alive) + ", HP - " + str(perished.HP)
                            #       + ", number - " + str(number))
                            # number += 1

                if army.hero is not None:
                    b.earned_experience = math.ceil(b.earned_experience * (1 + army.hero.level * 0.05))

                print("earned_experience = " + str(b.earned_experience))
                break


def apply_aura(unit, b, army_id):
    if len(unit.skills) > 0:
        for s in unit.skills:
            # print("Skill - " + str(s))
            if s.method == "Aura":
                inclusivity = True
                if s.application == "exclusive aura":
                    inclusivity = False

                if s.quantity == 1:
                    for tile in square_one(unit.position, inclusivity):
                        TileNum = (tile[1] - 1) * game_stats.battle_width + tile[0] - 1
                        b.battle_map[TileNum].aura_effects.append([int(army_id),
                                                                   list(unit.position),
                                                                   str(s.quality)])
                else:
                    for tile in circle_range(unit.position, s.quantity, inclusivity):
                        TileNum = (tile[1] - 1) * game_stats.battle_width + tile[0] - 1
                        b.battle_map[TileNum].aura_effects.append([int(army_id),
                                                                   list(unit.position),
                                                                   str(s.quality)])


def square_one(xy, inclusive):
    reach = []
    for position in [[-1, -1], [0, -1], [1, -1],
                     [-1, 0], [0, 0], [1, 0],
                     [-1, 1], [0, 1], [1, 1]]:
        if 0 < xy[0] + position[0] <= game_stats.battle_width:
            if 0 < xy[1] + position[1] <= game_stats.battle_height:
                if inclusive:
                    reach.append([int(xy[0] + position[0]), int(xy[1] + position[1])])
                else:
                    if position != [0, 0]:
                        reach.append([int(xy[0] + position[0]), int(xy[1] + position[1])])

    return reach


def circle_range(start, distance, inclusive):
    # print("Start - " + str(start) + " and distance - " + str(distance))
    reach = []
    for x_pos in range(start[0] - distance, start[0] + distance + 1):
        if 0 < x_pos <= game_stats.battle_width:
            for y_pos in range(start[1] - distance, start[1] + distance + 1):
                if 0 < y_pos <= game_stats.battle_height:
                    # print("Tile - [" + str(x_pos) + ", " + str(y_pos) + "]")
                    # print("Distance^2 - {0}, x^2 - {1} y^2 - {2}".format(str(distance ** 2), str(x_pos ** 2),
                    #                                                      str(y_pos ** 2)))
                    if distance ** 2 >= ((x_pos - start[0]) ** 2) + ((y_pos - start[1]) ** 2):
                        if inclusive:
                            reach.append([x_pos, y_pos])
                        else:
                            if [x_pos, y_pos] != start:
                                reach.append([x_pos, y_pos])

    return reach


def remove_aura_effects(unit_position, b):
    # TileNum = (unit_position[1] - 1) * game_stats.battle_width + unit_position[0] - 1
    for tile in b.battle_map:
        if len(tile.aura_effects) > 0:
            index_list = []
            number = 0
            for aura in tile.aura_effects:
                if aura[1] == unit_position:
                    index_list.append(int(number))

                number += 1

            common_lists.reversed_list_cleaning(tile.aura_effects, index_list)


def set_initiative(unit, acting_hero, action_type):
    initiative = 1.0
    reduction_list = []
    if acting_hero is not None:
        for skill in acting_hero.skills:
            for effect in skill.effects:
                if effect.application == "Initiative time reduction":
                    if effect.method == "subtraction":
                        if action_type in effect.skill_tags:
                            appropriate_unit = False
                            if len(effect.other_tags) > 0:
                                for unit_tag in unit.reg_tags:
                                    if unit_tag in effect.other_tags:
                                        appropriate_unit = True
                            else:
                                appropriate_unit = True

                            if appropriate_unit:
                                reduction_list.append(float(effect.quantity))

        if len(acting_hero.inventory) > 0:
            for artifact in acting_hero.inventory:
                for effect in artifact.effects:
                    if effect.application == "Initiative time reduction":
                        if effect.method == "subtraction":
                            if action_type in effect.application_tags:
                                appropriate_unit = False
                                if len(effect.other_tags) > 0:
                                    for unit_tag in unit.reg_tags:
                                        if unit_tag in effect.other_tags:
                                            appropriate_unit = True
                                else:
                                    appropriate_unit = True

                                if appropriate_unit:
                                    reduction_list.append(float(effect.quantity))
    if len(reduction_list) > 0:
        for item in reduction_list:
            initiative = initiative * (1 - item)

        initiative = math.ceil(initiative * 100) / 100

    # print("initiative - " + str(initiative) + ", reduction_list - " + str(reduction_list))
    unit.initiative = float(initiative)


def calculate_speed(unit, acting_hero):
    final_speed = int(unit.speed)
    addition_bonus_list = []
    subtraction_bonus_list = []
    # print(unit.name + ": starting speed - " + str(final_speed))

    if acting_hero is not None:
        # print("Hero - " + str(acting_hero.name))
        # Skills
        for skill in acting_hero.skills:
            for effect in skill.effects:
                if effect.application == "Bonus speed":
                    if effect.method == "addition":
                        appropriate_unit = False
                        if len(effect.other_tags) > 0:
                            for unit_tag in unit.reg_tags:
                                if unit_tag in effect.other_tags:
                                    appropriate_unit = True
                        else:
                            appropriate_unit = True

                        if appropriate_unit:
                            addition_bonus_list.append(int(effect.quantity))

        if len(acting_hero.inventory) > 0:
            for artifact in acting_hero.inventory:
                for effect in artifact.effects:
                    if effect.application == "Bonus speed":
                        appropriate_unit = False
                        if len(effect.other_tags) > 0:
                            for unit_tag in unit.reg_tags:
                                if unit_tag in effect.other_tags:
                                    appropriate_unit = True
                        else:
                            appropriate_unit = True

                        if appropriate_unit:
                            if effect.method == "addition":
                                addition_bonus_list.append(int(effect.quantity))
                            elif effect.method == "subtraction":
                                subtraction_bonus_list.append(int(effect.quantity))

    if len(unit.effects) > 0:
        for effect in unit.effects:
            for buff in effect.buffs:
                if buff.application == "Speed":
                    if buff.method == "addition":
                        addition_bonus_list.append(int(buff.quantity))
                    elif buff.method == "subtraction":
                        subtraction_bonus_list.append(int(buff.quantity))

    if len(addition_bonus_list) > 0:
        for item in addition_bonus_list:
            final_speed += int(item)

    if len(subtraction_bonus_list) > 0:
        for subtraction in subtraction_bonus_list:
            final_speed -= int(subtraction)
            if final_speed < 0:
                final_speed = 0

    # Minimal speed could be only 2
    if final_speed < 2:
        final_speed = int(0)
    # print("Final speed - " + str(final_speed))

    return final_speed


def check_if_no_one_left_alive(b):
    print("")
    print("check_if_no_one_left_alive()")
    print("b.enemy_army_id - " + str(b.enemy_army_id))
    alive = False
    army = common_selects.select_army_by_id(b.enemy_army_id)
    for unit in army.units:
        if len(unit.crew) > 0:
            alive = True
            break

    if not alive:
        battle_ending(b)


def attack_range_effect(army, unit, base_range):
    final_range = int(base_range)
    addition_bonus_list = []

    if army.hero:
        # Hero artifacts
        if len(army.hero.inventory) > 0:
            for artifact in army.hero.inventory:
                for effect in artifact.effects:
                    if effect.application == "Attack range":
                        appropriate_unit = False
                        if len(effect.other_tags) > 0:
                            for unit_tag in unit.reg_tags:
                                if unit_tag in effect.other_tags:
                                    appropriate_unit = True
                        else:
                            appropriate_unit = True

                        if appropriate_unit:
                            if effect.method == "addition":
                                addition_bonus_list.append(int(effect.quantity))

    if len(addition_bonus_list) > 0:
        for addition in addition_bonus_list:
            final_range += int(addition)

    # print("base_range - " + str(base_range) + " => "
    #       + "final_range - " + str(final_range))
    return final_range


def check_direction(unit, primary_target, directions):
    attacker_relative_position = None
    if unit.position[0] < primary_target.position[0]:
        if unit.position[1] < primary_target.position[1]:
            attacker_relative_position = "NW"
        elif unit.position[1] == primary_target.position[1]:
            attacker_relative_position = "W"
        elif unit.position[1] > primary_target.position[1]:
            attacker_relative_position = "SW"

    elif unit.position[0] == primary_target.position[0]:
        if unit.position[1] < primary_target.position[1]:
            attacker_relative_position = "N"
        elif unit.position[1] > primary_target.position[1]:
            attacker_relative_position = "S"

    elif unit.position[0] > primary_target.position[0]:
        if unit.position[1] < primary_target.position[1]:
            attacker_relative_position = "NE"
        elif unit.position[1] == primary_target.position[1]:
            attacker_relative_position = "E"
        elif unit.position[1] > primary_target.position[1]:
            attacker_relative_position = "SE"

    print("attacker_relative_position - " + str(attacker_relative_position))
    if attacker_relative_position in directions:
        return True
    else:
        return False


def rotation_direction(b, acting_army, enemy_army):
    print("rotation_direction(): b.primary - " + str(b.primary) + "; b.secondary - " + str(b.secondary))
    if len(b.attacking_rotate) > 0:

        # When defending regiment is directly facing attacking regiment, it doesn’t need to show rotating animation
        # Therefore it only matter during primary == "Melee attack"
        # During primary == "Counterattack" defending regiment still facing attacking regiment, but rotating animation
        # gives and impression of performing attack in this case
        num_list = []
        num = 0
        for regiment_info in b.defending_rotate:
            unit = enemy_army.units[regiment_info.number]
            new_direction = change_direction(unit.position, b.queue[0].position)
            if unit.direction != new_direction:
                print("defending_rotate: " + unit.name + " " + str(regiment_info.number)
                      + " new direction - " + unit.direction)
            else:
                # Defending unit already facing attacking unit and
                # it is attacking unit that is performing attack right now
                if b.secondary == "Melee attack":
                    print("defending_rotate: " + str(num) + " delete from defending_rotate (already facing attacker)")
                    num_list.append(num)
            num += 1

        common_lists.reversed_list_cleaning(b.defending_rotate, num_list)
        print_rotating_units(b)
        print("")


def print_rotating_units(b):
    text = "attacking_rotate:"
    for regiment_info in b.attacking_rotate:
        text += " " + str(regiment_info.number)
    print(text)
    text = "defending_rotate:"
    for regiment_info in b.defending_rotate:
        text += " " + str(regiment_info.number)
    print(text)


def change_side_direction(unit, b, acting_army, enemy_army):
    if b.primary in ["Move", "Route"]:
        # The location of the regiment relative to the target tile on battle map
        direction = simple_direction(unit.position, b.tile_trail[0])

        if direction in ["NW", "W", "SW"]:
            if not unit.right_side:
                unit.right_side = True

        elif direction in ["NE", "E", "SE"]:
            if unit.right_side:
                unit.right_side = False
    elif b.primary == "Rotate":
        if len(b.attacking_rotate) > 0:
            # print("b.attacking_rotate - " + str(b.attacking_rotate))
            for regiment_info in b.attacking_rotate:
                regiment = acting_army.units[regiment_info.number]
                direction = simple_direction(regiment.position, b.target_destination)

                if direction in ["NW", "W", "SW"]:
                    if not regiment.right_side:
                        regiment.right_side = True

                elif direction in ["NE", "E", "SE"]:
                    if regiment.right_side:
                        regiment.right_side = False

        if len(b.defending_rotate) > 0:
            # print("b.defending_rotate - " + str(b.defending_rotate))
            for regiment_info in b.defending_rotate:
                regiment = enemy_army.units[regiment_info.number]
                direction = simple_direction(regiment.position, b.queue[0].position)
                print(str(regiment.position) + " - " + str(b.queue[0].position))
                print(regiment.name + " is standing " + str(direction) + " relative to enemy")

                if direction in ["NW", "W", "SW"]:
                    if not regiment.right_side:
                        regiment.right_side = True

                elif direction in ["NE", "E", "SE"]:
                    if regiment.right_side:
                        regiment.right_side = False


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


def gates_destruction(b, TileNum):
    toughness = siege_warfare_catalog.detailed_hardness_table[b.battle_map[TileNum].map_object.obj_name]
    attack = 4
    result = random.randint(1, attack + toughness)
    tile = b.battle_map[TileNum]
    if result <= attack:
        b.anim_message.append(game_classes.Battle_Message(["The gate has been destroyed"],
                                                          "Structure",
                                                          (tile.posxy[0], tile.posxy[1])))
        b.battle_map[TileNum].map_object.obj_name = siege_warfare_catalog.name_change_after_destruction[
            b.battle_map[TileNum].map_object.obj_name]
        b.battle_map[TileNum].map_object.img_path = siege_warfare_catalog.path_change_after_destruction[
            b.battle_map[TileNum].map_object.obj_name]

        # Update visuals
        update_gf_battle.add_structure_obstacle_sprites([[b.battle_map[TileNum].map_object.obj_name,
                                                          b.battle_map[TileNum].map_object.img_path]])

    else:
        b.anim_message.append(game_classes.Battle_Message(["The gate has been destroyed"],
                                                          "Structure",
                                                          (tile.posxy[0], tile.posxy[1])))


def dock_the_wall(b):
    army = common_selects.select_army_by_id(b.queue[0].army_id)
    the_unit = army.units[b.queue[0].number]

    the_unit.siege_engine = None

    x1 = int(b.queue[0].position[0])
    y1 = int(b.queue[0].position[1])
    TileNum = (y1 - 1) * game_stats.battle_width + x1 - 1
    b.battle_map[TileNum].siege_tower_deployed = True


def open_or_close_the_gate(b, TileNum):
    if b.battle_type == "Siege":
        if len(b.tile_trail) > 1:
            x1 = int(b.tile_trail[0][0])
            y1 = int(b.tile_trail[0][1])
            TileNum1 = (y1 - 1) * game_stats.battle_width + x1 - 1

            x2 = int(b.tile_trail[1][0])
            y2 = int(b.tile_trail[1][1])

            if simple_direction([x1, y1], [x2, y2]) == "E":

                Tile_Obj = b.battle_map[TileNum1].map_object

                # print("open_or_close_the_gate")

                # Open the gate
                if Tile_Obj:
                    print(Tile_Obj.obj_name)
                    if Tile_Obj.obj_name in siege_warfare_catalog.name_change_open_gates:
                        # old_name = Tile_Obj.obj_name
                        Tile_Obj.obj_name = siege_warfare_catalog.name_change_open_gates[Tile_Obj.obj_name]
                        Tile_Obj.disposition = siege_warfare_catalog.position_change_open_gates[Tile_Obj.obj_name]
                        Tile_Obj.img_path = siege_warfare_catalog.path_change_open_gates[Tile_Obj.obj_name]

                        print(str(Tile_Obj.obj_name))
                        print(str(Tile_Obj.img_path))

                        # Update visuals
                        update_gf_battle.add_structure_obstacle_sprites([[Tile_Obj.obj_name,
                                                                          Tile_Obj.img_path]])


def prepare_takeoff(b):
    unit = None
    army = common_selects.select_army_by_id(b.queue[0].army_id)
    if b.queue[0].obj_type != "Hero":
        unit = army.units[b.queue[0].number]

    for skill in unit.skills:
        if skill.application == "Movement":
            if skill.quality == "Can fly":
                unit.in_air = True
                if len(b.tile_trail) == 1:
                    b.move_figure = "1 tile hop"
                else:
                    b.move_figure = "takeoff"
                break


def choose_melee_attack_by_type(b, unit, primary_target):
    # When attacking regiment has more than one attack profile, it must choose the most appropriate one
    # print("")
    # print("choose_melee_attack_by_type")
    # print("Striking regiment - " + str(unit.name))
    number_of_melee_profiles = 0
    last_melee_attack_index = 0  # Generally it is 0
    index = 0
    for attack in unit.attacks:
        if attack.attack_type == "Melee":
            last_melee_attack_index = int(index)
            index += 1
            number_of_melee_profiles += 1

    # print("number_of_melee_profiles - " + str(number_of_melee_profiles))

    if number_of_melee_profiles == 0:
        b.attack_type_index = int(last_melee_attack_index)
        b.attack_type_in_use = unit.attacks[b.attack_type_index].attack_type
        b.attack_name = unit.attacks[b.attack_type_index].name

    else:  # Must choose
        # print("unit.max_HP - " + str(unit.max_HP))
        # print("primary_target.max_HP - " + str(primary_target.max_HP))
        if unit.max_HP / 2 >= primary_target.max_HP:
            # Enemy creatures are more squishy
            index = 0
            for attack in unit.attacks:
                if attack.name in ["Dragon breath", "Drake breath"]:
                    b.attack_type_index = int(index)
                    b.attack_type_in_use = unit.attacks[b.attack_type_index].attack_type
                    b.attack_name = unit.attacks[b.attack_type_index].name
                index += 1
        else:
            index = 0
            for attack in unit.attacks:
                if attack.name == "Melee assault":
                    b.attack_type_index = int(index)
                    b.attack_type_in_use = unit.attacks[b.attack_type_index].attack_type
                    b.attack_name = unit.attacks[b.attack_type_index].name
                index += 1

    # print(str(b.attack_name))
    # print(str(b.attack_type_in_use))
    # print("")


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
