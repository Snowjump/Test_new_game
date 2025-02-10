## Among Myth and Wonder
## battle_skills

import math

from Resources import effect_classes
from Resources import game_classes
from Resources import game_stats


def additional_damage_skill(unit):
    bonus = 0
    if len(unit.skills) > 0:
        for s in unit.skills:
            if s.application == "additional melee damage" and s.method == "Separate damage":
                bonus = s.quantity

    return bonus


def penetration_skill(unit, armor_value, attack_type, dmg):
    excess_armour = int(armor_value)
    final_dmg = int(dmg)
    penetration_value = 0
    used_penetration = -0
    if len(unit.skills) > 0:
        for s in unit.skills:
            if s.application == "penetration":
                # print("s.application == penetration")
                # print(str(s.skill_tags))
                for skill_tag in s.skill_tags:
                    # print("skill_tag - " + str(skill_tag))
                    if skill_tag == attack_type:
                        penetration_value += s.quantity
                        # print("skill_tag == attack_type - " + str(attack_type))
                        break

    if final_dmg - excess_armour < 1:
        excess_armour = excess_armour - final_dmg + 1
        final_dmg = 1
    else:
        final_dmg -= excess_armour
        excess_armour = 0

    if final_dmg + penetration_value > dmg:
        penetration_value = penetration_value - (dmg - final_dmg)
        used_penetration = int(dmg - final_dmg)
        final_dmg = int(dmg)
    else:
        final_dmg += penetration_value
        used_penetration = int(penetration_value)
        penetration_value = 0

    return final_dmg, excess_armour, penetration_value, used_penetration


def charge_dmg_bonus(b, unit, dmg, primary_target, queue, primary):
    charge_defence = []
    crushed_status = False
    crush_denied = False
    if len(primary_target.skills) > 0:
        for s in primary_target.skills:
            if s.application == "charge defence":
                charge_defence = list(s.skill_tags)
                print("Charge defence: " + str(charge_defence))
                break

    # Effects on defender tile
    TileNum = (primary_target.position[1] - 1) * game_stats.battle_width + primary_target.position[0] - 1
    if b.battle_map[TileNum].map_object:
        if b.battle_map[TileNum].map_object.obj_type == "Structure":
            print(b.battle_map[TileNum].map_object.obj_name)
            for effect in b.battle_map[TileNum].map_object.properties.effects:
                if effect.application == "Crush denied":
                    if check_direction(unit, primary_target, effect.directions):
                        crush_denied = True
                        print("crush_denied - " + str(crush_denied))

    new_dmg = int(dmg)
    # print(str(unit.name) + " has " + str(len(unit.skills)) + " skills")
    if len(unit.skills) > 0 and primary != "Counterattack" and not crush_denied and b.attack_name != "Hit and fly":
        # print("More than one skill")
        for s in unit.skills:
            if (s.quality == "Heavy charge" or s.quality == "Light charge") and s.quality not in charge_defence:
                # print("Perform - " + str(s.quality))
                if len(s.keep_details) == 0:
                    # Target position, current time, current position
                    # s.keep_details = [[int(primary_target.position[0]), int(primary_target.position[1])],
                    #                   float(queue[0].time_act),
                    #                   [int(unit.position[0]), int(unit.position[1])]]
                    new_dmg = math.ceil(dmg * (1 + s.quantity))
                    crushed_status = True
                    # print("0. Heavy charge - " + str(new_dmg))
                elif primary_target.position == s.keep_details[0]:
                    if unit.position == s.keep_details[2]:
                        # print(str(queue[0].time_act))
                        # print(str(s.keep_details[1]))
                        # print("queue[0].time_act - s.keep_details[1] = ? "
                        #       + str(queue[0].time_act) + " - " + str(s.keep_details[1]) + " = "
                        #       + str(queue[0].time_act - s.keep_details[1]))
                        if (queue[0].time_act - s.keep_details[1]) <= 1.0:
                            pass
                        else:
                            # s.keep_details = [[int(primary_target.position[0]), int(primary_target.position[1])],
                            #                   float(queue[0].time_act),
                            #                   [int(unit.position[0]), int(unit.position[1])]]
                            new_dmg = math.ceil(dmg * (1 + s.quantity))
                            crushed_status = True
                            # print("Heavy charge - " + str(new_dmg))

                    else:
                        # s.keep_details = [[int(primary_target.position[0]), int(primary_target.position[1])],
                        #                   float(queue[0].time_act),
                        #                   [int(unit.position[0]), int(unit.position[1])]]
                        new_dmg = math.ceil(dmg * (1 + s.quantity))
                        crushed_status = True
                        # print("Heavy charge - " + str(new_dmg))

                else:
                    # s.keep_details = [[int(primary_target.position[0]), int(primary_target.position[1])],
                    #                   float(queue[0].time_act),
                    #                   [int(unit.position[0]), int(unit.position[1])]]
                    new_dmg = math.ceil(dmg * (1 + s.quantity))
                    crushed_status = True
                    # print("Heavy charge - " + str(new_dmg))

    if crushed_status:

        info_card = None
        for card in queue:
            if card.position == primary_target.position and card.obj_type == "Regiment":
                info_card = card
                break

        add_crush = True
        if len(primary_target.effects) > 0:
            for effect in primary_target.effects:
                if effect.name == "Crushed":

                    for eff_card in queue:
                        if eff_card.position == primary_target.position and eff_card.obj_type == "Effect" \
                                and eff_card.title == "Crushed":
                            if eff_card.time_act == float(queue[0].time_act + 1.0):
                                add_crush = False
                            else:
                                queue.remove(eff_card)
                            break

                    if add_crush:
                        primary_target.effects.remove(effect)

                    break

        if add_crush:
            queue.append(game_classes.Queue_Card(float(queue[0].time_act + 1.0), "Effect", info_card.army_id,
                                                 info_card.owner, info_card.number, info_card.position,
                                                 "Icons", "eff", info_card.f_color, info_card.s_color,
                                                 4, 14, 0, 0, "Crushed"))

            primary_target.effects.append(effect_classes.Battle_Effect("Crushed", True,
                                                                       float(queue[0].time_act),
                                                                       float(queue[0].time_act + 1.0),
                                                                       [effect_classes.Buff("Armor", 2,
                                                                                            "division", None),
                                                                        effect_classes.Buff("Defence", 2,
                                                                                            "division", None),
                                                                        effect_classes.Buff("Melee mastery", 2,
                                                                                            "division", None)]))

    return new_dmg


