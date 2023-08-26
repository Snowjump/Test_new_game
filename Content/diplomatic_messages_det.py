## Miracle battles!

from Resources import game_classes
from Resources import game_stats
from Resources import game_obj
from Resources import game_basic


def acknowledge_and_close():
    notification_log = game_stats.selected_diplomatic_notifications
    letter = notification_log[game_stats.diplomatic_message_index]
    realm_name = str(letter.dm_to)

    for realm in game_obj.game_powers:
        if realm.name == realm_name:
            del realm.diplomatic_messages[game_stats.diplomatic_message_index]
            # remove_diplomatic_message(realm, letter)
            alt_update_new_tasks_status(realm)
            break

    game_stats.diplomatic_message_index = None
    game_stats.diplomatic_message_panel = None
    game_stats.event_panel_det = None


def accept_white_peace():
    notification_log = game_stats.selected_diplomatic_notifications
    letter = notification_log[game_stats.diplomatic_message_index]
    realm_name = str(letter.dm_to)

    player = None
    for realm in game_obj.game_powers:
        if realm.name == letter.dm_to:
            player = realm
            break

    opponent = None
    for realm in game_obj.game_powers:
        if realm.name == letter.dm_from:
            opponent = realm
            break

    # Remove war
    # print("message.dm_from - " + str(message.dm_from) + "; message.dm_to - " + str(message.dm_to))
    num = 0
    for war in game_obj.game_wars:
        # print("num - " + str(num) + "; war.initiator - " + str(war.initiator) +
        #       "; war.respondent - " + str(war.respondent))
        if war.initiator == letter.dm_from \
                or war.initiator == letter.dm_to:
            if war.respondent == letter.dm_from \
                    or war.respondent == letter.dm_to:
                # print("break: num - " + str(num))
                break
        num += 1

    del game_obj.game_wars[num]

    # Remove occupation
    for settlement in game_obj.game_cities:
        if settlement.owner == letter.dm_to:
            if settlement.military_occupation:
                if settlement.military_occupation[2] == letter.dm_from:
                    settlement.military_occupation = None
        elif settlement.owner == letter.dm_from:
            if settlement.military_occupation:
                if settlement.military_occupation[2] == letter.dm_to:
                    settlement.military_occupation = None

    # Remove war notification
    num = 0
    for notification in game_stats.ongoing_wars:
        if notification[2] in [letter.dm_from, letter.dm_to]:
            break
        num += 1

    del game_stats.ongoing_wars[num]

    if game_stats.war_notifications_index > 0:
        game_stats.war_notifications_index -= 1

    # Remove from lists of ongoing wars
    num = 0
    for enemy in opponent.relations.at_war:
        if enemy[2] == letter.dm_to:
            break
        num += 1
    if num < len(opponent.relations.at_war):
        del opponent.relations.at_war[num]

    num = 0
    for enemy in player.relations.at_war:
        if enemy[2] == letter.dm_from:
            break
        num += 1
    if num < len(player.relations.at_war):
        del player.relations.at_war[num]

    # Move out all armies from foreign settlements and finish sieges
    for army in game_obj.game_armies:
        if army.owner == letter.dm_from:
            if army.action in ["Stand", "Ready to move", "Moving", "Routing"]:
                if game_obj.game_map[army.location].lot:
                    if game_obj.game_map[army.location].lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.city_id == game_obj.game_map[army.location].city_id:
                                if settlement.owner == letter.dm_to:
                                    game_basic.move_out_army_from_settlement(army)
                                    break
            elif army.action == "Besieging":
                settlement, defender = game_basic.find_siege(army)
                if defender.owner == letter.dm_to:
                    game_basic.finish_settlement_blockade(settlement, army, defender)

        elif army.owner == letter.dm_to:
            if army.action in ["Stand", "Ready to move", "Moving", "Routing"]:
                if game_obj.game_map[army.location].lot:
                    if game_obj.game_map[army.location].lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.city_id == game_obj.game_map[army.location].city_id:
                                if settlement.owner == letter.dm_from:
                                    game_basic.move_out_army_from_settlement(army)
                                    break
            elif army.action == "Besieging":
                settlement, defender = game_basic.find_siege(army)
                if defender.owner == letter.dm_from:
                    game_basic.finish_settlement_blockade(settlement, army, defender)

    # Remove message
    for realm in game_obj.game_powers:
        if realm.name == realm_name:
            del realm.diplomatic_messages[game_stats.diplomatic_message_index]
            # remove_diplomatic_message(realm, letter)
            alt_update_new_tasks_status(realm)
            break

    game_stats.diplomatic_message_index = None
    game_stats.diplomatic_message_panel = None
    game_stats.event_panel_det = None


