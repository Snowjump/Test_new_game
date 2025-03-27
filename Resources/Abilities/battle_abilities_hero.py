## Among Myth and Wonder
## battle_abilities_hero

import math
import random
# import numpy

from Resources import game_classes
from Resources import effect_classes
from Resources import update_gf_battle

from Resources.Abilities import game_ability


# Scripts
def increase_morale(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]

    print("increase_morale(): before " + unit.name + " unit.morale - " + str(unit.morale))
    unit.simple_change_morale(0.3)
    print("increase_morale(): after " + unit.name + " unit.morale - " + str(unit.morale))


def advance_initiative(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]
    info_card = game_ability.find_queue_card(b, unit)

    index0 = int(b.queue.index(info_card))
    lowest_time = b.queue[0].time_act
    found_new_place = False
    while not found_new_place:
        if b.queue[index0 - 1].time_act == info_card.time_act - 0.25:
            info_card.time_act -= 0.25
            found_new_place = True
        elif b.queue[index0 - 1].time_act > info_card.time_act - 0.25:
            if b.queue[index0 - 1].time_act == lowest_time:
                info_card.time_act = float(lowest_time)
                found_new_place = True
            else:
                index0 -= 1
        else:  # b.queue[index0 - 1].time_act < UnitCard.time_act - 0.25:
            info_card.time_act -= 0.25
            found_new_place = True

    print(info_card.owner + ": index0 - " + str(index0))
    print(acting_army.units[info_card.number].name)
    b.queue.insert(index0, b.queue.pop(b.queue.index(info_card)))

    b.anim_message.append(game_classes.Battle_Message(["Direct order",
                                                       "Morale + 0.3",
                                                       "Initiative - 0.25"],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def increase_army_morale(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]

    print("increase_army_morale(): before " + unit.name + " unit.morale - " + str(unit.morale))
    unit.simple_change_morale(0.5)
    print("increase_army_morale(): after " + unit.name + " unit.morale - " + str(unit.morale))
    b.anim_message.append(game_classes.Battle_Message(["Rally",
                                                       "Morale + 0.5"],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def bless_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]

    final_MP = int(magic_power + b.bonus_magic_power)

    duration = float(1.0 + final_MP)
    info_card = game_ability.find_queue_card(b, unit)

    add_effect = game_ability.add_or_prolong_effect(unit, b, "Bless", duration)

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

    b.anim_message.append(game_classes.Battle_Message(["Bless"],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def haste_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]

    final_MP = int(magic_power + b.bonus_magic_power)

    duration = float(1.0 + final_MP)
    increase = 2 + math.floor(final_MP / 2)
    info_card = game_ability.find_queue_card(b, unit)
    add_effect = game_ability.add_or_prolong_effect(unit, b, "Haste", duration)

    if add_effect:
        b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + duration), "Effect", info_card.army_id,
                                               info_card.owner, info_card.number, info_card.position,
                                               "Icons", "eff", info_card.f_color, info_card.s_color,
                                               4, 14, 20, 20, "Haste"))

        unit.effects.append(effect_classes.Battle_Effect("Haste", False,
                                                         float(b.queue[0].time_act),
                                                         float(b.queue[0].time_act + duration),
                                                         [effect_classes.Buff("Speed", increase,
                                                                              "addition", None)]))

    b.anim_message.append(game_classes.Battle_Message(["Haste", "Speed + " + str(increase)],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def healing_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]
    final_MP = int(magic_power + b.bonus_magic_power)

    charges = 4 + math.floor(final_MP / 3)
    heal_HP = 5 + math.floor(final_MP / 2)
    healed = 0

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
                healed += unit.max_HP - unit.crew[final_index].HP
                unit.crew[final_index].HP = int(unit.max_HP)
            else:
                unit.crew[final_index].HP += int(heal_HP)
                healed += heal_HP

            print(unit.crew[final_index].name + " HP - " + str(unit.crew[final_index].HP))

        charges -= 1

    b.anim_message.append(game_classes.Battle_Message(["Healing", "HP + " + str(healed)],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def divine_protection_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]
    final_MP = int(magic_power + b.bonus_magic_power)

    duration = float(1.0 + final_MP)
    increase = 2 + math.ceil(final_MP * 2 / 3)
    info_card = game_ability.find_queue_card(b, unit)

    add_effect = game_ability.add_or_prolong_effect(unit, b, "Divine protection", duration)

    if add_effect:
        b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + duration), "Effect", info_card.army_id,
                                               info_card.owner, info_card.number, info_card.position,
                                               "Icons", "eff", info_card.f_color, info_card.s_color,
                                               4, 14, 20, 20, "Divine protection"))

        unit.effects.append(effect_classes.Battle_Effect("Divine protection", False,
                                                         float(b.queue[0].time_act),
                                                         float(b.queue[0].time_act + duration),
                                                         [effect_classes.Buff("Defence", increase,
                                                                              "addition", None)]))

    b.anim_message.append(game_classes.Battle_Message(["Divine protection", "Defence + " + str(increase)],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def divine_strength_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]
    final_MP = int(magic_power + b.bonus_magic_power)

    duration = float(1.0 + final_MP)
    increase = 2 + math.ceil(final_MP * 2 / 3)
    info_card = game_ability.find_queue_card(b, unit)

    add_effect = game_ability.add_or_prolong_effect(unit, b, "Divine strength", duration)

    if add_effect:
        b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + duration), "Effect", info_card.army_id,
                                               info_card.owner, info_card.number, info_card.position,
                                               "Icons", "eff", info_card.f_color, info_card.s_color,
                                               4, 14, 20, 20, "Divine strength"))

        unit.effects.append(effect_classes.Battle_Effect("Divine strength", False,
                                                         float(b.queue[0].time_act),
                                                         float(b.queue[0].time_act + duration),
                                                         [effect_classes.Buff("Melee mastery", increase,
                                                                              "addition", None)]))

    b.anim_message.append(game_classes.Battle_Message(["Divine strength", "Melee mastery + " + str(increase)],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def inspiration_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]
    final_MP = int(magic_power + b.bonus_magic_power)

    morale_improvement = 1.0 + final_MP * 0.2
    increase = morale_improvement
    if unit.morale + morale_improvement > unit.leadership:
        increase = float(unit.leadership) - unit.morale
    unit.simple_change_morale(morale_improvement)

    b.anim_message.append(game_classes.Battle_Message(["Inspiration", "Morale + " + str(increase)],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def missile_shielding_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = acting_army.units[tile.unit_index]
    final_MP = int(magic_power + b.bonus_magic_power)

    duration = float(1.0 + final_MP)
    increase = 2 + math.ceil(final_MP * 2 / 3)
    info_card = game_ability.find_queue_card(b, unit)

    add_effect = game_ability.add_or_prolong_effect(unit, b, "Missile shielding", duration)
    print("add_effect - " + str(add_effect))
    if add_effect:
        b.queue.append(game_classes.Queue_Card(float(b.queue[0].time_act + duration), "Effect", info_card.army_id,
                                               info_card.owner, info_card.number, info_card.position,
                                               "Icons", "eff", info_card.f_color, info_card.s_color,
                                               4, 14, 20, 20, "Missile shielding"))

        unit.effects.append(effect_classes.Battle_Effect("Missile shielding", False,
                                                         float(b.queue[0].time_act),
                                                         float(b.queue[0].time_act + duration),
                                                         [effect_classes.Buff("Missile defence", increase,
                                                                              "addition", None)]))

    b.anim_message.append(game_classes.Battle_Message(["Missile shielding", "Missile defence + " + str(increase)],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def fire_arrows_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = opponent_army.units[tile.unit_index]
    final_MP = int(magic_power + b.bonus_magic_power)
    final_MP = game_ability.magic_resistance(unit, final_MP, opponent_army)
    print("hero.magic_power - " + str(acting_army.hero.magic_power) + ", final_MP - " + str(final_MP))
    b.dealt_damage = 0
    before_HP = 0
    for creature in unit.crew:
        before_HP += creature.HP

    charges = 7 + math.floor(final_MP / 3)

    dealt_damage = 0
    killed_creatures = 0

    if len(unit.crew) > 0:
        while charges > 0:
            damage = random.randint(3 + math.floor(final_MP * 2 / 3), 4 + math.floor(final_MP * 4 / 5))
            target = random.randint(0, len(unit.crew) - 1)
            print("Creature HP " + str(unit.crew[target].HP) + "; damage " + str(damage))
            unit.crew[target].HP -= damage

            if unit.crew[target].HP <= 0:
                dealt_damage += (damage + unit.crew[target].HP)
                killed_creatures += 1
                unit.crew[target].HP = 0
            else:
                dealt_damage += damage

            r = 49
            t = random.random()
            u = random.random()
            x = math.ceil(r * math.sqrt(t) * math.cos(2 * math.pi * u))
            y = math.ceil(r * math.sqrt(t) * math.sin(2 * math.pi * u))
            # print(x, y)
            b.positions_list.append([x - 8, y - 8])

            charges -= 1

        b.dealt_damage += dealt_damage
        game_ability.perished_creatures(b, unit, before_HP)

    print(str(killed_creatures) + " creatures died from dealing " + str(dealt_damage) + " damage")

    # Update visuals
    sprites_list = ["Battle_effects/flame_a_01", "Battle_effects/flame_a_02",
                    "Battle_effects/flame_a_03", "Battle_effects/flame_a_04"]
    update_gf_battle.add_battle_effects_sprites(sprites_list)
    b.anim_message.append(game_classes.Battle_Message(["Fire arrows", "Damage " + str(dealt_damage),
                                                       "Killed " + str(killed_creatures)],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def lightning_bolts_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = opponent_army.units[tile.unit_index]
    final_MP = int(magic_power + b.bonus_magic_power)
    final_MP = game_ability.magic_resistance(unit, final_MP, opponent_army)
    b.dealt_damage = 0
    before_HP = 0
    for creature in unit.crew:
        before_HP += creature.HP

    charges = 4 + math.floor(final_MP / 4)

    dealt_damage = 0
    killed_creatures = 0

    if len(unit.crew) > 0:
        while charges > 0:
            damage = random.randint(2 + math.floor(final_MP * 2 / 5), 8 + math.floor(final_MP * 3 / 2))
            target = random.randint(0, len(unit.crew) - 1)
            print("Creature HP " + str(unit.crew[target].HP) + "; damage " + str(damage))
            unit.crew[target].HP -= damage

            if unit.crew[target].HP <= 0:
                dealt_damage += (damage + unit.crew[target].HP)
                killed_creatures += 1
                unit.crew[target].HP = 0
            else:
                dealt_damage += damage

            r = 49
            t = random.random()
            u = random.random()
            x = math.ceil(r * math.sqrt(t) * math.cos(2 * math.pi * u))
            y = math.ceil(r * math.sqrt(t) * math.sin(2 * math.pi * u))
            # print(x, y)
            b.positions_list.append([x - 10, y - 38])

            charges -= 1

        b.dealt_damage += dealt_damage
        game_ability.perished_creatures(b, unit, before_HP)

    print(str(killed_creatures) + " creatures died from dealing " + str(dealt_damage) + " damage")
    print("")

    # Update visuals
    sprites_list = ["Battle_effects/lightning_bolt_a_01", "Battle_effects/lightning_bolt_a_02",
                    "Battle_effects/lightning_bolt_a_03", "Battle_effects/lightning_bolt_a_04"]
    update_gf_battle.add_battle_effects_sprites(sprites_list)
    b.anim_message.append(game_classes.Battle_Message(["Lightning bolts", "Damage " + str(dealt_damage),
                                                       "Killed " + str(killed_creatures)],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


def hail_spell(b, tile, acting_army, opponent_army, ability, magic_power):
    unit = opponent_army.units[tile.unit_index]
    final_MP = int(magic_power + b.bonus_magic_power)
    final_MP = game_ability.magic_resistance(unit, final_MP, opponent_army)
    b.dealt_damage = 0
    before_HP = 0
    for creature in unit.crew:
        before_HP += creature.HP

    charges = 4 + math.floor(final_MP / 3)
    dealt_damage = 0
    killed_creatures = 0

    if len(unit.crew) > 0:
        while charges > 0:
            damage = random.randint(2 + math.floor(final_MP * 3 / 5), 4 + math.floor(final_MP * 3 / 4))
            target = random.randint(0, len(unit.crew) - 1)
            print("Creature HP " + str(unit.crew[target].HP) + "; damage " + str(damage))
            unit.crew[target].HP -= damage

            if unit.crew[target].HP <= 0:
                dealt_damage += (damage + unit.crew[target].HP)
                killed_creatures += 1
                unit.crew[target].HP = 0
            else:
                dealt_damage += damage

            r = 49
            t = random.random()
            u = random.random()
            x = math.ceil(r * u)
            y = math.ceil(r * t)
            # print(x, y)
            b.positions_list.append([x - 3, y - 13])

            charges -= 1

        b.dealt_damage += dealt_damage
        game_ability.perished_creatures(b, unit, before_HP)

    print(str(killed_creatures) + " creatures died from dealing " + str(dealt_damage) + " damage")

    info_card = game_ability.find_queue_card(b, unit)
    add_effect = game_ability.add_or_prolong_effect(unit, b, "Freeze", 3.0)

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

    # Update visuals
    sprites_list = ["Battle_effects/icicle_a"]
    update_gf_battle.add_battle_effects_sprites(sprites_list)
    b.anim_message.append(game_classes.Battle_Message(["Hail", "Damage " + str(dealt_damage),
                                                       "Killed " + str(killed_creatures), "Freeze"],
                                                      "Regiment",
                                                      (unit.position[0], unit.position[1])))


script_cat = {"Direct order - increase morale" : increase_morale,
              "Direct order - advance initiative" : advance_initiative,
              "Rally" : increase_army_morale,
              "Bless" : bless_spell,
              "Haste" : haste_spell,
              "Healing" : healing_spell,
              "Divine protection" : divine_protection_spell,
              "Divine strength" : divine_strength_spell,
              "Inspiration" : inspiration_spell,
              "Missile shielding" : missile_shielding_spell,
              "Fire arrows" : fire_arrows_spell,
              "Lightning bolts" : lightning_bolts_spell,
              "Hail" : hail_spell}
