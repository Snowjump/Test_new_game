## Among Myth and Wonder
## economy_logic

import random
import copy

from Resources import game_stats
from Resources import game_obj
from Resources import game_basic
from Resources import game_classes
from Resources import artifact_classes
from Resources import algo_building
from Resources import skill_classes
from Resources import update_gf_game_board
from Resources import common_selects
from Resources import common_transactions

from Resources.Game_Hero import common_hero_funs

from Content import production_methods
from Content import unit_alignment_catalog
from Content import unit_rank_catalog
from Content import new_heroes_catalog
from Content import starting_skills
from Content import hero_skill_catalog
from Content import artifact_assortment
from Content import artifact_catalog
from Content import skills_curriculum
from Content import battle_attributes_assortment

from Storage import create_unit

from Strategy_AI import strategy_AI_classes
from Strategy_AI import hero_archetypes
from Strategy_AI import archetype_skill_weights


def manage_economy(player):
    economy = player.AI_cogs.economy_cogs
    if economy.new_round:
        economy.florins_income = 0
        economy.food_income = 0
        economy.wood_income = 0
        economy.metals_income = 0
        economy.stone_income = 0
        economy.ingredients_income = 0
        economy.armament_income = 0
        economy.tools_income = 0
        # ~~~#
        economy.florins_expenses = 0
        economy.food_expenses = 0
        economy.wood_expenses = 0
        economy.metals_expenses = 0
        economy.stone_expenses = 0
        economy.ingredients_expenses = 0
        economy.armament_expenses = 0
        economy.tools_expenses = 0
    # fa - factual amount
    # ea - expected amount
    settlements_fa = 0
    small_armies_ea = 0  # Int(1)
    medium_armies_ea = 0  # Int(2)
    large_armies_ea = 0  # Int(3)
    LUOS = []  # list of locations of unoccupied own settlements

    for settlement in game_obj.game_cities:
        if settlement.owner == player.name:
            settlements_fa += 1
            if settlement.military_occupation is None:
                small_armies_ea += 1
                medium_armies_ea += 1
                LUOS.append(int(settlement.location))

                tax_dict = production_methods.taxes_by_place_and_pops_dict
                for TileNum in settlement.property:
                    TileObj = game_obj.game_map[TileNum]
                    for pops in TileObj.lot.residency:
                        keyword = TileObj.lot.obj_name + "_" + pops.name
                        if keyword in tax_dict:
                            for product in tax_dict[keyword]:
                                if product[0] == "Florins":
                                    economy.florins_income += product[1]
                                elif product[0] == "Food":
                                    economy.food_income += product[1]
                                elif product[0] == "Wood":
                                    economy.wood_income += product[1]
                                elif product[0] == "Stone":
                                    economy.stone_income += product[1]
                                elif product[0] == "Metals":
                                    economy.metals_income += product[1]
                                elif product[0] == "Ingredients":
                                    economy.ingredients_income += product[1]
                                elif product[0] == "Armament":
                                    economy.armament_income += product[1]
                                elif product[0] == "Tools":
                                    economy.tools_income += product[1]
                                # economy.product_dict[product[0]] += int(product[1])
                                # print(product[0] + " - " + str(economy.product_dict[product[0]]))

                for pops in settlement.residency:
                    keyword = "Settlement_" + pops.name
                    if keyword in tax_dict:
                        for product in tax_dict[keyword]:
                            if product[0] == "Florins":
                                economy.florins_income += product[1]
                            elif product[0] == "Food":
                                economy.food_income += product[1]
                            elif product[0] == "Wood":
                                economy.wood_income += product[1]
                            elif product[0] == "Stone":
                                economy.stone_income += product[1]
                            elif product[0] == "Metals":
                                economy.metals_income += product[1]
                            elif product[0] == "Ingredients":
                                economy.ingredients_income += product[1]
                            elif product[0] == "Armament":
                                economy.armament_income += product[1]
                            elif product[0] == "Tools":
                                economy.tools_income += product[1]
                            # economy.product_dict[product[0]] += int(product[1])
                            # print(product[0] + " - " + str(economy.product_dict[product[0]]))

                # print("florins_income - " + str(economy.florins_income))
                # print("food_income - " + str(economy.food_income))
                # print("wood_income - " + str(economy.wood_income))
                # print("stone_income - " + str(economy.stone_income))
                # print("metals_income - " + str(economy.metals_income))
                # print("ingredients_income - " + str(economy.ingredients_income))
                # print("armament_income - " + str(economy.armament_income))
                # print("tools_income - " + str(economy.tools_income))

    for army in game_obj.game_armies:
        if army.owner == player.name:
            for unit in army.units:
                for expense in unit.cost:
                    if expense[0] == "Florins":
                        economy.florins_expenses += expense[1]
                    elif expense[0] == "Food":
                        economy.food_expenses += expense[1]
                    elif expense[0] == "Wood":
                        economy.wood_expenses += expense[1]
                    elif expense[0] == "Stone":
                        economy.stone_expenses += expense[1]
                    elif expense[0] == "Metals":
                        economy.metals_expenses += expense[1]
                    elif expense[0] == "Ingredients":
                        economy.ingredients_expenses += expense[1]
                    elif expense[0] == "Armament":
                        economy.armament_expenses += expense[1]
                    elif expense[0] == "Tools":
                        economy.tools_expenses += expense[1]

    for army_role in player.AI_cogs.army_roles:
        if army_role.army_size == 1:
            small_armies_ea -= 1
        elif army_role.army_size == 2:
            medium_armies_ea -= 1

    build_new_structures(player)
    build_new_army(player, small_armies_ea, medium_armies_ea, LUOS)

    if economy.new_round:
        economy.new_round = False
    player.AI_cogs.cognition_stage = "Manage armies"


