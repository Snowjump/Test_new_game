## Miracle battles
import copy
import sys, pygame, math, random

from Resources import game_stats
from Resources import game_classes
from Content import faction_names
from Content import character_names
from Resources import level_save
from Content import terrain_catalog
from Resources import game_road_img
from Content import alinement_info
from Content import units_info
from Storage import create_unit
from Resources import game_basic
from Content import facility_catalog

yVar = game_stats.game_window_height - 800

button_zone = [[1150, 10, 1250, 32],
               [1040, 40, 1140, 62],
               [1150, 40, 1250, 62],
               [930, 40, 1030, 62],
               [1040, 10, 1140, 32],
               [930, 10, 1030, 32],
               [820, 10, 920, 32],
               [820, 40, 920, 62],
               [720, 10, 820, 32]]

brush_panel_zone = [[1044, 104, 1111, 126],
                    [1121, 104, 1188, 126],
                    [1198, 104, 1265, 126],
                    [1044, 134, 1150, 156],
                    [1160, 134, 1266, 156]]

roads_panel_zone = [[1044, 104, 1150, 126],
                    [1160, 104, 1266, 126]]

create_city_panel_zone = [[1044, 134, 1184, 166],
                          [1194, 134, 1226, 166],
                          [1234, 134, 1266, 166],
                          [1180, 174, 1266, 196],
                          [1214, 234, 1236, 256],
                          [1244, 234, 1266, 256],
                          [1044, 294, 1140, 316],
                          [1148, 294, 1266, 316]]

powers_panel_zone = [[1044, 134, 1184, 166],
                     [1194, 134, 1226, 166],
                     [1234, 134, 1266, 166],
                     [1180, 174, 1266, 196],
                     [1214, 264, 1236, 286],
                     [1244, 264, 1266, 286],
                     [1214, 294, 1236, 316],
                     [1244, 294, 1266, 316],
                     [1044, 324, 1266, 346],
                     [1244, 354, 1266, 376],
                     [1244, 469, 1266, 491]]

create_army_panel_zone = [[1044, 74, 1150, 96],
                          [1214, 74, 1236, 96],
                          [1244, 74, 1266, 96],
                          [1212, 194, 1266, 216],
                          [1044, 134, 1150, 156],
                          [1160, 134, 1266, 156]]

objects_panel_zone = [[1044, 74, 1175, 96],
                      [1044, 104, 1150, 126],
                      [1160, 104, 1266, 126]]

create_facility_panel_zone = [[1044, 74, 1185, 96],
                              [1244, 104, 1266, 126],
                              [1244, 469, 1266, 491]]

powers_lower_panel_zone = [[202, 664 + yVar, 260, 685 + yVar]]

create_city_lower_panel_zone = [[202, 694 + yVar, 260, 715 + yVar],
                                [202, 724 + yVar, 260, 745 + yVar]]

create_army_lower_panel_zone = [[202, 634 + yVar, 300, 655 + yVar]]

objects_forest_panel_zone = [[1044, 164, 1150, 186]]

objects_trees_panel_zone = [[1044, 164, 1150, 186]]


def level_editor_keys(key_action):
    if game_stats.map_operations == True:
        if key_action == 119:
            game_stats.pov_pos[1] -= 1
        elif key_action == 115:
            game_stats.pov_pos[1] += 1
        elif key_action == 97:
            game_stats.pov_pos[0] -= 1
        elif key_action == 100:
            game_stats.pov_pos[0] += 1

    ##    print("Key pressed " + str(key_action))
    pass


