## Among Myth and Wonder
## le_draw_tiles_funs

import math

from Screens.colors_catalog import *
from Screens.fonts_catalog import *
from Screens.draw_alpha_funs import *

from Resources import game_stats
from Resources import common_selects

from Content import city_catalog
from Content import objects_img_catalog
from Content import terrain_seasons
from Content import exploration_catalog

from Screens.Interface_Elements import flags


def draw_terrain(screen):
    for x in range(0, 28):
        for y in range(0, math.ceil(game_stats.game_window_height / 48) + 1):
            num_x = x + game_stats.pov_pos[0]
            num_y = y + game_stats.pov_pos[1]
            if 0 < num_x <= game_stats.new_level_width and 0 < num_y <= game_stats.new_level_height:
                TileNum = (num_y - 1) * game_stats.new_level_width + num_x - 1
                TileObj = game_stats.level_map[TileNum]

                # Terrain
                terrain_img = game_stats.gf_terrain_dict[TileObj.conditions]
                screen.blit(terrain_img, ((x - 1) * 48, (y - 1) * 48))

                # Roads
                if TileObj.road is not None:
                    draw_road(screen, TileObj, x, y)

                # Border line
                if game_stats.grid_vision:
                    terrain_img = game_stats.gf_terrain_dict["Terrains/border_48_48_250"]
                    screen.blit(terrain_img, ((x - 1) * 48, (y - 1) * 48))


def draw_road(screen, TileObj, x, y):
    # Central piece
    if TileObj.road.material == "Earthen":
        road_central_piece = game_stats.gf_road_dict["Earthen_m_m_plains"]
        screen.blit(road_central_piece, ((x - 1) * 48 + 22, (y - 1) * 48 + 22))
    # West piece
    if TileObj.road.material == "Earthen":
        if TileObj.road.l_m:
            road_l_m_piece = game_stats.gf_road_dict["Earthen_l_m_plains"]
            screen.blit(road_l_m_piece, ((x - 1) * 48 + 1, (y - 1) * 48 + 22))
    # East piece
    if TileObj.road.material == "Earthen":
        if TileObj.road.r_m:
            road_r_m_piece = game_stats.gf_road_dict["Earthen_r_m_plains"]
            screen.blit(road_r_m_piece, ((x - 1) * 48 + 28, (y - 1) * 48 + 22))
    # North piece
    if TileObj.road.material == "Earthen":
        if TileObj.road.m_t:
            road_m_t_piece = game_stats.gf_road_dict["Earthen_m_t_plains"]
            screen.blit(road_m_t_piece, ((x - 1) * 48 + 22, (y - 1) * 48 + 1))
    # South piece
    if TileObj.road.material == "Earthen":
        if TileObj.road.m_b:
            road_m_b_piece = game_stats.gf_road_dict["Earthen_m_b_plains"]
            screen.blit(road_m_b_piece, ((x - 1) * 48 + 22, (y - 1) * 48 + 28))
    # North-east piece
    if TileObj.road.material == "Earthen":
        if TileObj.road.r_t:
            road_r_t_piece = game_stats.gf_road_dict["Earthen_r_t_plains"]
            # road_r_t_piece.set_colorkey(WhiteColor)
            screen.blit(road_r_t_piece, ((x - 1) * 48 + 26, (y - 1) * 48 + 1))
    # South-west piece
    if TileObj.road.material == "Earthen":
        if TileObj.road.l_b:
            road_l_b_piece = game_stats.gf_road_dict["Earthen_l_b_plains"]
            # road_l_b_piece.set_colorkey(WhiteColor)
            screen.blit(road_l_b_piece, ((x - 1) * 48 - 2, (y - 1) * 48 + 26))
    # North-west piece
    if TileObj.road.material == "Earthen":
        if TileObj.road.l_t:
            road_l_t_piece = game_stats.gf_road_dict["Earthen_l_t_plains"]
            # road_l_t_piece.set_colorkey(WhiteColor)
            screen.blit(road_l_t_piece, ((x - 1) * 48 - 2, (y - 1) * 48 + 1))
    # South-east piece
    if TileObj.road.material == "Earthen":
        if TileObj.road.r_b:
            road_r_b_piece = game_stats.gf_road_dict["Earthen_r_b_plains"]
            # road_r_b_piece.set_colorkey(WhiteColor)
            screen.blit(road_r_b_piece, ((x - 1) * 48 + 26, (y - 1) * 48 + 26))


