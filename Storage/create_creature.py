## Miracle battles!

from Resources import game_classes

LE_neutrals_new_creatures = []

LE_knight_lords_new_creatures = []

LE_nature_keepers_new_creatures = []

LE_creatures_dict_by_alignment = {"Neutrals" : LE_neutrals_new_creatures,
                              "Knight Lords" : LE_knight_lords_new_creatures,
                              "Nature Keepers" : LE_nature_keepers_new_creatures}


def create_creatures_neutrals():
    # 1 - Rolagar anarchists
    LE_neutrals_new_creatures.append(game_classes.Creature("Simurg's anarchists",
                                                           "simurg_anarchists",
                                                           "neutrals", 23, 27,  # Img_source, img width, img height
                                                           7))  # HP

    # 2 - Bandit archers
    LE_neutrals_new_creatures.append(game_classes.Creature("Bandit archers",
                                                           "bandit_archers",
                                                           "neutrals", 20, 27,  # Img_source, img width, img height
                                                           8))  # HP

    # 3 - Highway robbers
    LE_neutrals_new_creatures.append(game_classes.Creature("Highway robbers",
                                                           "highway_robbers",
                                                           "neutrals", 23, 27,  # Img_source, img width, img height
                                                           8))  # HP

    # 4 - Robber knights
    LE_neutrals_new_creatures.append(game_classes.Creature("Robber knights",
                                                           "robber_knights",
                                                           "neutrals", 23, 27,  # Img_source, img width, img height
                                                           16))  # HP


create_creatures_neutrals()
