## Miracle battles

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


# def search_tunel_mining(tile_xy, fac_name, given_task_id):
#     check = False
#     for fac in game_obj.game_factions:
#         if fac.name == fac_name:
#             if len(fac.population) > 0:
#                 check = True
#     ##    print("Check status is " + str(check))
#     if check:  # Search for nearby tiles, from where characters can dig mines
#         adj_tiles = []
#         for adj_tile in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
#             approved = True
#             if tile_xy[0] + adj_tile[0] > game_stats.cur_level_width:
#                 approved = False
#             if tile_xy[0] + adj_tile[0] < 1:
#                 approved = False
#             if tile_xy[1] + adj_tile[1] > game_stats.cur_level_height:
#                 approved = False
#             if tile_xy[1] + adj_tile[1] < 1:
#                 approved = False
#             if [tile_xy[0] + adj_tile[0], tile_xy[1] + adj_tile[1]] not in game_stats.known_map:
#                 approved = False
#
#             x_pos = tile_xy[0] + adj_tile[0]
#             y_pos = tile_xy[1] + adj_tile[1]
#             TileNum = (y_pos - 1) * game_stats.cur_level_width + x_pos
#
#             if game_obj.game_map[TileNum - 1].matter == "Monolith":
#                 approved = False
#             if game_obj.game_map[TileNum - 1].tunnels == False:
#                 approved = False
#
#             if approved:
#                 adj_tiles.append([tile_xy[0] + adj_tile[0], tile_xy[1] + adj_tile[1]])
#         if len(adj_tiles) > 0:
#             print("Nearby tiles: " + str(adj_tiles))
#             candidates = []
#             for fac in game_obj.game_factions:
#                 if fac.name == fac_name:
#                     for pop in fac.population:
#
#                         if pop.occupation == "not occupied":
#
#                             if pop.location % game_stats.cur_level_width == 0:
#                                 x = game_stats.cur_level_width
#                             else:
#                                 x = pop.location % game_stats.cur_level_width
#                             y = math.ceil(pop.location / game_stats.cur_level_width)
#                             print("Character's location " + str([x, y]) + " with ID " + str(pop.personal_id))
#                             candidates.append([[x, y], pop.personal_id])
#             print("Candidates for work: " + str(candidates))
#             list_routes = []
#             if len(candidates) > 0:
#                 for adj_tile in adj_tiles:
#                     for candidate in candidates:
#                         print("Path for " + str(candidate) + " moving to " + str(adj_tile))
#                         route = algo_astar.astar(candidate[0], adj_tile)
#                         if len(route) > 0:
#                             new_route = found_path(candidate[0], candidate[1], route, len(route))
#                             list_routes.append(new_route)
#                             print("Success " + str(len(route)))
#
#             # Get the optimal character and route
#             current_route = None
#             current_index = None
#             if len(list_routes) > 0:
#                 current_route = list_routes[0]
#                 current_index = 0
#                 for index, item in enumerate(list_routes):
#                     if item.distance < current_route.distance:
#                         current_route = item
#                         current_index = index
#                 print("Distance of current route - " + str(current_route.distance) + " Char ID - " + str(
#                     current_route.personal_id))
#
#                 # Updating task list with performer ID
#                 for task in game_obj.task_list:
#                     if task.task_id == given_task_id:
#                         print("Task ID is " + str(task.task_id))
#                         task.performer = current_route.personal_id
#
#                 # Assigning new mining task to unoccupied character
#                 for fac in game_obj.game_factions:
#                     if fac.name == fac_name:
#                         for pop in fac.population:
#                             if pop.personal_id == current_route.personal_id:
#                                 new_task = game_classes.work_task("Commuting", current_route.path, tile_xy,
#                                                                   "Tunel mining", given_task_id)
#                                 pop.goal = new_task
#                                 pop.occupation = "commuting"


