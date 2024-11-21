## Among Myth and Wonder
## common_selects

from Resources import game_obj
from Resources import game_stats


def copy_nested_list(original):
    # Function to help copy two-level lists (list of lists) to avoid weird bugs with references
    copied_list = []
    for i in original:
        copied_list.append(list(i))

    return copied_list


def select_settlement_by_id(given_settlement_id, report=None, location="game_cities"):
    settlements_location = {"game_cities": game_obj.game_cities,
                            "editor_cities": game_stats.editor_cities}
    selected_settlement = None
    for settlement in settlements_location[location]:
        if settlement.city_id == given_settlement_id:
            selected_settlement = settlement
            break

    if report:
        # print(location + " - " + str(settlements_location[location]))
        print("select_settlement_by_id: given_settlement_id - " + str(given_settlement_id) + "; name - "
              + selected_settlement.name)

    return selected_settlement


def select_army_by_id(given_army_id, report=None):
    selected_army = None
    for army in game_obj.game_armies:
        if army.army_id == given_army_id:
            selected_army = army
            break

    if report:
        print("select_army_by_id: army " + str(selected_army.army_id))

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
