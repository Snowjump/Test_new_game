## Among Myth and Wonder
## update_gf_level_editor

import math
import pygame.draw

from Resources import game_stats

from Content import city_catalog
from Content import objects_img_catalog
from Content import terrain_seasons
from Content import exploration_catalog
from Content import new_heroes_catalog
from Content import unit_img_catalog

WhiteColor = (255, 255, 255)


def update_sprites():
    game_stats.gf_terrain_dict = {}
    game_stats.gf_road_dict = {}
    game_stats.gf_settlement_dict = {}
    game_stats.gf_obstacle_dict = {}
    game_stats.gf_facility_dict = {}
    game_stats.gf_exploration_dict = {}
    game_stats.gf_regiment_dict = {}
    game_stats.gf_hero_dict = {}

    for x in range(0, 27):
        for y in range(0, math.ceil(game_stats.game_window_height / 48)):
            num_x = x + game_stats.pov_pos[0]
            num_y = y + game_stats.pov_pos[1]
            if 0 < num_x <= game_stats.new_level_width and 0 < num_y <= game_stats.new_level_height:
                TileNum = (num_y - 1) * game_stats.new_level_width + num_x - 1
                TileObj = game_stats.level_map[TileNum]

                # Terrain
                if TileObj.conditions not in game_stats.gf_terrain_dict:
                    terrain_img = pygame.image.load('img/Terrains/' + TileObj.conditions + '.png').convert()
                    game_stats.gf_terrain_dict[str(TileObj.conditions)] = terrain_img

                # Roads
                if TileObj.road is not None:
                    add_road_centre_sprites(TileNum)
                    if TileObj.road.l_m:
                        add_single_road_sprites(TileNum, "l_m")
                    if TileObj.road.r_m:
                        add_single_road_sprites(TileNum, "r_m")
                    if TileObj.road.m_t:
                        add_single_road_sprites(TileNum, "m_t")
                    if TileObj.road.m_b:
                        add_single_road_sprites(TileNum, "m_b")
                    if TileObj.road.r_t:
                        add_single_road_sprites(TileNum, "r_t")
                    if TileObj.road.l_b:
                        add_single_road_sprites(TileNum, "l_b")
                    if TileObj.road.r_b:
                        add_single_road_sprites(TileNum, "r_b")
                    if TileObj.road.l_t:
                        add_single_road_sprites(TileNum, "l_t")

                # Objects
                # -------
                if TileObj.lot is not None:
                    # Settlements
                    if TileObj.lot == "City":
                        for city in game_stats.editor_cities:
                            if city.city_id == TileObj.city_id:
                                settlement = city_catalog.city_cat[city.alignment]
                                if settlement not in game_stats.gf_settlement_dict:
                                    city_img = pygame.image.load('img/Cities/' +
                                                                 settlement +
                                                                 '.png').convert_alpha()
                                    city_img.set_colorkey(WhiteColor)
                                    game_stats.gf_settlement_dict[str(settlement)] = city_img

                                break
                    else:
                        # Objects
                        # -------
                        # Obstacles
                        if TileObj.lot.obj_typ == "Obstacle":
                            obj_cal = objects_img_catalog.object_calendar[TileObj.lot.obj_name]
                            season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.LE_month]
                            number_variations = objects_img_catalog.object_variations[TileObj.lot.obj_name]
                            for var in range(1, number_variations + 1):
                                # print(obj_cal[season] + " var - " + str(var))
                                if obj_cal[season] + "_0" + str(var) not in game_stats.gf_obstacle_dict:
                                    obj_img = pygame.image.load('img/' +
                                                                TileObj.lot.img_path + obj_cal[season] + "_0" + str(var)
                                                                + '.png').convert_alpha()
                                    obj_img.set_colorkey(WhiteColor)
                                    game_stats.gf_obstacle_dict[str(obj_cal[season] + "_0" + str(var))] = obj_img

                        # Facilities
                        elif TileObj.lot.obj_typ == "Facility":
                            if TileObj.lot.img_path + TileObj.lot.img_name not in game_stats.gf_facility_dict:
                                obj_img = pygame.image.load('img/' +
                                                            TileObj.lot.img_path + TileObj.lot.img_name +
                                                            '.png')
                                obj_img.set_colorkey(WhiteColor)
                                game_stats.gf_facility_dict[str(TileObj.lot.img_path + TileObj.lot.img_name)] = obj_img

                        # Exploration objects
                        elif TileObj.lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                            path_var = TileObj.lot.img_path + TileObj.lot.properties.img_name
                            if path_var not in game_stats.gf_exploration_dict:
                                obj_img = pygame.image.load('img/' + TileObj.lot.img_path +
                                                            TileObj.lot.properties.img_name +
                                                            '.png')
                                obj_img.set_colorkey(WhiteColor)
                                game_stats.gf_exploration_dict[str(path_var)] = obj_img

                # Armies
                if TileObj.army_id is not None:
                    for army in game_stats.editor_armies:
                        if army.army_id == TileObj.army_id:
                            if army.hero is None:
                                if len(army.units) > 0 and army.leader is not None:
                                    unit = army.units[army.leader]
                                    if unit.img_source + "/" + unit.img + "_r" not in game_stats.gf_regiment_dict:
                                        army_img = pygame.image.load(
                                            'img/Creatures/' + str(unit.img_source) + "/" + str(
                                                unit.img) + '_r.png')
                                        army_img.set_colorkey(WhiteColor)
                                        game_stats.gf_regiment_dict[
                                            str(unit.img_source + "/" + unit.img + "_r")] = army_img

                                    if unit.img_source + "/" + unit.img + "_l" not in game_stats.gf_regiment_dict:
                                        army_img = pygame.image.load(
                                            'img/Creatures/' + str(unit.img_source) + "/" + str(
                                                unit.img) + '_l.png')
                                        army_img.set_colorkey(WhiteColor)
                                        game_stats.gf_regiment_dict[
                                            str(unit.img_source + "/" + unit.img + "_l")] = army_img
                            break

    # print(str(game_stats.gf_terrain_dict))


