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
                                                           "neutrals", 27, 39,  # Img_source, img width, img height
                                                           16))  # HP

    # 5 - Grey dragon
    LE_neutrals_new_creatures.append(game_classes.Creature("Grey dragon",
                                                           "grey_dragon",
                                                           "neutrals", 60, 58,  # Img_source, img width, img height
                                                           145))  # HP

    # 6 - Grey drakes
    LE_neutrals_new_creatures.append(game_classes.Creature("Grey drakes",
                                                           "grey_drakes",
                                                           "neutrals", 32, 40,  # Img_source, img width, img height
                                                           36))  # HP


def create_creatures_KL():
    # 1 - Peasant mob
    LE_knight_lords_new_creatures.append(game_classes.Creature("Peasant mob",
                                                               "peasant_mob",
                                                               "KL", 12, 30,  # Img_source, img width, img height
                                                               7))  # HP

    # 2 - Peasant bowmen
    LE_knight_lords_new_creatures.append(game_classes.Creature("Peasant bowmen",
                                                               "peasant_bowmen",
                                                               "KL", 16, 27,  # Img_source, img width, img height
                                                               7))  # HP

    # 3 - Crossbowmen
    LE_knight_lords_new_creatures.append(game_classes.Creature("Crossbowmen",
                                                               "crossbowmen",
                                                               "KL", 16, 29,  # Img_source, img width, img height
                                                               8))  # HP

    # 4 - Spear footmen
    LE_knight_lords_new_creatures.append(game_classes.Creature("Spear footmen",
                                                               "spear_footmen",
                                                               "KL", 16, 29,  # Img_source, img width, img height
                                                               8))  # HP

    # 5 - Sword footmen
    LE_knight_lords_new_creatures.append(game_classes.Creature("Sword footmen",
                                                               "sword_footmen",
                                                               "KL", 20, 28,  # Img_source, img width, img height
                                                               8))  # HP

    # 6 - Squires
    LE_knight_lords_new_creatures.append(game_classes.Creature("Squires",
                                                               "squire",
                                                               "KL", 19, 27,  # Img_source, img width, img height
                                                               8))  # HP

    # 7 - Knights
    LE_knight_lords_new_creatures.append(game_classes.Creature("Knights",
                                                               "knights",
                                                               "KL", 34, 39,  # Img_source, img width, img height
                                                               16))  # HP

    # 8 - Priests of Salvation
    LE_knight_lords_new_creatures.append(game_classes.Creature("Priests of Salvation",
                                                               "priests_of_salvation",
                                                               "KL", 11, 28,  # Img_source, img width, img height
                                                               8))  # HP

    # 9 - Battle monks
    LE_knight_lords_new_creatures.append(game_classes.Creature("Battle monks",
                                                               "battle_monks",
                                                               "KL", 22, 28,  # Img_source, img width, img height
                                                               8))  # HP

    # 10 - Griffons
    LE_knight_lords_new_creatures.append(game_classes.Creature("Griffons",
                                                               "griffons",
                                                               "KL", 44, 29,  # Img_source, img width, img height
                                                               20))  # HP

    # 11 - Pegasus knights
    LE_knight_lords_new_creatures.append(game_classes.Creature("Pegasus knights",
                                                               "pegasus_knights",
                                                               "KL", 40, 37,  # Img_source, img width, img height
                                                               16))  # HP

    # 12 - Field ballistas
    LE_knight_lords_new_creatures.append(game_classes.Creature("Field ballistas",
                                                               "field_ballistas",
                                                               "KL", 42, 34,  # Img_source, img width, img height
                                                               25))  # HP


create_creatures_neutrals()
create_creatures_KL()
