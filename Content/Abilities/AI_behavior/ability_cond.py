## Among Myth and Wonder
## ability_cond

from Resources.Abilities import game_ability
from Resources.Abilities import AI_game_ability


def direct_order_cond(b, own_units, enemy_units):
    need_to_improve_morale = False
    for unit in own_units:
        if not unit.deserted:
            if float(unit.leadership) - unit.morale >= 0.3:
                need_to_improve_morale = True
                break

    need_to_improve_initiative = False
    for unit in own_units:
        if not unit.deserted:
            card = game_ability.find_queue_card(b, unit)
            if card.time_act > b.queue[0].time_act + 0.25:
                need_to_improve_initiative = True
                break

    if need_to_improve_morale or need_to_improve_initiative:
        return 5
    return 0


def rally_cond(b, own_units, enemy_units):
    number_of_units_in_need_to_improve_morale = 0
    for unit in own_units:
        if not unit.deserted:
            if float(unit.leadership) - unit.morale >= 0.5:
                number_of_units_in_need_to_improve_morale += 1

    if number_of_units_in_need_to_improve_morale >= 2:
        return 5 + (number_of_units_in_need_to_improve_morale - 1)
    return 0


def bless_cond(b, own_units, enemy_units):
    number_of_units_for_buffing = 0
    for unit in own_units:
        if not unit.deserted and unit.morale > 1.0:
            if not AI_game_ability.effect_is_present(unit, "Bless"):
                number_of_units_for_buffing += 1

    if number_of_units_for_buffing > 0:
        return 10
    return 0


def healing_cond(b, own_units, enemy_units):
    number_of_patients = 0
    for unit in own_units:
        if not unit.deserted:
            healing_pool = 0
            for creature in unit.crew:
                healing_pool += (unit.max_HP - creature.HP)
            if healing_pool >= 10:
                number_of_patients += 1

    if number_of_patients > 0:
        return 5 + (number_of_patients - 1)
    return 0


def inspiration_cond(b, own_units, enemy_units):
    priority = 0
    for unit in own_units:
        if not unit.deserted:
            if unit.morale < - 0.3:
                priority += 2
            elif unit.morale < unit.leadership - 1.0:
                priority += 1

    if priority > 0:
        return 35 + (priority - 1)
    return 0


def fire_arrows_cond(b, own_units, enemy_units):
    number_of_targets = 0
    for unit in enemy_units:
        if not unit.deserted:
            number_of_targets += 1

    if number_of_targets > 0:
        return 8
    return 0


def lightning_bolts_cond(b, own_units, enemy_units):
    number_of_targets = 0
    for unit in enemy_units:
        if not unit.deserted:
            number_of_targets += 1

    if number_of_targets > 0:
        return 8
    return 0


def hail_cond(b, own_units, enemy_units):
    number_of_targets = 0
    for unit in enemy_units:
        if not unit.deserted:
            number_of_targets += 1

    if number_of_targets > 0:
        return 8
    return 0


cond_cat = {"Direct order" : direct_order_cond,
            "Rally" : rally_cond,
            "Bless" : bless_cond,
            "Healing" : healing_cond,
            "Inspiration" : inspiration_cond,
            "Fire arrows" : fire_arrows_cond,
            "Lightning bolts" : lightning_bolts_cond,
            "Hail" : hail_cond}
