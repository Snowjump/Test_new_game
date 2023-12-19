## Among Myth and Wonder

from Resources import game_stats
from Resources import game_obj
from Resources import game_classes
from Resources import update_gf_game_board
from Resources import game_basic


def find_target():
    quest, the_realm = quest_message_details()

    new_pov = None
    if quest.target_type == "Army":
        for army in game_obj.game_armies:
            if army.army_id == quest.target_id:
                if army.posxy in the_realm.known_map:
                    new_pov = list(army.posxy)
                break

    if new_pov is None:
        for settlement in game_obj.game_cities:
            if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
                new_pov = list(settlement.posxy)
                break

    print("new_pov - " + str(new_pov))
    game_stats.pov_pos = [new_pov[0] - 14, new_pov[1] - 8]

    game_stats.quest_message_index = None
    game_stats.quest_message_panel = None
    game_stats.event_panel_det = None
    game_stats.game_board_panel = ""

    # Update visuals
    update_gf_game_board.update_sprites()


def provide_stone_materials():
    quest, the_realm = quest_message_details()
    print(quest.name)

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[quest.settlement_location].city_id:
            the_settlement = settlement
            print(the_settlement.name)
            break

    enough_resources = False
    for res in the_realm.coffers:
        if res[0] == "Stone":
            if res[1] >= 1600:
                res[1] -= 1600
                enough_resources = True
            break

    if enough_resources:
        for effect in the_settlement.local_effects:
            if effect.name == "Vassal awaits for stone":
                the_settlement.local_effects.remove(effect)
                break

        for faction in the_settlement.factions:
            if faction.name == "Nobility estate":
                faction.loyalty += 1
                break

        remove_quest_message(quest.name)
        game_stats.quest_message_index = None
        game_stats.quest_message_panel = None
        game_stats.event_panel_det = None
        game_basic.update_new_tasks_status(the_settlement)


def poachers_in_royal_forest_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: find_target},
                                                             [[281, 290, 395, 310]],
                                                             [244, 143, 637, 538],
                                                             None)


def slay_the_grey_dragon_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: find_target},
                                                             [[281, 290, 395, 310]],
                                                             [244, 143, 637, 538],
                                                             None)


def provide_stone_to_vassal_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: provide_stone_materials},
                                                             [[281, 330, 395, 350]],
                                                             [244, 143, 637, 538],
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
                print("quest_message.name - " + quest_message.name)
                if quest_message.name == quest_name:
                    realm.quests_messages.remove(quest_message)
                    break
            break


details_dict = {"Poachers in Royal forest" : poachers_in_royal_forest_det,
                "Slay the Grey dragon" : slay_the_grey_dragon_det,
                "Provide stone to vassal" : provide_stone_to_vassal_det}
