## Among Myth and Wonder
## explore_neutral_lands

import math

from Resources import game_stats
from Resources import game_obj
from Resources import common_selects
from Resources import algo_astar
from Resources import algo_square_range
from Resources import game_pathfinding

from Strategy_AI import AI_exploration_cond

from Strategy_AI.Logic_Solutions import power_ranking


def solution(realm, role, friendly_cities, hostile_cities, at_war_list):
    print("")
    print("explore_neutral_lands")
    rank_sum = 0
    army = common_selects.select_army_by_id(role.army_id)

    for unit in army.units:
        rank_sum += unit.rank

    if realm.AI_cogs.exploration_targets:  # Non-empty list of exploration targets
        if rank_sum >= army_rank_dic[role.army_size] / 3:
            print("Army " + str(army.army_id) + " size - " + str(rank_sum) + ", big enough to be sent into exploration")
            print(realm.name + " exploration targets: " + str(realm.AI_cogs.exploration_targets))
            assemble_exploration_destinations(realm, role, army, realm.AI_cogs.exploration_targets, rank_sum,
                                              friendly_cities, hostile_cities, at_war_list)


def assemble_exploration_destinations(realm, role, army, targets, rank_sum, friendly_cities, hostile_cities,
                                      at_war_list):
    print("")
    tile_list = []

    for target in targets:
        distance = math.sqrt(((army.posxy[0] - target[0]) ** 2) +
                             ((army.posxy[1] - target[1]) ** 2))
        distance = math.floor(distance * 100) / 100
        tile_list.append(["Undiscovered", list(target), distance])

    tile_list = sorted(tile_list, key=lambda x: x[2])

    if tile_list:
        destination_list = []
        limit = 10
        num_limit = len(tile_list)
        num = 0
        calculate = True

        # Next step is to find undiscovered tile from exploration targets list with minimal route
        # from a list of 10 targets with closest distance
        while calculate:
            route = algo_astar.astar(army.army_id, army.posxy, tile_list[num][1], "Empty", friendly_cities,
                                     hostile_cities, realm.known_map)

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
            print("1) Destination - " + str(destination_list[0][0]) + " " + destination_list[0][2]
                  + " len(army.route) - " + str(destination_list[0][1]))

            tile_list = [["Undiscovered", list(destination_list[0][0]), destination_list[0][1]]]
            # Next step to collect tiles around already selected target and select tiles
            # that are either also undiscovered or contain places of interest

            square = algo_square_range.within_square_range(destination_list[0][0], 4)
            square.remove(destination_list[0][0])
            comparative_distance = math.sqrt(((army.posxy[0] - destination_list[0][0][0]) ** 2) +
                                             ((army.posxy[1] - destination_list[0][0][1]) ** 2))
            comparative_distance = math.floor(comparative_distance * 100) / 100
            for tile in square:
                distance = math.sqrt(((army.posxy[0] - tile[0]) ** 2) +
                                     ((army.posxy[1] - tile[1]) ** 2))
                distance = math.floor(distance * 100) / 100

                if distance <= comparative_distance:
                    # Filter out tiles that are further away
                    if tile not in realm.known_map:
                        tile_list.append(["Undiscovered", list(tile), distance])

                    else:
                        TileNum = (tile[1] - 1) * game_stats.cur_level_width + tile[0] - 1
                        if game_obj.game_map[TileNum].lot is not None:
                            if game_obj.game_map[TileNum].lot != "City":
                                map_obj = game_obj.game_map[TileNum].lot
                                if map_obj.obj_typ == "Bonus":
                                    check_bonus_object(map_obj, army, tile, tile_list)

                                elif map_obj.obj_typ == "Lair":
                                    check_lair_object(map_obj, army, tile, tile_list, rank_sum)

                        else:
                            # Tile without a lot
                            check_hostile_armies(army, tile, tile_list, rank_sum, TileNum, at_war_list)

            print("2) len(tile_list) - " + str(len(tile_list)))

    if tile_list:
        destination_list = []
        limit = 10
        num_limit = len(tile_list)
        num = 0
        calculate = True

        # Final step to choose a tile with shortest route
        while calculate:
            route = algo_astar.astar(army.army_id, army.posxy, tile_list[num][1], "Empty", friendly_cities,
                                     hostile_cities, realm.known_map)

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
            role.army_role = "Exploration"
            game_pathfinding.search_army_movement("AI",
                                                  int(army.army_id),
                                                  str(realm.name),
                                                  destination_list[0][0])
            army.action = "Ready to move"
            print("3) Destination - " + str(destination_list[0][0]) + " " + destination_list[0][2]
                  + " len(army.route) - " + str(len(army.route)))