# Maybe later I will learn how to implement this way with dictionaries
# product_dict = {"Florins" : florins_income,
#                 "Food" : food_income,
#                 "Wood" : wood_income,
#                 "Stone" : stone_income,
#                 "Metals" : metals_income,
#                 "Ingredients" : ingredients_income,
#                 "Armament" : armament_income,
#                 "Tools" : tools_income}


def build_new_structures(player):
    # One in every settlement
    economy = player.AI_cogs.economy_cogs
    if economy.new_round:
        for settlement in game_obj.game_cities:
            if settlement.owner == player.name:
                if settlement.military_occupation is None:
                    affordable_buildings = []
                    for plot in settlement.buildings:
                        if plot.status in ["Empty", "Built"]:
                            # print(plot.upgrade.name)
                            if plot.upgrade is not None:
                                if game_basic.enough_resources_to_pay(plot.upgrade.construction_cost, player.coffers):
                                    # print(str(plot.upgrade.construction_cost))
                                    if plot.upgrade.fulfilled_conditions:
                                        affordable_buildings.append(plot.screen_position)
                    # print("affordable_buildings: " + str(affordable_buildings))
                    if len(affordable_buildings) > 0:
                        plot_number = random.choice(affordable_buildings)
                        the_plot = None
                        for plot in settlement.buildings:
                            if plot.screen_position == plot_number:
                                the_plot = plot
                                print(player.name + " has started to build " + the_plot.upgrade.name +
                                      " in " + settlement.name)
                        algo_building.consume_constructions_materials(player.coffers,
                                                                      the_plot.upgrade.construction_cost,
                                                                      settlement)
                        algo_building.start_construction(the_plot)


def build_new_army(player, small_armies_ea, medium_armies_ea, LUOS):
    print(player.name + ": build_new_army")
    economy = player.AI_cogs.economy_cogs
    settlements_with_dedicated_medium_armies = []  # city_id
    for army_role in player.AI_cogs.army_roles:
        if army_role.base_of_operation != 0:
            if army_role.base_of_operation not in settlements_with_dedicated_medium_armies:
                settlements_with_dedicated_medium_armies.append(int(army_role.base_of_operation))
    # print("settlements_with_dedicated_medium_armies: " + str(settlements_with_dedicated_medium_armies))

    # If medium_armies_ea > 0
    create_medium_armies(player, economy, medium_armies_ea, settlements_with_dedicated_medium_armies)

    # If number of units in garrison armies less than 5, hire more regiments
    hire_more_regiments(player, economy, LUOS)

    # Interact with settlement buildings
    # Buy artifacts
    buy_artifacts_settlements(player, economy, LUOS)

    # Learn skills
    learn_skills_settlements(player, economy, LUOS)

    # Obtain hero attributes
    obtain_attributes_settlement(player, economy, LUOS)


