## Among Myth and Wonder
## strategy_logic

import math
import random

from Resources import game_obj
from Resources import game_stats
from Resources import game_diplomacy
from Resources import algo_circle_range
from Resources import game_pathfinding
from Resources import game_basic
from Resources import common_selects
from Resources import common_lists

from Strategy_AI import diplomacy_logic
from Strategy_AI import economy_logic
from Strategy_AI import quest_logic

from Strategy_AI.Logic_Solutions import immediate_targets
from Strategy_AI.Logic_Solutions import territory_targets
from Strategy_AI.Logic_Solutions import military_expedition
from Strategy_AI.Logic_Solutions import explore_neutral_lands
from Strategy_AI.Logic_Solutions import adventure_role_AI


def manage_realm():
    # print("")
    # print("manage_realm()")
    ## Quest log
    for realm in game_obj.game_powers:
        if realm.AI_player:
            quest_logic.manage_messages(realm)

    ## Diplomacy
    ## Diplomatic messages
    for realm in game_obj.game_powers:
        if realm.AI_player:
            accept_everything_AI(realm)

    ## Turn start operations
    ## Diplomacy
    for realm in game_obj.game_powers:
        if realm.AI_player:
            if realm.AI_cogs.cognition_stage == "Diplomacy":
                # Always propose white peace
                # diplomacy_logic.propose_white_peace_to_humans_AI(realm)
                # Always propose peace offer
                diplomacy_logic.propose_peace_agreement_to_humans_AI(realm)
                # # Always declare war
                diplomacy_logic.attack_humans_AI(realm)

    ## Manage building new structures, creating armies, hiring regiments and heroes
    for realm in game_obj.game_powers:
        if realm.AI_player:
            if realm.AI_cogs.cognition_stage == "Economy":
                economy_logic.manage_economy(realm)

    ## Manage armies
    for realm in game_obj.game_powers:
        if realm.AI_player:
            manage_armies(realm)

    ## Turn end
    for realm in game_obj.game_powers:
        if realm.AI_player:
            idle_AI(realm)


def idle_AI(realm):
    # Test module
    # Pass the turn without actions
    if realm.AI_cogs.cognition_stage == "Finished turn":
        # print(realm.name + " cognition_stage - " + str(realm.AI_cogs.cognition_stage))
        if not realm.turn_completed:
            realm.turn_completed = True


def accept_everything_AI(realm):
    # Test module
    realm_name = str(realm.name)
    if realm.diplomatic_messages:
        for message in realm.diplomatic_messages:
            print(message.dm_from + " => " + message.dm_to + " message.subject - " + str(message.subject))
            if message.subject == "White peace":
                game_diplomacy.accept_white_peace(realm.diplomatic_messages, message)
                print(realm.name + " // messages: " + str(len(realm.diplomatic_messages)))

            elif message.subject == "Surrender request":
                game_diplomacy.accept_peace_agreement(realm.diplomatic_messages, message)

            elif message.subject == "Capitulation offer":
                game_diplomacy.accept_peace_agreement(realm.diplomatic_messages, message)

            elif message.subject == "Threat":
                # Conditions
                all_conditions_met = True
                controlled_settlements = 0
                for settlement in game_obj.game_cities:
                    if settlement.owner == realm_name:
                        controlled_settlements += 1

                check_available_settlements = False
                settlements_names = []
                for demand in message.contents:
                    if demand[2] == "Territory concession":
                        settlements_names.append(demand[0])
                        check_available_settlements = True
                        all_conditions_met = False

                print("check_available_settlements - " + str(check_available_settlements))
                if check_available_settlements:
                    print("controlled_settlements - " + str(controlled_settlements))
                    if controlled_settlements > 1:
                        found_settlements = 0
                        for settlement in game_obj.game_cities:
                            if settlement.name in settlements_names:
                                if not settlement.military_occupation:
                                    found_settlements += 1

                        if found_settlements == len(settlements_names):
                            all_conditions_met = True

                if all_conditions_met:
                    game_diplomacy.accept_threat_demand(realm.diplomatic_messages, message)
                    print(realm.name + " // messages: " + str(len(realm.diplomatic_messages)))
                else:
                    # Discard message
                    message.discard = True

    # realm.diplomatic_messages = []