def level_editor_surface_m1(position):
    button_pressed = False
    ##    print("Success")
    button_numb = 0
    for square in button_zone:
        button_numb += 1
        ##        print("Level editor surface button " + str(button_numb))
        if square[0] < position[0] and square[1] < position[1] and square[2] > position[0] and square[3] > position[1]:
            button_funs[button_numb]()
            button_pressed = True
            break

    # Panels' zone
    if game_stats.level_editor_panel != "":
        p_funs = panel_buttons[game_stats.level_editor_panel]
        p_button_zone = panel_zone[game_stats.level_editor_panel]

        button_numb = 0
        for square in p_button_zone:
            button_numb += 1
            ##            print("Level editor panel button " + str(button_numb))
            if square[0] < position[0] and square[1] < position[1] and square[2] > position[0] and square[3] > position[
                1]:
                p_funs[button_numb]()
                button_pressed = True
                break

    # Right panel
    if game_stats.level_editor_panel != "":
        square = [1040, 70, 1270, 495]
        if square[0] < position[0] and square[1] < position[1] and square[2] > position[0] and square[3] > position[1]:
            button_pressed = True

            if position[1] >= 354 and position[0] < 1244 and game_stats.level_editor_panel == "powers panel":
                game_stats.white_index = math.floor((position[1] - 354) / 50) + game_stats.power_short_index
                print("white_index - " + str(game_stats.white_index) + " and power_short_index - " + str(
                    game_stats.power_short_index))

                game_stats.lower_panel = "powers lower panel"
                game_stats.powers_l_p_index = int(game_stats.white_index)

            elif position[1] >= 254 and position[0] < 1244 and game_stats.level_editor_panel == "create army panel":
                game_stats.white_index = math.floor((position[1] - 254) / 26) + game_stats.unit_short_index
                print("white_index - " + str(game_stats.white_index) + " and unit_short_index - " + str(
                    game_stats.unit_short_index))

                add_unit_to_army()

            elif position[1] >= 164 and position[0] < 1244 and game_stats.level_editor_panel == "objects panel":
                button_numb = 0
                for square in objects_panel_zone[game_stats.object_category]:
                    button_numb += 1
                    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                        objects_panel_buttons[game_stats.object_category][button_numb]()

            elif position[1] >= 104 and position[0] < 1244 and game_stats.level_editor_panel == "create facility panel":
                game_stats.white_index = math.floor((position[1] - 104) / 30) + game_stats.facility_short_index
                print("white_index - " + str(game_stats.white_index) + " and facility_short_index - " + str(
                    game_stats.facility_short_index))

                create_new_facility()

    # Lower panel
    if game_stats.lower_panel != "":
        yVar = game_stats.game_window_height - 800

        print("game_stats.lower_panel - " + str(game_stats.lower_panel))
        lp_funs = lower_panel_buttons[game_stats.lower_panel]
        lp_button_zone = lower_panel_zone[game_stats.lower_panel]

        button_numb = 0

        for square in lp_button_zone:
            button_numb += 1

            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                lp_funs[button_numb]()
                button_pressed = True
                break

        square = [200, 600 + yVar, 1080, 800 + yVar]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_pressed = True

        if position[1] >= 604 + yVar and position[0] >= 430 and game_stats.lower_panel == "create army lower panel":
            delete_selected_unit(position)

    # Click on game map
    if button_pressed == False:
        game_stats.selected_tile = []

        x = math.ceil(position[0] / 48)
        y = math.ceil(position[1] / 48)
        x = int(x) + int(game_stats.pov_pos[0])
        y = int(y) + int(game_stats.pov_pos[1])
        print("Coordinates - x " + str(x) + " y " + str(y))
        game_stats.selected_tile = [int(x), int(y)]

        # Brush instrument coded separately, because it could use different size of brush
        if game_stats.edit_instrument == "brush":
            game_stats.level_editor_panel = "brush panel"

            # Going through every tile in brush depending on it size
            y_axis = range((game_stats.brush_size - 1) * -1, game_stats.brush_size)
            for i in y_axis:
                x_axis = range((game_stats.brush_size - 1) * -1, game_stats.brush_size)
                for j in x_axis:

                    # Index of selected tile in map list
                    x2 = int(game_stats.selected_tile[0]) + j
                    y2 = int(game_stats.selected_tile[1]) + i
                    TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1

                    if x2 > 0 and x2 <= game_stats.new_level_width:
                        if y2 > 0 and y2 <= game_stats.new_level_height:

                            if game_stats.brush in ["Plain", "Northlands"]:
                                game_stats.level_map[TileNum].terrain = game_stats.brush
                                game_stats.level_map[TileNum].conditions = \
                                    terrain_catalog.terrain_calendar[game_stats.brush][game_stats.LE_month]
                            elif game_stats.brush == "Passage":
                                game_stats.level_map[TileNum].natural_feature = game_classes.passage("Passage")
                                if game_stats.level_map[TileNum].cave == False:
                                    game_stats.level_map[TileNum].cave = True
                            elif game_stats.brush == "Remove passage":
                                game_stats.level_map[TileNum].natural_feature = None

        elif game_stats.edit_instrument == "put object":

            # Index of selected tile in map list
            x2 = int(game_stats.selected_tile[0])
            y2 = int(game_stats.selected_tile[1])
            TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1

            if 0 < x2 <= game_stats.new_level_width:
                if 0 < y2 <= game_stats.new_level_height:
                    # Brush to remove any terrain objects
                    if game_stats.brush == "Remove object":
                        if game_stats.level_map[TileNum].lot is not None:
                            if game_stats.level_map[TileNum].lot != "City":
                                if game_stats.level_map[TileNum].lot.obj_typ == "Obstacle":
                                    game_stats.level_map[TileNum].lot = None
                                    game_stats.level_map[TileNum].travel = True

                    # Objects
                    # Forest
                    if game_stats.brush == "Obj - Oak forest":
                        if game_stats.level_map[TileNum].lot is None:
                            game_stats.level_map[TileNum].lot = game_classes.Map_Object([x2, y2], int(TileNum),
                                                                                        "Oak", "Nature/Trees/",
                                                                                        "Obstacle",
                                                                                        [[1, 0], [26, 0], [14, 14],
                                                                                         [3, 25], [28, 23]])
                            print('img/' + game_stats.level_map[TileNum].lot.img_path + "oak_summer" + '.png')
                            game_stats.level_map[TileNum].travel = False
                    elif game_stats.brush == "Obj - Oak trees":
                        if game_stats.level_map[TileNum].lot is None:
                            game_stats.level_map[TileNum].lot = game_classes.Map_Object([x2, y2], int(TileNum),
                                                                                        "Oak", "Nature/Trees/",
                                                                                        "Obstacle",
                                                                                        [[6, 22], [24, 6]])
                            print('img/' + game_stats.level_map[TileNum].lot.img_path + "oak_summer" + '.png')
                            game_stats.level_map[TileNum].travel = True

        # Index of selected tile in map list
        x2 = int(game_stats.selected_tile[0])
        y2 = int(game_stats.selected_tile[1])
        TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1

        if 0 < x2 <= game_stats.new_level_width:
            if 0 < y2 <= game_stats.new_level_height:

                if game_stats.edit_instrument == "create army":
                    game_stats.level_editor_panel = "create army panel"

                elif game_stats.edit_instrument == "road":
                    if game_stats.brush == "Remove road":
                        game_stats.level_map[TileNum].road = None
                    else:
                        game_road_img.add_road(TileNum, x2, y2)

                elif game_stats.edit_instrument == "create city":
                    game_stats.level_editor_panel = "create city panel"
                    if game_stats.level_map[TileNum].lot is not None:
                        game_stats.lower_panel = "create city lower panel"

                elif game_stats.edit_instrument == "draw control zone":
                    draw_control_zone(TileNum)

                elif game_stats.edit_instrument == "create facility":
                    game_stats.level_editor_panel = "create facility panel"


