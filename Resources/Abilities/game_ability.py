## Among Myth and Wonder
## game_ability

from Resources import game_battle, game_stats, common_selects, graphics_basic, graphics_obj
from Resources.Abilities import battle_abilities_hero


def confirm_target(b, TileNum, player_army, opponent_army, ability):
    if ability.target == "single_ally":
        return find_single_ally(b, TileNum, player_army)
    elif ability.target == "single_enemy":
        return find_single_enemy(b, TileNum, opponent_army)


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


def skill_bonus(hero, MP_addition_list, initiative_reduction):
    for skill in hero.skills:
        for effect in skill.effects:
            if "Haste" in effect.other_tags:
                if effect.application == "Ability bonus Magic Power":
                    if effect.method == "addition":
                        MP_addition_list.append(int(effect.quantity))
                elif effect.application == "Ability bonus initiative":
                    if effect.method == "subtraction":
                        initiative_reduction.append(effect.quantity)


def artifact_bonus(spell_name, school, hero, MP_addition_list, initiative_reduction, mana_cost_subtraction):
    print("artifact_bonus")
    print(spell_name + "; " + school)
    print(hero.name)
    print("inventory - " + str(len(hero.inventory)) + ": " + str(hero.inventory))
    if len(hero.inventory) > 0:
        for artifact in hero.inventory:
            print(artifact.name)
            for effect in artifact.effects:
                allowed = True
                if len(effect.other_tags) > 0:
                    allowed = False
                    if spell_name in effect.other_tags or school in effect.other_tags:
                        allowed = True

                print("Allowed - " + str(allowed) + "; application - " + str(effect.application))
                if allowed:
                    if effect.application == "Ability bonus Magic Power":
                        if effect.method == "addition":
                            print("Ability bonus magic power adds + " + str(effect.quantity))
                            MP_addition_list.append(int(effect.quantity))
                    elif effect.application == "Ability bonus initiative":
                        if effect.method == "subtraction":
                            initiative_reduction.append(effect.quantity)
                    elif effect.application == "Ability mana cost":
                        if effect.method == "subtraction":
                            print("Ability mana cost subtraction: " + artifact.name + " -" + str(effect.quantity))
                            mana_cost_subtraction.append(effect.quantity)
                        elif effect.method == "addition":
                            mana_cost_subtraction.append(effect.quantity * -1)


def magic_resistance(unit, final_MP, opponent_army):
    print("name - " + str(unit.name) + ", magic_power " + str(unit.magic_power))
    unit_MP = int(unit.magic_power)
    the_hero = opponent_army.hero

    if the_hero:
        if len(the_hero.inventory) > 0:
            for artifact in the_hero.inventory:
                for effect in artifact.effects:
                    allowed = True
                    if len(effect.other_tags) > 0:
                        allowed = False
                        for tag in unit.reg_tags:
                            if tag in effect.other_tags:
                                allowed = True

                    if allowed:
                        # Magic power bonus from artifacts calculated in the beginning of the fight now and allocated to
                        # regiment.magic_power
                        pass

    if final_MP - int(unit_MP) < 0:
        final_MP = 0
    else:
        final_MP -= int(unit_MP)

    print("final_MP - " + str(final_MP) + ", unit_MP - " + str(unit_MP))
    return final_MP


def allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction, initiative, mana_cost_subtraction, mana_bonus):
    print("allocate_bonuses()")
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
    print("MP_bonus - " + str(MP_bonus))
    print("initiative - " + str(initiative))
    return MP_bonus, initiative, mana_bonus


def calculate_bonus(spell_name, school, hero, MP_addition_list, initiative_reduction, mana_cost_subtraction, MP_bonus,
                    initiative, mana_bonus):
    print("calculate_bonus()")
    print("initiative - " + str(initiative))
    skill_bonus(hero, MP_addition_list, initiative_reduction)
    artifact_bonus(spell_name, school, hero, MP_addition_list, initiative_reduction, mana_cost_subtraction)
    return allocate_bonuses(MP_addition_list, MP_bonus, initiative_reduction, initiative, mana_cost_subtraction,
                            mana_bonus)


def perished_creatures(b, unit, before_HP):
    # before_HP is required to calculate morale hit
    # Let's check who died in unit
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

    # If no alive creatures left, kill this unit
    if len(unit.crew) == 0:
        game_battle.kill_unit(b, unit)

    # Reduce morale
    game_battle.reduce_morale(b, unit, before_HP, "Spell")

    game_battle.check_if_no_one_left_alive(b)


def find_queue_card(b, unit):
    for card in b.queue:
        if card.position == unit.position and card.obj_type == "Regiment":
            return card


def manage_ability_targets(b):
    tile = (b.selected_tile[0], b.selected_tile[1])
    print("manage_ability_targets(): b.selected_tile " + str(b.selected_tile))
    if tile in b.ability_targets:
        b.ability_targets.remove(tile)
        print("b.ability_targets: " + str(b.ability_targets))
    else:
        if len(b.ability_targets) < b.total_targets:
            b.ability_targets.append(tile)


def select_all_targets(b, army):
    print("select_all_targets()")
    for card in b.queue:
        if card.army_id == army.army_id and card.obj_type == "Regiment":
            unit = army.units[card.number]
            if unit.crew and not unit.deserted:
                b.ability_targets.append((unit.position[0], unit.position[1]))


def execute_ability(b, ability):
    print("execute_ability()")
    player_army_id = int(b.queue[0].army_id)
    # opponent_army_id = int(b.attacker_id)
    # if b.attacker_realm == game_stats.player_power:
    #     player_army_id = int(b.queue[0].army_id)
    #     opponent_army_id = int(b.defender_id)
    opponent_army_id = int(b.attacker_id)
    if opponent_army_id == player_army_id:
        opponent_army_id = int(b.defender_id)
    player_army = common_selects.select_army_by_id(player_army_id)
    opponent_army = common_selects.select_army_by_id(opponent_army_id)

    player_army.hero.mana_reserve -= b.ability_mana_cost
    print("hero.initiative - " + str(player_army.hero.initiative) + "; b.initiative_cost - " + str(b.initiative_cost))
    player_army.hero.initiative = float(b.initiative_cost)
    print("hero.initiative = " + str(player_army.hero.initiative))

    if ability.target in ["single_ally", "single_enemy", "all_allies"]:
        for target in b.ability_targets:
            TileNum = (target[1] - 1) * game_stats.battle_width + target[0] - 1
            tile = b.battle_map[TileNum]
            for action in ability.action:
                if b.queue[0].obj_type == "Hero":
                    battle_abilities_hero.script_cat[action.script](b, tile, player_army, opponent_army, ability)

        graphics_basic.remove_specific_objects(["Selected targets counter panel"], graphics_obj.battle_objects)

    b.ready_to_act = False
    game_battle.action_order(b, "Pass", None)
