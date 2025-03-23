## Among Myth and Wonder
## AI_select_target

from Resources.Abilities import game_ability
from Resources.Abilities import AI_game_ability
from Resources.Abilities import AI_ability_target_pool_class


def direct_order_select_target(b, units):
    # Idea is for AI hero to pick only regiments in need to restore their morale
    # If no such regiments is found, then some that could use a boost of its initiative
    list_of_positions = []
    for unit in units:
        if not unit.deserted:
            if float(unit.leadership) - unit.morale >= 0.3:
                list_of_positions.append((unit.position[0], unit.position[1]))

    if not list_of_positions:
        for unit in units:
            if not unit.deserted:
                card = game_ability.find_queue_card(b, unit)
                if card.time_act > b.queue[0].time_act + 0.25:
                    list_of_positions.append((unit.position[0], unit.position[1]))

    return AI_ability_target_pool_class.AI_Target_Pool(list_of_positions)


def bless_select_target(b, units):
    list_of_positions = []
    for unit in units:
        if not unit.deserted and unit.morale > 1.0:
            if not AI_game_ability.effect_is_present(unit, "Bless"):
                list_of_positions.append((unit.position[0], unit.position[1]))

    return AI_ability_target_pool_class.AI_Target_Pool(list_of_positions)


def healing_select_target(b, units):
    priority_1 = []
    priority_2 = []
    for unit in units:
        if not unit.deserted:
            healing_pool = 0
            for creature in unit.crew:
                healing_pool += (unit.max_HP - creature.HP)
            if healing_pool >= 10:
                priority_1.append((unit.position[0], unit.position[1]))
            elif healing_pool > 0:
                priority_2.append((unit.position[0], unit.position[1]))
            # print("healing " + str(unit.position) + " " + unit.name + "; healing_pool " + str(healing_pool))

    return AI_ability_target_pool_class.AI_Target_Pool(priority_1, priority_2)


def inspiration_target(b, units):
    priority_1 = []
    priority_2 = []
    priority_3 = []
    for unit in units:
        if not unit.deserted:
            if unit.morale < - 0.3:
                priority_1.append((unit.position[0], unit.position[1]))
            elif unit.morale < unit.leadership - 1.0:
                priority_2.append((unit.position[0], unit.position[1]))
            elif unit.morale < unit.leadership:
                priority_3.append((unit.position[0], unit.position[1]))

    return AI_ability_target_pool_class.AI_Target_Pool(priority_1, priority_2, priority_3)


def fire_arrows_select_target(b, units):
    list_of_positions = []
    for unit in units:
        if not unit.deserted:
            list_of_positions.append((unit.position[0], unit.position[1]))

    return AI_ability_target_pool_class.AI_Target_Pool(list_of_positions)


def lightning_bolts_select_target(b, units):
    list_of_positions = []
    for unit in units:
        if not unit.deserted:
            list_of_positions.append((unit.position[0], unit.position[1]))

    return AI_ability_target_pool_class.AI_Target_Pool(list_of_positions)


def hail_select_target(b, units):
    list_of_positions = []
    for unit in units:
        if not unit.deserted:
            list_of_positions.append((unit.position[0], unit.position[1]))

    return AI_ability_target_pool_class.AI_Target_Pool(list_of_positions)


ability_cat = {"Direct order": direct_order_select_target,
               "Bless": bless_select_target,
               "Healing": healing_select_target,
               "Inspiration" : inspiration_target,
               "Fire arrows": fire_arrows_select_target,
               "Lightning bolts": lightning_bolts_select_target,
               "Hail": hail_select_target}