def level_editor_surface_m3(position):
    print("level_editor_surface_m3")


def return_to_main_menu_but():
    game_stats.current_screen = "Entrance Menu"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "main_menu_screen"
    game_stats.edit_instrument = ""
    game_stats.selected_tile = []
    game_stats.level_editor_panel = ""


def brush_but():
    game_stats.edit_instrument = "brush"
    game_stats.level_editor_panel = "brush panel"


def roads_but():
    game_stats.edit_instrument = "road"
    game_stats.level_editor_panel = "roads panel"


def save_but():
    level_save.save_new_level()
    print("Saved map")


def Terrain_Plain_but():
    game_stats.brush = "Plain"


def Terrain_Northlands_but():
    game_stats.brush = "Northlands"


def brush_1x1_but():
    game_stats.brush_size = 1


def brush_3x3_but():
    game_stats.brush_size = 2


def brush_5x5_but():
    game_stats.brush_size = 3


def Earthen_road_but():
    game_stats.brush = "Earthen"


def Remove_road_but():
    game_stats.brush = "Remove road"


def create_city_but():
    game_stats.edit_instrument = "create city"
    game_stats.level_editor_panel = ""
    game_stats.powers_l_p_index = 0
    game_stats.city_allegiance = "Neutral"
    game_stats.option_box_alinement_index = 0


