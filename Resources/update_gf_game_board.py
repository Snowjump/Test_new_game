## Among Myth and Wonder
## update_gf_game_board

import math
import pygame.draw

from Resources import game_stats
from Resources import game_obj
from Resources import common_selects

from Content import city_catalog
from Content import objects_img_catalog
from Content import terrain_seasons
from Content import exploration_catalog
from Content import new_heroes_catalog
from Content import unit_img_catalog
from Content import artifact_assortment
from Content import artifact_imgs_cat
from Content import skills_curriculum
from Content import hero_skill_catalog

from Screens.Game_Board_Windows import rw_building

WhiteColor = (255, 255, 255)


def update_misc_sprites():
    game_stats.gf_misc_img_dict = {}

    # Background - grey 32 x 120
    misc_img = pygame.image.load('img/Icons/grey_background_32_120.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/grey_background_32_120"] = misc_img

    # Background - grey 90 x 48
    misc_img = pygame.image.load('img/Icons/grey_background_90_48.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/grey_background_90_48"] = misc_img

    # Background - grey 559 x 32
    misc_img = pygame.image.load('img/Icons/grey_background_559_32.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/grey_background_559_32"] = misc_img

    # Background - light grey 559 x 32
    misc_img = pygame.image.load('img/Icons/light_grey_background_559_32.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/light_grey_background_559_32"] = misc_img

    # Background - grey granite 559 x 30
    misc_img = pygame.image.load('img/Icons/grey_granite_background_559_30.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/grey_granite_background_559_30"] = misc_img

    # Background - matte grey granite 559 x 30
    misc_img = pygame.image.load('img/Icons/matte_grey_granite_background_559_30.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/matte_grey_granite_background_559_30"] = misc_img

    # Background - matte dark-grey granite 559 x 30
    misc_img = pygame.image.load('img/Icons/matte_dark-grey_granite_background_559_30.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/matte_dark-grey_granite_background_559_30"] = misc_img

    # Background - grey 559 x 30
    misc_img = pygame.image.load('img/Icons/grey_background_559_30.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/grey_background_559_30"] = misc_img

    # Icon - hourglass false
    misc_img = pygame.image.load('img/Icons/hourglass_false.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/hourglass_false"] = misc_img

    # Icon - hourglass true
    misc_img = pygame.image.load('img/Icons/hourglass_true.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/hourglass_true"] = misc_img

    # Icon - crown (realm menu)
    misc_img = pygame.image.load('img/Icons/crown.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/crown"] = misc_img

    # Icon - masks (cultures)
    misc_img = pygame.image.load('img/Icons/masks.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/masks"] = misc_img

    # Icon - crown (realm leader)
    misc_img = pygame.image.load('img/Icons/crown_bigger.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/crown_bigger"] = misc_img

    # Icon - new task scroll
    misc_img = pygame.image.load('img/Icons/new_task_scroll.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/new_task_scroll"] = misc_img

    # Icon - old task scroll
    misc_img = pygame.image.load('img/Icons/old_task_scroll.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/old_task_scroll"] = misc_img

    # # Icon - dilemma icon
    # misc_img = pygame.image.load('img/Icons/scales_icon.png').convert_alpha()
    # misc_img.set_colorkey(WhiteColor)
    # game_stats.gf_misc_img_dict["Icons/scales_icon"] = misc_img
    #
    # # Icon - quest icon
    # misc_img = pygame.image.load('img/Icons/wind_rose_icon.png').convert_alpha()
    # misc_img.set_colorkey(WhiteColor)
    # game_stats.gf_misc_img_dict["Icons/wind_rose_icon"] = misc_img

    # Icon - feather and ink (diplomacy)
    misc_img = pygame.image.load('img/Icons/diplomacy.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/diplomacy"] = misc_img

    # Icon - plus points for hero
    misc_img = pygame.image.load('img/Icons/plus_sign_24_2.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/plus_sign_24_2"] = misc_img

    # Icon - accept 14x14
    misc_img = pygame.image.load('img/Icons/accept_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/accept_icon"] = misc_img

    # Icon - cancel 14x14
    misc_img = pygame.image.load('img/Icons/cancel_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/cancel_icon"] = misc_img

    # Icon - ongoing war
    misc_img = pygame.image.load('img/Icons/sword_and_axe_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/sword_and_axe_icon"] = misc_img

    # Icon - ongoing war (smaller)
    misc_img = pygame.image.load('img/Icons/sword_and_axe_icon_14_x_12.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/sword_and_axe_icon_14_x_12"] = misc_img

    # Icon - chevron left
    misc_img = pygame.image.load('img/Icons/chevron_left.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/chevron_left"] = misc_img

    # Icon - chevron right
    misc_img = pygame.image.load('img/Icons/chevron_right.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/chevron_right"] = misc_img

    # Icon - white peace
    misc_img = pygame.image.load('img/Icons/white_peace.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/white_peace"] = misc_img

    # Icon - capitulation
    misc_img = pygame.image.load('img/Icons/capitulation.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/capitulation"] = misc_img

    ## War goals icons
    # Conquest
    misc_img = pygame.image.load('img/Icons/captured_province.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/captured_province"] = misc_img

    # Tribute
    misc_img = pygame.image.load('img/Icons/coins_tribute.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/coins_tribute"] = misc_img

    # Resources icons
    # ---------------
    # Icon - Florins
    misc_img = pygame.image.load('img/Icons/resource_florins.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["resource_florins"] = misc_img

    # Icon - Food
    misc_img = pygame.image.load('img/Icons/resource_food.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["resource_food"] = misc_img

    # Icon - Wood
    misc_img = pygame.image.load('img/Icons/resource_wood.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["resource_wood"] = misc_img

    # Icon - Metals
    misc_img = pygame.image.load('img/Icons/resource_metals.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["resource_metals"] = misc_img

    # Icon - Stone
    misc_img = pygame.image.load('img/Icons/resource_stone.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["resource_stone"] = misc_img

    # Icon - Armament
    misc_img = pygame.image.load('img/Icons/resource_armament.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["resource_armament"] = misc_img

    # Icon - Tools
    misc_img = pygame.image.load('img/Icons/resource_tools.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["resource_tools"] = misc_img

    # Icon - Ingredients
    misc_img = pygame.image.load('img/Icons/resource_ingredients.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["resource_ingredients"] = misc_img

    # Siege icons
    # ---------------
    # Icon - Sledgehammer
    misc_img = pygame.image.load('img/Icons/sledgehammer_icon_18x18.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["sledgehammer_icon_18x18"] = misc_img

    # Icon - Trebuchet
    misc_img = pygame.image.load('img/Icons/siege_trebuchet_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["siege_trebuchet_icon"] = misc_img

    # Icon - Siege tower
    misc_img = pygame.image.load('img/Icons/siege_tower_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["siege_tower_icon"] = misc_img

    # Icon - Battering ram
    misc_img = pygame.image.load('img/Icons/siege_battering_ram_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["siege_battering_ram_icon"] = misc_img

    # Icon - Closed gate
    misc_img = pygame.image.load('img/Icons/castle_gate_closed_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["castle_gate_closed_icon"] = misc_img

    # Icon - Destroyed gate
    misc_img = pygame.image.load('img/Icons/castle_gate_destroyed_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["castle_gate_destroyed_icon"] = misc_img

    # Icon - Opened gate
    misc_img = pygame.image.load('img/Icons/castle_gate_opened_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["castle_gate_opened_icon"] = misc_img

    # Icon - Supplies
    misc_img = pygame.image.load('img/Icons/supplies_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["supplies_icon"] = misc_img

    # Icon - Siege duration
    misc_img = pygame.image.load('img/Icons/duration_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/duration_icon"] = misc_img


def update_sprites():
    game_stats.gf_terrain_dict = {}
    game_stats.gf_road_dict = {}
    game_stats.gf_settlement_dict = {}
    game_stats.gf_obstacle_dict = {}
    game_stats.gf_facility_dict = {}
    game_stats.gf_exploration_dict = {}
    game_stats.gf_regiment_dict = {}
    game_stats.gf_hero_dict = {}

    # Terrain border 48x48
    misc_img = pygame.image.load('img/Terrains/border_48_48_200.png').convert_alpha()
    # misc_img.set_colorkey(WhiteColor)
    game_stats.gf_terrain_dict["Terrains/border_48_48_200"] = misc_img

    for x in range(0, 28):
        for y in range(0, math.ceil(game_stats.game_window_height / 48 + 1)):
            num_x = x + game_stats.pov_pos[0]
            num_y = y + game_stats.pov_pos[1]
            if 0 < num_x <= game_stats.cur_level_width and 0 < num_y <= game_stats.cur_level_height:
                TileNum = (num_y - 1) * game_stats.cur_level_width + num_x - 1
                TileObj = game_obj.game_map[TileNum]

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
                        city = common_selects.select_settlement_by_id(TileObj.city_id)
                        settlement = city_catalog.city_cat[city.alignment]
                        if settlement not in game_stats.gf_settlement_dict:
                            city_img = pygame.image.load('img/Cities/' +
                                                         settlement +
                                                         '.png').convert_alpha()
                            city_img.set_colorkey(WhiteColor)
                            game_stats.gf_settlement_dict[str(settlement)] = city_img

                    else:
                        # Objects
                        # -------
                        # Obstacles
                        if TileObj.lot.obj_typ == "Obstacle":
                            obj_cal = objects_img_catalog.object_calendar[TileObj.lot.obj_name]
                            season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.game_month]
                            number_variations = objects_img_catalog.object_variations[TileObj.lot.obj_name]
                            for var in range(1, number_variations + 1):
                                if obj_cal[season] + "_0" + str(var) not in game_stats.gf_obstacle_dict:
                                    obj_img = pygame.image.load('img/' +
                                                                TileObj.lot.img_path + obj_cal[season] + "_0" + str(var)
                                                                + '.png').convert_alpha()
                                    obj_img.set_colorkey(WhiteColor)
                                    game_stats.gf_obstacle_dict[str(obj_cal[season]) + "_0" + str(var)] = obj_img

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
                    army = common_selects.select_army_by_id(TileObj.army_id)
                    if army.hero is None:
                        unit = army.units[army.leader]
                        # print(game_stats.gf_regiment_dict)
                        if unit.img_source + "/" + unit.img + "_r" not in game_stats.gf_regiment_dict:
                            army_img = pygame.image.load(
                                'img/Creatures/' + str(unit.img_source) + '/' + str(unit.img) + '_r.png')
                            army_img.set_colorkey(WhiteColor)
                            game_stats.gf_regiment_dict[
                                str(unit.img_source + "/" + unit.img + "_r")] = army_img

                        if unit.img_source + "/" + unit.img + "_l" not in game_stats.gf_regiment_dict:
                            army_img = pygame.image.load(
                                'img/Creatures/' + str(unit.img_source) + '/' + str(unit.img) + '_l.png')
                            army_img.set_colorkey(WhiteColor)
                            game_stats.gf_regiment_dict[
                                str(unit.img_source + "/" + unit.img + "_l")] = army_img
                    else:
                        if army.hero.img + "/" + army.hero.img_source + "_r" not in game_stats.gf_hero_dict:
                            army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + '/' +
                                                         str(army.hero.img) + '_r.png')
                            army_img.set_colorkey(WhiteColor)
                            game_stats.gf_hero_dict[
                                str(army.hero.img_source + "/" + army.hero.img + "_r")] = army_img

                        if army.hero.img + "/" + army.hero.img_source + "_l" not in game_stats.gf_hero_dict:
                            army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + '/' +
                                                         str(army.hero.img) + '_l.png')
                            army_img.set_colorkey(WhiteColor)
                            game_stats.gf_hero_dict[
                                str(army.hero.img_source + "/" + army.hero.img + "_l")] = army_img

    update_regiment_sprites()


def update_regiment_sprites():
    # print("update_regiment_sprites()")
    if game_stats.selected_object == "Army":
        army = common_selects.select_army_by_id(game_stats.selected_army)
        for unit in army.units:
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

        # print(game_stats.gf_regiment_dict)

    elif game_stats.selected_object == "Settlement":
        TileObj = None
        settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)
        x2 = int(settlement.posxy[0])
        y2 = int(settlement.posxy[1])
        TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1
        TileObj = game_obj.game_map[TileNum]

        if TileObj.army_id is not None:
            army = common_selects.select_army_by_id(TileObj.army_id)
            for unit in army.units:
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

            # Hero
            if army.hero is not None:
                # print(army.hero.hero_class)
                if army.hero.img + "/" + army.hero.img_source + "_r" not in game_stats.gf_hero_dict:
                    army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + '/' +
                                                 str(army.hero.img) + '_r.png')
                    army_img.set_colorkey(WhiteColor)
                    game_stats.gf_hero_dict[str(army.hero.img_source + "/" + army.hero.img + "_r")] = army_img

                if army.hero.img + "/" + army.hero.img_source + "_l" not in game_stats.gf_hero_dict:
                    army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + '/' +
                                                 str(army.hero.img) + '_l.png')
                    army_img.set_colorkey(WhiteColor)
                    game_stats.gf_hero_dict[str(army.hero.img_source + "/" + army.hero.img + "_l")] = army_img

        if game_stats.settlement_area == "Heroes":
            settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)
            for hero in new_heroes_catalog.heroes_classes_dict_by_alignment[settlement.alignment]:
                hero_info = new_heroes_catalog.heroes_img_dict_by_alignment[settlement.alignment][hero]

                if hero_info[1] + "/" + hero_info[0] + "_r" not in game_stats.gf_hero_dict:
                    army_img = pygame.image.load('img/Heroes/' + str(hero_info[1]) + '/' +
                                                 str(hero_info[0]) + '_r.png')
                    army_img.set_colorkey(WhiteColor)
                    game_stats.gf_hero_dict[str(hero_info[1] + "/" + hero_info[0] + "_r")] = army_img

                if hero_info[1] + "/" + hero_info[0] + "_l" not in game_stats.gf_hero_dict:
                    army_img = pygame.image.load('img/Heroes/' + str(hero_info[1]) + '/' +
                                                 str(hero_info[0]) + '_l.png')
                    army_img.set_colorkey(WhiteColor)
                    game_stats.gf_hero_dict[str(hero_info[1] + "/" + hero_info[0] + "_l")] = army_img

        elif game_stats.settlement_area == "Recruiting":
            settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)
            for plot in settlement.buildings:
                if plot.structure is not None:
                    if len(plot.structure.recruitment) > 0 and plot.status == "Built":
                        for recruit in plot.structure.recruitment:
                            unit_info = unit_img_catalog.units_img_dict_by_alignment[settlement.alignment][
                                recruit.unit_name]

                            if unit_info[1] + "/" + unit_info[0] + "_r" not in game_stats.gf_regiment_dict:
                                army_img = pygame.image.load(
                                    'img/Creatures/' + str(unit_info[1]) + '/' + str(unit_info[0]) + '_r.png')
                                army_img.set_colorkey(WhiteColor)
                                game_stats.gf_regiment_dict[
                                    str(unit_info[1] + "/" + unit_info[0] + "_r")] = army_img

                            if unit_info[1] + "/" + unit_info[0] + "_l" not in game_stats.gf_regiment_dict:
                                army_img = pygame.image.load(
                                    'img/Creatures/' + str(unit_info[1]) + '/' + str(unit_info[0]) + '_l.png')
                                army_img.set_colorkey(WhiteColor)
                                game_stats.gf_regiment_dict[
                                    str(unit_info[1] + "/" + unit_info[0] + "_l")] = army_img

    if game_stats.game_board_panel in ["begin battle panel", "settlement blockade panel"]:
        for army in game_obj.game_armies:
            if army.army_id == game_stats.attacker_army_id or army.army_id == game_stats.defender_army_id:
                for unit in army.units:
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

    elif game_stats.game_board_panel == "army exchange panel":
        army = common_selects.select_army_by_id(game_stats.selected_second_army)
        for unit in army.units:
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

    # If reward contains regiments, load regiment images
    if game_stats.reward_for_demonstration is not None:
        for reward in game_stats.reward_for_demonstration:
            if reward[0] == "Regiment":
                culture = unit_img_catalog.units_img_dict_by_alignment[reward[2]]
                unit_info = culture[reward[1]]
                if unit_info[1] + "/" + unit_info[0] + "_r" not in game_stats.gf_regiment_dict:
                    army_img = pygame.image.load(
                        'img/Creatures/' + str(unit_info[1]) + '/' + str(unit_info[0]) + '_r.png')
                    army_img.set_colorkey(WhiteColor)
                    game_stats.gf_regiment_dict[str(unit_info[1] + "/" + unit_info[0] + "_r")] = army_img
                if unit_info[1] + "/" + unit_info[0] + "_l" not in game_stats.gf_regiment_dict:
                    army_img = pygame.image.load(
                        'img/Creatures/' + str(unit_info[1]) + '/' + str(unit_info[0]) + '_l.png')
                    army_img.set_colorkey(WhiteColor)
                    game_stats.gf_regiment_dict[str(unit_info[1] + "/" + unit_info[0] + "_l")] = army_img


def update_regiment_sprites_from_object(army):
    # print("update_regiment_sprites_from_object()")
    for unit in army.units:
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

    # Hero
    if army.hero is not None:
        print(army.hero.hero_class)
        if army.hero.img + "/" + army.hero.img_source + "_r" not in game_stats.gf_hero_dict:
            army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + '/' +
                                         str(army.hero.img) + '_r.png')
            army_img.set_colorkey(WhiteColor)
            game_stats.gf_hero_dict[str(army.hero.img_source + "/" + army.hero.img + "_r")] = army_img

        if army.hero.img + "/" + army.hero.img_source + "_l" not in game_stats.gf_hero_dict:
            army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + '/' +
                                         str(army.hero.img) + '_l.png')
            army_img.set_colorkey(WhiteColor)
            game_stats.gf_hero_dict[str(army.hero.img_source + "/" + army.hero.img + "_l")] = army_img


def remove_regiment_sprites():
    game_stats.gf_regiment_dict = {}

    for x in range(0, 28):
        for y in range(0, math.ceil(game_stats.game_window_height / 48 + 1)):
            num_x = x + game_stats.pov_pos[0]
            num_y = y + game_stats.pov_pos[1]
            if 0 < num_x <= game_stats.cur_level_width and 0 < num_y <= game_stats.cur_level_height:
                TileNum = (num_y - 1) * game_stats.cur_level_width + num_x - 1
                TileObj = game_obj.game_map[TileNum]

                # Armies
                if TileObj.army_id is not None:
                    army = common_selects.select_army_by_id(TileObj.army_id)
                    if army.hero is None:
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


def remove_hero_sprites():
    game_stats.gf_hero_dict = {}

    for x in range(0, 28):
        for y in range(0, math.ceil(game_stats.game_window_height / 48 + 1)):
            num_x = x + game_stats.pov_pos[0]
            num_y = y + game_stats.pov_pos[1]
            if 0 < num_x <= game_stats.cur_level_width and 0 < num_y <= game_stats.cur_level_height:
                TileNum = (num_y - 1) * game_stats.cur_level_width + num_x - 1
                TileObj = game_obj.game_map[TileNum]

                # Armies
                if TileObj.army_id is not None:
                    army = common_selects.select_army_by_id(TileObj.army_id)
                    if army.hero is not None:
                        if army.hero.img + "/" + army.hero.img_source + "_r" not in game_stats.gf_hero_dict:
                            army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + '/' +
                                                         str(army.hero.img) + '_r.png')
                            army_img.set_colorkey(WhiteColor)
                            game_stats.gf_hero_dict[
                                str(army.hero.img_source + "/" + army.hero.img + "_r")] = army_img

                        if army.hero.img + "/" + army.hero.img_source + "_l" not in game_stats.gf_hero_dict:
                            army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + '/' +
                                                         str(army.hero.img) + '_l.png')
                            army_img.set_colorkey(WhiteColor)
                            game_stats.gf_hero_dict[
                                str(army.hero.img_source + "/" + army.hero.img + "_l")] = army_img


def update_settlement_misc_sprites():
    # Building - settlement interface area
    if "Icons/building_icon" not in game_stats.gf_misc_img_dict:
        misc_img = pygame.image.load('img/Icons/building_icon.png').convert_alpha()
        misc_img.set_colorkey(WhiteColor)
        game_stats.gf_misc_img_dict["Icons/building_icon"] = misc_img

    # Recruiting - settlement interface area
    if "Icons/recruiting_icon" not in game_stats.gf_misc_img_dict:
        misc_img = pygame.image.load('img/Icons/recruiting_icon.png').convert_alpha()
        misc_img.set_colorkey(WhiteColor)
        game_stats.gf_misc_img_dict["Icons/recruiting_icon"] = misc_img

    # Heroes - settlement interface area
    if "Icons/heroes_icon" not in game_stats.gf_misc_img_dict:
        misc_img = pygame.image.load('img/Icons/heroes_icon.png').convert_alpha()
        misc_img.set_colorkey(WhiteColor)
        game_stats.gf_misc_img_dict["Icons/heroes_icon"] = misc_img

    # Economy - settlement interface area
    if "Icons/economy_icon" not in game_stats.gf_misc_img_dict:
        misc_img = pygame.image.load('img/Icons/economy_icon.png').convert_alpha()
        misc_img.set_colorkey(WhiteColor)
        game_stats.gf_misc_img_dict["Icons/economy_icon"] = misc_img

    # Factions - settlement interface area
    if "Icons/factions_icon" not in game_stats.gf_misc_img_dict:
        misc_img = pygame.image.load('img/Icons/factions_icon.png').convert_alpha()
        misc_img.set_colorkey(WhiteColor)
        game_stats.gf_misc_img_dict["Icons/factions_icon"] = misc_img


def remove_settlement_misc_sprites(img_list):
    for img in img_list:
        if img in game_stats.gf_misc_img_dict:
            del game_stats.gf_misc_img_dict[img]

    print(game_stats.gf_misc_img_dict)


def add_misc_sprites(img_list):
    for img in img_list:
        if img not in game_stats.gf_misc_img_dict:
            misc_img = pygame.image.load('img/' + img + '.png').convert_alpha()
            misc_img.set_colorkey(WhiteColor)
            game_stats.gf_misc_img_dict[img] = misc_img


def open_settlement_building_sprites():
    if game_stats.game_board_panel == "settlement panel":
        settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)
        for plot in settlement.buildings:
            if plot.structure is not None:
                building_img = pygame.image.load(plot.structure.img).convert_alpha()
                building_img.set_colorkey(WhiteColor)
                game_stats.gf_building_dict[plot.structure.name] = building_img

            if plot.status == "Building" and "Icons/duration_icon" not in game_stats.gf_misc_img_dict:
                misc_img = pygame.image.load('img/Icons/duration_icon.png').convert_alpha()
                misc_img.set_colorkey(WhiteColor)
                game_stats.gf_misc_img_dict["Icons/duration_icon"] = misc_img

    elif game_stats.game_board_panel == "settlement blockade panel":
        if "Icons/paper_2_square_50_x_40" not in game_stats.gf_misc_img_dict:
            misc_img = pygame.image.load('img/Icons/paper_2_square_50_x_40.png').convert()
            game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"] = misc_img

        settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)
        for plot in settlement.buildings:
            if plot.structure is not None:
                if plot.status == "Built" and plot.structure.defensive_structure is not None:
                    building_img = pygame.image.load(plot.structure.img).convert_alpha()
                    building_img.set_colorkey(WhiteColor)
                    game_stats.gf_building_dict[plot.structure.name] = building_img

                    if "Icons/paper_2_square_50_x_40" not in game_stats.gf_misc_img_dict:
                        misc_img = pygame.image.load('img/Icons/paper_2_square_50_x_40.png').convert()
                        game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"] = misc_img


def add_settlement_building_sprites(building_name, building_img):
    building_img = pygame.image.load(building_img).convert_alpha()
    building_img.set_colorkey(WhiteColor)
    game_stats.gf_building_dict[building_name] = building_img

    if "Icons/duration_icon" not in game_stats.gf_misc_img_dict:
        misc_img = pygame.image.load('img/Icons/duration_icon.png').convert_alpha()
        misc_img.set_colorkey(WhiteColor)
        game_stats.gf_misc_img_dict["Icons/duration_icon"] = misc_img


def update_skills_sprites():
    hero = game_stats.rw_object
    if game_stats.hero_information_option == "Skills":
        for skill in hero.skills:
            if skill.img not in game_stats.gf_skills_dict:
                skill_img = pygame.image.load('Img/Skills/' + skill.img + '.png').convert_alpha()
                skill_img.set_colorkey(WhiteColor)
                game_stats.gf_skills_dict[skill.img] = skill_img

        # print(game_stats.gf_artifact_dict)

    elif game_stats.hero_information_option == "New skills":
        print("Hero new skills: " + str(hero.new_skills))
        for skill in hero.new_skills:
            img = hero_skill_catalog.hero_skill_data[skill][0]
            if img not in game_stats.gf_skills_dict:
                skill_img = pygame.image.load('Img/Skills/' + img + '.png').convert_alpha()
                skill_img.set_colorkey(WhiteColor)
                game_stats.gf_skills_dict[img] = skill_img

    if game_stats.rw_object is not None:
        print("rw_object - " + game_stats.rw_object.name)
        if game_stats.rw_object.name == "KL School of magic":
            name = rw_building.special_structures[game_stats.rw_object.name]
            curriculum = skills_curriculum.curriculum_by_school[name]
            for skill in curriculum:
                skill_name = hero_skill_catalog.hero_skill_data[skill][0]
                skill_img = pygame.image.load('Img/Skills/' + skill_name + '.png').convert_alpha()
                skill_img.set_colorkey(WhiteColor)
                game_stats.gf_skills_dict[skill_name] = skill_img


def update_artifact_sprites():
    print("update_artifact_sprites")
    # print(str(game_stats.rw_object))
    # print(game_stats.rw_object.name)
    hero = game_stats.rw_object
    if game_stats.hero_information_option == "Inventory":
        for artifact in hero.inventory:
            if artifact.img not in game_stats.gf_artifact_dict:
                art_img = pygame.image.load(artifact.img).convert_alpha()
                art_img.set_colorkey(WhiteColor)
                game_stats.gf_artifact_dict[artifact.img] = art_img

        # print(game_stats.gf_artifact_dict)

    if game_stats.hero_inventory is not None:
        for artifact in game_stats.hero_inventory:
            if artifact.img not in game_stats.gf_artifact_dict:
                art_img = pygame.image.load(artifact.img).convert_alpha()
                art_img.set_colorkey(WhiteColor)
                game_stats.gf_artifact_dict[artifact.img] = art_img

    if game_stats.realm_artifact_collection is not None:
        for artifact in game_stats.realm_artifact_collection:
            if artifact.img not in game_stats.gf_artifact_dict:
                art_img = pygame.image.load(artifact.img).convert_alpha()
                art_img.set_colorkey(WhiteColor)
                game_stats.gf_artifact_dict[artifact.img] = art_img

    if game_stats.rw_object is not None:
        print("rw_object - " + game_stats.rw_object.name)
        if game_stats.rw_object.name in ["KL artifact market"]:
            name = rw_building.special_structures[game_stats.rw_object.name]
            assortment = artifact_assortment.stock_by_place[name]
            for artifact in assortment:
                art = artifact_imgs_cat.imgs_catalog[artifact]
                if art not in game_stats.gf_artifact_dict:
                    art_img = pygame.image.load(art).convert_alpha()
                    art_img.set_colorkey(WhiteColor)
                    game_stats.gf_artifact_dict[art] = art_img
            print(game_stats.gf_artifact_dict)


def add_road_centre_sprites(TileNum):
    if game_obj.game_map[TileNum].road.material + "_m_m_plains" not in game_stats.gf_road_dict:
        road_img = pygame.image.load(
            'Img/Roads/' + game_obj.game_map[TileNum].road.material + "_m_m_plains" + '.png').convert()
        game_stats.gf_road_dict[str(game_obj.game_map[TileNum].road.material) + "_m_m_plains"] = road_img


def add_single_road_sprites(TileNum, road):
    if game_obj.game_map[TileNum].road.material + road not in game_stats.gf_road_dict:
        road_img = pygame.image.load(
            'Img/Roads/' + game_obj.game_map[TileNum].road.material + '_' + road + '_plains.png').convert_alpha()
        game_stats.gf_road_dict[str(game_obj.game_map[TileNum].road.material + "_" + road + "_plains")] = road_img
