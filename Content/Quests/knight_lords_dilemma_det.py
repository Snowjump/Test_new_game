## Among Myth and Wonder

import copy
import random

from Resources import game_stats
from Resources import game_obj
from Resources import game_basic
from Resources import game_classes
from Resources import campaign_effect_classes
from Resources import update_gf_game_board

from Content import recruitment_structures

from Storage import create_unit


def forrest_law_upheld():
    quest, the_realm = quest_message_details()
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

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            # Adjust faction loyalty
            settlement.local_effects.append(effect)
            for faction in settlement.factions:
                if faction.name == "Peasant estate":
                    faction.loyalty -= 1

            # Adjust recruitment
            for plot in settlement.buildings:
                if plot.structure is not None:
                    if len(plot.structure.recruitment) > 0:
                        if plot.status == "Built":
                            for lodge in plot.structure.recruitment:
                                if "peasant" in recruitment_structures.unit_tags[lodge.unit_name]:
                                    lodge.time_passed = 0
                                    lodge.ready_units = 0
            break

    remove_quest_message(quest.name)
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def forrest_law_lenient():
    print("forrest_law_lenient")
    quest, the_realm = quest_message_details()
    print("quest.settlement_location - " + str(quest.settlement_location))
    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
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
        units_list = list(create_unit.LE_units_dict_by_alignment["Neutrals"])
        # Add regiments to created army
        for army in game_obj.game_armies:
            if army.army_id == game_stats.army_id_counter:
                # Add bandit archers
                army.units.append(copy.deepcopy(units_list[1]))

                game_basic.establish_leader(game_stats.army_id_counter, "Game")

                army.event = game_classes.Post_Battle_Event("Poachers in Royal forest",
                                                            int(quest.settlement_location),
                                                            str(the_realm.name))
                break

        # Add new quest to eliminate rogue army
        the_realm.quests_messages.append(game_classes.Quest_Message("Poachers in Royal forest",
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

    remove_quest_message(quest.name)
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def rule_of_monastic_life_ignore():
    quest, the_realm = quest_message_details()
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

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            settlement.local_effects.append(effect)

            # Adjust recruitment
            for plot in settlement.buildings:
                if plot.structure is not None:
                    if len(plot.structure.recruitment) > 0:
                        if plot.status == "Built":
                            for lodge in plot.structure.recruitment:
                                if "Battle monks" in recruitment_structures.unit_tags[lodge.unit_name]:
                                    lodge.replenishment_rate += 2
                                    break
            break

    remove_quest_message("Rule of Monastic Life")
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def rule_of_monastic_life_aid_reform():
    quest, the_realm = quest_message_details()
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

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            settlement.local_effects.append(effect1)
            settlement.local_effects.append(effect2)
            # Adjust faction loyalty
            for faction in settlement.factions:
                if faction.name == "Clergy estate":
                    faction.loyalty -= 2
            break

    remove_quest_message("Rule of Monastic Life")
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def grant_land_holdings():
    quest, the_realm = quest_message_details()
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

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            # Adjust faction loyalty
            settlement.local_effects.append(effect1)
            settlement.local_effects.append(effect2)
            for faction in settlement.factions:
                if faction.name == "Nobility estate":
                    faction.loyalty += 2
                elif faction.name == "Clergy estate":
                    faction.loyalty -= 1
            break

    remove_quest_message("Favor abbey's lands")
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def support_monastery_school():
    if game_basic.enough_resources_to_pay([["Florins", 5000]]):
        quest, the_realm = quest_message_details()
        game_basic.realm_payment(the_realm.name, [["Florins", 5000]])
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

        the_settlement = None
        for settlement in game_obj.game_cities:
            if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
                the_settlement = settlement
                # Apply effect
                settlement.local_effects.append(effect)

        remove_quest_message("Monastery school")
        game_stats.quest_message_index = None
        game_stats.quest_message_panel = None
        game_stats.event_panel_det = None
        game_basic.update_new_tasks_status(the_settlement)


def pass_on_this_opportunity():
    quest, the_realm = quest_message_details()

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            break

    remove_quest_message(quest.name)
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def track_the_dragon():
    quest, the_realm = quest_message_details()
    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            # print(the_settlement.name)
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
        units_list = list(create_unit.LE_units_dict_by_alignment["Neutrals"])
        # Add regiments to created army
        for army in game_obj.game_armies:
            if army.army_id == game_stats.army_id_counter:
                # Add grey dragon
                army.units.append(copy.deepcopy(units_list[4]))

                game_basic.establish_leader(game_stats.army_id_counter, "Game")

                army.event = game_classes.Post_Battle_Event("Slay the Grey dragon",
                                                            int(quest.settlement_location),
                                                            str(the_realm.name))
                break

        # Add new quest to eliminate rogue army
        the_realm.quests_messages.append(game_classes.Quest_Message("Slay the Grey dragon",
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

    game_stats.dilemma_additional_options = []
    remove_quest_message("Grey dragon slayer")
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def send_party_of_huntsmen():
    quest, the_realm = quest_message_details()

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            break

    game_stats.dilemma_additional_options = []
    remove_quest_message(quest.name)
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def trade_with_dwarves():
    quest, the_realm = quest_message_details()

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            break

    if game_basic.enough_resources_to_pay([["Florins", 2500]]):
        game_basic.realm_payment(the_realm.name, [["Florins", 2500]])
        game_basic.realm_income(the_realm.name, [["Armament", 2500]])

        remove_quest_message("Dwarven caravan")
        game_stats.quest_message_index = None
        game_stats.quest_message_panel = None
        game_stats.event_panel_det = None
        game_basic.update_new_tasks_status(the_settlement)


def dwarves_spend_money():
    quest, the_realm = quest_message_details()

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            break

    for pops in the_settlement.residency:
        if pops.name == "Merchants":
            game_basic.simple_add_resources(pops.reserve, [["Florins", 250]])
            break

    remove_quest_message(quest.name)
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def promise_to_supply_stone():
    quest, the_realm = quest_message_details()
    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            print(the_settlement.name)
            break

    # Add new quest to provide stone to vassal
    the_realm.quests_messages.append(game_classes.Quest_Message("Provide stone to vassal",
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

    remove_quest_message(quest.name)
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def provide_troops_to_vassal():
    quest, the_realm = quest_message_details()
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

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            settlement.local_effects.append(effect)

            # Adjust recruitment
            for plot in settlement.buildings:
                if plot.structure is not None:
                    if len(plot.structure.recruitment) > 0:
                        if plot.status == "Built":
                            for lodge in plot.structure.recruitment:
                                if "men-at-arms" in recruitment_structures.unit_tags[lodge.unit_name]:
                                    lodge.time_passed = 0
                                    lodge.ready_units = 0
            break

    remove_quest_message(quest.name)
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def reject_request_for_stone_materials():
    quest, the_realm = quest_message_details()
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

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            settlement.local_effects.append(effect2)
            # Adjust faction loyalty
            for faction in settlement.factions:
                if faction.name == "Nobility estate":
                    faction.loyalty -= 2
            break

    remove_quest_message(quest.name)
    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_basic.update_new_tasks_status(the_settlement)


def forrest_law_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: forrest_law_upheld,
                                                              2: forrest_law_lenient},
                                                             [[281, 380, 421, 400],
                                                              [281, 425, 421, 445]],
                                                             [277, 143, 677, 538],
                                                             None)


def rule_of_monastic_life_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: rule_of_monastic_life_ignore,
                                                              2: rule_of_monastic_life_aid_reform},
                                                             [[281, 398, 421, 418],
                                                              [281, 443, 421, 463]],
                                                             [277, 143, 677, 538],
                                                             None)


def favor_abbeys_lands_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: grant_land_holdings,
                                                              2: pass_on_this_opportunity},
                                                             [[281, 380, 431, 400],
                                                              [281, 425, 431, 445]],
                                                             [277, 143, 677, 538],
                                                             None)


