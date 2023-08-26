## Miracle battles

import copy
import math
import random

from Resources import game_stats
from Resources import game_obj
from Resources import game_basic
from Resources import game_classes
from Resources import algo_circle_range
from Resources import faction_classes

from Strategy_AI import strategy_AI_classes

from Content import realm_leader_traits
from Content import unit_alignment_catalog

from Storage import create_unit


def prepare_known_map(player_power):
    for power in game_obj.game_powers:
        # print("power.name - " + str(power.name))
        power.known_map = []
        tiles_pool = []
        for city in game_obj.game_cities:
            # print("Settlement " + str(city.name) + " location is " + str(city.location) + " owned by "
            #       + str(city.owner))
            if city.owner == power.name:

                x = int((city.location + 1) % game_stats.cur_level_width)
                if x == 0:
                    x = int(game_stats.cur_level_width)
                y = int(math.ceil((city.location + 1) / game_stats.cur_level_width))
                # print("X is " + str(x) + " and Y is " + str(y))

                # if power.name == "Seventeenth":
                #     print("Seventeenth - " + "X is " + str(x) + " and Y is " + str(y))
                #     print("Seventeenth - " + str(city.location))
                #     print("game_stats.cur_level_width - " + str(game_stats.cur_level_width))

                for tile in algo_circle_range.within_circle_range([x, y], 4):
                    if tile not in power.known_map:
                        power.known_map.append(tile)
                    if tile not in tiles_pool:
                        tiles_pool.append(tile)

                    # if power.name == "Seventeenth":
                    #     print("Seventeenth - " + str(tile))

                # print("known_map - length " + str(len(power.known_map)) + " - " + str(power.known_map))

                # Facilities
                for TileNum in city.property:
                    for tile in algo_circle_range.simple_square_range(game_obj.game_map[TileNum].lot.posxy):
                        if tile not in power.known_map:
                            power.known_map.append(tile)
                        if tile not in tiles_pool:
                            tiles_pool.append(tile)

                        # if power.name == "Seventeenth":
                        #     print("Seventeenth - " + str(tile))

                # break

        for army in game_obj.game_armies:
            # print("Army location is " + str(army.location))
            # print("Army owner is " + str(army.owner))
            if army.owner == power.name:
                # print("Army location is " + str(army.location))
                x = int((army.location + 1) % game_stats.cur_level_width)
                y = int(math.ceil((army.location + 1) / game_stats.cur_level_width))
                # print("X is " + str(x) + " and Y is " + str(y))
                for tile in algo_circle_range.within_circle_range([x, y], 5):
                    if tile not in power.known_map:
                        power.known_map.append(tile)
                    if tile not in tiles_pool:
                        tiles_pool.append(tile)

                break

        prepare_diplomatic_contacts(power, tiles_pool)

        if power.name == player_power:
            print("power.known_map: " + str(power.known_map))
            game_stats.map_to_display = power.known_map
            print("map_to_display: " + str(game_stats.map_to_display))
            # print("prepare_known_map - contacts: " + str(power.contacts))

        # if power.name == "Seventeenth":
        #     print("prepare_known_map - Seventeenth - contacts: " + str(power.contacts))


