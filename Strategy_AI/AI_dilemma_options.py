## Among Myth and Wonder
## AI_dilemma_options

import random
import copy

from Resources import game_obj
from Resources import game_basic
from Resources import game_stats
from Resources import game_classes
from Resources import campaign_effect_classes
from Resources import update_gf_game_board
from Resources import common_selects

from Content import recruitment_structures

from Storage import create_unit


def remove_quest_message(realm, message):
    for quest_message in realm.quests_messages:
        if quest_message.name == message.name:
            realm.quests_messages.remove(quest_message)
            break

    print(realm.name + ": len(realm.quests_messages) - " + str(len(realm.quests_messages)))


def AI_forrest_law_upheld(realm, message):
    # Add effect
    effect = campaign_effect_classes.Settlement_Effect("Forest law restored",
                                                       "Settlement",
                                                       "Loyalty",
                                                       [campaign_effect_classes.Faction_Effect("Peasant estate",
                                                                                               "Loyalty",
                                                                                               1,
                                                                                               "Subtraction"),
                                                        campaign_effect_classes.Recruitment_Effect(["peasant"],
                                                                                                   "Replenishment and ready",
                                                                                                   None,
                                                                                                   "Banned")
                                                        ],
                                                       8)

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            # Adjust faction loyalty
            settlement.local_effects.append(effect)
            for faction in settlement.factions:
                if faction.name == "Peasant estate":
                    faction.loyalty -= 1

            # Adjust recruitment
            for plot in settlement.buildings:
                if plot.structure is not None:
                    if plot.structure.recruitment:
                        if plot.status == "Built":
                            for lodge in plot.structure.recruitment:
                                if "peasant" in recruitment_structures.unit_tags[lodge.unit_name]:
                                    lodge.time_passed = 0
                                    lodge.ready_units = 0
            break

    remove_quest_message(realm, message)


def AI_forrest_law_lenient(realm, message):
    print("forrest_law_lenient")
    print("quest.settlement_location - " + str(message.settlement_location))
    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            the_settlement = settlement
            print(the_settlement.name)
            break

    # Create neutral army
    unoccupied_territory = []

    print("the_settlement.control_zone: " + str(the_settlement.control_zone))
    for Tile in the_settlement.control_zone:
        if game_obj.game_map[Tile].army_id is None:
            if game_obj.game_map[Tile].lot is None:
                unoccupied_territory.append(int(Tile))

    print("unoccupied_territory: " + str(unoccupied_territory))
    if len(unoccupied_territory) > 0:
        TileNum = random.choice(unoccupied_territory)
        x = game_obj.game_map[TileNum].posxy[0]
        y = game_obj.game_map[TileNum].posxy[1]
        game_stats.army_id_counter += 1
        game_obj.game_map[TileNum].army_id = int(game_stats.army_id_counter)

        game_obj.game_armies.append(game_classes.Army([int(x), int(y)], int(TileNum),
                                                      int(game_stats.army_id_counter),
                                                      "Neutral",
                                                      True))

        # print("Number of armies - " + str(len(game_obj.game_armies)))
        # print("game_stats.army_id_counter - " + str(game_stats.army_id_counter))
        units_list = create_unit.LE_units_dict_by_alignment["Neutrals"]
        # Add regiments to created army
        army = common_selects.select_army_by_id(game_stats.army_id_counter)
        # Add bandit archers
        army.units.append(units_list["Bandit archers"]())

        game_basic.establish_leader(game_stats.army_id_counter, "Game")

        army.event = game_classes.Post_Battle_Event("Poachers in Royal forest",
                                                    int(message.settlement_location),
                                                    str(realm.name))

        # Add new quest to eliminate rogue army
        realm.quests_messages.append(game_classes.Quest_Message("Poachers in Royal forest",
                                                                int(the_settlement.location),
                                                                str(the_settlement.name),
                                                                "Quest",
                                                                str(the_settlement.alignment),
                                                                "Army",
                                                                int(game_stats.army_id_counter),
                                                                None))

        update_gf_game_board.update_sprites()

    # Add effect
    effect = campaign_effect_classes.Settlement_Effect("Poachers in Royal forest",
                                                       "Settlement",
                                                       "Loyalty",
                                                       [campaign_effect_classes.Faction_Effect("Nobility estate",
                                                                                               "Loyalty",
                                                                                               1,
                                                                                               "Subtraction")
                                                        ],
                                                       True)

    the_settlement.local_effects.append(effect)
    for faction in the_settlement.factions:
        if faction.name == "Nobility estate":
            faction.loyalty -= 1

    remove_quest_message(realm, message)