def add_terrain_sprites(TileNum):
    TileObj = game_stats.level_map[TileNum]

    # Terrain
    if TileObj.conditions not in game_stats.gf_terrain_dict:
        terrain_img = pygame.image.load('img/Terrains/' + TileObj.conditions + '.png').convert()
        game_stats.gf_terrain_dict[str(TileObj.conditions)] = terrain_img


def add_road_centre_sprites(TileNum):
    if game_stats.level_map[TileNum].road.material + "_m_m_plains" not in game_stats.gf_road_dict:
        road_img = pygame.image.load(
            'Img/Roads/' + game_stats.level_map[TileNum].road.material + "_m_m_plains" + '.png').convert()
        game_stats.gf_road_dict[str(game_stats.level_map[TileNum].road.material) + "_m_m_plains"] = road_img


def add_road_sprites(first, second):
    if game_stats.level_map[first[0]].road.material + first[1] not in game_stats.gf_road_dict:
        road_img = pygame.image.load(
            'Img/Roads/' + game_stats.level_map[first[0]].road.material + '_' + first[1] + '_plains.png').convert_alpha()
        # road_img.set_colorkey(WhiteColor)
        game_stats.gf_road_dict[str(game_stats.level_map[first[0]].road.material + "_" + first[1] + "_plains")] = road_img

    if game_stats.level_map[second[0]].road.material + second[1] not in game_stats.gf_road_dict:
        road_img = pygame.image.load(
            'Img/Roads/' + game_stats.level_map[second[0]].road.material + '_' + second[1] + '_plains.png').convert_alpha()
        # road_img.set_colorkey(WhiteColor)
        game_stats.gf_road_dict[str(game_stats.level_map[second[0]].road.material + "_" + second[1] + "_plains")] = road_img

    print(str(game_stats.gf_road_dict))


def add_single_road_sprites(TileNum, road):
    if game_stats.level_map[TileNum].road.material + road not in game_stats.gf_road_dict:
        road_img = pygame.image.load(
            'Img/Roads/' + game_stats.level_map[TileNum].road.material + '_' + road + '_plains.png').convert_alpha()
        game_stats.gf_road_dict[str(game_stats.level_map[TileNum].road.material + "_" + road + "_plains")] = road_img


def add_settlement_sprites(TileNum):
    TileObj = game_stats.level_map[TileNum]
    for city in game_stats.editor_cities:
        if city.city_id == TileObj.city_id:
            settlement = city_catalog.city_cat[city.alignment]
            if settlement not in game_stats.gf_settlement_dict:
                city_img = pygame.image.load('img/Cities/' +
                                             settlement +
                                             '.png').convert_alpha()
                city_img.set_colorkey(WhiteColor)
                game_stats.gf_settlement_dict[str(settlement)] = city_img

            break


