## Miracle battles
## sf_battle_editor

import copy
import sys, pygame, math, random

from Resources import game_stats
from Resources import game_classes
from Resources import faction_classes
from Resources import level_save
from Resources import update_gf_level_editor
from Resources import algo_building
from Resources import game_road_img
from Resources import game_basic
from Resources import algo_circle_range
from Resources import algo_square_range

from Content import objects_img_catalog
from Content import terrain_catalog
from Content import faction_names
from Content import alinement_info
from Content import units_info
from Content import facility_catalog
from Content import starting_resources
from Content import starting_settlement_effects
from Content import settlement_plots
from Content import settlement_structures
from Content import ef_structures
from Content import recruitment_structures
from Content import settlement_defences
from Content import exploration_catalog
from Content import lair_army_catalog
from Content import realm_leader_names
from Content import realm_leader_traits
from Content import terrain_seasons

from Storage import create_unit

yVar = game_stats.game_window_height - 800

button_zone = [[1150, 10, 1250, 32],
               [1040, 40, 1140, 62],
               [1150, 40, 1250, 62],
               [930, 40, 1030, 62],
               [1040, 10, 1140, 32],
               [930, 10, 1030, 32],
               [820, 10, 920, 32],
               [820, 40, 920, 62],
               [710, 10, 810, 32],
               [710, 40, 810, 62],
               [86, 5, 99, 18],
               [106, 5, 120, 18],
               [126, 1, 146, 18],
               [156, 1, 176, 18],
               [186, 1, 206, 18],
               [216, 1, 246, 18]]

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

building_menu_left_panel_zone = [[615, 85, 634, 104],
                                 [615, 112, 634, 132],
                                 [615, 407, 634, 426]]

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
                          [1160, 134, 1266, 156],
                          [1244, 254, 1266, 276],
                          [1244, 469, 1266, 491]]

objects_panel_zone = [[1044, 74, 1175, 96],
                      [1044, 104, 1150, 126],
                      [1160, 104, 1266, 126]]

exploration_panel_zone = [[1044, 74, 1175, 96],
                          [1044, 104, 1066, 126],
                          [1244, 104, 1266, 126]]

create_facility_panel_zone = [[1044, 74, 1185, 96],
                              [1244, 104, 1266, 126],
                              [1244, 469, 1266, 491]]

powers_lower_panel_zone = [[205, 664 + yVar, 263, 685 + yVar],
                           [274, 664 + yVar, 350, 685 + yVar]]

create_city_lower_panel_zone = [[202, 694 + yVar, 260, 715 + yVar],
                                [202, 724 + yVar, 270, 745 + yVar],
                                [355, 603 + yVar, 493, 625 + yVar],
                                [503, 603 + yVar, 641, 625 + yVar],
                                [202, 754 + yVar, 285, 775 + yVar]]

create_army_lower_panel_zone = [[202, 634 + yVar, 300, 655 + yVar]]

population_lower_panel_zone = []

objects_forest_panel_zone = [[1044, 164, 1150, 186],
                             [1160, 164, 1266, 186]]

objects_trees_panel_zone = [[1044, 164, 1150, 186],
                            [1160, 164, 1266, 186]]

realm_leader_panel_zone = [[621, 628 + yVar, 640, 647 + yVar],
                           [621, 775 + yVar, 640, 794 + yVar],
                           [781, 768 + yVar, 846, 790 + yVar],
                           [401, 683 + yVar, 470, 699 + yVar],
                           [401, 702 + yVar, 470, 718 + yVar]]


def level_editor_keys(key_action):
    if game_stats.map_operations:
        if key_action == 119:
            game_stats.pov_pos[1] -= 1
            update_gf_level_editor.update_sprites()
        elif key_action == 115:
            game_stats.pov_pos[1] += 1
            update_gf_level_editor.update_sprites()
        elif key_action == 97:
            game_stats.pov_pos[0] -= 1
            update_gf_level_editor.update_sprites()
        elif key_action == 100:
            game_stats.pov_pos[0] += 1
            update_gf_level_editor.update_sprites()

    ##    print("Key pressed " + str(key_action))
    pass


