## Miracle battles!

import math
import random
import pygame.math

from Resources import game_classes
from Resources import effect_classes
from Resources import game_obj
from Resources import game_stats
from Resources import algo_movement_range
from Battle_AI import battle_logic


# Battle queue keeps record in what order will act regiments, heroes and effects
def form_queue(b):  # b - stands for Battle
    blank = []

    for army in game_obj.game_armies:
        if army.army_id in [b.attacker_id, b.defender_id]:
            a = army
            first_color = None
            second_color = None
            if a.owner != "Neutral":
                for power in game_obj.game_powers:
                    if a.owner == power.name:
                        first_color = str(power.f_color)
                        second_color = str(power.s_color)

            index = 0
            for unit in a.units:
                blank.append([a.army_id, a.owner, index, unit.position, unit.img_source, unit.img, first_color,
                              second_color, unit.x_offset, unit.y_offset])
                index += 1

    random.shuffle(blank)

    for item in blank:
        b.queue.append(game_classes.Queue_Card(0.0, "Regiment", item[0], item[1], item[2], item[3], item[4],
                                               item[5], item[6], item[7], item[8], item[9]))


# Check next queue card and prepare battle state
def advance_queue(b):  # b - stands for Battle
    # Resetting
    b.attacking_rotate = []
    b.defending_rotate = []

    b.realm_in_control = str(b.queue[0].owner)

    if b.realm_in_control == b.attacker_realm:
        b.enemy = b.defender_realm
    else:
        b.enemy = b.attacker_realm

    print("b.realm_in_control - " + str(b.realm_in_control) + " b.attacker_realm - " + str(b.attacker_realm) +
          " b.defender_realm - " + str(b.defender_realm) + " b.enemy - " + str(b.enemy))

    if b.realm_in_control == game_stats.player_power:
        b.ready_to_act = True
    else:
        b.AI_ready = True

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

    for army in game_obj.game_armies:
        if army.army_id == b.queue[0].army_id:
            MP = army.units[b.queue[0].number].speed
            start = b.queue[0].position

    b.path, b.movement_grid = algo_movement_range.pseudo_astar(None, start, MP, b)

    for army in game_obj.game_armies:
        if army.army_id == b.queue[0].army_id:
            b.attack_type_index = 0
            b.attack_type_in_use = army.units[b.queue[0].number].attacks[b.attack_type_index].attack_type
            b.cur_effective_range = army.units[b.queue[0].number].attacks[b.attack_type_index].effective_range
            b.cur_range_limit = army.units[b.queue[0].number].attacks[b.attack_type_index].range_limit

            unit = army.units[b.queue[0].number]
            # Reset engage status
            unit.engaged = False
            # Reset counterattack counter
            unit.counterattack = 1
            # Restore some morale
            if unit.morale + game_stats.battle_morale_base_restoration > unit.leadership:
                unit.morale = float(unit.leadership)
            else:
                unit.morale += game_stats.battle_morale_base_restoration
            # Check if unit should route due to low morale
            if unit.morale <= 0.0:
                b.primary = "Move"
                b.secondary = "Route"

            # Check duration of effects
            for e in unit.effects:
                if e.until_next_turn:
                    print(str(e.name) + " effect has ended")
                    unit.effects.remove(e)


def complete_turn(b, add_time):
    print("complete_turn")
    # b.queue[0].time_act += add_time
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
    advance_queue(b)


def action_order(b, first_action, second_action):
    b.primary = first_action
    b.secondary = second_action
    print("First action - " + str(b.primary))

    if first_action == "Move":
        # print("length of b.path - " + str(len(b.path)))
        for node in b.path:
            # print("node position - " + str(node.position))
            if node.position == b.move_destination:
                print("node.position - " + str(node.position) + " and b.move_destination - " + str(b.move_destination))
                pathway = []
                current = node
                while current is not None:
                    pathway.append(current.position)
                    current = current.parent
                print("Final unreversed path is " + str(pathway))
                b.tile_trail = list(pathway[::-1])
                b.tile_trail = b.tile_trail[1:]
                print("Final reversed path is " + str(b.tile_trail))

        # b.move_destination = None
        b.movement_grid = None
        b.path = None

        # Disengaging surrounding units
        disengage(b, b.queue[0].position)


