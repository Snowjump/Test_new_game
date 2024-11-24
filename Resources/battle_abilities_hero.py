## Among Myth and Wonder
## battle_abilities_hero

import math
import random
# import numpy

from Resources import game_obj
from Resources import game_classes
from Resources import effect_classes
from Resources import game_battle
from Resources import update_gf_battle
from Resources import common_selects

from Content import ability_catalog


def find_single_ally(b, TileNum, acting_army):
    unit = None  # Will stay None if player clicked on opponent's regiment
    if b.battle_map[TileNum].army_id == acting_army.army_id:
        unit = acting_army.units[b.battle_map[TileNum].unit_index]

    return unit


def find_single_enemy(b, TileNum, opponent_army):
    unit = None  # Will stay None if player clicked on one of the own regiments
    if b.battle_map[TileNum].army_id == opponent_army.army_id:
        unit = opponent_army.units[b.battle_map[TileNum].unit_index]

    return unit


def add_or_prolong_effect(unit, b, effect_name, duration):
    add_effect = True
    if len(unit.effects) > 0:
        for effect in unit.effects:
            if effect.name == effect_name:

                for eff_card in b.queue:
                    if eff_card.position == unit.position and eff_card.obj_type == "Effect"\
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
def increase_morale(b, TileNum, acting_army, opponent_army):
    unit = find_single_ally(b, TileNum, acting_army)

    if unit:
        print("Before: " + unit.name + " unit.morale - " + str(unit.morale))
        if unit.morale + 0.3 > unit.leadership:
            unit.morale = float(unit.leadership)
        else:
            unit.morale = float(math.ceil((unit.morale + 0.3) * 100) / 100)
        print("After: " + unit.name + " unit.morale - " + str(unit.morale))
        return True
    else:
        print("increase_morale() - Selected wrong unit")
        return False


def advance_initiative(b, TileNum, acting_army, opponent_army):
    initiative = 1.0
    MP_bonus = 0
    MP_addition_list = []
    initiative_reduction = []
    mana_bonus = 0
    mana_cost_subtraction = []

    artifact_bonus("Direct order", "Tactics", acting_army.hero, MP_addition_list, initiative_reduction,
                   mana_cost_subtraction)

    MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                        initiative, mana_cost_subtraction, mana_bonus)

    UnitCard = None
    for Card in b.queue:
        if Card.number == b.battle_map[TileNum].unit_index and Card.army_id == b.battle_map[TileNum].army_id:
            UnitCard = Card
            break

    index0 = int(b.queue.index(UnitCard))
    lowest_time = b.queue[0].time_act
    found_new_place = False
    while not found_new_place:
        if b.queue[index0 - 1].time_act == UnitCard.time_act - 0.25:
            UnitCard.time_act -= 0.25
            found_new_place = True
        elif b.queue[index0 - 1].time_act > UnitCard.time_act - 0.25:
            if b.queue[index0 - 1].time_act == lowest_time:
                UnitCard.time_act = float(lowest_time)
                found_new_place = True
            else:
                index0 -= 1
        else:  # b.queue[index0 - 1].time_act < UnitCard.time_act - 0.25:
            UnitCard.time_act -= 0.25
            found_new_place = True

    print(UnitCard.owner + ": index0 - " + str(index0))
    print(acting_army.units[UnitCard.number].name)
    b.queue.insert(index0, b.queue.pop(b.queue.index(UnitCard)))
    print("Final: initiative - " + str(initiative))
    acting_army.hero.initiative = float(initiative)
    return True


def bless_spell(b, TileNum, acting_army, opponent_army):
    initiative = 1.0
    unit = find_single_ally(b, TileNum, acting_army)

    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        artifact_bonus("Bless", "Devine magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)

        duration = float(1.0 + final_MP)
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
                                                   4, 14, 20, 20, "Bless"))

            unit.effects.append(effect_classes.Battle_Effect("Bless", False,
                                                             float(b.queue[0].time_act),
                                                             float(b.queue[0].time_act + duration),
                                                             [effect_classes.Buff("Damage", None,
                                                                                  None, "Bless")]))

        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        acting_army.hero.initiative = float(initiative)
        return True
    else:
        print("bless_spell() - Selected wrong unit")
        return False