def level_editor_surface_m1(position):
    button_pressed = False
    ##    print("Success")
    button_numb = 0
    for square in button_zone:
        button_numb += 1
        ##        print("Level editor surface button " + str(button_numb))
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
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
            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                p_funs[button_numb]()
                button_pressed = True
                break

    # Right panel
    if game_stats.level_editor_panel != "":
        square = [1040, 70, 1270, 495]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_pressed = True

            if position[1] >= 354 and position[0] < 1244 and game_stats.level_editor_panel == "powers panel":
                game_stats.white_index = math.floor((position[1] - 354) / 50) + game_stats.power_short_index
                print("white_index - " + str(game_stats.white_index) + " and power_short_index - " + str(
                    game_stats.power_short_index))

                if game_stats.white_index < len(game_stats.editor_powers):
                    game_stats.lower_panel = "powers lower panel"
                    game_stats.powers_l_p_index = int(game_stats.white_index)
                    game_stats.realm_leader_white_line = ""
                    game_stats.realm_leader_traits_index = 0
                    game_stats.picked_leader_trait = ""
                    game_stats.realm_leader_traits_list = []

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

            elif position[1] >= 134 and position[
                0] < 1244 and game_stats.level_editor_panel == "exploration objects panel":
                game_stats.white_index = math.floor((position[1] - 134) / 30)
                if game_stats.white_index + 1 <= len(exploration_catalog.groups_cat[game_stats.object_category]):
                    game_stats.brush = exploration_catalog.groups_cat[game_stats.object_category][
                        game_stats.white_index]

    # Lower panel
    if game_stats.lower_panel != "":
        xVarDic = {"powers lower panel": 0,
                   "create army lower panel": 0,
                   "create city lower panel": 0,
                   "population lower panel": 200}
        yVar = game_stats.game_window_height - 800
        xVar = xVarDic[game_stats.lower_panel]

        # print("game_stats.lower_panel - " + str(game_stats.lower_panel))
        lp_funs = lower_panel_buttons[game_stats.lower_panel]
        lp_button_zone = lower_panel_zone[game_stats.lower_panel]

        button_numb = 0

        for square in lp_button_zone:
            button_numb += 1

            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                lp_funs[button_numb]()
                button_pressed = True
                break

        square = [200 + xVar, 600 + yVar, 1080 - xVar, 800 + yVar]
        if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
            button_pressed = True

        if game_stats.lower_panel == "powers lower panel":
            # print("game_stats.lower_panel = powers lower panel")
            power_option_funs = power_option_buttons[game_stats.power_option_view]
            po_zone = power_option_zone[game_stats.power_option_view]

            button_numb = 0

            for square in po_zone:
                button_numb += 1
                # print("button_numb - " + str(button_numb))

                if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                    power_option_funs[button_numb]()
                    break

            if 646 <= position[0] < 736 and 626 + yVar <= position[1]:
                choose_leader_trait(position, yVar)

        elif game_stats.lower_panel == "create army lower panel":
            if position[1] >= 604 + yVar and position[0] >= 430:
                delete_selected_unit(position)

        elif game_stats.lower_panel == "population lower panel":
            if position[1] >= 634 + yVar and 410 <= position[0] < 500:
                index_number = math.floor((position[1] - (634 + yVar)) / 30)
                if index_number < len(game_stats.lot_information.residency):
                    game_stats.population_l_p_index = int(index_number)

        elif game_stats.lower_panel == "create city lower panel":
            if game_stats.settlement_option_view == "Population":
                if position[1] >= 664 + yVar and 360 <= position[0] < 450:
                    index_number = math.floor((position[1] - (664 + yVar)) / 30)
                    x = int(game_stats.selected_tile[0])
                    y = int(game_stats.selected_tile[1])
                    TileNum = (y - 1) * game_stats.new_level_width + x - 1
                    for city in game_stats.editor_cities:
                        if city.city_id == game_stats.level_map[TileNum].city_id:
                            if index_number < len(city.residency):
                                game_stats.population_l_p_index = int(index_number)
                            break
            elif game_stats.settlement_option_view == "Factions":
                if position[1] >= 664 + yVar and 360 <= position[0] < 620:
                    index_number = math.floor((position[1] - (664 + yVar)) / 30)
                    x = int(game_stats.selected_tile[0])
                    y = int(game_stats.selected_tile[1])
                    TileNum = (y - 1) * game_stats.new_level_width + x - 1
                    for city in game_stats.editor_cities:
                        if city.city_id == game_stats.level_map[TileNum].city_id:
                            if index_number < len(city.factions):
                                game_stats.faction_l_p_index = int(index_number)
                            break

    # Left panel
    if game_stats.level_editor_left_panel != "":
        # print("Left panel")
        left_p_funs = left_panel_buttons[game_stats.level_editor_left_panel]
        left_p_button_zone = left_panel_zone[game_stats.level_editor_left_panel]

        button_numb = 0
        for square in left_p_button_zone:
            button_numb += 1

            if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
                left_p_funs[button_numb]()
                button_pressed = True
                break

        if not button_pressed:
            click_zone = left_panel_click_zone[game_stats.level_editor_left_panel]
            if click_zone[0] < position[0] < click_zone[2] and click_zone[1] < position[1] < click_zone[3]:
                button_pressed = True
                # print("level_editor_left_panel = " + str(game_stats.level_editor_left_panel))

                if game_stats.level_editor_left_panel == "building menu left panel":
                    square2 = [1, 112, 639, 430]
                    if square2[0] < position[0] < square2[2] and square2[1] < position[1] < square2[3]:
                        x_axis, y_axis = position[0], position[1]
                        x_axis -= 5
                        y_axis -= 112
                        if 0 < x_axis % 153 < 143 and 0 < y_axis % 108 < 100:
                            if 73 < y_axis % 108:
                                if x_axis % 153 < 35:
                                    x_axis = math.ceil(x_axis / 153)
                                    y_axis = math.ceil(y_axis / 108)
                                    # Order to build a new structure
                                    for city in game_stats.editor_cities:
                                        if city.city_id == game_stats.selected_city_id:
                                            for plot in city.buildings:
                                                if plot.upgrade is not None:
                                                    if plot.screen_position == [x_axis,
                                                                                y_axis + game_stats.building_row_index]:
                                                        build_structure(city, plot)
                                            break

    # Click on game map
    if not button_pressed:
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
            terrain_brush_click()

            # # Going through every tile in brush depending on it size
            # y_axis = range((game_stats.brush_size - 1) * -1, game_stats.brush_size)
            # for i in y_axis:
            #     x_axis = range((game_stats.brush_size - 1) * -1, game_stats.brush_size)
            #     for j in x_axis:
            #
            #         # Index of selected tile in map list
            #         x2 = int(game_stats.selected_tile[0]) + j
            #         y2 = int(game_stats.selected_tile[1]) + i
            #         TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1
            #
            #         if 0 < x2 <= game_stats.new_level_width:
            #             if 0 < y2 <= game_stats.new_level_height:
            #
            #                 if game_stats.brush in ["Plain", "Northlands"]:
            #                     game_stats.level_map[TileNum].terrain = game_stats.brush
            #                     game_stats.level_map[TileNum].conditions = \
            #                         terrain_catalog.terrain_calendar[game_stats.brush][game_stats.LE_month]
            #
            #                     # Update visuals
            #                     update_gf_level_editor.add_terrain_sprites(TileNum)

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
                    if game_stats.brush in ["Obj - Oak forest", "Obj - Birch forest"]:
                        put_obstacle_forest(x2, y2)

                    elif game_stats.brush in ["Obj - Oak trees", "Obj - Birch trees"]:
                        put_obstacle_trees(x2, y2)

        elif game_stats.edit_instrument == "put exploration object":

            # Index of selected tile in map list
            x2 = int(game_stats.selected_tile[0])
            y2 = int(game_stats.selected_tile[1])
            TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1

            if 0 < x2 <= game_stats.new_level_width:
                if 0 < y2 <= game_stats.new_level_height:
                    print(game_stats.brush)
                    print(game_stats.object_category)
                    # Brush to remove any terrain objects
                    if game_stats.brush == "Remove object":
                        if game_stats.level_map[TileNum].lot is not None:
                            if game_stats.level_map[TileNum].lot != "City":
                                if game_stats.level_map[
                                    TileNum].lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                                    if game_stats.level_map[TileNum].lot.properties.army_id is not None:
                                        for army in game_stats.editor_armies:
                                            if army.army_id == game_stats.level_map[TileNum].lot.properties.army_id:
                                                game_stats.editor_armies.remove(army)
                                                break
                                    game_stats.level_map[TileNum].lot = None
                                    game_stats.level_map[TileNum].travel = True

                    # Exploration objects
                    elif game_stats.brush in exploration_catalog.groups_cat[game_stats.object_category]:
                        if game_stats.level_map[TileNum].lot is None:
                            print("Success")
                            details = exploration_catalog.details_cat[game_stats.object_category][game_stats.brush]
                            game_stats.level_map[TileNum].lot = game_classes.Map_Object([x2, y2],
                                                                                        int(TileNum),
                                                                                        str(game_stats.brush),
                                                                                        str(details[0]),
                                                                                        str(details[1]),
                                                                                        list(details[2]),
                                                                                        game_classes.Object_Properties(
                                                                                            str(details[3]),
                                                                                            str(details[4]),
                                                                                            int(details[5])))

                            if details[1] == "Lair":
                                fill_lair_with_army(game_stats.level_map[TileNum].lot)
                            # print('img/' + game_stats.level_map[
                            #     TileNum].lot.img_path + "oak_summer" + '.png')

                            # Update visuals
                            update_gf_level_editor.add_exploration_sprites(TileNum)

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
                        if game_stats.level_map[TileNum].lot == "City":
                            game_stats.lower_panel = "create city lower panel"
                            game_stats.selected_city_id = int(game_stats.level_map[TileNum].city_id)

                elif game_stats.edit_instrument in ["draw control zone", "remove control zone"]:
                    draw_control_zone()

                elif game_stats.edit_instrument == "create facility":
                    game_stats.level_editor_panel = "create facility panel"

                    game_stats.lower_panel = ""
                    if game_stats.level_map[TileNum].lot is not None:
                        if type(game_stats.level_map[TileNum].lot) != str:
                            # print(game_stats.level_map[TileNum].lot)
                            if game_stats.level_map[TileNum].lot.obj_typ == "Facility":
                                game_stats.lot_information = game_stats.level_map[TileNum].lot
                                game_stats.lower_panel = "population lower panel"
                                game_stats.population_l_p_index = 0


def level_editor_surface_m3(position):
    print("level_editor_surface_m3")


def brush_shape_rectangle():
    game_stats.brush_shape = 1

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def brush_shape_circle():
    game_stats.brush_shape = 2

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def brush_size_1():
    game_stats.brush_size = 1

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def brush_size_2():
    game_stats.brush_size = 2

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def brush_size_3():
    game_stats.brush_size = 3

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def brush_size_4():
    game_stats.brush_size = 4

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def return_to_main_menu_but():
    game_stats.current_screen = "Entrance Menu"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "main_menu_screen"
    game_stats.edit_instrument = ""
    game_stats.selected_tile = []
    game_stats.level_editor_panel = ""
    game_stats.record_text = False

    game_stats.editor_powers = []
    game_stats.editor_cities = []
    game_stats.editor_armies = []
    game_stats.LE_cities_id_counter = 0
    game_stats.LE_army_id_counter = 0
    game_stats.LE_hero_id_counter = 0
    game_stats.LE_population_id_counter = 0
    game_stats.LE_faction_id_counter = 0

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def brush_but():
    game_stats.edit_instrument = "brush"
    game_stats.level_editor_panel = "brush panel"
    game_stats.lower_panel = ""

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def roads_but():
    game_stats.edit_instrument = "road"
    game_stats.level_editor_panel = "roads panel"
    game_stats.lower_panel = ""

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def save_but():
    level_save.save_new_level()
    print("Saved map")
    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


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