def execute_order(b):
    for army in game_obj.game_armies:
        if army.army_id == b.queue[0].army_id:
            unit = army.units[b.queue[0].number]

    if b.primary == "Move":
        # print("execute_order - Move")
        for army in game_obj.game_armies:
            if army.army_id == b.queue[0].army_id:
                unit = army.units[b.queue[0].number]

        x1 = int(b.queue[0].position[0])
        y1 = int(b.queue[0].position[1])
        TileNum1 = (y1 - 1) * game_stats.battle_width + x1 - 1

        b.queue[0].position = b.tile_trail.pop(0)

        x2 = int(b.queue[0].position[0])
        y2 = int(b.queue[0].position[1])
        TileNum2 = (y2 - 1) * game_stats.battle_width + x2 - 1

        b.battle_map[TileNum2].unit_index = int(b.battle_map[TileNum1].unit_index)
        b.battle_map[TileNum1].unit_index = None
        b.battle_map[TileNum2].army_id = int(b.battle_map[TileNum1].army_id)
        b.battle_map[TileNum1].army_id = None

        unit.position = [int(x2), int(y2)]
        unit.direction = change_direction([x1, y1], [x2, y2])

        if len(b.tile_trail) == 0:
            b.tile_trail = None
            b.primary = None
            if b.secondary is None:
                b.move_destination = None
                complete_turn(b, 1.0)
            elif b.secondary == "Melee attack":
                b.primary = "Rotate"

    elif b.primary == "Wait":
        b.primary = "Wait message"
        b.anim_message = "Wait"
        # print("b.primary")
    elif b.primary == "Wait message":
        b.primary = "Wait message1"
        b.anim_message = "Wait"
    elif b.primary == "Wait message1":
        b.primary = None
        b.anim_message = None
        complete_turn(b, 0.5)

    elif b.primary == "Defend":
        unit.effects.append(effect_classes.Battle_Effect("Defend action", True, 0,
                                                         [effect_classes.Buff("Armor", int(unit.armor),
                                                                              "addition", None),
                                                          effect_classes.Buff("Defence", int(unit.defence),
                                                                              "addition", None)]))
        b.primary = "Defend message"
        b.anim_message = "Defend"
    elif b.primary == "Defend message":
        b.primary = "Defend message1"
        b.anim_message = "Defend"
    elif b.primary == "Defend message1":
        b.primary = None
        b.anim_message = None
        complete_turn(b, 1.0)

    elif b.primary == "Rotate":
        if b.secondary == "Melee attack":
            b.primary = "Melee attack"
            b.secondary = None
            if len(b.attacking_rotate) > 0:
                for army in game_obj.game_armies:
                    if army.army_id == b.queue[0].army_id:
                        for number in b.attacking_rotate:
                            unit = army.units[number]
                            unit.direction = change_direction(unit.position, b.target_destination)

                    if army.army_id == b.enemy_army_id:
                        for number in b.defending_rotate:
                            unit = army.units[number]
                            unit.direction = change_direction(unit.position, b.queue[0].position)

        elif b.secondary == "Counterattack":
            b.primary = "Counterattack"
            b.secondary = None

            TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
            for army in game_obj.game_armies:
                if army.army_id == b.battle_map[TileNum2].army_id:
                    b.enemy_army_id = army.army_id
                    if not army.units[b.battle_map[TileNum2].unit_index].engaged:
                        army.units[b.battle_map[TileNum2].unit_index].engaged = True

                    b.defending_rotate.append(b.battle_map[TileNum2].unit_index)

            if len(b.attacking_rotate) > 0:
                for army in game_obj.game_armies:
                    if army.army_id == b.queue[0].army_id:
                        for number in b.attacking_rotate:
                            unit = army.units[number]
                            unit.direction = change_direction(unit.position, b.target_destination)

                    if army.army_id == b.enemy_army_id:
                        for number in b.defending_rotate:
                            unit = army.units[number]
                            unit.direction = change_direction(unit.position, b.queue[0].position)

        # complete_turn(b, 1.0)
        elif b.secondary == "Ranged attack":
            for army in game_obj.game_armies:
                if army.army_id == b.queue[0].army_id:
                    unit = army.units[b.queue[0].number]
                    unit.direction = str(b.changed_direction)

            b.primary = "Ranged attack"
            b.secondary = None

    elif b.primary == "Melee attack":
        TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
        for army in game_obj.game_armies:
            if army.army_id == b.queue[0].army_id:
                unit_at = army.units[b.queue[0].number].direction
                unit = army.units[b.queue[0].number]

            elif army.army_id == b.enemy_army_id:
                unit_df = army.units[b.battle_map[TileNum2].unit_index].direction
                primary_target = army.units[b.battle_map[TileNum2].unit_index]

        angle = attack_angle(unit_at, unit_df)

        b.perform_attack = form_list_of_attackers(b, unit)
        complete_melee_attack(b, unit, primary_target, angle)
        b.primary = "Damage message"
        b.anim_message = "Damage and kills"

    elif b.primary == "Damage message":
        b.primary = "Damage message1"
        b.anim_message = "Damage and kills"
    elif b.primary == "Damage message1":
        b.primary = None
        b.anim_message = None

        TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
        if b.battle_map[TileNum2].army_id is not None:
            for army in game_obj.game_armies:

                if army.army_id == b.enemy_army_id:
                    unit = army.units[b.battle_map[TileNum2].unit_index]

            # Check if enemy unit is routing or should start routing
            if unit.morale <= 0.0:
                b.secondary = None
                complete_turn(b, 1.0)
            else:
                # Check if attacked unit can counterattack back
                if unit.counterattack > 0 and len(unit.crew) > 0 and b.secondary != "Ranged attack":
                    b.primary = "Rotate"
                    b.secondary = "Counterattack"
                    unit.counterattack -= 1

                else:
                    b.secondary = None
                    complete_turn(b, 1.0)
        else:
            # Defending unit has been killed before it could counterattack
            complete_turn(b, 1.0)

    elif b.primary == "Counterattack":

        TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
        for army in game_obj.game_armies:
            if army.army_id == b.queue[0].army_id:
                unit_df = army.units[b.queue[0].number].direction
                primary_target = army.units[b.queue[0].number]

            elif army.army_id == b.enemy_army_id:
                unit_at = army.units[b.battle_map[TileNum2].unit_index].direction
                unit = army.units[b.battle_map[TileNum2].unit_index]

        angle = attack_angle(unit_at, unit_df)

        b.perform_attack = form_list_of_attackers(b, unit)
        complete_melee_attack(b, unit, primary_target, angle)

        b.primary = "Counterattack damage message"
        b.anim_message = "Damage and kills"

    elif b.primary == "Counterattack damage message":
        b.primary = "Counterattack damage message1"
        b.anim_message = "Damage and kills"
    elif b.primary == "Counterattack damage message1":
        b.primary = None
        b.anim_message = None

        complete_turn(b, 1.0)

    elif b.primary == "Ranged attack":
        TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
        print("b.target_destination - " + str(b.target_destination) + " TileNum2 - " + str(TileNum2))
        print("b.enemy_army_id - " + str(b.enemy_army_id) + " b.queue[0].army_id - " + str(b.queue[0].army_id))

        for army in game_obj.game_armies:
            if army.army_id == b.queue[0].army_id:
                print("b.queue[0].army_id - " + str(b.queue[0].army_id) + " owner - " + str(b.queue[0].owner))
                unit = army.units[b.queue[0].number]
                print("Unit object - " + str(unit) + " b.queue[0].number - " + str(b.queue[0].number))

            elif army.army_id == b.enemy_army_id:
                print("b.queue[0].army_id - " + str(b.enemy_army_id) + " owner - " + str(army.owner))
                primary_target = army.units[b.battle_map[TileNum2].unit_index]

        print("Again, unit object - " + str(unit) + " len(unit.crew) - " + str(len(unit.crew)))
        complete_ranged_attack(b, unit, primary_target)  # complete_ranged_attack(b, unit, primary_target)
        b.primary = "Damage message"
        b.anim_message = "Damage and kills"
        b.secondary = "Ranged attack"


