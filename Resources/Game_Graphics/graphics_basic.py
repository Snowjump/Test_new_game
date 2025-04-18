## Among Myth and Wonder
## graphics_basic

from Content.production_catalog import *

from Resources import game_stats
from Resources import game_obj
from Resources import common_selects
from Resources.Game_Graphics import graphics_classes, graphics_obj

from Content import production_methods

from Screens.Game_Board_Windows import panel_exit_to_menu
from Screens.Game_Board_Windows import panel_save_game
from Screens.Game_Board_Windows import panel_calendar
from Screens.Game_Board_Windows import panel_resource_ribbon
from Screens.Game_Board_Windows import panel_left_ribbon_menu
from Screens.Game_Board_Windows import panel_vision_mode
from Screens.Sc_Battle_Windows import panel_waiting_list, panel_battle_queue, panel_battle_actions, \
    panel_selected_targets_counter
from Screens.Game_Board_Windows import info_panel_army
from Screens.Game_Board_Windows import info_panel_settlement
from Screens.Game_Board_Windows import info_panel_tile_obj
from Screens.Sc_Menus_Windows import panel_entrance_menu_buttons
from Screens.Sc_Menus_Windows import panel_skirmish_menu_interface
from Screens.Sc_Menus_Windows import panel_game_board_pause_menu_interface
from Screens.Sc_Menus_Windows import panel_load_game_menu_interface


def init_entrance_menu_graphics():
    # print("init_entrance_menu_graphics()")
    graphics_obj.menus_objects = []
    prepare_entrance_menu_buttons()


def init_skirmish_menu_graphics():
    # print("init_skirmish_menu_graphics()")
    graphics_obj.menus_objects = []
    prepare_skirmish_menu_interface()


def init_load_game_menu_graphics():
    # print("init_skirmish_menu_graphics()")
    graphics_obj.menus_objects = []
    prepare_load_game_menu_interface()


def init_game_board_graphics():
    graphics_obj.game_board_objects = []
    prepare_exit_to_menu()
    prepare_save_game()
    prepare_calendar()
    prepare_resource_ribbon()
    prepare_left_ribbon_menu()
    prepare_vision_mode_buttons()


def init_game_board_pause_menu_graphics():
    graphics_obj.menus_objects = []
    prepare_game_board_pause_menu_interface()


def init_level_editor_graphics():
    graphics_obj.level_editor_objects = []
    prepare_vision_mode_buttons()


def init_formation_battle_graphics():
    graphics_obj.battle_objects = []
    prepare_waiting_list()


def init_fighting_battle_graphics():
    graphics_obj.battle_objects = []
    prepare_battle_queue()
    prepare_battle_action_buttons()


def refresh_graphics_object(new_object, objects_list):
    for obj in objects_list:
        # print(obj.name)
        if obj.name == new_object.name:
            objects_list.remove(obj)
            break

    objects_list.append(new_object)


def remove_specific_objects(names_of_objects, location):
    print("remove_specific_objects()")
    for name in names_of_objects:
        print("remove " + name)
        for obj in location:
            print("obj name is " + obj.name)
            if obj.name == name:
                location.remove(obj)
                break


def remove_selected_objects(location):
    list_of_names = ["Info panel army",
                     "Info panel settlement",
                     "Info panel tile object"]
    remove_specific_objects(list_of_names, location)


def prepare_entrance_menu_buttons():
    # print("prepare_entrance_menu_buttons()")
    new_object = panel_entrance_menu_buttons.Entrance_Menu_Buttons_Panel("Entrance menu")
    refresh_graphics_object(new_object, graphics_obj.menus_objects)


def prepare_skirmish_menu_interface():
    new_object = panel_skirmish_menu_interface.Skirmish_Menu_Interface_Panel("Skirmish menu")
    refresh_graphics_object(new_object, graphics_obj.menus_objects)


def prepare_load_game_menu_interface():
    new_object = panel_load_game_menu_interface.Load_Game_Menu_Interface_Panel("Load game menu")
    refresh_graphics_object(new_object, graphics_obj.menus_objects)


def prepare_exit_to_menu():
    new_object = panel_exit_to_menu.Exit_To_Menu_Panel("Exit to menu")
    refresh_graphics_object(new_object, graphics_obj.game_board_objects)


def prepare_save_game():
    new_object = panel_save_game.Save_Game_Panel("Save game")
    refresh_graphics_object(new_object, graphics_obj.game_board_objects)


def prepare_calendar():
    new_object = panel_calendar.Calendar_Panel("Calendar")
    refresh_graphics_object(new_object, graphics_obj.game_board_objects)


def prepare_left_ribbon_menu():
    new_object = panel_left_ribbon_menu.Left_Ribbon_Menu("Left ribbon menu")
    refresh_graphics_object(new_object, graphics_obj.game_board_objects)


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
    refresh_graphics_object(new_object, graphics_obj.game_board_objects)


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


def prepare_army_panel():
    new_object = info_panel_army.Army_Panel("Info panel army")
    refresh_graphics_object(new_object, graphics_obj.game_board_objects)


def prepare_settlement_info_panel():
    new_object = info_panel_settlement.Settlement_Info_Panel("Info panel settlement")
    refresh_graphics_object(new_object, graphics_obj.game_board_objects)


def prepare_tile_obj_info_panel():
    new_object = info_panel_tile_obj.Tile_Obj_Panel("Info panel tile object")
    refresh_graphics_object(new_object, graphics_obj.game_board_objects)


def prepare_vision_mode_buttons():
    new_object = panel_vision_mode.Vision_Mode_Panel("Vision mode panel")
    print("prepare_vision_mode_buttons(): " + str(game_stats.current_screen))
    if game_stats.current_screen == "Game Board":
        refresh_graphics_object(new_object, graphics_obj.game_board_objects)
    elif game_stats.current_screen in ["Create Level", "Load Level Into Editor"]:
        refresh_graphics_object(new_object, graphics_obj.level_editor_objects)


def prepare_waiting_list():
    new_object = panel_waiting_list.Waiting_List_Panel("Waiting list panel")
    refresh_graphics_object(new_object, graphics_obj.battle_objects)


def prepare_game_board_pause_menu_interface():
    new_object = panel_game_board_pause_menu_interface.Game_Board_Pause_Menu_Interface_Panel("Game board pause menu")
    refresh_graphics_object(new_object, graphics_obj.menus_objects)


def prepare_save_game_submenu_interface():
    new_object = panel_game_board_pause_menu_interface.Save_Game_Interface_Panel("Save game submenu")
    refresh_graphics_object(new_object, graphics_obj.menus_objects)


def prepare_load_game_submenu_interface():
    new_object = panel_game_board_pause_menu_interface.Load_Game_Interface_Panel("Load game submenu")
    refresh_graphics_object(new_object, graphics_obj.menus_objects)


def prepare_battle_queue():
    new_object = panel_battle_queue.Battle_Queue_Panel("Battle queue panel")
    refresh_graphics_object(new_object, graphics_obj.battle_objects)


def prepare_battle_action_buttons():
    new_object = panel_battle_actions.Battle_Actions_Panel("Battle actions panel")
    refresh_graphics_object(new_object, graphics_obj.battle_objects)


def prepare_selected_targets_counter():
    new_object = panel_selected_targets_counter.Selected_Targets_Counter_Panel("Selected targets counter panel")
    refresh_graphics_object(new_object, graphics_obj.battle_objects)
