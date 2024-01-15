## Among Myth and Wonder
## exploration_targets

from Resources import game_stats
from Resources import common_checks
from Resources import game_obj

shifts = [[-5, -5], [0, -5], [5, -5],
          [-5, 0],           [5, 0],
          [-5, 5],  [0, 5],  [5, 5]]


def collect_new_exploration_targets(realm, known_territory, targets):
    # print("")
    # print("collect_new_exploration_targets() - " + str(realm.name))
    # known_territory (realm.known_map) - list of lists [int x, int y]
    # targets (realm.AI_cogs.exploration_targets) - list of lists [int x, int y]
    avoid_friendly_settlements = friendly_cities(realm.name)
    # print("avoid_friendly_settlements: " + str(avoid_friendly_settlements))
    for orig_tile in known_territory:  # original tile
        for i in shifts:
            new_tile = [orig_tile[0] + i[0], orig_tile[1] + i[1]]
            new_tile_num = (new_tile[1] - 1) * game_stats.cur_level_width + new_tile[0] - 1
            # print("new_tile - " + str(new_tile))
            if acceptable_target(new_tile, new_tile_num, avoid_friendly_settlements, realm, targets):
                # print("new_tile - " + str(new_tile))
                targets.append(new_tile)

    print(realm.name + " targets: " + str(targets))


def friendly_cities(realm_name):
    list_of_cities = []
    for settlement in game_obj.game_cities:
        if settlement.owner == realm_name:
            list_of_cities.append(settlement.city_id)

    return list_of_cities


def acceptable_target(new_tile, new_tile_num, avoid_friendly_settlements, realm, targets):
    # New targets shouldn't be closer more than 5 tiles from other targets
    distance = 5
    verdict = False
    if common_checks.within_map_limits(new_tile):
        # print("new_tile - " + str(new_tile))
        if new_tile not in realm.known_map:
            # print("new_tile - " + str(new_tile))
            if game_obj.game_map[new_tile_num].city_id not in avoid_friendly_settlements:
                # print("new_tile - " + str(new_tile))
                no_intersection = True
                for target in targets:
                    if distance ** 2 > ((target[0] - new_tile[0]) ** 2) + ((target[1] - new_tile[1]) ** 2):
                        # print("new_tile - " + str(new_tile))
                        no_intersection = False
                        break

                if no_intersection:
                    verdict = True

    return verdict
