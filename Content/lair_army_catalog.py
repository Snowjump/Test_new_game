## Miracle battles
## lair_army_catalog

import copy

from Storage import create_unit


def runaway_serfs_refuge_army(units):
    # 6 peasant mob
    # 4 peasant archers
    units_list = list(create_unit.LE_units_dict_by_alignment["Knight Lords"])

    for i in range(6):
        units.append(copy.deepcopy(units_list[0]))

    for i in range(4):
        units.append(copy.deepcopy(units_list[1]))


def treasure_tower_army(units):
    # 2 crossbowmen
    # 2 spear footmen
    # 1 sword footmen
    # 1 knights
    units_list = list(create_unit.LE_units_dict_by_alignment["Knight Lords"])

    for i in range(2):
        units.append(copy.deepcopy(units_list[2]))

    for i in range(2):
        units.append(copy.deepcopy(units_list[3]))

    for i in range(1):
        units.append(copy.deepcopy(units_list[4]))

    for i in range(1):
        units.append(copy.deepcopy(units_list[6]))


def lair_of_grey_dragons_army(units):
    # 2 Grey dragons
    # 1 Grey drakes
    units_list = list(create_unit.LE_units_dict_by_alignment["Neutrals"])

    for i in range(2):
        units.append(copy.deepcopy(units_list[4]))

    for i in range(1):
        units.append(copy.deepcopy(units_list[5]))


lair_dictionary = {"Runaway serfs refuge" : runaway_serfs_refuge_army,
                   "Treasure tower" : treasure_tower_army,
                   "Lair of grey dragons" : lair_of_grey_dragons_army}