def AI_rule_of_monastic_life_ignore(realm, message):
    # Add effect
    effect = campaign_effect_classes.Settlement_Effect("Frivolous monks",
                                                       "Settlement",
                                                       "Replenishment",
                                                       [
                                                           campaign_effect_classes.Recruitment_Effect(["Battle monks"],
                                                                                                      "Replenishment and ready",
                                                                                                      2,
                                                                                                      "Addition")
                                                       ],
                                                       True)

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            settlement.local_effects.append(effect)

            # Adjust recruitment
            for plot in settlement.buildings:
                if plot.structure is not None:
                    if plot.structure.recruitment:
                        if plot.status == "Built":
                            for lodge in plot.structure.recruitment:
                                if "Battle monks" in recruitment_structures.unit_tags[lodge.unit_name]:
                                    lodge.replenishment_rate += 2
                                    break
            break

    remove_quest_message(realm, message)


def AI_rule_of_monastic_life_aid_reform(realm, message):
    # Add effect
    effect1 = campaign_effect_classes.Settlement_Effect("Rule of Monastic Life",
                                                        "Settlement",
                                                        "Control",
                                                        [
                                                            campaign_effect_classes.Control_Effect("Knight Lords",
                                                                                                   "Control",
                                                                                                   1,
                                                                                                   "Addition")
                                                        ],
                                                        True)
    effect2 = campaign_effect_classes.Settlement_Effect("Disciplined monks",
                                                        "Settlement",
                                                        "Loyalty",
                                                        [campaign_effect_classes.Faction_Effect("Clergy estate",
                                                                                                "Loyalty",
                                                                                                2,
                                                                                                "Subtraction")
                                                         ],
                                                        8)

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            settlement.local_effects.append(effect1)
            settlement.local_effects.append(effect2)
            # Adjust faction loyalty
            for faction in settlement.factions:
                if faction.name == "Clergy estate":
                    faction.loyalty -= 2
            break

    remove_quest_message(realm, message)


def AI_grant_land_holdings(realm, message):
    # Add effect
    effect1 = campaign_effect_classes.Settlement_Effect("Bribed local lord",
                                                        "Settlement",
                                                        "Loyalty",
                                                        [
                                                            campaign_effect_classes.Faction_Effect("Nobility estate",
                                                                                                   "Loyalty",
                                                                                                   2,
                                                                                                   "Addition")
                                                        ],
                                                        8)
    effect2 = campaign_effect_classes.Settlement_Effect("Transferred abbey's land holdings",
                                                        "Settlement",
                                                        "Loyalty",
                                                        [campaign_effect_classes.Faction_Effect("Clergy estate",
                                                                                                "Loyalty",
                                                                                                1,
                                                                                                "Subtraction")
                                                         ],
                                                        12)

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            # Adjust faction loyalty
            settlement.local_effects.append(effect1)
            settlement.local_effects.append(effect2)
            for faction in settlement.factions:
                if faction.name == "Nobility estate":
                    faction.loyalty += 2
                elif faction.name == "Clergy estate":
                    faction.loyalty -= 1
            break

    remove_quest_message(realm, message)


def AI_pass_on_this_opportunity(realm, message):
    remove_quest_message(realm, message)


def AI_support_monastery_school(realm, message):
    game_basic.realm_payment(realm.name, [["Florins", 5000]])
    # Add effect
    effect = campaign_effect_classes.Settlement_Effect("Monastery school",
                                                       "Settlement",
                                                       "New heroes",
                                                       [
                                                           campaign_effect_classes.New_Heroes_Effect(
                                                               ["Priest of Salvation"],
                                                               "Level",
                                                               1,
                                                               "Addition")
                                                       ],
                                                       True)

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            # Apply effect
            settlement.local_effects.append(effect)

    remove_quest_message(realm, message)


