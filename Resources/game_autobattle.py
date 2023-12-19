## Among Myth and Wonder
## game_autobattle

import math
import random

from Resources import game_classes
from Resources import game_stats
from Resources import game_basic
from Resources import game_obj
from Resources import algo_movement_range
from Resources import game_pathfinding

from Content import exploration_catalog
from Content import reward_catalog
from Content import battle_result_scripts

from Content.Quests import knight_lords_quest_result_scripts

from Strategy_AI import AI_battle_result_scripts
from Strategy_AI import strategy_logic


def begin_battle(attacker, defender, battle_type, battle_result_script):
    print("")
    print("game_autobattle - begin_battle")
    attacker_hero_bonus = 1.0
    attacker_action_bonus = 1.0
    attacker_action_level = 0
    attacker_troops_power_level_list = []

    defender_hero_bonus = 1.0
    defender_action_bonus = 1.0
    defender_action_level = 0
    defender_troops_power_level_list = []

    attacker_realm = None
    defender_realm = None
    for realm in game_obj.game_powers:
        if realm.name == attacker.owner:
            attacker_realm = realm
            print("attacker_realm - " + attacker_realm.name)
        elif realm.name == defender.owner:
            defender_realm = realm
            print("defender_realm - " + defender_realm.name)

    print("Attacker list")
    # print(str(attacker.hero))
    # Calculate attacker's power level
    if attacker.hero is not None:
        # print(attacker.hero.name)
        for skill in attacker.hero.skills:
            # print(skill.name)
            if skill.skill_level in ["Perk", "Basic"]:
                attacker_hero_bonus += 0.04
            elif skill.skill_level == "Advanced":
                attacker_hero_bonus += 0.08
            elif skill.skill_level == "Expert":
                attacker_hero_bonus += 0.12

            if skill.theme in ["Devine magic", "Elemental magic"]:
                if skill.skill_level == "Basic" and attacker_action_level < 1:
                    attacker_action_level = 1
                elif skill.skill_level == "Advanced" and attacker_action_level < 2:
                    attacker_action_level = 2
                elif skill.skill_level == "Expert" and attacker_action_level < 3:
                    attacker_action_level = 3

        for artifact in attacker.hero.inventory:
            for effect in artifact.effects:
                if effect.application == "Cast spells":
                    attacker_hero_bonus += 0.03
                elif effect.application == "Ability bonus Magic Power":
                    if effect.method == "addition":
                        attacker_action_bonus += 0.02
                    elif effect.method == "subtraction":
                        attacker_action_bonus -= 0.02
                elif effect.application == "Ability mana cost":
                    if effect.method == "addition":
                        attacker_action_bonus -= 0.02
                    elif effect.method == "subtraction":
                        attacker_action_bonus += 0.02
                elif effect.application == "Ability bonus initiative":
                    if effect.method == "addition":
                        attacker_action_bonus += 0.05
                    elif effect.method == "subtraction":
                        attacker_action_bonus -= 0.05
                elif effect.application == "Bonus leadership":
                    if effect.method == "addition":
                        attacker_hero_bonus += 0.04
                    elif effect.method == "subtraction":
                        attacker_hero_bonus -= 0.04

    attacker_hero_bonus = math.floor(attacker_hero_bonus * 100) / 100

    num = 0
    for unit in attacker.units:
        power_level = float((len(unit.crew) / (unit.number * unit.rows)) * unit.rank)
        power_bonus = 0.0
        bonus_leadership = 0.0

        if attacker.hero is not None:
            for package in attacker.hero.attributes_list:
                for attribute in package.attribute_list:
                    if attribute.tag in unit.reg_tags:
                        power_bonus += 0.07 * attribute.value

            for artifact in attacker.hero.inventory:
                for effect in artifact.effects:
                    for tag in effect.other_tags:
                        if tag in unit.reg_tags:
                            if effect.application in ["Initiative time reduction"]:
                                if effect.method == "subtraction":
                                    power_bonus += (effect.quantity / 0.05) * 0.03
                            else:
                                if effect.method == "addition":
                                    power_bonus += 0.1 * effect.quantity
                                elif effect.method == "subtraction":
                                    power_bonus -= 0.1 * effect.quantity

                            break

        if attacker.hero is not None:
            # Skills
            for skill in attacker.hero.skills:
                for effect in skill.effects:
                    if effect.application == "Bonus leadership":
                        if effect.method == "addition":
                            bonus_leadership += float(effect.quantity)

            # Artifacts
            if len(attacker.hero.inventory) > 0:
                for artifact in attacker.hero.inventory:
                    for effect in artifact.effects:
                        if effect.application == "Bonus leadership":
                            if effect.method == "addition":
                                bonus_leadership += float(effect.quantity)
                            elif effect.method == "subtraction":
                                bonus_leadership -= float(effect.quantity)

        morale = float(unit.base_leadership) + float(bonus_leadership)

        # print("attacker_hero_bonus - " + str(attacker_hero_bonus) + "; power_bonus - " + str(power_bonus))
        power_level = power_level * (attacker_hero_bonus + power_bonus)
        power_level = math.floor(power_level * 100) / 100
        attacker_troops_power_level_list.append(game_classes.Autobattle_Regiment_Card(num,
                                                                                      str(unit.name),
                                                                                      float(power_level),
                                                                                      float(power_level),
                                                                                      morale))

        print(str(num) + "; " + str(unit.name) + "; power_level - " + str(power_level) + "; morale - " + str(morale))
        num += 1

    print("Defender list")
    # Calculate defender's power level
    if defender.hero is not None:
        for skill in defender.hero.skills:
            if skill.skill_level in ["Perk", "Basic"]:
                defender_hero_bonus += 0.04
            elif skill.skill_level == "Advanced":
                defender_hero_bonus += 0.08
            elif skill.skill_level == "Expert":
                defender_hero_bonus += 0.12

            if skill.theme in ["Devine magic", "Elemental magic"]:
                if skill.skill_level == "Basic" and defender_action_level < 1:
                    defender_action_level = 1
                elif skill.skill_level == "Advanced" and defender_action_level < 2:
                    defender_action_level = 2
                elif skill.skill_level == "Expert" and defender_action_level < 3:
                    defender_action_level = 3

        for artifact in defender.hero.inventory:
            for effect in artifact.effects:
                if effect.application == "Cast spells":
                    defender_hero_bonus += 0.03
                elif effect.application == "Ability bonus Magic Power":
                    if effect.method == "addition":
                        defender_action_bonus += 0.02
                    elif effect.method == "subtraction":
                        defender_action_bonus -= 0.02
                elif effect.application == "Ability mana cost":
                    if effect.method == "addition":
                        defender_action_bonus -= 0.02
                    elif effect.method == "subtraction":
                        defender_action_bonus += 0.02
                elif effect.application == "Ability bonus initiative":
                    if effect.method == "addition":
                        defender_action_bonus += 0.05
                    elif effect.method == "subtraction":
                        defender_action_bonus -= 0.05
                elif effect.application == "Bonus leadership":
                    if effect.method == "addition":
                        defender_hero_bonus += 0.04
                    elif effect.method == "subtraction":
                        defender_hero_bonus -= 0.04

    defender_hero_bonus = math.floor(defender_hero_bonus * 100) / 100

    num = 0
    for unit in defender.units:
        power_level = float((len(unit.crew) / (unit.number * unit.rows)) * unit.rank)
        power_bonus = 0.0
        bonus_leadership = 0.0

        if defender.hero is not None:
            for package in defender.hero.attributes_list:
                for attribute in package.attribute_list:
                    if attribute.tag in unit.reg_tags:
                        power_bonus += 0.07 * attribute.value

            for artifact in defender.hero.inventory:
                for effect in artifact.effects:
                    for tag in effect.other_tags:
                        if tag in unit.reg_tags:
                            if effect.application in ["Initiative time reduction"]:
                                if effect.method == "subtraction":
                                    power_bonus += (effect.quantity / 0.05) * 0.03
                            else:
                                if effect.method == "addition":
                                    power_bonus += 0.1 * effect.quantity
                                elif effect.method == "subtraction":
                                    power_bonus -= 0.1 * effect.quantity

                            break

        if defender.hero is not None:
            # Skills
            for skill in defender.hero.skills:
                for effect in skill.effects:
                    if effect.application == "Bonus leadership":
                        if effect.method == "addition":
                            bonus_leadership += float(effect.quantity)

            # Artifacts
            if len(defender.hero.inventory) > 0:
                for artifact in defender.hero.inventory:
                    for effect in artifact.effects:
                        if effect.application == "Bonus leadership":
                            if effect.method == "addition":
                                bonus_leadership += float(effect.quantity)
                            elif effect.method == "subtraction":
                                bonus_leadership -= float(effect.quantity)

        morale = float(unit.base_leadership) + float(bonus_leadership)

        # print("defender_hero_bonus - " + str(defender_hero_bonus) + "; power_bonus - " + str(power_bonus))
        power_level = power_level * (defender_hero_bonus + power_bonus)
        power_level = math.floor(power_level * 100) / 100
        defender_troops_power_level_list.append(game_classes.Autobattle_Regiment_Card(num,
                                                                                      str(unit.name),
                                                                                      float(power_level),
                                                                                      float(power_level),
                                                                                      morale))

        print(str(num) + "; " + str(unit.name) + "; power_level - " + str(power_level) + "; morale - " + str(morale))
        num += 1

    # Calculate battle results
    result, exp_attackers, exp_defenders, \
        attacker_no_troops_left, \
        defender_no_troops_left, \
        attacker_troops_power_level_list, \
        defender_troops_power_level_list = play_battle(attacker_troops_power_level_list,
                                                       defender_troops_power_level_list, attacker_action_bonus,
                                                       defender_action_bonus, attacker_action_level,
                                                       defender_action_level, attacker.hero,
                                                       defender.hero, attacker, defender, battle_type)

    print("Battle result is " + str(result) + "; exp_attackers - " + str(exp_attackers) + "; exp_defenders -  " +
          str(exp_defenders))

    # print("After battle attacker_troops_power_level_list: " + str(len(attacker_troops_power_level_list)))
    # print("After battle defender_troops_power_level_list: " + str(len(defender_troops_power_level_list)))

    if result == "Attacker has won" and attacker.hero is not None:
        if attacker_realm.AI_player:
            game_basic.hero_next_level(attacker.hero, exp_defenders)
        else:
            attacker.hero.experience += int(exp_defenders)

    elif result == "Defender has won" and defender.hero is not None and battle_type != "special":
        if defender_realm.AI_player:
            game_basic.hero_next_level(defender.hero, exp_attackers)
        else:
            defender.hero.experience += int(exp_attackers)

    AI_battle = True
    if attacker_realm is not None:
        print(attacker_realm.name + " attacker_realm.AI_player - " + str(attacker_realm.AI_player))
        if not attacker_realm.AI_player:
            AI_battle = False
    if defender_realm is not None:
        print(defender_realm.name + " defender_realm.AI_player - " + str(defender_realm.AI_player))
        if not defender_realm.AI_player:
            AI_battle = False

    if not AI_battle:
        if attacker.owner != "Neutral":
            print(attacker_realm.name + " AI_player - " + str(attacker_realm.AI_player))
        if defender.owner != "Neutral":
            print(defender_realm.name + " AI_player - " + str(defender_realm.AI_player))

        game_stats.attacker_army = attacker
        game_stats.defender_army = defender
        game_stats.attacker_troops_power_level_list = attacker_troops_power_level_list
        game_stats.defender_troops_power_level_list = defender_troops_power_level_list
        game_stats.battle_type = battle_type
        game_stats.attacker_no_troops_left = attacker_no_troops_left
        game_stats.defender_no_troops_left = defender_no_troops_left

        game_stats.game_board_panel = "autobattle conclusion panel"
        # print("game_board_panel - " + game_stats.game_board_panel)

        if result == "Attacker has won":  # exp_attackers, exp_defenders
            game_stats.battle_result = "Attacker has won"
            if attacker.owner == game_stats.player_power:
                game_stats.result_statement = "Victory"
                game_stats.earned_experience = int(exp_defenders)
            else:
                game_stats.result_statement = "Defeat"
        elif result == "Defender has won":
            game_stats.battle_result = "Defender has won"
            if attacker.owner == game_stats.player_power:
                game_stats.result_statement = "Defeat"
                game_stats.earned_experience = int(exp_attackers)
            else:
                game_stats.result_statement = "Victory"
        elif result == "Draw":
            game_stats.battle_result = "Draw"
            game_stats.result_statement = "Draw"

    else:
        # There is no human player
        # Therefore proceed to after battle actions
        print("Input attacker_troops_power_level_list: " + str(len(attacker_troops_power_level_list)))
        print("Input defender_troops_power_level_list: " + str(len(defender_troops_power_level_list)))
        after_battle_processing(attacker, defender, attacker_troops_power_level_list, defender_troops_power_level_list,
                                attacker_realm, defender_realm, battle_type, attacker_no_troops_left,
                                defender_no_troops_left, result, battle_result_script)


