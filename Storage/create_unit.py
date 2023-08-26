## Miracle battles!

import copy
from Resources import game_classes
from Resources import skill_classes
from Storage import create_creature

LE_neutrals_new_units = []

LE_knight_lords_new_units = []

LE_nature_keepers_new_units = []

LE_units_dict_by_alignment = {"Neutrals" : LE_neutrals_new_units,
                              "Knight Lords" : LE_knight_lords_new_units,
                              "Nature Keepers" : LE_nature_keepers_new_units}


def create_neutrals():
    # 1 - Simurg anarchists
    LE_neutrals_new_units.append(game_classes.Regiment("Simurg's anarchists", 4,  # name, rank
                                                       "simurg_anarchists",  # img
                                                       "neutrals", 16, 14, 5,  # img_source, x_offset, y_offset, speed
                                                       23, 27,  # img width, img height
                                                       # Base HP, max mana reserve, base MP, number and rows
                                                       7, 0, 0, 5, 4,
                                                       ["melee", "melee infantry"],
                                                       fill_with_creatures(5, 4, "Neutrals", 0),  # creatures
                                                       [game_classes.Strike("Melee assault", "Melee",
                                                                            ["Melee", "Physical"],
                                                                            3, 5, 4,  # min_dmg, max_dmg, mastery
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
                                                       []))

    # 2 - Bandit archers
    LE_neutrals_new_units.append(game_classes.Regiment("Bandit archers", 4,  # name, rank
                                                       "bandit_archers",  # img
                                                       "neutrals", 17, 14, 6,  # img_source, x_offset, y_offset, speed
                                                       20, 27,  # img width, img height
                                                       # Base HP, max mana reserve, base MP, number and rows
                                                       8, 0, 0, 5, 4,
                                                       ["ranged", "ranged infantry"],
                                                       fill_with_creatures(5, 4, "Neutrals", 1),  # creatures
                                                       [game_classes.Strike("Melee assault", "Melee",
                                                                            ["Melee", "Physical"],
                                                                            1, 2, 2,  # min_dmg, max_dmg, mastery
                                                                            0, 0),  # effective and limit range
                                                        game_classes.Strike("Shooting", "Ranged",
                                                                            ["Ranged", "Physical"],
                                                                            1, 3, 4,  # min_dmg, max_dmg, mastery
                                                                            6, 12)],  # effective and limit range
                                                       1, 1, 4,  # Armour and defence and base leadership
                                                       # Skills
                                                       [],
                                                       [["Florins", 8], ["Armament", 6]],
                                                       # Abilities
                                                       []))

    # 3 - Highway robbers
    LE_neutrals_new_units.append(game_classes.Regiment("Highway robbers", 6,  # name, rank
                                                       "highway_robbers",  # img
                                                       "neutrals", 16, 14, 6,  # img_source, x_offset, y_offset, speed
                                                       23, 27,  # img width, img height
                                                       # Base HP, max mana reserve, base MP, number and rows
                                                       8, 0, 0, 5, 4,
                                                       ["melee", "melee infantry"],
                                                       fill_with_creatures(5, 4, "Neutrals", 2),  # creatures
                                                       [game_classes.Strike("Melee assault", "Melee",
                                                                            ["Melee", "Physical"],
                                                                            3, 6, 5,  # min_dmg, max_dmg, mastery
                                                                            0, 0)],  # effective and limit range
                                                       2, 2, 4,  # Armour and defence and base leadership
                                                       # Skills
                                                       [],
                                                       [["Florins", 8], ["Armament", 7]],
                                                       # Abilities
                                                       []))

    # 4 - Robber knights
    LE_neutrals_new_units.append(game_classes.Regiment("Robber knights", 10,  # name, rank
                                                       "robber_knights",  # img
                                                       "neutrals", 10, 5, 9,  # img_source, x_offset, y_offset, speed
                                                       27, 39,  # img width, img height
                                                       # Base HP, max mana reserve, base MP, number and rows
                                                       16, 0, 0, 4, 2,
                                                       ["melee", "melee cavalry"],
                                                       fill_with_creatures(4, 2, "Neutrals", 3),  # creatures
                                                       [game_classes.Strike("Melee assault", "Melee",
                                                                            ["Melee", "Physical"],
                                                                            4, 7, 8,  # min_dmg, max_dmg, mastery
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
                                                       []))

    # 5 - Grey dragon
    LE_neutrals_new_units.append(game_classes.Regiment("Grey dragon", 20,  # name, rank
                                                       "grey_dragon",  # img
                                                       "neutrals", -1, 0, 12,  # img_source, x_offset, y_offset, speed
                                                       60, 58,  # img width, img height
                                                       # Base HP, max mana reserve, base MP, number and rows
                                                       145, 0, 0, 1, 1,
                                                       ["melee", "gargantuan"],
                                                       fill_with_creatures(1, 1, "Neutrals", 4),  # creatures
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
                                                       []))

    # 6 - Grey drakes
    LE_neutrals_new_units.append(game_classes.Regiment("Grey drakes", 15,  # name, rank
                                                       "grey_drakes",  # img
                                                       "neutrals", 8, 4, 12,  # img_source, x_offset, y_offset, speed
                                                       32, 40,  # img width, img height
                                                       # Base HP, max mana reserve, base MP, number and rows
                                                       36, 0, 0, 2, 2,
                                                       ["melee", "monster"],
                                                       fill_with_creatures(2, 2, "Neutrals", 5),  # creatures
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
                                                       []))


def create_KL():
    # 1 - Peasant mob
    LE_knight_lords_new_units.append(game_classes.Regiment("Peasant mob", 3,  # name, rank
                                                           "peasant_mob",  # img
                                                           "KL", 20, 12, 5,  # img_source, x_offset, y_offset, speed
                                                           12, 30,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           7, 0, 0, 5, 4,
                                                           ["melee", "melee infantry", "peasant"],
                                                           fill_with_creatures(5, 4, "Knight Lords", 0),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                2, 4, 4,  # min_dmg, max_dmg, mastery
                                                                                0, 0)],  # effective and limit range
                                                           2, 1, 3,  # Armour and defence and base leadership
                                                           # Skills
                                                           [],
                                                           [["Florins", 5], ["Armament", 3], ["Food", 4]],
                                                           # Abilities
                                                           []))

    # 2 - Peasant bowmen
    LE_knight_lords_new_units.append(game_classes.Regiment("Peasant bowmen", 3,  # name, rank
                                                           "peasant_bowmen",  # img
                                                           "KL", 16, 14, 5,  # img_source, x_offset, y_offset, speed
                                                           16, 27,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           7, 0, 0, 5, 4,
                                                           ["ranged", "ranged infantry", "peasant"],
                                                           fill_with_creatures(5, 4, "Knight Lords", 1),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                1, 2, 1,  # min_dmg, max_dmg, mastery
                                                                                0, 0),  # effective and limit range
                                                            game_classes.Strike("Shooting", "Ranged",
                                                                                ["Ranged", "Physical"],
                                                                                1, 3, 3,  # min_dmg, max_dmg, mastery
                                                                                6, 12)],  # effective and limit range
                                                           0, 0, 3,  # Armour and defence and base leadership
                                                           # Skills
                                                           [],
                                                           [["Florins", 5], ["Armament", 4], ["Food", 4]],
                                                           # Abilities
                                                           []))

    # 3 - Crossbowmen
    LE_knight_lords_new_units.append(game_classes.Regiment("Crossbowmen", 5,  # name, rank
                                                           "crossbowmen",  # img
                                                           "KL", 17, 14, 6,  # img_source, x_offset, y_offset, speed
                                                           16, 29,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           8, 0, 0, 5, 4,
                                                           ["ranged", "ranged infantry", "men-at-arms"],
                                                           fill_with_creatures(5, 4, "Knight Lords", 2),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                1, 2, 2,  # min_dmg, max_dmg, mastery
                                                                                0, 0),  # effective and limit range
                                                            game_classes.Strike("Shooting", "Ranged",
                                                                                ["Ranged", "Physical"],
                                                                                2, 3, 6,  # min_dmg, max_dmg, mastery
                                                                                4, 10)],  # effective and limit range
                                                           2, 1, 4,  # Armour and defence and base leadership
                                                           # Skills
                                                           [skill_classes.Battle_Skill("Armour penetration 1",
                                                                                       "penetration",
                                                                                       1,
                                                                                       None,
                                                                                       None,
                                                                                       ["Ranged"])],
                                                           [["Florins", 10], ["Armament", 6], ["Food", 5]],
                                                           # Abilities
                                                           []))

    # 4 - Spear footmen
    LE_knight_lords_new_units.append(game_classes.Regiment("Spear footmen", 6,  # name, rank
                                                           "spear_footmen",  # img
                                                           "KL", 16, 12, 6,  # img_source, x_offset, y_offset, speed
                                                           16, 29,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           8, 0, 0, 5, 4,
                                                           ["melee", "melee infantry", "men-at-arms"],
                                                           fill_with_creatures(5, 4, "Knight Lords", 3),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                3, 5, 5,  # min_dmg, max_dmg, mastery
                                                                                0, 0)],  # effective and limit range
                                                           3, 2, 4,  # Armour and defence and base leadership
                                                           # Skills
                                                           [skill_classes.Battle_Skill("Charge defence",
                                                                                       "charge defence",
                                                                                       None,
                                                                                       "Ignore",
                                                                                       "Heavy and light charge defence",
                                                                                       ["Heavy charge",
                                                                                        "Light charge"]),
                                                            skill_classes.Battle_Skill("Long spears",
                                                                                       "increase damage in melee",
                                                                                       1.5,
                                                                                       "Multiplication",
                                                                                       None,
                                                                                       ["melee cavalry", "monster",
                                                                                        "gargantuan"])
                                                            ],
                                                           [["Florins", 10], ["Armament", 7], ["Food", 5]],
                                                           # Abilities
                                                           []))

    # 5 - Sword footmen
    LE_knight_lords_new_units.append(game_classes.Regiment("Sword footmen", 6,  # name, rank
                                                           "sword_footmen",  # img
                                                           "KL", 16, 14, 6,  # img_source, x_offset, y_offset, speed
                                                           20, 28,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           8, 0, 0, 5, 4,
                                                           ["melee", "melee infantry", "men-at-arms"],
                                                           fill_with_creatures(5, 4, "Knight Lords", 4),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                3, 6, 5,  # min_dmg, max_dmg, mastery
                                                                                0, 0)],  # effective and limit range
                                                           3, 2, 4,  # Armour and defence and base leadership
                                                           # Skills
                                                           [skill_classes.Battle_Skill("Big shields",
                                                                                       "missile protection",
                                                                                       2.0,
                                                                                       "Division",
                                                                                       None,
                                                                                       []),
                                                            skill_classes.Battle_Skill("Provides cover",
                                                                                       "exclusive aura",
                                                                                       1,
                                                                                       "Aura",
                                                                                       "Missile cover",
                                                                                       [])
                                                            ],
                                                           [["Florins", 10], ["Armament", 7], ["Food", 5]],
                                                           # Abilities
                                                           []))

    # 6 - Squires
    LE_knight_lords_new_units.append(game_classes.Regiment("Squires", 7,  # name, rank
                                                           "squire",  # img
                                                           "KL", 16, 14, 6,  # img_source, x_offset, y_offset, speed
                                                           19, 27,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           8, 0, 0, 5, 4,
                                                           ["melee", "melee infantry", "men-at-arms"],
                                                           fill_with_creatures(5, 4, "Knight Lords", 5),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                3, 6, 6,  # min_dmg, max_dmg, mastery
                                                                                0, 0)],  # effective and limit range
                                                           4, 2, 4,  # Armour and defence and base leadership
                                                           # Skills
                                                           [skill_classes.Battle_Skill("Big shields",
                                                                                       "missile protection",
                                                                                       2.0,
                                                                                       "Division",
                                                                                       None,
                                                                                       []),
                                                            skill_classes.Battle_Skill("Armour penetration 1",
                                                                                       "penetration",
                                                                                       1,
                                                                                       None,
                                                                                       None,
                                                                                       ["Melee"])
                                                            ],
                                                           [["Florins", 12], ["Armament", 8], ["Food", 5]],
                                                           # Abilities
                                                           []))

    # 7 - Knights
    LE_knight_lords_new_units.append(game_classes.Regiment("Knights", 10,  # name, rank
                                                           "knights",  # img
                                                           "KL", 10, 3, 9,  # img_source, x_offset, y_offset, speed
                                                           34, 39,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           16, 0, 0, 4, 2,
                                                           ["melee", "melee cavalry"],
                                                           fill_with_creatures(4, 2, "Knight Lords", 6),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                4, 7, 8,  # min_dmg, max_dmg, mastery
                                                                                0, 0)],  # effective and limit range
                                                           5, 4, 4,  # Armour and defence and leadership
                                                           # Skills
                                                           [skill_classes.Battle_Skill("Heavy charge",
                                                                                       "charge",
                                                                                       0.5,
                                                                                       "Increase damage",
                                                                                       "Heavy charge",
                                                                                       [])],
                                                           [["Florins", 20], ["Armament", 12], ["Food", 12]],
                                                           # Abilities
                                                           []))

    # 8 - Priests of Salvation
    LE_knight_lords_new_units.append(game_classes.Regiment("Priests of Salvation", 6,  # name, rank
                                                           "priests_of_salvation",  # img
                                                           "KL", 20, 15, 5,  # img_source, x_offset, y_offset, speed
                                                           11, 28,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           8, 16, 4, 4, 4,
                                                           ["caster"],
                                                           fill_with_creatures(4, 4, "Knight Lords", 7),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                1, 2, 0,  # min_dmg, max_dmg, mastery
                                                                                0, 0),  # effective and limit range
                                                            game_classes.Strike("Abilities", "Abilities",
                                                                                [],
                                                                                0, 0, 0,  # min_dmg, max_dmg, mastery
                                                                                0, 0)],  # effective and limit range
                                                           0, 0, 4,  # Armour and defence and leadership
                                                           # Skills
                                                           [skill_classes.Battle_Skill("Air shield",
                                                                                       "missile protection",
                                                                                       2.0,
                                                                                       "Division",
                                                                                       None,
                                                                                       [])],
                                                           [["Florins", 10], ["Ingredients", 3], ["Food", 5]],
                                                           # Abilities
                                                           ["Healing", "Bless"]))

    # 9 - Battle monks
    LE_knight_lords_new_units.append(game_classes.Regiment("Battle monks", 8,  # name, rank
                                                           "battle_monks",  # img
                                                           "KL", 12, 14, 6,  # img_source, x_offset, y_offset, speed
                                                           22, 28,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           8, 0, 3, 4, 4,
                                                           ["hybrid", "hybrid infantry"],
                                                           fill_with_creatures(4, 4, "Knight Lords", 8),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                3, 5, 4,  # min_dmg, max_dmg, mastery
                                                                                0, 0),  # effective and limit range
                                                            game_classes.Strike("Shooting", "Ranged",
                                                                                ["Ranged", "Physical"],
                                                                                2, 4, 5,  # min_dmg, max_dmg, mastery
                                                                                5, 9)],  # effective and limit range
                                                           2, 2, 4,  # Armour and defence and leadership
                                                           # Skills
                                                           [],
                                                           [["Florins", 12], ["Armament", 5], ["Ingredients", 2],
                                                            ["Food", 5]],
                                                           # Abilities
                                                           []))

    # 10 - Griffons
    LE_knight_lords_new_units.append(game_classes.Regiment("Griffons", 9,  # name, rank
                                                           "griffons",  # img
                                                           "KL", 2, 9, 10,  # img_source, x_offset, y_offset, speed
                                                           44, 29,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           20, 0, 0, 4, 2,
                                                           ["melee", "monster"],
                                                           fill_with_creatures(4, 2, "Knight Lords", 9),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                3, 8, 7,  # min_dmg, max_dmg, mastery
                                                                                0, 0)],  # effective and limit range
                                                           1, 5, 4,  # Armour and defence and leadership
                                                           # Skills
                                                           [skill_classes.Battle_Skill("Fly",
                                                                                       "Movement",
                                                                                       None,
                                                                                       None,
                                                                                       "Can fly",
                                                                                       []),
                                                            skill_classes.Battle_Skill("Cat reflex",
                                                                                       "Counterattack",
                                                                                       None,
                                                                                       None,
                                                                                       "Unlimited counterattacks",
                                                                                       [])
                                                            ],
                                                           [["Florins", 12], ["Food", 16]],
                                                           # Abilities
                                                           []))

    # 11 - Pegasus knights
    LE_knight_lords_new_units.append(game_classes.Regiment("Pegasus knights", 10,  # name, rank
                                                           "pegasus_knights",  # img
                                                           "KL", 4, 5, 8,  # img_source, x_offset, y_offset, speed
                                                           40, 37,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           16, 0, 0, 4, 2,
                                                           ["melee", "melee cavalry"],
                                                           fill_with_creatures(4, 2, "Knight Lords", 10),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                3, 7, 7,  # min_dmg, max_dmg, mastery
                                                                                0, 0),  # effective and limit range
                                                            game_classes.Strike("Hit and fly", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                3, 7, 7,  # min_dmg, max_dmg, mastery
                                                                                0, 5)  # effective and limit range
                                                            ],
                                                           2, 4, 4,  # Armour and defence and leadership
                                                           # Skills
                                                           [skill_classes.Battle_Skill("Fly",
                                                                                       "Movement",
                                                                                       None,
                                                                                       None,
                                                                                       "Can fly",
                                                                                       []),
                                                            skill_classes.Battle_Skill("Heavy charge",
                                                                                       "charge",
                                                                                       0.5,
                                                                                       "Increase damage",
                                                                                       "Heavy charge",
                                                                                       [])
                                                            ],
                                                           [["Florins", 24], ["Armament", 11], ["Food", 12]],
                                                           # Abilities
                                                           []))

    # 12 - Field ballistas
    LE_knight_lords_new_units.append(game_classes.Regiment("Field ballistas", 10,  # name, rank
                                                           "field_ballistas",  # img
                                                           "KL", 3, 7, 3,  # img_source, x_offset, y_offset, speed
                                                           42, 34,  # img width, img height
                                                           # Base HP, max mana reserve, base MP, number and rows
                                                           25, 0, 0, 2, 2,
                                                           ["ranged", "machines"],
                                                           fill_with_creatures(2, 2, "Knight Lords", 11),  # creatures
                                                           [game_classes.Strike("Melee assault", "Melee",
                                                                                ["Melee", "Physical"],
                                                                                2, 4, 2,  # min_dmg, max_dmg, mastery
                                                                                0, 0),  # effective and limit range
                                                            game_classes.Strike("Shooting", "Ranged",
                                                                                ["Ranged", "Physical"],
                                                                                4, 9, 5,  # min_dmg, max_dmg, mastery
                                                                                7, 13)],  # effective and limit range
                                                           3, 1, 4,  # Armour and defence and base leadership
                                                           # Skills
                                                           [skill_classes.Battle_Skill("Armour penetration 2",
                                                                                       "penetration",
                                                                                       2,
                                                                                       None,
                                                                                       None,
                                                                                       ["Ranged"])],
                                                           [["Florins", 70], ["Armament", 60], ["Food", 40]],
                                                           # Abilities
                                                           []))


def fill_with_creatures(number, rows, alignment, index):
    creature_list = []
    for i in range(1, rows*number + 1):  # Temporary for testing (-2)
        creature_list.append(copy.deepcopy(create_creature.LE_creatures_dict_by_alignment[alignment][index]))

    return list(creature_list)


create_neutrals()
create_KL()