def draw_map_objects(screen):
    for x in range(0, 28):
        for y in range(0, math.ceil(game_stats.game_window_height / 48) + 1):
            num_x = x + game_stats.pov_pos[0]
            num_y = y + game_stats.pov_pos[1]
            if 0 < num_x <= game_stats.new_level_width and 0 < num_y <= game_stats.new_level_height:
                TileNum = (num_y - 1) * game_stats.new_level_width + num_x - 1
                TileObj = game_stats.level_map[TileNum]

                # Cities
                if TileObj.lot is not None:
                    if TileObj.lot == "City":
                        # Cities
                        draw_city(screen, TileObj, x, y)

                    else:
                        # Objects
                        draw_tile_object(screen, TileObj, x, y)

                # Armies
                if TileObj.army_id:
                    # Armies
                    draw_army(screen, TileObj, x, y)


def draw_city(screen, TileObj, x, y):
    city = common_selects.select_settlement_by_id(TileObj.city_id, location="editor_cities")
    city_img = game_stats.gf_settlement_dict[city_catalog.city_cat[city.alignment]]
    screen.blit(city_img, ((x - 1) * 48, (y - 1) * 48))

    # Name
    indent = int(len(city.name) * 2)
    text_panel1 = tnr_font10.render(city.name, True, TitleText)
    screen.blit(text_panel1, ((x - 1) * 48 + 24 - indent, (y - 1) * 48 + 50))

    # Flag
    if city.owner != "Neutral":
        power = common_selects.select_realm_by_name(city.owner, location="editor_powers")
        xb = (x - 1) * 48 + 32
        yb = (y - 1) * 48
        flags.adventure_flag(screen, xb, yb, 0, 0, 0, FlagpoleColor,
                             FlagColors[power.f_color], FlagColors[power.s_color])


def draw_tile_object(screen, TileObj, x, y):
    if TileObj.lot.obj_typ == "Obstacle":
        for item in TileObj.lot.disposition:
            obj_cal = objects_img_catalog.object_calendar[TileObj.lot.obj_name]
            season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.LE_month]
            obj_img = game_stats.gf_obstacle_dict[obj_cal[season] + "_0" + item[2]]
            screen.blit(obj_img, ((x - 1) * 48 + item[0] - obj_img.get_width() / 2,
                                  (y - 1) * 48 + item[1] - obj_img.get_height() / 2))

    elif TileObj.lot.obj_typ == "Facility":
        # if TileObj.city_id is None:
        for item in TileObj.lot.disposition:
            obj_img = game_stats.gf_facility_dict[TileObj.lot.img_path + TileObj.lot.img_name]
            screen.blit(obj_img, ((x - 1) * 48 + item[0], (y - 1) * 48 + item[1]))

    # Exploration objects
    elif TileObj.lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
        for item in TileObj.lot.disposition:
            path_var = TileObj.lot.img_path + TileObj.lot.properties.img_name
            obj_img = game_stats.gf_exploration_dict[path_var]
            screen.blit(obj_img, ((x - 1) * 48 + item[0], (y - 1) * 48 + item[1]))


def draw_army(screen, TileObj, x, y):
    focus = TileObj.army_id
    army = common_selects.select_army_by_id(focus, location="editor_armies")

    if army.hero is None:
        if len(army.units) > 0 and army.leader is not None:
            side = "_l"
            if army.right_side:
                side = "_r"
            unit = army.units[army.leader]
            army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img
                                                   + side]
            screen.blit(army_img, ((x - 1) * 48 + unit.x_offset,
                                   (y - 1) * 48 + unit.y_offset))
        else:
            text_panel1 = tnr_font10.render("No units", True, CancelFieldColor)
            screen.blit(text_panel1, ((x - 1) * 48 + 5, (y - 1) * 48 + 19))

        if army.owner != "Neutral":  # Draw flag
            power = common_selects.select_realm_by_name(army.owner, location="editor_powers")
            xb = (x - 1) * 48
            yb = (y - 1) * 48
            flags.adventure_flag(screen, xb, yb, 0, 0, 0, FlagpoleColor,
                                 FlagColors[power.f_color], FlagColors[power.s_color])


