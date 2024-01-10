## Among Myth and Wonder
## immediate_targets

import math

from Resources import game_obj
from Resources import game_stats
from Resources import algo_movement_range
from Resources import algo_path_arrows
from Resources import common_selects

from Strategy_AI.Logic_Solutions import power_ranking


def solution(realm, role, army, friendly_cities, hostile_cities, at_war_list):
    # Search for targets that could be reached in one turn of moving over strategy map
    own_army_sum_rank = 0
    army_MP = 0  # Movement points
    for unit in army.units:
        if not army_MP:
            army_MP = float(unit.movement_points)
        elif army_MP > unit.movement_points:
            army_MP = float(unit.movement_points)

    # print(str(realm.name) + "'s known map: " + str(realm.known_map))
    path, grid = algo_movement_range.range_astar(army, army.posxy, army_MP, friendly_cities,
                                                 hostile_cities, realm.known_map, False, at_war_list)

    closest_tile = None
    shortest_distance = 0.0
    for tile in grid:
        if tile in realm.known_map:
            distance = math.sqrt(((tile[0] - army.posxy[0]) ** 2) + ((tile[1] - army.posxy[1]) ** 2))
            # print("tile - " + str(tile) + "; distance - " + str(distance))
            TileNum = (tile[1] - 1) * game_stats.cur_level_width + tile[0] - 1
            TileObj = game_obj.game_map[TileNum]
            add_tile = False
            if TileObj.army_id is not None:
                for target in game_obj.game_armies:
                    if target.army_id == TileObj.army_id:
                        if target.owner in at_war_list and target.owner != "Neutral":
                            if not own_army_sum_rank:
                                for unit in army.units:
                                    own_army_sum_rank += unit.rank
                                print("immediate_targets(): Own army: len(army.units) - " + str(len(army.units))
                                      + "; own_army_sum_rank - " + str(own_army_sum_rank))

                            # Standard border is 120
                            power_border = 120
                            # But for human player factions increase to 145, since humans are better at battling
                            selected_realm = common_selects.select_realm_by_name(target.owner)
                            if not selected_realm.AI_player:
                                power_border = 135

                            if power_ranking.rank_ratio_calculation(own_army_sum_rank, target, power_border):
                                add_tile = True
                                print("Add army - " + str(target.army_id) + "; distance - " + str(distance))
                        break

            elif TileObj.lot is not None:
                if TileObj.lot == "City":
                    for settlement in game_obj.game_cities:
                        if settlement.city_id == TileObj.city_id:
                            if settlement.owner in at_war_list and not settlement.military_occupation:
                                # Enemy unoccupied settlement is detected
                                add_tile = True
                                print("Add enemy settlement - " + str(settlement.name) + "; distance - "
                                      + str(distance))
                            elif settlement.owner == army.owner and settlement.military_occupation:
                                # Own occupied settlement is detected
                                add_tile = True
                                print("Add occupied settlement - " + str(settlement.name) + "; distance - "
                                      + str(distance))

                            break

            if add_tile:
                if closest_tile is None:
                    closest_tile = list(tile)
                    shortest_distance = float(distance)

                elif distance < shortest_distance:
                    closest_tile = list(tile)
                    shortest_distance = float(distance)

    print("Military target search: closest_tile - " + str(closest_tile) + "; shortest_distance - " +
          str(shortest_distance))

    if closest_tile:
        for node in path:
            if node.position == closest_tile:
                # print("node.position - " + str(node.position) + " and closest_tile - " + str(closest_tile))
                pathway = []
                current = node
                while current is not None:
                    pathway.append(current.position)
                    current = current.parent

                # print("Final unreversed path is " + str(pathway))
                army.route = list(pathway[::-1])
                algo_path_arrows.construct_path(army.army_id, army.route)
                army.route = army.route[1:]

                # print("Final reversed path is " + str(army.route))
                # print("Arrows path is " + str(army.path_arrows))
                army.action = "Ready to move"

                TileNum = (node.position[1] - 1) * game_stats.cur_level_width + node.position[0] - 1
                TileObj = game_obj.game_map[TileNum]
                if TileObj.army_id is not None:
                    role.army_role = "Advance - enemy army"
                    role.target_army_id = int(TileObj.army_id)
                elif TileObj.lot is not None:
                    if TileObj.lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.city_id == TileObj.city_id:
                                role.target_city_id = int(TileObj.city_id)
                                if settlement.owner in at_war_list and not settlement.military_occupation:
                                    # Target is enemy unoccupied settlement
                                    role.army_role = "Advance - enemy settlement"
                                elif settlement.owner == army.owner and settlement.military_occupation:
                                    # Target is own occupied settlement
                                    role.army_role = "Advance - liberate settlement"

                                break

        return False
    else:
        return True
