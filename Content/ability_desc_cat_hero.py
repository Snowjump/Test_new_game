## Miracle battles

import math


def direct_order_desc(hero):
    description = ["Inspire 1 regiment", "Increase morale by 0.3", "Move initiative by 0.25"]

    return description


def bless_desc(hero):
    description = ["Regiment will deal", "only maximum damage",
                   "Duration " + str(1 + hero.magic_power)]

    return description


def haste_desc(hero):
    additional_line = ""
    MP_bonus = 0
    MP_addition_list = []
    for skill in hero.skills:
        for effect in skill.effects:
            if "Haste" in effect.other_tags:
                if effect.application == "Ability bonus Magic Power":
                    if effect.method == "addition":
                        MP_addition_list.append(int(effect.quantity))
                elif effect.application == "Ability bonus initiative":
                    if effect.method == "reduction":
                        additional_line = "Initiative reduced by half"

    if len(MP_addition_list) > 0:
        for addition in MP_addition_list:
            MP_bonus += addition

    final_MP = int(hero.magic_power + MP_bonus)

    description = ["Grant 1 regiment +" + str(2 + math.floor(final_MP / 2)) + " speed",
                   "Duration " + str(1 + final_MP), additional_line]

    return description


def healing_desc(hero):
    description = ["Heal health of 1 regiment", str(4 + math.floor(hero.magic_power / 3)) + " healing charges",
                   "By healing " + str(5 + math.floor(hero.magic_power / 2)) + " HP per charge"]

    return description


def divine_protection_desc(hero):
    description = ["Grant 1 regiment +" + str(2 + math.ceil(hero.magic_power * 2 / 3)) + " defence",
                   "Duration " + str(1 + hero.magic_power)]

    return description


def divine_strength_desc(hero):
    description = ["Grant 1 regiment +" + str(2 + math.ceil(hero.magic_power * 2 / 3)) + " melee mastery",
                   "Duration " + str(1 + hero.magic_power)]

    return description


def inspiration_desc(hero):
    description = ["Inspire 1 regiment",
                   "Increase morale by" + str(1.0 + hero.magic_power * 0.2)]

    return description


def missile_shielding_desc(hero):
    description = ["Grant 1 regiment +" + str(2 + math.ceil(hero.magic_power * 2 / 3)) + " defence",
                   "against ranged attack",
                   "Duration " + str(1 + hero.magic_power)]

    return description


def fire_arrows_desc(hero):
    description = ["Strike 1 regiment", str(7 + math.floor(hero.magic_power / 3)) + " fire arrow charges",
                   "By dealing " + str(3 + math.floor(hero.magic_power * 2 / 3)) + "-" +
                   str(4 + math.floor(hero.magic_power * 4 / 5)) + " damage per charge"]

    return description


def lightning_bolts_desc(hero):
    description = ["Strike 1 regiment", str(4 + math.floor(hero.magic_power / 4)) + " lightning bolt charges",
                   "By dealing " + str(2 + math.floor(hero.magic_power * 2 / 5)) + "-" +
                   str(8 + math.floor(hero.magic_power * 3 / 2)) + " damage per charge"]

    return description


def hail_desc(hero):
    description = ["Strike 1 regiment with a hail of ", str(7 + math.floor(hero.magic_power / 3)) + " icicle charges",
                   "By dealing " + str(2 + math.floor(hero.magic_power * 3 / 5)) + "-" +
                   str(4 + math.floor(hero.magic_power * 3 / 4)) + " damage per charge",
                   "", "Freeze:",
                   "Apply -1 speed",
                   "Duration 3"]

    return description


script_cat = {"Direct order" : direct_order_desc,
              "Bless" : bless_desc,
              "Haste" : haste_desc,
              "Healing" : healing_desc,
              "Divine protection" : divine_protection_desc,
              "Divine strength" : divine_strength_desc,
              "Inspiration" : inspiration_desc,
              "Missile shielding" : missile_shielding_desc,
              "Fire arrows" : fire_arrows_desc,
              "Lightning bolts" : lightning_bolts_desc,
              "Hail" : hail_desc}