def city_name_field_enter():
    print("type city name")
    game_stats.active_city_name_field = True
    game_stats.map_operations = False


def approve_city_name_but():
    game_stats.new_city_name = game_stats.boxed_city_name
    game_stats.boxed_city_name = ""
    game_stats.input_text = ""
    game_stats.active_city_name_field = False
    game_stats.map_operations = True


def cancel_city_name_but():
    game_stats.boxed_city_name = ""
    game_stats.input_text = ""
    game_stats.active_city_name_field = False
    game_stats.map_operations = True


def prev_power_index_but():
    if len(game_stats.editor_powers) > 0:
        if game_stats.powers_l_p_index == 0:
            game_stats.powers_l_p_index = len(game_stats.editor_powers) - 1
        elif game_stats.powers_l_p_index == -1:
            if len(game_stats.editor_powers) == 1:
                game_stats.powers_l_p_index = 0
            else:
                game_stats.powers_l_p_index = len(game_stats.editor_powers) - 2
        else:
            game_stats.powers_l_p_index -= 1


def next_power_index_but():
    if len(game_stats.editor_powers) > 0:
        if game_stats.powers_l_p_index == len(game_stats.editor_powers) - 1:
            game_stats.powers_l_p_index = 0
        elif game_stats.powers_l_p_index == -1:
            if len(game_stats.editor_powers) == 1:
                game_stats.powers_l_p_index = 0
            else:
                game_stats.powers_l_p_index = 0
        else:
            game_stats.powers_l_p_index += 1


def city_allegiance_but():
    if game_stats.city_allegiance == "Neutral":
        game_stats.city_allegiance = "Player's"
    else:
        game_stats.city_allegiance = "Neutral"


def create_new_city_but():
    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1
    print("TileNum - " + str(TileNum) + ", x - " + str(x) + ", y - " + str(y))

    if game_stats.level_map[TileNum].lot is None and game_stats.new_city_name != "":
        if (game_stats.city_allegiance == "Neutral") or \
                (game_stats.city_allegiance != "Neutral" and len(game_stats.editor_powers) > 0):
            owner = "Neutral"
            if game_stats.city_allegiance != "Neutral" and len(game_stats.editor_powers) > 0:
                owner = game_stats.editor_powers[game_stats.powers_l_p_index].name
            game_stats.LE_cities_id_counter += 1
            game_stats.level_map[TileNum].lot = "City"
            game_stats.level_map[TileNum].city_id = int(game_stats.LE_cities_id_counter)
            game_stats.editor_cities.append(game_classes.Settlement([x, y], int(TileNum),
                                                                    int(game_stats.LE_cities_id_counter),
                                                                    str(game_stats.new_city_name),
                                                                    alinement_info.alinements_list[
                                                                        game_stats.option_box_alinement_index],
                                                                    owner))

        game_stats.lower_panel = "create city lower panel"


def delete_city_but():
    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    focus = int(game_stats.level_map[TileNum].city_id)
    game_stats.level_map[TileNum].city_id = None
    game_stats.level_map[TileNum].lot = None

    for city in game_stats.editor_cities:
        if city.city_id == focus:
            game_stats.editor_cities.remove(city)

    game_stats.lower_panel = ""


def control_zone_but():
    if game_stats.edit_instrument == "create city":
        game_stats.edit_instrument = "draw control zone"
        game_stats.saved_selected_tile = list(game_stats.selected_tile)

        # Index of selected tile in map list
        x = int(game_stats.selected_tile[0])
        y = int(game_stats.selected_tile[1])
        TileNum = (y - 1) * game_stats.new_level_width + x - 1

        focus = int(game_stats.level_map[TileNum].city_id)

        game_stats.last_city_id = focus
    else:
        game_stats.edit_instrument = "create city"
        game_stats.selected_tile = list(game_stats.saved_selected_tile)
        game_stats.saved_selected_tile = []