def change_direction(position1, position2):
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
    dir_code = {"NE" : 1,
                "E" : 2,
                "SE" : 3,
                "S" : 4,
                "SW" : 5,
                "W" : 6,
                "NW" : 7,
                "N" : 8}

    attacker = dir_code[unit_at]
    defender = dir_code[unit_df]

    step1 = (int(attacker) + 4) % 8
    step2 = int(defender) - step1
    step3 = 8 - step2
    step4 = step3 % 8

    if step4 == 0:
        step4 = 8

    angle_code = {1 : "Front right",
                  2 : "Right flank",
                  3 : "Rear right",
                  4 : "Rear",
                  5 : "Rear left",
                  6 : "Left flank",
                  7 : "Front left",
                  8 : "Front"}

    direction_angle = angle_code[step4]
    print("unit_at - " + str(unit_at) + ", unit_df - " + str(unit_df))
    print("attacker - " + str(attacker) + ", defender - " + str(defender))
    print("step1 - " + str(step1) + ", step2 - " + str(step2) + ", step3 - " + str(step3) + ", " + str(step4))
    print("attack_angle - " + str(direction_angle))

    return direction_angle


def form_list_of_attackers(b, unit):
    if b.primary == "Melee attack" or b.primary == "Counterattack":
        index_list = []
        index_count = 0
        while index_count <= len(unit.crew) - 1 and index_count <= unit.number - 1:
            index_list.append(index_count)
            index_count += 1

        print("index_list - " + str(index_list))
        return index_list


