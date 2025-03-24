## Among Myth and Wonder
## knight_lords_new_units

from Resources import skill_classes

from Resources.Game_Regiment.regiment_classes import *

from Storage import create_unit

from Storage.Knight_Lords import knight_lords_new_creatures

creature_dict = knight_lords_new_creatures.creature_creation_dict


def create_peasant_mob():
    new_unit = Regiment("Peasant mob", 3,  # name, rank
                        "peasant_mob",  # img
                        "KL", 20, 12, 5,
                        # img_source, x_offset, y_offset, speed
                        12, 30,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        7, 0, 0, 5, 4,
                        ["melee", "melee infantry", "peasant"],
                        create_unit.fill_with_creatures(5, 4, creature_dict,
                                                        "Peasant mob"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                2, 5, 4,  # min_dmg, max_dmg, mastery
                                0, 0)],  # effective and limit range
                        2, 1, 3,  # Armour and defence and base leadership
                        # Skills
                        [],
                        [["Florins", 5], ["Armament", 3], ["Food", 4]],
                        # Abilities
                        [])
    return new_unit


def create_peasant_bowmen():
    new_unit = Regiment("Peasant bowmen", 3,  # name, rank
                        "peasant_bowmen",  # img
                        "KL", 16, 14, 5,
                        # img_source, x_offset, y_offset, speed
                        16, 27,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        7, 0, 0, 5, 4,
                        ["ranged", "ranged infantry", "peasant"],
                        create_unit.fill_with_creatures(5, 4, creature_dict,
                                                        "Peasant bowmen"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                1, 2, 1,  # min_dmg, max_dmg, mastery
                                0, 0),  # effective and limit range
                            Strike(
                                "Shooting", "Ranged",
                                ["Ranged", "Physical"],
                                2, 4, 5,  # min_dmg, max_dmg, mastery
                                6, 12)],  # effective and limit range
                        0, 0, 3,  # Armour and defence and base leadership
                        # Skills
                        [],
                        [["Florins", 5], ["Armament", 4], ["Food", 4]],
                        # Abilities
                        [])
    return new_unit


def create_crossbowmen():
    new_unit = Regiment("Crossbowmen", 5,  # name, rank
                        "crossbowmen",  # img
                        "KL", 17, 14, 6,
                        # img_source, x_offset, y_offset, speed
                        16, 29,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        8, 0, 0, 5, 4,
                        ["ranged", "ranged infantry", "men-at-arms"],
                        create_unit.fill_with_creatures(5, 4, creature_dict,
                                                        "Crossbowmen"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                1, 2, 2,  # min_dmg, max_dmg, mastery
                                0, 0),  # effective and limit range
                            Strike(
                                "Shooting", "Ranged",
                                ["Ranged", "Physical"],
                                3, 5, 8,  # min_dmg, max_dmg, mastery
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
                        [])
    return new_unit


def create_spear_footmen():
    new_unit = Regiment("Spear footmen", 6,  # name, rank
                        "spear_footmen",  # img
                        "KL", 16, 12, 6,
                        # img_source, x_offset, y_offset, speed
                        16, 29,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        8, 0, 0, 5, 4,
                        ["melee", "melee infantry", "men-at-arms"],
                        create_unit.fill_with_creatures(5, 4, creature_dict,
                                                        "Spear footmen"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                3, 6, 5,  # min_dmg, max_dmg, mastery
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
                                                    ["melee cavalry",
                                                     "monster",
                                                     "gargantuan"])
                         ],
                        [["Florins", 10], ["Armament", 7], ["Food", 5]],
                        # Abilities
                        [])
    return new_unit