def draw_control_zone(TileNum):
    if game_stats.level_map[TileNum].lot != "City":
        if game_stats.level_map[TileNum].city_id is None:
            game_stats.level_map[TileNum].city_id = game_stats.last_city_id
            focus1 = int(game_stats.level_map[TileNum].city_id)
            update_property(TileNum, focus1, None)
        elif game_stats.level_map[TileNum].city_id == game_stats.last_city_id:
            focus1 = int(game_stats.level_map[TileNum].city_id)
            game_stats.level_map[TileNum].city_id = None
            update_property(TileNum, focus1, None)
        else:
            focus2 = int(game_stats.level_map[TileNum].city_id)
            game_stats.level_map[TileNum].city_id = game_stats.last_city_id
            focus1 = int(game_stats.last_city_id)

            update_property(TileNum, focus1, focus2)


def powers_but():
    game_stats.edit_instrument = ""
    game_stats.level_editor_panel = "powers panel"
    game_stats.lower_panel = ""
    game_stats.power_short_index = 0
    game_stats.white_index = None
    game_stats.option_box_alinement_index = 0


def country_name_field_enter():
    print("type country name")
    game_stats.active_country_name_field = True
    game_stats.map_operations = False


def approve_country_name_but():
    game_stats.new_country_name = game_stats.boxed_country_name
    game_stats.boxed_country_name = ""
    game_stats.input_text = ""
    game_stats.active_country_name_field = False
    game_stats.map_operations = True


def cancel_country_name_but():
    game_stats.boxed_country_name = ""
    game_stats.input_text = ""
    game_stats.active_country_name_field = False
    game_stats.map_operations = True


def next_alinement_but():
    if game_stats.option_box_alinement_index + 1 == len(alinement_info.alinements_list):
        game_stats.option_box_alinement_index = 0
    else:
        game_stats.option_box_alinement_index += 1


def prev_first_color_but():
    if game_stats.option_box_first_color_index - 1 < 0:
        game_stats.option_box_first_color_index = len(faction_names.colors_list) - 1
    else:
        game_stats.option_box_first_color_index -= 1


def next_first_color_but():
    if game_stats.option_box_first_color_index + 1 == len(faction_names.colors_list):
        game_stats.option_box_first_color_index = 0
    else:
        game_stats.option_box_first_color_index += 1


def prev_second_color_but():
    if game_stats.option_box_second_color_index - 1 < 0:
        game_stats.option_box_second_color_index = len(faction_names.colors_list) - 1
    else:
        game_stats.option_box_second_color_index -= 1


def next_second_color_but():
    if game_stats.option_box_second_color_index + 1 == len(faction_names.colors_list):
        game_stats.option_box_second_color_index = 0
    else:
        game_stats.option_box_second_color_index += 1


def create_new_country_but():
    check = False
    if len(game_stats.editor_powers) > 0:
        check = True
        for power in game_stats.editor_powers:
            if power.name == game_stats.new_country_name:
                check = False
    else:
        check = True

    if check:
        game_stats.editor_powers.append(game_classes.Realm(game_stats.new_country_name,
                                                           faction_names.colors_list[
                                                               game_stats.option_box_first_color_index],
                                                           faction_names.colors_list[
                                                               game_stats.option_box_second_color_index],
                                                           alinement_info.alinements_list[
                                                               game_stats.option_box_alinement_index]))
        print("New country has been created")
        game_stats.lower_panel = "powers lower panel"
        game_stats.powers_l_p_index = -1


def prev_power_but():
    if len(game_stats.editor_powers) > 3:
        if game_stats.power_short_index == 0:
            game_stats.power_short_index = len(game_stats.editor_powers) - 3
        else:
            game_stats.power_short_index -= 1


def next_power_but():
    if len(game_stats.editor_powers) > 3:
        if game_stats.power_short_index == len(game_stats.editor_powers) - 3:
            game_stats.power_short_index = 0
        else:
            game_stats.power_short_index += 1


