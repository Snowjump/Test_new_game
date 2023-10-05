## Miracle battles!
## hero_AI

import random

from Surfaces import sf_battle
from Resources import battle_abilities_hero
from Resources import game_stats
from Resources import game_battle
from Content import ability_catalog


def manage_hero(b, acting_hero, own_units, enemy_units, own_army_id, enemy_army_id):
    print("manage_hero: " + acting_hero.hero_class + " " + acting_hero.name)
    # WIP, therefore only Direct order ability would be used
    sf_battle.open_hero_ability_menu_but(b)
    # Close it immediately
    b.battle_window = None

    for ability_name in b.list_of_abilities:
        if ability_name == "Direct order":
            b.selected_ability = "Direct order"
            break

    index_list = []
    num = 0
    for unit in own_units:
        if len(unit.crew) > 0 and not unit.deserted:
            index_list.append(num)
        num += 1
    if index_list:
        pos_xy = own_units[random.choice(index_list)].position
        TileNum = (pos_xy[1] - 1) * game_stats.battle_width + pos_xy[0] - 1
        b.selected_tile = [int(pos_xy[0]), int(pos_xy[1])]
        # Use ability
        b.AI_ready = False
        for action in ability_catalog.ability_cat[b.selected_ability].action:
            battle_abilities_hero.script_cat[action.script](b, TileNum, acting_hero)
        game_battle.action_order(b, "Pass", None)

    else:
        # Wait
        b.AI_ready = False
        game_battle.action_order(b, "Wait", None)