def manage_armies(realm):
    friendly_cities, hostile_cities, at_war_list = game_pathfinding.find_friendly_cities(realm.name)

    if realm.AI_cogs.cognition_stage == "Manage armies":
        # War orders
        war_orders_AI(realm, friendly_cities, hostile_cities, at_war_list)

        # Local adventures and exploration of new territories
        adventure_orders(realm, friendly_cities, hostile_cities, at_war_list)

        # Return to base
        return_to_base(realm, friendly_cities, hostile_cities)

    # Test module
    # Change armies roles and give out orders
    # if realm.AI_cogs.cognition_stage == "Manage armies":
    #     all_offensive_AI(realm)
    #
    #     # Give commands to armies
    #     command_armies(realm)


def all_offensive_AI(realm):
    all_finished = True
    for role in realm.AI_cogs.army_roles:
        print("role: " + str(role.army_id) + ", " + str(role.army_role))
        if role.army_role not in ["Finished", "Nothing to do"]:
            all_finished = False

            if role.army_role == "Idle":
                role.army_role = "Conquest"

    if all_finished:
        realm.AI_cogs.cognition_stage = "Finished turn"


def command_armies(realm):
    target_names = []
    for target in realm.relations.at_war:
        target_names.append(str(target[2]))

    occupied_targets = []
    for role in realm.AI_cogs.army_roles:
        if role.army_role == "Conquest":
            for army in game_obj.game_armies:
                if army.army_id == role.army_id and army.action == "Stand":
                    available_targets = []

                    min_movement_points = None
                    for regiment in army.units:
                        if min_movement_points is None:
                            min_movement_points = regiment.movement_points
                        elif regiment.movement_points < min_movement_points:
                            min_movement_points = regiment.movement_points

                    print("army_id - " + str(army.army_id) + "; min_movement_points - " + str(min_movement_points))
                    if min_movement_points < 100:
                        # Not enough movement points to move
                        role.army_role = "Finished"

                    else:
                        move_range = math.floor(min_movement_points / 100)

                        for tile in algo_circle_range.within_circle_range(army.posxy, move_range):
                            if tile in realm.known_map:
                                TileNum = (tile[1] - 1) * game_stats.cur_level_width + tile[0] - 1
                                TileObj = game_obj.game_map[TileNum]
                                if TileObj.lot:
                                    if TileObj.lot == "City":
                                        for settlement in game_obj.game_cities:
                                            if settlement.city_id == TileObj.city_id:
                                                if settlement.owner in target_names:
                                                    if settlement.military_occupation:
                                                        if settlement.military_occupation[2] in target_names:
                                                            permit = True
                                                            for new_target in occupied_targets:
                                                                if new_target[0] == "Settlement" and \
                                                                        new_target[2] == settlement.city_id:
                                                                    permit = False
                                                            if permit:
                                                                available_targets.append(["Settlement", list(tile),
                                                                                          int(settlement.city_id)])
                                                    else:
                                                        permit = True
                                                        for new_target in occupied_targets:
                                                            if new_target[0] == "Settlement" and \
                                                                    new_target[2] == settlement.city_id:
                                                                permit = False
                                                        if permit:
                                                            available_targets.append(["Settlement", list(tile),
                                                                                      int(settlement.city_id)])
                                                break

                                elif TileObj.army_id:
                                    # print("Army in range; army_id - " + str(TileObj.army_id))
                                    for enemy_army in game_obj.game_armies:
                                        if enemy_army.army_id == TileObj.army_id:
                                            if enemy_army.owner in target_names:
                                                permit = True
                                                for new_target in occupied_targets:
                                                    if new_target[0] == "Army" and \
                                                            new_target[2] == TileObj.army_id:
                                                        permit = False
                                                if permit:
                                                    available_targets.append(["Army", list(tile),
                                                                              int(enemy_army.army_id)])
                                            break

                        if len(available_targets) == 0:
                            role.army_role = "Nothing to do"
                        else:
                            print("available_targets: " + str(available_targets))
                            num = 0
                            distance = None
                            index = 0
                            for target in available_targets:
                                if distance is None:
                                    distance = math.sqrt(((army.posxy[0] - target[1][0]) ** 2) + (
                                                         (army.posxy[1] - target[1][1]) ** 2))
                                    index = int(num)
                                else:
                                    new_distance = math.sqrt(((army.posxy[0] - target[1][0]) ** 2) + (
                                                             (army.posxy[1] - target[1][1]) ** 2))
                                    if new_distance < distance:
                                        distance = float(new_distance)
                                        index = int(num)
                                num += 1

                                selected_target = available_targets.pop(index)
                                occupied_targets.append(selected_target)
                                game_pathfinding.search_army_movement("AI",
                                                                      int(army.army_id),
                                                                      str(realm.name),
                                                                      selected_target[1])
                                army.action = "Ready to move"

                    break