def delete_country_but():
    del game_stats.editor_powers[game_stats.powers_l_p_index]
    game_stats.power_short_index = 0
    game_stats.white_index = None
    if len(game_stats.editor_powers) == 0:
        game_stats.lower_panel = ""


def create_army_but():
    game_stats.edit_instrument = "create army"
    game_stats.level_editor_panel = ""
    game_stats.powers_l_p_index = 0
    game_stats.unit_short_index = 0
    game_stats.army_allegiance = "Neutral"
    game_stats.option_box_alinement_index = 0


def army_allegiance_but():
    if game_stats.army_allegiance == "Neutral":
        game_stats.army_allegiance = "Player's"
    else:
        game_stats.army_allegiance = "Neutral"


def next_army_alinement_but():
    game_stats.unit_short_index = 0
    if game_stats.option_box_alinement_index + 1 == len(alinement_info.advanced_alinements_list):
        game_stats.option_box_alinement_index = 0
    else:
        game_stats.option_box_alinement_index += 1


def create_new_army_but():
    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    # allegiance = alinement_info.advanced_alinements_list[game_stats.option_box_alinement_index]
    allegiance = str(game_stats.army_allegiance)
    print("Allegiance - " + allegiance)

    if game_stats.level_map[TileNum].army_id is None:
        # print("army_id is None")
        if (allegiance == "Neutral") or \
                (allegiance != "Neutral" and len(game_stats.editor_powers) > 0):
            owner = "Neutral"
            print("1. Owner - " + str(owner))
            if allegiance != "Neutral" and len(game_stats.editor_powers) > 0:
                owner = game_stats.editor_powers[game_stats.powers_l_p_index].name
                print("2. Owner - " + str(owner))
            game_stats.LE_army_id_counter += 1
            game_stats.level_map[TileNum].army_id = int(game_stats.LE_army_id_counter)
            game_stats.editor_armies.append(game_classes.Army([x, y], int(TileNum),
                                                              int(game_stats.LE_army_id_counter),
                                                              owner))

        game_stats.lower_panel = "create army lower panel"


def add_unit_to_army():
    print("add_unit_to_army")

    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    if game_stats.level_map[TileNum].army_id is not None:
        focus = game_stats.level_map[TileNum].army_id

        for army in game_stats.editor_armies:
            if army.army_id == focus:
                if len(army.units) < 20:
                    alignment = str(alinement_info.advanced_alinements_list[game_stats.option_box_alinement_index])
                    units_list = list(create_unit.LE_units_dict_by_alignment[alignment])

                    army.units.append(copy.deepcopy(units_list[game_stats.white_index]))
                    print("Added to army new unit - " + units_list[game_stats.white_index].name)

                    game_basic.establish_leader(focus)


def delete_army_but():
    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    if game_stats.level_map[TileNum].army_id is not None:
        focus = game_stats.level_map[TileNum].army_id
        for army in game_stats.editor_armies:
            if army.army_id == focus:
                game_stats.editor_armies.remove(army)
                game_stats.lower_panel = ""
                game_stats.level_map[TileNum].army_id = None


def delete_unit_but():
    if game_stats.delete_option == True:
        game_stats.delete_option = False
    else:
        # Switch status to give ability to delete units from army by clicking their names
        game_stats.delete_option = True


def delete_selected_unit(position):
    # If game_stats.delete_option == True, then user could click on unit's name to delete it
    x_numb = math.floor((position[0] - 430) / 160)
    y_numb = math.ceil((position[1] - (604 + yVar)) / 26)
    print("position x - " + str(x_numb) + " position y - " + str(y_numb))
    index = x_numb * 5 + y_numb - 1

    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    focus = game_stats.level_map[TileNum].army_id

    for army in game_stats.editor_armies:
        if army.army_id == focus:
            if len(army.units) - 1 >= index:
                del army.units[index]

    game_basic.establish_leader(focus)


def objects_but():
    game_stats.edit_instrument = "put object"
    game_stats.level_editor_panel = "objects panel"
    game_stats.object_category = ""
    game_stats.brush = ""


