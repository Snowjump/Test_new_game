## Miracle battles!
# Check here conditions for creating new quests

import random

from Resources import game_obj


def forest_law_quest_cond(quest_list, settlement):
    effect_name_list = ["Forest law restored", "Poachers in Royal forest"]
    if effect_block(effect_name_list, settlement):
        quest_list.append("Forest law")


def rule_of_monastic_life_cond(quest_list, settlement):
    # print("Conditions for: rule_of_monastic_life_cond")
    add_quest = False
    effect_name_list = ["Frivolous monks", "Disciplined monks"]
    if effect_block(effect_name_list, settlement):
        # print("No block")
        for plot in settlement.buildings:
            if plot.structure is not None:
                # print(plot.structure.name)
                if plot.status == "Built" and plot.structure.name == "Monastery":
                    add_quest = True
                    break

    if add_quest:
        quest_list.append("Rule of Monastic Life")


def grant_abbey_lands_cond(quest_list, settlement):
    # No conditions yet
    quest_list.append("Favor abbey's lands")


def monastery_school_cond(quest_list, settlement):
    add_quest = False
    effect_name_list = ["Monastery school"]
    if effect_block(effect_name_list, settlement):
        for plot in settlement.buildings:
            if plot.structure is not None:
                if plot.status == "Built" and plot.structure.name == "Monastery":
                    add_quest = True
                    break

    if add_quest:
        quest_list.append("Monastery school")


def grey_dragon_slayer_cond(quest_list, settlement):
    effect_name_list = ["Slayer of the Grey dragon", "Slay the Grey dragon"]
    if effect_block(effect_name_list, settlement):
        for Tile in settlement.control_zone:
            if game_obj.game_map[Tile].army_id is None:
                if game_obj.game_map[Tile].lot is None:
                    quest_list.append("Grey dragon slayer")
                    break


def dwarf_caravan_cond(quest_list, settlement):
    # No conditions yet
    quest_list.append("Dwarven caravan")


def desolated_defences_cond(quest_list, settlement):
    effect_name_list = ["Vassal awaits for stone", "Provided retinue to vassal", "Rejected request for stone",
                        "Failed to provide stone"]
    if effect_block(effect_name_list, settlement):
        quest_list.append("Desolated defences")


def effect_block(effect_name_list, settlement):
    result = True
    for local_effect in settlement.local_effects:
        # print("local_effect - " + local_effect.name)
        if local_effect.name in effect_name_list:
            result = False
            break

    # print("result - " + str(result))
    return result


def check_conditions(settlement):
    quest_list = []

    # forest_law_quest_cond(quest_list, settlement)
    # rule_of_monastic_life_cond(quest_list, settlement)
    # grant_abbey_lands_cond(quest_list, settlement)
    # monastery_school_cond(quest_list, settlement)
    grey_dragon_slayer_cond(quest_list, settlement)
    # dwarf_caravan_cond(quest_list, settlement)
    # desolated_defences_cond(quest_list, settlement)
    print("quest_list:")
    for text_line in quest_list:
        print(text_line)
    print("")

    return random.choice(quest_list)
