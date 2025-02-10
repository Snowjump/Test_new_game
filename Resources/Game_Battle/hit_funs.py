## Among Myth and Wonder
## hit_funs

import math
import random

from Resources import game_stats
from Resources import game_battle
from Resources import battle_skills


def melee_hit(b, at_creature, unit, primary_target, target, acting_hero, enemy_hero):
    s = unit.attacks[b.attack_type_index]

    min_dmg, max_dmg = game_battle.damage_value(s, acting_hero, unit)
    # print("min_dmg, max_dmg " + str(min_dmg) + ", " + str(max_dmg))
    dmg = random.randint(min_dmg, max_dmg)
    print("Random damage - " + str(dmg))
    dmg = battle_skills.charge_dmg_bonus(b, unit, dmg, primary_target, b.queue, b.primary)
    dmg = battle_skills.simple_dmg_bonus(unit, primary_target, dmg)
    print("Damage after skills bonuses - " + str(dmg))

    # armor = battle_skills.penetration_skill(unit, primary_target.armor)
    # total_defence = int(armor + primary_target.defence)
    # total_defence += armor_effect(primary_target) + defence_effect(primary_target)
    armour = armour_effect(b, unit, primary_target, primary_target.armour, acting_hero, enemy_hero)
    print("Armour - " + str(armour))
    dmg, excess_armour, excess_penetration, used_penetration = battle_skills.penetration_skill(unit, armour,
                                                                                               s.attack_type, dmg)
    print("Damage - " + str(dmg) + "; excess_armour - " + str(excess_armour) +
          "; excess_penetration - " + str(excess_penetration))
    defence = defence_effect(primary_target, primary_target.defence, enemy_hero)
    total_attack = melee_assault_effect(b, int(s.mastery), acting_hero, unit, primary_target)
    additional_damage = battle_skills.additional_damage_skill(unit)

    dif = total_attack - defence

    modifier = 1.0

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

    dmg, excess_armour, excess_penetration = excess_armour_penetration(dmg, excess_armour, excess_penetration,
                                                                       used_penetration)

    base_dmg = int(dmg)
    dmg += int(additional_damage)
    print("Melee attack by " + str(unit.name) + " with " +
          "mastery - " + str(total_attack) + ", defence - " + str(defence) + ", damage - " + str(base_dmg) +
          ", damage with additional bonus - " + str(dmg))
    # print("len(primary_target.crew) - " + str(len(primary_target.crew)) + " target - " + str(target))
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

    # print("Crew size left - " + str(len(primary_target.crew)))
    if len(primary_target.crew) == 0:
        game_battle.kill_unit(b, primary_target)