def terrain_brush_click():
    tile_list = []
    if game_stats.brush_shape == 1:
        if game_stats.brush_size == 1:
            x2 = int(game_stats.selected_tile[0])
            y2 = int(game_stats.selected_tile[1])
            # TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1
            tile_list.append([x2, y2])

        elif game_stats.brush_size == 2:
            tile_list = algo_circle_range.simple_square_range(game_stats.selected_tile)
            print(tile_list)

        else:
            tile_list = algo_square_range.within_square_range(game_stats.selected_tile, game_stats.brush_size - 1)
            print(tile_list)

    elif game_stats.brush_shape == 2:
        if game_stats.brush_size == 1:
            x2 = int(game_stats.selected_tile[0])
            y2 = int(game_stats.selected_tile[1])
            # TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1
            tile_list.append([x2, y2])

        elif game_stats.brush_size == 2:
            tile_list = algo_circle_range.simple_square_range(game_stats.selected_tile)
            print(tile_list)

        else:
            tile_list = algo_circle_range.within_circle_range(game_stats.selected_tile, game_stats.brush_size - 1)
            print(tile_list)

    for tile in tile_list:
        TileNum = (tile[1] - 1) * game_stats.new_level_width + tile[0] - 1
        if game_stats.brush in ["Plain", "Northlands"]:
            game_stats.level_map[TileNum].terrain = game_stats.brush
            game_stats.level_map[TileNum].conditions = \
                terrain_catalog.terrain_calendar[game_stats.brush][game_stats.LE_month]

            # Update visuals
            update_gf_level_editor.add_terrain_sprites(TileNum)


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

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def city_name_field_enter():
    print("type city name")
    game_stats.input_text = ""
    game_stats.record_text = True
    game_stats.active_city_name_field = True
    game_stats.map_operations = False


def approve_city_name_but():
    game_stats.new_city_name = game_stats.boxed_city_name
    game_stats.boxed_city_name = ""
    game_stats.input_text = ""
    game_stats.record_text = False
    game_stats.active_city_name_field = False
    game_stats.map_operations = True


def cancel_city_name_but():
    game_stats.boxed_city_name = ""
    game_stats.input_text = ""
    game_stats.record_text = False
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
            alignment = alinement_info.alinements_list[game_stats.option_box_alinement_index]
            game_stats.editor_cities.append(game_classes.Settlement([x, y], int(TileNum),
                                                                    int(game_stats.LE_cities_id_counter),
                                                                    str(game_stats.new_city_name),
                                                                    alignment,
                                                                    owner,
                                                                    fill_factions(alignment,
                                                                                  str(game_stats.new_city_name)),
                                                                    create_development_plots(alignment),
                                                                    random.randint(5, 11)))

            fill_effects_and_control(game_stats.LE_cities_id_counter, alignment)

            print("LE_cities_id_counter - " + str(game_stats.LE_cities_id_counter))
            print("alignment - " + str(alignment))

            alin = alinement_info.alinements_list[game_stats.option_box_alinement_index]
            facil = "Settlement"
            # residents = faction_classes.fac_groups_for_pop[alin][facil]
            settlement = None
            for city in game_stats.editor_cities:
                if city.city_id == game_stats.LE_cities_id_counter:
                    settlement = city
                    break
            for pops in faction_classes.fac_groups_for_pop[alin][facil]:
                game_stats.LE_population_id_counter += 1
                population_id = int(game_stats.LE_population_id_counter)
                name = str(pops[0])
                reserve = []
                for res in pops[1]:
                    reserve.append([str(res[0]), int(res[1])])
                settlement.residency.append(faction_classes.Population(int(population_id), str(name)))

                required_faction = faction_classes.pop_membership[name]
                for faction in settlement.factions:
                    if faction.name == required_faction:
                        faction.members.append([int(population_id), str(name), int(TileNum),
                                                str(game_stats.new_city_name)])
                        break

            settlement.control_zone.append(int(TileNum))
            print("control_zone: " + str(settlement.control_zone))

            # game_stats.editor_cities[game_stats.LE_cities_id_counter - 1].residency = residents

            game_stats.selected_city_id = int(game_stats.level_map[TileNum].city_id)

        game_stats.lower_panel = "create city lower panel"
        game_stats.population_l_p_index = 0
        game_stats.settlement_option_view = "Population"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()

    # Update visuals
    update_gf_level_editor.add_settlement_sprites(TileNum)


def fill_effects_and_control(settlement_id, alignment):
    for settlement in game_stats.editor_cities:
        if settlement.city_id == settlement_id:
            effect = starting_settlement_effects.alignment_base_control[alignment]
            # print("effect - " + str(effect))
            settlement.local_effects.append(effect)
            settlement.control.append([str(effect.content[0].realm_type), int(effect.content[0].bonus)])
            break


def fill_factions(alignment, settlement_name):
    create_faction_list = []
    # New settlement needs to be filled with appropriate factions
    for faction_data in faction_classes.fac_groups[alignment]:
        game_stats.LE_faction_id_counter += 1
        faction_id = int(game_stats.LE_faction_id_counter)
        create_faction_list.append(faction_classes.Faction(faction_id, str(faction_data[0]),
                                                           str(faction_data[0]) + " of " + settlement_name,
                                                           int(faction_data[1])))

    return create_faction_list


def create_development_plots(alignment):
    development_plots_list = []
    # New settlement needs to be filled with development plots, where structure would be built
    for plot in settlement_plots.development_plot_groups[alignment]:
        parameters = settlement_structures.structures_groups[alignment][str(plot[0])]
        ef_list = ef_structures.ef_structures_cat[alignment][str(plot[0])]
        recruitment = recruitment_structures.prepare_recruitment(recruitment_structures.structures_groups[alignment]
                                                                 [str(plot[0])])
        existing_structure = None
        next_upgrade = None
        if parameters[5]:
            defences = None
            if parameters[8] is not None:
                defences = str(parameters[8])
            existing_ef_list = ef_structures.ef_structures_cat[alignment][str(plot[0])]
            existing_structure = settlement_structures.Structure(parameters[0],
                                                                 parameters[1],
                                                                 parameters[2],
                                                                 parameters[3],
                                                                 parameters[4],
                                                                 existing_ef_list,
                                                                 recruitment,
                                                                 list(parameters[6]),
                                                                 list(parameters[7]),
                                                                 defences)

            upgrade_name = settlement_structures.new_upgrades_cat[alignment][str(plot[0])]
            upgrade = settlement_structures.structures_groups[alignment][upgrade_name]
            if upgrade is None:
                pass
            else:
                print("Next upgrade is - " + str(upgrade[0]))
                ef_list = ef_structures.ef_structures_cat[alignment][str(plot[0])]
                recruitment = recruitment_structures.prepare_recruitment(recruitment_structures.structures_groups
                                                                         [alignment][str(upgrade[0])])
                # if len(recruitment) > 0:
                #     for recruit in recruitment:
                #         print("Recruitment: " + str(recruit.unit_name) + ", " + str(recruit.hiring_capacity))
                defences = None
                if parameters[8] is not None:
                    defences = str(parameters[8])
                next_upgrade = settlement_structures.Structure(upgrade[0],
                                                               upgrade[1],
                                                               upgrade[2],
                                                               upgrade[3],
                                                               upgrade[4],
                                                               ef_list,
                                                               recruitment,
                                                               list(parameters[6]),
                                                               list(parameters[7]),
                                                               defences)
        else:
            defences = None
            if parameters[8] is not None:
                defences = str(parameters[8])
            next_upgrade = settlement_structures.Structure(parameters[0],
                                                           parameters[1],
                                                           parameters[2],
                                                           parameters[3],
                                                           parameters[4],
                                                           ef_list,
                                                           recruitment,
                                                           list(parameters[6]),
                                                           list(parameters[7]),
                                                           defences)

        development_plots_list.append(game_classes.Development_Plot(list(plot[1]),
                                                                    existing_structure,
                                                                    str(plot[2]),
                                                                    next_upgrade))

    return development_plots_list


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

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def control_zone_but():
    if game_stats.edit_instrument == "create city":
        game_stats.edit_instrument = "draw control zone"
        game_stats.saved_selected_tile = list(game_stats.selected_tile)

        game_stats.last_city_id = game_stats.selected_city_id
    elif game_stats.edit_instrument == "draw control zone":
        game_stats.edit_instrument = "remove control zone"
    else:
        game_stats.edit_instrument = "create city"
        game_stats.selected_tile = list(game_stats.saved_selected_tile)
        game_stats.saved_selected_tile = []

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def buildings_menu_but():
    if game_stats.level_editor_left_panel == "building menu left panel":
        game_stats.level_editor_left_panel = ""
    else:
        game_stats.level_editor_left_panel = "building menu left panel"
        game_stats.building_row_index = 0

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()

    # Update visuals
    update_gf_level_editor.update_building_sprites()


