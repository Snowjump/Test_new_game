## Among Myth and Wonder
## ability_desc_cat_hero

import math

from Content.Abilities import ability_targets


def direct_order_desc(b, magic_power, MP_bonus):
    description = ["Inspire one regiment", "Increase morale by 0.3", "Move initiative by 0.25"]

    return description


def rally_desc(b, magic_power, MP_bonus):
    description = ["Rally all ally regiments", "Increase morale by 0.5", "Hero initiative cost 1.5"]

    return description


def bless_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)
    description = ["Regiment will deal", "only maximum damage", "Duration " + str(1 + final_MP),
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


def haste_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)

    description = ["Grant a regiment +" + str(2 + math.floor(final_MP / 2)) + " speed", "Duration " + str(1 + final_MP),
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


def healing_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)
    description = ["Heal health of a regiment", str(4 + math.floor(final_MP / 3)) + " healing charges",
                   "By healing " + str(5 + math.floor(final_MP / 2)) + " HP per charge",
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


def divine_protection_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)
    description = ["Grant 1 regiment +" + str(2 + math.ceil(final_MP * 2 / 3)) + " defence",
                   "Duration " + str(1 + final_MP),
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


def divine_strength_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)
    description = ["Grant 1 regiment +" + str(2 + math.ceil(final_MP * 2 / 3)) + " melee mastery",
                   "Duration " + str(1 + final_MP),
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


def inspiration_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)
    description = ["Inspire 1 regiment", "Increase morale by" + str(1.0 + final_MP * 0.2),
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


def missile_shielding_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)
    description = ["Grant 1 regiment +" + str(2 + math.ceil(final_MP * 2 / 3)) + " defence",
                   "against ranged attack", "Duration " + str(1 + final_MP),
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


def fire_arrows_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)
    description = ["Strike 1 regiment", str(7 + math.floor(final_MP / 3)) + " fire arrow charges",
                   "By dealing " + str(3 + math.floor(final_MP * 2 / 3)) + "-" +
                   str(4 + math.floor(final_MP * 4 / 5)) + " damage per charge",
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


def lightning_bolts_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)
    description = ["Strike 1 regiment", str(4 + math.floor(final_MP / 4)) + " lightning bolt charges",
                   "By dealing " + str(2 + math.floor(final_MP * 2 / 5)) + "-" +
                   str(8 + math.floor(final_MP * 3 / 2)) + " damage per charge",
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


def hail_desc(b, magic_power, MP_bonus):
    final_MP = int(magic_power + MP_bonus)
    description = ["Strike 1 regiment with a hail of ", str(7 + math.floor(final_MP / 3)) + " icicle charges",
                   "By dealing " + str(2 + math.floor(final_MP * 3 / 5)) + "-" +
                   str(4 + math.floor(final_MP * 3 / 4)) + " damage per charge", "", "Freeze:",
                   "Apply -1 speed", "Duration 3",
                   "Number of targets is " + str(ability_targets.ability_cat[b.selected_ability](final_MP))]

    return description


script_cat = {"Direct order": direct_order_desc,
              "Rally": rally_desc,
              "Bless": bless_desc,
              "Haste": haste_desc,
              "Healing": healing_desc,
              "Divine protection": divine_protection_desc,
              "Divine strength": divine_strength_desc,
              "Inspiration": inspiration_desc,
              "Missile shielding": missile_shielding_desc,
              "Fire arrows": fire_arrows_desc,
              "Lightning bolts": lightning_bolts_desc,
              "Hail": hail_desc}