def create_medium_armies(player, economy, medium_armies_ea, settlements_with_dedicated_medium_armies):
    if medium_armies_ea > 0:
        print(player.name + ": create_medium_armies")
        create_armies = True
        all_players_settlements = []  # city_id (unoccupied)
        settlements_without_dedicated_medium_armies = []  # city_id
        for settlement in game_obj.game_cities:
            # print(settlement.owner + ": " + settlement.name + " city_id - " + str(settlement.city_id) +
            #       " military_occupation - " + str(settlement.military_occupation))
            if settlement.owner == player.name and settlement.military_occupation is None:
                all_players_settlements.append(int(settlement.city_id))
                # print("all_players_settlements: " + str(all_players_settlements))
                if settlement.city_id not in settlements_with_dedicated_medium_armies:
                    settlements_without_dedicated_medium_armies.append(int(settlement.city_id))
                    # print("settlements_without_dedicated_medium_armies: " + str(settlements_without_dedicated_medium_armies))

        while create_armies:
            settlement_with_new_army = 0  # city_id
            if len(settlements_without_dedicated_medium_armies) > 0:
                city_id = random.choice(settlements_without_dedicated_medium_armies)
                settlement_with_new_army = int(city_id)
                settlements_without_dedicated_medium_armies.remove(city_id)
            else:
                city_id = random.choice(all_players_settlements)
                settlement_with_new_army = int(city_id)
                all_players_settlements.remove(city_id)

            the_settlement = common_selects.select_settlement_by_id(settlement_with_new_army)

            unit_roster = []
            for plot in the_settlement.buildings:
                if plot.status == "Built" and plot.structure.recruitment:
                    # print("Looking for recruitment options in " + plot.structure.name + " from " + the_settlement.name)
                    for hire_unit in plot.structure.recruitment:
                        print(str(hire_unit.unit_name) + " ready_units - " + str(hire_unit.ready_units))
                        if hire_unit.ready_units > 0:
                            if game_basic.enough_resources_to_hire(hire_unit.unit_name, the_settlement):
                                alignment = unit_alignment_catalog.alignment_dict[hire_unit.unit_name]
                                unit_list = create_unit.LE_units_dict_by_alignment[alignment]
                                affordable = True
                                # for unit in unit_list:
                                unit = unit_list[hire_unit.unit_name]()
                                for expense in unit.cost:
                                    if expense[0] == "Florins":
                                        if economy.florins_expenses + expense[1] > economy.florins_income * 0.8:
                                            affordable = False
                                    elif expense[0] == "Food":
                                        if economy.food_expenses + expense[1] > economy.food_income * 0.8:
                                            affordable = False
                                    elif expense[0] == "Armament":
                                        if economy.armament_expenses + expense[1] > economy.armament_income * 0.8:
                                            affordable = False
                                    elif expense[0] == "Ingredients":
                                        if economy.ingredients_expenses + expense[1] > economy.ingredients_income * 0.8:
                                            affordable = False
                                    elif expense[0] == "Wood":
                                        if economy.wood_expenses + expense[1] > economy.wood_income * 0.8:
                                            affordable = False
                                    elif expense[0] == "Stone":
                                        if economy.stone_expenses + expense[1] > economy.stone_income * 0.8:
                                            affordable = False
                                    elif expense[0] == "Metals":
                                        if economy.metals_expenses + expense[1] > economy.metals_income * 0.8:
                                            affordable = False
                                    elif expense[0] == "Tools":
                                        if economy.tools_expenses + expense[1] > economy.tools_income * 0.8:
                                            affordable = False

                                if affordable:
                                    # print("Could afford " + str(hire_unit.unit_name))
                                    unit_roster.append(hire_unit)

            if not unit_roster:
                create_armies = False
            else:
                rank_sum = 0

                keep_building = True

                # print(unit_roster)
                army_id_in_settlement = game_obj.game_map[the_settlement.location].army_id
                the_army = None
                if army_id_in_settlement:
                    the_army = common_selects.select_army_by_id(army_id_in_settlement)

                while keep_building:
                    new_unit = random.choice(unit_roster)
                    alignment = unit_alignment_catalog.alignment_dict[new_unit.unit_name]
                    # Rank check
                    rank_list = unit_rank_catalog.units_dict_by_alignment[alignment]
                    # Recruiting cost check
                    enough_resources = game_basic.enough_resources_to_hire(new_unit.unit_name, the_settlement)
                    # Expenses check
                    unit_list = create_unit.LE_units_dict_by_alignment[alignment]
                    affordable = True
                    unit = unit_list[new_unit.unit_name]()
                    for expense in unit.cost:
                        if expense[0] == "Florins":
                            if economy.florins_expenses + expense[1] > economy.florins_income * 0.8:
                                affordable = False
                        elif expense[0] == "Food":
                            if economy.food_expenses + expense[1] > economy.food_income * 0.8:
                                affordable = False
                        elif expense[0] == "Armament":
                            if economy.armament_expenses + expense[1] > economy.armament_income * 0.8:
                                affordable = False
                        elif expense[0] == "Ingredients":
                            if economy.ingredients_expenses + expense[1] > economy.ingredients_income * 0.8:
                                affordable = False
                        elif expense[0] == "Wood":
                            if economy.wood_expenses + expense[1] > economy.wood_income * 0.8:
                                affordable = False
                        elif expense[0] == "Stone":
                            if economy.stone_expenses + expense[1] > economy.stone_income * 0.8:
                                affordable = False
                        elif expense[0] == "Metals":
                            if economy.metals_expenses + expense[1] > economy.metals_income * 0.8:
                                affordable = False
                        elif expense[0] == "Tools":
                            if economy.tools_expenses + expense[1] > economy.tools_income * 0.8:
                                affordable = False

                    if rank_sum + rank_list[new_unit.unit_name] > 90 or not affordable:
                        keep_building = False
                    elif not enough_resources:
                        unit_roster.remove(new_unit)
                        if len(unit_roster) == 0:
                            keep_building = False
                    else:
                        rank_sum += int(rank_list[new_unit.unit_name])
                        print("New rank sum - " + str(rank_sum))

                        # Create army if necessary
                        if army_id_in_settlement is None:
                            owner = str(the_settlement.owner)
                            game_stats.army_id_counter += 1
                            game_obj.game_map[the_settlement.location].army_id = int(game_stats.army_id_counter)
                            game_obj.game_armies.append(game_classes.Army([int(the_settlement.posxy[0]),
                                                                           int(the_settlement.posxy[1])],
                                                                          int(the_settlement.location),
                                                                          int(game_stats.army_id_counter),
                                                                          str(owner),
                                                                          random.choice([True, False])))
                            print("Created new army, ID - " + str(game_stats.army_id_counter))

                            # Army role
                            the_army = common_selects.select_army_by_id(game_stats.army_id_counter)
                            player.AI_cogs.army_roles.append(
                                strategy_AI_classes.army_roles(int(the_army.army_id),
                                                               "Idle",
                                                               2))  # Medium size

                            for army_role in player.AI_cogs.army_roles:
                                if army_role.army_id == the_army.army_id:
                                    print("base_of_operation: " + the_settlement.name + "; city_id - " +
                                          str(the_settlement.city_id))
                                    army_role.base_of_operation = int(the_settlement.city_id)
                                    break

                        for creating_unit in unit_list:
                            if creating_unit == new_unit.unit_name:
                                creating_unit = unit_list[new_unit.unit_name]()
                                # Create new regiment
                                the_army.units.append(creating_unit)
                                game_basic.establish_leader(the_army.army_id, "Game")

                                # Increase estimated expenses
                                for expense in creating_unit.cost:
                                    if expense[0] == "Florins":
                                        economy.florins_expenses += int(expense[1])
                                    elif expense[0] == "Food":
                                        economy.food_expenses += int(expense[1])
                                    elif expense[0] == "Armament":
                                        economy.armament_expenses += int(expense[1])
                                    elif expense[0] == "Ingredients":
                                        economy.ingredients_expenses += int(expense[1])
                                    elif expense[0] == "Wood":
                                        economy.wood_expenses += int(expense[1])
                                    elif expense[0] == "Stone":
                                        economy.stone_expenses += int(expense[1])
                                    elif expense[0] == "Metals":
                                        economy.metals_expenses += int(expense[1])
                                    elif expense[0] == "Tools":
                                        economy.tools_expenses += int(expense[1])

                                print("Created new regiment - " + creating_unit.name)
                                # Spend resources
                                game_basic.realm_payment_for_object(creating_unit.name, the_settlement)

                                # Decrease available regiments for recruiting
                                new_unit.ready_units -= 1
                                if new_unit.ready_units == 0:
                                    unit_roster.remove(new_unit)
                                print("len(unit_roster) " + str(len(unit_roster)))
                                break

                        if len(unit_roster) == 0:
                            keep_building = False
                        if len(the_army.units) == 20:
                            keep_building = False
                        # keep_building = False

                if the_army.hero is None:
                    hire_a_hero(player, economy, the_army, the_settlement)

                # print("update_regiment_sprites_from_object")
                update_gf_game_board.update_regiment_sprites_from_object(the_army)
            create_armies = False