def AI_track_the_dragon(realm, message):
    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            the_settlement = settlement
            # print(the_settlement.name)
            break

    # Create neutral army
    unoccupied_territory = []

    # print("the_settlement.control_zone: " + str(the_settlement.control_zone))
    for Tile in the_settlement.control_zone:
        if game_obj.game_map[Tile].army_id is None:
            if game_obj.game_map[Tile].lot is None:
                unoccupied_territory.append(int(Tile))

    if len(unoccupied_territory) > 0:
        TileNum = random.choice(unoccupied_territory)
        x = game_obj.game_map[TileNum].posxy[0]
        y = game_obj.game_map[TileNum].posxy[1]
        game_stats.army_id_counter += 1
        game_obj.game_map[TileNum].army_id = int(game_stats.army_id_counter)

        game_obj.game_armies.append(game_classes.Army([int(x), int(y)], int(TileNum),
                                                      int(game_stats.army_id_counter),
                                                      "Neutral",
                                                      True))

        # print("Number of armies - " + str(len(game_obj.game_armies)))
        # print("game_stats.army_id_counter - " + str(game_stats.army_id_counter))
        units_list = create_unit.LE_units_dict_by_alignment["Neutrals"]
        # Add regiments to created army
        army = common_selects.select_army_by_id(game_stats.army_id_counter)
        # Add grey dragon
        army.units.append(units_list["Grey dragon"]())

        game_basic.establish_leader(game_stats.army_id_counter, "Game")

        army.event = game_classes.Post_Battle_Event("Slay the Grey dragon",
                                                    int(message.settlement_location),
                                                    str(realm.name))

        # Add new quest to eliminate rogue army
        realm.quests_messages.append(game_classes.Quest_Message("Slay the Grey dragon",
                                                                int(the_settlement.location),
                                                                str(the_settlement.name),
                                                                "Quest",
                                                                str(the_settlement.alignment),
                                                                "Army",
                                                                int(game_stats.army_id_counter),
                                                                None))

        update_gf_game_board.update_sprites()

    # Add effect
    effect0 = campaign_effect_classes.Settlement_Effect("Slay the Grey dragon",
                                                        "Settlement",
                                                        "Loyalty",
                                                        [campaign_effect_classes.Faction_Effect("Nobility estate",
                                                                                                "Loyalty",
                                                                                                1,
                                                                                                "Subtraction"),
                                                         campaign_effect_classes.Faction_Effect("Peasant estate",
                                                                                                "Loyalty",
                                                                                                1,
                                                                                                "Subtraction")
                                                         ],
                                                        True)

    the_settlement.local_effects.append(effect0)
    for faction in the_settlement.factions:
        if faction.name in ["Nobility estate", "Peasant estate"]:
            faction.loyalty -= 1

    remove_quest_message(realm, message)
    print(message.name + ": In the realm " + str(realm.name) + " loyal warriors are tracking the Grey Dragon")


def AI_send_party_of_huntsmen(realm, message):
    remove_quest_message(realm, message)
    print(message.name + ": In the realm " + str(realm.name) + " hunters were dispatched to chase the Grey Dragon")


def AI_trade_with_dwarves(realm, message):
    game_basic.realm_payment(realm.name, [["Florins", 2500]])
    game_basic.realm_income(realm.name, [["Armament", 2500]])

    remove_quest_message(realm, message)


def AI_dwarves_spend_money(realm, message):
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            for pops in settlement.residency:
                if pops.name == "Merchants":
                    game_basic.simple_add_resources(pops.reserve, [["Florins", 250]])
                    break
            break

    remove_quest_message(realm, message)


def AI_promise_to_supply_stone(realm, message):
    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            the_settlement = settlement
            print(the_settlement.name)
            break

    # Add new quest to provide stone to vassal
    realm.quests_messages.append(game_classes.Quest_Message("Provide stone to vassal",
                                                            int(the_settlement.location),
                                                            str(the_settlement.name),
                                                            "Quest",
                                                            str(the_settlement.alignment),
                                                            None,
                                                            None,
                                                            5))

    # Add effect
    effect0 = campaign_effect_classes.Settlement_Effect("Vassal awaits for stone",
                                                        "Settlement",
                                                        "Loyalty",
                                                        [campaign_effect_classes.Faction_Effect("Nobility estate",
                                                                                                "Loyalty",
                                                                                                1,
                                                                                                "Subtraction")
                                                         ],
                                                        True)

    the_settlement.local_effects.append(effect0)
    for faction in the_settlement.factions:
        if faction.name == "Nobility estate":
            faction.loyalty -= 1

    remove_quest_message(realm, message)