def complete_melee_attack(b, unit, primary_target, angle):
    # Total HP among all creatures in targeted regiment
    # Needed to calculate morale hit
    before_HP = 0
    for creature in primary_target.crew:
        before_HP += creature.HP

    # Reset damage counter
    b.dealt_damage = 0
    b.killed_creatures = 0

    for at_creature in b.perform_attack:
        if len(primary_target.crew) > 0:
            target = choose_melee_target(b, at_creature, primary_target, angle)
            melee_hit(b, at_creature, unit, primary_target, target)

    # Reduce morale
    reduce_morale(b, primary_target, before_HP, angle)


def choose_melee_target(b, at_creature, primary_target, angle):
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
        target = enemy_list[math.ceil((len(enemy_list)/len(b.perform_attack) * (at_creature + 1)) * -1)]
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
        target = enemy_list[math.ceil(len(enemy_list) / len(b.perform_attack) * (at_creature + 1)) - 1]
        print("target - " + str(target) + " for creature - " + str(at_creature))
        return target

    elif angle == "Left flank":
        rows_left = math.ceil(len(primary_target.crew) / primary_target.number)
        for i in range(0, rows_left):
            enemy_list.append(i * primary_target.number)

        # print("enemy_list - " + str(enemy_list))
        target = enemy_list[math.ceil(len(enemy_list) / len(b.perform_attack) * (at_creature + 1)) - 1]
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
        target = enemy_list[math.ceil((len(enemy_list)/len(b.perform_attack) * (at_creature + 1)) * -1)]
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
        target = enemy_list[math.ceil(len(enemy_list) / len(b.perform_attack) * (at_creature + 1)) - 1]
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
        target = enemy_list[math.ceil(len(enemy_list) / len(b.perform_attack) * (at_creature + 1)) - 1]
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
        target = enemy_list[math.ceil(len(enemy_list) / len(b.perform_attack) * (at_creature + 1)) - 1]
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
        target = enemy_list[math.ceil(len(enemy_list) / len(b.perform_attack) * (at_creature + 1)) - 1]
        print("target - " + str(target) + " for creature - " + str(at_creature))
        return target


def melee_hit(b, at_creature, unit, primary_target, target):
    s = unit.attacks[b.attack_type_index]

    total_defence = int(primary_target.armor + primary_target.defence)
    total_defence += armor_effect(primary_target) + defence_effect(primary_target)
    total_attack = int(s.mastery)
    additional_damage = addtional_attack_skill(unit)

    dif = total_attack - total_defence

    modifier = 1.0
    dmg = random.randint(s.min_dmg, s.max_dmg)

    print("Random damage is " + str(dmg))

    if dif > 0:  # Advantage

        for i in range(1, dif + 1):
            step1 = i / ((i - 1) + i)
            step2 = float(game_stats.battle_base_modifier) * step1
            modifier += step2

        dmg = math.ceil(dmg * modifier)

    elif dif < 0:  # Disadvantage

        dif = dif * -1
        for i in range(1, dif + 1):

            step1 = i / ((i - 1) + i)

            step2 = float(game_stats.battle_base_modifier) * step1
            # print("i - " + str(i) + ", step1 - " + str(step1) + ", step2 - " + str(step2))
            modifier += step2

        # print("modifier " + str(modifier))
        dmg = math.floor(dmg / modifier)
        if dmg == 0:
            dmg = 1

    base_dmg = int(dmg)
    dmg += int(additional_damage)
    print("Mastery - " + str(total_attack) + ", total defence - " + str(total_defence) + ", damage - " + str(base_dmg) +
          " damage with skills - " + str(dmg))
    print("len(primary_target.crew) - " + str(len(primary_target.crew)) + " target - " + str(target))
    # print("Creature " + str(at_creature) + " hurt creature " + str(target) + " with " +
    #       str(primary_target.crew[target].HP) + " HP by dealing " + str(dmg) + " damage")
    primary_target.crew[target].HP -= dmg

    b.damage_msg_position = list(primary_target.position)

    if primary_target.crew[target].HP <= 0:
        b.dealt_damage += (dmg + primary_target.crew[target].HP)
        b.killed_creatures += 1

        primary_target.crew[target].HP = 0
        primary_target.cemetery.append(primary_target.crew.pop(target))

    else:
        b.dealt_damage += dmg

    print("Crew size left - " + str(len(primary_target.crew)))
    if len(primary_target.crew) == 0:
        kill_unit(b, primary_target)