def draw_border(screen):
    if game_stats.border_vision:
        for x in range(0, 28):
            for y in range(0, math.ceil(game_stats.game_window_height / 48) + 1):
                num_x = x + game_stats.pov_pos[0]
                num_y = y + game_stats.pov_pos[1]
                if 0 < num_x <= game_stats.new_level_width and 0 < num_y <= game_stats.new_level_height:
                    TileNum = (num_y - 1) * game_stats.new_level_width + num_x - 1
                    rb = game_stats.LE_borders_map[TileNum]  # rb - realm border
                    # print("TileNum - " + str(TileNum) + "; num_x, num_y - " + str((num_x, num_y)))
                    # print(type(rb))
                    if rb:
                        f_border_color = rb.f_color
                        s_border_color = rb.s_color
                        if rb.nw:
                            xb = (x - 1) * 48
                            xy = (y - 1) * 48
                            draw_line_alpha(screen, f_border_color, (0, 1), (2, 1), 3, (xb, xy))
                            draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb + 3, xy + 3))
                            if not rb.w:
                                draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb, xy + 3))
                            if not rb.n:
                                draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb + 3, xy))
                        if rb.n:
                            xb = (x - 1) * 48 + 3
                            xy = (y - 1) * 48
                            draw_line_alpha(screen, f_border_color, (0, 1), (41, 1), 3, (xb, xy))
                            draw_line_alpha(screen, s_border_color, (0, 1), (35, 1), 3, (xb + 3, xy + 3))
                        if rb.ne:
                            xb = (x - 1) * 48 + 45
                            xy = (y - 1) * 48
                            draw_line_alpha(screen, f_border_color, (0, 1), (2, 1), 3, (xb, xy))
                            draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb - 3, xy + 3))
                            if not rb.e:
                                draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb, xy + 3))
                            if not rb.n:
                                draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb - 3, xy))
                        if rb.e:
                            xb = (x - 1) * 48 + 45
                            xy = (y - 1) * 48 + 3
                            draw_line_alpha(screen, f_border_color, (1, 0), (1, 41), 3, (xb, xy))
                            draw_line_alpha(screen, s_border_color, (1, 0), (1, 35), 3, (xb - 3, xy + 3))
                        if rb.se:
                            xb = (x - 1) * 48 + 45
                            xy = (y - 1) * 48 + 45
                            draw_line_alpha(screen, f_border_color, (0, 1), (2, 1), 3, (xb, xy))
                            draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb - 3, xy - 3))
                            if not rb.e:
                                draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb, xy - 3))
                            if not rb.s:
                                draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb - 3, xy))
                        if rb.s:
                            xb = (x - 1) * 48 + 3
                            xy = (y - 1) * 48 + 45
                            draw_line_alpha(screen, f_border_color, (0, 1), (41, 1), 3, (xb, xy))
                            draw_line_alpha(screen, s_border_color, (0, 1), (35, 1), 3, (xb + 3, xy - 3))
                        if rb.sw:
                            xb = (x - 1) * 48
                            xy = (y - 1) * 48 + 45
                            draw_line_alpha(screen, f_border_color, (0, 1), (2, 1), 3, (xb, xy))
                            draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb + 3, xy - 3))
                            if not rb.w:
                                draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb, xy - 3))
                            if not rb.s:
                                draw_line_alpha(screen, s_border_color, (0, 1), (2, 1), 3, (xb + 3, xy))
                        if rb.w:
                            xb = (x - 1) * 48
                            xy = (y - 1) * 48 + 3
                            draw_line_alpha(screen, f_border_color, (1, 0), (1, 41), 3, (xb, xy))
                            draw_line_alpha(screen, s_border_color, (1, 0), (1, 35), 3, (xb + 3, xy + 3))
