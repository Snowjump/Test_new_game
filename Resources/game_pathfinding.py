## Among Myth and Wonder
## game_pathfinding

import math

from Resources import game_stats
from Resources import game_obj
from Resources import algo_astar
from Resources import algo_path_arrows
from Resources import game_classes
from Resources import game_basic

from Content import exploration_catalog


def search_army_movement(actor, selected_army, army_owner, tile_position):
    start = []
    friendly_cities, hostile_cities, at_war_list = find_friendly_cities(army_owner)
    for army in game_obj.game_armies:
        if army.army_id == selected_army:
            start = army.posxy
            break

    the_realm = None
    for realm in game_obj.game_powers:
        if realm.name == army_owner:
            the_realm = realm
            break

    # for TileObj in game_obj.game_map:
    #     x = TileObj.posxy[0]
    #     y = TileObj.posxy[1]
    #     x -= int(game_stats.pov_pos[0])
    #     y -= int(game_stats.pov_pos[1])
    #
    #     if 0 < x <= 27 and 0 < y <= math.ceil(game_stats.game_window_height):
    #         if [x, y] == tile_position:
    TileNum = (tile_position[1] - 1) * game_stats.cur_level_width + tile_position[0] - 1
    TileObj = game_obj.game_map[TileNum]

    route = []

    if tile_position in the_realm.known_map:
        if TileObj.lot is not None:
            if TileObj.lot == "City":
                settlement = None
                for city in game_obj.game_cities:
                    if city.city_id == TileObj.city_id:
                        settlement = city
                        break

                if settlement.owner == army_owner:
                    print("Moving to settlement - " + str(TileObj.city_id))
                    route = algo_astar.astar(selected_army, start, tile_position, "Settlement", friendly_cities,
                                             hostile_cities, the_realm.known_map)

                elif settlement.owner == "Neutral":
                    print("Moving to neutral settlement - " + str(TileObj.city_id))
                    route = algo_astar.astar(selected_army, start, tile_position, "Settlement", friendly_cities,
                                             hostile_cities, the_realm.known_map)

                elif settlement.city_id in hostile_cities:
                    print("Moving to enemy settlement - " + str(TileObj.city_id))
                    route = algo_astar.astar(selected_army, start, tile_position, "Settlement", friendly_cities,
                                             hostile_cities, the_realm.known_map)

            elif TileObj.lot.obj_typ == "Obstacle":
                if TileObj.travel:
                    print("Moving to cross-country")
                    route = algo_astar.astar(selected_army, start, tile_position, "Empty", friendly_cities,
                                             hostile_cities, the_realm.known_map)

                else:
                    print("Location is blocked")

            elif TileObj.lot.obj_typ == "Facility":
                print("Moving to " + str(TileObj.lot.obj_name))
                route = algo_astar.astar(selected_army, start, tile_position, "Facility", friendly_cities,
                                         hostile_cities, the_realm.known_map)

            elif TileObj.lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                print("Moving to " + str(TileObj.lot.obj_name))
                route = algo_astar.astar(selected_army, start, tile_position, str(TileObj.lot.obj_name),
                                         friendly_cities, hostile_cities, the_realm.known_map)

        elif TileObj.army_id is not None:
            if TileObj.army_id == selected_army:
                print("You clicked on the same spot that army is located")

            else:
                for army in game_obj.game_armies:
                    if army.army_id == TileObj.army_id:
                        if army.owner == army_owner:
                            print("Moving toward your other army")
                            route = algo_astar.astar(selected_army, start, tile_position, "Own army", friendly_cities,
                                                     hostile_cities, the_realm.known_map)

                        elif army.owner == "Neutral":
                            print("Moving toward neutral army")
                            route = algo_astar.astar(selected_army, start, tile_position, "Neutral army",
                                                     friendly_cities, hostile_cities, the_realm.known_map)

                        elif army.owner in at_war_list:
                            print("Moving toward enemy army")
                            route = algo_astar.astar(selected_army, start, tile_position, "Enemy army", friendly_cities,
                                                     hostile_cities, the_realm.known_map)

        else:
            print("Moving to empty location")
            # print("start - " + str(start))
            # print("game_stats.cur_level_width - " + str(game_stats.cur_level_width))
            # print("game_stats.cur_level_height - " + str(game_stats.cur_level_height))
            route = algo_astar.astar(selected_army, start, tile_position, "Empty", friendly_cities, hostile_cities,
                                     the_realm.known_map)

    else:
        print("Moving to undiscovered location")
        route = algo_astar.astar(selected_army, start, tile_position, "Empty", friendly_cities, hostile_cities,
                                 the_realm.known_map)

    if route is None:
        pass
    else:
        if len(route) > 0:
            # Record arrows for movement
            algo_path_arrows.construct_path(selected_army, route)

            del route[0]  # Remove starting point where army is standing
            # print("Route is " + str(route))

        for army in game_obj.game_armies:
            if army.army_id == selected_army:
                army.route = route
                break
    # break


class found_path():

    def __init__(self, position=None, personal_id=None, path=None, distance=None):
        self.position = position
        self.personal_id = personal_id
        self.path = path
        self.distance = distance

    def __eq__(self, other):
        return self.distance == other.distance


def find_friendly_cities(player):
    list_of_friendly_city_id = []
    list_of_hostile_city_id = []
    at_war_list = []

    for realm in game_obj.game_powers:
        if realm.name == player:
            for enemy in realm.relations.at_war:
                at_war_list.append(enemy[2])
            # print("realm.relations.at_war:")
            break

    for settlement in game_obj.game_cities:
        if settlement.owner == player:
            list_of_friendly_city_id.append(settlement.city_id)
        elif settlement.owner == "Neutral":
            list_of_hostile_city_id.append(settlement.city_id)
        elif settlement.owner in at_war_list:
            list_of_hostile_city_id.append(settlement.city_id)

    # print("list_of_hostile_city_id: " + str(list_of_hostile_city_id))

    return list_of_friendly_city_id, list_of_hostile_city_id, at_war_list