def war_orders_AI(realm, friendly_cities, hostile_cities, at_war_list):
    print("")
    all_finished = True
    military_targets = common_lists.legitimate_settlement_targets(realm)

    for role in realm.AI_cogs.army_roles:
        print("war_orders_AI - role: " + str(role.army_id) + ", " + str(role.army_role))
        if role.army_role not in ["Nothing to do"] and role.status != "Finished":
            all_finished = False

            if role.army_role == "Idle" or role.army_role in\
                    ["Advance - enemy army", "Advance - enemy settlement", "Advance - liberate settlement",
                     "Exploration"]:
                # if role.army_role == "Idle":
                #     role.army_role = "Nothing to do"  # Preemptively

                army = common_selects.select_army_by_id(role.army_id)
                print("Army " + str(army.army_id) + " is " + army.action.lower())
                new_war_order = False
                if army.shattered == "Shattered":
                    # Shouldn't go to adventure
                    print("Army is shattered")
                    pass
                elif army.action in ["Fighting", "Besieged", "Besieging"]:
                    # Shouldn't go to adventure due to fighting
                    print("Army " + str(army.army_id) + " is busy " + army.action.lower())
                    if army.action == "Besieging" and role.status == "Start":
                        print("Army " + str(army.army_id) + " is besieging a settlement")
                        print("Role - " + str(role.army_role) + "; role.status - " + str(role.status))
                        facilitate_siege(army, realm)

                ## elif role.army_role == "Adventure":

                else:
                    if len(army.route) > 0:
                        print("war_orders_AI - 1; army.action - " + str(army.action))
                        next_point = list(army.route[-1])
                        TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1
                        TileObj = game_obj.game_map[TileNum]

                        if role.army_role == "Advance - enemy army":
                            # Confirm that target still available
                            print("next_point - " + str(next_point) + "; TileObj.army_id - " + str(TileObj.army_id)
                                  + "; role.target_army_id - " + str(role.target_army_id))
                            if TileObj.army_id != role.target_army_id:
                                adjust_path(army, role, "Army")
                        else:
                            army.action = "Ready to move"

                    else:
                        print("war_orders_AI - 2; army.action - " + str(army.action))
                        # print("len(army.units): " + str(len(army.units)))
                        if len(army.units) >= 5 and army.hero is not None:
                            if game_obj.game_map[army.location].city_id is not None:
                                new_war_order = True

                if not at_war_list:
                    # If there is no enemy realms at war with this realm,
                    # then there is no need to give military orders
                    new_war_order = False

                if new_war_order:
                    while True:
                        print("new_war_order")
                        next_order = False
                        next_order = immediate_targets.solution(realm, role, army, friendly_cities,
                                                                hostile_cities, at_war_list)
                        if next_order:
                            next_order = territory_targets.solution(realm, role, army, friendly_cities,
                                                                    hostile_cities, at_war_list)
                        else:
                            break

                        if next_order:
                            next_order = military_expedition.solution(realm, role, army, friendly_cities,
                                                                      hostile_cities, military_targets)

                        else:
                            break

                        if next_order:
                            if role.army_role in ["Advance - enemy army", "Advance - enemy settlement",
                                                  "Advance - liberate settlement"]:
                                role.army_role = "Idle"

                        break

    if all_finished:
        print("war_orders_AI: cognition_stage = Finished turn")
        print("")
        realm.AI_cogs.cognition_stage = "Finished turn"


