## Among Myth and Wonder
## defence_action_funs

import math


def defence_action_effect(base_defence, hero):
    # Calculated when a regiment performs defence action
    final_defence = base_defence
    addition_bonus_list = []
    if hero:
        # Skills
        for s in hero.skills:
            for effect in s.effects:
                if effect.application == "Defence action bonus":
                    if effect.method == "addition":
                        addition_bonus_list.append(base_defence * effect.quantity)

    if addition_bonus_list:
        for addition in addition_bonus_list:
            final_defence += addition

    final_defence = int(math.ceil(final_defence))
    print("defence_action_effect: base_defence - " + str(base_defence) + " => "
          + "final_defence - " + str(final_defence))

    return final_defence


def missile_defence_action(base_missile_defence, hero):
    # Calculated when a regiment performs defence action
    final_defence = base_missile_defence
    addition_bonus_list = []
    if hero:
        # Skills
        for s in hero.skills:
            for effect in s.effects:
                if effect.application == "Defence action bonus":
                    if effect.method == "addition":
                        addition_bonus_list.append(effect.quantity)

    if addition_bonus_list:
        for addition in addition_bonus_list:
            final_defence += addition

    return final_defence


def defence_morale_restoration(unit, hero):
    addition_bonus_list = []
    if hero:
        # Skills
        for s in hero.skills:
            for effect in s.effects:
                if effect.application == "Defence morale restoration":
                    if effect.method == "addition":
                        addition_bonus_list.append(effect.quantity)

    if addition_bonus_list:
        for addition in addition_bonus_list:
            unit.morale += addition

    if unit.morale > unit.leadership:
        unit.morale = float(unit.leadership)