def remove_object_but():
    game_stats.brush = "Remove object"


def forest_category_but():
    game_stats.object_category = "Forest"


def trees_category_but():
    game_stats.object_category = "Trees"


def forest_oak_but():
    game_stats.brush = "Obj - Oak forest"
    print("game_stats.brush = Obj - Oak forest")


def trees_oak_but():
    game_stats.brush = "Obj - Oak trees"
    print("game_stats.brush = Obj - Oak trees")


def facility_but():
    game_stats.edit_instrument = "create facility"
    game_stats.level_editor_panel = ""
    game_stats.facility_short_index = 0


def remove_facility_but():
    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    if game_stats.level_map[TileNum].lot is not None:
        if game_stats.level_map[TileNum].lot != "City":
            if game_stats.level_map[TileNum].city_id is None:
                game_stats.level_map[TileNum].lot = None
            else:
                focus = int(game_stats.level_map[TileNum].city_id)
                for city in game_stats.editor_cities:
                    if city.city_id == focus:
                        for prop in city.property:
                            if prop == TileNum:
                                city.property.remove(prop)
                                game_stats.level_map[TileNum].lot = None


def create_new_facility():
    print("create_new_facility")

    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    if game_stats.level_map[TileNum].lot is None:
        if game_stats.level_map[TileNum].city_id is None:  # territory is without settlement yet
            facil = facility_catalog.LE_facility_list[game_stats.white_index]
            game_stats.level_map[TileNum].lot = game_classes.Facility([x, y], int(TileNum),
                                                                      facil,
                                                                      "Facilities/Neutral/",
                                                                      facility_catalog.LE_facility_img_name_list_neutral[
                                                                          game_stats.white_index],
                                                                      "Facility",
                                                                      [[0, 0]],
                                                                      "Neutrals")
        else:  # territory has a settlement
            focus = int(game_stats.level_map[TileNum].city_id)
            for city in game_stats.editor_cities:
                if city.city_id == focus:
                    alin = str(city.alignment)
                    facil = facility_catalog.LE_facility_list[game_stats.white_index]
                    facil_path = facility_catalog.facility_path_cat[alin][game_stats.white_index]
                    facil_name = facility_catalog.facility_img_name_cat[alin][game_stats.white_index]
                    game_stats.level_map[TileNum].lot = game_classes.Facility([x, y], int(TileNum),
                                                                              facil,
                                                                              facil_path,
                                                                              facil_name,
                                                                              "Facility",
                                                                              [[0, 0]],
                                                                              str(alin))
                    # Register new facility among settlement's property
                    city.property.append(int(TileNum))


def update_property(TileNum, focus1, focus2):
    if game_stats.level_map[TileNum].lot is not None:
        if game_stats.level_map[TileNum].lot != "City":
            if game_stats.level_map[TileNum].lot.obj_typ == "Facility":
                if game_stats.level_map[TileNum].city_id == None:
                    # Facility
                    game_stats.level_map[TileNum].lot.img_path = "Facilities/Neutral/"
                    number = facility_catalog.LE_facility_list.index(game_stats.level_map[TileNum].lot.obj_name)
                    game_stats.level_map[TileNum].lot.img_name = facility_catalog.LE_facility_img_name_list_neutral[
                        number]
                    game_stats.level_map[TileNum].alignment = "Neutrals"
                    # Settlement
                    for city in game_stats.editor_cities:
                        if city.city_id == focus1:
                            city.property.remove(int(TileNum))
                elif focus2 is None:
                    for city in game_stats.editor_cities:
                        if city.city_id == focus1:
                            # Facility
                            alin = str(city.alignment)
                            number = facility_catalog.LE_facility_list.index(game_stats.level_map[TileNum].lot.obj_name)
                            game_stats.level_map[TileNum].lot.img_path = facility_catalog.facility_path_cat[alin][
                                number]
                            game_stats.level_map[TileNum].lot.img_name = facility_catalog.facility_img_name_cat[alin][
                                number]
                            game_stats.level_map[TileNum].alignment = str(alin)

                            # Settlement
                            city.property.append(int(TileNum))

                else:
                    for city in game_stats.editor_cities:
                        if city.city_id == focus1:
                            # Facility
                            alin = str(city.alignment)
                            number = facility_catalog.LE_facility_list.index(game_stats.level_map[TileNum].lot.obj_name)
                            game_stats.level_map[TileNum].lot.img_path = facility_catalog.facility_path_cat[alin][
                                number]
                            game_stats.level_map[TileNum].lot.img_name = facility_catalog.facility_img_name_cat[alin][
                                number]
                            game_stats.level_map[TileNum].alignment = str(alin)

                            # New settlement
                            city.property.append(int(TileNum))
                    for city in game_stats.editor_cities:
                        if city.city_id == focus2:
                            # Old settlement
                            city.property.remove(int(TileNum))


