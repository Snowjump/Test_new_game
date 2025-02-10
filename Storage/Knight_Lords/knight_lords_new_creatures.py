## Among Myth and Wonder
## knight_lords_new_creatures

from Resources import game_classes


def create_peasant_mob():
    new_unit = game_classes.Creature("Peasant mob",
                                     "peasant_mob",
                                     "KL", 12, 30,  # Img_source, img width, img height
                                     7)  # HP
    return new_unit


def create_peasant_bowmen():
    new_unit = game_classes.Creature("Peasant bowmen",
                                     "peasant_bowmen",
                                     "KL", 16, 27,  # Img_source, img width, img height
                                     7)  # HP
    return new_unit


def create_crossbowmen():
    new_unit = game_classes.Creature("Crossbowmen",
                                     "crossbowmen",
                                     "KL", 16, 29,  # Img_source, img width, img height
                                     8)  # HP
    return new_unit


def create_spear_footmen():
    new_unit = game_classes.Creature("Spear footmen",
                                     "spear_footmen",
                                     "KL", 16, 29,  # Img_source, img width, img height
                                     8)  # HP
    return new_unit


def create_sword_footmen():
    new_unit = game_classes.Creature("Sword footmen",
                                     "sword_footmen",
                                     "KL", 20, 28,  # Img_source, img width, img height
                                     8)  # HP
    return new_unit


def create_squires():
    new_unit = game_classes.Creature("Squires",
                                     "squires",
                                     "KL", 19, 27,  # Img_source, img width, img height
                                     8)  # HP
    return new_unit


def create_knights():
    new_unit = game_classes.Creature("Knights",
                                     "knights",
                                     "KL", 34, 39,  # Img_source, img width, img height
                                     16)  # HP
    return new_unit


def create_priests_of_salvation():
    new_unit = game_classes.Creature("Priests of Salvation",
                                     "priests_of_salvation",
                                     "KL", 11, 28,  # Img_source, img width, img height
                                     8)  # HP
    return new_unit


def create_battle_monks():
    new_unit = game_classes.Creature("Battle monks",
                                     "battle_monks",
                                     "KL", 22, 28,  # Img_source, img width, img height
                                     8)  # HP
    return new_unit


def create_griffons():
    new_unit = game_classes.Creature("Griffons",
                                     "griffons",
                                     "KL", 44, 29,  # Img_source, img width, img height
                                     20)  # HP
    return new_unit


def create_pegasus_knights():
    new_unit = game_classes.Creature("Pegasus knights",
                                     "pegasus_knights",
                                     "KL", 40, 37,  # Img_source, img width, img height
                                     16)  # HP
    return new_unit


def create_field_ballistas():
    new_unit = game_classes.Creature("Field ballistas",
                                     "field_ballistas",
                                     "KL", 42, 34,  # Img_source, img width, img height
                                     25)  # HP
    return new_unit


creature_creation_dict = {"Peasant mob": create_peasant_mob,
                          "Peasant bowmen": create_peasant_bowmen,
                          "Crossbowmen": create_crossbowmen,
                          "Spear footmen": create_spear_footmen,
                          "Sword footmen": create_sword_footmen,
                          "Squires": create_squires,
                          "Knights": create_knights,
                          "Priests of Salvation": create_priests_of_salvation,
                          "Battle monks": create_battle_monks,
                          "Griffons": create_griffons,
                          "Pegasus knights": create_pegasus_knights,
                          "Field ballistas": create_field_ballistas}