# def search_cave_mining(tile_xy, fac_name, given_task_id):
#     check = False
#     for fac in game_obj.game_factions:
#         if fac.name == fac_name:
#             if len(fac.population) > 0:
#                 check = True
#     if check:  # Search for nearby tiles, from where characters can dig mines
#
#         x_pos = tile_xy[0]
#         y_pos = tile_xy[1]
#         TileNum = (y_pos - 1) * game_stats.cur_level_width + x_pos
#
#         candidates = []
#         for fac in game_obj.game_factions:
#             if fac.name == fac_name:
#                 for pop in fac.population:
#                     if pop.occupation == "not occupied":
#
#                         if pop.location % game_stats.cur_level_width == 0:
#                             x = game_stats.cur_level_width
#                         else:
#                             x = pop.location % game_stats.cur_level_width
#                         y = math.ceil(pop.location / game_stats.cur_level_width)
#                         print("Character's location " + str([x, y]) + " with ID " + str(pop.personal_id))
#                         candidates.append([[x, y], pop.personal_id])
#         print("Candidates for work: " + str(candidates))
#         list_routes = []
#         if len(candidates) > 0:
#             for candidate in candidates:
#                 print("Path for " + str(candidate) + " moving to " + str(tile_xy))
#                 route = algo_astar.astar(candidate[0], tile_xy)
#                 if len(route) > 0:
#                     new_route = found_path(candidate[0], candidate[1], route, len(route))
#                     list_routes.append(new_route)
#                     print("Success " + str(len(route)))
#
#         # Get the optimal character and route
#         current_route = None
#         current_index = None
#         if len(list_routes) > 0:
#             current_route = list_routes[0]
#             current_index = 0
#             for index, item in enumerate(list_routes):
#                 if item.distance < current_route.distance:
#                     current_route = item
#                     current_index = index
#             print("Distance of current route - " + str(current_route.distance) + " Char ID - " + str(
#                 current_route.personal_id))
#
#             # Updating task list with performer ID
#             for task in game_obj.task_list:
#                 if task.task_id == given_task_id:
#                     print("Task ID is " + str(task.task_id))
#                     task.performer = current_route.personal_id
#
#             # Assigning new mining task to unoccupied character
#             for fac in game_obj.game_factions:
#                 if fac.name == fac_name:
#                     for pop in fac.population:
#                         if pop.personal_id == current_route.personal_id:
#                             new_task = game_classes.work_task("Commuting", current_route.path, tile_xy, "Cave mining",
#                                                               given_task_id)
#                             pop.goal = new_task
#                             pop.occupation = "commuting"


# def search_mashroom_cutting(tile_xy, fac_name, given_task_id):
#     check = False
#     for fac in game_obj.game_factions:
#         if fac.name == fac_name:
#             if len(fac.population) > 0:
#                 check = True
#     if check:  # Search for nearby tiles, where characters can cut mashrooms
#
#         x_pos = tile_xy[0]
#         y_pos = tile_xy[1]
#         TileNum = (y_pos - 1) * game_stats.cur_level_width + x_pos
#
#         candidates = []
#         for fac in game_obj.game_factions:
#             if fac.name == fac_name:
#                 for pop in fac.population:
#                     if pop.occupation == "not occupied":
#
#                         if pop.location % game_stats.cur_level_width == 0:
#                             x = game_stats.cur_level_width
#                         else:
#                             x = pop.location % game_stats.cur_level_width
#                         y = math.ceil(pop.location / game_stats.cur_level_width)
#                         print("Character's location " + str([x, y]) + " with ID " + str(pop.personal_id))
#                         candidates.append([[x, y], pop.personal_id])
#         print("Candidates for work: " + str(candidates))
#         list_routes = []
#         if len(candidates) > 0:
#             for candidate in candidates:
#                 print("Path for " + str(candidate) + " moving to " + str(tile_xy))
#                 route = algo_astar.astar(candidate[0], tile_xy)
#                 if len(route) > 0:
#                     new_route = found_path(candidate[0], candidate[1], route, len(route))
#                     list_routes.append(new_route)
#                     print("Success " + str(len(route)))
#
#         # Get the optimal character and route
#         current_route = None
#         current_index = None
#         if len(list_routes) > 0:
#             current_route = list_routes[0]
#             current_index = 0
#             for index, item in enumerate(list_routes):
#                 if item.distance < current_route.distance:
#                     current_route = item
#                     current_index = index
#             print("Distance of current route - " + str(current_route.distance) + " Char ID - " + str(
#                 current_route.personal_id))
#
#             # Updating task list with performer ID
#             for task in game_obj.task_list:
#                 if task.task_id == given_task_id:
#                     print("Task ID is " + str(task.task_id))
#                     task.performer = current_route.personal_id
#
#             # Assigning new mining task to unoccupied character
#             for fac in game_obj.game_factions:
#                 if fac.name == fac_name:
#                     for pop in fac.population:
#                         if pop.personal_id == current_route.personal_id:
#                             new_task = game_classes.work_task("Commuting", current_route.path, tile_xy,
#                                                               "Mashroom cutting", given_task_id)
#                             pop.goal = new_task
#                             pop.occupation = "commuting"


