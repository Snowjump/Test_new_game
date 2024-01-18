## Among Myth and Wonder
## military_expedition

import math

from Resources import game_stats
from Resources import game_obj
from Resources import game_pathfinding
from Resources import algo_astar


def solution(realm, role, army, friendly_cities, hostile_cities, military_targets):
    print("")
    print("military_expedition")
    rank_sum = 0

    for unit in army.units:
        rank_sum += unit.rank

    if rank_sum >= army_rank_dic[role.army_size] / 2:
        print(realm.name + " army " + str(army.army_id) + " size - " + str(rank_sum)
              + ", big enough to be sent into military expedition")
        print(realm.name + " military targets: " + str(military_targets))

        if military_targets:
            give_next_order = assemble_expedition_destinations(realm, role, army, military_targets, friendly_cities,
                                                               hostile_cities)
            if give_next_order:
                return True
            else:
                return False
        else:
            return True

    else:
        return True


def assemble_expedition_destinations(realm, role, army, military_targets, friendly_cities, hostile_cities):
    tile_list = []

    for target in military_targets:
        target_position = target[1]
        distance = math.sqrt(((army.posxy[0] - target_position[0]) ** 2) +
                             ((army.posxy[1] - target_position[1]) ** 2))
        distance = math.floor(distance * 100) / 100
        tile_list.append([list(target_position), distance])

    tile_list = sorted(tile_list, key=lambda x: x[1])

    destination_list = []
    limit = 10
    num_limit = len(tile_list)
    num = 0
    calculate = True

    while calculate:
        print("num - " + str(num) + "; tile_list[num][1] - " + str(tile_list[num][0]))
        route = algo_astar.astar(army.army_id, army.posxy, tile_list[num][0], "Empty", friendly_cities,
                                 hostile_cities, realm.known_map)

        if route is not None:
            limit -= 1
            destination_list.append([list(tile_list[num][0]), len(route)])

        if limit == 0:
            calculate = False

        num += 1
        if num == num_limit:
            calculate = False

    if destination_list:
        destination_list = sorted(destination_list, key=lambda x: x[1])
        destination = destination_list[0]
        print("Destination - " + str(destination[0])
              + " len(army.route) - " + str(destination[1]))

        TileNum = (destination[0][1] - 1) * game_stats.cur_level_width + destination[0][0] - 1
        TileObj = game_obj.game_map[TileNum]
        if TileObj.city_id in friendly_cities:
            role.army_role = "Advance - liberate settlement"
        else:
            role.army_role = "Advance - enemy settlement"
        game_pathfinding.search_army_movement("AI",
                                              int(army.army_id),
                                              str(realm.name),
                                              destination[0])
        army.action = "Ready to move"
        return False
    else:
        return True


army_rank_dic = {1: 35,
                 2: 90,
                 3: 144}