def kill_unit(b, primary_target):

    x = int(primary_target.position[0])
    y = int(primary_target.position[1])
    TileNum = (y - 1) * game_stats.battle_width + x - 1

    # Remove regiment's card in battle queue
    for card in b.queue:
        if card.army_id == b.battle_map[TileNum].army_id and card.number == b.battle_map[TileNum].unit_index:
            b.queue.remove(card)
            b.queue_index = 0

    # Making new grave in tile's graveyard for killed regiment
    b.battle_map[TileNum].graveyard.append(game_classes.Grave(b.battle_map[TileNum].unit_index,
                                                              b.battle_map[TileNum].army_id))

    # Clearing tile information about regiment
    b.battle_map[TileNum].unit_index = None
    b.battle_map[TileNum].army_id = None

    # Disengaging surrounding units
    disengage(b, b.battle_map[TileNum].posxy)


def complete_ranged_attack(b, unit, primary_target):
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
            ranged_hit(b, unit, primary_target, target)

    # Let's check who died in unit
    for df_creature in primary_target.crew:
        if df_creature.HP == 0:
            # Remove killed creature
            primary_target.cemetery.append(df_creature)
            primary_target.crew.remove(df_creature)

    # If no alive creatures left, kill this unit
    if len(primary_target.crew) == 0:
        kill_unit(b, primary_target)

    # Reduce morale
    reduce_morale(b, primary_target, before_HP, "Ranged")


def choose_ranged_target(b, primary_target):
    return random.randint(0, len(primary_target.crew) - 1)


def ranged_hit(b, unit, primary_target, target):

    s = unit.attacks[b.attack_type_index]

    distance = (math.sqrt(((primary_target.position[0] - unit.position[0]) ** 2) + (
            (primary_target.position[1] - unit.position[1]) ** 2)))

    successful_hit = True
    # Base accuracy of 50d could be lowered if enemy regiment is not full
    accuracy = math.ceil(50 * len(primary_target.crew) / (primary_target.rows * primary_target.number))

    total_attack = int(s.mastery)

    if distance <= b.cur_effective_range:
        # Everything is good, creature hit with maximum accuracy and with full strength
        pass
    else:
        total_attack = math.ceil(int(s.mastery) / 2)
        # Accuracy: base is 50 if enemy regiment is full
        # After effective range it declines
        accuracy += math.ceil(50 * (distance - b.cur_effective_range) / (b.cur_range_limit - b.cur_effective_range))
        shot_dice = random.randint(1, 100)
        if shot_dice <= accuracy:
            successful_hit = True
        else:
            successful_hit = False

    total_defence = int(primary_target.armor)

    dif = total_attack - total_defence

    modifier = 1.0
    dmg = random.randint(s.min_dmg, s.max_dmg)

    if successful_hit:
        # Target was hit by this creature
        if dif > 0:  # Advantage

            for i in range(1, dif + 1):
                step1 = i / ((i - 1) + i)
                step2 = float(game_stats.battle_base_modifier) * step1
                modifier += step2

            dmg = math.ceil(dmg * modifier)

        elif dif < 0:  # Disadvantage

            for i in range(1, dif + 1):
                step1 = i / ((i - 1) + i)
                step2 = float(game_stats.battle_base_modifier) * step1
                modifier += step2 * -1

            dmg = math.floor(dmg / modifier)
            if dmg == 0:
                dmg = 1

        b.damage_msg_position = list(primary_target.position)

        if primary_target.crew[target].HP > 0:
            primary_target.crew[target].HP -= dmg

            if primary_target.crew[target].HP <= 0:
                # Target was determined before hit, it is possible that several creatures hit the same target
                # that has been already killed by previous shooters
                b.dealt_damage += (dmg + primary_target.crew[target].HP)
                b.killed_creatures += 1

                primary_target.crew[target].HP = 0

            else:
                b.dealt_damage += dmg