def population_section_but():
    game_stats.population_l_p_index = 0
    game_stats.settlement_option_view = "Population"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def faction_section_but():
    game_stats.faction_l_p_index = 0
    game_stats.settlement_option_view = "Factions"

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def draw_control_zone():
    print("game_stats.edit_instrument == draw_control_zone")
    tile_list = []
    if game_stats.brush_shape == 1:
        if game_stats.brush_size == 1:
            x2 = int(game_stats.selected_tile[0])
            y2 = int(game_stats.selected_tile[1])
            # TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1
            tile_list.append([x2, y2])

        elif game_stats.brush_size == 2:
            tile_list = algo_circle_range.simple_square_range(game_stats.selected_tile)
            print(tile_list)

        else:
            tile_list = algo_square_range.within_square_range(game_stats.selected_tile, game_stats.brush_size - 1)
            print(tile_list)

    elif game_stats.brush_shape == 2:
        if game_stats.brush_size == 1:
            x2 = int(game_stats.selected_tile[0])
            y2 = int(game_stats.selected_tile[1])
            # TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1
            tile_list.append([x2, y2])

        elif game_stats.brush_size == 2:
            tile_list = algo_circle_range.simple_square_range(game_stats.selected_tile)
            print(tile_list)

        else:
            tile_list = algo_circle_range.within_circle_range(game_stats.selected_tile, game_stats.brush_size - 1)
            print(tile_list)

    for tile in tile_list:
        TileNum = (tile[1] - 1) * game_stats.new_level_width + tile[0] - 1
        if game_stats.level_map[TileNum].lot != "City":
            if game_stats.edit_instrument == "draw control zone":
                if game_stats.level_map[TileNum].city_id is None:
                    game_stats.level_map[TileNum].city_id = game_stats.last_city_id
                    focus1 = int(game_stats.level_map[TileNum].city_id)
                    update_property(TileNum, focus1, None)

                    for settlement in game_stats.editor_cities:
                        if settlement.city_id == game_stats.last_city_id:
                            settlement.control_zone.append(int(TileNum))
                            break
                elif game_stats.level_map[TileNum].city_id != game_stats.last_city_id:
                    focus2 = int(game_stats.level_map[TileNum].city_id)
                    game_stats.level_map[TileNum].city_id = game_stats.last_city_id
                    focus1 = int(game_stats.last_city_id)
                    update_property(TileNum, focus1, focus2)

                    for settlement in game_stats.editor_cities:
                        if settlement.city_id == game_stats.last_city_id:
                            settlement.control_zone.append(int(TileNum))
                            break

            elif game_stats.edit_instrument == "remove control zone":
                if game_stats.level_map[TileNum].city_id == game_stats.last_city_id:
                    focus1 = int(game_stats.level_map[TileNum].city_id)
                    game_stats.level_map[TileNum].city_id = None
                    update_property(TileNum, focus1, None)

                    for settlement in game_stats.editor_cities:
                        if settlement.city_id == game_stats.last_city_id:
                            settlement.control_zone.remove(int(TileNum))
                            break


def close_building_menu_left_panel_but():
    game_stats.level_editor_left_panel = ""

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()

    # Update visuals
    game_stats.gf_building_dict = {}


def plot_row_up():
    if game_stats.building_row_index > 0:
        game_stats.building_row_index -= 1


def plot_row_down():
    settlement = None
    for city in game_stats.editor_cities:
        if city.city_id == game_stats.selected_city_id:
            settlement = city
            break

    list_of_rows = []
    for plot in settlement.buildings:
        if int(plot.screen_position[1]) not in list_of_rows:
            list_of_rows.append(int(plot.screen_position[1]))

    max_row = max(list_of_rows)

    if game_stats.building_row_index < max_row - 3:
        game_stats.building_row_index += 1


def build_structure(city, plot):
    plot.status = "Built"
    plot.structure = plot.upgrade
    plot.upgrade = None
    next_upgrade = settlement_structures.new_upgrades_cat[city.alignment][plot.structure.name]
    if plot.structure.defensive_structure is not None:
        settlement_defences.defence_scripts[plot.structure.name](city)
    if next_upgrade is not None:
        parameters = settlement_structures.structures_groups[city.alignment][next_upgrade]
        ef_list = ef_structures.ef_structures_cat[city.alignment][plot.structure.name]
        recruitment = recruitment_structures.prepare_recruitment(
            recruitment_structures.structures_groups[city.alignment]
            [parameters[0]])
        plot.upgrade = settlement_structures.Structure(str(parameters[0]),
                                                       list(parameters[1]),
                                                       str(parameters[2]),
                                                       list(parameters[3]),
                                                       int(parameters[4]),
                                                       list(ef_list),
                                                       recruitment,
                                                       list(parameters[6]),
                                                       list(parameters[7]),
                                                       str(parameters[8]))
    algo_building.update_control(plot.structure, city)

    # Update visuals
    update_gf_level_editor.add_settlement_building_sprites(plot.structure.name, plot.structure.img)


def powers_but():
    game_stats.edit_instrument = ""
    game_stats.level_editor_panel = "powers panel"
    game_stats.lower_panel = ""
    game_stats.power_short_index = 0
    game_stats.white_index = None
    game_stats.option_box_alinement_index = 0

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def country_name_field_enter():
    print("type country name")
    game_stats.input_text = ""
    game_stats.record_text = True
    game_stats.active_country_name_field = True
    game_stats.map_operations = False