def hire_more_regiments(player, economy, LUOS):
    for TileNum in LUOS:
        if game_obj.game_map[TileNum].army_id:
            print(player.name + ": hire_more_regiments")
            the_army = common_selects.select_army_by_id(game_obj.game_map[TileNum].army_id)

            if the_army.action not in ["Fighting", "Besieged"]:
                rank_sum = 0
                for regiment in the_army.units:
                    rank_sum += int(regiment.rank)

                the_army_size = 0
                for army_role in player.AI_cogs.army_roles:
                    if army_role.army_id == the_army.army_id:
                        the_army_size = int(army_role.army_size)
                        break

                if the_army_size == 2 and rank_sum < 90 and len(the_army.units) < 20:
                    the_settlement = common_selects.select_settlement_by_id(game_obj.game_map[TileNum].city_id)

                    hire_new_regiments(player, economy, rank_sum, 90, the_army, the_settlement)

                update_gf_game_board.update_regiment_sprites_from_object(the_army)


def hire_new_regiments(player, economy, rank_sum, rank_ea, the_army, the_settlement):
    # rank_ea - expected amount of rank sum for an army
    unit_roster = []
    for plot in the_settlement.buildings:
        if plot.status == "Built" and plot.structure.recruitment:
            for hire_unit in plot.structure.recruitment:
                # print(str(hire_unit.unit_name) + " ready_units - " + str(hire_unit.ready_units))
                if hire_unit.ready_units > 0:
                    if game_basic.enough_resources_to_hire(hire_unit.unit_name, the_settlement):
                        alignment = unit_alignment_catalog.alignment_dict[hire_unit.unit_name]
                        unit_list = create_unit.LE_units_dict_by_alignment[alignment]
                        affordable = True
                        # for unit in unit_list:
                        unit = unit_list[hire_unit.unit_name]()
                        for expense in unit.cost:
                            if expense[0] == "Florins":
                                if economy.florins_expenses + expense[1] > economy.florins_income * 0.8:
                                    affordable = False
                            elif expense[0] == "Food":
                                if economy.food_expenses + expense[1] > economy.food_income * 0.8:
                                    affordable = False
                            elif expense[0] == "Armament":
                                if economy.armament_expenses + expense[1] > economy.armament_income * 0.8:
                                    affordable = False
                            elif expense[0] == "Ingredients":
                                if economy.ingredients_expenses + expense[1] > economy.ingredients_income * 0.8:
                                    affordable = False
                            elif expense[0] == "Wood":
                                if economy.wood_expenses + expense[1] > economy.wood_income * 0.8:
                                    affordable = False
                            elif expense[0] == "Stone":
                                if economy.stone_expenses + expense[1] > economy.stone_income * 0.8:
                                    affordable = False
                            elif expense[0] == "Metals":
                                if economy.metals_expenses + expense[1] > economy.metals_income * 0.8:
                                    affordable = False
                            elif expense[0] == "Tools":
                                if economy.tools_expenses + expense[1] > economy.tools_income * 0.8:
                                    affordable = False

                        if affordable:
                            # print("Could afford " + str(hire_unit.unit_name))
                            unit_roster.append(hire_unit)

    if unit_roster:
        keep_building = True

        while keep_building:
            new_unit = random.choice(unit_roster)
            alignment = unit_alignment_catalog.alignment_dict[new_unit.unit_name]
            # Rank check
            rank_list = unit_rank_catalog.units_dict_by_alignment[alignment]
            # Recruiting cost check
            enough_resources = game_basic.enough_resources_to_hire(new_unit.unit_name, the_settlement)
            # Expenses check
            unit_list = create_unit.LE_units_dict_by_alignment[alignment]
            affordable = True
            unit = unit_list[new_unit.unit_name]()
            for expense in unit.cost:
                if expense[0] == "Florins":
                    if economy.florins_expenses + expense[1] > economy.florins_income * 0.8:
                        affordable = False
                elif expense[0] == "Food":
                    if economy.food_expenses + expense[1] > economy.food_income * 0.8:
                        affordable = False
                elif expense[0] == "Armament":
                    if economy.armament_expenses + expense[1] > economy.armament_income * 0.8:
                        affordable = False
                elif expense[0] == "Ingredients":
                    if economy.ingredients_expenses + expense[1] > economy.ingredients_income * 0.8:
                        affordable = False
                elif expense[0] == "Wood":
                    if economy.wood_expenses + expense[1] > economy.wood_income * 0.8:
                        affordable = False
                elif expense[0] == "Stone":
                    if economy.stone_expenses + expense[1] > economy.stone_income * 0.8:
                        affordable = False
                elif expense[0] == "Metals":
                    if economy.metals_expenses + expense[1] > economy.metals_income * 0.8:
                        affordable = False
                elif expense[0] == "Tools":
                    if economy.tools_expenses + expense[1] > economy.tools_income * 0.8:
                        affordable = False

            if len(the_army.units) >= 5:
                if rank_sum + rank_list[new_unit.unit_name] > rank_ea:
                    keep_building = False
            if not affordable:
                keep_building = False
            elif not enough_resources:
                unit_roster.remove(new_unit)
                if len(unit_roster) == 0:
                    keep_building = False
            else:
                rank_sum += int(rank_list[new_unit.unit_name])
                print("New rank sum - " + str(rank_sum))

                for creating_unit in unit_list:
                    if creating_unit == new_unit.unit_name:
                        creating_unit = unit_list[new_unit.unit_name]()
                        # Create new regiment
                        the_army.units.append(creating_unit)
                        game_basic.establish_leader(the_army.army_id, "Game")

                        # Increase estimated expenses
                        for expense in creating_unit.cost:
                            if expense[0] == "Florins":
                                economy.florins_expenses += int(expense[1])
                            elif expense[0] == "Food":
                                economy.food_expenses += int(expense[1])
                            elif expense[0] == "Armament":
                                economy.armament_expenses += int(expense[1])
                            elif expense[0] == "Ingredients":
                                economy.ingredients_expenses += int(expense[1])
                            elif expense[0] == "Wood":
                                economy.wood_expenses += int(expense[1])
                            elif expense[0] == "Stone":
                                economy.stone_expenses += int(expense[1])
                            elif expense[0] == "Metals":
                                economy.metals_expenses += int(expense[1])
                            elif expense[0] == "Tools":
                                economy.tools_expenses += int(expense[1])

                        print("Created new regiment - " + creating_unit.name)
                        # Spend resources
                        game_basic.realm_payment_for_object(creating_unit.name, the_settlement)

                        # Decrease available regiments for recruiting
                        new_unit.ready_units -= 1
                        if new_unit.ready_units == 0:
                            unit_roster.remove(new_unit)
                        print("len(unit_roster) " + str(len(unit_roster)))
                        break

                if len(unit_roster) == 0:
                    keep_building = False
                if len(the_army.units) == 20:
                    keep_building = False