def ranged_hit(b, unit, primary_target, target, acting_hero, enemy_hero):
    s = unit.attacks[b.attack_type_index]

    distance = (math.sqrt(((primary_target.position[0] - unit.position[0]) ** 2) + (
            (primary_target.position[1] - unit.position[1]) ** 2)))

    successful_hit = True
    # Base accuracy of 50 could be lowered if enemy regiment is not full
    accuracy = math.ceil(50 * len(primary_target.crew) / (primary_target.rows * primary_target.number))

    total_attack = shooting_effect(int(s.mastery), acting_hero, unit, primary_target, b)

    # total_attack = int(s.mastery)
    # total_attack = battle_skills.big_shields_bonus(primary_target, int(total_attack))
    print("Mastery - " + str(s.mastery) + ", total attack - " + str(total_attack))
    # total_attack = cover_aura(unit, primary_target, int(total_attack), b)

    range_msg = " at effective range"
    if distance <= b.cur_effective_range:
        # Everything is good, creature hit with maximum accuracy and with full strength
        print("distance - " + str(distance) + " is within b.cur_effective_range - " + str(b.cur_effective_range))
        pass
    else:
        range_msg = " at far range"
        # total_attack = math.ceil(total_attack / 2)  # Will test without this modifier
        # Accuracy: base is 50 if enemy regiment is full
        # After effective range it declines
        print("base accuracy - " + str(accuracy))
        print("distance - " + str(distance) + "; b.cur_effective_range - " + str(b.cur_effective_range) +
              "; b.cur_range_limit - " + str(b.cur_range_limit))
        accuracy += math.ceil(50 * (distance - b.cur_effective_range) / (b.cur_range_limit - b.cur_effective_range))
        print("modified by range accuracy - " + str(accuracy))
        shot_dice = random.randint(1, 100)
        accuracy = accuracy_effect(b, accuracy, acting_hero, unit)
        if shot_dice <= accuracy:
            successful_hit = True
        else:
            successful_hit = False

    dmg = random.randint(s.min_dmg, s.max_dmg)
    base_dmg = int(dmg)
    print("Random damage - " + str(dmg))
    armour = armour_effect(b, unit, primary_target, primary_target.armour, acting_hero, enemy_hero)
    print("Armour - " + str(armour))
    dmg, excess_armour, excess_penetration, used_penetration = battle_skills.penetration_skill(unit, armour,
                                                                                               s.attack_type, dmg)
    print("Damage - " + str(dmg) + "; excess_armour - " + str(excess_armour) +
          "; excess_penetration - " + str(excess_penetration))

    total_defence = ranged_base_defence(distance, primary_target)
    total_defence += ranged_defence_effect(primary_target, enemy_hero)

    dif = total_attack - total_defence
    print("dif is " + str(dif) + ", total_attack - " + str(total_attack) + ", total_defence - " + str(total_defence))

    modifier = 1.0

    if successful_hit:
        # Target was hit by this creature
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
                modifier += step2  # * -1
                # print("i - " + str(i) + ", step1 - " + str(step1) + ", step2 - " + str(step2)
                #       + ", modifier - " + str(modifier))

            # print("dmg - " + str(dmg) + ", modifier - " + str(modifier))
            dmg = math.floor(dmg / modifier)
            if dmg == 0:
                dmg = 1

        dmg, excess_armour, excess_penetration = excess_armour_penetration(dmg, excess_armour, excess_penetration,
                                                                           used_penetration)

        b.damage_msg_position = list(primary_target.position)

        print(str(target) + ") "
              + "HP - " + str(primary_target.crew[target].HP) + ", damage - " + str(dmg)
              + ", killed - " + str(b.killed_creatures))
        if primary_target.crew[target].HP > 0:
            # base_dmg = int(dmg)
            base_HP = int(primary_target.crew[target].HP)

            # already_dead = False
            # if primary_target.crew[target].HP <= 0:
            #     already_dead = True
            primary_target.crew[target].HP -= dmg

            print("Ranged attack by " + str(unit.name) + range_msg + " with " +
                  "mastery - " + str(total_attack) + ", total defence - " + str(total_defence) + ", base damage - "
                  + str(base_dmg) + ", damage with skills - " + str(dmg)
                  + ", initial HP - " + str(base_HP) + ", final HP - " + str(primary_target.crew[target].HP))

            if primary_target.crew[target].HP <= 0:
                # Target was determined before hit, it is possible that several creatures hit the same target
                # that has been already killed by previous shooters
                b.dealt_damage += (dmg + primary_target.crew[target].HP)
                # if not already_dead:
                b.killed_creatures += 1
                print("Another creature is killed, total - " + str(b.killed_creatures))

                primary_target.crew[target].HP = 0

            else:
                b.dealt_damage += dmg


def excess_armour_penetration(dmg, excess_armour, excess_penetration, used_penetration):
    if excess_armour:
        used_penetration += int(excess_penetration)
        if excess_armour - excess_penetration < 0:
            excess_armour = 0
        else:
            excess_armour -= excess_penetration

        if dmg - excess_armour < 1:
            dmg = 1
        else:
            dmg -= excess_armour

        if dmg < used_penetration:
            dmg = int(used_penetration)

    return dmg, excess_armour, excess_penetration