def prepare_leader_traits(player_power):
    for power in game_obj.game_powers:
        # Behavior traits
        if power.name == player_power:
            # Human player doesn't need behavior traits
            power.leader.behavior_traits = ["Human player"]

        else:
            # Replace "Random" traits with real traits
            if power.leader.behavior_traits[0] == "Random":
                # First behavior trait
                game_stats.realm_leader_traits_list = list(realm_leader_traits.behavior_traits_list)
                if power.leader.behavior_traits[0] in game_stats.realm_leader_traits_list:
                    game_stats.realm_leader_traits_list.remove(power.leader.behavior_traits[0])
                if power.leader.behavior_traits[1] in game_stats.realm_leader_traits_list:
                    game_stats.realm_leader_traits_list.remove(power.leader.behavior_traits[1])

                ban_list = []

                if power.leader.behavior_traits[0] in realm_leader_traits.behavior_traits_incompatibility:
                    for trait in realm_leader_traits.behavior_traits_incompatibility[power.leader.behavior_traits[0]]:
                        if trait not in ban_list:
                            ban_list.append(trait)

                if power.leader.behavior_traits[1] in realm_leader_traits.behavior_traits_incompatibility:
                    for trait in realm_leader_traits.behavior_traits_incompatibility[power.leader.behavior_traits[1]]:
                        if trait not in ban_list:
                            ban_list.append(trait)

                for trait in ban_list:
                    if trait in realm_leader_traits.behavior_traits_list:
                        game_stats.realm_leader_traits_list.remove(trait)

                power.leader.behavior_traits[0] = random.choice(game_stats.realm_leader_traits_list)

                game_stats.realm_leader_traits_list = []

            if power.leader.behavior_traits[1] == "Random":
                # Second behavior trait
                game_stats.realm_leader_traits_list = list(realm_leader_traits.behavior_traits_list)
                if power.leader.behavior_traits[0] in game_stats.realm_leader_traits_list:
                    game_stats.realm_leader_traits_list.remove(power.leader.behavior_traits[0])
                if power.leader.behavior_traits[1] in game_stats.realm_leader_traits_list:
                    game_stats.realm_leader_traits_list.remove(power.leader.behavior_traits[1])

                ban_list = []

                if power.leader.behavior_traits[0] in realm_leader_traits.behavior_traits_incompatibility:
                    for trait in realm_leader_traits.behavior_traits_incompatibility[power.leader.behavior_traits[0]]:
                        if trait not in ban_list:
                            ban_list.append(trait)

                if power.leader.behavior_traits[1] in realm_leader_traits.behavior_traits_incompatibility:
                    for trait in realm_leader_traits.behavior_traits_incompatibility[power.leader.behavior_traits[1]]:
                        if trait not in ban_list:
                            ban_list.append(trait)

                for trait in ban_list:
                    if trait in realm_leader_traits.behavior_traits_list:
                        game_stats.realm_leader_traits_list.remove(trait)

                power.leader.behavior_traits[1] = random.choice(game_stats.realm_leader_traits_list)

        game_stats.realm_leader_traits_list = []

        # Lifestyle traits
        # Replace "Random" traits with real traits
        if power.leader.lifestyle_traits[0] == "Random":
            # First lifestyle trait
            game_stats.realm_leader_traits_list = list(realm_leader_traits.lifestyle_traits_list)
            if power.leader.lifestyle_traits[0] in game_stats.realm_leader_traits_list:
                game_stats.realm_leader_traits_list.remove(power.leader.lifestyle_traits[0])
            if power.leader.lifestyle_traits[1] in game_stats.realm_leader_traits_list:
                game_stats.realm_leader_traits_list.remove(power.leader.lifestyle_traits[1])

            power.leader.lifestyle_traits[0] = random.choice(game_stats.realm_leader_traits_list)

            game_stats.realm_leader_traits_list = []

        if power.leader.lifestyle_traits[1] == "Random":
            # Second lifestyle trait
            game_stats.realm_leader_traits_list = list(realm_leader_traits.lifestyle_traits_list)
            if power.leader.lifestyle_traits[0] in game_stats.realm_leader_traits_list:
                game_stats.realm_leader_traits_list.remove(power.leader.lifestyle_traits[0])
            if power.leader.lifestyle_traits[1] in game_stats.realm_leader_traits_list:
                game_stats.realm_leader_traits_list.remove(power.leader.lifestyle_traits[1])

            power.leader.lifestyle_traits[1] = random.choice(game_stats.realm_leader_traits_list)

            game_stats.realm_leader_traits_list = []


def prepare_leader_nicknames():
    for power in game_obj.game_powers:
        list_of_nicknames = []
        for trait in power.leader.behavior_traits:
            if trait in realm_leader_traits.behavior_traits_nicknames:
                for nickname in realm_leader_traits.behavior_traits_nicknames[trait]:
                    if nickname not in list_of_nicknames:
                        list_of_nicknames.append(nickname)
            else:
                for nickname in realm_leader_traits.neutral_nicknames:
                    if nickname not in list_of_nicknames:
                        list_of_nicknames.append(nickname)

        for trait in power.leader.lifestyle_traits:
            if trait in realm_leader_traits.lifestyle_traits_nicknames:
                for nickname in realm_leader_traits.lifestyle_traits_nicknames[trait]:
                    if nickname not in list_of_nicknames:
                        list_of_nicknames.append(nickname)

        if len(list_of_nicknames) > 0:
            power.leader.name += " " + random.choice(list_of_nicknames)


def prepare_diplomatic_contacts(power, tiles_pool):
    explored_cities = []  # IDs
    explored_armies = []  # IDs

    for tile in tiles_pool:
        TileNum = (tile[1] - 1) * game_stats.cur_level_width + tile[0] - 1
        TileObj = game_obj.game_map[TileNum]

        if TileObj.city_id is not None:
            if TileObj.city_id not in explored_cities:
                explored_cities.append(TileObj.city_id)

            # if power.name == "Seventeenth":
            #     print(str(tile) + " - " + str(TileNum))

        if TileObj.army_id is not None:
            if TileObj.army_id not in explored_cities:
                explored_armies.append(TileObj.army_id)

    # print(power.name + " - explored_cities: " + str(explored_cities))

    for settlement in game_obj.game_cities:
        if settlement.city_id in explored_cities:
            if settlement.owner != power.name:
                if settlement.owner not in power.contacts:
                    power.contacts.append(str(settlement.owner))
                    for contacted_realm in game_obj.game_powers:
                        if contacted_realm.name == settlement.owner:
                            if power.name not in contacted_realm.contacts:
                                contacted_realm.contacts.append(str(power.name))
                            break

                    # if power.name == game_stats.player_power:
                    #     print("Settlement - " + str(settlement.owner))
                    #     print("Contacts: " + str(power.contacts))
                    #
                    # if power.name == "Seventeenth":
                    #     print("Seventeenth - Settlement - " + str(settlement.owner))
                    #     print("Seventeenth - Contacts: " + str(power.contacts))

    for army in game_obj.game_armies:
        if army.army_id in explored_armies:
            if army.owner != power.name:
                if army.owner not in power.contacts:
                    power.contacts.append(str(army.owner))
                    for contacted_realm in game_obj.game_powers:
                        if contacted_realm.name == army.owner:
                            if power.name not in contacted_realm.contacts:
                                contacted_realm.contacts.append(str(power.name))
                            break

                    # if power.name == game_stats.player_power:
                    #     print("Army - " + str(army.owner))
                    #     print("Contacts: " + str(power.contacts))
                    #
                    # if power.name == "Seventeenth":
                    #     print("Seventeenth - Settlement - " + str(army.owner))
                    #     print("Seventeenth - Contacts: " + str(power.contacts))


