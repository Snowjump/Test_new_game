## Miracle battles

import math


def healing_desc(unit):
    description = ["Heal health of 1 regiment", str(len(unit.crew)) + " healing charges",
                   "By healing " + str(math.ceil(unit.magic_power * 2 / 3)) + " HP per charge"]

    return description


def bless_desc(unit):
    length = 1.0 + float(math.ceil(((unit.magic_power * len(unit.crew) / (unit.rows * unit.number)) * 100)) / 100)
    description = ["Regiment will deal", "only maximum damage",
                   "Duration " + str(length)]

    return description


script_cat = {"Healing" : healing_desc,
              "Bless" : bless_desc}
