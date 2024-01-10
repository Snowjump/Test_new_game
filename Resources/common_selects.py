## Among Myth and Wonder
## common_selects

from Resources import game_obj


def select_settlement_by_id(given_settlement_id):
    selected_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == given_settlement_id:
            selected_settlement = settlement
            break

    return selected_settlement


def select_army_by_id(given_army_id):
    selected_army = None
    for army in game_obj.game_armies:
        if army.army_id == given_army_id:
            selected_army = army
            break

    return selected_army


def select_realm_by_name(given_realm_name):
    selected_realm = None
    for realm in game_obj.game_powers:
        if realm.name == given_realm_name:
            selected_realm = realm
            break

    return selected_realm