def hire_a_hero(player, economy, the_army, settlement):
    alignment = settlement.alignment
    hero_class = random.choice(new_heroes_catalog.heroes_classes_dict_by_alignment[alignment])
    # print(str(hero_class))
    hero_pick = new_heroes_catalog.basic_heroes_dict_by_alignment[alignment][hero_class]
    if game_basic.enough_resources_to_hire_hero(hero_pick, player.coffers):
        # Archetype
        hero_archetypes_list = list(hero_archetypes.hero_catalog[hero_class].keys())
        ha_weights_list = list(hero_archetypes.hero_catalog[hero_class].values())  # hero archetype weight list
        hero_archetype = random.choices(hero_archetypes_list, weights=ha_weights_list)[0]
        print("Hero archetype - " + str(hero_archetype))

        first_starting_skill, second_starting_skill = game_basic.form_starting_skills_pool(hero_class, "AI")

        first_skill_name = None
        if first_starting_skill is None:
            first_skill_name = starting_skills.locked_first_skill_by_class[hero_class]
        else:
            first_skill_list = list(starting_skills.starting_skills_by_class[hero_class])
            first_weight_list = []
            for skill_name in first_skill_list:
                first_weight_list.append(archetype_skill_weights.class_cat[hero_archetype][skill_name])
            first_skill_name = random.choices(first_skill_list, weights=first_weight_list)[0]

        second_skill_list = list(starting_skills.starting_skills_by_class[hero_class])
        if first_starting_skill is not None:
            second_skill_list.remove(first_skill_name)
        second_weight_list = []
        for skill_name in second_skill_list:
            second_weight_list.append(archetype_skill_weights.class_cat[hero_archetype][skill_name])
        second_skill_name = random.choices(second_skill_list, weights=second_weight_list)[0]

        print("first_skill_name - " + first_skill_name)
        first_skill = hero_skill_catalog.hero_skill_data[first_skill_name]
        print("second_skill_name - " + second_skill_name)
        second_skill = hero_skill_catalog.hero_skill_data[second_skill_name]

        the_army.hero = common_hero_funs.create_hero(hero_class, hero_pick, player, settlement,
                                                     first_skill_name, second_skill_name, first_skill, second_skill)
        the_army.hero.archetype = str(hero_archetype)
        print(str(the_army.hero.hero_class) + " " + the_army.hero.name)