def approve_country_name_but():
    game_stats.new_country_name = game_stats.boxed_country_name
    game_stats.boxed_country_name = ""
    game_stats.input_text = ""
    game_stats.record_text = False
    game_stats.active_country_name_field = False
    game_stats.map_operations = True

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def cancel_country_name_but():
    game_stats.boxed_country_name = ""
    game_stats.input_text = ""
    game_stats.record_text = False
    game_stats.active_country_name_field = False
    game_stats.map_operations = True

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def next_alinement_but():
    if game_stats.option_box_alinement_index + 1 == len(alinement_info.alinements_list):
        game_stats.option_box_alinement_index = 0
    else:
        game_stats.option_box_alinement_index += 1

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def prev_first_color_but():
    if game_stats.option_box_first_color_index - 1 < 0:
        game_stats.option_box_first_color_index = len(faction_names.colors_list) - 1
    else:
        game_stats.option_box_first_color_index -= 1

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def next_first_color_but():
    if game_stats.option_box_first_color_index + 1 == len(faction_names.colors_list):
        game_stats.option_box_first_color_index = 0
    else:
        game_stats.option_box_first_color_index += 1

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def prev_second_color_but():
    if game_stats.option_box_second_color_index - 1 < 0:
        game_stats.option_box_second_color_index = len(faction_names.colors_list) - 1
    else:
        game_stats.option_box_second_color_index -= 1

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def next_second_color_but():
    if game_stats.option_box_second_color_index + 1 == len(faction_names.colors_list):
        game_stats.option_box_second_color_index = 0
    else:
        game_stats.option_box_second_color_index += 1

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


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
        alignment = alinement_info.alinements_list[game_stats.option_box_alinement_index]
        print("result - " + str(starting_resources.alignment_resources[alignment]()))
        leader_name = random.choice(realm_leader_names.alignment_leader_names_cat[alignment])
        realm_leader = game_classes.Realm_Leader(leader_name,
                                                 ["Random", "Random"],
                                                 ["Random", "Random"])

        game_stats.editor_powers.append(game_classes.Realm(game_stats.new_country_name,
                                                           faction_names.colors_list[
                                                               game_stats.option_box_first_color_index],
                                                           faction_names.colors_list[
                                                               game_stats.option_box_second_color_index],
                                                           alignment,
                                                           list(starting_resources.alignment_resources[alignment]()),
                                                           realm_leader))
        print("New country has been created")
        game_stats.lower_panel = "powers lower panel"
        game_stats.powers_l_p_index = -1
        game_stats.realm_leader_white_line = ""
        game_stats.realm_leader_traits_index = 0
        game_stats.picked_leader_trait = ""
        game_stats.realm_leader_traits_list = []

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def prev_power_but():
    if len(game_stats.editor_powers) > 3:
        if game_stats.power_short_index == 0:
            game_stats.power_short_index = len(game_stats.editor_powers) - 3
        else:
            game_stats.power_short_index -= 1

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def next_power_but():
    if len(game_stats.editor_powers) > 3:
        if game_stats.power_short_index == len(game_stats.editor_powers) - 3:
            game_stats.power_short_index = 0
        else:
            game_stats.power_short_index += 1

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def delete_country_but():
    del game_stats.editor_powers[game_stats.powers_l_p_index]
    game_stats.power_short_index = 0
    game_stats.white_index = None
    if len(game_stats.editor_powers) == 0:
        game_stats.lower_panel = ""

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract2.ogg")
    click_sound.play()


def switch_playable_but():
    power = game_stats.editor_powers[game_stats.powers_l_p_index]
    if power.playable:
        power.playable = False
    else:
        power.playable = True


def create_army_but():
    game_stats.edit_instrument = "create army"
    game_stats.level_editor_panel = ""
    game_stats.powers_l_p_index = 0
    game_stats.unit_short_index = 0
    game_stats.army_allegiance = "Neutral"
    game_stats.option_box_alinement_index = 0
    game_stats.lower_panel = ""

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


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
                                                              owner,
                                                              random.choice([True, False])))

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

                    print("white_index - " + str(game_stats.white_index) + "; alignment - " + str(alignment) +
                          "; len(units_list) - " + str(len(units_list)))
                    print("Added to army new unit - " + units_list[game_stats.white_index].name)
                    print("Img - " + units_list[game_stats.white_index].img)

                    # Old code
                    # Now instead of copying an unit, a regiment card with minimum necessary information would be
                    # created
                    # army.units.append(copy.deepcopy(units_list[game_stats.white_index]))
                    unit_info = units_list[game_stats.white_index]
                    army.units.append(game_classes.LE_regiment_card(str(unit_info.name),
                                                                    str(unit_info.img_source),
                                                                    str(unit_info.img),
                                                                    int(unit_info.x_offset),
                                                                    int(unit_info.y_offset),
                                                                    int(unit_info.rank)))

                    # for unit in army.units:
                    #     print(str(unit.img))

                    game_basic.establish_leader(focus, "Editor")

                    # Update visuals
                    update_gf_level_editor.add_regiment_sprites(TileNum)

                break


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
                break


def up_unit_scroll_but():
    if game_stats.unit_short_index > 0:
        game_stats.unit_short_index -= 1
    else:
        alignment = str(alinement_info.advanced_alinements_list[game_stats.option_box_alinement_index])
        units_list = list(units_info.LE_units_dict_by_alinement[alignment])
        if len(units_list) > 9:
            game_stats.unit_short_index = len(units_list) - 9


def down_unit_scroll_but():
    alignment = str(alinement_info.advanced_alinements_list[game_stats.option_box_alinement_index])
    units_list = list(units_info.LE_units_dict_by_alinement[alignment])
    if len(units_list) > 9:
        if game_stats.unit_short_index == len(units_list) - 9:
            game_stats.unit_short_index = 0
        else:
            game_stats.unit_short_index += 1


def delete_unit_but():
    if game_stats.delete_option:
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

    game_basic.establish_leader(focus, "Editor")

    # Update visuals
    update_gf_level_editor.add_regiment_sprites(TileNum)


def objects_but():
    game_stats.edit_instrument = "put object"
    game_stats.level_editor_panel = "objects panel"
    game_stats.object_category = ""
    game_stats.brush = ""
    game_stats.lower_panel = ""

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def remove_object_but():
    game_stats.brush = "Remove object"


def forest_category_but():
    game_stats.object_category = "Forest"


def trees_category_but():
    game_stats.object_category = "Trees"


def forest_oak_but():
    game_stats.brush = "Obj - Oak forest"
    print("game_stats.brush = Obj - Oak forest")


def forest_birch_but():
    game_stats.brush = "Obj - Birch forest"
    print("game_stats.brush = Obj - Birch forest")


def trees_oak_but():
    game_stats.brush = "Obj - Oak trees"
    print("game_stats.brush = Obj - Oak trees")


def trees_birch_but():
    game_stats.brush = "Obj - Birch trees"
    print("game_stats.brush = Obj - Birch trees")