def charge_track(unit, primary_target, queue):
    # Record information about last performed charge
    if len(unit.skills) > 0:
        # print("More than one skill")
        for s in unit.skills:
            if s.quality == "Heavy charge" or s.quality == "Light charge":
                # print("Perform - " + str(s.quality))
                if len(s.keep_details) == 0:
                    # Target position, current time, current position
                    s.keep_details = [[int(primary_target.position[0]), int(primary_target.position[1])],
                                      float(queue[0].time_act),
                                      [int(unit.position[0]), int(unit.position[1])]]
                elif primary_target.position == s.keep_details[0]:
                    if unit.position == s.keep_details[2]:
                        if (queue[0].time_act - s.keep_details[1]) <= 1.0:
                            pass
                        else:
                            s.keep_details = [[int(primary_target.position[0]), int(primary_target.position[1])],
                                              float(queue[0].time_act),
                                              [int(unit.position[0]), int(unit.position[1])]]

                    else:
                        s.keep_details = [[int(primary_target.position[0]), int(primary_target.position[1])],
                                          float(queue[0].time_act),
                                          [int(unit.position[0]), int(unit.position[1])]]

                else:
                    s.keep_details = [[int(primary_target.position[0]), int(primary_target.position[1])],
                                      float(queue[0].time_act),
                                      [int(unit.position[0]), int(unit.position[1])]]


def passive_charge_track(unit):
    # Record information about unit’s position for charge skill
    if len(unit.skills) > 0:
        # print("More than one skill")
        for s in unit.skills:
            if s.quality == "Heavy charge" or s.quality == "Light charge":
                # print("Perform - " + str(s.quality))
                # Target position, current time, current position
                s.keep_details = [[int(-10), int(-10)],
                                  float(-10),
                                  [int(unit.position[0]), int(unit.position[1])]]


def simple_dmg_bonus(unit, primary_target, dmg):
    final_dmg = dmg
    multiplication_bonus_list = []
    if len(unit.skills) > 0:
        for s in unit.skills:
            if s.application == "increase damage in melee":
                weakness = False
                for skill_tag in s.skill_tags:
                    if skill_tag in primary_target.reg_tags:
                        weakness = True
                        break
                if weakness:
                    if s.method == "Multiplication":
                        multiplication_bonus_list.append(s.quantity)

        if len(multiplication_bonus_list) > 0:
            for multiplication in multiplication_bonus_list:
                final_dmg *= float(multiplication)

            final_dmg = int(math.ceil(final_dmg))
            print("Multiplied damage is " + str(final_dmg))

    return final_dmg


def big_shields_bonus(primary_target, division_bonus_list):
    if len(primary_target.skills) > 0:
        for s in primary_target.skills:
            if s.application == "missile protection":
                if s.method == "Division":
                    division_bonus_list.append(float(s.quantity))

    return division_bonus_list


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
