## Miracle battles
## knight_lords_quest_result_scripts

# Scripts are executed either due to elimination of the quest army or running out of time to complete the quest
# (then army = None)

from Resources import game_stats
from Resources import game_obj
from Resources import game_classes
from Resources import campaign_effect_classes


def quest_message_close():
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def poachers_in_royal_forest_result(army, army_realm, quest_event):
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest_event.settlement_location].city_id:
            for faction in settlement.factions:
                if faction.name == "Nobility estate":
                    faction.loyalty += 1

            # print("quest_event.name - " + quest_event.name)
            for effect in settlement.local_effects:
                # print("Effect name - " + effect.name)
                if effect.name == quest_event.name:
                    settlement.local_effects.remove(effect)
                    break
            break

    for realm in game_obj.game_powers:
        if realm.name == quest_event.realm_name:
            for quest_message in realm.quests_messages:
                if quest_message.name == quest_event.name:
                    realm.quests_messages.remove(quest_message)
                    break
            break

    if army.owner == quest_event.realm_name:
        if not army_realm.AI_player:
            game_stats.game_board_panel = "poachers in royal forest result panel"
            game_stats.event_panel_det = game_classes.Object_Surface({1: quest_message_close},
                                                                     [[611, 406, 670, 426]],
                                                                     [481, 101, 800, 430],
                                                                     None)


def slay_the_grey_dragon_result(army, army_realm, quest_event):
    effect = campaign_effect_classes.Settlement_Effect("Slayer of the Grey dragon",
                                                       "Settlement",
                                                       "Loyalty",
                                                       [campaign_effect_classes.Faction_Effect("Nobility estate",
                                                                                               "Loyalty",
                                                                                               1,
                                                                                               "Addition")
                                                        ],
                                                       15)
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest_event.settlement_location].city_id:
            settlement.local_effects.append(effect)

            for faction in settlement.factions:
                # Restore loyalty
                if faction.name in ["Nobility estate", "Peasant estate"]:
                    faction.loyalty += 1

                # Increase bonus loyalty
                if faction.name == "Nobility estate":
                    faction.loyalty += 1

            # print("quest_event.name - " + quest_event.name)
            for effect in settlement.local_effects:
                # print("Effect name - " + effect.name)
                if effect.name == quest_event.name:
                    settlement.local_effects.remove(effect)
                    break
            break

    for realm in game_obj.game_powers:
        if realm.name == quest_event.realm_name:
            for quest_message in realm.quests_messages:
                if quest_message.name == quest_event.name:
                    realm.quests_messages.remove(quest_message)
                    break
            break

    if army.owner == quest_event.realm_name:
        if not army_realm.AI_player:
            game_stats.game_board_panel = "slay the grey dragon result panel"
            game_stats.event_panel_det = game_classes.Object_Surface({1: quest_message_close},
                                                                     [[611, 406, 670, 426]],
                                                                     [481, 101, 800, 430],
                                                                     None)


def failed_to_provide_stone_to_vassal(army, army_realm, quest_event):
    effect = campaign_effect_classes.Settlement_Effect("Failed to provide stone",
                                                       "Settlement",
                                                       "Loyalty",
                                                       [campaign_effect_classes.Faction_Effect("Nobility estate",
                                                                                               "Loyalty",
                                                                                               2,
                                                                                               "Subtraction")
                                                        ],
                                                       25)

    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest_event.settlement_location].city_id:
            settlement.local_effects.append(effect)

            for local_effect in settlement.local_effects:
                if local_effect.name == "Vassal awaits for stone":
                    settlement.local_effects.remove(local_effect)
                    break

            # Subtract loyalty even further
            for faction in settlement.factions:
                # Subtract loyalty
                if faction.name == "Nobility estate":
                    faction.loyalty -= 1
            break


result_scripts = {
    "Poachers in Royal forest" : poachers_in_royal_forest_result,
    "Slay the Grey dragon" : slay_the_grey_dragon_result,
    "Provide stone to vassal" : failed_to_provide_stone_to_vassal}
