## Among Myth and Wonder
## ability_targets

import math


def direct_order_targets(magic_power):
    return 1


def bless_targets(magic_power):
    # print("bless_targets(): magic_power - " + str(magic_power))
    number = 1 + math.floor(magic_power / 4)
    return number


def haste_targets(magic_power):
    number = 1 + math.floor(magic_power / 3)
    return number


def healing_targets(magic_power):
    number = 1 + math.floor(magic_power / 3)
    return number


def divine_protection_targets(magic_power):
    number = 1 + math.floor(magic_power / 3)
    return number


def divine_strength_targets(magic_power):
    number = 1 + math.floor(magic_power / 4)
    return number


def inspiration_targets(magic_power):
    number = 1 + math.floor(magic_power / 4)
    return number


def missile_shielding_targets(magic_power):
    number = 1 + math.floor(magic_power / 4)
    return number


def fire_arrows_targets(magic_power):
    # print("fire_arrows_targets(): magic_power - " + str(magic_power))
    number = 1 + math.floor(magic_power / 4)
    return number


def lightning_bolts_targets(magic_power):
    number = 1 + math.floor(magic_power / 4)
    return number


def hail_targets(magic_power):
    number = 1 + math.floor(magic_power / 4)
    return number


ability_cat = {"Direct order": direct_order_targets,
               "Bless": bless_targets,
               "Haste": haste_targets,
               "Healing": healing_targets,
               "Divine protection": divine_protection_targets,
               "Divine strength": divine_strength_targets,
               "Inspiration": inspiration_targets,
               "Missile shielding": missile_shielding_targets,
               "Fire arrows": fire_arrows_targets,
               "Lightning bolts": lightning_bolts_targets,
               "Hail": hail_targets}
