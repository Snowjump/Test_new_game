## Miracle battles
## strategy_logic

import math
import random

from Resources import game_obj
from Resources import game_stats
from Resources import game_diplomacy
from Resources import algo_circle_range
from Resources import game_pathfinding
from Resources import algo_astar
from Resources import game_basic

from Strategy_AI import diplomacy_logic
from Strategy_AI import economy_logic
from Strategy_AI import AI_exploration_cond
from Strategy_AI import quest_logic


def manage_realm():
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
        # Local adventure
        adventure_role_AI(realm, friendly_cities, hostile_cities, at_war_list)

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


def adventure_role_AI(realm, friendly_cities, hostile_cities, at_war_list):
    print("")
    all_finished = True
    for role in realm.AI_cogs.army_roles:
        print("adventure_role_AI - role: " + str(role.army_id) + ", " + str(role.army_role))
        if role in ["Idle", "Nothing to do"]:
            print("role: " + str(role.army_id) + ", " + str(role.army_role))

        if role.army_role not in ["Nothing to do"] and role.status != "Finished":
            all_finished = False

            if role.army_role == "Idle" or role.army_role == "Adventure":
                # Local adventure
                if role.army_role == "Idle":
                    role.army_role = "Nothing to do"  # Preemptively

                for army in game_obj.game_armies:
                    if army.army_id == role.army_id:
                        city_id_in_location = game_obj.game_map[army.location].city_id
                        go_to_adventure = False
                        if army.shattered == "Shattered":
                            # Shouldn't go to adventure
                            print("Army is shattered")
                            pass
                        elif army.action == "Fighting":
                            # Shouldn't go to adventure due to fighting
                            print("Army " + str(army.army_id) + " is busy fighting")
                            pass
                        elif role.army_role == "Adventure":
                            print("army.route: " + str(army.route))
                            print("army.army_id = " + str(army.army_id) + "; army.action = " + str(army.action))
                            if len(army.route) == 0:
                                print("role.army_role - 'Adventure'; len(army.route) - " + str(len(army.route)))
                                go_to_adventure = True

                            else:
                                check_standing = True

                                if not game_basic.enough_movement_points(army):
                                    role.status = "Finished"
                                    check_standing = False

                                if len(army.route) > 1:
                                    next_point = list(army.route[0])
                                    TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1
                                    TileObj = game_obj.game_map[TileNum]
                                    if TileObj.army_id is not None:
                                        army.action = "Stand"
                                        army.route = []
                                        army.path_arrows = []
                                        go_to_adventure = True
                                        role.army_role = "Idle"
                                        check_standing = False
                                        print("1) Path to adventure is blocked by army " + str(TileObj.army_id))

                                if check_standing:
                                    if army.action == "Stand":
                                        army.action = "Ready to move"
                        else:
                            print("len(army.units): " + str(len(army.units)))
                            if len(army.units) >= 5 and army.hero is not None:
                                if game_obj.game_map[army.location].city_id is not None:
                                    go_to_adventure = True

                        if go_to_adventure:
                            issued_order = False
                            for settlement in game_obj.game_cities:
                                if settlement.city_id == city_id_in_location:
                                    if settlement.owner == realm.name:
                                        # role.army_role = "Adventure"
                                        assemble_adventure_destinations(realm, role, army, settlement,
                                                                        friendly_cities, hostile_cities, at_war_list)
                                        issued_order = True
                                        break

                            if not issued_order:
                                # It could happened if the army during adventuring stepped into foreign territory
                                for settlement in game_obj.game_cities:
                                    if settlement.city_id == role.base_of_operation:
                                        print(settlement.name + "; city_id - " + str(settlement.city_id))
                                        print("base_of_operation - " + str(role.base_of_operation))
                                        assemble_adventure_destinations(realm, role, army, settlement,
                                                                        friendly_cities, hostile_cities, at_war_list)
                                        break
                        break

    if all_finished:
        print("adventure_role_AI: cognition_stage = Finished turn")
        print("")
        realm.AI_cogs.cognition_stage = "Finished turn"


