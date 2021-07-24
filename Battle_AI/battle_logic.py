## Miracle battles!

from Resources import game_obj
from Resources import game_battle
from Battle_AI import melee_AI
from Battle_AI import ranged_AI


def manage_unit(b, own_units, enemy_units, acting_unit, own_army_id, enemy_army_id):
    card = b.queue[0]

    if card.obj_type == "Regiment":

        for army in game_obj.game_armies:
            if army.army_id == card.army_id:
                unit = army.units[card.number]

        # Count units by type
        own_melee, own_ranged, enemy_melee, enemy_ranged = unit_account(own_units, enemy_units)

        if "ranged" in unit.reg_tags:
            ranged_AI.manage_ranged(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee,
                                    enemy_ranged, enemy_units)

            # # Wait
            # b.AI_ready = False
            # game_battle.action_order(b, "Wait", None)
            # # game_battle.complete_turn(b, 0.5)

        elif "melee" in unit.reg_tags:
            melee_AI.manage_melee(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee,
                                  enemy_ranged, enemy_units)

            # # Wait
            # b.AI_ready = False
            # game_battle.action_order(b, "Wait", None)
            # # game_battle.complete_turn(b, 0.5)


def unit_account(own_units, enemy_units):
    own_melee = 0
    own_ranged = 0
    enemy_melee = 0
    enemy_ranged = 0

    for i in own_units:
        if "melee" in i.reg_tags:
            own_melee += 1
        elif "ranged" in i.reg_tags:
            own_ranged += 1

    for i in enemy_units:
        if "melee" in i.reg_tags:
            enemy_melee += 1
        elif "ranged" in i.reg_tags:
            enemy_ranged += 1

    return own_melee, own_ranged, enemy_melee, enemy_ranged