def monastery_school_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: support_monastery_school,
                                                              2: pass_on_this_opportunity},
                                                             [[281, 394, 431, 414],
                                                              [281, 439, 431, 459]],
                                                             [277, 143, 677, 538],
                                                             None)


def grey_dragon_slayer_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: track_the_dragon},
                                                             [[281, 340, 421, 360]],
                                                             [277, 143, 677, 538],
                                                             None)

    the_realm = None
    for realm in game_obj.game_powers:
        if realm.name == game_stats.player_power:
            the_realm = realm
            break

    if the_realm.leader.lifestyle_traits[0] == "Hunter" or the_realm.leader.lifestyle_traits[1] == "Hunter":
        game_stats.event_panel_det.obj_funs[2] = send_party_of_huntsmen
        game_stats.event_panel_det.obj_button_zone.append([281, 390, 421, 410])
        game_stats.dilemma_additional_options.append("Leader trait - Hunter")


def dwarven_caravan_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: trade_with_dwarves,
                                                              2: dwarves_spend_money},
                                                             [[281, 380, 431, 400],
                                                              [281, 425, 431, 445]],
                                                             [277, 143, 677, 538],
                                                             None)


def desolated_defences_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: promise_to_supply_stone,
                                                              2: provide_troops_to_vassal,
                                                              3: reject_request_for_stone_materials},
                                                             [[281, 380, 431, 400],
                                                              [281, 425, 431, 445],
                                                              [281, 470, 431, 495]],
                                                             [277, 143, 677, 538],
                                                             None)


def quest_message_details():
    quest_log = None
    the_realm = None
    for realm in game_obj.game_powers:
        if realm.name == game_stats.player_power:
            quest_log = realm.quests_messages
            the_realm = realm
            break

    return quest_log[game_stats.quest_message_index], the_realm


def remove_quest_message(quest_name):
    for realm in game_obj.game_powers:
        if realm.name == game_stats.player_power:
            for quest_message in realm.quests_messages:
                if quest_message.name == quest_name:
                    realm.quests_messages.remove(quest_message)
                    break
            break


details_dict = {"Forest law" : forrest_law_det,
                "Rule of Monastic Life" : rule_of_monastic_life_det,
                "Favor abbey's lands" : favor_abbeys_lands_det,
                "Monastery school" : monastery_school_det,
                "Grey dragon slayer" : grey_dragon_slayer_det,
                "Dwarven caravan" : dwarven_caravan_det,
                "Desolated defences" : desolated_defences_det}