def assemble_adventure_destinations(realm, role, army, settlement, friendly_cities, hostile_cities, at_war_list):
    tile_list = []
    print("")
    # print("len(settlement.control_zone) : " + str(len(settlement.control_zone)))
    # print("len(realm.known_map) : " + str(len(realm.known_map)))
    # print("realm.known_map : " + str(realm.known_map))
    own_army_sum_rank = 0
    for unit in army.units:
        own_army_sum_rank += unit.rank
    print("Own army: len(army.units) - " + str(len(army.units)) + "; own_army_sum_rank - " + str(own_army_sum_rank))
    for TileNum in settlement.control_zone:
        # Adventuring on your own territory

        # print(str(tile))
        # print(str(realm.known_map))
        # print(str(game_obj.game_map[TileNum].posxy))
        if list(game_obj.game_map[TileNum].posxy) not in realm.known_map:
            distance = math.sqrt(((army.posxy[0] - game_obj.game_map[TileNum].posxy[0]) ** 2) + (
                    (army.posxy[1] - game_obj.game_map[TileNum].posxy[1]) ** 2))
            distance = math.floor(distance * 100) / 100
            tile_list.append(["Und", list(game_obj.game_map[TileNum].posxy), distance])

        # else:
            # print(str(list(game_obj.game_map[TileNum].posxy)))
        elif TileNum != army.location:
            # Exclude army's own position
            if game_obj.game_map[TileNum].lot is not None:
                if game_obj.game_map[TileNum].lot != "City":
                    map_obj = game_obj.game_map[TileNum].lot
                    # print(map_obj.obj_name)
                    if map_obj.obj_typ == "Bonus":
                        # Exploration objects
                        if map_obj.obj_name in exploration_objects_group_1:
                            if army.hero.hero_id not in map_obj.properties.hero_list \
                                    and not map_obj.properties.need_replenishment:
                                passed_verification = True
                                if map_obj.obj_name in AI_exploration_cond.event_conditions:
                                    passed_verification = AI_exploration_cond.event_conditions[map_obj.obj_name](army)
                                if passed_verification:
                                    distance = math.sqrt(((army.posxy[0] - game_obj.game_map[TileNum].posxy[0]) ** 2) +
                                                         ((army.posxy[1] - game_obj.game_map[TileNum].posxy[1]) ** 2))
                                    distance = math.floor(distance * 100) / 100
                                    tile_list.append(["Bonus", list(game_obj.game_map[TileNum].posxy), distance])
                        elif map_obj.obj_name in exploration_objects_group_2:
                            if not map_obj.properties.need_replenishment:
                                distance = math.sqrt(((army.posxy[0] - game_obj.game_map[TileNum].posxy[0]) ** 2) + (
                                        (army.posxy[1] - game_obj.game_map[TileNum].posxy[1]) ** 2))
                                distance = math.floor(distance * 100) / 100
                                tile_list.append(["Bonus", list(game_obj.game_map[TileNum].posxy), distance])

                    elif map_obj.obj_typ == "Lair":
                        # Lair objects with opportunity to fight for a prize
                        if map_obj.properties.army_id is not None:
                            print("obj.properties.army_id - " + str(map_obj.properties.army_id))
                            for target in game_obj.game_armies:
                                if target.army_id == map_obj.properties.army_id:
                                    target_sum_rank = 0
                                    for unit in target.units:
                                        target_sum_rank += unit.rank
                                    print("len(target.units) - " + str(len(target.units)) + "; target_sum_rank - " +
                                          str(target_sum_rank))

                                    rank_ratio = int(own_army_sum_rank / target_sum_rank * 100)
                                    random_risk_level = random.randint(0, 40)
                                    # Standard border is 120
                                    print("rank_ratio - " + str(rank_ratio) + "; random_risk_level - " +
                                          str(random_risk_level) + "; result - " + str(120 - random_risk_level))
                                    if rank_ratio >= 120 - random_risk_level:
                                        print("Ready to attack lair")
                                        distance = math.sqrt(
                                            ((army.posxy[0] - game_obj.game_map[TileNum].posxy[0]) ** 2) + (
                                                    (army.posxy[1] - game_obj.game_map[TileNum].posxy[1]) ** 2))
                                        distance = math.floor(distance * 100) / 100
                                        tile_list.append(["Lair", list(game_obj.game_map[TileNum].posxy), distance])
                                    break

            else:
                # Tile without a lot
                if game_obj.game_map[TileNum].army_id is not None:
                    # But there is an army
                    print("Tile.army_id - " + str(game_obj.game_map[TileNum].army_id))
                    for target in game_obj.game_armies:
                        if target.army_id == game_obj.game_map[TileNum].army_id:
                            if target.action == "Stand":
                                # Targeting standing armies
                                if target.owner == "Neutral":
                                    # Targeting neutral armies
                                    target_sum_rank = 0
                                    for unit in target.units:
                                        target_sum_rank += unit.rank
                                    print("len(target.units) - " + str(len(target.units)) + "; target_sum_rank - " +
                                          str(target_sum_rank))

                                    rank_ratio = int(own_army_sum_rank / target_sum_rank * 100)
                                    random_risk_level = random.randint(0, 40)
                                    # Standard border is 120
                                    print("rank_ratio - " + str(rank_ratio) + "; random_risk_level - " +
                                          str(random_risk_level) + "; result - " + str(120 - random_risk_level))
                                    if rank_ratio >= 120 - random_risk_level:
                                        print("Ready to attack neutral army")
                                        distance = math.sqrt(
                                            ((army.posxy[0] - game_obj.game_map[TileNum].posxy[0]) ** 2) + (
                                                    (army.posxy[1] - game_obj.game_map[TileNum].posxy[1]) ** 2))
                                        distance = math.floor(distance * 100) / 100
                                        tile_list.append(["Enemy army", list(game_obj.game_map[TileNum].posxy),
                                                          distance])
                                    break

                                elif target.owner in at_war_list:
                                    # Targeting armies from realms who are at war with this realm
                                    target_sum_rank = 0
                                    for unit in target.units:
                                        target_sum_rank += unit.rank
                                    print("len(target.units) - " + str(len(target.units)) + "; target_sum_rank - " +
                                          str(target_sum_rank))

                                    rank_ratio = int(own_army_sum_rank / target_sum_rank * 100)
                                    random_risk_level = random.randint(0, 40)
                                    # Standard border is 120
                                    power_border = 120
                                    # But for human player factions increase to 145, since humans are better at battling
                                    for realm in game_obj.game_powers:
                                        if realm.name == target.owner:
                                            if not realm.AI_player:
                                                power_border = 145
                                            break
                                    print("rank_ratio - " + str(rank_ratio) + "; random_risk_level - " +
                                          str(random_risk_level) + "; result - " +
                                          str(power_border - random_risk_level))
                                    if rank_ratio >= power_border - random_risk_level:
                                        print("Ready to attack " + str(target.owner) + " army")
                                        distance = math.sqrt(
                                            ((army.posxy[0] - game_obj.game_map[TileNum].posxy[0]) ** 2) + (
                                                    (army.posxy[1] - game_obj.game_map[TileNum].posxy[1]) ** 2))
                                        distance = math.floor(distance * 100) / 100
                                        tile_list.append(["Enemy army", list(game_obj.game_map[TileNum].posxy),
                                                          distance])
                                    break

    # print("len(tile_list) : " + str(len(tile_list)))
    # print("tile_list: " + str(tile_list))
    tile_list = sorted(tile_list, key=lambda x: x[2])
    print("sorted tile_list: " + str(tile_list))
    nowhere_to_go = False

    if tile_list:
        destination_list = []
        limit = 10
        num_limit = len(tile_list)
        num = 0
        calculate = True
        while calculate:
            route = algo_astar.astar(army.army_id, army.posxy, tile_list[num][1], "Empty", friendly_cities,
                                     hostile_cities, realm.known_map)
            # if tile_list[num][0] == "Und":
            #     print("Und " + str(tile_list[num][1]) + " - " + str(route))
            # if len(route) > 0:
            if route is not None:
                limit -= 1
                destination_list.append([list(tile_list[num][1]), len(route), str(tile_list[num][0])])

            if limit == 0:
                calculate = False

            num += 1
            if num == num_limit:
                calculate = False

        if destination_list:
            destination_list = sorted(destination_list, key=lambda x: x[1])
            role.army_role = "Adventure"
            game_pathfinding.search_army_movement("AI",
                                                  int(army.army_id),
                                                  str(realm.name),
                                                  destination_list[0][0])
            army.action = "Ready to move"
            print("Destination - " + str(destination_list[0][0]) + " " + destination_list[0][2] + " len(army.route) - "
                  + str(len(army.route)))

        else:
            nowhere_to_go = True

    else:
        nowhere_to_go = True

    if nowhere_to_go:
        if role.army_role == "Adventure":
            role.army_role = "Nothing to do"
            # role.status = "Finished"
            print("Nowhere to go on adventure, army.role set to 'Nothing to do'")


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

        if role.army_role in ["Adventure"] and role.status != "Finished":
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
                        print("settlement.military_occupation is None")
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


exploration_objects_group_1 = ["Mythic monolith",
                               "Stone circle",
                               "Scholar's tower",
                               "Stone well"]

exploration_objects_group_2 = ["Burial mound",
                               "Angler's cabin"]
