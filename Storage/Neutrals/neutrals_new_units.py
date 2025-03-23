## Among Myth and Wonder
## neutrals_new_units

from Resources import game_classes
from Resources import skill_classes
from Storage import create_unit
from Storage.Neutrals import neutrals_new_creatures

creature_dict = neutrals_new_creatures.creature_creation_dict


def create_simurg_anarchists():
    new_unit = game_classes.Regiment("Simurg's anarchists", 4,  # name, rank
                                     "simurg_anarchists",  # img
                                     "neutrals", 16, 14, 5,  # img_source, x_offset, y_offset, speed
                                     23, 27,  # img width, img height
                                     # Base HP, max mana reserve, base MP, number and rows
                                     7, 0, 0, 5, 4,
                                     ["melee", "melee infantry"],
                                     create_unit.fill_with_creatures(5, 4, creature_dict, "Simurg's anarchists"),
                                     # creatures
                                     [game_classes.Strike("Melee assault", "Melee",
                                                          ["Melee", "Physical"],
                                                          3, 6, 4,  # min_dmg, max_dmg, mastery
                                                          0, 0)],  # effective and limit range
                                     2, 1, 3,  # Armour and defence and leadership
                                     # Skills
                                     [skill_classes.Battle_Skill("Inflamed weapons",
                                                                 "additional melee damage",
                                                                 1,
                                                                 "Separate damage",
                                                                 None,
                                                                 ["Magical", "Fire"])],
                                     [["Florins", 7], ["Armament", 6]],
                                     # Abilities
                                     [])
    return new_unit


def create_bandit_archers():
    new_unit = game_classes.Regiment("Bandit archers", 4,  # name, rank
                                     "bandit_archers",  # img
                                     "neutrals", 17, 14, 6,  # img_source, x_offset, y_offset, speed
                                     20, 27,  # img width, img height
                                     # Base HP, max mana reserve, base MP, number and rows
                                     8, 0, 0, 5, 4,
                                     ["ranged", "ranged infantry"],
                                     create_unit.fill_with_creatures(5, 4, creature_dict, "Bandit archers"),
                                     # creatures
                                     [game_classes.Strike("Melee assault", "Melee",
                                                          ["Melee", "Physical"],
                                                          1, 2, 2,  # min_dmg, max_dmg, mastery
                                                          0, 0),  # effective and limit range
                                      game_classes.Strike("Shooting", "Ranged",
                                                          ["Ranged", "Physical"],
                                                          2, 4, 6,  # min_dmg, max_dmg, mastery
                                                          6, 12)],  # effective and limit range
                                     1, 1, 4,  # Armour and defence and base leadership
                                     # Skills
                                     [],
                                     [["Florins", 8], ["Armament", 6]],
                                     # Abilities
                                     [])
    return new_unit


def create_highway_robbers():
    new_unit = game_classes.Regiment("Highway robbers", 6,  # name, rank
                                     "highway_robbers",  # img
                                     "neutrals", 16, 14, 6,  # img_source, x_offset, y_offset, speed
                                     23, 27,  # img width, img height
                                     # Base HP, max mana reserve, base MP, number and rows
                                     8, 0, 0, 5, 4,
                                     ["melee", "melee infantry"],
                                     create_unit.fill_with_creatures(5, 4, creature_dict, "Highway robbers"),
                                     # creatures
                                     [game_classes.Strike("Melee assault", "Melee",
                                                          ["Melee", "Physical"],
                                                          3, 7, 5,  # min_dmg, max_dmg, mastery
                                                          0, 0)],  # effective and limit range
                                     2, 2, 4,  # Armour and defence and base leadership
                                     # Skills
                                     [],
                                     [["Florins", 8], ["Armament", 7]],
                                     # Abilities
                                     [])
    return new_unit


