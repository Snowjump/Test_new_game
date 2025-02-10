## Among Myth and Wonder
## neutrals_new_creatures

from Resources import game_classes


def create_simurg_anarchists():
    new_unit = game_classes.Creature("Simurg's anarchists",
                                     "simurg_anarchists",
                                     "neutrals", 23, 27,  # Img_source, img width, img height
                                     7)  # HP
    return new_unit


def create_bandit_archers():
    new_unit = game_classes.Creature("Bandit archers",
                                     "bandit_archers",
                                     "neutrals", 20, 27,  # Img_source, img width, img height
                                     8)  # HP
    return new_unit


def create_highway_robbers():
    new_unit = game_classes.Creature("Highway robbers",
                                     "highway_robbers",
                                     "neutrals", 23, 27,  # Img_source, img width, img height
                                     8)  # HP
    return new_unit


def create_robber_knights():
    new_unit = game_classes.Creature("Robber knights",
                                     "robber_knights",
                                     "neutrals", 27, 39,  # Img_source, img width, img height
                                     16)  # HP
    return new_unit


def create_grey_dragon():
    new_unit = game_classes.Creature("Grey dragon",
                                     "grey_dragon",
                                     "neutrals", 60, 58,  # Img_source, img width, img height
                                     145)  # HP
    return new_unit


def create_grey_drakes():
    new_unit = game_classes.Creature("Grey drakes",
                                     "grey_drakes",
                                     "neutrals", 32, 40,  # Img_source, img width, img height
                                     36)  # HP
    return new_unit


creature_creation_dict = {"Simurg's anarchists": create_simurg_anarchists,
                          "Bandit archers": create_bandit_archers,
                          "Highway robbers": create_highway_robbers,
                          "Robber knights": create_robber_knights,
                          "Grey dragon": create_grey_dragon,
                          "Grey drakes": create_grey_drakes}