def haste_spell(b, TileNum, acting_army, opponent_army):
    initiative = 1.0
    unit = find_single_ally(b, TileNum, acting_army)

    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        for skill in acting_army.hero.skills:
            for effect in skill.effects:
                if "Haste" in effect.other_tags:
                    if effect.application == "Ability bonus Magic Power":
                        if effect.method == "addition":
                            MP_addition_list.append(int(effect.quantity))
                    elif effect.application == "Ability bonus initiative":
                        if effect.method == "subtraction":
                            initiative_reduction.append(effect.quantity)

        artifact_bonus("Haste", "Devine magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)

        duration = float(1.0 + final_MP)

        info_card = None
        for card in b.queue:
            if card.position == unit.position and card.obj_type == "Regiment":
                info_card = card
                break

        add_effect = add_or_prolong_effect(unit, b, "Haste", duration)

        if add_effect:

            b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + duration), "Effect", info_card.army_id,
                                                   info_card.owner, info_card.number, info_card.position,
                                                   "Icons", "eff", info_card.f_color, info_card.s_color,
                                                   4, 14, 20, 20, "Haste"))

            unit.effects.append(effect_classes.Battle_Effect("Haste", False,
                                                             float(b.queue[0].time_act),
                                                             float(b.queue[0].time_act + duration),
                                                             [effect_classes.Buff("Speed", 2 + math.floor(final_MP / 2),
                                                                                  "addition", None)]))

        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        acting_army.hero.initiative = float(initiative)
        return True
    else:
        print("haste_spell() - Selected wrong unit")
        return False


def healing_spell(b, TileNum, acting_army, opponent_army):
    initiative = 1.0
    unit = find_single_ally(b, TileNum, acting_army)
    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        artifact_bonus("Healing", "Devine magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)

        charges = 4 + math.floor(final_MP / 3)
        heal_HP = 5 + math.floor(final_MP / 2)

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
        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        print("hero.initiative - " + str(acting_army.hero.initiative) + ", time_act - " + str(b.queue[0].time_act) +
              ", initiative - " + str(initiative))
        acting_army.hero.initiative = float(initiative)
        return True
    else:
        print("healing_spell() - Selected wrong unit")
        return False


def devine_protection_spell(b, TileNum, acting_army, opponent_army):
    initiative = 1.0
    unit = find_single_ally(b, TileNum, acting_army)
    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        artifact_bonus("Devine protection", "Devine magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)

        duration = float(1.0 + final_MP)

        info_card = None
        for card in b.queue:
            if card.position == unit.position and card.obj_type == "Regiment":
                info_card = card
                break

        add_effect = add_or_prolong_effect(unit, b, "Devine protection", duration)

        if add_effect:
            b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + duration), "Effect", info_card.army_id,
                                                   info_card.owner, info_card.number, info_card.position,
                                                   "Icons", "eff", info_card.f_color, info_card.s_color,
                                                   4, 14, 20, 20, "Devine protection"))

            unit.effects.append(effect_classes.Battle_Effect("Devine protection", False,
                                                             float(b.queue[0].time_act),
                                                             float(b.queue[0].time_act + duration),
                                                             [effect_classes.Buff("Defence", 2 + math.ceil(final_MP * 2 / 3),
                                                                                  "addition", None)]))

        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        acting_army.hero.initiative = float(initiative)
        return True
    else:
        print("devine_protection_spell() - Selected wrong unit")
        return False


def devine_strength_spell(b, TileNum, acting_army, opponent_army):
    initiative = 1.0
    unit = find_single_ally(b, TileNum, acting_army)
    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        artifact_bonus("Devine strength", "Devine magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)

        duration = float(1.0 + final_MP)

        info_card = None
        for card in b.queue:
            if card.position == unit.position and card.obj_type == "Regiment":
                info_card = card
                break

        add_effect = add_or_prolong_effect(unit, b, "Devine strength", duration)

        if add_effect:
            b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + duration), "Effect", info_card.army_id,
                                                   info_card.owner, info_card.number, info_card.position,
                                                   "Icons", "eff", info_card.f_color, info_card.s_color,
                                                   4, 14, 20, 20, "Devine strength"))

            unit.effects.append(effect_classes.Battle_Effect("Devine strength", False,
                                                             float(b.queue[0].time_act),
                                                             float(b.queue[0].time_act + duration),
                                                             [effect_classes.Buff("Melee mastery",
                                                                                  2 + math.ceil(final_MP * 2 / 3),
                                                                                  "addition", None)]))

        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        acting_army.hero.initiative = float(initiative)
        return True
    else:
        print("devine_strength_spell() - Selected wrong unit")
        return False