# def search_delivery(res_list, position, fac_name, given_task_id):
#     check = False
#     for fac in game_obj.game_factions:
#         if fac.name == fac_name:
#             if len(fac.population) > 0:
#                 check = True
#
#     if check:  # Search for tiles with resources
#         res_tiles = []  # List of lists ["Resource name", amount, coordinates]
#
#         for resource in res_list:
#
#             for TileObj in game_obj.game_map:
#                 if [TileObj.posxy[0], TileObj.posxy[1]] in game_stats.known_map and [TileObj.posxy[0],
#                                                                                      TileObj.posxy[1]] != position:
#                     if TileObj.tunnels:
#                         if len(TileObj.output) > 0:
#                             item_reserve = []
#                             for item in TileObj.output:
#                                 if item == resource:
#                                     if len(res_tiles) == 0:
#                                         res_tiles.append([resource, 1, [TileObj.posxy[0], TileObj.posxy[1]]])
#                                     else:
#                                         check2 = True
#                                         for res in res_tiles:  # Same resource
#                                             if res[0] == resource and res[2] == [TileObj.posxy[0], TileObj.posxy[1]]:
#                                                 if TileObj.output.count(item) > res[1]:
#                                                     res[1] += 1
#                                                     check2 = False
#
#                                         if check2:
#                                             res_tiles.append([resource, 1, [TileObj.posxy[0], TileObj.posxy[1]]])
#
#         if len(res_tiles) > 0:
#             print("Resources: " + str(res_tiles))
#             candidates = []
#             for fac in game_obj.game_factions:
#                 if fac.name == fac_name:
#                     for pop in fac.population:
#                         ##                        print
#                         if pop.occupation == "not occupied":
#
#                             if pop.location % game_stats.cur_level_width == 0:
#                                 x = game_stats.cur_level_width
#                             else:
#                                 x = pop.location % game_stats.cur_level_width
#                             y = math.ceil(pop.location / game_stats.cur_level_width)
#                             print("Character's location " + str([x, y]) + " with ID " + str(pop.personal_id))
#                             candidates.append([[x, y], pop.personal_id])
#             print("Candidates for work: " + str(candidates))
#             list_routes = []
#             if len(candidates) > 0:
#                 for res_tile in res_tiles:
#                     for candidate in candidates:
#                         print("Path for " + str(candidate) + " moving to " + str(res_tile[2]))
#                         route = algo_astar.astar(candidate[0], res_tile[2])
#                         if len(route) > 0:
#                             new_route = found_path(candidate[0], candidate[1], route, len(route))
#                             list_routes.append(new_route)
#                             print("Success " + str(len(route)))
#
#             # Get the optimal character and route
#             current_route = None
#             current_index = None
#             if len(list_routes) > 0:
#                 current_route = list_routes[0]
#                 current_index = 0
#                 for index, item in enumerate(list_routes):
#                     if item.distance < current_route.distance:
#                         current_route = item
#                         current_index = index
#                 print("Distance of current route - " + str(current_route.distance) + " Char ID - " + str(
#                     current_route.personal_id))
#
#                 # Updating task list with performer ID
#                 for task in game_obj.task_list:
#                     if task.task_id == given_task_id:
#                         print("Task ID is " + str(task.task_id))
#                         task.performer = current_route.personal_id
#
#                 # Assigning new delivering task to unoccupied character
#                 for fac in game_obj.game_factions:
#                     if fac.name == fac_name:
#                         for pop in fac.population:
#                             if pop.personal_id == current_route.personal_id:
#                                 new_task = game_classes.work_task("Commuting", current_route.path, position,
#                                                                   "Pick up resource", given_task_id)
#                                 pop.goal = new_task
#                                 pop.goal.delivery_list = res_list
#                                 pop.occupation = "commuting"
#                                 pop.goal.purpose = "for building"
#                                 # if pop.AP > 0:
#                                 #     game_basic.stage2_actions_repeat()


