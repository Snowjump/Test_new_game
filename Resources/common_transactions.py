## Among Myth and Wonder
## common_transactions

from Resources import game_stats
from Resources import graphics_basic


def payment(resources, realm):
    for price in resources:
        print("payment() - " + str(price))
        for res in realm.coffers:
            if res[0] == price[0]:
                if res[1] - price[1] > 0:
                    res[1] -= price[1]
                else:
                    res[1] = 0

    if realm.name == game_stats.player_power:
        graphics_basic.prepare_resource_ribbon()


def sufficient_funds(resources, realm):
    enough_to_pay = False
    all_resources_present = True

    for price in resources:
        for res in realm.coffers:
            if res[0] == price[0]:
                if res[1] < price[1]:
                    all_resources_present = False
                    break

    if all_resources_present:
        enough_to_pay = True

    return enough_to_pay