def inspiration_spell(b, TileNum, acting_army, opponent_army):
    initiative = 1.0
    unit = find_single_ally(b, TileNum, acting_army)
    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        artifact_bonus("Inspiration", "Devine magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)
        morale_improvement = 1.0 + final_MP * 0.2
        if unit.morale + morale_improvement > unit.leadership:
            unit.morale = float(unit.leadership)
        else:
            unit.morale += float(morale_improvement)

        print("mana_cost " + str(ability_catalog.ability_cat[b.selected_ability].mana_cost))
        print("mana_bonus " + str(mana_bonus))
        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        print("hero.initiative - " + str(acting_army.hero.initiative) + ", time_act - " + str(b.queue[0].time_act) +
              ", initiative - " + str(initiative))
        acting_army.hero.initiative = float(initiative)
        return True
    else:
        print("inspiration_spell() - Selected wrong unit")
        return False


def missile_shielding_spell(b, TileNum, acting_army, opponent_army):
    initiative = 1.0
    unit = find_single_ally(b, TileNum, acting_army)
    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        artifact_bonus("Missile shielding", "Devine magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)

        duration = float(1.0 + final_MP)

        info_card = None
        for card in b.queue:
            if card.position == unit.position and card.obj_type == "Regiment":
                info_card = card
                break

        add_effect = add_or_prolong_effect(unit, b, "Missile shielding", duration)
        print("add_effect - " + str(add_effect))
        if add_effect:
            b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + duration), "Effect", info_card.army_id,
                                                   info_card.owner, info_card.number, info_card.position,
                                                   "Icons", "eff", info_card.f_color, info_card.s_color,
                                                   4, 14, 20, 20, "Missile shielding"))

            unit.effects.append(effect_classes.Battle_Effect("Missile shielding", False,
                                                             float(b.queue[0].time_act),
                                                             float(b.queue[0].time_act + duration),
                                                             [effect_classes.Buff("Missile defence",
                                                                                  2 + math.ceil(final_MP * 2 / 3),
                                                                                  "addition", None)]))

        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        acting_army.hero.initiative = float(initiative)
        return True
    else:
        print("missile_shielding_spell() - Selected wrong unit")
        return False