def create_robber_knights():
    new_unit = game_classes.Regiment("Robber knights", 10,  # name, rank
                                     "robber_knights",  # img
                                     "neutrals", 10, 5, 9,  # img_source, x_offset, y_offset, speed
                                     27, 39,  # img width, img height
                                     # Base HP, max mana reserve, base MP, number and rows
                                     16, 0, 0, 4, 2,
                                     ["melee", "melee cavalry"],
                                     create_unit.fill_with_creatures(4, 2, creature_dict, "Robber knights"),
                                     # creatures
                                     [game_classes.Strike("Melee assault", "Melee",
                                                          ["Melee", "Physical"],
                                                          4, 8, 8,  # min_dmg, max_dmg, mastery
                                                          0, 0)],  # effective and limit range
                                     4, 4, 4,  # Armour and defence and leadership
                                     # Skills
                                     [skill_classes.Battle_Skill("Heavy charge",
                                                                 "charge",
                                                                 0.5,
                                                                 "Increase damage",
                                                                 "Heavy charge",
                                                                 [])],
                                     [["Florins", 20], ["Armament", 12]],
                                     # Abilities
                                     [])
    return new_unit


def create_grey_dragon():
    new_unit = game_classes.Regiment("Grey dragon", 20,  # name, rank
                                     "grey_dragon",  # img
                                     "neutrals", -1, 0, 12,  # img_source, x_offset, y_offset, speed
                                     60, 58,  # img width, img height
                                     # Base HP, max mana reserve, base MP, number and rows
                                     145, 0, 0, 1, 1,
                                     ["melee", "gargantuan"],
                                     create_unit.fill_with_creatures(1, 1, creature_dict, "Grey dragon"),  # creatures
                                     [game_classes.Strike("Dragon breath", "Melee",
                                                          ["Melee", "Fire", "Dragon breath"],
                                                          5, 8, 6,  # min_dmg, max_dmg, mastery
                                                          0, 0),  # effective and limit range
                                      game_classes.Strike("Melee assault", "Melee",
                                                          ["Melee", "Physical"],
                                                          21, 38, 10,  # min_dmg, max_dmg, mastery
                                                          0, 0)],  # effective and limit range
                                     4, 5, 5,  # Armour and defence and leadership
                                     # Skills
                                     [skill_classes.Battle_Skill("Fly",
                                                                 "Movement",
                                                                 None,
                                                                 None,
                                                                 "Can fly",
                                                                 []),
                                      skill_classes.Battle_Skill("Fire resistance 50%",
                                                                 "Resistance",
                                                                 2,
                                                                 "division",
                                                                 None,
                                                                 ["Fire"])
                                      ],
                                     [["Florins", 200], ["Food", 80]],
                                     # Abilities
                                     [])
    return new_unit


def create_grey_drakes():
    new_unit = game_classes.Regiment("Grey drakes", 15,  # name, rank
                                     "grey_drakes",  # img
                                     "neutrals", 8, 4, 12,  # img_source, x_offset, y_offset, speed
                                     32, 40,  # img width, img height
                                     # Base HP, max mana reserve, base MP, number and rows
                                     36, 0, 0, 2, 2,
                                     ["melee", "monster"],
                                     create_unit.fill_with_creatures(2, 2, creature_dict, "Grey drakes"),  # creatures
                                     [game_classes.Strike("Drake breath", "Melee",
                                                          ["Melee", "Fire", "Drake breath"],
                                                          4, 6, 6,  # min_dmg, max_dmg, mastery
                                                          0, 0),  # effective and limit range
                                      game_classes.Strike("Melee assault", "Melee",
                                                          ["Melee", "Physical"],
                                                          12, 18, 8,  # min_dmg, max_dmg, mastery
                                                          0, 0)],  # effective and limit range
                                     3, 4, 4,  # Armour and defence and leadership
                                     # Skills
                                     [skill_classes.Battle_Skill("Fly",
                                                                 "Movement",
                                                                 None,
                                                                 None,
                                                                 "Can fly",
                                                                 []),
                                      skill_classes.Battle_Skill("Fire resistance 50%",
                                                                 "Resistance",
                                                                 2,
                                                                 "division",
                                                                 None,
                                                                 ["Fire"])
                                      ],
                                     [["Florins", 40], ["Food", 10]],
                                     # Abilities
                                     [])
    return new_unit


unit_creation_dict = {"Simurg's anarchists": create_simurg_anarchists,
                      "Bandit archers": create_bandit_archers,
                      "Highway robbers": create_highway_robbers,
                      "Robber knights": create_robber_knights,
                      "Grey dragon": create_grey_dragon,
                      "Grey drakes": create_grey_drakes}