def put_obstacle_forest(x2, y2):
    tile_list = []
    if game_stats.brush_shape == 1:
        if game_stats.brush_size == 1:
            # TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1
            tile_list.append([x2, y2])

        elif game_stats.brush_size == 2:
            tile_list = algo_circle_range.simple_square_range(game_stats.selected_tile)
            print(tile_list)

        else:
            tile_list = algo_square_range.within_square_range(game_stats.selected_tile, game_stats.brush_size - 1)
            print(tile_list)

    elif game_stats.brush_shape == 2:
        if game_stats.brush_size == 1:
            # TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1
            tile_list.append([x2, y2])

        elif game_stats.brush_size == 2:
            tile_list = algo_circle_range.simple_square_range(game_stats.selected_tile)
            print(tile_list)

        else:
            tile_list = algo_circle_range.within_circle_range(game_stats.selected_tile, game_stats.brush_size - 1)
            print(tile_list)

    for tile in tile_list:
        TileNum = (tile[1] - 1) * game_stats.new_level_width + tile[0] - 1
        if game_stats.level_map[TileNum].lot is None:
            TileObj = game_stats.level_map[TileNum]
            trees_list = []
            positioning = [[1, 1], [2, 1], [3, 1],
                           [1, 2], [2, 2], [3, 2],
                           [1, 3], [2, 3], [3, 3]]
            number_of_objects = random.randint(5, 7)
            number_variations = objects_img_catalog.object_variations[objects_names[game_stats.brush]]
            # Update visuals
            update_gf_level_editor.add_obstacle_sprites(TileObj,
                                                        objects_names[game_stats.brush],
                                                        "Nature/Trees/")

            for num in range(number_of_objects):
                pos = random.choice(positioning)
                positioning.remove(pos)
                variant = str(random.randint(1, number_variations))

                obj_cal = objects_img_catalog.object_calendar[objects_names[game_stats.brush]]
                season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.LE_month]
                obj_img = game_stats.gf_obstacle_dict[obj_cal[season] + "_0" + variant]

                x_pos = int((48 / 3) * pos[0] + random.randint(-4, 4) - 8)
                y_pos = int((48 / 3) * pos[1] + random.randint(-4, 4) - obj_img.get_height()/2)
                trees_list.append(list([x_pos, y_pos, variant]))
                # print("Height - " + str(obj_img.get_height()) + ", y - " + str(y_pos) + ", pos - " + str(pos))

            sorted_list = sorted(trees_list, key=lambda x: (x[1], x[0]))
            print(sorted_list)

            game_stats.level_map[TileNum].lot = game_classes.Map_Object([x2, y2], int(TileNum),
                                                                        str(objects_names[game_stats.brush]),
                                                                        "Nature/Trees/",
                                                                        "Obstacle",
                                                                        list(sorted_list),
                                                                        None)

            # game_stats.level_map[TileNum].lot = game_classes.Map_Object([x2, y2], int(TileNum),
            #                                                             "Oak", "Nature/Trees/",
            #                                                             "Obstacle",
            #                                                             [[1, 0], [26, 0], [14, 14],
            #                                                              [3, 25], [28, 23]],
            #                                                             None)

            # print('img/' + game_stats.level_map[TileNum].lot.img_path + "oak_summer" + '.png')
            game_stats.level_map[TileNum].travel = False


def put_obstacle_trees(x2, y2):
    tile_list = []
    if game_stats.brush_shape == 1:
        if game_stats.brush_size == 1:
            # TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1
            tile_list.append([x2, y2])

        elif game_stats.brush_size == 2:
            tile_list = algo_circle_range.simple_square_range(game_stats.selected_tile)
            print(tile_list)

        else:
            tile_list = algo_square_range.within_square_range(game_stats.selected_tile, game_stats.brush_size - 1)
            print(tile_list)

    elif game_stats.brush_shape == 2:
        if game_stats.brush_size == 1:
            # TileNum = (y2 - 1) * game_stats.new_level_width + x2 - 1
            tile_list.append([x2, y2])

        elif game_stats.brush_size == 2:
            tile_list = algo_circle_range.simple_square_range(game_stats.selected_tile)
            print(tile_list)

        else:
            tile_list = algo_circle_range.within_circle_range(game_stats.selected_tile, game_stats.brush_size - 1)
            print(tile_list)

    print("tile_list: " + str(tile_list))
    for tile in tile_list:
        TileNum = (tile[1] - 1) * game_stats.new_level_width + tile[0] - 1
        if game_stats.level_map[TileNum].lot is None:
            TileObj = game_stats.level_map[TileNum]
            trees_list = []
            positioning = [[1, 1], [2, 1], [3, 1],
                           [1, 2], [2, 2], [3, 2],
                           [1, 3], [2, 3], [3, 3]]
            number_of_objects = random.randint(2, 3)
            number_variations = objects_img_catalog.object_variations[objects_names[game_stats.brush]]

            # Update visuals
            update_gf_level_editor.add_obstacle_sprites(TileObj,
                                                        objects_names[game_stats.brush],
                                                        "Nature/Trees/")

            for num in range(number_of_objects):
                pos = random.choice(positioning)
                positioning.remove(pos)
                variant = str(random.randint(1, number_variations))

                obj_cal = objects_img_catalog.object_calendar[objects_names[game_stats.brush]]
                season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.LE_month]
                obj_img = game_stats.gf_obstacle_dict[obj_cal[season] + "_0" + variant]

                x_pos = int((48 / 3) * pos[0] + random.randint(-4, 4) - 8)
                y_pos = int((48 / 3) * pos[1] + random.randint(-4, 4) - obj_img.get_height()/2)
                trees_list.append(list([x_pos, y_pos, variant]))

            sorted_list = sorted(trees_list, key=lambda x: (x[1], x[0]))
            print(sorted_list)

            game_stats.level_map[TileNum].lot = game_classes.Map_Object([x2, y2], int(TileNum),
                                                                        str(objects_names[game_stats.brush]),
                                                                        "Nature/Trees/",
                                                                        "Obstacle",
                                                                        list(sorted_list),
                                                                        None)

            # game_stats.level_map[TileNum].lot = game_classes.Map_Object([x2, y2], int(TileNum),
            #                                                             "Oak", "Nature/Trees/",
            #                                                             "Obstacle",
            #                                                             [[6, 22], [24, 6]],
            #                                                             None)
            # print('img/' + game_stats.level_map[TileNum].lot.img_path + "oak_summer" + '.png')
            game_stats.level_map[TileNum].travel = True


def facility_but():
    game_stats.edit_instrument = "create facility"
    game_stats.level_editor_panel = ""
    game_stats.facility_short_index = 0
    game_stats.lower_panel = ""

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


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
                        if TileNum in city.property:
                            # Remove population ID from faction membership lists
                            for pop in game_stats.level_map[TileNum].lot.residency:
                                for faction in city.factions:
                                    pop_number = None
                                    num = 0
                                    for member in faction.members:
                                        if member[0] == pop.population_id:
                                            pop_number = int(num)
                                        num += 1
                                    if pop_number is not None:
                                        del faction.members[pop_number]

                            city.property.remove(TileNum)
                            game_stats.level_map[TileNum].lot = None
                        break


def create_new_facility():
    print("create_new_facility")

    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    if game_stats.level_map[TileNum].lot is None:
        if game_stats.level_map[TileNum].city_id is None:  # territory is without settlement yet
            facil = facility_catalog.LE_facility_list[game_stats.white_index]
            thematic_name = facility_catalog.facility_thematic_name_cat["Neutral"][facil]
            game_stats.level_map[TileNum].lot = game_classes.Facility([x, y], int(TileNum),
                                                                      facil,
                                                                      "Facilities/Neutral/",
                                                                      facility_catalog.LE_facility_img_name_list_neutral[
                                                                          game_stats.white_index],
                                                                      "Facility",
                                                                      [[0, 0]],
                                                                      "Neutral",
                                                                      thematic_name)
        else:  # territory has a settlement
            focus = int(game_stats.level_map[TileNum].city_id)
            for city in game_stats.editor_cities:
                if city.city_id == focus:
                    alin = str(city.alignment)
                    facil = facility_catalog.LE_facility_list[game_stats.white_index]
                    facil_path = facility_catalog.facility_path_cat[alin]
                    facil_name = facility_catalog.facility_img_name_cat[alin][game_stats.white_index]
                    thematic_name = facility_catalog.facility_thematic_name_cat[alin][facil]
                    game_stats.level_map[TileNum].lot = game_classes.Facility([x, y], int(TileNum),
                                                                              facil,
                                                                              facil_path,
                                                                              facil_name,
                                                                              "Facility",
                                                                              [[0, 0]],
                                                                              str(alin),
                                                                              thematic_name)
                    # Register new facility among settlement's property
                    city.property.append(int(TileNum))

                    # Create population
                    # Only works because this tile belong to nearby settlement
                    for pops in faction_classes.fac_groups_for_pop[alin][facil]:
                        game_stats.LE_population_id_counter += 1
                        population_id = int(game_stats.LE_population_id_counter)
                        name = str(pops[0])
                        reserve = []
                        for res in pops[1]:
                            reserve.append([str(res[0]), int(res[1])])
                        game_stats.level_map[TileNum].lot.residency.append(
                            faction_classes.Population(int(population_id), str(name)))
                        # game_stats.level_map[TileNum].lot.residency = (faction_classes.fac_groups_for_pop[alin][facil])

                        # Add population ID to representing faction
                        required_faction = faction_classes.pop_membership[name]
                        for faction in city.factions:
                            if faction.name == required_faction:
                                faction.members.append([int(population_id), str(name), int(TileNum),
                                                        str(thematic_name)])
                                break

                    # Call lower population panel
                    game_stats.lot_information = game_stats.level_map[TileNum].lot
                    game_stats.lower_panel = "population lower panel"
                    game_stats.population_l_p_index = 0

                    break

        # Update facilities
        update_gf_level_editor.add_facility_sprites(TileNum)