def fire_arrows_spell(b, TileNum, acting_army, opponent_army):
    # Reset damage counter
    b.dealt_damage = 0
    b.killed_creatures = 0

    initiative = 1.0
    unit = find_single_enemy(b, TileNum, opponent_army)
    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        artifact_bonus("Fire arrows", "Elemental magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)
        final_MP = magic_resistance(b, unit, TileNum, final_MP)
        print("hero.magic_power - " + str(acting_army.hero.magic_power) + ", final_MP - " + str(final_MP))

        charges = 7 + math.floor(final_MP / 3)
        damage = random.randint(3 + math.floor(final_MP * 2 / 3), 4 + math.floor(final_MP * 4 / 5))

        # Animation coordinates for flame effect
        # n_samples = charges
        # r = 52
        # theta = numpy.linspace(0, 2 * numpy.pi, n_samples)
        # a, b = r * numpy.cos(theta), r * numpy.sin(theta)
        #
        # t = numpy.random.uniform(0, 1, size=n_samples)
        # u = numpy.random.uniform(0, 1, size=n_samples)
        #
        # x = r * numpy.sqrt(t) * numpy.cos(2 * numpy.pi * u)
        # y = r * numpy.sqrt(t) * numpy.sin(2 * numpy.pi * u)
        #
        # print("x " + str(x))
        # print("y " + str(y))

        if len(unit.crew) > 0:
            while charges > 0:
                target = random.randint(0, len(unit.crew) - 1)
                unit.crew[target].HP -= damage

                if unit.crew[target].HP <= 0:
                    b.dealt_damage += (damage + unit.crew[target].HP)
                    b.killed_creatures += 1
                    unit.crew[target].HP = 0
                else:
                    b.dealt_damage += damage

                r = 49
                t = random.random()
                u = random.random()
                x = math.ceil(r * math.sqrt(t) * math.cos(2 * math.pi * u))
                y = math.ceil(r * math.sqrt(t) * math.sin(2 * math.pi * u))
                print(x, y)
                b.positions_list.append([x - 8, y - 8])

                charges -= 1

            perished_creatures(b, unit)

        print("mana_cost " + str(ability_catalog.ability_cat[b.selected_ability].mana_cost))
        print("mana_bonus " + str(mana_bonus))
        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        print("hero.initiative - " + str(acting_army.hero.initiative) + ", time_act - " + str(b.queue[0].time_act) +
              ", initiative - " + str(initiative))
        acting_army.hero.initiative = float(initiative)

        # Update visuals
        sprites_list = ["Battle_effects/flame_a_01", "Battle_effects/flame_a_02",
                        "Battle_effects/flame_a_03", "Battle_effects/flame_a_04"]
        update_gf_battle.add_battle_effects_sprites(sprites_list)
        return True
    else:
        print("fire_arrows_spell() - Selected wrong unit")
        return False


def lightning_bolts_spell(b, TileNum, acting_army, opponent_army):
    # Reset damage counter
    b.dealt_damage = 0
    b.killed_creatures = 0

    initiative = 1.0
    unit = find_single_enemy(b, TileNum, opponent_army)
    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        artifact_bonus("Lightning bolts", "Elemental magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)
        final_MP = magic_resistance(b, unit, TileNum, final_MP)

        charges = 4 + math.floor(final_MP / 4)
        damage = random.randint(2 + math.floor(final_MP * 2 / 5), 8 + math.floor(final_MP * 3 / 2))

        if len(unit.crew) > 0:
            while charges > 0:
                target = random.randint(0, len(unit.crew) - 1)
                unit.crew[target].HP -= damage

                if unit.crew[target].HP <= 0:
                    b.dealt_damage += (damage + unit.crew[target].HP)
                    b.killed_creatures += 1
                    unit.crew[target].HP = 0
                else:
                    b.dealt_damage += damage

                r = 49
                t = random.random()
                u = random.random()
                x = math.ceil(r * math.sqrt(t) * math.cos(2 * math.pi * u))
                y = math.ceil(r * math.sqrt(t) * math.sin(2 * math.pi * u))
                print(x, y)
                b.positions_list.append([x - 10, y - 38])

                charges -= 1

            perished_creatures(b, unit)

        print("mana_cost " + str(ability_catalog.ability_cat[b.selected_ability].mana_cost))
        print("mana_bonus " + str(mana_bonus))
        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        print("hero.initiative - " + str(acting_army.hero.initiative) + ", time_act - " + str(b.queue[0].time_act) +
              ", initiative - " + str(initiative))
        acting_army.hero.initiative = float(initiative)

        # Update visuals
        sprites_list = ["Battle_effects/lightning_bolt_a_01", "Battle_effects/lightning_bolt_a_02",
                        "Battle_effects/lightning_bolt_a_03", "Battle_effects/lightning_bolt_a_04"]
        update_gf_battle.add_battle_effects_sprites(sprites_list)
        return True
    else:
        print("lightning_bolts_spell() - Selected wrong unit")
        return False


def hail_spell(b, TileNum, acting_army, opponent_army):
    # Reset damage counter
    b.dealt_damage = 0
    b.killed_creatures = 0

    initiative = 1.0
    unit = find_single_enemy(b, TileNum, opponent_army)
    if unit:
        MP_bonus = 0
        MP_addition_list = []
        initiative_reduction = []
        mana_bonus = 0
        mana_cost_subtraction = []

        artifact_bonus("Hail", "Elemental magic", acting_army.hero, MP_addition_list, initiative_reduction,
                       mana_cost_subtraction)

        MP_bonus, initiative, mana_bonus = allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction,
                                                            initiative, mana_cost_subtraction, mana_bonus)

        final_MP = int(acting_army.hero.magic_power + MP_bonus)
        final_MP = magic_resistance(b, unit, TileNum, final_MP)

        charges = 4 + math.floor(final_MP / 3)
        damage = random.randint(2 + math.floor(final_MP * 3 / 5), 4 + math.floor(final_MP * 3 / 4))

        if len(unit.crew) > 0:
            while charges > 0:
                target = random.randint(0, len(unit.crew) - 1)
                unit.crew[target].HP -= damage

                if unit.crew[target].HP <= 0:
                    b.dealt_damage += (damage + unit.crew[target].HP)
                    b.killed_creatures += 1
                    unit.crew[target].HP = 0
                else:
                    b.dealt_damage += damage

                r = 49
                t = random.random()
                u = random.random()
                x = math.ceil(r * u)
                y = math.ceil(r * t)
                print(x, y)
                b.positions_list.append([x - 3, y - 13])

                charges -= 1

            perished_creatures(b, unit)

        info_card = None
        for card in b.queue:
            if card.position == unit.position and card.obj_type == "Regiment":
                info_card = card
                break

        add_effect = add_or_prolong_effect(unit, b, "Freeze", 3.0)

        if add_effect:
            b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + 3.0), "Effect", info_card.army_id,
                                                   info_card.owner, info_card.number, info_card.position,
                                                   "Icons", "eff", info_card.f_color, info_card.s_color,
                                                   4, 14, 20, 20, "Freeze"))

            unit.effects.append(effect_classes.Battle_Effect("Freeze", False,
                                                             float(b.queue[0].time_act),
                                                             float(3.0),
                                                             [effect_classes.Buff("Speed", 1,
                                                                                  "subtraction", None)]))

        print("mana_cost " + str(ability_catalog.ability_cat[b.selected_ability].mana_cost))
        print("mana_bonus " + str(mana_bonus))
        acting_army.hero.mana_reserve -= int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
        print("hero.initiative - " + str(acting_army.hero.initiative) + ", time_act - " + str(b.queue[0].time_act) +
              ", initiative - " + str(initiative))
        acting_army.hero.initiative = float(initiative)

        # Update visuals
        sprites_list = ["Battle_effects/icicle_a"]
        update_gf_battle.add_battle_effects_sprites(sprites_list)
        return True
    else:
        print("hail_spell() - Selected wrong unit")
        return False


