## Among Myth and Wonder
## AI_game_ability

from Content.Abilities.AI_behavior import AI_select_target


def effect_is_present(unit, effect_name):
    present = False
    if unit.effects:
        for effect in unit.effects:
            if effect.name == effect_name:
                present = True
                break

    return present


def AI_manage_ability_seperate_targets(b, ability, acting_army, enemy_army):
    print("b.total_targets - " + str(b.total_targets))
    units = acting_army.units
    if ability.target == "single_enemy":
        units = enemy_army.units
    target_pool = AI_select_target.ability_cat[ability.name](b, units)
    target_pool.pick_targets(b)

    print("b.ability_targets: " + str(b.ability_targets))