def adventure_orders(realm, friendly_cities, hostile_cities, at_war_list):
    print("")
    all_finished = True
    for role in realm.AI_cogs.army_roles:
        print("adventure_orders - role: " + str(role.army_id) + ", " + str(role.army_role))
        army = common_selects.select_army_by_id(role.army_id)
        busy_fighting = False
        if army.action in ["Fighting", "Besieged", "Besieging"]:
            # Shouldn't go to adventure due to fighting
            print("Army " + str(army.army_id) + " is busy " + army.action.lower())
            busy_fighting = True

        if not busy_fighting:
            if role.army_role in ["Idle", "Nothing to do"]:
                print("role: " + str(role.army_id) + ", " + str(role.army_role))

            if role.army_role not in ["Nothing to do"] and role.status != "Finished":
                all_finished = False
                print("Could do something")

                if role.army_role == "Idle" or role.army_role == "Adventure":
                    if role.army_role == "Idle":
                        role.army_role = "Nothing to do"  # Preemptively

                    adventure_role_AI.solution(realm, role, friendly_cities, hostile_cities, at_war_list, army)

                if role.army_role == "Nothing to do" or role.army_role == "Exploration":
                    explore_neutral_lands.solution(realm, role, friendly_cities, hostile_cities, at_war_list, army)

    if all_finished:
        print("adventure_role_AI: cognition_stage = Finished turn")
        print("")
        realm.AI_cogs.cognition_stage = "Finished turn"


def return_to_base(realm, friendly_cities, hostile_cities):
    print("")
    all_finished = True
    for role in realm.AI_cogs.army_roles:
        print("return_to_base - role: " + str(role.army_id) + "; " + str(role.army_role) + "; " + str(role.status))

        army = None
        for the_army in game_obj.game_armies:
            if the_army.army_id == role.army_id:
                army = the_army
                break

        if role.army_role in ["Adventure", "Advance - enemy army"] and role.status != "Finished":
            all_finished = False
            if army.shattered == "Shattered" and army.action != "Routing":
                # This will make this army to return to settlement
                role.army_role = "Nothing to do"

        if role.army_role in ["Nothing to do"] and role.status != "Finished":
            print("role.army_role in ['Nothing to do'] and role.status != 'Finished'")
            # all_finished = False
            role.status = "Finished"  # Preemptively (might delete this line later)

            print("army.army_id = " + str(army.army_id) + "; army.action - " + str(army.action))
            city_id_in_location = game_obj.game_map[army.location].city_id
            issued_order = False
            if army.action == "Routing":
                # Army is routing
                print("Army is shattered")
                issued_order = True
            elif city_id_in_location is not None:
                for settlement in game_obj.game_cities:
                    if settlement.city_id == city_id_in_location and settlement.owner == army.owner and\
                            settlement.military_occupation is None:
                        # print("settlement.military_occupation is None")
                        # print("settlement.city_id == city_id_in_location")
                        if settlement.location == army.location:
                            # Army is already garrisoned at settlement
                            print("Army is already garrisoned at settlement")
                            issued_order = True  # Even so order is to stay
                        else:
                            print("settlement.location - " + str(settlement.location) +
                                  "; settlement.posxy - " + str(settlement.posxy))
                            print("game_obj.game_map[settlement.location].army_id = " +
                                  str(game_obj.game_map[settlement.location].army_id))
                            if game_obj.game_map[settlement.location].army_id is None:
                                print("game_obj.game_map[settlement.location].army_id is None")
                                # Settlement is neither occupied nor accommodates another army
                                all_finished = False
                                realm.AI_cogs.cognition_stage = "Manage armies"
                                destination_to_base(realm, role, army, settlement,
                                                    friendly_cities, hostile_cities)
                                issued_order = True
                        break

            if not issued_order:
                for settlement in game_obj.game_cities:
                    if settlement.city_id == role.base_of_operation and settlement.military_occupation is None\
                            and game_obj.game_map[settlement.location].army_id is None:
                        print("Returning to the base of operation: " + settlement.name + "; city_id - " +
                              str(settlement.city_id))
                        all_finished = False
                        realm.AI_cogs.cognition_stage = "Manage armies"
                        destination_to_base(realm, role, army, settlement,
                                            friendly_cities, hostile_cities)

                        break

        elif role.army_role == "Travel to settlement":
            # if role.status == "Start":
            #     all_finished = False
            print("Travel to settlement: army.action - " + str(army.action))
            if army.action != "Stand":
                all_finished = False
                # Verification that next tile on a path is not blocked
                if len(army.route) > 0:
                    next_point = list(army.route[0])
                    TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1
                    TileObj = game_obj.game_map[TileNum]
                    if TileObj.army_id is not None:
                        army.action = "Stand"
                        army.route = []
                        army.path_arrows = []
                        print("1) Path to settlement is blocked by army " + str(TileObj.army_id))
            elif army.action == "Stand":
                give_command_to_move = True

                if game_obj.game_map[army.location].lot is not None:
                    if game_obj.game_map[army.location].lot == "City":
                        give_command_to_move = False
                        role.army_role = "Nothing to do"
                        role.status = "Finished"
                        print("Army has returned to settlement")

                if len(army.route) == 0:
                    # Most likely army's path has been blocked by someone
                    give_command_to_move = False
                    role.army_role = "Idle"
                    all_finished = False

                else:
                    next_point = list(army.route[0])
                    TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1
                    TileObj = game_obj.game_map[TileNum]
                    if TileObj.army_id is not None:
                        army.action = "Stand"
                        army.route = []
                        army.path_arrows = []
                        give_command_to_move = False
                        role.army_role = "Idle"
                        all_finished = False
                        print("2) Path to settlement is blocked by army " + str(TileObj.army_id))

                # If army hasn't reached settlement yet but doesn't have movement points to travel
                # It must change status to Finished
                # This prevent army from making fake animation of moving over map
                if give_command_to_move:
                    if role.status == "Finished":
                        give_command_to_move = False
                        print("No movement points left")

                if give_command_to_move:
                    army.action = "Ready to move"
                    all_finished = False
                    print("New action: army.action - " + str(army.action))

    if all_finished:
        print("return_to_base: cognition_stage = Finished turn")
        print("")
        realm.AI_cogs.cognition_stage = "Finished turn"