def armour_effect(b, unit, primary_target, base_armour, acting_hero, enemy_hero):
    final_armour = int(base_armour)
    addition_bonus_list = []
    subtraction_bonus_list = []
    division_bonus_list = []
    # print("armor_effect: len(primary_target.effects) - " + str(len(primary_target.effects)))
    if len(primary_target.effects) > 0:
        for e in primary_target.effects:
            for buff in e.buffs:
                if buff.application == "Armour":
                    if buff.method == "addition":
                        # bonus = buff.quantity
                        addition_bonus_list.append(buff.quantity)
                    elif buff.method == "division":
                        division_bonus_list.append(buff.quantity)

    # Hero skills and battle attributes
    if enemy_hero:
        # Attributes
        if len(enemy_hero.attributes_list) > 0:
            for pack in enemy_hero.attributes_list:
                for a in pack.attribute_list:
                    if a.stat == "armour":
                        if a.tag in primary_target.reg_tags:
                            addition_bonus_list.append(a.value)

        # Artifacts
        if len(enemy_hero.inventory) > 0:
            for artifact in enemy_hero.inventory:
                for effect in artifact.effects:
                    if effect.application == "Armour":
                        allowed = True
                        if len(effect.other_tags) > 0:
                            allowed = False
                            for tag in effect.other_tags:
                                if tag in primary_target.reg_tags:
                                    allowed = True
                                    break
                        if allowed:
                            if effect.method == "addition":
                                addition_bonus_list.append(effect.quantity)

    if acting_hero:
        # Skills
        for s in acting_hero.skills:
            for effect in s.effects:
                if effect.application == "Bonus armour penetration":
                    if b.attack_type_in_use in effect.skill_tags:
                        permitted = False
                        for tag in effect.other_tags:
                            if tag in unit.reg_tags:
                                permitted = True
                                break
                        if permitted:
                            if effect.method == "addition":
                                subtraction_bonus_list.append(effect.quantity)

    if len(addition_bonus_list) > 0:
        for addition in addition_bonus_list:
            final_armour += int(addition)

    if len(subtraction_bonus_list) > 0:
        for subtraction in subtraction_bonus_list:
            final_armour -= int(subtraction)

    if len(division_bonus_list) > 0:
        for division in division_bonus_list:
            final_armour /= int(division)

        final_armour = int(math.floor(final_armour))

    if final_armour < 0:
        print("Armour below zero - " + str(final_armour))
        final_armour = 0

    # print("Base armour - " + str(base_armour) + ", final armour - " + str(final_armour))
    return final_armour