def buy_artifacts_settlements(player, economy, LUOS):
    # print(player.name + ": buy_artifacts_settlements")
    for TileNum in LUOS:
        if game_obj.game_map[TileNum].army_id:
            the_settlement = common_selects.select_settlement_by_id(game_obj.game_map[TileNum].city_id)
            the_army = common_selects.select_army_by_id(game_obj.game_map[TileNum].army_id)

            if the_army.hero:
                the_hero = the_army.hero
                print(the_hero.name + ": buy_artifacts_settlements")

                buy_artifact = False
                # Inventory not full
                if len(the_hero.inventory) < 4:
                    # Random chance to buy new artifact
                    if random.randint(0, 100) <= 80 - 20 * len(the_hero.inventory):
                        buy_artifact = True

                artifact_list = []
                if buy_artifact:
                    for plot in the_settlement.buildings:
                        if plot.status == "Built":
                            if plot.structure.name in ["KL artifact market"]:

                                for artifact_name in artifact_assortment.stock_by_place[plot.structure.name]:
                                    enough_florins = False
                                    for res in player.coffers:
                                        if res[0] == "Florins":
                                            # print("Florins - " + str(res[1]) + "; " + str(artifact_name) + " - " +
                                            #       str(artifact_catalog.artifact_data[artifact_name][2]))
                                            if artifact_catalog.artifact_data[artifact_name][2] <= res[1]:
                                                enough_florins = True
                                                break

                                    if enough_florins:
                                        add_artifact = True
                                        for artifact in the_hero.inventory:
                                            if artifact_name == artifact.name:
                                                add_artifact = False
                                                break

                                        if add_artifact:
                                            artifact_list.append(str(artifact_name))

                if artifact_list:
                    # print("Artifacts: " + str(artifact_list))
                    new_artifact = random.choice(artifact_list)
                    print("New artifact - " + str(new_artifact) + " (-" +
                          str(artifact_catalog.artifact_data[new_artifact][2]) + " florins)")

                    # Spent money
                    for res in player.coffers:
                        if res[0] == "Florins":
                            res[1] -= int(artifact_catalog.artifact_data[new_artifact][2])
                            break

                    # Transfer money to traders
                    for pops in the_settlement.residency:
                        if pops.name == "Merchants":
                            no_money = True
                            for product in pops.reserve:
                                # Pay money to seller
                                if product[0] == "Florins":
                                    no_money = False
                                    product[1] += int(artifact_catalog.artifact_data[new_artifact][2])

                            if no_money:
                                pops.reserve.append(["Florins", int(artifact_catalog.artifact_data[new_artifact][2])])
                            break

                    # Give artifact to hero
                    details = artifact_catalog.artifact_data[new_artifact]
                    the_hero.inventory.append(artifact_classes.Artifact(details[0],
                                                                        details[1],
                                                                        details[2],
                                                                        details[3],
                                                                        details[4]))