def perform_battle_actions():
    # print("perform_battle_actions")
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

            for army in game_obj.game_armies:
                if army.army_id in [b.attacker_id, b.defender_id]:
                    if army.owner == b.realm_in_control:
                        own_units = army.units
                        acting_unit = own_units[b.queue[0].number]
                        own_army_id = army.army_id
                    elif army.owner == b.enemy:

                        enemy_units = army.units
                        enemy_army_id = army.army_id
                        # print("b.enemy - " + str(b.enemy) + " army.army_id - " + str(army.army_id) +
                        #       " enemy_army_id - " + str(enemy_army_id))

            if b.realm_in_control != game_stats.player_power and b.AI_ready:
                battle_logic.manage_unit(b, own_units, enemy_units, acting_unit, own_army_id, enemy_army_id)

            execute_order(b)


def advance_battle_time(time_counted):
    for b in game_obj.game_battles:
        if b.attacker_realm == game_stats.player_power or \
                b.defender_realm == game_stats.player_power:

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
                        perform_battle_actions()


def melee_attack_preparation(b, TileNum, position, x2, y2):
    # x, y - coordinates of target
    x = position[0] % 96
    y = position[1] % 96
    print("x, y - " + str([x, y]))

    check = True

    if x < 32:
        if y < 32:
            word = "melee_attack_nw"
            approach = [x2 - 1, y2 - 1]
        elif 32 <= y < 64:
            word = "melee_attack_w"
            approach = [x2 - 1, y2]
        elif 64 <= y:
            word = "melee_attack_sw"
            approach = [x2 - 1, y2 + 1]
    elif 32 <= x < 64:
        if y < 32:
            word = "melee_attack_n"
            approach = [x2, y2 - 1]
        elif 32 <= y < 64:
            check = False
        elif 64 <= y:
            word = "melee_attack_s"
            approach = [x2, y2 + 1]
    elif 64 <= x < 96:
        if y < 32:
            word = "melee_attack_ne"
            approach = [x2 + 1, y2 - 1]
        elif 32 <= y < 64:
            word = "melee_attack_e"
            approach = [x2 + 1, y2]
        elif 64 <= y:
            word = "melee_attack_se"
            approach = [x2 + 1, y2 + 1]

    if check:
        ApproachTile = (approach[1] - 1) * game_stats.battle_width + approach[0] - 1
        print("ApproachTile is " + str(ApproachTile))

        if approach in b.movement_grid:

            b.attacking_rotate.append(b.queue[0].number)

            TileNum2 = (y2 - 1) * game_stats.battle_width + x2 - 1
            for army in game_obj.game_armies:
                if army.army_id == b.battle_map[TileNum2].army_id:
                    b.enemy_army_id = army.army_id
                    if not army.units[b.battle_map[TileNum2].unit_index].engaged:
                        army.units[b.battle_map[TileNum2].unit_index].engaged = True
                        b.defending_rotate.append(b.battle_map[TileNum2].unit_index)

                elif army.army_id == b.queue[0].army_id:
                    if not army.units[b.queue[0].number].engaged:
                        army.units[b.queue[0].number].engaged = True

            print("defending_rotate set to - " + str(b.defending_rotate))
            print("It's possible to approach from - " + str(approach))
            b.move_destination = [int(approach[0]), int(approach[1])]
            b.target_destination = [int(x2), int(y2)]
            action_order(b, "Move", "Melee attack")

        elif approach == b.queue[0].position:

            b.attacking_rotate.append(b.queue[0].number)

            TileNum2 = (y2 - 1) * game_stats.battle_width + x2 - 1
            for army in game_obj.game_armies:
                if army.army_id == b.battle_map[TileNum2].army_id:
                    b.enemy_army_id = army.army_id
                    if not army.units[b.battle_map[TileNum2].unit_index].engaged:
                        army.units[b.battle_map[TileNum2].unit_index].engaged = True
                        b.defending_rotate.append(b.battle_map[TileNum2].unit_index)

                elif army.army_id == b.queue[0].army_id:
                    if not army.units[b.queue[0].number].engaged:
                        army.units[b.queue[0].number].engaged = True

            print("attacking_rotate set to - " + str(b.attacking_rotate))
            print("defending_rotate set to - " + str(b.defending_rotate))
            print("Standing in same position - " + str(approach))
            b.target_destination = [int(x2), int(y2)]
            action_order(b, "Rotate", "Melee attack")


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
        print("Angle - " + str(facing_angle))

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
        for army in game_obj.game_armies:
            if army.army_id == b.battle_map[TileNum2].army_id:
                b.enemy_army_id = army.army_id

        b.target_destination = [int(x2), int(y2)]
        b.secondary = "Ranged attack"
        b.primary = "Rotate"


