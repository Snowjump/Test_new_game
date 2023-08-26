## Miracle battles!

import random
import math

from Resources import game_obj
from Resources import game_stats
from Resources import update_gf_game_board

from Content import siege_warfare_catalog
from Content import unit_alignment_catalog


def advance_siege(settlement, siege):
    TileObj = game_obj.game_map[settlement.location]
    at_army = None
    df_army = None
    for army in game_obj.game_armies:
        if army.army_id == siege.attacker_id:
            at_army = army
        elif army.army_id == TileObj.army_id:
            df_army = army

    siege.siege_log = []

    siege_machinery_construction(at_army, siege)

    trebuchet_attack(siege, settlement, at_army)

    supplies_attrition(df_army, siege.supplies, siege.siege_log, TileObj)

    siege_attrition(at_army, df_army, siege.siege_log, TileObj)

    siege.time_passed += 1
    if siege.supplies > 0:
        siege.supplies -= 1

    at_army_perished = False
    df_army_perished = False

    if df_army is not None:
        if len(df_army.units) == 0:
            df_army_perished = True
    if len(at_army.units) == 0:
        at_army_perished = True

    if at_army_perished:
        game_obj.game_map[at_army.location].army_id = None
        # print("1. len(game_obj.game_armies): " + str(len(game_obj.game_armies)))
        game_obj.game_armies.remove(at_army)
        # print("2. len(game_obj.game_armies): " + str(len(game_obj.game_armies)))
        # Close siege window
        game_stats.attacker_army_id = 0
        game_stats.attacker_realm = ""
        game_stats.defender_army_id = 0
        game_stats.defender_realm = ""
        game_stats.blockaded_settlement_name = ""
        game_stats.selected_object = ""
        game_stats.selected_army = -1
        settlement.siege = None

        if game_stats.game_board_panel == "settlement blockade panel":
            game_stats.selected_settlement = -1
            game_stats.game_board_panel = ""

        if df_army_perished:
            game_obj.game_map[df_army.location].army_id = None
            game_obj.game_armies.remove(df_army)
        else:
            if df_army is not None:
                df_army.action = "Stand"

    else:
        if df_army_perished:
            game_obj.game_map[df_army.location].army_id = None
            game_obj.game_armies.remove(df_army)

            if settlement.owner == "Neutral":
                at_army.action = "Stand"

                settlement.siege = None

                settlement.owner = str(at_army.owner)

                if game_stats.game_board_panel == "settlement blockade panel":
                    game_stats.attacker_army_id = 0
                    game_stats.attacker_realm = ""
                    game_stats.defender_army_id = 0
                    game_stats.defender_realm = ""
                    game_stats.blockaded_settlement_name = ""

                    game_stats.selected_settlement = -1
                    game_stats.game_board_panel = ""

                    game_stats.selected_object = ""
                    game_stats.selected_army = -1
                    game_stats.selected_second_army = -1
                    game_stats.details_panel_mode = ""
                    game_stats.first_army_exchange_list = []
                    game_stats.second_army_exchange_list = []

                    # Update visuals
                    update_gf_game_board.update_settlement_misc_sprites()