def decline_white_peace():
    notification_log = game_stats.selected_diplomatic_notifications
    letter = notification_log[game_stats.diplomatic_message_index]
    realm_name = str(letter.dm_to)

    # Remove message
    for realm in game_obj.game_powers:
        if realm.name == realm_name:
            del realm.diplomatic_messages[game_stats.diplomatic_message_index]
            # remove_diplomatic_message(realm, letter)
            alt_update_new_tasks_status(realm)
            break

    game_stats.diplomatic_message_index = None
    game_stats.diplomatic_message_panel = None
    game_stats.event_panel_det = None


def accept_capitulation_offer():
    notification_log = game_stats.selected_diplomatic_notifications
    letter = notification_log[game_stats.diplomatic_message_index]
    realm_name = str(letter.dm_to)

    player = None
    for realm in game_obj.game_powers:
        if realm.name == letter.dm_to:
            player = realm
            break

    opponent = None
    for realm in game_obj.game_powers:
        if realm.name == letter.dm_from:
            opponent = realm
            break

    # Remove war
    # print("message.dm_from - " + str(message.dm_from) + "; message.dm_to - " + str(message.dm_to))
    num = 0
    for war in game_obj.game_wars:
        # print("num - " + str(num) + "; war.initiator - " + str(war.initiator) +
        #       "; war.respondent - " + str(war.respondent))
        if war.initiator == letter.dm_from \
                or war.initiator == letter.dm_to:
            if war.respondent == letter.dm_from \
                    or war.respondent == letter.dm_to:
                # print("break: num - " + str(num))
                break
        num += 1

    del game_obj.game_wars[num]

    # Remove war notification
    num = 0
    for notification in game_stats.ongoing_wars:
        if notification[2] in [letter.dm_from, letter.dm_to]:
            break
        num += 1

    del game_stats.ongoing_wars[num]

    if game_stats.war_notifications_index > 0:
        game_stats.war_notifications_index -= 1

    # Remove from lists of ongoing wars
    num = 0
    for enemy in opponent.relations.at_war:
        if enemy[2] == letter.dm_to:
            break
        num += 1
    if num < len(opponent.relations.at_war):
        del opponent.relations.at_war[num]

    num = 0
    for enemy in player.relations.at_war:
        if enemy[2] == letter.dm_from:
            break
        num += 1
    if num < len(player.relations.at_war):
        del player.relations.at_war[num]

    ## Enforcing concessions
    # Transfer province ownership
    for demand in letter.contents:
        if demand[0] == "Conquest":
            for settlement in game_obj.game_cities:
                if settlement.city_id == demand[3]:
                    print("settlement.owner - " + str(settlement.owner) + "; letter.dm_to - " + str(letter.dm_to))
                    # settlement.military_occupation = None
                    settlement.owner = str(letter.dm_to)

    # Remove occupation
    for settlement in game_obj.game_cities:
        if settlement.owner == letter.dm_to:
            if settlement.military_occupation:
                if settlement.military_occupation[2] == letter.dm_from:
                    settlement.military_occupation = None
        elif settlement.owner == letter.dm_from:
            if settlement.military_occupation:
                if settlement.military_occupation[2] == letter.dm_to:
                    settlement.military_occupation = None

    # Move out all armies from foreign settlements and finish sieges
    for army in game_obj.game_armies:
        if army.owner == letter.dm_from:
            if army.action in ["Stand", "Ready to move", "Moving", "Routing"]:
                if game_obj.game_map[army.location].lot:
                    if game_obj.game_map[army.location].lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.city_id == game_obj.game_map[army.location].city_id:
                                if settlement.owner == letter.dm_to:
                                    game_basic.move_out_army_from_settlement(army)
                                    break
            elif army.action == "Besieging":
                settlement, defender = game_basic.find_siege(army)
                if defender.owner == letter.dm_to:
                    game_basic.finish_settlement_blockade(settlement, army, defender)

        elif army.owner == letter.dm_to:
            # print("army.owner - " + str(army.owner) + "; army.army_id - " + str(army.army_id))
            if army.action in ["Stand", "Ready to move", "Moving", "Routing"]:
                if game_obj.game_map[army.location].lot:
                    if game_obj.game_map[army.location].lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.city_id == game_obj.game_map[army.location].city_id:
                                if settlement.owner == letter.dm_from:
                                    # print("settlement.owner - " + str(settlement.owner)
                                    #       + "; letter.dm_from - " + str(letter.dm_from))
                                    game_basic.move_out_army_from_settlement(army)
                                    break
            elif army.action == "Besieging":
                settlement, defender = game_basic.find_siege(army)
                if defender.owner == letter.dm_from:
                    game_basic.finish_settlement_blockade(settlement, army, defender)

    # Remove message
    for realm in game_obj.game_powers:
        if realm.name == realm_name:
            del realm.diplomatic_messages[game_stats.diplomatic_message_index]
            # remove_diplomatic_message(realm, letter)
            alt_update_new_tasks_status(realm)
            break

    game_stats.diplomatic_message_index = None
    game_stats.diplomatic_message_panel = None
    game_stats.event_panel_det = None


