## Among Myth and Wonder
## caster_AI

import random

from Content.Abilities import ability_catalog
from Content.Abilities.AI_behavior import reg_abilities_application, reg_abilities_probability

from Battle_AI import common_search_funs
from Battle_AI import common_battle_funs

from Resources import game_stats
from Resources import game_battle

from Resources.Abilities import battle_abilities_regiment


def manage_caster(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee,
                  enemy_ranged, enemy_units, own_army, enemy_army, enemy_hero):
    # At beginning asses available abilities
    abilities_list = []
    application_type = []
    probability_to_use = []

    print("acting_unit.abilities - " + str(acting_unit.abilities))
    for ability in acting_unit.abilities:
        # print("ability - " + str(ability))
        if ability_catalog.ability_cat[ability].mana_cost <= acting_unit.mana_reserve:
            abilities_list.append(str(ability))
            application_type.append(str(reg_abilities_application.ability_role[ability]))
            probability_to_use.append(int(reg_abilities_probability.ability_value[ability]))

    ## Let's go through every ability tag, to determine which is possible to use
    if len(abilities_list) > 0:
        # Are there sufficiently enough hurt regiments to restore HP?
        if "Restore HP" in application_type:
            ignore_HP_restoration = True
            for unit in own_army.units:
                if unit.morale > 0.0:
                    HP_pool = 0
                    for creature in unit.crew:
                        HP_pool += int(creature.HP)

                    if len(unit.crew) * unit.max_HP - HP_pool >= 20:
                        ignore_HP_restoration = False
                        break

            # No application for HP restoration
            if ignore_HP_restoration:
                indexes = []
                num = 0
                for application in application_type:
                    if application == "Restore HP":
                        indexes.append(int(num))
                    num += 1

                indexes.reverse()

                for ind in indexes:
                    del abilities_list[ind]
                    del application_type[ind]
                    del probability_to_use[ind]

        if "Single ally buff" in application_type:
            # print("Ability tag - Single ally buff")
            ignore_buff = True
            alive_regiments = 0  # Regiments formidable enough to be worth to be buffed
            for unit in own_army.units:
                if unit.morale > 0.0 and len(unit.crew) > (unit.number * unit.rows) / 5:
                    # print(unit.name + " with morale - " + str(unit.morale) + ", crew size - " + str(len(unit.crew)))
                    alive_regiments += 1
            if alive_regiments > 1:
                # Remove those buffs, that can't be applied, due to presence of same buff
                remove_list = []
                num = 0
                for application in application_type:
                    if application == "Single ally buff":
                        print("Check ability - " + str(abilities_list[num]))
                        count = int(alive_regiments)
                        for unit in own_army.units:
                            if unit.morale > 0.0 and len(unit.crew) > (unit.number * unit.rows) / 5:
                                if present_effect(unit, abilities_list[num]):
                                    count -= 1

                        print("Counted regiments for buffing - " + str(count))
                        if count <= 1:
                            remove_list.append(num)

                    num += 1
                if len(remove_list) > 0:
                    remove_list.reverse()
                    for ind in remove_list:
                        del abilities_list[ind]
                        del application_type[ind]
                        del probability_to_use[ind]

                ignore_buff = False

            # No regiments to be buffed
            if ignore_buff:
                indexes = []
                num = 0
                for application in application_type:
                    if application == "Single ally buff":
                        indexes.append(int(num))
                    num += 1

                indexes.reverse()

                for ind in indexes:
                    del abilities_list[ind]
                    del application_type[ind]
                    del probability_to_use[ind]

    # Time to use ability if it possible
    if abilities_list:
        # print("abilities_list - " + str(abilities_list))
        # print("probability_to_use - " + str(probability_to_use))
        ability_to_perform = random.choices(abilities_list, weights=probability_to_use)
        print(str(acting_unit.name) + " will use ability - " + str(ability_to_perform[0]))
        position = abilities_list.index(ability_to_perform[0])
        ability_application = application_type[position]
        b.selected_ability = str(ability_to_perform[0])
        b.AI_ready = False
        ability_script_by_application[ability_application](ability_to_perform[0], b, acting_unit, own_army, enemy_army)

    else:
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


def present_effect(unit, effect_name):
    present = False
    if len(unit.effects) > 0:
        for effect in unit.effects:
            if effect.name == effect_name:
                present = True

    return present


def restore_HP_script(ability, b, acting_unit, own_army, enemy_army):
    regiment_index = []
    num = 0

    for unit in own_army.units:
        if unit.morale > 0.0:
            HP_pool = 0
            for creature in unit.crew:
                HP_pool += int(creature.HP)

                if len(unit.crew) * unit.max_HP - HP_pool >= 20:
                    regiment_index.append(num)

        num += 1

    selected_index = random.choice(regiment_index)

    TileNum = None
    x2 = int(own_army.units[selected_index].position[0])
    y2 = int(own_army.units[selected_index].position[1])
    TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1

    for action in ability_catalog.ability_cat[ability].action:
        battle_abilities_regiment.script_cat[action.script](b, TileNum, own_army.hero, acting_unit)

    game_battle.action_order(b, "Pass", None)


def single_ally_buff_script(ability, b, acting_unit, own_army, enemy_army):
    regiment_index = []
    num = 0

    for unit in own_army.units:
        if unit.morale > 0.0 and len(unit.crew) > (unit.number * unit.rows) / 5:
            regiment_index.append(num)

        num += 1

    selected_index = random.choice(regiment_index)
    TileNum = None
    x2 = int(own_army.units[selected_index].position[0])
    y2 = int(own_army.units[selected_index].position[1])
    TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1
    print("single_ally_buff_script, TileNum - " + str(TileNum))

    for action in ability_catalog.ability_cat[ability].action:
        battle_abilities_regiment.script_cat[action.script](b, TileNum, own_army.hero, acting_unit)

    game_battle.action_order(b, "Pass", None)


ability_script_by_application = {"Restore HP" : restore_HP_script,
                                 "Single ally buff" : single_ally_buff_script}
