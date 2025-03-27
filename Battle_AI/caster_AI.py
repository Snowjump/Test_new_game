## Among Myth and Wonder
## caster_AI

import random

from Content.Abilities import ability_catalog
from Content.Abilities import ability_targets

from Content.Abilities.AI_behavior import ability_cond

from Battle_AI import common_search_funs
from Battle_AI import common_battle_funs

from Resources import game_battle

from Resources.Abilities import game_ability
from Resources.Abilities import AI_game_ability

from Surfaces.Sf_Battle import ability_menu_funs


def manage_caster(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee,
                  enemy_ranged, enemy_units, own_army, enemy_army, enemy_hero):
    performed_ability = use_abilities(b, acting_unit, own_army, enemy_army)

    if not performed_ability:
        # Let's look at tiles surrounding this regiment, searching for enemies
        old_position = acting_unit.position
        enemy_nearby = common_search_funs.surrounding_enemies(b, enemy_army_id, old_position)

        if enemy_nearby:
            # Regiment has an enemy in nearby tile
            # Let's look for enemies without counterattack

            targets_without_counterattack = []

            for e in enemy_units:
                if e.position in enemy_nearby:
                    if e.counterattack == 0:
                        targets_without_counterattack.append(e.position)

            if targets_without_counterattack:
                print("Opportunity to hit an enemy without counterattack")
                common_battle_funs.set_melee_attack(b, acting_unit, targets_without_counterattack, old_position)
            else:
                print("No opportunity to hit an enemy without counterattack, therefore regiment shall defend itself")
                b.AI_ready = False
                game_battle.action_order(b, "Defend", None)

        else:
            # No enemy nearby
            # Let's find targets for ranged attack

            # Run out of options
            print("Run out of options")
            b.AI_ready = False
            game_battle.action_order(b, "Wait", None)


def use_abilities(b, caster, acting_army, enemy_army):
    b.attack_name = "Abilities"
    ability_menu_funs.open_regiment_ability_menu_but(b)
    # Close it immediately
    b.battle_window = None

    # 1) Select abilities that could be afforded with available mana
    available_ability_list = []
    for ability_name in b.list_of_abilities:
        if ability_catalog.ability_cat[ability_name].mana_cost <= caster.mana_reserve:
            available_ability_list.append(ability_name)
    print("available_ability_list: " + str(available_ability_list))

    # 2) Check if abilities fulfill conditions to be used in battle
    approved_ability_list = []
    weight_list = []
    for ability_name in available_ability_list:
        if ability_name in ability_cond.cond_cat:
            weight = ability_cond.cond_cat[ability_name](b, acting_army.units, enemy_army.units)
            if weight:
                approved_ability_list.append(ability_catalog.ability_cat[ability_name])
                # 2.1) Assign weights
                weight_list.append(weight)
                print("With weight " + str(weight) + " added ability - " + str(ability_name))

    print("approved_ability_list: " + str(len(approved_ability_list)))
    print("weight_list: " + str(weight_list))

    selected_ability = None
    if approved_ability_list:
        # 3) Select ability for use
        selected_ability = random.choices(approved_ability_list, weights=weight_list)[0]
    if selected_ability:
        print("selected_ability - " + str(selected_ability.name))
        MP_bonus, initiative, mana_bonus = game_ability.calculate_bonus_regiment(selected_ability.name,
                                                                                 selected_ability.school,
                                                                                 acting_army.hero,
                                                                                 caster,
                                                                                 selected_ability.base_initiative)
        b.ability_mana_cost = int(selected_ability.mana_cost + mana_bonus)
        b.initiative_cost = initiative
        b.bonus_magic_power = int(MP_bonus)

        # 4) Get targets for ability
        # print("4) Get targets for ability")
        # print("b.total_targets - " + str(b.total_targets))
        b.ability_targets = []
        if selected_ability.target == "all_allies":
            game_ability.select_all_targets(b, acting_army)
        else:
            # print("magic_power - " + str(acting_army.hero.magic_power) +
            #       "; bonus_magic_power - " + str(b.bonus_magic_power))
            b.total_targets = ability_targets.ability_cat[selected_ability.name](acting_army.hero.magic_power +
                                                                                 b.bonus_magic_power)
            AI_game_ability.AI_manage_ability_seperate_targets(b, selected_ability, acting_army, enemy_army)

    if selected_ability:
        # 5) Execute ability
        # Ability is performed
        game_ability.execute_ability(b, selected_ability)
        b.AI_ready = False
        game_battle.action_order(b, "Pass", None)
        return True
    else:
        return False