button_funs = {1: return_to_main_menu_but,
               2: roads_but,
               3: brush_but,
               4: create_army_but,
               5: save_but,
               6: create_city_but,
               7: powers_but,
               8: objects_but,
               9: facility_but}

brush_panel_funs = {1: brush_1x1_but,
                    2: brush_3x3_but,
                    3: brush_5x5_but,
                    4: Terrain_Plain_but,
                    5: Terrain_Northlands_but}

roads_panel_funs = {1: Earthen_road_but,
                    2: Remove_road_but}

create_city_panel_funs = {1: city_name_field_enter,
                          2: approve_city_name_but,
                          3: cancel_city_name_but,
                          4: next_alinement_but,
                          5: prev_power_index_but,
                          6: next_power_index_but,
                          7: city_allegiance_but,
                          8: create_new_city_but}

powers_panel_funs = {1: country_name_field_enter,
                     2: approve_country_name_but,
                     3: cancel_country_name_but,
                     4: next_alinement_but,
                     5: prev_first_color_but,
                     6: next_first_color_but,
                     7: prev_second_color_but,
                     8: next_second_color_but,
                     9: create_new_country_but,
                     10: prev_power_but,
                     11: next_power_but}

create_army_panel_funs = {1: army_allegiance_but,
                          2: prev_power_index_but,
                          3: next_power_index_but,
                          4: next_army_alinement_but,
                          5: create_new_army_but,
                          6: delete_army_but}

objects_panel_funs = {1: remove_object_but,
                      2: forest_category_but,
                      3: trees_category_but}

create_facility_panel_funs = {1: remove_facility_but,
                              2: forest_category_but,
                              3: trees_category_but}

powers_lower_panel_funs = {1: delete_country_but}

create_city_lower_panel_funs = {1: delete_city_but,
                                2: control_zone_but}

create_army_lower_panel_funs = {1: delete_unit_but}

obj_forest_panel_funs = {1: forest_oak_but}

obj_trees_panel_funs = {1: trees_oak_but}

panel_buttons = {"brush panel": brush_panel_funs,
                 "roads panel": roads_panel_funs,
                 "create city panel": create_city_panel_funs,
                 "powers panel": powers_panel_funs,
                 "create army panel": create_army_panel_funs,
                 "objects panel": objects_panel_funs,
                 "create facility panel": create_facility_panel_funs}

objects_panel_buttons = {"Forest": obj_forest_panel_funs,
                         "Trees": obj_trees_panel_funs}

panel_zone = {"brush panel": brush_panel_zone,
              "roads panel": roads_panel_zone,
              "create city panel": create_city_panel_zone,
              "powers panel": powers_panel_zone,
              "create army panel": create_army_panel_zone,
              "objects panel": objects_panel_zone,
              "create facility panel": create_facility_panel_zone}

lower_panel_buttons = {"powers lower panel": powers_lower_panel_funs,
                       "create city lower panel": create_city_lower_panel_funs,
                       "create army lower panel": create_army_lower_panel_funs}

lower_panel_zone = {"powers lower panel": powers_lower_panel_zone,
                    "create city lower panel": create_city_lower_panel_zone,
                    "create army lower panel": create_army_lower_panel_zone}

objects_panel_zone = {"Forest": objects_forest_panel_zone,
                      "Trees": objects_trees_panel_zone}
