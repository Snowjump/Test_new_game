## Miracle battles

from Resources import game_classes

# Knight lords
knight_attributes = [  # 2 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "melee mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "magic power",
        1)])
     ],  # 3 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee cavalry",
        "melee mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee cavalry",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "knowledge",
        1)])
     ],  # 4 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "ranged infantry",
        "ranged mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "ranged infantry",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "armour",
        1)])
     ],  # 5 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "melee mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "magic power",
        1)])
     ],  # 6 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee cavalry",
        "melee mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee cavalry",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "knowledge",
        1)])
     ],  # 7  level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "ranged infantry",
        "ranged mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "ranged infantry",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee cavalry",
        "melee mastery",
        1)])
     ],  # 8  level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "melee mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "magic power",
        1)])
     ]]

priest_of_salvation = [  # 2 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee cavalry",
        "melee mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "knowledge",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "magic power",
        1)])
     ],  # 3 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "melee mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "knowledge",
        1)])
     ],  # 4 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "caster",
        "armour",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "magic power",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "knowledge",
        1)])
     ],  # 5 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "ranged infantry",
        "ranged mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "ranged infantry",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "magic power",
        1)])
     ],  # 6 level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee cavalry",
        "melee mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "knowledge",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "magic power",
        1)])
     ],  # 7  level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "caster",
        "melee mastery",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "caster",
        "defence",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "knowledge",
        1)])
     ],  # 8  level
    [game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee infantry",
        "armour",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "knowledge",
        1)]),
     game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "hero",
        "magic power",
        1)])
     ]]

basic_heroes_attributes = {"Knight": knight_attributes,
                           "Priest of Salvation": priest_of_salvation}