def siege_machinery_construction(the_army, siege):
    construction_points = 0
    for unit in the_army.units:
        alignment = unit_alignment_catalog.alignment_dict[unit.name]
        capacity_list = siege_warfare_catalog.units_siege_dict_by_alignment[alignment][unit.name]
        construction_points += len(unit.crew) * capacity_list[2]

    if the_army.hero is not None:
        multiplication_bonus_list = []
        for skill in the_army.hero.skills:
            for effect in skill.effects:
                if effect.application == "Siege construction points":
                    if effect.method == "multiplication":
                        multiplication_bonus_list.append(float(effect.quantity))

        if len(multiplication_bonus_list) > 0:
            print("construction_points before skill - " + str(construction_points))
            for bonus in multiplication_bonus_list:
                construction_points *= bonus
            construction_points = int(math.ceil(construction_points))
            print("construction_points after skill - " + str(construction_points))

    if len(siege.construction_orders) > 0:
        constructed_trebuchets = 0
        constructed_siege_towers = 0
        constructed_battering_rams = 0
        while construction_points > 0:
            if len(siege.construction_orders) > 0:
                construction_points_required = 0
                if siege.construction_orders[0][0] == "Trebuchet":
                    construction_points_required += 160 - siege.construction_orders[0][1]
                elif siege.construction_orders[0][0] == "Siege tower":
                    construction_points_required += 160 - siege.construction_orders[0][1]
                elif siege.construction_orders[0][0] == "Battering ram":
                    construction_points_required += 80 - siege.construction_orders[0][1]

                if construction_points >= construction_points_required:
                    construction_points -= construction_points_required
                    if siege.construction_orders[0][0] == "Trebuchet":
                        siege.trebuchets_ordered -= 1
                        siege.trebuchets_ready += 1
                        constructed_trebuchets += 1
                        del siege.construction_orders[0]
                    elif siege.construction_orders[0][0] == "Siege tower":
                        siege.siege_towers_ordered -= 1
                        siege.siege_towers_ready += 1
                        constructed_siege_towers += 1
                        del siege.construction_orders[0]
                    elif siege.construction_orders[0][0] == "Battering ram":
                        siege.battering_rams_ordered -= 1
                        siege.battering_rams_ready += 1
                        constructed_battering_rams += 1
                        del siege.construction_orders[0]
                else:
                    siege.construction_orders[0][1] += int(construction_points)
                    construction_points = 0
            else:
                construction_points = 0

        if constructed_trebuchets == 1:
            siege.siege_log.append("Trebuchet has been constructed")
        elif constructed_trebuchets > 1:
            siege.siege_log.append(str(constructed_trebuchets) + " trebuchets have been constructed")

        if constructed_siege_towers == 1:
            siege.siege_log.append("Siege tower has been constructed")
        elif constructed_siege_towers > 1:
            siege.siege_log.append(str(constructed_siege_towers) + " siege towers have been constructed")

        if constructed_battering_rams == 1:
            siege.siege_log.append("Battering ram has been constructed")
        elif constructed_battering_rams > 1:
            siege.siege_log.append(str(constructed_battering_rams) + " battering rams have been constructed")


def trebuchet_attack(siege, settlement, the_army):
    performing_trebuchets = int(siege.trebuchets_ready)
    destructible_structures = []
    attack = 4

    if the_army.hero is not None:
        addition_bonus_list = []
        for skill in the_army.hero.skills:
            for effect in skill.effects:
                if effect.application == "Trebuchet attack":
                    if effect.method == "addition":
                        addition_bonus_list.append(float(effect.quantity))

        if len(addition_bonus_list) > 0:
            for bonus in addition_bonus_list:
                attack += bonus
            attack = int(attack)

    print("Trebuchet attack level - " + str(attack))

    for structure in settlement.defences:
        num = 0
        for def_obj in structure.def_objects:
            if def_obj.state in ["Unbroken", "Opened"]:
                destructible_structures.append([structure.name, num, def_obj.section_name])
            num += 1

    while performing_trebuchets > 0:
        performing_trebuchets -= 1
        if len(destructible_structures) > 0:
            chosen_obj = random.choice(destructible_structures)

            # For trebuchet results between 1 and 4 are successfully destroy section of defensive structure
            result = random.randint(1, attack + siege_warfare_catalog.hardness_table[chosen_obj[0]])
            print("Trebuchet attack result is " + str(result))
            if result <= attack:
                for structure in settlement.defences:
                    if structure.name == chosen_obj[0]:
                        structure.def_objects[chosen_obj[1]].state = "Broken"
                        break
                siege.siege_log.append("Trebuchet has destroyed " + chosen_obj[2].lower())
                destructible_structures.remove(chosen_obj)


