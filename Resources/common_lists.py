## Among Myth and Wonder
## common_lists

import math

from Resources import game_obj


def reversed_list_cleaning(target_list, index_list):
    if index_list:  # If index list is filled with indexes of elements to be deleted
        index_list = sorted(index_list, reverse=True)
        for index in index_list:
            del target_list[index]


def legitimate_settlement_targets(realm):
    targets = []
    at_war_list = realms_at_war(realm)

    for settlement in game_obj.game_cities:
        if settlement.military_occupation:
            if settlement.owner == realm.name and settlement.military_occupation[2] in at_war_list:
                # Own settlement occupied by enemy
                targets.append([settlement.city_id, settlement.posxy, settlement.location])
        else:
            if settlement.owner in at_war_list:
                if settlement.posxy in realm.known_map:
                    # Unoccupied enemy settlements with known location
                    targets.append([settlement.city_id, settlement.posxy, settlement.location])

    return targets


def realms_at_war(realm):
    at_war_list = []
    for enemy in realm.relations.at_war:
        at_war_list.append(enemy[2])
    return at_war_list
