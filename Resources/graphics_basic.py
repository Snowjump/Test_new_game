## Among Myth and Wonder
## graphics_basic

from Content.production_catalog import *

from Resources import game_stats
from Resources import game_obj
from Resources import graphics_obj
from Resources import common_selects
from Resources import graphics_classes

from Content import production_methods

from Screens.Game_Board_Windows import panel_resource_ribbon
from Screens.Game_Board_Windows import panel_calendar
from Screens.Game_Board_Windows import panel_left_ribbon_menu


def init_game_board_graphics():
    prepare_resource_ribbon()
    prepare_calendar()
    prepare_left_ribbon_menu()


def refresh_graphics_object(new_object):
    for obj in graphics_obj.game_board_objects:
        if obj.name == new_object.name:
            graphics_obj.game_board_objects.remove(obj)
            break

    graphics_obj.game_board_objects.append(new_object)


def prepare_calendar():
    new_object = panel_calendar.Calendar_Panel("Calendar")
    refresh_graphics_object(new_object)


def prepare_left_ribbon_menu():
    new_object = panel_left_ribbon_menu.Left_Ribbon_Menu("Left ribbon menu")
    refresh_graphics_object(new_object)


def prepare_resource_ribbon():
    treasury = common_selects.select_treasury_by_realm_name(game_stats.player_power)

    graphics_obj.resource_ribbon = []

    for resource in treasury:
        new_item = graphics_classes.Resource_Ribbon_Item(resource[0], resource[1], 0)
        graphics_obj.resource_ribbon.append(new_item)

    total_taxes = []

    for city in game_obj.game_cities:
        if city.owner == game_stats.player_power and not city.military_occupation:
            for tile_num in city.property:
                tile_obj = game_obj.game_map[tile_num]
                for pops in tile_obj.lot.residency:
                    estimate_taxes_by_pop(pops, city.buildings, tile_obj.lot.obj_name, total_taxes)
            for pops in city.residency:
                estimate_taxes_by_pop(pops, city.buildings, "Settlement", total_taxes)

    for recorded in total_taxes:
        found_resource = False
        for resource in graphics_obj.resource_ribbon:
            if resource.name == recorded[0]:
                resource.delta += recorded[1]
                found_resource = True
                break

        if not found_resource:
            new_item = graphics_classes.Resource_Ribbon_Item(recorded[0], 0, recorded[1])
            graphics_obj.resource_ribbon.append(new_item)

    total_expenses = []
    estimate_expenses(total_expenses)

    for recorded in total_expenses:
        found_resource = False
        for resource in graphics_obj.resource_ribbon:
            if resource.name == recorded[0]:
                resource.delta -= recorded[1]
                found_resource = True
                break

        if not found_resource:
            new_item = graphics_classes.Resource_Ribbon_Item(recorded[0], 0, recorded[1] * -1)
            graphics_obj.resource_ribbon.append(new_item)

    new_object = panel_resource_ribbon.Resource_Ribbon("Resource ribbon")
    # graphics_obj.resource_ribbon_panel = new_object
    refresh_graphics_object(new_object)


def estimate_taxes_by_pop(pops, building_plots, facility, total_taxes):
    reference = facility + "_" + pops.name
    if reference in taxes_by_place_and_pops_dict:
        taxes = common_selects.copy_nested_list(taxes_by_place_and_pops_dict[reference])
        # print("Base taxes: " + str(taxes))
        goods, taxes = production_methods.apply_effects(pops, building_plots, [], taxes)
        # print("Taxes in dictionary: " + str(taxes_by_place_and_pops_dict[reference]))
        # original = {"abc" : [[100, 200]]}
        # copy_list = list(original["abc"])
        # print("1) original: " + str(original))
        # print("1) copy_list: " + str(copy_list))
        # for i in copy_list:
        #     i[0] += 10
        #     print("i - " + str(i))
        # print("2) original: " + str(original))
        # print("2) copy_list: " + str(copy_list))
        for resource in taxes:
            found_record = False
            for recorded in total_taxes:
                if recorded[0] == resource[0]:
                    recorded[1] += resource[1]
                    found_record = True
                    break

            if not found_record:
                total_taxes.append([str(resource[0]), int(resource[1])])


def estimate_expenses(total_expenses):
    for army in game_obj.game_armies:
        if army.owner == game_stats.player_power:
            for unit in army.units:
                for upkeep in unit.cost:
                    add_new_resource = True
                    for resource in total_expenses:
                        if resource[0] == upkeep[0]:
                            add_new_resource = False
                            resource[1] += int(upkeep[1] * len(unit.crew))
                            break
                    if add_new_resource:
                        total_expenses.append([str(upkeep[0]), int(upkeep[1] * len(unit.crew))])
