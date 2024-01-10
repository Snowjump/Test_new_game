## Among Myth and Wonder
## territory_targets

import math

from Resources import game_stats
from Resources import game_obj
from Resources import common_selects
from Resources import game_pathfinding

from Strategy_AI.Logic_Solutions import power_ranking


def solution(realm, role, army, friendly_cities, hostile_cities, at_war_list):
    print("")
    print("territory_targets")
    # Search for targets that situated in same province as this army
    own_army_sum_rank = 0
    closest_tile = None
    shortest_distance = 0.0
    settlement_id = game_obj.game_map[army.location].city_id
    better_retreat = False

    if settlement_id and at_war_list:
        settlement = common_selects.select_settlement_by_id(settlement_id)

        for tile_number in settlement.control_zone:
            tile = game_obj.game_map[tile_number]
            distance = math.sqrt(((tile.posxy[0] - army.posxy[0]) ** 2) + ((tile.posxy[1] - army.posxy[1]) ** 2))
            add_tile = False
            if tile.army_id and tile.army_id != army.army_id:
                selected_army = common_selects.select_army_by_id(tile.army_id)
                if selected_army.owner in at_war_list and selected_army.owner != "Neutral":
                    if not own_army_sum_rank:
                        for unit in army.units:
                            own_army_sum_rank += unit.rank
                        print("territory_targets(): Own army: len(army.units) - " + str(len(army.units))
                              + "; own_army_sum_rank - " + str(own_army_sum_rank))

                    # Standard border is 120
                    power_border = 120
                    # But for human player factions increase to 145, since humans are better at battling
                    selected_realm = common_selects.select_realm_by_name(selected_army.owner)
                    if not selected_realm.AI_player:
                        power_border = 135

                    if power_ranking.rank_ratio_calculation(own_army_sum_rank, selected_army, power_border):
                        add_tile = True
                        print("Add army - " + str(selected_army.army_id) + " from " + str(selected_army.owner))
                    else:
                        better_retreat = True

            elif tile.lot is not None:
                if tile.lot == "City":
                    if settlement.owner in at_war_list and not settlement.military_occupation:
                        # Enemy unoccupied settlement is detected
                        add_tile = True
                        print("Add enemy settlement - " + str(settlement.name) + "; distance - " + str(distance))
                    elif settlement.owner == army.owner and settlement.military_occupation:
                        # Own occupied settlement is detected
                        add_tile = True
                        print("Add occupied settlement - " + str(settlement.name) + "; distance - " + str(distance))

            if add_tile:
                if closest_tile is None:
                    closest_tile = list(tile.posxy)
                    shortest_distance = float(distance)

                elif distance < shortest_distance:
                    closest_tile = list(tile.posxy)
                    shortest_distance = float(distance)

    if better_retreat:
        # Dangerous enemy found in this province
        # AI army suggested to retreat to settlement if possible
        settlement = common_selects.select_settlement_by_id(settlement_id)
        tile = game_obj.game_map[settlement.location]
        if tile.army_id:
            if tile.army_id == army.army_id:
                # This army already stationed inside garrison
                # It won't do anything until the next turn and will stand put
                role.army_role = "Nothing to do"
                role.status = "Finished"
                return False
        else:
            # There is a vacant settlement without a garrison
            closest_tile = list(tile.posxy)

    if closest_tile:
        TileNum = (closest_tile[1] - 1) * game_stats.cur_level_width + closest_tile[0] - 1
        TileObj = game_obj.game_map[TileNum]
        if TileObj.army_id is not None:
            role.army_role = "Advance - enemy army"
            role.target_army_id = int(TileObj.army_id)
        elif TileObj.lot is not None:
            if TileObj.lot == "City":
                settlement = common_selects.select_settlement_by_id(TileObj.city_id)
                role.target_city_id = int(TileObj.city_id)

                if settlement.owner in at_war_list and not settlement.military_occupation:
                    # Target is enemy unoccupied settlement
                    role.army_role = "Advance - enemy settlement"
                elif settlement.owner == army.owner and settlement.military_occupation:
                    # Target is own occupied settlement
                    role.army_role = "Advance - liberate settlement"

        game_pathfinding.search_army_movement("AI",
                                              int(army.army_id),
                                              str(realm.name),
                                              closest_tile)
        army.action = "Ready to move"
        print("Destination - " + str(closest_tile) + " len(army.route) - " + str(len(army.route)))
        return False
    else:
        return True