# def search_complete_delivery(tile_xy, fac_name, given_task_id, char_id):
#     check = False
#     for fac in game_obj.game_factions:
#         if fac.name == fac_name:
#             if len(fac.population) > 0:
#                 check = True
#     if check:
#
#         x_pos = tile_xy[0]
#         y_pos = tile_xy[1]
#         TileNum = (y_pos - 1) * game_stats.cur_level_width + x_pos
#
#         candidates = []
#         for fac in game_obj.game_factions:
#             if fac.name == fac_name:
#                 for pop in fac.population:
#                     if pop.personal_id == char_id:
#
#                         if pop.location % game_stats.cur_level_width == 0:
#                             x = game_stats.cur_level_width
#                         else:
#                             x = pop.location % game_stats.cur_level_width
#                         y = math.ceil(pop.location / game_stats.cur_level_width)
#                         print("Character's location " + str([x, y]) + " with ID " + str(pop.personal_id))
#                         candidates.append([[x, y], pop.personal_id])
#
#         list_routes = []
#         if len(candidates) > 0:
#             for candidate in candidates:
#                 print("Path for " + str(candidate) + " moving to " + str(tile_xy))
#                 route = algo_astar.astar(candidate[0], tile_xy)
#                 if len(route) > 0:
#                     new_route = found_path(candidate[0], candidate[1], route, len(route))
#                     list_routes.append(new_route)
#                     print("Success " + str(len(route)))
#
#         # Get the optimal character and route
#         current_route = None
#         current_index = None
#         if len(list_routes) > 0:
#             current_route = list_routes[0]
#             current_index = 0
#             for index, item in enumerate(list_routes):
#                 if item.distance < current_route.distance:
#                     current_route = item
#                     current_index = index
#             print("Distance of current route - " + str(current_route.distance) + " Char ID - " + str(
#                 current_route.personal_id))
#
#             # Assigning new mining task to unoccupied character
#             for fac in game_obj.game_factions:
#                 if fac.name == fac_name:
#                     for pop in fac.population:
#                         if pop.personal_id == current_route.personal_id:
#                             pop.goal.route = current_route.path
#
#                             pop.occupation = "commuting"
#                             # if pop.AP > 0:
#                             #     game_basic.stage2_actions_repeat()


# def search_builder(tile_xy, fac_name, given_task_id):
#     print("search_builder function is started")
#     check = False
#     for fac in game_obj.game_factions:
#         if fac.name == fac_name:
#             if len(fac.population) > 0:
#                 check = True
#     if check:
#
#         x_pos = tile_xy[0]
#         y_pos = tile_xy[1]
#         TileNum = (y_pos - 1) * game_stats.cur_level_width + x_pos
#
#         candidates = []
#         for fac in game_obj.game_factions:
#             if fac.name == fac_name:
#                 for pop in fac.population:
#                     if pop.occupation == "not occupied":
#
#                         if pop.location % game_stats.cur_level_width == 0:
#                             x = game_stats.cur_level_width
#                         else:
#                             x = pop.location % game_stats.cur_level_width
#                         y = math.ceil(pop.location / game_stats.cur_level_width)
#                         print("Character's location " + str([x, y]) + " with ID " + str(pop.personal_id))
#                         candidates.append([[x, y], pop.personal_id])
#         print("Candidates for building: " + str(candidates))
#         list_routes = []
#         if len(candidates) > 0:
#             for candidate in candidates:
#                 print("Path for " + str(candidate) + " moving to " + str(tile_xy))
#                 route = algo_astar.astar(candidate[0], tile_xy)
#                 if len(route) > 0:
#                     new_route = found_path(candidate[0], candidate[1], route, len(route))
#                     list_routes.append(new_route)
#                     print("Success " + str(len(route)))
#
#         # Get the optimal character and route
#         current_route = None
#         current_index = None
#         if len(list_routes) > 0:
#             current_route = list_routes[0]
#             current_index = 0
#             for index, item in enumerate(list_routes):
#                 if item.distance < current_route.distance:
#                     current_route = item
#                     current_index = index
#             print("Distance of current route - " + str(current_route.distance) + " Char ID - " + str(
#                 current_route.personal_id))
#
#             # Updating task list with performer ID
#             for task in game_obj.task_list:
#                 if task.task_id == given_task_id:
#                     print("Task ID is " + str(task.task_id))
#                     task.performer = current_route.personal_id
#
#             # Assigning new building task to unoccupied character
#             for fac in game_obj.game_factions:
#                 if fac.name == fac_name:
#                     for pop in fac.population:
#                         if pop.personal_id == current_route.personal_id:
#                             print("Assigning new task to build a structure to character")
#                             new_task = game_classes.work_task("Commuting", current_route.path, tile_xy,
#                                                               "Build structure", given_task_id)
#                             pop.goal = new_task
#                             pop.occupation = "commuting"
