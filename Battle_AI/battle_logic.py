## Among Myth and Wonder
## battle_logic

from Resources import game_battle
from Resources import common_selects

from Battle_AI import hero_AI
from Battle_AI import melee_AI
from Battle_AI import ranged_AI
from Battle_AI import hybrid_AI
from Battle_AI import caster_AI


def manage_unit(b, own_units, enemy_units, acting_unit, own_army_id, enemy_army_id, acting_hero):
    card = b.queue[0]
    print("manage_unit() b.queue[0]: " + str(card.obj_type) + " " + str(card.owner))
    if acting_hero is not None:
        print("manage_unit: " + acting_hero.hero_class + " " + acting_hero.name)

    if card.obj_type == "Regiment":

        route_true = False
        army = common_selects.select_army_by_id(card.army_id)
        unit = army.units[card.number]

        if unit.morale <= 0.0:
            route_true = True

        # Count units by type
        own_melee, own_ranged, enemy_melee, enemy_ranged = unit_account(own_units, enemy_units)

        if "ranged" in unit.reg_tags:
            if route_true:
                print("Ranged regiment is routing from battlefield")
                b.AI_ready = False
                game_battle.action_order(b, "Move", "Route")

            else:
                ranged_AI.manage_ranged(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee,
                                        enemy_ranged, enemy_units)

            # # Wait
            # b.AI_ready = False
            # game_battle.action_order(b, "Wait", None)
            # # game_battle.complete_turn(b, 0.5)

        elif "hybrid" in unit.reg_tags:
            if route_true:
                print("Hybrid regiment is routing from battlefield")
                b.AI_ready = False
                game_battle.action_order(b, "Move", "Route")

            else:
                hybrid_AI.manage_hybrid(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee,
                                        enemy_ranged, enemy_units)

        elif "melee" in unit.reg_tags:
            if route_true:
                print("Melee regiment is routing from battlefield")
                b.AI_ready = False
                game_battle.action_order(b, "Move", "Route")

            else:
                melee_AI.manage_melee(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee,
                                      enemy_ranged, enemy_units, acting_hero)

            # # Wait
            # b.AI_ready = False
            # game_battle.action_order(b, "Wait", None)
            # # game_battle.complete_turn(b, 0.5)

        elif "caster" in unit.reg_tags:
            if route_true:
                print("Caster regiment is routing from battlefield")
                b.AI_ready = False
                game_battle.action_order(b, "Move", "Route")

            else:
                caster_AI.manage_caster(b, acting_unit, own_army_id, enemy_army_id, own_melee, own_ranged, enemy_melee,
                                        enemy_ranged, enemy_units)

    elif card.obj_type == "Hero":
        hero_AI.manage_hero(b, acting_hero, own_units, enemy_units, own_army_id, enemy_army_id)


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
