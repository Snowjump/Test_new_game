## Among Myth and Wonder
## common_selects

from Resources import game_obj


def copy_nested_list(original):
    # Function to help copy two-level lists (list of lists) to avoid weird bugs with references
    copied_list = []
    for i in original:
        copied_list.append(list(i))

    return copied_list


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


def select_army_role_by_id(realm, given_army_id):
    selected_role = None
    for role in realm.AI_cogs.army_roles:
        if role.army_id == given_army_id:
            selected_role = role
            break

    return selected_role


def select_treasury_by_realm_name(realm_name):
    selected_treasury = None
    for realm in game_obj.game_powers:
        if realm.name == realm_name:
            selected_treasury = realm.coffers
            break

    return selected_treasury