def play_battle(attacker_troops_power_level_list, defender_troops_power_level_list, attacker_action_bonus,
                defender_action_bonus, attacker_action_level, defender_action_level, attacker_hero, defender_hero,
                attacker, defender, battle_type):
    result = ""
    keep_fighting = True
    attacker_no_troops_left = True
    defender_no_troops_left = True
    experience_for_defeated_attackers = 0
    experience_for_defeated_defenders = 0

    settlement = None
    if battle_type == "Siege":
        for city in game_obj.game_cities:
            if city.city_id == game_obj.game_map[defender.location].city_id:
                settlement = city
                break

    while keep_fighting:
        print("")
        print("New round of autobattle")
        attacker_pl_sum = 0.0
        defender_pl_sum = 0.0

        for card in attacker_troops_power_level_list:
            if card.status == "Fighting":
                attacker_pl_sum += card.power_level
                # print("attacker_pl_sum - " + str(attacker_pl_sum) + "; card.power_level - " + str(card.power_level))

        for card in defender_troops_power_level_list:
            if card.status == "Fighting":
                defender_pl_sum += card.power_level
                # print("defender_pl_sum - " + str(defender_pl_sum) + "; card.power_level - " + str(card.power_level))

        attacker_pl_sum = math.floor(attacker_pl_sum * 100) / 100
        defender_pl_sum = math.floor(defender_pl_sum * 100) / 100

        print("Total attacker_pl_sum from regiments - " + str(attacker_pl_sum))
        print("Total defender_pl_sum from regiments - " + str(defender_pl_sum))

        attacker_random_ratio = math.floor((1.0 + (random.randint(-30, 30) / 100)) * 100) / 100
        defender_random_ratio = math.floor((1.0 + (random.randint(-30, 30) / 100)) * 100) / 100
        attacker_pl_sum = math.floor(((attacker_pl_sum / 6) * attacker_random_ratio) * 100) / 100
        defender_pl_sum = math.floor(((defender_pl_sum / 6) * defender_random_ratio) * 100) / 100
        print("attacker_random_ratio - " + str(attacker_random_ratio) + "; round attacker_pl_sum - " +
              str(attacker_pl_sum))
        print("defender_random_ratio - " + str(defender_random_ratio) + "; round defender_pl_sum - " +
              str(defender_pl_sum))

        if attacker_hero is not None:
            if attacker_action_level == 0:
                attacker_pl_sum += 0.4
            else:
                required_mana = 0
                if attacker_action_level == 1:
                    required_mana = 4
                elif attacker_action_level == 2:
                    required_mana = random.randint(4, 6)
                else:
                    required_mana = random.randint(6, 8)
                if attacker_hero.mana_reserve >= required_mana:
                    attacker_hero.mana_reserve -= int(required_mana)
                    attacker_pl_sum += float(attacker_action_bonus * attacker_action_level)
                    print("attacker_action_bonus  - " + str(attacker_action_bonus) + "; attacker_action_level  - " +
                          str(attacker_action_level))
                else:
                    attacker_pl_sum += 0.4

        if defender_hero is not None:
            if defender_action_level == 0:
                defender_pl_sum += 0.4
            else:
                required_mana = 0
                if defender_action_level == 1:
                    required_mana = 4
                elif defender_action_level == 2:
                    required_mana = random.randint(4, 6)
                else:
                    required_mana = random.randint(6, 8)
                if defender_hero.mana_reserve >= required_mana:
                    defender_hero.mana_reserve -= int(required_mana)
                    defender_pl_sum += float(defender_action_bonus * defender_action_level)
                else:
                    defender_pl_sum += 0.4

        attacker_pl_sum = math.floor(attacker_pl_sum * 100) / 100
        defender_pl_sum = math.floor(defender_pl_sum * 100) / 100
        print("attacker_pl_sum with hero - " + str(attacker_pl_sum))
        print("defender_pl_sum with hero - " + str(defender_pl_sum))

        if battle_type == "Siege":
            defender_pl_sum = defence_structures_power_level_bonus(defender_pl_sum, defender_troops_power_level_list,
                                                                   settlement)
            print("Siege: defender_pl_sum with defences - " + str(defender_pl_sum))

        attacker_unit_damage_sum = 0.0
        defender_unit_damage_sum = 0.0

        for card in attacker_troops_power_level_list:
            if card.status == "Routed" or card.power_level == 0:
                card.receiving_damage = 0.0
            else:
                card.receiving_damage = 1.0 + (random.randint(-50, 50) / 100)
                attacker_unit_damage_sum += float(card.receiving_damage)

        for card in defender_troops_power_level_list:
            if card.status == "Routed" or card.power_level == 0:
                card.receiving_damage = 0.0
            else:
                card.receiving_damage = 1.0 + (random.randint(-50, 50) / 100)
                defender_unit_damage_sum += float(card.receiving_damage)

        attacker_unit_damage_sum = math.floor(attacker_unit_damage_sum * 100) / 100
        defender_unit_damage_sum = math.floor(defender_unit_damage_sum * 100) / 100

        print("attacker_unit_damage_sum - " + str(attacker_unit_damage_sum))
        print("defender_unit_damage_sum - " + str(defender_unit_damage_sum))

        for card in attacker_troops_power_level_list:
            if card.status != "Routed" and card.power_level > 0:
                if card.status == "Routing":
                    escape = random.randint(1, 100)
                    if escape <= 50:
                        card.status = "Routed"

                damage = math.floor(((card.receiving_damage / attacker_unit_damage_sum) * defender_pl_sum)
                                    * 100) / 100
                current_pl = float(card.power_level)
                card.power_level -= float(damage)
                if card.power_level < 0.0:
                    card.power_level = 0.0
                else:
                    card.power_level = math.floor(card.power_level * 100) / 100

                # print(card.name + ": current_pl - " + str(current_pl) + "; damage - " + str(damage) +
                #       "; card.power_level - " + str(card.power_level) + "; status - " + str(card.status))

                # print(str(card.index) + " starting_power_level - " + str(card.starting_power_level) +
                #       "; current_pl - " + str(current_pl))
                damage_part_1 = (damage / 2) / current_pl
                damage_part_1 = math.floor(damage_part_1 * 1000) / 1000
                damage_part_2 = (damage / 2) / card.starting_power_level
                damage_part_2 = math.floor(damage_part_2 * 1000) / 1000
                damage_fraction = damage_part_1 + damage_part_2
                damage_fraction = math.floor(damage_fraction * 1000) / 1000
                morale_hit = float(math.ceil(damage_fraction / game_stats.battle_base_morale_hit))
                card.morale = float(int((card.morale - morale_hit) * 100)) / 100
                # print("damage - " + str(damage) + "; damage_part_1 - " + str(damage_part_1) + "; damage_part_2 - " +
                #       str(damage_part_2) + "; damage_fraction - " + str(damage_fraction) +
                #       "; battle_base_morale_hit - " + str(game_stats.battle_base_morale_hit) + "; morale_hit - " +
                #       str(morale_hit) + "; card.morale - " + str(card.morale))
                if card.morale < 0.0:
                    card.status = "Routing"
                    # print(card.name + " " + str(card.index) + " is routing")

        for card in defender_troops_power_level_list:
            if card.status != "Routed" and card.power_level > 0:
                if card.status == "Routing":
                    escape = random.randint(1, 100)
                    if escape <= 50:
                        card.status = "Routed"

                damage = math.floor(((card.receiving_damage / defender_unit_damage_sum) * attacker_pl_sum)
                                    * 100) / 100
                current_pl = float(card.power_level)
                card.power_level -= float(damage)
                if card.power_level < 0.0:
                    card.power_level = 0.0
                else:
                    card.power_level = math.floor(card.power_level * 100) / 100

                # print(card.name + ": current_pl - " + str(current_pl) + "; damage - " + str(damage) +
                #       "; card.power_level - " + str(card.power_level) + "; status - " + str(card.status))

                damage_part_1 = (damage / 2) / current_pl
                damage_part_1 = math.floor(damage_part_1 * 1000) / 1000
                damage_part_2 = (damage / 2) / card.starting_power_level
                damage_part_2 = math.floor(damage_part_2 * 1000) / 1000
                damage_fraction = damage_part_1 + damage_part_2
                damage_fraction = math.floor(damage_fraction * 1000) / 1000
                morale_hit = float(math.ceil(damage_fraction / game_stats.battle_base_morale_hit))
                card.morale = float(int((card.morale - morale_hit) * 100)) / 100
                if card.morale < 0.0:
                    card.status = "Routing"
                    # print(card.name + " " + str(card.index) + " is routing")

        attacker_no_troops_left = True
        defender_no_troops_left = True

        for card in attacker_troops_power_level_list:
            if card.status == "Fighting" and card.power_level > 0.0:
                attacker_no_troops_left = False
                break

        for card in defender_troops_power_level_list:
            if card.status == "Fighting" and card.power_level > 0.0:
                defender_no_troops_left = False
                break

        if attacker_no_troops_left or defender_no_troops_left:
            # Battle ending
            keep_fighting = False

            # Remove creatures and gain experience
            for card in attacker_troops_power_level_list:
                # print("Attacker - " + str(card.name))
                regiment = attacker.units[card.index]
                total_hp = int(len(regiment.crew) * regiment.base_HP)
                # print("starting_power_level - " + str(card.starting_power_level) +
                #       "; power_level - " + str(card.power_level))
                total_damage = int(math.floor((card.starting_power_level - card.power_level) /
                                              card.starting_power_level * total_hp))
                # print("total_hp - " + str(total_hp) + "; total_damage - " + str(total_damage))
                while total_damage > 0:
                    if total_damage >= regiment.base_HP:
                        # print("len(regiment.crew) - " + str(len(regiment.crew)))
                        experience_for_defeated_attackers += int(regiment.rank)
                        regiment.cemetery.append(regiment.crew[-1])
                        del regiment.crew[-1]
                    total_damage -= regiment.base_HP

            for card in defender_troops_power_level_list:
                regiment = defender.units[card.index]
                total_hp = int(len(regiment.crew) * regiment.base_HP)
                total_damage = int(math.floor((card.starting_power_level - card.power_level) /
                                              card.starting_power_level * total_hp))
                while total_damage > 0:
                    if total_damage >= regiment.base_HP:
                        experience_for_defeated_defenders += int(regiment.rank)
                        regiment.cemetery.append(regiment.crew[-1])
                        del regiment.crew[-1]
                    total_damage -= regiment.base_HP

    if attacker_no_troops_left and defender_no_troops_left:
        result = "Draw"
    elif not attacker_no_troops_left and defender_no_troops_left:
        result = "Attacker has won"

    elif attacker_no_troops_left and not defender_no_troops_left:
        result = "Defender has won"

    print("result - " + result + "; attacker_no_troops_left - " + str(attacker_no_troops_left) +
          "; defender_no_troops_left - " + str(defender_no_troops_left))

    # print("attacker_troops_power_level_list: " + str(len(attacker_troops_power_level_list)))
    # print("defender_troops_power_level_list: " + str(len(defender_troops_power_level_list)))

    return result, experience_for_defeated_attackers, experience_for_defeated_defenders, attacker_no_troops_left, \
        defender_no_troops_left, attacker_troops_power_level_list, defender_troops_power_level_list


