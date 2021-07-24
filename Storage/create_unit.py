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
                                                       7, 5, 4,  # Base HP, number and rows
                                                       ["melee", "melee infantry"],
                                                       fill_with_creatures(5, 4, "Neutrals", 0),  # creatures
                                                       [game_classes.Strike("Melee assault", "Melee",
                                                                            ["Melee", "Physical"],
                                                                            3, 6, 4,  # min_dmg, max_dmg, mastery
                                                                            0, 0)],  # effective and limit range
                                                       2, 1, 3,  # Armor and defence and leadership
                                                       [skill_classes.Battle_Skill("Inflamed weapons",
                                                                                   "additional melee damage",
                                                                                   1,
                                                                                   "Separate damage",
                                                                                   None,
                                                                                   ["Magical", "Fire"])]))

    # 2 - Bandit archers
    LE_neutrals_new_units.append(game_classes.Regiment("Bandit archers", 4,  # name, rank
                                                       "bandit_archers",  # img
                                                       "neutrals", 17, 14, 6,  # img_source, x_offset, y_offset, speed
                                                       8, 5, 4,  # Base HP, number and rows
                                                       ["ranged", "ranger infantry"],
                                                       fill_with_creatures(5, 4, "Neutrals", 1),  # creatures
                                                       [game_classes.Strike("Melee assault", "Melee",
                                                                            ["Melee", "Physical"],
                                                                            1, 2, 2,  # min_dmg, max_dmg, mastery
                                                                            0, 0),  # effective and limit range
                                                        game_classes.Strike("Shooting", "Ranged",
                                                                            ["Ranged", "Physical"],
                                                                            1, 3, 4,  # min_dmg, max_dmg, mastery
                                                                            6, 12)],  # effective and limit range
                                                       1, 1, 4,  # Armor and defence and base leadership
                                                       []))  # Skills

    # 3 - Highway robbers
    LE_neutrals_new_units.append(game_classes.Regiment("Highway robbers", 6,  # name, rank
                                                       "highway_robbers",  # img
                                                       "neutrals", 16, 14, 6,  # img_source, x_offset, y_offset, speed
                                                       8, 5, 4,   # Base HP, number and rows
                                                       ["melee", "melee infantry"],
                                                       fill_with_creatures(5, 4, "Neutrals", 2),  # creatures
                                                       [game_classes.Strike("Melee assault", "Melee",
                                                                            ["Melee", "Physical"],
                                                                            3, 6, 5,  # min_dmg, max_dmg, mastery
                                                                            0, 0)],  # effective and limit range
                                                       2, 2, 4,  # Armor and defence and base leadership
                                                       []))  # Skills

    # 4 - Robber knights
    LE_neutrals_new_units.append(game_classes.Regiment("Robber knights", 12,  # name, rank
                                                       "robber_knights",  # img
                                                       "neutrals", 16, 14, 6,  # img_source, x_offset, y_offset, speed
                                                       16, 4, 2,   # Base HP, number and rows
                                                       ["melee", "melee cavalry"],
                                                       fill_with_creatures(4, 2, "Neutrals", 3),  # creatures
                                                       [game_classes.Strike("Melee assault", "Melee",
                                                                            ["Melee", "Physical"],
                                                                            3, 3, 7,  # min_dmg, max_dmg
                                                                            0, 0)],  # effective and limit range
                                                       2, 1, 4,  # Armor and defence and leadership
                                                       []))  # Skills


def fill_with_creatures(number, rows, alignment, index):
    creature_list = []
    for i in range(1, rows*number + 1 - 2):  # Temporary for testing
        creature_list.append(copy.deepcopy(create_creature.LE_creatures_dict_by_alignment[alignment][index]))

    return list(creature_list)


create_neutrals()