def armor_effect(primary_target):
    bonus = 0
    # print("armor_effect: len(primary_target.effects) - " + str(len(primary_target.effects)))
    if len(primary_target.effects) > 0:
        for e in primary_target.effects:
            for buff in e.buffs:
                if buff.application == "Armor":
                    if buff.method == "addition":
                        bonus = buff.quantity

    return bonus


def defence_effect(primary_target):
    bonus = 0
    # print("defence_effect: len(primary_target.effects) - " + str(len(primary_target.effects)))
    if len(primary_target.effects) > 0:
        for e in primary_target.effects:
            for buff in e.buffs:
                if buff.application == "Defence":
                    if buff.method == "addition":
                        bonus = buff.quantity

    return bonus


def addtional_attack_skill(unit):
    bonus = 0
    if len(unit.skills) > 0:
        for s in unit.skills:
            if s.application == "additional melee damage" and s.method == "Separate damage":
                bonus = s.quantity

    return bonus


def surrounded_by_enemy(b):
    for army in game_obj.game_armies:
        if army.army_id in [b.attacker_id, b.defender_id]:
            if army.owner == b.enemy:
                enemy_army_id = army.army_id

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
    print("Position - " + str(position))
    # If unit has died or left its position than all other units who were engaged in battle with it should disengage
    for xy in [[0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0]]:
        new_position = [position[0] + xy[0], position[1] + xy[1]]
        if 0 < new_position[0] <= game_stats.battle_width:
            if 0 < new_position[1] <= game_stats.battle_height:
                TileNum = (new_position[1] - 1) * game_stats.battle_width + new_position[0] - 1

                if b.battle_map[TileNum].army_id is not None:
                    check = ""
                    if xy[0] == 1:
                        if xy[1] == 1:
                            check = "NW"
                        elif xy[1] == 0:
                            check = "W"
                        elif xy[1] == -1:
                            check = "SW"
                    elif xy[0] == 0:
                        if xy[1] == 1:
                            check = "N"
                        elif xy[1] == -1:
                            check = "S"
                    elif xy[0] == -1:
                        if xy[1] == 1:
                            check = "NE"
                        elif xy[1] == 0:
                            check = "E"
                        elif xy[1] == -1:
                            check = "SE"

                    for army in game_obj.game_armies:
                        if army.army_id == b.battle_map[TileNum].army_id:
                            army.units[b.battle_map[TileNum].unit_index].engaged = False


def reduce_morale(b, primary_target, before_HP, angle):
    angle_modifier = {"Front right" : 100.0,
                      "Right flank" : 125.0,
                      "Rear right" : 150.0,
                      "Rear" : 150.0,
                      "Rear left" : 150.0,
                      "Left flank" : 125.0,
                      "Front left" : 100.0,
                      "Front" : 100.0,
                      "Ranged" : 100.0}

    total_HP = primary_target.rows * primary_target.number * primary_target.base_HP
    damage_fraction = (b.dealt_damage / 2) / before_HP + (b.dealt_damage / 2) / total_HP
    morale_hit = float(math.ceil(damage_fraction / game_stats.battle_base_morale_hit * angle_modifier[angle])) / 100
    print("angle_modifier - " + str(angle_modifier[angle]) + " damage_fraction - " + str(damage_fraction) +
          " morale_hit - " + str(morale_hit) + " b.dealt_damage - " + str(b.dealt_damage))
    primary_target.morale -= morale_hit
    primary_target.morale = float(int(primary_target.morale * 100)) / 100

    # if primary_target.morale < 0.0:
    #     primary_target.morale = 0.0


def routing_path(routing_unit):
    # First step - gather list of positions beyond the edge of battlefield
    exit_positions = []
    if routing_unit.owner == b.attacker_realm:
        for i in range (1, 13):
            exit_positions.append(17)

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