def learn_skills_settlements(player, economy, LUOS):
    for TileNum in LUOS:
        if game_obj.game_map[TileNum].army_id:
            the_settlement = common_selects.select_settlement_by_id(game_obj.game_map[TileNum].city_id)
            the_army = common_selects.select_army_by_id(game_obj.game_map[TileNum].army_id)

            if the_army.hero:
                the_hero = the_army.hero
                print(the_hero.name + ": learn_skills_settlements")

                learn_skill = False
                # Random chance (30%) to learn new skill
                if random.randint(0, 100) <= 30:
                    learn_skill = True

                skills_list = []
                resources = [["Florins", 2000]]
                if learn_skill:
                    for plot in the_settlement.buildings:
                        if plot.status == "Built":
                            if plot.structure.name in ["KL School of magic"]:

                                for new_skill in skills_curriculum.curriculum_by_school[plot.structure.name]:
                                    enough_florins = common_transactions.sufficient_funds(resources, player)

                                    if enough_florins:
                                        add_skill = True
                                        for skill in the_hero.skills:
                                            if new_skill in skill.tags:
                                                add_skill = False
                                                break

                                        if add_skill:
                                            skills_list.append(str(new_skill))

                    if skills_list:
                        # print("Skills: " + str(skills_list))
                        new_skill = random.choice(skills_list)
                        # print("New skill - " + str(new_skill))

                        # Pay for skill
                        common_transactions.payment(resources, player)

                        # Transfer money to traders
                        for pops in the_settlement.residency:
                            if pops.name == "Merchants":
                                no_money = True
                                for product in pops.reserve:
                                    # Pay money to seller
                                    if product[0] == "Florins":
                                        no_money = False
                                        product[1] += 2000

                                if no_money:
                                    pops.reserve.append(["Florins", 2000])
                                break

                        # Learn new skill
                        details = hero_skill_catalog.hero_skill_data[new_skill]
                        counting = 0
                        for skill in the_hero.skills:
                            if skill.skill_type == "Skill":
                                counting += 1

                        position = [0, int(counting)]

                        the_hero.skills.append(skill_classes.Hero_Skill(str(new_skill),
                                                                        str(details[0]),
                                                                        str(details[1]),
                                                                        str(details[2]),
                                                                        str(details[3]),
                                                                        str(details[4]),
                                                                        list(details[5]),
                                                                        list(details[6]),
                                                                        details[7],
                                                                        position))

                        for skill in the_hero.skills:
                            print(skill.name)