def supplies_attrition(df_army, supplies, siege_log, TileObj):
    if supplies == 0:
        result = random.randint(1, 100)
        if result <= 40:
            # Defending army suffer attrition from hunger
            total_casualties = 0
            empty_regiment_index = []
            empty_index = 0
            # Lethality - chance for every creature to die from attrition
            lethality = random.randint(10, 25)  # 10-25

            for unit in df_army.units:
                dead_index = []
                num = 0
                for creature in unit.crew:
                    death_roll = random.randint(1, 100)
                    if death_roll <= lethality:
                        dead_index.append(num)
                        total_casualties += 1
                    num += 1

                dead_index.reverse()
                for index in dead_index:
                    del unit.crew[index]

                if len(unit.crew) == 0:
                    empty_regiment_index.append(empty_index)

                empty_index += 1

            empty_regiment_index.reverse()
            for index in empty_regiment_index:
                del df_army.units[index]

            # if len(df_army.units) == 0:
            #     TileObj.army_id = None
            #     print("1. len(game_obj.game_armies): " + str(len(game_obj.game_armies)))
            #     game_obj.game_armies.remove(df_army)
            #     print("2. len(game_obj.game_armies): " + str(len(game_obj.game_armies)))

            siege_log.append("Casualties from lack of supplies: " + str(total_casualties))


def siege_attrition(at_army, df_army, siege_log, TileObj):
    if len(df_army.units) > 0:
        result = random.randint(1, 12)
        if result == 1:
            # Defending army suffer attrition from siege warfare
            total_casualties = 0
            empty_regiment_index = []
            empty_index = 0
            upper_limit = 20
            lower_limit = 10

            if df_army.hero is not None:
                subtraction_bonus_list = []
                for skill in df_army.hero.skills:
                    for effect in skill.effects:
                        if effect.application == "Siege attrition":
                            if effect.method == "subtraction":
                                subtraction_bonus_list.append(float(effect.quantity))

                if len(subtraction_bonus_list) > 0:
                    for bonus in subtraction_bonus_list:
                        upper_limit = int(upper_limit - bonus)
                        lower_limit = int(lower_limit - bonus)

                    print("Defending army lower_limit - " + str(lower_limit) + ", upper_limit - " + str(upper_limit))

            # Lethality - chance for every creature to die from attrition
            lethality = random.randint(lower_limit, upper_limit)

            for unit in df_army.units:
                dead_index = []
                num = 0
                for creature in unit.crew:
                    death_roll = random.randint(1, 100)
                    if death_roll <= lethality:
                        dead_index.append(num)
                        total_casualties += 1
                    num += 1

                dead_index.reverse()
                for index in dead_index:
                    del unit.crew[index]

                if len(unit.crew) == 0:
                    empty_regiment_index.append(empty_index)

                empty_index += 1

            empty_regiment_index.reverse()
            for index in empty_regiment_index:
                del df_army.units[index]

            siege_log.append("Casualties among defenders from attrition: " + str(total_casualties))

    result = random.randint(1, 12)
    if result == 1:
        # Attacking army suffer attrition from siege warfare
        total_casualties = 0
        empty_regiment_index = []
        empty_index = 0
        upper_limit = 20
        lower_limit = 10

        if at_army.hero is not None:
            subtraction_bonus_list = []
            for skill in at_army.hero.skills:
                for effect in skill.effects:
                    if effect.application == "Siege attrition":
                        if effect.method == "subtraction":
                            subtraction_bonus_list.append(float(effect.quantity))

            if len(subtraction_bonus_list) > 0:
                for bonus in subtraction_bonus_list:
                    upper_limit = int(upper_limit - bonus)
                    lower_limit = int(lower_limit - bonus)

                print("Attacking army lower_limit - " + str(lower_limit) + ", upper_limit - " + str(upper_limit))

        # Lethality - chance for every creature to die from attrition
        lethality = random.randint(lower_limit, upper_limit)

        for unit in at_army.units:
            dead_index = []
            num = 0
            for creature in unit.crew:
                death_roll = random.randint(1, 100)
                if death_roll <= lethality:
                    dead_index.append(num)
                    total_casualties += 1
                num += 1

            dead_index.reverse()
            for index in dead_index:
                del unit.crew[index]

            if len(unit.crew) == 0:
                empty_regiment_index.append(empty_index)

            empty_index += 1

        empty_regiment_index.reverse()
        for index in empty_regiment_index:
            del at_army.units[index]

        siege_log.append("Casualties among attackers from attrition: " + str(total_casualties))
