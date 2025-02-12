## Among Myth and Wonder
## adventure_role_AI

import math

from Resources import game_stats
from Resources import game_obj
from Resources import game_basic
from Resources import common_selects
from Resources import game_pathfinding
from Resources import algo_astar

from Strategy_AI import AI_exploration_cond

from Strategy_AI.Logic_Solutions import power_ranking


def solution(realm, role, friendly_cities, hostile_cities, at_war_list, army):
    print("")
    print("adventure_role_AI.solution()")

    city_id_in_location = game_obj.game_map[army.location].city_id
    go_to_adventure = False
    if army.shattered == "Shattered":
        # Shouldn't go to adventure
        print("Army is shattered")
        pass
    # elif army.action in ["Fighting", "Besieged", "Besieging"]:
    #     # Shouldn't go to adventure due to fighting
    #     print("Army " + str(army.army_id) + " is busy " + army.action.lower())
    #     pass
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
        print("city_id_in_location - " + str(city_id_in_location))
        settlement = common_selects.select_settlement_by_id(city_id_in_location)
        if settlement.owner == realm.name:
            # role.army_role = "Adventure"
            print("city_id_in_location - " + str(city_id_in_location) +
                  "; settlement.name - " + str(settlement.name))
            assemble_adventure_destinations(realm, role, army, settlement,
                                            friendly_cities, hostile_cities, at_war_list)
            issued_order = True

        if not issued_order:
            # It could happened if the army during adventuring stepped into foreign territory
            for settlement in game_obj.game_cities:
                if settlement.city_id == role.base_of_operation:
                    print(settlement.name + "; city_id - " + str(settlement.city_id))
                    print("base_of_operation - " + str(role.base_of_operation))
                    assemble_adventure_destinations(realm, role, army, settlement,
                                                    friendly_cities, hostile_cities, at_war_list)
                    break


def assemble_adventure_destinations(realm, role, army, settlement, friendly_cities, hostile_cities, at_war_list):
    tile_list = []
    print("")
    # print("len(settlement.control_zone) : " + str(len(settlement.control_zone)))
    # print(realm.name + " - len(realm.known_map) : " + str(len(realm.known_map)))
    # print("realm.known_map : " + str(realm.known_map))
    own_army_sum_rank = 0
    for unit in army.units:
        own_army_sum_rank += unit.rank
    print("assemble_adventure_destinations(): Own army: len(army.units) - " + str(len(army.units))
          + "; own_army_sum_rank - " + str(own_army_sum_rank))
    for TileNum in settlement.control_zone:
        # Adventuring on your own territory

        # print(str(tile))
        # print(str(realm.known_map))
        # print(str(game_obj.game_map[TileNum].posxy))
        if list(game_obj.game_map[TileNum].posxy) not in realm.known_map:
            # print("Undiscovered tile - " + str(list(game_obj.game_map[TileNum].posxy)))
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
                                    if power_ranking.rank_ratio_calculation(own_army_sum_rank, target, 120):
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
                                    if power_ranking.rank_ratio_calculation(own_army_sum_rank, target, 120):
                                        print("Ready to attack neutral army")
                                        distance = math.sqrt(
                                            ((army.posxy[0] - game_obj.game_map[TileNum].posxy[0]) ** 2) + (
                                                    (army.posxy[1] - game_obj.game_map[TileNum].posxy[1]) ** 2))
                                        distance = math.floor(distance * 100) / 100
                                        tile_list.append(["Enemy army", list(game_obj.game_map[TileNum].posxy),
                                                          distance])

                                elif target.owner in at_war_list:
                                    # Targeting armies from realms who are at war with this realm
                                    # Standard border is 120
                                    power_border = 120
                                    # But for human player factions increase to 145, since humans are better at battling
                                    for power in game_obj.game_powers:
                                        if power.name == target.owner:
                                            if not power.AI_player:
                                                power_border = 145
                                            break
                                    if power_ranking.rank_ratio_calculation(own_army_sum_rank, target, power_border):
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


exploration_objects_group_1 = ["Mythic monolith",
                               "Stone circle",
                               "Scholar's tower",
                               "Stone well",
                               "Champion's tent",
                               "Leshy's hut"]

exploration_objects_group_2 = ["Burial mound",
                               "Angler's cabin"]