def create_sword_footmen():
    new_unit = Regiment("Sword footmen", 6,  # name, rank
                        "sword_footmen",  # img
                        "KL", 16, 14, 6,
                        # img_source, x_offset, y_offset, speed
                        20, 28,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        8, 0, 0, 5, 4,
                        ["melee", "melee infantry", "men-at-arms"],
                        create_unit.fill_with_creatures(5, 4, creature_dict,
                                                        "Sword footmen"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                3, 7, 5,  # min_dmg, max_dmg, mastery
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
                        [])
    return new_unit


def create_squires():
    new_unit = Regiment("Squires", 7,  # name, rank
                        "squires",  # img
                        "KL", 16, 14, 6,
                        # img_source, x_offset, y_offset, speed
                        19, 27,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        8, 0, 0, 5, 4,
                        ["melee", "melee infantry", "men-at-arms"],
                        create_unit.fill_with_creatures(5, 4, creature_dict,
                                                        "Squires"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                3, 7, 6,  # min_dmg, max_dmg, mastery
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
                        [])
    return new_unit


def create_knights():
    new_unit = Regiment("Knights", 10,  # name, rank
                        "knights",  # img
                        "KL", 10, 3, 9,
                        # img_source, x_offset, y_offset, speed
                        34, 39,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        16, 0, 0, 4, 2,
                        ["melee", "melee cavalry"],
                        create_unit.fill_with_creatures(4, 2, creature_dict,
                                                        "Knights"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                4, 8, 8,  # min_dmg, max_dmg, mastery
                                0, 0)],  # effective and limit range
                        5, 4, 4,  # Armour and defence and leadership
                        # Skills
                        [skill_classes.Battle_Skill("Heavy charge",
                                                    "charge",
                                                    0.5,
                                                    "Increase damage",
                                                    "Heavy charge",
                                                    [])],
                        [["Florins", 25], ["Armament", 20], ["Food", 12]],
                        # Abilities
                        [])
    return new_unit


def create_priests_of_salvation():
    new_unit = Regiment("Priests of Salvation", 6,  # name, rank
                        "priests_of_salvation",  # img
                        "KL", 20, 15, 5,
                        # img_source, x_offset, y_offset, speed
                        11, 28,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        8, 16, 4, 4, 4,
                        ["caster"],
                        create_unit.fill_with_creatures(4, 4, creature_dict,
                                                        "Priests of Salvation"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                1, 2, 0,  # min_dmg, max_dmg, mastery
                                0, 0),  # effective and limit range
                            Strike(
                                "Abilities", "Abilities",
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
                        ["Healing", "Bless"])
    return new_unit


def create_battle_monks():
    new_unit = Regiment("Battle monks", 8,  # name, rank
                        "battle_monks",  # img
                        "KL", 12, 14, 6,
                        # img_source, x_offset, y_offset, speed
                        22, 28,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        8, 0, 3, 4, 4,
                        ["hybrid", "hybrid infantry"],
                        create_unit.fill_with_creatures(4, 4, creature_dict,
                                                        "Battle monks"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                3, 5, 4,  # min_dmg, max_dmg, mastery
                                0, 0),  # effective and limit range
                            Strike(
                                "Shooting", "Ranged",
                                ["Ranged", "Physical"],
                                2, 4, 6,  # min_dmg, max_dmg, mastery
                                5, 9)],  # effective and limit range
                        2, 2, 4,  # Armour and defence and leadership
                        # Skills
                        [],
                        [["Florins", 12], ["Armament", 5], ["Ingredients", 2],
                         ["Food", 5]],
                        # Abilities
                        [])
    return new_unit


def create_griffons():
    new_unit = Regiment("Griffons", 9,  # name, rank
                        "griffons",  # img
                        "KL", 2, 9, 10,
                        # img_source, x_offset, y_offset, speed
                        44, 29,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        20, 0, 0, 4, 2,
                        ["melee", "monster"],
                        create_unit.fill_with_creatures(4, 2, creature_dict,
                                                        "Griffons"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
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
                        [])
    return new_unit


def create_pegasus_knights():
    new_unit = Regiment("Pegasus knights", 10,  # name, rank
                        "pegasus_knights",  # img
                        "KL", 4, 5, 8,  # img_source, x_offset, y_offset, speed
                        40, 37,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        16, 0, 0, 4, 2,
                        ["melee", "melee cavalry"],
                        create_unit.fill_with_creatures(4, 2, creature_dict,
                                                        "Pegasus knights"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                3, 7, 7,  # min_dmg, max_dmg, mastery
                                0, 0),  # effective and limit range
                            Strike(
                                "Hit and fly", "Melee",
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
                        [])
    return new_unit


def create_field_ballistas():
    new_unit = Regiment("Field ballistas", 10,  # name, rank
                        "field_ballistas",  # img
                        "KL", 3, 7, 3,  # img_source, x_offset, y_offset, speed
                        42, 34,  # img width, img height
                        # Base HP, max mana reserve, base MP, number and rows
                        25, 0, 0, 2, 2,
                        ["ranged", "machines"],
                        create_unit.fill_with_creatures(2, 2, creature_dict,
                                                        "Field ballistas"),
                        # creatures
                        [
                            Strike(
                                "Melee assault", "Melee",
                                ["Melee", "Physical"],
                                2, 4, 2,  # min_dmg, max_dmg, mastery
                                0, 0),  # effective and limit range
                            Strike(
                                "Shooting", "Ranged",
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
                        [])
    return new_unit


unit_creation_dict = {"Peasant mob": create_peasant_mob,
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
