## Among Myth and Wonder
## lair_army_catalog

import copy

from Storage import create_unit


def runaway_serfs_refuge_army(units):
    # 6 peasant mob
    # 4 peasant bowmen
    units_list = create_unit.LE_units_dict_by_alignment["Knight Lords"]

    for i in range(6):
        units.append(units_list["Peasant mob"]())

    for i in range(4):
        units.append(units_list["Peasant bowmen"]())


def treasure_tower_army(units):
    # 2 crossbowmen
    # 2 spear footmen
    # 1 sword footmen
    # 1 knights
    units_list = create_unit.LE_units_dict_by_alignment["Knight Lords"]

    for i in range(2):
        units.append(units_list["Crossbowmen"]())

    for i in range(2):
        units.append(units_list["Spear footmen"]())

    for i in range(1):
        units.append(units_list["Sword footmen"]())

    for i in range(1):
        units.append(units_list["Knights"]())


def lair_of_grey_dragons_army(units):

    # 2 Grey dragons
    # 1 Grey drakes
    units_list = create_unit.LE_units_dict_by_alignment["Neutrals"]

    for i in range(2):
        units.append(units_list["Grey dragon"]())

    for i in range(1):
        units.append(units_list["Grey drakes"]())


lair_dictionary = {"Runaway serfs refuge" : runaway_serfs_refuge_army,
                   "Treasure tower" : treasure_tower_army,
                   "Lair of grey dragons" : lair_of_grey_dragons_army}