def add_obstacle_sprites(TileObj, ObjName, ImgPath):
    obj_cal = objects_img_catalog.object_calendar[ObjName]
    season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.LE_month]
    number_variations = objects_img_catalog.object_variations[ObjName]
    for var in range(1, number_variations + 1):
        if obj_cal[season] + "_0" + str(var) not in game_stats.gf_obstacle_dict:
            obj_img = pygame.image.load('img/' +
                                        ImgPath + obj_cal[season] + "_0" + str(var) +
                                        '.png').convert_alpha()
            obj_img.set_colorkey(WhiteColor)
            game_stats.gf_obstacle_dict[str(obj_cal[season] + "_0" + str(var))] = obj_img

    print("gf_obstacle_dict: " + str(game_stats.gf_obstacle_dict))


def add_facility_sprites(TileNum):
    TileObj = game_stats.level_map[TileNum]
    if TileObj.lot.img_path + TileObj.lot.img_name not in game_stats.gf_facility_dict:
        obj_img = pygame.image.load('img/' +
                                    TileObj.lot.img_path + TileObj.lot.img_name +
                                    '.png')
        obj_img.set_colorkey(WhiteColor)
        game_stats.gf_facility_dict[str(TileObj.lot.img_path + TileObj.lot.img_name)] = obj_img


def add_exploration_sprites(TileNum):
    TileObj = game_stats.level_map[TileNum]
    path_var = TileObj.lot.img_path + TileObj.lot.properties.img_name
    if path_var not in game_stats.gf_exploration_dict:
        obj_img = pygame.image.load('img/' + TileObj.lot.img_path +
                                    TileObj.lot.properties.img_name +
                                    '.png')
        obj_img.set_colorkey(WhiteColor)
        game_stats.gf_exploration_dict[str(path_var)] = obj_img


def add_regiment_sprites(TileNum):
    TileObj = game_stats.level_map[TileNum]
    for army in game_stats.editor_armies:
        if army.army_id == TileObj.army_id:
            if army.hero is None:
                if len(army.units) > 0 and army.leader is not None:
                    unit = army.units[army.leader]
                    if unit.img_source + "/" + unit.img + "_r" not in game_stats.gf_regiment_dict:
                        army_img = pygame.image.load(
                            'img/Creatures/' + str(unit.img_source) + '/' + str(unit.img) + '_r.png')
                        army_img.set_colorkey(WhiteColor)
                        game_stats.gf_regiment_dict[str(unit.img_source + "/" + unit.img + "_r")] = army_img

                    if unit.img_source + "/" + unit.img + "_l" not in game_stats.gf_regiment_dict:
                        army_img = pygame.image.load(
                            'img/Creatures/' + str(unit.img_source) + '/' + str(unit.img) + '_l.png')
                        army_img.set_colorkey(WhiteColor)
                        game_stats.gf_regiment_dict[str(unit.img_source + "/" + unit.img + "_l")] = army_img
            break


def update_building_sprites():
    game_stats.gf_building_dict = {}

    settlement = None
    for city in game_stats.editor_cities:
        if city.city_id == game_stats.selected_city_id:
            settlement = city
            break

    for plot in settlement.buildings:
        if plot.structure is not None:
            building_img = pygame.image.load(plot.structure.img).convert_alpha()
            building_img.set_colorkey(WhiteColor)
            game_stats.gf_building_dict[plot.structure.name] = building_img

        if plot.status == "Building" and "Icons/duration_icon" not in game_stats.gf_misc_img_dict:
            misc_img = pygame.image.load('img/Icons/duration_icon.png').convert_alpha()
            misc_img.set_colorkey(WhiteColor)
            game_stats.gf_misc_img_dict["Icons/duration_icon"] = misc_img


def add_settlement_building_sprites(building_name, building_img):
    building_img = pygame.image.load(building_img).convert_alpha()
    building_img.set_colorkey(WhiteColor)
    game_stats.gf_building_dict[building_name] = building_img

    if "Icons/duration_icon" not in game_stats.gf_misc_img_dict:
        misc_img = pygame.image.load('img/Icons/duration_icon.png').convert_alpha()
        misc_img.set_colorkey(WhiteColor)
        game_stats.gf_misc_img_dict["Icons/duration_icon"] = misc_img