def defence_effect(primary_target, base_defence, enemy_hero):
    final_defence = int(base_defence)
    addition_bonus_list = []
    subtraction_bonus_list = []
    division_bonus_list = []
    multiplication_bonus_list = []
    # print("defence_effect: len(primary_target.effects) - " + str(len(primary_target.effects)))
    # Effects
    if len(primary_target.effects) > 0:
        for e in primary_target.effects:
            for buff in e.buffs:
                if buff.application == "Defence":
                    if buff.method == "addition":
                        # bonus = buff.quantity
                        addition_bonus_list.append(buff.quantity)
                    elif buff.method == "division":
                        division_bonus_list.append(buff.quantity)

    # Hero skills and battle attributes
    if enemy_hero:
        # print("Defence bonus provided by " + str(enemy_hero.name))
        # Skills
        for s in enemy_hero.skills:
            for effect in s.effects:
                if effect.application == "Defence":
                    if effect.method == "multiplication":
                        multiplication_bonus_list.append(effect.quantity)

        # Attributes
        if len(enemy_hero.attributes_list) > 0:
            for pack in enemy_hero.attributes_list:
                for a in pack.attribute_list:
                    if a.stat == "defence":
                        if a.tag in primary_target.reg_tags:
                            addition_bonus_list.append(a.value)

        # Hero artifacts
        if len(enemy_hero.inventory) > 0:
            for artifact in enemy_hero.inventory:
                for effect in artifact.effects:
                    if effect.application == "Defence":
                        appropriate_unit = False
                        if len(effect.other_tags) > 0:
                            for unit_tag in primary_target.reg_tags:
                                if unit_tag in effect.other_tags:
                                    appropriate_unit = True
                        else:
                            appropriate_unit = True

                        if appropriate_unit:
                            if effect.method == "addition":
                                addition_bonus_list.append(int(effect.quantity))
                            elif effect.method == "subtraction":
                                subtraction_bonus_list.append(int(effect.quantity))

    if len(addition_bonus_list) > 0:
        for addition in addition_bonus_list:
            final_defence += int(addition)

    if len(subtraction_bonus_list) > 0:
        for addition in addition_bonus_list:
            final_defence -= int(addition)
            if final_defence < 0:
                final_defence = int(0)

    if len(multiplication_bonus_list) > 0:
        for multiplication in multiplication_bonus_list:
            final_defence *= float(multiplication)
            print("Testing: final_defence - " + str(final_defence))

    if len(division_bonus_list) > 0:
        for division in division_bonus_list:
            final_defence /= float(division)

    if final_defence > base_defence:
        final_defence = int(math.ceil(final_defence))
    elif final_defence < base_defence:
        final_defence = int(math.floor(final_defence))
    else:
        final_defence = int(final_defence)

    # print("base_defence - " + str(base_defence) + " => "
    #       + "final_defence - " + str(final_defence))
    return final_defence


def ranged_defence_effect(primary_target, enemy_hero):
    addition_bonus_list = []
    # Effects
    if len(primary_target.effects) > 0:
        for e in primary_target.effects:
            for buff in e.buffs:
                if buff.application == "Missile defence":
                    if buff.method == "addition":
                        addition_bonus_list.append(buff.quantity)

    final_defence = 0
    if len(addition_bonus_list) > 0:
        for addition in addition_bonus_list:
            final_defence += int(addition)

    # print("final_defence against ranged attack - " + str(final_defence))
    return final_defence