def obtain_attributes_settlement(player, economy, LUOS):
    for TileNum in LUOS:
        if game_obj.game_map[TileNum].army_id:
            the_settlement = common_selects.select_settlement_by_id(game_obj.game_map[TileNum].city_id)
            the_army = common_selects.select_army_by_id(game_obj.game_map[TileNum].army_id)

            if the_army.hero:
                the_hero = the_army.hero
                obtain_attribute = False
                # Random chance (20%) to learn new skill
                if random.randint(0, 100) <= 20:
                    obtain_attribute = True

                attributes_list = []
                if obtain_attribute:
                    for plot in the_settlement.buildings:
                        if plot.status == "Built":
                            if plot.structure.name in ["Wheelwright guild"]:
                                dic = battle_attributes_assortment.assortment_by_place[plot.structure.name]
                                key_list = list(dic)
                                for key in key_list:
                                    attribute = dic[key]
                                    resources = [["Florins", attribute[4]]]
                                    enough_florins = common_transactions.sufficient_funds(resources, player)

                                    if enough_florins:
                                        add_attribute = True
                                        for package in the_hero.attributes_list:
                                            if package.package_name == key:
                                                add_attribute = False
                                                break

                                        if add_attribute:
                                            attributes_list.append([str(key), dic])

                    if attributes_list:
                        new_attribute = random.choice(attributes_list)
                        attribute_info = new_attribute[1][new_attribute[0]]

                        # Pay for attribute
                        resources = [["Florins", attribute_info[4]]]
                        common_transactions.payment(resources, player)

                        # Learn new attribute
                        att = game_classes.Battle_Attribute(
                            str(attribute_info[0]),
                            str(attribute_info[1]),
                            int(attribute_info[2]))

                        pack = game_classes.Attribute_Package([att],
                                                              new_attribute[0])

                        for attribute in pack.attribute_list:
                            if attribute.tag == "hero":
                                if attribute.stat == "magic power":
                                    the_hero.magic_power += int(attribute.value)
                                elif attribute.stat == "knowledge":
                                    the_hero.knowledge += int(attribute.value)
                                    the_hero.max_mana_reserve += int(attribute.value * 10)
                                    the_hero.mana_reserve += int(attribute.value * 10)

                        the_hero.attributes_list.append(pack)