def update_property(TileNum, focus1, focus2):
    if game_stats.level_map[TileNum].lot is not None:
        if game_stats.level_map[TileNum].lot != "City":
            if game_stats.level_map[TileNum].lot.obj_typ == "Facility":
                if game_stats.level_map[TileNum].city_id is None:
                    # Facility
                    game_stats.level_map[TileNum].lot.img_path = "Facilities/Neutral/"
                    number = facility_catalog.LE_facility_list.index(game_stats.level_map[TileNum].lot.obj_name)
                    game_stats.level_map[TileNum].lot.img_name = facility_catalog.LE_facility_img_name_list_neutral[
                        number]
                    game_stats.level_map[TileNum].alignment = "Neutral"
                    # Settlement
                    for city in game_stats.editor_cities:
                        if city.city_id == focus1:
                            city.property.remove(int(TileNum))

                            # Remove population ID from faction membership lists
                            for pop in game_stats.level_map[TileNum].lot.residency:
                                for faction in city.factions:
                                    pop_number = None
                                    num = 0
                                    for member in faction.members:
                                        if member[0] == pop.population_id:
                                            pop_number = int(num)
                                        num += 1
                                    if pop_number is not None:
                                        del faction.members[pop_number]

                    # Population
                    game_stats.level_map[TileNum].lot.residency = []
                elif focus2 is None:
                    print("Add neutral facility")
                    for city in game_stats.editor_cities:
                        if city.city_id == focus1:
                            # Facility
                            alin = str(city.alignment)
                            number = facility_catalog.LE_facility_list.index(game_stats.level_map[TileNum].lot.obj_name)
                            game_stats.level_map[TileNum].lot.img_path = facility_catalog.facility_path_cat[alin]
                            game_stats.level_map[TileNum].lot.img_name = facility_catalog.facility_img_name_cat[alin][
                                number]
                            game_stats.level_map[TileNum].alignment = str(alin)

                            # Settlement
                            city.property.append(int(TileNum))

                            # Population
                            game_stats.level_map[TileNum].lot.residency = []
                            facil = game_stats.level_map[TileNum].lot.obj_name

                            for pops in faction_classes.fac_groups_for_pop[alin][facil]:
                                game_stats.LE_population_id_counter += 1
                                population_id = int(game_stats.LE_population_id_counter)
                                name = str(pops[0])
                                reserve = []
                                for res in pops[1]:
                                    reserve.append([str(res[0]), int(res[1])])
                                game_stats.level_map[TileNum].lot.residency.append(
                                    faction_classes.Population(int(population_id), str(name)))

                                # Add population ID to representing faction
                                required_faction = faction_classes.pop_membership[name]
                                print(name + " - " + required_faction)
                                for faction in city.factions:
                                    if faction.name == required_faction:
                                        faction.members.append([int(population_id), str(name), int(TileNum),
                                                                str(game_stats.level_map[TileNum].lot.thematic_name)])
                                        print("Found faction - " + faction.name)
                                        break

                            # game_stats.level_map[TileNum].lot.residency =
                            # faction_classes.fac_groups_for_pop[alin][facil]
                            break

                else:
                    for city in game_stats.editor_cities:
                        if city.city_id == focus1:
                            for old_city in game_stats.editor_cities:
                                if old_city.city_id == focus2:
                                    # Old settlement
                                    old_city.property.remove(int(TileNum))
                                    old_city.control_zone.remove(int(TileNum))

                                    # Remove population ID from faction membership lists
                                    for pop in game_stats.level_map[TileNum].lot.residency:
                                        for faction in old_city.factions:
                                            pop_number = None
                                            num = 0
                                            for member in faction.members:
                                                if member[0] == pop.population_id:
                                                    pop_number = int(num)
                                                num += 1
                                            if pop_number is not None:
                                                del faction.members[pop_number]
                                    break
                            # Facility
                            alin = str(city.alignment)
                            number = facility_catalog.LE_facility_list.index(game_stats.level_map[TileNum].lot.obj_name)
                            game_stats.level_map[TileNum].lot.img_path = facility_catalog.facility_path_cat[alin][
                                number]
                            game_stats.level_map[TileNum].lot.img_name = facility_catalog.facility_img_name_cat[alin][
                                number]
                            game_stats.level_map[TileNum].alignment = str(alin)

                            # Population
                            game_stats.level_map[TileNum].lot.residency = []
                            facil = game_stats.level_map[TileNum].lot.obj_name

                            for pops in faction_classes.fac_groups_for_pop[alin][facil]:
                                game_stats.LE_population_id_counter += 1
                                population_id = int(game_stats.LE_population_id_counter)
                                name = str(pops[0])
                                reserve = []
                                for res in pops[1]:
                                    reserve.append([str(res[0]), int(res[1])])
                                game_stats.level_map[TileNum].lot.residency.append(
                                    faction_classes.Population(int(population_id), str(name)))

                                # Add population ID to representing faction
                                required_faction = faction_classes.pop_membership[name]
                                for faction in city.factions:
                                    if faction.name == required_faction:
                                        faction.members.append([int(population_id), str(name), int(TileNum),
                                                                str(game_stats.level_map[TileNum].lot.thematic_name)])
                                        break

                            # game_stats.level_map[TileNum].lot.residency =
                            # faction_classes.fac_groups_for_pop[alin][facil]

                            # New settlement
                            city.property.append(int(TileNum))
                            break

                # Update facilities
                update_gf_level_editor.add_facility_sprites(TileNum)


def exploration_but():
    game_stats.edit_instrument = "put exploration object"
    game_stats.level_editor_panel = "exploration objects panel"
    game_stats.object_category = exploration_catalog.exploration_objects_groups_cat[0]
    game_stats.brush = exploration_catalog.groups_cat[game_stats.object_category][0]
    game_stats.lower_panel = ""

    click_sound = pygame.mixer.Sound("Sound/Interface/Abstract1.ogg")
    click_sound.play()


def previous_object_group_but():
    group_position = exploration_catalog.exploration_objects_groups_cat.index(game_stats.object_category)
    if group_position == 0:
        length = len(exploration_catalog.exploration_objects_groups_cat)
        game_stats.object_category = exploration_catalog.exploration_objects_groups_cat[length - 1]
    else:
        game_stats.object_category = exploration_catalog.exploration_objects_groups_cat[group_position - 1]

    game_stats.brush = exploration_catalog.groups_cat[game_stats.object_category][0]


def next_object_group_but():
    group_position = exploration_catalog.exploration_objects_groups_cat.index(game_stats.object_category)
    if group_position + 1 == len(exploration_catalog.exploration_objects_groups_cat):
        game_stats.object_category = exploration_catalog.exploration_objects_groups_cat[0]
    else:
        game_stats.object_category = exploration_catalog.exploration_objects_groups_cat[group_position + 1]

    game_stats.brush = exploration_catalog.groups_cat[game_stats.object_category][0]


def fill_lair_with_army(lot):
    x = int(lot.posxy[0])
    y = int(lot.posxy[1])
    TileNum = int(lot.location)

    game_stats.LE_army_id_counter += 1
    game_stats.editor_armies.append(game_classes.Army([x, y], int(TileNum),
                                                      int(game_stats.LE_army_id_counter),
                                                      "Neutral",
                                                      random.choice([True, False])))

    lot.properties.army_id = int(game_stats.LE_army_id_counter)

    for army in game_stats.editor_armies:
        if army.army_id == lot.properties.army_id:
            lair_army_catalog.lair_dictionary[lot.obj_name](army.units)

            break