def destination_to_base(realm, role, army, settlement, friendly_cities, hostile_cities):
    # print("destination_to_base")
    role.army_role = "Travel to settlement"
    game_pathfinding.search_army_movement("AI",
                                          int(army.army_id),
                                          str(realm.name),
                                          settlement.posxy)
    # print("After game_pathfinding.search_army_movement")
    if game_basic.enough_movement_points(army):
        army.action = "Ready to move"
        role.status = "Start"
        print("Destination - " + str(settlement.posxy) + " " + settlement.name + " len(army.route) - "
              + str(len(army.route)))
        # print("First step - " + str(army.route[0]) + "; army.posxy - " + str(army.posxy))
    else:
        role.status = "Finished"
        print("Not enough movement points to travel towards settlement")


def facilitate_siege(attacker, attacker_realm):
    if game_stats.game_board_panel not in ["settlement blockade panel", "autobattle conclusion panel"]:
        # Check to make sure that AI avoid to repeat siege action if siege window has already popped up
        settlement, defender = game_basic.find_siege(attacker)
        game_basic.AI_blockade_settlement(settlement, attacker, defender, attacker_realm)


def complete_war_order(army, army_realm):
    print("complete_war_order(): " + army_realm.name + "; army_id " + str(army.army_id))
    if army_realm.AI_player:
        the_role = common_selects.select_army_role_by_id(army_realm, army.army_id)

        if the_role:
            if the_role.army_role in ["Advance - enemy army",
                                      "Advance - enemy settlement",
                                      "Advance - liberate settlement"]:
                the_role.army_role = "Idle"
            # print("army_role - " + str(the_role.army_role))


def adjust_path(the_army, role, target_type):
    print("")
    print("adjust_path()")
    print("target_type - " + str(target_type))
    if target_type == "Army":
        target_army = common_selects.select_army_by_id(role.target_army_id)
        print("target_army.army_id - " + str(target_army.army_id))

        if target_army:
            print("adjust_path(): new path towards " + str(target_army.posxy))
            game_pathfinding.search_army_movement("AI",
                                                  int(the_army.army_id),
                                                  str(the_army.owner),
                                                  list(target_army.posxy))

        else:
            print("adjust_path(): can't find army " + str(role.target_army_id))
            the_army.action = "Stand"
            the_army.route = []
            the_army.path_arrows = []
            role.target_army_id = 0
            role.army_role = "Idle"
