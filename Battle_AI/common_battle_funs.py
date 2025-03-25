## Among Myth and Wonder
## common_battle_funs

import random

from Battle_AI import common_search_funs

from Resources import game_stats
from Resources import game_battle


def set_melee_attack(b, acting_unit, enemy_nearby, approach_tile, find_approach_tile=False):
    # Regiment has an enemy in nearby tile
    # For now let's choose enemy at random
    melee_attacks_list = []
    num = 0
    for s in acting_unit.attacks:
        if s.attack_type == "Melee":
            melee_attacks_list.append(num)
        num += 1

    b.attack_type_index = random.choice(melee_attacks_list)
    b.attack_type_in_use = acting_unit.attacks[b.attack_type_index].attack_type

    chosen_enemy = random.choice(enemy_nearby)
    print("Hit nearby enemy at " + str(chosen_enemy))
    if find_approach_tile:
        approach_tile = common_search_funs.choose_approach(chosen_enemy, b)
        print("approach_tile - " + str(approach_tile))
    pos = game_battle.direction_of_hit(chosen_enemy, approach_tile)
    TileNum = (chosen_enemy[1] - 1) * game_stats.battle_width + chosen_enemy[0] - 1
    b.AI_ready = False
    game_battle.melee_attack_preparation(b, TileNum, pos, chosen_enemy[0], chosen_enemy[1])