def AI_provide_troops_to_vassal(realm, message):
    # Add effect
    effect = campaign_effect_classes.Settlement_Effect("Provided retinue to vassal",
                                                       "Settlement",
                                                       "Replenishment",
                                                       [campaign_effect_classes.Recruitment_Effect(["men-at-arms"],
                                                                                                   "Replenishment and ready",
                                                                                                   None,
                                                                                                   "Banned")
                                                        ],
                                                       10)

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            settlement.local_effects.append(effect)

            # Adjust recruitment
            for plot in settlement.buildings:
                if plot.structure is not None:
                    if plot.structure.recruitment:
                        if plot.status == "Built":
                            for lodge in plot.structure.recruitment:
                                if "men-at-arms" in recruitment_structures.unit_tags[lodge.unit_name]:
                                    lodge.time_passed = 0
                                    lodge.ready_units = 0
            break

    remove_quest_message(realm, message)


def AI_reject_request_for_stone_materials(realm, message):
    # Add effect
    effect2 = campaign_effect_classes.Settlement_Effect("Rejected request for stone",
                                                        "Settlement",
                                                        "Loyalty",
                                                        [campaign_effect_classes.Faction_Effect("Nobility estate",
                                                                                                "Loyalty",
                                                                                                2,
                                                                                                "Subtraction")
                                                         ],
                                                        20)

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            settlement.local_effects.append(effect2)
            # Adjust faction loyalty
            for faction in settlement.factions:
                if faction.name == "Nobility estate":
                    faction.loyalty -= 2
            break

    remove_quest_message(realm, message)


## Options
def forrest_law_options(realm):
    options_list = [AI_forrest_law_upheld, AI_forrest_law_lenient]
    weights_list = [5, 5]
    return options_list, weights_list


def rule_of_monastic_life_options(realm):
    options_list = [AI_rule_of_monastic_life_ignore, AI_rule_of_monastic_life_aid_reform]
    weights_list = [2, 8]
    return options_list, weights_list


def favor_abbeys_lands_options(realm):
    options_list = [AI_grant_land_holdings, AI_pass_on_this_opportunity]
    weights_list = [8, 2]
    return options_list, weights_list


def monastery_school_options(realm):
    options_list = [AI_pass_on_this_opportunity]
    weights_list = [2]

    if game_basic.enough_resources_to_pay([["Florins", 5000]], realm.coffers):
        options_list.append(AI_support_monastery_school)
        weights_list.append(8)

    return options_list, weights_list


def grey_dragon_slayer_options(realm):
    options_list = [AI_track_the_dragon]
    weights_list = [1]

    if realm.leader.lifestyle_traits[0] == "Hunter" or realm.leader.lifestyle_traits[1] == "Hunter":
        options_list.append(AI_send_party_of_huntsmen)
        weights_list.append(9)

    return options_list, weights_list


def dwarven_caravan_options(realm):
    options_list = [AI_dwarves_spend_money]
    weights_list = [2]

    if game_basic.enough_resources_to_pay([["Florins", 2500]], realm.coffers):
        options_list.append(AI_trade_with_dwarves)
        weights_list.append(8)

    return options_list, weights_list


def desolated_defences_options(realm):
    options_list = [AI_provide_troops_to_vassal, AI_reject_request_for_stone_materials]
    weights_list = [4, 1]

    for resource in realm.coffers:
        if resource[0] == "Stone":
            if resource[1] >= 1600:
                options_list.append(AI_promise_to_supply_stone)
                weights_list.append(10)
            else:
                options_list.append(AI_promise_to_supply_stone)
                weights_list.append(5)
            break

    return options_list, weights_list


options_dict = {"Forest law" : forrest_law_options,
                "Rule of Monastic Life" : rule_of_monastic_life_options,
                "Favor abbey's lands" : favor_abbeys_lands_options,
                "Monastery school" : monastery_school_options,
                "Grey dragon slayer" : grey_dragon_slayer_options,
                "Dwarven caravan" : dwarven_caravan_options,
                "Desolated defences" : desolated_defences_options}