def after_battle_processing(attacker, defender, attacker_troops_power_level_list, defender_troops_power_level_list,
                            attacker_realm, defender_realm, battle_type, attacker_no_troops_left,
                            defender_no_troops_left, result, battle_result_script):
    print("")
    print("attacker_no_troops_left - " + str(attacker_no_troops_left))
    print("defender_no_troops_left - " + str(defender_no_troops_left))
    # if attacker_realm is not None:
    #     print("Attacking realm - " + attacker_realm.name + "; AI_player - " + str(attacker_realm.AI_player))
    # else:
    #     print("Attacking is None")
    remove_army_id = []

    # Remove regiments
    unit_list = []
    # print("attacker_troops_power_level_list: " + str(attacker_troops_power_level_list))
    for card in attacker_troops_power_level_list:
        # print("Attacker - " + str(card.name))
        regiment = attacker.units[card.index]

        if len(regiment.crew) == 0:
            unit_list.append(card.index)

    unit_list = sorted(unit_list, reverse=True)

    # print("attacker unit_list: " + str(unit_list))
    for ind in unit_list:
        del attacker.units[ind]
    game_basic.establish_leader(attacker.army_id, "Game")

    if len(attacker.units) == 0:
        remove_army_id.append(int(attacker.army_id))

    unit_list = []
    for card in defender_troops_power_level_list:
        regiment = defender.units[card.index]
        # print("Defender - " + str(card.name) + " " + str(regiment.crew))

        if len(regiment.crew) == 0:
            unit_list.append(card.index)

    unit_list = sorted(unit_list, reverse=True)

    # print("defender unit_list: " + str(unit_list))
    for ind in unit_list:
        del defender.units[ind]
    game_basic.establish_leader(defender.army_id, "Game")

    if len(defender.units) == 0:
        remove_army_id.append(int(defender.army_id))

    attacker_posxy = list(attacker.posxy)
    defender_posxy = list(defender.posxy)

    # print("attacker.action - " + attacker.action)
    # print("defender.action - " + defender.action)

    attacker.action = "Stand"
    defender.action = "Stand"

    # Routing
    if attacker is not None and attacker_no_troops_left:
        if attacker.shattered == "Stable":
            attacker.shattered = "Shattered"

        friendly_cities = []
        hostile_cities = []
        at_war_list = []
        known_map = []

        if attacker.owner != "Neutral":
            known_map = attacker_realm.known_map
            friendly_cities, hostile_cities, at_war_list = game_pathfinding.find_friendly_cities(attacker_realm.name)
        else:
            known_map = game_stats.map_positions

        routing_path, routing_grid = algo_movement_range.range_astar(None, attacker_posxy, 600.0, friendly_cities,
                                                                     hostile_cities, known_map, True, [])

        if len(routing_grid) > 0:
            farthest_tile = None
            biggest_distance = 0.0
            for tile in routing_grid:
                distance = math.sqrt(((tile[0] - defender_posxy[0]) ** 2) + ((tile[1] - defender_posxy[1]) ** 2))
                if farthest_tile is None:
                    farthest_tile = list(tile)
                    biggest_distance = float(distance)

                elif distance > biggest_distance:
                    farthest_tile = list(tile)
                    biggest_distance = float(distance)

            print("Attacker routing: farthest_tile - " + str(farthest_tile) + " biggest_distance - " +
                  str(biggest_distance))

            for node in routing_path:
                if node.position == farthest_tile:
                    print("node.position - " + str(node.position) + " and farthest_tile - " + str(farthest_tile))
                    pathway = []
                    current = node
                    while current is not None:
                        pathway.append(current.position)
                        current = current.parent

                    print("Final unreversed path is " + str(pathway))
                    attacker.route = list(pathway[::-1])
                    attacker.route = attacker.route[1:]
                    print("Final reversed path is " + str(attacker.route))
                    attacker.action = "Routing"

        else:
            attacker.action = "Stand"

    if defender is not None and defender_no_troops_left and battle_type not in ["special"] \
            and not attacker_no_troops_left:
        # [not attacker_no_troops_left] is here in case of draw the defending army shouldn't route
        if defender.shattered == "Shattered":
            # Defeated shattered army should be destroyed
            if defender.army_id not in remove_army_id:  # Could have been added before
                remove_army_id.append(int(defender.army_id))

        elif defender.shattered == "Stable":
            defender.shattered = "Shattered"

            friendly_cities = []
            hostile_cities = []
            at_war_list = []
            known_map = []

            if defender.owner != "Neutral":
                known_map = defender_realm.known_map
                friendly_cities, hostile_cities, at_war_list = game_pathfinding.find_friendly_cities(defender_realm.name)
            else:
                known_map = game_stats.map_positions

            routing_path, routing_grid = algo_movement_range.range_astar(None, defender_posxy, 600.0, friendly_cities,
                                                                         hostile_cities, known_map, True, [])

            if len(routing_grid) > 0:
                farthest_tile = None
                biggest_distance = 0.0
                for tile in routing_grid:
                    distance = math.sqrt(((tile[0] - attacker_posxy[0]) ** 2) + ((tile[1] - attacker_posxy[1]) ** 2))
                    if farthest_tile is None:
                        farthest_tile = list(tile)
                        biggest_distance = float(distance)

                    elif distance > biggest_distance:
                        farthest_tile = list(tile)
                        biggest_distance = float(distance)

                print("Defender routing: farthest_tile - " + str(farthest_tile) + " biggest_distance - " +
                      str(biggest_distance))

                for node in routing_path:
                    if node.position == farthest_tile:
                        print("node.position - " + str(node.position) + " and farthest_tile - " + str(farthest_tile))
                        pathway = []
                        current = node
                        while current is not None:
                            pathway.append(current.position)
                            current = current.parent

                        print("Final unreversed path is " + str(pathway))
                        defender.route = list(pathway[::-1])
                        defender.route = defender.route[1:]
                        print("Final reversed path is " + str(defender.route))
                        defender.action = "Routing"

            else:
                defender.action = "Stand"

    if not attacker_no_troops_left and defender_no_troops_left:
        # Defender is defeated; draw doesn't count
        if defender.owner == "Neutral":
            print(defender.owner + " army id - " + str(defender.army_id) + " is defeated")
            if defender.army_id not in remove_army_id:  # Could have been added before
                remove_army_id.append(int(defender.army_id))

            if game_obj.game_map[defender.location].lot is not None:
                if game_obj.game_map[defender.location].lot != "City":
                    # Removing army ID from exploration object if it was an event battle
                    if game_obj.game_map[
                        defender.location].lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                        if game_obj.game_map[defender.location].lot.properties.army_id == defender.army_id:
                            game_obj.game_map[defender.location].lot.properties.army_id = None

    settlement = None
    if game_obj.game_map[defender.location].city_id:
        for city in game_obj.game_cities:
            if city.city_id == game_obj.game_map[defender.location].city_id:
                settlement = city
                break

    if settlement:
        if settlement.siege:
            settlement.siege = None

    settlement_captured = False
    if battle_type in ["Siege", "Sortie"]:
        if result == "Attacker has won":
            # If attacking army wins siege battle, then defending army gets destroyed
            if defender.army_id not in remove_army_id:  # Could have been added before
                remove_army_id.append(int(defender.army_id))
            settlement_captured = True

    # Battle victories score
    if result != "Draw":
        for war in game_obj.game_wars:
            if war.initiator in [attacker.owner, defender.owner]:
                if war.respondent in [attacker.owner, defender.owner]:
                    if result == "Attacker has won":
                        if war.initiator == attacker.owner:
                            war.initiator_battle_victories += 1
                        else:
                            war.respondent_battle_victories += 1
                    else:
                        if war.initiator == attacker.owner:
                            war.respondent_battle_victories += 1
                        else:
                            war.initiator_battle_victories += 1
                    break

    # Removing destroyed armies
    if len(remove_army_id) > 0:
        # print("after_battle_processing() - # Removing destroyed armies ")
        # Removing army ID from location
        for id_item in remove_army_id:
            if id_item == attacker.army_id:
                if game_obj.game_map[attacker.location].army_id == attacker.army_id:
                    game_obj.game_map[attacker.location].army_id = None

            elif id_item == defender.army_id:
                if game_obj.game_map[defender.location].army_id == defender.army_id:
                    game_obj.game_map[defender.location].army_id = None

        # Delete army
        game_basic.remove_army(remove_army_id)

    if attacker:
        if attacker.owner != "Neutral":
            strategy_logic.complete_war_order(attacker, attacker_realm)

    if defender:
        if defender.owner != "Neutral":
            strategy_logic.complete_war_order(defender, defender_realm)

    # Special battles (lairs)
    if result == "Attacker has won" and battle_type == "special":
        if attacker_realm.AI_player:
            print("Attacking army - " + str(attacker.army_id) + " owned by " + str(attacker.owner))
            print("battle_result_script - " + str(battle_result_script))
            AI_battle_result_scripts.result_scripts[battle_result_script](attacker, attacker_realm)
            print("AI player " + attacker_realm.name + " has received its reward")
            game_stats.battle_result = ""

        else:
            special_autobattle_result(attacker)

    # Quest battles
    if result == "Attacker has won" and defender.event is not None:
        if attacker_realm.AI_player:
            quest_autobattle_result(attacker, attacker_realm, defender)

        else:
            quest_autobattle_result(attacker, attacker_realm, defender)

    if settlement_captured:
        winner_alive = True
        if attacker_no_troops_left:
            winner_alive = False
        game_basic.capture_settlement(settlement, attacker_realm.name, winner_alive, attacker)