def prepare_AI_class_AI_cogs():
    for realm in game_obj.game_powers:
        realm.AI_cogs = game_classes.AI_cognition()


def prepare_AI_army_roles():
    for realm in game_obj.game_powers:
        if realm.AI_player:
            # Settlement capacity
            small_armies = 0  # Int(1)
            medium_armies = 0  # Int(2)
            large_armies = 0  # Int(3)
            for settlement in game_obj.game_cities:
                if settlement.owner == realm.name:
                    if settlement.military_occupation is None:
                        small_armies += 1
                        medium_armies += 1

            for army in game_obj.game_armies:
                if army.owner == realm.name:
                    realm.AI_cogs.army_roles.append(strategy_AI_classes.army_roles(int(army.army_id),
                                                                                   "Idle",
                                                                                   1))  # Army size

            if medium_armies > 0:
                # Upscale army_size if rank allows it
                print(str(realm.name) + ": Upscale army_size if rank allows it")
                for army in game_obj.game_armies:
                    if army.owner == realm.name:
                        if medium_armies > 0:
                            rank_sum = 0
                            for unit in army.units:
                                rank_sum += int(unit.rank)
                            if rank_sum > 35:
                                for army_role in realm.AI_cogs.army_roles:
                                    if army_role.army_id == army.army_id:
                                        army_role.army_size = 2
                                        break

            if medium_armies > 0:
                # Upscale army_size even if rank lower recommended value
                print(str(realm.name) + ": Upscale army_size even if rank lower recommended value")
                for army in game_obj.game_armies:
                    if army.owner == realm.name:
                        if medium_armies > 0:
                            for army_role in realm.AI_cogs.army_roles:
                                if army_role.army_id == army.army_id:
                                    army_role.army_size = 2
                                    break

            for army in game_obj.game_armies:
                if army.owner == realm.name:
                    if game_obj.game_map[army.location].city_id is not None:
                        for settlement in game_obj.game_cities:
                            if settlement.city_id == game_obj.game_map[army.location].city_id:
                                for army_role in realm.AI_cogs.army_roles:
                                    if army_role.army_id == army.army_id:
                                        army_role.base_of_operation = int(settlement.city_id)
                                        break
                                break


def prepare_population_reserves():
    for tile in game_obj.game_map:
        if tile.lot == "City":
            for settlement in game_obj.game_cities:
                if settlement.city_id == tile.city_id:
                    for population in settlement.residency:
                        place_group = faction_classes.fac_groups_for_pop[settlement.alignment]
                        pop_group = place_group["Settlement"]
                        for pop_type in pop_group:
                            if pop_type[0] == population.name:
                                basket = list(pop_type[1])
                                # print(str(list(pop_type[1])))
                                for item in basket:
                                    # population.reserve = list(pop_type[1])
                                    population.reserve.append([str(item[0]), int(item[1])])
                                break
                    break

        elif tile.lot is not None:
            if tile.lot.obj_typ == "Facility":
                for population in tile.lot.residency:
                    place_group = faction_classes.fac_groups_for_pop[tile.lot.alignment]
                    pop_group = place_group[tile.lot.obj_name]
                    for pop_type in pop_group:
                        if pop_type[0] == population.name:
                            basket = list(pop_type[1])
                            # print(str(list(pop_type[1])))
                            for item in basket:
                                # population.reserve = list(pop_type[1])
                                population.reserve.append([str(item[0]), int(item[1])])
                            break


def prepare_regiments():
    for army in game_obj.game_armies:
        temp_list = list(army.units)
        army.units = []
        for card in temp_list:
            alignment = unit_alignment_catalog.alignment_dict[card.name]
            units_list = list(create_unit.LE_units_dict_by_alignment[alignment])
            for new_unit in units_list:
                if new_unit.name == card.name:
                    army.units.append(copy.deepcopy(new_unit))
                    break

        game_basic.establish_leader(army.army_id, "Game")


def map_all_tiles():
    map_positions = []
    for tile in game_obj.game_map:
        map_positions.append([int(tile.posxy[0]), int(tile.posxy[1])])

    return map_positions
