## Among Myth and Wonder
## power_ranking

import math
import random

from Resources import game_obj
from Resources import common_selects


def rank_ratio_calculation(own_army_sum_rank, target, power_border):
    target_sum_rank = 0
    for unit in target.units:
        target_sum_rank += unit.rank
    print("len(target.units) - " + str(len(target.units)) + "; target_sum_rank - " +
          str(target_sum_rank))

    tile = game_obj.game_map[target.location]
    if tile.lot is not None:
        if tile.lot == "City":
            settlement = common_selects.select_settlement_by_id(tile.city_id)
            if settlement.siege:
                # This is siege battle and target could get a power bonus from defensive structures
                # print("besieged = " + str(besieged))
                settlement_id = game_obj.game_map[target.location].city_id
                for settlement in game_obj.game_cities:
                    if settlement.city_id == settlement_id:
                        target_sum_rank = defence_structures_rank_bonus(target_sum_rank, target, settlement)
                        print("Siege target_sum_rank - " + str(target_sum_rank))
                        break

    rank_ratio = int(own_army_sum_rank / target_sum_rank * 100)
    random_risk_level = random.randint(0, 40)
    # Standard power border is 120, but against humans its 145
    print("rank_ratio - " + str(rank_ratio) + "; random_risk_level - " +
          str(random_risk_level) + "; result - " + str(power_border - random_risk_level))

    if rank_ratio >= power_border - random_risk_level:
        return True
    else:
        return False


def defence_structures_rank_bonus(sum_rank, target, settlement):
    number_of_rams = int(settlement.siege.battering_rams_ready)
    number_of_siege_towers = int(settlement.siege.siege_towers_ready)

    number_of_fighting_regiments = 0
    for regiment in target.units:
        number_of_fighting_regiments += 1

    number_of_gates = 0
    number_of_walls = 0
    number_of_barriers = 0
    for structure in settlement.defences:
        for def_obj in structure.def_objects:
            if def_obj.section_type in ["Wall", "Tower"]:
                if def_obj.state == "Unbroken":
                    number_of_walls += 1
            elif def_obj.section_type == "Gate":
                if def_obj.state == "Unbroken":
                    number_of_gates += 1
            elif def_obj.section_type == "Barrier":
                number_of_barriers += 1

    if number_of_rams > 0:
        number_of_gates = 0

    if number_of_walls - number_of_siege_towers < 0:
        number_of_walls = 0
    else:
        number_of_walls -= number_of_siege_towers

    number_of_walls += number_of_gates
    print("number_of_walls - " + str(number_of_walls))

    if number_of_barriers >= number_of_fighting_regiments:
        sum_rank *= 1.1
    else:
        sum_rank = sum_rank * (1 + 0.1 * (number_of_barriers / number_of_fighting_regiments))

    if number_of_walls >= number_of_fighting_regiments:
        sum_rank *= 1.25
    else:
        sum_rank = sum_rank * (1 + 0.25 * (number_of_walls / number_of_fighting_regiments))

    sum_rank = math.floor(sum_rank * 100) / 100

    return sum_rank