def melee_assault_effect(b, base_attack_mastery, acting_hero, unit, primary_target):
    final_attack_mastery = int(base_attack_mastery)
    addition_bonus_list = []
    subtraction_bonus_list = []
    division_bonus_list = []
    multiplication_bonus_list = []

    # Effects on attacker
    if len(unit.effects) > 0:
        for e in unit.effects:
            for buff in e.buffs:
                if buff.application == "Melee mastery":
                    if buff.method == "addition":
                        # bonus = buff.quantity
                        addition_bonus_list.append(buff.quantity)
                    elif buff.method == "division":
                        division_bonus_list.append(buff.quantity)

    # Attack type
    non_physical = True
    element = None
    for tag in unit.attacks[b.attack_type_index].tags:
        if tag == "Physical":
            non_physical = False
        elif tag == "Fire":
            element = tag

    # Physical and elemental attacks
    if non_physical:
        increase_mastery = True
        for skill in primary_target.skills:
            if skill.application == "Resistance":
                if element in skill.skill_tags:
                    increase_mastery = False
                    if skill.method == "division":
                        division_bonus_list.append(skill.quantity)
                    break
        if increase_mastery:
            multiplication_bonus_list.append(1.5)

    # Effects on defender tile
    TileNum = (primary_target.position[1] - 1) * game_stats.battle_width + primary_target.position[0] - 1
    if b.battle_map[TileNum].map_object:
        if b.battle_map[TileNum].map_object.obj_type == "Structure":
            # print(b.battle_map[TileNum].map_object.obj_name)
            for effect in b.battle_map[TileNum].map_object.properties.effects:
                if effect.application == "Incoming attack":
                    if game_battle.check_direction(unit, primary_target, effect.directions):
                        if effect.method == "division":
                            division_bonus_list.append(effect.quantity)

    if acting_hero:
        # Hero skills
        print(str(acting_hero.name))
        for s in acting_hero.skills:
            for effect in s.effects:
                if effect.application == "Melee":
                    if effect.method == "multiplication":
                        multiplication_bonus_list.append(effect.quantity)

        # Attributes
        if len(acting_hero.attributes_list) > 0:
            for pack in acting_hero.attributes_list:
                for a in pack.attribute_list:
                    if a.stat == "melee mastery":
                        if a.tag in unit.reg_tags:
                            addition_bonus_list.append(a.value)

        # Hero artifacts
        if len(acting_hero.inventory) > 0:
            for artifact in acting_hero.inventory:
                for effect in artifact.effects:
                    if effect.application == "Melee mastery":
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

    if len(addition_bonus_list) > 0:
        for addition in addition_bonus_list:
            final_attack_mastery += int(addition)

    if len(subtraction_bonus_list) > 0:
        for subtraction in subtraction_bonus_list:
            final_attack_mastery -= int(subtraction)
            if final_attack_mastery < 0:
                final_attack_mastery = 0

    if len(multiplication_bonus_list) > 0:
        for multiplication in multiplication_bonus_list:
            final_attack_mastery *= float(multiplication)

    if len(division_bonus_list) > 0:
        for division in division_bonus_list:
            final_attack_mastery /= float(division)

    if final_attack_mastery > base_attack_mastery:
        final_attack_mastery = int(math.ceil(final_attack_mastery))
    elif final_attack_mastery < base_attack_mastery:
        final_attack_mastery = int(math.floor(final_attack_mastery))
    else:
        final_attack_mastery = int(final_attack_mastery)

    # print("melee assault: base_attack_mastery - " + str(base_attack_mastery) + " => "
    #       + "final_attack_mastery - " + str(final_attack_mastery))
    return final_attack_mastery


def shooting_effect(base_attack_mastery, acting_hero, unit, primary_target, b):
    final_attack_mastery = int(base_attack_mastery)
    addition_bonus_list = []
    subtraction_bonus_list = []
    division_bonus_list = []
    multiplication_bonus_list = []

    if len(primary_target.skills) > 0:
        for s in primary_target.skills:
            # print("name - " + str(s.name) + ", method - " + str(s.method) +
            #       ", application - " + str(s.application) + ", quantity - " + str(s.quantity))
            if s.application == "missile protection":
                if s.method == "Division":
                    division_bonus_list.append(float(s.quantity))
                    print("skill: division_bonus_list - " + str(division_bonus_list))

    if acting_hero:
        # Hero skills
        print(str(acting_hero.name))
        for s in acting_hero.skills:
            for effect in s.effects:
                if effect.application == "Ranged":
                    if effect.method == "multiplication":
                        multiplication_bonus_list.append(effect.quantity)

        # Attributes
        if len(acting_hero.attributes_list) > 0:
            for pack in acting_hero.attributes_list:
                for a in pack.attribute_list:
                    if a.stat == "ranged mastery":
                        if a.tag in unit.reg_tags:
                            addition_bonus_list.append(a.value)

    division_bonus_list = cover_aura(unit, primary_target, division_bonus_list, b)
    # print("cover: division_bonus_list - " + str(division_bonus_list))
    # Obsolete skill check
    # division_bonus_list = battle_skills.big_shields_bonus(primary_target, division_bonus_list)

    if len(addition_bonus_list) > 0:
        for addition in addition_bonus_list:
            final_attack_mastery += int(addition)

    if len(subtraction_bonus_list) > 0:
        for subtraction in subtraction_bonus_list:
            final_attack_mastery -= int(subtraction)
            if final_attack_mastery < 0:
                final_attack_mastery = 0

    if len(multiplication_bonus_list) > 0:
        for multiplication in multiplication_bonus_list:
            final_attack_mastery *= float(multiplication)

    # print("final: division_bonus_list - " + str(division_bonus_list))
    if len(division_bonus_list) > 0:
        for division in division_bonus_list:
            final_attack_mastery /= float(division)

    if final_attack_mastery > base_attack_mastery:
        final_attack_mastery = int(math.ceil(final_attack_mastery))
    elif final_attack_mastery < base_attack_mastery:
        final_attack_mastery = int(math.floor(final_attack_mastery))
    else:
        final_attack_mastery = int(final_attack_mastery)

    # print("shooting: base_attack_mastery - " + str(base_attack_mastery) + " => "
    #       + "final_attack_mastery - " + str(final_attack_mastery))
    return final_attack_mastery