def special_autobattle_result(winner_army):
    game_stats.reward_id_counter += 1
    game_obj.game_rewards.append(reward_catalog.reward_scripts[game_stats.battle_result_script](winner_army))

    for reward in game_obj.game_rewards:
        if reward[0] == game_stats.reward_id_counter:
            game_stats.reward_for_demonstration = list(reward[1])
            break

    for realm in game_obj.game_powers:
        if realm.name == winner_army.owner:
            realm.reward_IDs.append(int(game_stats.reward_id_counter))
            break

    battle_result_scripts.result_scripts[game_stats.battle_result_script](winner_army)


def quest_autobattle_result(winner, attacker_realm, loser):
    print("quest_autobattle_result: Event name - " + loser.event.name)
    if loser.event.name in knight_lords_quest_result_scripts.result_scripts:
        knight_lords_quest_result_scripts.result_scripts[loser.event.name](winner, attacker_realm, loser.event)


def defence_structures_power_level_bonus(defender_pl_sum, defender_troops_power_level_list, settlement):
    # In siege battle intact defence structures provide power level bonus
    number_of_rams = int(settlement.siege.battering_rams_ready)
    number_of_siege_towers = int(settlement.siege.siege_towers_ready)

    number_of_fighting_regiments = 0
    for card in defender_troops_power_level_list:
        if card.status == "Fighting":
            number_of_fighting_regiments += 1

    number_of_gates = 0
    number_of_walls = 0
    number_of_barriers = 0
    for structure in settlement.defences:
        for def_obj in structure.def_objects:
            if def_obj.section_type in ["Wall", "Tower"]:
                if def_obj.state == "Unbroken":
                    number_of_walls += 1
            elif def_obj.section_type == "Gate":
                if def_obj.state == "Unbroken":
                    number_of_gates += 1
            elif def_obj.section_type == "Barrier":
                number_of_barriers += 1

    if number_of_rams > 0:
        number_of_gates = 0

    if number_of_walls - number_of_siege_towers < 0:
        number_of_walls = 0
    else:
        number_of_walls -= number_of_siege_towers

    number_of_walls += number_of_gates
    print("number_of_walls - " + str(number_of_walls))

    if number_of_barriers >= number_of_fighting_regiments:
        defender_pl_sum *= 1.1
    else:
        defender_pl_sum = defender_pl_sum * (1 + 0.1 * (number_of_barriers / number_of_fighting_regiments))

    if number_of_walls >= number_of_fighting_regiments:
        defender_pl_sum *= 1.25
    else:
        defender_pl_sum = defender_pl_sum * (1 + 0.25 * (number_of_walls / number_of_fighting_regiments))

    defender_pl_sum = math.floor(defender_pl_sum * 100) / 100

    return defender_pl_sum