def check_bonus_object(map_obj, army, tile, tile_list):
    # Exploration objects
    if map_obj.obj_name in exploration_objects_group_1:
        if army.hero.hero_id not in map_obj.properties.hero_list \
                and not map_obj.properties.need_replenishment:
            passed_verification = True
            if map_obj.obj_name in AI_exploration_cond.event_conditions:
                passed_verification = AI_exploration_cond.event_conditions[
                    map_obj.obj_name](army)
            if passed_verification:
                distance = math.sqrt(((army.posxy[0] - tile[0]) ** 2) + ((army.posxy[1] - tile[1]) ** 2))
                distance = math.floor(distance * 100) / 100
                tile_list.append(["Bonus", list(tile), distance])
    elif map_obj.obj_name in exploration_objects_group_2:
        if not map_obj.properties.need_replenishment:
            distance = math.sqrt(((army.posxy[0] - tile[0]) ** 2) + ((army.posxy[1] - tile[1]) ** 2))
            distance = math.floor(distance * 100) / 100
            tile_list.append(["Bonus", list(tile), distance])


def check_lair_object(map_obj, army, tile, tile_list, own_army_sum_rank):
    # Lair objects with opportunity to fight for a prize
    if map_obj.properties.army_id is not None:
        print("obj.properties.army_id - " + str(map_obj.properties.army_id))
        for target in game_obj.game_armies:
            if target.army_id == map_obj.properties.army_id:
                if power_ranking.rank_ratio_calculation(own_army_sum_rank, target, 120):
                    print("Ready to attack lair")
                    distance = math.sqrt(((army.posxy[0] - tile[0]) ** 2) + ((army.posxy[1] - tile[1]) ** 2))
                    distance = math.floor(distance * 100) / 100
                    tile_list.append(["Lair", list(tile), distance])
                break


def check_hostile_armies(army, tile, tile_list, rank_sum, TileNum, at_war_list):
    if game_obj.game_map[TileNum].army_id is not None:
        # There is an army
        print("Tile.army_id - " + str(game_obj.game_map[TileNum].army_id))
        for target in game_obj.game_armies:
            if target.army_id == game_obj.game_map[TileNum].army_id:
                if target.action == "Stand":
                    # Targeting standing armies
                    if target.owner == "Neutral":
                        # Targeting neutral armies
                        if power_ranking.rank_ratio_calculation(rank_sum, target, 120):
                            print("Ready to attack neutral army")
                            distance = math.sqrt(((army.posxy[0] - tile[0]) ** 2) + ((army.posxy[1] - tile[1]) ** 2))
                            distance = math.floor(distance * 100) / 100
                            tile_list.append(["Enemy army", list(tile), distance])

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
                        if power_ranking.rank_ratio_calculation(rank_sum, target, power_border):
                            print("Ready to attack " + str(target.owner) + " army")
                            distance = math.sqrt(((army.posxy[0] - tile[0]) ** 2) + ((army.posxy[1] - tile[1]) ** 2))
                            distance = math.floor(distance * 100) / 100
                            tile_list.append(["Enemy army", list(tile), distance])
                break


army_rank_dic = {1 : 35,
                 2 : 90,
                 3 : 144}

exploration_objects_group_1 = ["Mythic monolith",
                               "Stone circle",
                               "Scholar's tower",
                               "Stone well"]

exploration_objects_group_2 = ["Burial mound",
                               "Angler's cabin"]