def accuracy_effect(b, base_accuracy, acting_hero, unit):
    final_accuracy = int(base_accuracy)
    addition_bonus_list = []

    if acting_hero is not None:
        # Hero skills
        # print(str(acting_hero.name))
        for s in acting_hero.skills:
            for effect in s.effects:
                if effect.application == "Bonus accuracy":
                    if b.attack_type_in_use in effect.skill_tags:
                        permitted = False
                        for tag in effect.other_tags:
                            if tag in unit.reg_tags:
                                permitted = True
                                break
                        if permitted:
                            if effect.method == "addition":
                                addition_bonus_list.append(effect.quantity)

    if len(addition_bonus_list) > 0:
        for addition in addition_bonus_list:
            final_accuracy += int(addition)

    # print("shooting at far range: base_accuracy - " + str(base_accuracy) + " => "
    #       + "final_accuracy - " + str(final_accuracy))
    return final_accuracy


def cover_aura(unit, primary_target, division_bonus_list, b):
    # final_attack = attack_value
    division_bonus_list = division_bonus_list

    TileNum = (primary_target.position[1] - 1) * game_stats.battle_width + primary_target.position[0] - 1
    ShooterTileNum = (unit.position[1] - 1) * game_stats.battle_width + unit.position[0] - 1

    if len(b.battle_map[TileNum].aura_effects) > 0:
        for aura in b.battle_map[TileNum].aura_effects:
            if aura[0] == b.battle_map[TileNum].army_id:
                if aura[2] == "Missile cover":
                    target_distance_sq = ((unit.position[0] - primary_target.position[0]) ** 2) \
                                         + ((unit.position[1] - primary_target.position[1]) ** 2)
                    protector_distance_sq = ((unit.position[0] - primary_target.position[0]) ** 2) \
                                            + ((unit.position[1] - primary_target.position[1]) ** 2)
                    if target_distance_sq < protector_distance_sq:
                        division_bonus_list.append(2.0)

            if aura[2] == "Medium fortification cover":
                apply_cover_effect = True
                if len(b.battle_map[ShooterTileNum].aura_effects) > 0:
                    for aura2 in b.battle_map[ShooterTileNum].aura_effects:
                        if aura2[2] in ["Medium fortification cover", "Light fortification cover"]:
                            apply_cover_effect = False
                            break

                if apply_cover_effect:
                    division_bonus_list.append(2.0)

            if aura[2] == "Light fortification cover":
                apply_cover_effect = True
                if len(b.battle_map[ShooterTileNum].aura_effects) > 0:
                    for aura2 in b.battle_map[ShooterTileNum].aura_effects:
                        if aura2[2] in ["Medium fortification cover", "Light fortification cover"]:
                            apply_cover_effect = False
                            break

                if apply_cover_effect:
                    division_bonus_list.append(1.33)

        # if len(division_bonus_list) > 0:
        #     for division in division_bonus_list:
        #         final_attack /= float(division)

        # final_attack = int(math.floor(final_attack))
        # print("Modified attack by cover is " + str(final_attack))

    # return final_attack
    return division_bonus_list


def ranged_base_defence(distance, primary_target):
    base_value = distance / 2
    for s in primary_target.skills:
        if s.name == "Fly":
            base_value *= 1.25
            break
    base_defence = int(math.ceil(base_value))
    return base_defence