def decline_capitulation_offer():
    notification_log = game_stats.selected_diplomatic_notifications
    letter = notification_log[game_stats.diplomatic_message_index]
    realm_name = str(letter.dm_to)

    # Remove message
    for realm in game_obj.game_powers:
        if realm.name == realm_name:
            del realm.diplomatic_messages[game_stats.diplomatic_message_index]
            # remove_diplomatic_message(realm, letter)
            alt_update_new_tasks_status(realm)
            break

    game_stats.diplomatic_message_index = None
    game_stats.diplomatic_message_panel = None
    game_stats.event_panel_det = None


def declaration_of_war_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: acknowledge_and_close},
                                                             [[421, 511, 533, 533]],
                                                             [277, 143, 677, 538],
                                                             None)


def white_peace_proposition_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: accept_white_peace,
                                                              2: decline_white_peace},
                                                             [[356, 511, 467, 533],
                                                              [486, 511, 598, 533]],
                                                             [277, 143, 677, 538],
                                                             None)


def capitulation_proposition_det():
    game_stats.event_panel_det = game_classes.Object_Surface({1: accept_capitulation_offer,
                                                              2: decline_capitulation_offer},
                                                             [[356, 511, 467, 533],
                                                              [486, 511, 598, 533]],
                                                             [277, 143, 677, 538],
                                                             None)


def alt_update_new_tasks_status(realm):
    new_tasks_exist = False
    for quest in realm.quests_messages:
        if quest.message_type == "Dilemma":
            new_tasks_exist = True
            break

    if realm.diplomatic_messages:
        new_tasks_exist = True

    if new_tasks_exist:
        game_stats.new_tasks = True
    else:
        game_stats.new_tasks = False


details_dict = {"Declaration of war" : declaration_of_war_det,
                "White peace" : white_peace_proposition_det,
                "Capitulation offer" : capitulation_proposition_det}
