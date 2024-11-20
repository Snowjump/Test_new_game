## Among Myth and Wonder
## new_heroes_catalog

from Resources import game_classes

# Images
knight_lords_heroes_img = {"Knight" : ["knight_hero_icon", "KL", 12, 2],
                           "Priest of Salvation" : ["priest_hero_icon", "KL", 14, 8]}

nature_keepers_heroes_img = {}

heroes_img_dict_by_alignment = {"Knight Lords" : knight_lords_heroes_img,
                                "Nature Keepers" : nature_keepers_heroes_img}

# Heroes' classes
knight_lords_heroes_classes = ["Knight", "Priest of Salvation"]

nature_keepers_heroes_classes = []

heroes_classes_dict_by_alignment = {"Knight Lords" : knight_lords_heroes_classes,
                                    "Nature Keepers" : nature_keepers_heroes_classes}

# Basic heroes details
# Class name, magic power, knowledge, level, img, img_source, x_offset, y_offset
knight_lords_basic_heroes = {"Knight" : ["Knight", 0, 1, 1,
                                         "knight_hero_icon", "KL", 12, 4,  # 10, 6  # 5, 1
                                         [game_classes.Attribute_Package([game_classes.Battle_Attribute(
                                                                              "melee infantry",
                                                                              "defence",
                                                                              1)]),
                                          game_classes.Attribute_Package([game_classes.Battle_Attribute(
                                                                              "melee cavalry",
                                                                              "defence",
                                                                              1)])]],
                             "Priest of Salvation": ["Priest of Salvation", 1, 2, 1,
                                                     "priest_hero_icon", "KL", 15, 8,  # 10, 6  # 5, 1
                                                     [game_classes.Attribute_Package([game_classes.Battle_Attribute(
                                                                                     "caster",
                                                                                     "defence",
                                                                                     2)]),
                                                      game_classes.Attribute_Package([game_classes.Battle_Attribute(
                                                                                     "ranged infantry",
                                                                                     "defence",
                                                                                     1)])]]
                             }

nature_keepers_basic_heroes = []

basic_heroes_dict_by_alignment = {"Knight Lords" : knight_lords_basic_heroes,
                                  "Nature Keepers" : nature_keepers_basic_heroes}
