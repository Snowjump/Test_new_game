## Among Myth and Wonder
## create_unit

# import copy
from Storage.Neutrals import neutrals_new_units
from Storage.Knight_Lords import knight_lords_new_units


LE_units_dict_by_alignment = {"Neutrals" : neutrals_new_units.unit_creation_dict,
                              "Knight Lords" : knight_lords_new_units.unit_creation_dict}


def fill_with_creatures(number, rows, dictionary, creature_name):
    creature_list = []
    for i in range(1, rows*number + 1):  # Temporary for testing (-2)
        creature_list.append(dictionary[creature_name]())

    return list(creature_list)
