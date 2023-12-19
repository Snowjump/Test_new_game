## Among Myth and Wonder

import math
import random

from Resources import game_obj
from Resources import game_classes
from Resources import effect_classes
from Content import ability_catalog


def find_single_ally(b, TileNum):
    unit = None
    for army in game_obj.game_armies:
        if army.army_id == b.queue[0].army_id:
            unit = army.units[b.battle_map[TileNum].unit_index]
            break

    return unit


def add_or_prolong_effect(unit, b, effect_name, duration):
    add_effect = True
    if len(unit.effects) > 0:
        for effect in unit.effects:
            if effect.name == effect_name:

                for eff_card in b.queue:
                    if eff_card.position == unit.position and eff_card.obj_type == "Effect" \
                            and eff_card.title == effect_name:
                        if eff_card.time_act <= float(b.queue[0].time_act + duration):
                            add_effect = False
                        else:
                            b.queue.remove(eff_card)
                        break

                if add_effect:
                    unit.effects.remove(effect)

                break

    return add_effect


# Scripts
def bless_spell(b, TileNum, hero, caster):
    initiative = 1.0
    unit = find_single_ally(b, TileNum)

    MP_bonus = 0
    MP_addition_list = []
    initiative_reduction = []
    mana_bonus = 0
    mana_cost_subtraction = []

    artifact_bonus("Bless", "Devine magic", hero, MP_addition_list, initiative_reduction, mana_cost_subtraction, caster)

    MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                        initiative, mana_cost_subtraction, mana_bonus)

    final_MP = int(caster.magic_power + MP_bonus)
    length = 1.0 + float(math.ceil(((final_MP * len(unit.crew) / (unit.rows * unit.number)) * 100)) / 100)
    print("caster.magic_power - " + str(caster.magic_power) + ", final_MP - " + str(final_MP))

    duration = float(1.0 + length)
    info_card = None
    for card in b.queue:
        if card.position == unit.position and card.obj_type == "Regiment":
            info_card = card
            break

    add_effect = add_or_prolong_effect(unit, b, "Bless", duration)

    if add_effect:
        b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + duration), "Effect", info_card.army_id,
                                               info_card.owner, info_card.number, info_card.position,
                                               "Icons", "eff", info_card.f_color, info_card.s_color,
                                               0, 0, 4, 14, "Bless"))

        unit.effects.append(effect_classes.Battle_Effect("Bless", False,
                                                         float(b.queue[0].time_act),
                                                         float(b.queue[0].time_act + duration),
                                                         [effect_classes.Buff("Damage", None,
                                                                              None, "Bless")]))

    print(str(caster.name) + ": b.selected_ability - " + str(b.selected_ability))
    caster.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
    caster.initiative = float(initiative)


def healing_spell(b, TileNum, hero, caster):
    initiative = 1.0
    unit = find_single_ally(b, TileNum)

    MP_bonus = 0
    MP_addition_list = []
    initiative_reduction = []
    mana_bonus = 0
    mana_cost_subtraction = []

    artifact_bonus("Healing", "Devine magic", hero, MP_addition_list, initiative_reduction, mana_cost_subtraction,
                   caster)

    MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                        initiative, mana_cost_subtraction, mana_bonus)

    final_MP = int(caster.magic_power + MP_bonus)

    charges = int(len(caster.crew))
    heal_HP = int(math.ceil(final_MP * 2 / 3))

    while charges > 0:
        index_list = []
        ind = 0
        for creature in unit.crew:
            if creature.HP < unit.max_HP:
                index_list.append(int(ind))

            ind += 1

        if len(index_list) > 0:
            final_index = random.choice(index_list)
            if unit.crew[final_index].HP + heal_HP > unit.max_HP:
                unit.crew[final_index].HP = int(unit.max_HP)
            else:
                unit.crew[final_index].HP += int(heal_HP)

            print(unit.crew[final_index].name + " HP - " + str(unit.crew[final_index].HP))

        charges -= 1

    print("mana_cost " + str(ability_catalog.ability_cat[b.selected_ability].mana_cost))
    print("mana_bonus " + str(mana_bonus))
    caster.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
    print("caster.initiative - " + str(caster.initiative) + ", time_act - " + str(b.queue[0].time_act) +
          ", initiative - " + str(initiative))
    caster.initiative = float(initiative)


def artifact_bonus(spell_name, school, hero, MP_addition_list, initiative_reduction, mana_cost_subtraction, caster):

    if hero is not None:
        if len(hero.inventory) > 0:
            for artifact in hero.inventory:
                for effect in artifact.effects:
                    allowed = True
                    if len(effect.other_tags) > 0:
                        allowed = False
                        for tag in caster.reg_tags:
                            if tag in effect.other_tags:
                                allowed = True

                    # print("Allowed - " + str(allowed))
                    if allowed:
                        # Magic power bonus from artifacts calculated in the beginning of the fight now and allocated to
                        # regiment.magic_power
                        # if effect.application == "Bonus Magic Power":
                        #     if effect.method == "addition":
                        #         MP_addition_list.append(int(effect.quantity))
                        if effect.application == "Ability bonus initiative":
                            if effect.method == "subtraction":
                                initiative_reduction.append(effect.quantity)
                        elif effect.application == "Ability mana cost":
                            if effect.method == "subtraction":
                                # print("Ability mana cost subtraction")
                                mana_cost_subtraction.append(effect.quantity)
                            elif effect.method == "addition":
                                mana_cost_subtraction.append(effect.quantity * -1)


def allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction, initiative, mana_cost_subtraction, mana_bonus):
    if len(MP_addition_list) > 0:
        for addition in MP_addition_list:
            MP_bonus += addition

    if len(initiative_reduction) > 0:
        for reduction in initiative_reduction:
            initiative = float(1 - reduction)

    if len(mana_cost_subtraction) > 0:
        for subtraction in mana_cost_subtraction:
            mana_bonus -= subtraction
            print("mana_bonus " + str(mana_bonus))

    return MP_bonus, initiative, mana_bonus


script_cat = {"Bless" : bless_spell,
              "Healing" : healing_spell}