def choose_leader_trait(position, yVar):
    y_axis = position[1]
    y_axis -= (626 + yVar)
    y_axis = math.ceil(y_axis / 19) - 1
    print(str(y_axis))

    if game_stats.realm_leader_white_line != "":
        if game_stats.realm_leader_traits_index + y_axis + 1 <= len(game_stats.realm_leader_traits_list):
            game_stats.picked_leader_trait = game_stats.realm_leader_traits_list[game_stats.realm_leader_traits_index
                                                                                 + y_axis]


def up_traits_list():
    if game_stats.realm_leader_white_line != "":
        if game_stats.realm_leader_traits_index - 1 >= 0:
            game_stats.realm_leader_traits_index -= 1
        else:
            if len(game_stats.realm_leader_traits_list) <= 9:
                game_stats.realm_leader_traits_index = 0
            else:
                game_stats.realm_leader_traits_index = len(game_stats.realm_leader_traits_list) - 9


def down_traits_list():
    if game_stats.realm_leader_white_line != "":
        if game_stats.realm_leader_traits_index + 1 <= len(game_stats.realm_leader_traits_list) - 9:
            game_stats.realm_leader_traits_index += 1
        else:
            game_stats.realm_leader_traits_index = 0


def assign_leader_trait():
    power = game_stats.editor_powers[game_stats.powers_l_p_index]

    if game_stats.realm_leader_white_line == "First behavior trait":
        power.leader.behavior_traits[0] = str(game_stats.picked_leader_trait)
    elif game_stats.realm_leader_white_line == "Second behavior trait":
        power.leader.behavior_traits[1] = str(game_stats.picked_leader_trait)

    game_stats.realm_leader_white_line = ""
    game_stats.realm_leader_traits_index = 0
    game_stats.picked_leader_trait = ""
    game_stats.realm_leader_traits_list = []


def first_behavior_trait_but():
    power = game_stats.editor_powers[game_stats.powers_l_p_index]

    game_stats.realm_leader_white_line = "First behavior trait"
    game_stats.realm_leader_traits_index = 0

    game_stats.realm_leader_traits_list = list(realm_leader_traits.behavior_traits_list)
    if power.leader.behavior_traits[0] in game_stats.realm_leader_traits_list:
        game_stats.realm_leader_traits_list.remove(power.leader.behavior_traits[0])
    if power.leader.behavior_traits[1] in game_stats.realm_leader_traits_list:
        game_stats.realm_leader_traits_list.remove(power.leader.behavior_traits[1])
    if power.leader.behavior_traits[0] != "Random" and power.leader.behavior_traits[1] != "Random":
        game_stats.realm_leader_traits_list.append("Random")

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


def second_behavior_trait_but():
    power = game_stats.editor_powers[game_stats.powers_l_p_index]

    game_stats.realm_leader_white_line = "Second behavior trait"
    game_stats.realm_leader_traits_index = 0

    game_stats.realm_leader_traits_list = list(realm_leader_traits.behavior_traits_list)
    if power.leader.behavior_traits[0] in game_stats.realm_leader_traits_list:
        game_stats.realm_leader_traits_list.remove(power.leader.behavior_traits[0])
    if power.leader.behavior_traits[1] in game_stats.realm_leader_traits_list:
        game_stats.realm_leader_traits_list.remove(power.leader.behavior_traits[1])
    if power.leader.behavior_traits[0] != "Random" and power.leader.behavior_traits[1] != "Random":
        game_stats.realm_leader_traits_list.append("Random")

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


button_funs = {1: return_to_main_menu_but,
               2: roads_but,
               3: brush_but,
               4: create_army_but,
               5: save_but,
               6: create_city_but,
               7: powers_but,
               8: objects_but,
               9: facility_but,
               10: exploration_but,
               11: brush_shape_rectangle,
               12: brush_shape_circle,
               13: brush_size_1,
               14: brush_size_2,
               15: brush_size_3,
               16: brush_size_4}

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

building_menu_left_panel_funs = {1: close_building_menu_left_panel_but,
                                 2: plot_row_up,
                                 3: plot_row_down}

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
                          6: delete_army_but,
                          7: up_unit_scroll_but,
                          8: down_unit_scroll_but}

objects_panel_funs = {1: remove_object_but,
                      2: forest_category_but,
                      3: trees_category_but}

create_facility_panel_funs = {1: remove_facility_but,
                              2: forest_category_but,
                              3: trees_category_but}

powers_lower_panel_funs = {1: delete_country_but,
                           2: switch_playable_but}

population_lower_panel_funs = {}

create_city_lower_panel_funs = {1: delete_city_but,
                                2: control_zone_but,
                                3: population_section_but,
                                4: faction_section_but,
                                5: buildings_menu_but}

create_army_lower_panel_funs = {1: delete_unit_but}

obj_forest_panel_funs = {1: forest_oak_but,
                         2: forest_birch_but}

obj_trees_panel_funs = {1: trees_oak_but,
                        2: trees_birch_but}

exploration_panel_funs = {1: remove_object_but,
                          2: previous_object_group_but,
                          3: next_object_group_but}

realm_leader_panel_funs = {1: up_traits_list,
                           2: down_traits_list,
                           3: assign_leader_trait,
                           4: first_behavior_trait_but,
                           5: second_behavior_trait_but}

panel_buttons = {"brush panel": brush_panel_funs,
                 "roads panel": roads_panel_funs,
                 "create city panel": create_city_panel_funs,
                 "powers panel": powers_panel_funs,
                 "create army panel": create_army_panel_funs,
                 "objects panel": objects_panel_funs,
                 "create facility panel": create_facility_panel_funs,
                 "exploration objects panel": exploration_panel_funs}

objects_panel_buttons = {"Forest": obj_forest_panel_funs,
                         "Trees": obj_trees_panel_funs}

panel_zone = {"brush panel": brush_panel_zone,
              "roads panel": roads_panel_zone,
              "create city panel": create_city_panel_zone,
              "powers panel": powers_panel_zone,
              "create army panel": create_army_panel_zone,
              "objects panel": objects_panel_zone,
              "create facility panel": create_facility_panel_zone,
              "exploration objects panel": exploration_panel_zone}

lower_panel_buttons = {"powers lower panel": powers_lower_panel_funs,
                       "create city lower panel": create_city_lower_panel_funs,
                       "create army lower panel": create_army_lower_panel_funs,
                       "population lower panel": population_lower_panel_funs}

lower_panel_zone = {"powers lower panel": powers_lower_panel_zone,
                    "create city lower panel": create_city_lower_panel_zone,
                    "create army lower panel": create_army_lower_panel_zone,
                    "population lower panel": population_lower_panel_zone}

power_option_buttons = {"Realm leader": realm_leader_panel_funs}

power_option_zone = {"Realm leader": realm_leader_panel_zone}

left_panel_buttons = {"building menu left panel": building_menu_left_panel_funs}

left_panel_zone = {"building menu left panel": building_menu_left_panel_zone}

objects_panel_zone = {"Forest": objects_forest_panel_zone,
                      "Trees": objects_trees_panel_zone}

exploration_panel_zone = {"Forest": objects_forest_panel_zone,
                          "Trees": objects_trees_panel_zone}

left_panel_click_zone = {"building menu left panel": [1, 80, 639, 430]}


objects_names = {"Obj - Oak forest" : "Oak",
                 "Obj - Birch forest" : "Birch",
                 "Obj - Oak trees" : "Oak",
                 "Obj - Birch trees" : "Birch"}