def artifact_bonus(spell_name, school, hero, MP_addition_list, initiative_reduction, mana_cost_subtraction):
    if len(hero.inventory) > 0:
        for artifact in hero.inventory:
            for effect in artifact.effects:
                allowed = True
                if len(effect.other_tags) > 0:
                    allowed = False
                    if spell_name in effect.other_tags or school in effect.other_tags:
                        allowed = True

                # print("Allowed - " + str(allowed))
                if allowed:
                    if effect.application == "Ability bonus Magic Power":
                        if effect.method == "addition":
                            MP_addition_list.append(int(effect.quantity))
                    elif effect.application == "Ability bonus initiative":
                        if effect.method == "subtraction":
                            initiative_reduction.append(effect.quantity)
                    elif effect.application == "Ability mana cost":
                        if effect.method == "subtraction":
                            # print("Ability mana cost subtraction")
                            mana_cost_subtraction.append(effect.quantity)
                        elif effect.method == "addition":
                            mana_cost_subtraction.append(effect.quantity * -1)


def magic_resistance(b, unit, TileNum, final_MP):
    print("name - " + str(unit.name) + ", magic_power " + str(unit.magic_power))
    unit_MP = int(unit.magic_power)
    the_hero = None
    for army in game_obj.game_armies:
        if army.army_id == b.battle_map[TileNum].army_id:
            if army.hero is not None:
                the_hero = army.hero
            break

    if the_hero is not None:
        if len(the_hero.inventory) > 0:
            for artifact in the_hero.inventory:
                for effect in artifact.effects:
                    allowed = True
                    if len(effect.other_tags) > 0:
                        allowed = False
                        for tag in caster.reg_tags:
                            if tag in effect.other_tags:
                                allowed = True

                    if allowed:
                        # Magic power bonus from artifacts calculated in the beginning of the fight now and allocated to
                        # regiment.magic_power
                        # if effect.application == "Bonus Magic Power":
                        #     if effect.method == "addition":
                        #         unit_MP += int(effect.quantity)
                        pass

    if final_MP - int(unit_MP) < 0:
        final_MP = 0
    else:
        final_MP -= int(unit_MP)

    print("final_MP - " + str(final_MP) + ", unit_MP - " + str(unit_MP))
    return final_MP


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


def perished_creatures(b, unit):
    # Needed to calculate morale hit
    before_HP = 0
    for creature in unit.crew:
        before_HP += creature.HP

    # Let's check who died in unit
    long_msg = ""
    number = 1
    perished_list = []
    index = 0
    for df_creature in unit.crew:
        number += 1
        if df_creature.HP == 0:
            perished_list.append(index)

        index += 1

    perished_list.reverse()

    for perished in perished_list:
        # Remove killed creature
        unit.cemetery.append(unit.crew[perished])
        del unit.crew[perished]

    print(long_msg)

    # If no alive creatures left, kill this unit
    if len(unit.crew) == 0:
        game_battle.kill_unit(b, unit)

    # Reduce morale
    game_battle.reduce_morale(b, unit, before_HP, "Spell")

    game_battle.check_if_no_one_left_alive(b)


script_cat = {"Direct order - increase morale" : increase_morale,
              "Direct order - advance initiative" : advance_initiative,
              "Bless" : bless_spell,
              "Haste" : haste_spell,
              "Healing" : healing_spell,
              "Devine protection" : devine_protection_spell,
              "Devine strength" : devine_strength_spell,
              "Inspiration" : inspiration_spell,
              "Missile shielding" : missile_shielding_spell,
              "Fire arrows" : fire_arrows_spell,
              "Lightning bolts" : lightning_bolts_spell,
              "Hail" : hail_spell}
