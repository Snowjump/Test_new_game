## Miracle battles!
## sc_game_board

import math
import pygame.transform
import pygame.draw
import pygame.font

from Content import alinement_info
from Content import building_drafts
from Content import city_catalog
from Content import facility_catalog
from Content import objects_img_catalog
from Content import terrain_catalog
from Content import terrain_seasons
from Content import units_info
from Content import exploration_catalog
from Resources import game_obj
from Resources import game_stats
from Screens import draw_movement_arrows
from Screens import anim_army_move
from Screens.Game_Board_Windows import det_settlement_buildings
from Screens.Game_Board_Windows import det_settlement_recruiting
from Screens.Game_Board_Windows import det_settlement_heroes
from Screens.Game_Board_Windows import det_settlement_economy
from Screens.Game_Board_Windows import det_settlement_factions
from Screens.Game_Board_Windows import det_diplomacy
from Screens.Game_Board_Windows import det_quest_log
from Screens.Game_Board_Windows import det_war
from Screens.Game_Board_Windows import rw_upgrade_building
from Screens.Game_Board_Windows import rw_building
from Screens.Game_Board_Windows import rw_new_regiment_information
from Screens.Game_Board_Windows import rw_new_hero_skill_tree
from Screens.Game_Board_Windows import rw_hero_window
from Screens.Game_Board_Windows import win_autobattle_conclusion

# Ask someone how to do it better
from Screens.Panels.Bonus_panels import mythic_monolith_win
from Screens.Panels.Bonus_panels import stone_circle_win
from Screens.Panels.Bonus_panels import scholars_tower_win
from Screens.Panels.Bonus_panels import stone_well_win
from Screens.Panels.Bonus_panels import burial_mound_win
from Screens.Panels.Bonus_panels import anglers_cabin_win
from Screens.Panels.Lair_panels import runaway_serfs_refuge_win
from Screens.Panels.Lair_panels import treasure_tower_win
from Screens.Panels.Lair_panels import lair_of_grey_dragons_win

from Screens.Panels.Result_panels import runaway_serfs_refuge_result_win
from Screens.Panels.Result_panels import treasure_tower_result_win
from Screens.Panels.Result_panels import lair_of_grey_dragons_result_win

from Screens.Panels.Quest_result_panels import poachers_in_royal_forest_result_win
from Screens.Panels.Quest_result_panels import slay_the_grey_dragon_result_win

pygame.init()

WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
MainMenuColorDark1 = [0x8D, 0x87, 0x87]
NewGameColor = [0x8D, 0x86, 0x86]
LineMainMenuColor1 = [0x60, 0x60, 0x60]
Board1 = [0x8A, 0xAA, 0xE5]  # Light blue
Board2 = [0x8A, 0xB9, 0xE5]  # More light blue

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]
SecondaryText = [0xB8, 0xFF, 0x9A]

MaleGender = [0x08, 0x57, 0xA5]
FemaleGender = [0xFA, 0x40, 0x40]

BorderNewGameColor = [0xDA, 0xAE, 0x83]
FillButton = [0xD8, 0xBD, 0xA2]
HighlightBorder = [0xF7, 0x82, 0x0C]
FieldColor = [0xA0, 0xA0, 0xA0]
ApproveFieldColor = [0x00, 0x99, 0x00]
ApproveElementsColor = [0x00, 0x66, 0x00]
CancelFieldColor = [0xFF, 0x00, 0x00]
CancelElementsColor = [0x99, 0x00, 0x00]
BeaverField = [0xA8, 0x94, 0x80]
FieldColor2 = [0xBE, 0xB0, 0xA2]

MapLimitColor = [0x83, 0x62, 0x42]  # DEB887
TileBorder = [11, 11, 11, 200]  # 0x0B, 0x0B, 0x0B
WhiteBorder = [249, 238, 227, 200]
LimeBorder = [51, 255, 51, 200]

UndiscoveredTile = [0x6A, 0x7D, 0x7B]
RockColor = [0x6F, 0x6F, 0x6F]
MonolithColor = [0x14, 0x16, 0x22]
TunelCommonColor = [0x00, 0x51, 0x51]
CaveCommonColor = [0x51, 0x51, 0x00]
PassageColor = [0xFF, 0xFF, 0x99]

RockTunel = [0x89, 0x89, 0x89]
MonolithTunel = [0x24, 0x27, 0x3D]

# Construction icons
TunelIcon = (102, 255, 178, 120)
CaveIcon = (143, 163, 199, 120)
DraftIcon = (255, 128, 0, 160)
FlagpoleColor = (139, 105, 12, 160)

HighlightOption = [0x00, 0xCC, 0xCC]
HighlightRemoval = [0xFF, 0x1A, 0x1A]

ScarletColor = [0xFF, 0x24, 0x00]
CopperColor = [0xE9, 0x75, 0x00]
NightBlueColor = [0x19, 0x2F, 0xF0]
MoonColor = [0xD2, 0xD6, 0xFA]
BullBrownColor = [0x40, 0x21, 0x02]
BlackHoovesColor = [0x0A, 0x06, 0x02]
RoyalPurple = [0x8B, 0x00, 0x8B]
GoldColor = [0xFF, 0xD7, 0x00]
TribesTide = [0x00, 0x64, 0x00]
ForestGreen = [0x22, 0x8B, 0x22]
MaroonColor = [0x80, 0x00, 0x00]
SlateGray = [0x70, 0x80, 0x90]

MatterColors = {"Rock": RockColor,
                "Monolith": MonolithColor}

TunelColors = {"Rock": RockTunel,
               "Monolith": MonolithTunel}

FlagColors = {"Scarlet": ScarletColor,
              "Copper": CopperColor,
              "NightBlue": NightBlueColor,
              "Moon": MoonColor,
              "BullBrown": BullBrownColor,
              "BlackHooves": BlackHoovesColor,
              "RoyalPurple": RoyalPurple,
              "GoldColor": GoldColor,
              "TribesTide": TribesTide,
              "ForestGreen": ForestGreen,
              "MaroonColor": MaroonColor,
              "SlateGray": SlateGray}

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)
font20 = pygame.font.SysFont('timesnewroman', 20)
font16 = pygame.font.SysFont('timesnewroman', 16)
font14 = pygame.font.SysFont('timesnewroman', 14)
font12 = pygame.font.SysFont('timesnewroman', 10)
font8 = pygame.font.SysFont('arial', 8)

arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)

resources_icons = {"Florins": "resource_florins",
                   "Food": "resource_food",
                   "Wood": "resource_wood",
                   "Metals": "resource_metals",
                   "Stone": "resource_stone",
                   "Armament": "resource_armament",
                   "Tools": "resource_tools",
                   "Ingredients": "resource_ingredients"}


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def draw_tiles(screen):
    if len(game_obj.game_map) > 0:
        # Transferred this step to game_basic.prepare_known_map
        # # First step is to find player's realm and copy its discovered map
        # map_to_display = []
        # for power in game_obj.game_powers:
        #     if power.name == game_stats.perspective:
        #         map_to_display = power.known_map

        for x in range(0, 27):
            for y in range(0, math.ceil(game_stats.game_window_height / 48)):
                num_x = x + game_stats.pov_pos[0]
                num_y = y + game_stats.pov_pos[1]
                if 0 < num_x <= game_stats.cur_level_width and 0 < num_y <= game_stats.cur_level_height:
                    TileNum = (num_y - 1) * game_stats.cur_level_width + num_x - 1
                    TileObj = game_obj.game_map[TileNum]

                    # Old code
                    # for TileObj in game_obj.game_map:
                    #     x = TileObj.posxy[0]
                    #     y = TileObj.posxy[1]
                    #     x -= int(game_stats.pov_pos[0])
                    #     y -= int(game_stats.pov_pos[1])
                    #
                    #     if 0 < x <= 27 and 0 < y <= math.ceil(game_stats.game_window_height):

                    # Draw only discovered tiles
                    if [TileObj.posxy[0], TileObj.posxy[1]] in game_stats.map_to_display or \
                            game_stats.display_everything:
                        # New code
                        terrain_img = game_stats.gf_terrain_dict[TileObj.conditions]
                        screen.blit(terrain_img, ((x - 1) * 48, (y - 1) * 48))

                        # Roads
                        if TileObj.road is not None:
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
                                    road_r_t_piece.set_colorkey(WhiteColor)
                                    screen.blit(road_r_t_piece, ((x - 1) * 48 + 26, (y - 1) * 48 + 1))
                            # South-west piece
                            if TileObj.road.material == "Earthen":
                                if TileObj.road.l_b:
                                    road_l_b_piece = game_stats.gf_road_dict["Earthen_l_b_plains"]
                                    road_l_b_piece.set_colorkey(WhiteColor)
                                    screen.blit(road_l_b_piece, ((x - 1) * 48 - 2, (y - 1) * 48 + 26))
                            # North-west piece
                            if TileObj.road.material == "Earthen":
                                if TileObj.road.l_t:
                                    road_l_t_piece = game_stats.gf_road_dict["Earthen_l_t_plains"]
                                    road_l_t_piece.set_colorkey(WhiteColor)
                                    screen.blit(road_l_t_piece, ((x - 1) * 48 - 2, (y - 1) * 48 + 1))
                            # South-east piece
                            if TileObj.road.material == "Earthen":
                                if TileObj.road.r_b:
                                    road_r_b_piece = game_stats.gf_road_dict["Earthen_r_b_plains"]
                                    road_r_b_piece.set_colorkey(WhiteColor)
                                    screen.blit(road_r_b_piece, ((x - 1) * 48 + 26, (y - 1) * 48 + 26))

                        # Border line
                        # pygame.draw.polygon(screen, TileBorder,
                        #                     [[(x - 1) * 48 + 1, (y - 1) * 48 + 1],
                        #                      [(x - 1) * 48 + 48, (y - 1) * 48 + 1],
                        #                      [(x - 1) * 48 + 48, (y - 1) * 48 + 48],
                        #                      [(x - 1) * 48 + 1, (y - 1) * 48 + 48]],
                        #                     1)

                        terrain_img = game_stats.gf_terrain_dict["Terrains/border_48_48_200"]
                        screen.blit(terrain_img, ((x - 1) * 48, (y - 1) * 48))

                    # Draw undiscovered tiles as dark purple tiles
                    elif not game_stats.display_everything:
                        pygame.draw.polygon(screen, UndiscoveredTile,
                                            [[(x - 1) * 48, (y - 1) * 48],
                                             [(x - 1) * 48 + 47, (y - 1) * 48],
                                             [(x - 1) * 48 + 47, (y - 1) * 48 + 47],
                                             [(x - 1) * 48, (y - 1) * 48 + 47]])

        # for TileObj in game_obj.game_map:
        #     x = TileObj.posxy[0]
        #     y = TileObj.posxy[1]
        #     x -= int(game_stats.pov_pos[0])
        #     y -= int(game_stats.pov_pos[1])
        #
        #     if 0 < x <= 27 and 0 < y <= math.ceil(game_stats.game_window_height):
        #
        #         if [TileObj.posxy[0], TileObj.posxy[1]] in game_stats.map_to_display:

        for x in range(0, 27):
            for y in range(0, math.ceil(game_stats.game_window_height / 48)):
                num_x = x + game_stats.pov_pos[0]
                num_y = y + game_stats.pov_pos[1]
                if 0 < num_x <= game_stats.cur_level_width and 0 < num_y <= game_stats.cur_level_height:
                    TileNum = (num_y - 1) * game_stats.cur_level_width + num_x - 1
                    TileObj = game_obj.game_map[TileNum]

                    # Draw only discovered tiles
                    if [TileObj.posxy[0], TileObj.posxy[1]] in game_stats.map_to_display or \
                            game_stats.display_everything:
                        # Cities
                        if TileObj.lot is not None:
                            if TileObj.lot == "City":
                                for city in game_obj.game_cities:
                                    if city.city_id == TileObj.city_id:
                                        # print("City")
                                        # Previous code
                                        # city_img = pygame.image.load('img/Cities/' +
                                        #                              city_catalog.city_cat[city.alignment] +
                                        #                              '.png').convert_alpha()
                                        # city_img.set_colorkey(WhiteColor)
                                        # screen.blit(city_img, ((x - 1) * 48 + 1, (y - 1) * 48 + 1))

                                        # New code
                                        terrain_img = game_stats.gf_settlement_dict[
                                            city_catalog.city_cat[city.alignment]]
                                        screen.blit(terrain_img, ((x - 1) * 48 + 1, (y - 1) * 48 + 1))

                                        # Name
                                        indent = int(len(city.name) * 2)
                                        text_panel1 = font12.render(city.name, True, TitleText)
                                        screen.blit(text_panel1, ((x - 1) * 48 + 24 - indent, (y - 1) * 48 + 50))

                                        # Flag
                                        if city.owner != "Neutral":
                                            for power in game_obj.game_powers:
                                                if city.owner == power.name:
                                                    yc = 0
                                                    if city.military_occupation:
                                                        mo = city.military_occupation
                                                        yc += 5

                                                        # Occupation flag
                                                        xb = (x - 1) * 48
                                                        yb = (y - 1) * 48
                                                        pygame.draw.polygon(screen, FlagpoleColor,
                                                                            ([xb + 3, yb + 34],
                                                                             [xb + 4, yb + 34],
                                                                             [xb + 4, yb + 48],
                                                                             [xb + 3, yb + 48]))
                                                        pygame.draw.polygon(screen, FlagColors[mo[0]],
                                                                            ([xb + 5, yb + 34],
                                                                             [xb + 14, yb + 34],
                                                                             [xb + 14, yb + 37],
                                                                             [xb + 5, yb + 37]))
                                                        pygame.draw.polygon(screen, FlagColors[mo[1]],
                                                                            ([xb + 5, yb + 38],
                                                                             [xb + 14, yb + 38],
                                                                             [xb + 14, yb + 41],
                                                                             [xb + 5, yb + 41]))

                                                    xb = (x - 1) * 48 + 32
                                                    yb = (y - 1) * 48
                                                    pygame.draw.polygon(screen, FlagpoleColor,
                                                                        ([xb + 3, yb + 34],
                                                                         [xb + 4, yb + 34],
                                                                         [xb + 4, yb + 48],
                                                                         [xb + 3, yb + 48]))
                                                    pygame.draw.polygon(screen, FlagColors[power.f_color],
                                                                        ([xb + 5, yb + 34 + yc],
                                                                         [xb + 14, yb + 34 + yc],
                                                                         [xb + 14, yb + 37 + yc],
                                                                         [xb + 5, yb + 37 + yc]))
                                                    pygame.draw.polygon(screen, FlagColors[power.s_color],
                                                                        ([xb + 5, yb + 38 + yc],
                                                                         [xb + 14, yb + 38 + yc],
                                                                         [xb + 14, yb + 41 + yc],
                                                                         [xb + 5, yb + 41 + yc]))
                                        break
                            else:
                                # Objects
                                if TileObj.lot.obj_typ == "Obstacle":
                                    for item in TileObj.lot.disposition:
                                        obj_cal = objects_img_catalog.object_calendar[TileObj.lot.obj_name]
                                        season = terrain_seasons.terrain_calendar[TileObj.terrain][
                                            game_stats.game_month]
                                        obj_img = game_stats.gf_obstacle_dict[obj_cal[season] + "_0" + item[2]]
                                        screen.blit(obj_img, ((x - 1) * 48 + item[0] - obj_img.get_width() / 2,
                                                              (y - 1) * 48 + item[1] - obj_img.get_height() / 2))

                                elif TileObj.lot.obj_typ == "Facility":
                                    # print("Facility - " + str(TileObj.lot.obj_name))
                                    # if TileObj.city_id is None:
                                    # Old code
                                    # for item in TileObj.lot.disposition:
                                    #     obj_img = pygame.image.load('img/' +
                                    #                                 TileObj.lot.img_path + TileObj.lot.img_name +
                                    #                                 '.png')
                                    #     obj_img.set_colorkey(WhiteColor)
                                    #     screen.blit(obj_img, ((x - 1) * 48 + item[0], (y - 1) * 48 + item[1]))

                                    # New code
                                    obj_img = game_stats.gf_facility_dict[TileObj.lot.img_path + TileObj.lot.img_name]
                                    screen.blit(obj_img, ((x - 1) * 48,
                                                          (y - 1) * 48))

                                # Exploration objects
                                elif TileObj.lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                                    # Old code
                                    # for item in TileObj.lot.disposition:
                                    #     obj_img = pygame.image.load('img/' + TileObj.lot.img_path +
                                    #                                 TileObj.lot.properties.img_name +
                                    #                                 '.png')
                                    #     obj_img.set_colorkey(WhiteColor)
                                    #     screen.blit(obj_img, ((x - 1) * 48 + item[0], (y - 1) * 48 + item[1]))

                                    # New code
                                    path_var = TileObj.lot.img_path + TileObj.lot.properties.img_name
                                    obj_img = game_stats.gf_exploration_dict[path_var]
                                    screen.blit(obj_img, ((x - 1) * 48 + TileObj.lot.disposition[0][0],
                                                          (y - 1) * 48 + TileObj.lot.disposition[0][1]))

                        # Armies
                        if TileObj.army_id is not None:
                            focus = TileObj.army_id
                            # print(TileObj.army_id)

                            for army in game_obj.game_armies:
                                if army.army_id == focus:

                                    if len(army.units) > 0 and army.leader is not None:
                                        xy_animation = [0, 0]
                                        if army.action in ["Move", "Routing"]:
                                            xy_animation = anim_army_move.army_march(army.route[0], army.posxy)

                                        side = "_l"
                                        if army.right_side:
                                            side = "_r"

                                        if army.hero is None:
                                            unit = army.units[army.leader]
                                            # print('img/Creatures/' +str(unit.img_source) + str(unit.img) + '.png')
                                            # Old code
                                            # army_img = pygame.image.load(
                                            #     'img/Creatures/' + str(unit.img_source) + "/" + str(unit.img) + '.png')
                                            # army_img.set_colorkey(WhiteColor)

                                            # New code
                                            if unit.img_width > 44 or unit.img_height > 44:
                                                army_img = game_stats.gf_regiment_dict[unit.img_source + "/"
                                                                                       + unit.img + side]
                                                if unit.img_width > 44:
                                                    proportion = 44 / unit.img_width
                                                    army_img = pygame.transform.scale(army_img,
                                                                                      (44,
                                                                                       int(unit.img_height * proportion)))
                                                    x_offset = 3
                                                    y_offset = (48 - (unit.img_height * proportion)) / 2
                                                else:
                                                    proportion = 44 / unit.img_height
                                                    army_img = pygame.transform.scale(army_img,
                                                                                      (int(unit.img_width * proportion),
                                                                                       44))
                                                    x_offset = (48 - (unit.img_width * proportion)) / 2
                                                    y_offset = 3
                                            else:
                                                army_img = game_stats.gf_regiment_dict[unit.img_source + "/"
                                                                                       + unit.img + side]
                                                x_offset = unit.x_offset
                                                y_offset = unit.y_offset
                                        else:
                                            img = army.hero.img
                                            source = army.hero.img_source
                                            # Old code
                                            # army_img = pygame.image.load(
                                            #     'img/Heroes/' + str(source) + "/" + str(img) + '.png')
                                            # army_img.set_colorkey(WhiteColor)

                                            # New code
                                            army_img = game_stats.gf_hero_dict[source + "/" + img + side]
                                            x_offset = army.hero.x_offset
                                            y_offset = army.hero.y_offset

                                        screen.blit(army_img,
                                                    ((x - 1) * 48 + x_offset + xy_animation[0],
                                                     (y - 1) * 48 + y_offset + xy_animation[1]))

                                    if army.owner != "Neutral":  # Draw flag
                                        for power in game_obj.game_powers:
                                            if army.owner == power.name:
                                                pygame.draw.polygon(screen, FlagpoleColor,
                                                                    ([(x - 1) * 48 + 3 + xy_animation[0],
                                                                      (y - 1) * 48 + 34 + xy_animation[1]],
                                                                     [(x - 1) * 48 + 4 + xy_animation[0],
                                                                      (y - 1) * 48 + 34 + xy_animation[1]],
                                                                     [(x - 1) * 48 + 4 + xy_animation[0],
                                                                      (y - 1) * 48 + 48 + xy_animation[1]],
                                                                     [(x - 1) * 48 + 3 + xy_animation[0],
                                                                      (y - 1) * 48 + 48 + xy_animation[1]]))
                                                pygame.draw.polygon(screen, FlagColors[power.f_color],
                                                                    ([(x - 1) * 48 + 5 + xy_animation[0],
                                                                      (y - 1) * 48 + 34 + xy_animation[1]],
                                                                     [(x - 1) * 48 + 14 + xy_animation[0],
                                                                      (y - 1) * 48 + 34 + xy_animation[1]],
                                                                     [(x - 1) * 48 + 14 + xy_animation[0],
                                                                      (y - 1) * 48 + 37 + xy_animation[1]],
                                                                     [(x - 1) * 48 + 5 + xy_animation[0],
                                                                      (y - 1) * 48 + 37 + xy_animation[1]]))
                                                pygame.draw.polygon(screen, FlagColors[power.s_color],
                                                                    ([(x - 1) * 48 + 5 + xy_animation[0],
                                                                      (y - 1) * 48 + 38 + xy_animation[1]],
                                                                     [(x - 1) * 48 + 14 + xy_animation[0],
                                                                      (y - 1) * 48 + 38 + xy_animation[1]],
                                                                     [(x - 1) * 48 + 14 + xy_animation[0],
                                                                      (y - 1) * 48 + 41 + xy_animation[1]],
                                                                     [(x - 1) * 48 + 5 + xy_animation[0],
                                                                      (y - 1) * 48 + 41 + xy_animation[1]]))
                                    break

                    # # Draw undiscovered tiles as dark purple tiles
                    # else:
                    #     pygame.draw.polygon(screen, UndiscoveredTile,
                    #                         [[(x - 1) * 48 + 1, (y - 1) * 48 + 1],
                    #                          [(x - 1) * 48 + 48, (y - 1) * 48 + 1],
                    #                          [(x - 1) * 48 + 48, (y - 1) * 48 + 48],
                    #                          [(x - 1) * 48 + 1, (y - 1) * 48 + 48]])


def details_panel(screen):
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 600 + yVar], [1080, 600 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    for fac in game_obj.game_factions:
        if fac.name == game_stats.location_factions[game_stats.faction_num]:
            id_var = game_stats.pop_in_location[game_stats.white_index]  # Selected character index

            for pop in fac.population:
                if pop.personal_id == id_var:
                    # Character's name
                    text_panel = font20.render(pop.name, True, TitleText)
                    screen.blit(text_panel, [210, 604 + yVar])

                    # Occupation
                    text_panel = font20.render(pop.occupation, True, TitleText)
                    screen.blit(text_panel, [310, 604 + yVar])

                    # Gender
                    if pop.gender == "Male":
                        color = MaleGender
                    else:
                        color = FemaleGender
                    text_panel = font20.render(pop.gender[0:1], True, color)
                    screen.blit(text_panel, [210, 634 + yVar])

                    # Race
                    text_panel = font20.render(pop.race, True, TitleText)
                    screen.blit(text_panel, [230, 634 + yVar])

                    # Inventory
                    text_panel = font20.render("Inventory", True, TitleText)
                    screen.blit(text_panel, [450, 604 + yVar])

                    if len(pop.inventory) > 0:
                        shelf = []
                        for resource in pop.inventory:
                            if len(shelf) == 0:
                                shelf.append([resource, 1])
                            else:
                                check = True
                                for item in shelf:
                                    if item[0] == resource:
                                        item[1] += 1
                                        check = False
                                if check:
                                    shelf.append([resource, 1])

                        number = 0
                        if len(shelf) > 0:
                            for resource in shelf:
                                number += 1
                                text_panel = font20.render(str(resource[1]) + " X " + str(resource[0]), True, TitleText)
                                screen.blit(text_panel,
                                            [450 + math.floor(number / 6) * 120, 634 + (number - 1) % 6 * 30 + yVar])

                    # Highlight destination tile
                    if pop.goal is not None:
                        x2 = int(pop.goal.destination[0])
                        y2 = int(pop.goal.destination[1])
                        x2 -= int(game_stats.pov_pos[0])
                        y2 -= int(game_stats.pov_pos[1])

                        pygame.draw.polygon(screen, LimeBorder,
                                            [[(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 1],
                                             [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 1],
                                             [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 48],
                                             [(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 48]], 1)


def terrain_panel(screen, TileNum, xy_pos):
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 600 + yVar], [1080, 600 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    # Natural feature
    if game_obj.game_map[TileNum - 1].natural_feature is not None:
        text_panel = font20.render(game_obj.game_map[TileNum - 1].natural_feature.name, True, TitleText)
        screen.blit(text_panel, [210, 694 + yVar])


def building_panel(screen, TileNum, xy_pos):
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 600 + yVar], [1080, 600 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    # No building in selected tile
    if game_obj.game_map[TileNum - 1].lot is None:
        text_panel = font20.render("No buildings", True, TitleText)
        screen.blit(text_panel, [210, 604 + yVar])
    else:
        # Construction site exist in selected tile
        if game_obj.game_map[TileNum - 1].lot.structure_type == "con_site":
            text_panel = font20.render(game_obj.game_map[TileNum - 1].lot.name + " is under construction", True,
                                       TitleText)
            screen.blit(text_panel, [210, 604 + yVar])


def begin_battle_panel(screen):
    pygame.draw.polygon(screen, Board1, [[380, 100], [900, 100], [900, 440], [380, 440]])

    pygame.draw.polygon(screen, Board2, [[388, 196], [637, 196], [637, 432], [388, 432]])
    pygame.draw.polygon(screen, Board2, [[643, 196], [892, 196], [892, 432], [643, 432]])

    # Battle title
    if game_stats.battle_type == "Battle":
        end_part = str(game_stats.defender_realm)
        if game_stats.defender_realm == "Neutral":
            end_part = "neutral army"
        title_text = game_stats.attacker_realm + " attack on " + end_part
        text_panel1 = font20.render(title_text, True, TitleText)
        screen.blit(text_panel1, [550 - len(title_text), 103])

    # Button - play battle
    pygame.draw.polygon(screen, FillButton, [[590, 138], [690, 138], [690, 160], [590, 160]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[590, 138], [690, 138], [690, 160], [590, 160]], 3)
    text_panel5 = font20.render("Play battle", True, DarkText)
    screen.blit(text_panel5, [595, 138])

    # Button - autobattle
    pygame.draw.polygon(screen, FillButton, [[590, 168], [690, 168], [690, 190], [590, 190]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[590, 168], [690, 168], [690, 190], [590, 190]], 3)
    text_panel5 = font20.render("Autobattle", True, DarkText)
    screen.blit(text_panel5, [597, 168])

    # Display units
    for army in game_obj.game_armies:
        if army.army_id == game_stats.attacker_army_id:  # Attacker
            # Units
            if len(army.units) > 0:
                number = 0
                for unit in army.units:
                    x_pos = 388 + math.floor(number % 5) * 50 - 2
                    y_pos = 198 + math.floor(number / 5) * 55

                    # Previous code
                    # army_img = pygame.image.load(
                    #     'img/Creatures/' + str(unit.img_source) + "/" + str(unit.img) + '.png')
                    # army_img.set_colorkey(WhiteColor)

                    # New code
                    if unit.crew[0].img_width > 44 or unit.crew[0].img_height > 44:
                        army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                        if unit.crew[0].img_width > 44:
                            proportion = 44 / unit.crew[0].img_width
                            army_img = pygame.transform.scale(army_img,
                                                              (44,
                                                               int(unit.crew[0].img_height * proportion)))
                            x_offset = 3
                            y_offset = (48 - (unit.crew[0].img_height * proportion)) / 2
                        else:
                            proportion = 44 / unit.crew[0].img_height
                            army_img = pygame.transform.scale(army_img,
                                                              (int(unit.crew[0].img_width * proportion),
                                                               44))
                            x_offset = (48 - (unit.crew[0].img_width * proportion)) / 2
                            y_offset = 3
                    else:
                        army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                        x_offset = unit.x_offset
                        y_offset = unit.y_offset

                    screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])

                    # army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                    # screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

                    # Number of creatures
                    number_of_creatures = str(len(unit.crew)) + "/" + str(unit.rows * unit.number)
                    text_panel = arial_font14.render(number_of_creatures, True, DarkText)
                    screen.blit(text_panel, [x_pos + 10, y_pos + 42])

                    number += 1

        elif army.army_id == game_stats.defender_army_id:  # Defender
            # Units
            if len(army.units) > 0:
                number = 0
                for unit in army.units:
                    x_pos = 643 + math.floor(number % 5) * 50 - 2
                    y_pos = 198 + math.floor(number / 5) * 55

                    # Previous code
                    # army_img = pygame.image.load(
                    #     'img/Creatures/' + str(unit.img_source) + "/" + str(unit.img) + '.png')
                    # army_img.set_colorkey(WhiteColor)

                    # New code
                    if unit.crew[0].img_width > 44 or unit.crew[0].img_height > 44:
                        army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                        if unit.crew[0].img_width > 44:
                            proportion = 44 / unit.crew[0].img_width
                            army_img = pygame.transform.scale(army_img,
                                                              (44,
                                                               int(unit.crew[0].img_height * proportion)))
                            x_offset = 3
                            y_offset = (48 - (unit.crew[0].img_height * proportion)) / 2
                        else:
                            proportion = 44 / unit.crew[0].img_height
                            army_img = pygame.transform.scale(army_img,
                                                              (int(unit.crew[0].img_width * proportion),
                                                               44))
                            x_offset = (48 - (unit.crew[0].img_width * proportion)) / 2
                            y_offset = 3
                    else:
                        army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_l"]
                        x_offset = unit.x_offset
                        y_offset = unit.y_offset

                    screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])

                    # army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_l"]
                    # screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

                    # Number of creatures
                    number_of_creatures = str(len(unit.crew)) + "/" + str(unit.rows * unit.number)
                    text_panel = arial_font14.render(number_of_creatures, True, DarkText)
                    screen.blit(text_panel, [x_pos + 10, y_pos + 42])

                    number += 1


def settlement_blockade_panel(screen):
    the_settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            the_settlement = city
            break
    pygame.draw.polygon(screen, Board1, [[121, 70], [1159, 70], [1159, 500], [121, 500]])

    pygame.draw.polygon(screen, Board2, [[128, 336], [637, 336], [637, 490], [128, 490]])
    pygame.draw.polygon(screen, Board2, [[643, 336], [1152, 336], [1152, 490], [643, 490]])

    pygame.draw.polygon(screen, Board2, [[811, 120], [1152, 120], [1152, 298], [811, 298]])

    # Battle title
    title_text = "Blockade of " + game_stats.blockaded_settlement_name
    text_panel1 = font20.render(title_text, True, TitleText)
    screen.blit(text_panel1, [575 - len(title_text), 73])

    # Close settlement siege window
    if game_stats.besieged_by_human or (not game_stats.besieged_by_human and not game_stats.siege_assault):
        pygame.draw.polygon(screen, CancelFieldColor, [[1135, 75], [1154, 75], [1154, 94], [1135, 94]])
        pygame.draw.polygon(screen, CancelElementsColor, [[1135, 75], [1154, 75], [1154, 94], [1135, 94]], 2)
        pygame.draw.line(screen, CancelElementsColor, [1138, 78], [1151, 91], 2)
        pygame.draw.line(screen, CancelElementsColor, [1138, 91], [1151, 78], 2)

    # Siege duration
    text_panel5 = font16.render("Siege duration:", True, DarkText)
    screen.blit(text_panel5, [128, 95])

    duration_img = game_stats.gf_misc_img_dict["Icons/duration_icon"]
    screen.blit(duration_img, (128, 114))

    duration_text = None
    if the_settlement.siege.time_passed == 1:
        duration_text = "1 turn"
    else:
        duration_text = str(the_settlement.siege.time_passed) + " turns"
    text_panel5 = font16.render(duration_text, True, DarkText)
    screen.blit(text_panel5, [143, 112])

    y_base = 139
    y_shift = 30
    y_num = 0

    # Button - Start assault
    text = "Start assault"
    x = 0
    if not game_stats.besieged_by_human and not game_stats.siege_assault:
        text = "Start sortie"
        x = 4
    pygame.draw.polygon(screen, FillButton, [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                                             [238, y_base + y_shift * y_num + 22],
                                             [128, y_base + y_shift * y_num + 22]])
    if game_stats.assault_allowed:  # Works both for Battle and autobattle
        color1 = HighlightOption
    else:
        color1 = CancelElementsColor
    pygame.draw.polygon(screen, color1, [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                                         [238, y_base + y_shift * y_num + 22], [128, y_base + y_shift * y_num + 22]], 3)
    text_panel5 = font20.render(text, True, DarkText)
    screen.blit(text_panel5, [133 + x, y_base + y_shift * y_num])
    y_num += 1

    # Button - Autobattle
    pygame.draw.polygon(screen, FillButton, [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                                             [238, y_base + y_shift * y_num + 22],
                                             [128, y_base + y_shift * y_num + 22]])
    pygame.draw.polygon(screen, color1, [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                                         [238, y_base + y_shift * y_num + 22], [128, y_base + y_shift * y_num + 22]], 3)
    text_panel5 = font20.render("Autobattle", True, DarkText)
    screen.blit(text_panel5, [139, y_base + y_shift * y_num])
    y_num += 1

    # Button - Encircle
    if game_stats.besieged_by_human:
        pygame.draw.polygon(screen, FillButton, [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                                                 [238, y_base + y_shift * y_num + 22],
                                                 [128, y_base + y_shift * y_num + 22]])
        pygame.draw.polygon(screen, LineMainMenuColor1,
                            [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                             [238, y_base + y_shift * y_num + 22], [128, y_base + y_shift * y_num + 22]], 3)
        text_panel5 = font20.render("Encircle", True, DarkText)
        screen.blit(text_panel5, [151, y_base + y_shift * y_num])
        y_num += 1

    # Button - retreat
    if game_stats.besieged_by_human:
        pygame.draw.polygon(screen, FillButton, [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                                                 [238, y_base + y_shift * y_num + 22],
                                                 [128, y_base + y_shift * y_num + 22]])
        pygame.draw.polygon(screen, LineMainMenuColor1,
                            [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                             [238, y_base + y_shift * y_num + 22], [128, y_base + y_shift * y_num + 22]], 3)
        text_panel5 = font20.render("Retreat", True, DarkText)
        screen.blit(text_panel5, [155, y_base + y_shift * y_num])

        # Display defensive structures
        text_panel5 = font20.render("Defences", True, DarkText)
        screen.blit(text_panel5, [322, 95])

    # Defenders supplies
    # Background image
    background_img = game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"]
    screen.blit(background_img, (256, 123))

    # Icon image
    supplies_img = game_stats.gf_misc_img_dict["supplies_icon"]
    screen.blit(supplies_img, (256 + 5, 123))

    # Supplies message
    supplies_msg = None
    if the_settlement.siege.supplies == 1:
        supplies_msg = "1 turn"
    else:
        supplies_msg = str(the_settlement.siege.supplies) + " turns"
    text_panel5 = font16.render(supplies_msg, True, DarkText)
    screen.blit(text_panel5, [256 + 3, 164])

    num = 0
    for structure in the_settlement.defences:
        # Background image
        background_img = game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"]
        screen.blit(background_img, (326 + num * 52, 123))

        # Icon image
        structure_img = game_stats.gf_building_dict[structure.name]
        x = structure_img.get_width()
        screen.blit(structure_img, (326 + num * 52 + ((50 - x) / 2), 123))

        unbroken_wall_sections = 0
        total_wal_sections = 0
        # print(str(len(structure.def_objects)) + " objects")
        for def_object in structure.def_objects:
            # Check wall
            if def_object.section_type == "Wall":
                total_wal_sections += 1
                if def_object.state == "Unbroken":
                    unbroken_wall_sections += 1

            # Check gate
            if def_object.section_type == "Gate":
                gate_img = None
                gate_msg = None
                if def_object.state == "Unbroken":
                    gate_img = game_stats.gf_misc_img_dict["castle_gate_closed_icon"]
                    gate_msg = "Closed"
                elif def_object.state == "Broken":
                    gate_img = game_stats.gf_misc_img_dict["castle_gate_destroyed_icon"]
                    gate_msg = "Destroyed"

                # Background image
                background_img = game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"]
                screen.blit(background_img, (256, 187))

                # Icon image
                screen.blit(gate_img, (256 + 5, 187))

                # Gate message
                text_panel5 = font16.render(gate_msg, True, DarkText)
                screen.blit(text_panel5, [256 + 25 - (len(gate_msg) * 4), 228])

        if total_wal_sections > 0:
            # Number message
            number_msg = str(unbroken_wall_sections) + "/" + str(total_wal_sections)
            text_panel5 = font16.render(number_msg, True, DarkText)
            screen.blit(text_panel5, [326 + num * 52 + 25 - (len(number_msg) * 4), 164])

    y_base = 95
    y_shift = 44
    circle_radius = 9

    # Display siege engines
    text_panel5 = font20.render("Siege engines", True, DarkText)
    screen.blit(text_panel5, [662, y_base])

    y_base += 28
    # Trebuchets
    # Background image
    background_img = game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"]
    screen.blit(background_img, (650, y_base + y_shift * 0))

    # Icon image
    trebuchet_img = game_stats.gf_misc_img_dict["siege_trebuchet_icon"]
    screen.blit(trebuchet_img, (654, y_base + y_shift * 0))

    # Sledgehammer icon
    sledgehammer_img = game_stats.gf_misc_img_dict["sledgehammer_icon_18x18"]
    screen.blit(sledgehammer_img, (702, y_base + y_shift * 0 + 2))

    # Ordered trebuchets
    if the_settlement.siege.trebuchets_ordered > 0:
        text_panel = font20.render(str(the_settlement.siege.trebuchets_ordered), True, DarkText)
        screen.blit(text_panel, [725, y_base + y_shift * 0])

    if game_stats.besieged_by_human:
        # + button
        pygame.draw.circle(screen, FillButton, [734, y_base + y_shift * 0 + 30], circle_radius)
        pygame.draw.circle(screen, LineMainMenuColor1, [734, y_base + y_shift * 0 + 30], circle_radius, 1)
        pygame.draw.line(screen, LineMainMenuColor1, [729, y_base + y_shift * 0 + 29], [738, y_base + y_shift * 0 + 29],
                         2)
        pygame.draw.line(screen, LineMainMenuColor1, [733, y_base + y_shift * 0 + 25], [733, y_base + y_shift * 0 + 34],
                         2)
        # - button
        pygame.draw.circle(screen, FillButton, [714, y_base + y_shift * 0 + 30], circle_radius)
        pygame.draw.circle(screen, LineMainMenuColor1, [714, y_base + y_shift * 0 + 30], circle_radius, 1)
        pygame.draw.line(screen, LineMainMenuColor1, [709, y_base + y_shift * 0 + 29], [718, y_base + y_shift * 0 + 29],
                         2)

    # Amount
    text_line = str(the_settlement.siege.trebuchets_ready) + "/" + \
                str(the_settlement.siege.trebuchets_max_quantity)
    text_panel = font20.render(text_line, True, DarkText)
    screen.blit(text_panel, [752, y_base + y_shift * 0 + 10])

    # Siege towers
    # Background image
    background_img = game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"]
    screen.blit(background_img, (650, y_base + y_shift * 1))

    # Icon image
    siege_tower_img = game_stats.gf_misc_img_dict["siege_tower_icon"]
    screen.blit(siege_tower_img, (657, y_base + y_shift * 1))

    # Sledgehammer icon
    sledgehammer_img = game_stats.gf_misc_img_dict["sledgehammer_icon_18x18"]
    screen.blit(sledgehammer_img, (702, y_base + y_shift * 1 + 2))

    # Ordered siege towers
    if the_settlement.siege.siege_towers_ordered > 0:
        text_panel = font20.render(str(the_settlement.siege.siege_towers_ordered), True, DarkText)
        screen.blit(text_panel, [725, y_base + y_shift * 1])

    if game_stats.besieged_by_human:
        # + button
        pygame.draw.circle(screen, FillButton, [734, y_base + y_shift * 1 + 30], circle_radius)
        pygame.draw.circle(screen, LineMainMenuColor1, [734, y_base + y_shift * 1 + 30], circle_radius, 1)
        pygame.draw.line(screen, LineMainMenuColor1, [729, y_base + y_shift * 1 + 29], [738, y_base + y_shift * 1 + 29],
                         2)
        pygame.draw.line(screen, LineMainMenuColor1, [733, y_base + y_shift * 1 + 25], [733, y_base + y_shift * 1 + 34],
                         2)
        # - button
        pygame.draw.circle(screen, FillButton, [714, y_base + y_shift * 1 + 30], circle_radius)
        pygame.draw.circle(screen, LineMainMenuColor1, [714, y_base + y_shift * 1 + 30], circle_radius, 1)
        pygame.draw.line(screen, LineMainMenuColor1, [709, y_base + y_shift * 1 + 29], [718, y_base + y_shift * 1 + 29],
                         2)

    # Amount
    text_line = str(the_settlement.siege.siege_towers_ready) + "/" + \
                str(the_settlement.siege.siege_towers_max_quantity)
    text_panel = font20.render(text_line, True, DarkText)
    screen.blit(text_panel, [752, y_base + y_shift * 1 + 10])

    # Battering rams
    # Background image
    background_img = game_stats.gf_misc_img_dict["Icons/paper_2_square_50_x_40"]
    screen.blit(background_img, (650, y_base + y_shift * 2))

    # Icon image
    battering_ram_img = game_stats.gf_misc_img_dict["siege_battering_ram_icon"]
    screen.blit(battering_ram_img, (651, y_base + y_shift * 2 + 4))

    # Sledgehammer icon
    sledgehammer_img = game_stats.gf_misc_img_dict["sledgehammer_icon_18x18"]
    screen.blit(sledgehammer_img, (702, y_base + y_shift * 2 + 2))

    # Ordered battering rams
    if the_settlement.siege.battering_rams_ordered > 0:
        text_panel = font20.render(str(the_settlement.siege.battering_rams_ordered), True, DarkText)
        screen.blit(text_panel, [725, y_base + y_shift * 2])

    if game_stats.besieged_by_human:
        # + button
        pygame.draw.circle(screen, FillButton, [734, y_base + y_shift * 2 + 30], circle_radius)
        pygame.draw.circle(screen, LineMainMenuColor1, [734, y_base + y_shift * 2 + 30], circle_radius, 1)
        pygame.draw.line(screen, LineMainMenuColor1, [729, y_base + y_shift * 2 + 29], [738, y_base + y_shift * 2 + 29],
                         2)
        pygame.draw.line(screen, LineMainMenuColor1, [733, y_base + y_shift * 2 + 25], [733, y_base + y_shift * 2 + 34],
                         2)
        # - button
        pygame.draw.circle(screen, FillButton, [714, y_base + y_shift * 2 + 30], circle_radius)
        pygame.draw.circle(screen, LineMainMenuColor1, [714, y_base + y_shift * 2 + 30], circle_radius, 1)
        pygame.draw.line(screen, LineMainMenuColor1, [709, y_base + y_shift * 2 + 29], [718, y_base + y_shift * 2 + 29],
                         2)

    # Amount
    text_line = str(the_settlement.siege.battering_rams_ready) + "/" + \
                str(the_settlement.siege.battering_rams_max_quantity)
    text_panel = font20.render(text_line, True, DarkText)
    screen.blit(text_panel, [752, y_base + y_shift * 2 + 10])

    # Siege log
    text_panel5 = font20.render("Events log", True, DarkText)
    screen.blit(text_panel5, [935, 95])

    y_base = 123
    y_shift = 16
    y_num = 0
    for text_log in the_settlement.siege.siege_log:
        text_panel = font16.render(text_log, True, DarkText)
        screen.blit(text_panel, [821, y_base + y_shift * y_num])
        y_num += 1

    # Display units
    for army in game_obj.game_armies:
        if army.army_id == game_stats.attacker_army_id:  # Attacker
            if army.owner == "Neutral":
                text_panel = font20.render("Neutral", True, DarkText)
                screen.blit(text_panel, [351, 312])
            else:
                for power in game_obj.game_powers:
                    if power.name == army.owner:
                        x_cor = 351
                        y_cor = 312
                        # Country's name
                        text_panel = font20.render(power.name, True, DarkText)
                        screen.blit(text_panel, [x_cor, y_cor])

                        # Flag
                        pygame.draw.polygon(screen, FlagColors[power.f_color],
                                            [[x_cor - 35, y_cor], [x_cor - 5, y_cor], [x_cor - 5, y_cor + 11],
                                             [x_cor - 35, y_cor + 11]])
                        pygame.draw.polygon(screen, FlagColors[power.s_color],
                                            [[x_cor - 35, y_cor + 12], [x_cor - 5, y_cor + 12], [x_cor - 5, y_cor + 20],
                                             [x_cor - 35, y_cor + 20]])
                        break

            # Units
            if len(army.units) > 0:
                number = 0
                for unit in army.units:
                    x_pos = 135 + math.floor(number % 10) * 50
                    y_pos = 338 + math.floor(number / 10) * 55

                    army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                    screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

                    # Number of creatures
                    number_of_creatures = str(len(unit.crew)) + "/" + str(unit.rows * unit.number)
                    text_panel = arial_font14.render(number_of_creatures, True, DarkText)
                    screen.blit(text_panel, [x_pos + 12, y_pos + 42])

                    number += 1

        elif army.army_id == game_stats.defender_army_id:  # Defender
            if army.owner == "Neutral":
                text_panel = font20.render("Neutral", True, DarkText)
                screen.blit(text_panel, [841, 312])
            else:
                for power in game_obj.game_powers:
                    if power.name == army.owner:
                        x_cor = 841
                        y_cor = 312
                        # Country's name
                        text_panel = font20.render(power.name, True, DarkText)
                        screen.blit(text_panel, [x_cor, y_cor])

                        # Flag
                        pygame.draw.polygon(screen, FlagColors[power.f_color],
                                            [[x_cor - 35, y_cor], [x_cor - 5, y_cor], [x_cor - 5, y_cor + 11],
                                             [x_cor - 35, y_cor + 11]])
                        pygame.draw.polygon(screen, FlagColors[power.s_color],
                                            [[x_cor - 35, y_cor + 12], [x_cor - 5, y_cor + 12], [x_cor - 5, y_cor + 20],
                                             [x_cor - 35, y_cor + 20]])
                        break

            # Units
            if len(army.units) > 0:
                number = 0
                for unit in army.units:
                    x_pos = 650 + math.floor(number % 10) * 50
                    y_pos = 338 + math.floor(number / 10) * 55

                    army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_l"]
                    screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

                    # Number of creatures
                    number_of_creatures = str(len(unit.crew)) + "/" + str(unit.rows * unit.number)
                    text_panel = arial_font14.render(number_of_creatures, True, DarkText)
                    screen.blit(text_panel, [x_pos + 12, y_pos + 42])

                    number += 1


def army_panel(screen):
    # White border around selected tile
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:
            x2 = int(army.posxy[0])
            y2 = int(army.posxy[1])
            x2 -= int(game_stats.pov_pos[0])
            y2 -= int(game_stats.pov_pos[1])

            # Draw movement arrows
            if len(army.path_arrows) > 0:
                draw_movement_arrows.arrow_icon(screen, army.route, army.path_arrows)

            # Border line
            pygame.draw.polygon(screen, WhiteBorder,
                                [[(x2 - 1) * 48, (y2 - 1) * 48], [(x2 - 1) * 48 + 47, (y2 - 1) * 48],
                                 [(x2 - 1) * 48 + 47, (y2 - 1) * 48 + 47], [(x2 - 1) * 48, (y2 - 1) * 48 + 47]], 1)

            break

    # Lower panel
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 650 + yVar], [1080, 650 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    # Army button
    pygame.draw.polygon(screen, FieldColor,
                        [[200, 627 + yVar], [260, 627 + yVar], [260, 649 + yVar], [200, 649 + yVar]])
    if game_stats.selected_object == "Army":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[200, 627 + yVar], [260, 627 + yVar], [260, 649 + yVar], [200, 649 + yVar]], 3)
    text_panel5 = font20.render("Army", True, DarkText)
    screen.blit(text_panel5, [206, 627 + yVar])

    # Ownership
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:

            if army.owner == "Neutral":
                text_panel = font20.render("Neutral", True, TitleText)
                screen.blit(text_panel, [240, 654 + yVar])
            else:
                for power in game_obj.game_powers:
                    if power.name == army.owner:
                        # Country's name
                        text_panel = font20.render(power.name, True, TitleText)
                        screen.blit(text_panel, [240, 654 + yVar])

                        # Flag
                        pygame.draw.polygon(screen, FlagColors[power.f_color],
                                            [[205, 654 + yVar], [235, 654 + yVar], [235, 665 + yVar],
                                             [205, 665 + yVar]])
                        pygame.draw.polygon(screen, FlagColors[power.s_color],
                                            [[205, 666 + yVar], [235, 666 + yVar], [235, 676 + yVar],
                                             [205, 676 + yVar]])
                        break

            # Hero
            if army.hero is not None:
                # Name
                text_panel = font20.render(army.hero.name, True, TitleText)
                screen.blit(text_panel, [203, 706 + yVar])

                # Class
                text_panel = font16.render(army.hero.hero_class, True, DarkText)
                screen.blit(text_panel, [253, 726 + yVar])

                # Level
                text_panel = font16.render("Level " + str(army.hero.level), True, DarkText)
                screen.blit(text_panel, [253, 746 + yVar])

                # Hero image
                img = army.hero.img
                source = army.hero.img_source
                # Previous code
                # army_img = pygame.image.load('img/Heroes/' + str(source) + "/" + str(img) + '.png')
                # army_img.set_colorkey(WhiteColor)
                x_offset = army.hero.x_offset
                y_offset = army.hero.y_offset
                side = "_l"
                if army.right_side:
                    side = "_r"
                # New code
                army_img = game_stats.gf_hero_dict[source + "/" + img + side]
                screen.blit(army_img, (203 + x_offset, 726 + yVar + y_offset))

                # Open hero window
                border_color = HighlightOption
                pygame.draw.polygon(screen, border_color,
                                    [[203, 776 + yVar], [253, 776 + yVar], [253, 794 + yVar], [203, 794 + yVar]], 2)
                text_panel1 = font16.render("Hero", True, DarkText)
                screen.blit(text_panel1, [213, 777 + yVar])

                # New attribute or skill points are available
                if army.hero.new_attribute_points > 0 or army.hero.new_skill_points > 0:
                    icon_img = game_stats.gf_misc_img_dict["Icons/plus_sign_24_2"]
                    # army_img.set_colorkey(WhiteColor)
                    screen.blit(icon_img, (258, 774 + yVar))

            break

    movement_points_left = -1
    least_max_movement_points = -1
    # Display units
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:
            side = "_l"
            if army.right_side:
                side = "_r"

            # Units
            if len(army.units) > 0:
                number = 0
                for unit in army.units:
                    x_pos = 430 + math.floor(number % 10) * 52
                    y_pos = 654 + yVar + math.floor(number / 10) * 57
                    # New code
                    if unit.img_width > 44 or unit.img_height > 44:
                        army_img = game_stats.gf_regiment_dict[unit.img_source + "/"
                                                               + unit.img + side]
                        if unit.img_width > 44:
                            proportion = 44 / unit.img_width
                            army_img = pygame.transform.scale(army_img,
                                                              (44,
                                                               int(unit.img_height * proportion)))
                            x_offset = 3
                            y_offset = (48 - (unit.img_height * proportion)) / 2
                        else:
                            proportion = 44 / unit.img_height
                            army_img = pygame.transform.scale(army_img,
                                                              (int(unit.img_width * proportion),
                                                               44))
                            x_offset = (48 - (unit.img_width * proportion)) / 2
                            y_offset = 3
                    else:
                        army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + side]
                        x_offset = unit.x_offset
                        y_offset = unit.y_offset

                    screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])
                    # screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

                    # Number of creatures
                    number_of_creatures = str(len(unit.crew)) + "/" + str(unit.rows * unit.number)
                    text_panel = arial_font14.render(number_of_creatures, True, DarkText)
                    screen.blit(text_panel, [x_pos + 12, y_pos + 42])

                    if int(number) in game_stats.first_army_exchange_list:
                        pygame.draw.polygon(screen, ApproveElementsColor,
                                            [[x_pos + unit.x_offset - 10, y_pos + unit.y_offset - 3],
                                             [x_pos + unit.x_offset + 21, y_pos + unit.y_offset - 3],
                                             [x_pos + unit.x_offset + 6, y_pos + unit.y_offset - 9]])

                    number += 1

                    # Update movement points information
                    if movement_points_left < 0:
                        movement_points_left = int(unit.movement_points)
                    elif unit.movement_points < movement_points_left:
                        movement_points_left = int(unit.movement_points)

                    if least_max_movement_points < 0:
                        least_max_movement_points = int(unit.max_movement_points)
                    elif unit.max_movement_points < least_max_movement_points:
                        least_max_movement_points = int(unit.max_movement_points)

            # Not the best way to design additional points from skills
            if army.hero is not None:
                for skill in army.hero.skills:
                    for effect in skill.effects:
                        if effect.application == "Movement points":
                            if effect.method == "addition":
                                least_max_movement_points += int(effect.quantity)

                if len(army.hero.inventory) > 0:
                    # print("len(army.hero.inventory) > 0")
                    for artifact in army.hero.inventory:
                        for effect in artifact.effects:
                            if effect.application == "Movement points":
                                # print("effect.application == Movement points")
                                if effect.method == "addition":
                                    least_max_movement_points += int(effect.quantity)
                                    # print(str(least_max_movement_points))

            break

    # Movement points bar
    xVar = int(movement_points_left / least_max_movement_points * 80)
    pygame.draw.polygon(screen, ApproveFieldColor,
                        [[203, 684 + yVar], [203 + xVar, 684 + yVar], [203 + xVar, 706 + yVar], [203, 706 + yVar]])
    pygame.draw.polygon(screen, ApproveElementsColor,
                        [[203, 684 + yVar], [283, 684 + yVar], [283, 706 + yVar], [203, 706 + yVar]], 3)


def settlement_panel(screen):
    # Draw top left panel with interface to interact with settlement mechanics
    pygame.draw.polygon(screen, MainMenuColor,
                        [[1, 80], [639, 80], [639, 540], [1, 540]])

    # Buttons - settlement interface area
    # Building
    pygame.draw.polygon(screen, FillButton,
                        [[5, 85], [110, 85], [110, 104], [5, 104]])
    if game_stats.settlement_area == "Building":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[5, 85], [110, 85], [110, 104], [5, 104]], 2)

    icon_img = game_stats.gf_misc_img_dict["Icons/building_icon"]
    screen.blit(icon_img, (11, 88))

    text_panel1 = font16.render("Building", True, DarkText)
    screen.blit(text_panel1, [35, 85])

    # Recruiting
    pygame.draw.polygon(screen, FillButton,
                        [[120, 85], [225, 85], [225, 104], [120, 104]])
    if game_stats.settlement_area == "Recruiting":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[120, 85], [225, 85], [225, 104], [120, 104]], 2)

    icon_img = game_stats.gf_misc_img_dict["Icons/recruiting_icon"]
    icon_img.set_colorkey(WhiteColor)
    screen.blit(icon_img, (127, 88))

    text_panel1 = font16.render("Recruiting", True, DarkText)
    screen.blit(text_panel1, [150, 85])

    # Heroes
    pygame.draw.polygon(screen, FillButton,
                        [[235, 85], [340, 85], [340, 104], [235, 104]])
    if game_stats.settlement_area == "Heroes":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[235, 85], [340, 85], [340, 104], [235, 104]], 2)

    icon_img = game_stats.gf_misc_img_dict["Icons/heroes_icon"]
    icon_img.set_colorkey(WhiteColor)
    screen.blit(icon_img, (244, 88))

    text_panel1 = font16.render("Heroes", True, DarkText)
    screen.blit(text_panel1, [265, 85])

    # Economy
    pygame.draw.polygon(screen, FillButton,
                        [[350, 85], [455, 85], [455, 104], [350, 104]])
    if game_stats.settlement_area == "Economy":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[350, 85], [455, 85], [455, 104], [350, 104]], 2)

    icon_img = game_stats.gf_misc_img_dict["Icons/economy_icon"]
    icon_img.set_colorkey(WhiteColor)
    screen.blit(icon_img, (356, 88))

    text_panel1 = font16.render("Economy", True, DarkText)
    screen.blit(text_panel1, [380, 85])

    # Factions
    pygame.draw.polygon(screen, FillButton,
                        [[465, 85], [570, 85], [570, 104], [465, 104]])
    if game_stats.settlement_area == "Factions":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[465, 85], [570, 85], [570, 104], [465, 104]], 2)

    icon_img = game_stats.gf_misc_img_dict["Icons/factions_icon"]
    icon_img.set_colorkey(WhiteColor)
    screen.blit(icon_img, (471, 88))

    text_panel1 = font16.render("Factions", True, DarkText)
    screen.blit(text_panel1, [495, 85])

    # Close settlement window
    pygame.draw.polygon(screen, CancelFieldColor, [[615, 85], [634, 85], [634, 104], [615, 104]])
    pygame.draw.polygon(screen, CancelElementsColor, [[615, 85], [634, 85], [634, 104], [615, 104]], 2)
    pygame.draw.line(screen, CancelElementsColor, [618, 88], [631, 101], 2)
    pygame.draw.line(screen, CancelElementsColor, [618, 101], [631, 88], 2)

    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    # Draw area content
    detail_functions_voc = {"Building": det_settlement_buildings.draw_structures,
                            "Recruiting": det_settlement_recruiting.draw_units,
                            "Heroes": det_settlement_heroes.draw_heroes,
                            "Economy": det_settlement_economy.draw_economy,
                            "Factions": det_settlement_factions.draw_factions}

    detail_functions_voc[game_stats.settlement_area](screen, settlement)


def settlement_info_panel(screen):
    # Draw lower panel with information about settlement
    stationed_id = -1
    TileObj = None

    # White border around selected tile
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_stats.selected_settlement:
            x2 = int(settlement.posxy[0])
            y2 = int(settlement.posxy[1])

            TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1
            TileObj = game_obj.game_map[TileNum]
            # print("settlement TileNum is " + str(TileNum))

            x2 -= int(game_stats.pov_pos[0])
            y2 -= int(game_stats.pov_pos[1])

            # Border line
            pygame.draw.polygon(screen, WhiteBorder,
                                [[(x2 - 1) * 48, (y2 - 1) * 48], [(x2 - 1) * 48 + 47, (y2 - 1) * 48],
                                 [(x2 - 1) * 48 + 47, (y2 - 1) * 48 + 47], [(x2 - 1) * 48, (y2 - 1) * 48 + 47]], 1)

            break

    # Lower panel
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 650 + yVar], [1080, 650 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    if TileObj.army_id is not None:
        stationed_id = int(TileObj.army_id)
        # print("stationed_id - " + str(stationed_id))

        # Stationed army
        army = None

        for army_obj in game_obj.game_armies:
            if army_obj.army_id == stationed_id:
                army = army_obj
                break

        side = "_l"
        if army.right_side:
            side = "_r"

        # Ownership
        if army.owner == "Neutral":
            text_panel = font20.render("Neutral", True, TitleText)
            screen.blit(text_panel, [240, 654 + yVar])
        else:
            for power in game_obj.game_powers:
                if power.name == army.owner:
                    # Country's name
                    text_panel = font20.render(power.name, True, TitleText)
                    screen.blit(text_panel, [240, 654 + yVar])

                    # Flag
                    pygame.draw.polygon(screen, FlagColors[power.f_color],
                                        [[205, 654 + yVar], [235, 654 + yVar], [235, 665 + yVar],
                                         [205, 665 + yVar]])
                    pygame.draw.polygon(screen, FlagColors[power.s_color],
                                        [[205, 666 + yVar], [235, 666 + yVar], [235, 676 + yVar],
                                         [205, 676 + yVar]])

        movement_points_left = -1
        least_max_movement_points = -1
        # Display units
        if len(army.units) > 0:
            number = 0

            for unit in army.units:
                x_pos = 430 + math.floor(number % 10) * 52
                y_pos = 654 + yVar + math.floor(number / 10) * 52
                # New code
                if unit.crew[0].img_width > 44 or unit.crew[0].img_height > 44:
                    army_img = game_stats.gf_regiment_dict[unit.img_source + "/"
                                                           + unit.img + side]
                    if unit.crew[0].img_width > 44:
                        proportion = 44 / unit.crew[0].img_width
                        army_img = pygame.transform.scale(army_img,
                                                          (44,
                                                           int(unit.crew[0].img_height * proportion)))
                        x_offset = 3
                        y_offset = (48 - (unit.crew[0].img_height * proportion)) / 2
                    else:
                        proportion = 44 / unit.crew[0].img_height
                        army_img = pygame.transform.scale(army_img,
                                                          (int(unit.crew[0].img_width * proportion),
                                                           44))
                        x_offset = (48 - (unit.crew[0].img_width * proportion)) / 2
                        y_offset = 3
                else:
                    army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + side]
                    x_offset = unit.x_offset
                    y_offset = unit.y_offset

                screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])
                # screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

                # Number of creatures
                number_of_creatures = str(len(unit.crew)) + "/" + str(unit.rows * unit.number)
                text_panel = arial_font14.render(number_of_creatures, True, DarkText)
                screen.blit(text_panel, [x_pos + 12, y_pos + 42])

                number += 1

                # Update movement points information
                if movement_points_left < 0:
                    movement_points_left = int(unit.movement_points)
                elif unit.movement_points < movement_points_left:
                    movement_points_left = int(unit.movement_points)

                if least_max_movement_points < 0:
                    least_max_movement_points = int(unit.max_movement_points)
                elif unit.max_movement_points < least_max_movement_points:
                    least_max_movement_points = int(unit.max_movement_points)

        # Movement points bar
        xVar = int(movement_points_left / least_max_movement_points * 80)
        pygame.draw.polygon(screen, ApproveFieldColor,
                            [[203, 684 + yVar], [203 + xVar, 684 + yVar], [203 + xVar, 706 + yVar], [203, 706 + yVar]])
        pygame.draw.polygon(screen, ApproveElementsColor,
                            [[203, 684 + yVar], [283, 684 + yVar], [283, 706 + yVar], [203, 706 + yVar]], 3)

        # Select army button
        border_color = HighlightOption
        if len(army.units) < 5:
            text_panel1 = font14.render("Less than", True, DarkText)
            screen.blit(text_panel1, [312, 651 + yVar])
            text_panel1 = font14.render("5 regiments", True, DarkText)
            screen.blit(text_panel1, [312, 667 + yVar])
            border_color = LineMainMenuColor1
        pygame.draw.polygon(screen, border_color,
                            [[303, 684 + yVar], [393, 684 + yVar], [393, 706 + yVar], [303, 706 + yVar]], 3)
        text_panel1 = font16.render("Select army", True, DarkText)
        screen.blit(text_panel1, [312, 686 + yVar])

        # Hero
        if army.hero is not None:
            # Name
            text_panel = font20.render(army.hero.name, True, TitleText)
            screen.blit(text_panel, [203, 706 + yVar])

            # Class
            text_panel = font16.render(army.hero.hero_class, True, DarkText)
            screen.blit(text_panel, [253, 726 + yVar])

            # Level
            text_panel = font16.render("Level " + str(army.hero.level), True, DarkText)
            screen.blit(text_panel, [253, 746 + yVar])

            # Hero image
            img = army.hero.img
            source = army.hero.img_source
            x_offset = army.hero.x_offset
            y_offset = army.hero.y_offset

            # New code
            army_img = game_stats.gf_hero_dict[source + "/" + img + side]
            screen.blit(army_img, (203 + x_offset, 726 + yVar + y_offset))

            # Open hero window
            border_color = HighlightOption
            pygame.draw.polygon(screen, border_color,
                                [[203, 776 + yVar], [253, 776 + yVar], [253, 794 + yVar], [203, 794 + yVar]], 2)
            text_panel1 = font16.render("Hero", True, DarkText)
            screen.blit(text_panel1, [213, 777 + yVar])

            # New attribute or skill points are available
            if army.hero.new_attribute_points > 0 or army.hero.new_skill_points > 0:
                icon_img = game_stats.gf_misc_img_dict["Icons/plus_sign_24_2"]
                # army_img.set_colorkey(WhiteColor)
                screen.blit(icon_img, (258, 774 + yVar))


def realm_panel(screen):
    power = game_stats.realm_inspection

    # Draw top left panel with interface to interact with realm mechanics
    pygame.draw.polygon(screen, MainMenuColor,
                        [[34, 80], [679, 80], [679, 540], [34, 540]])

    # Buttons - realm interface area
    # Close realm window
    pygame.draw.polygon(screen, CancelFieldColor, [[655, 85], [674, 85], [674, 104], [655, 104]])
    pygame.draw.polygon(screen, CancelElementsColor, [[655, 85], [674, 85], [674, 104], [655, 104]], 2)
    pygame.draw.line(screen, CancelElementsColor, [658, 88], [671, 101], 2)
    pygame.draw.line(screen, CancelElementsColor, [658, 101], [671, 88], 2)

    ## Realm information
    # Flag
    x = 38
    y = 83
    pygame.draw.polygon(screen, FlagColors[power.f_color],
                        [[x, y], [x + 30, y],
                         [x + 30, y + 11], [x, y + 11]])
    pygame.draw.polygon(screen, FlagColors[power.s_color],
                        [[x, y + 12], [x + 30, y + 12],
                         [x + 30, y + 22], [x, y + 22]])

    text_panel = font20.render(power.name, True, TitleText)
    screen.blit(text_panel, [75, 85])

    icon_img = game_stats.gf_misc_img_dict["Icons/masks"]
    screen.blit(icon_img, (41, 109))

    text_panel = font20.render(power.alignment, True, TitleText)
    screen.blit(text_panel, [75, 110])

    icon_img = game_stats.gf_misc_img_dict["Icons/crown_bigger"]
    screen.blit(icon_img, (39, 134))

    text_panel = font20.render(power.leader.name, True, TitleText)
    screen.blit(text_panel, [75, 135])

    # Traits
    x_base = 38
    y_base = 160
    y_shift = 19
    y_num = 0

    # Speciality trait
    text_panel = font16.render("Speciality trait", True, TitleText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    y_num += 1

    # Behavior traits
    text_panel = font16.render("Behavior traits", True, TitleText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    text_panel = font16.render(power.leader.behavior_traits[0], True, DarkText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    if len(power.leader.behavior_traits) > 1:
        text_panel = font16.render(power.leader.behavior_traits[1], True, DarkText)
        screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    # Lifestyle traits
    text_panel = font16.render("Lifestyle traits", True, TitleText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    text_panel = font16.render(power.leader.lifestyle_traits[0], True, DarkText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    text_panel = font16.render(power.leader.lifestyle_traits[1], True, DarkText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1


def tile_obj_panel(screen):
    # White border around selected tile
    x2 = int(game_stats.info_tile[0])
    y2 = int(game_stats.info_tile[1])
    # x2 -= int(game_stats.pov_pos[0])
    # y2 -= int(game_stats.pov_pos[1])
    TileNum = (y2 - 1) * game_stats.cur_level_width + x2 - 1

    x3 = x2 - int(game_stats.pov_pos[0])
    y3 = y2 - int(game_stats.pov_pos[1])
    # Border line
    pygame.draw.polygon(screen, WhiteBorder,
                        [[(x3 - 1) * 48, (y3 - 1) * 48], [(x3 - 1) * 48 + 47, (y3 - 1) * 48],
                         [(x3 - 1) * 48 + 47, (y3 - 1) * 48 + 47], [(x3 - 1) * 48, (y3 - 1) * 48 + 47]], 1)

    # Lower panel
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 650 + yVar], [1080, 650 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    # Terrain information
    # Ownership
    if game_stats.tile_ownership == "Wild lands":
        text_panel = font20.render("Wild lands", True, TitleText)
        screen.blit(text_panel, [205, 654 + yVar])
    elif game_stats.tile_ownership == "Neutral lands":
        text_panel = font20.render("Neutral lands", True, TitleText)
        screen.blit(text_panel, [205, 654 + yVar])
    else:
        # Country's name
        text_panel = font20.render(game_stats.tile_ownership, True, TitleText)
        screen.blit(text_panel, [240, 654 + yVar])

        # Flag
        pygame.draw.polygon(screen, FlagColors[game_stats.tile_flag_colors[0]],
                            [[205, 654 + yVar], [235, 654 + yVar], [235, 665 + yVar],
                             [205, 665 + yVar]])
        pygame.draw.polygon(screen, FlagColors[game_stats.tile_flag_colors[1]],
                            [[205, 666 + yVar], [235, 666 + yVar], [235, 676 + yVar],
                             [205, 676 + yVar]])

    # Terrain type
    TileObj = game_obj.game_map[TileNum]
    text_panel = font20.render(TileObj.terrain, True, TitleText)
    screen.blit(text_panel, [205, 684 + yVar])

    # Road information
    yVar2 = 0
    if TileObj.road is not None:
        yVar2 += 30
        text_panel = font20.render(TileObj.road, True, TitleText)
        screen.blit(text_panel, [205, 684 + yVar + yVar2])

    ### Lot object information

    if TileObj.lot is not None:
        if TileObj.lot == "City":
            # If object is a city
            yVar2 += 30
            text_panel = font20.render("Settlement", True, TitleText)
            screen.blit(text_panel, [205, 684 + yVar + yVar2])

            settlement = None
            for city in game_obj.game_cities:
                if city.city_id == game_stats.right_click_city:
                    settlement = city

            ### Population information
            text_panel = font20.render("Population", True, TitleText)
            screen.blit(text_panel, [391, 654 + yVar])

            yPos = 0
            for pops in settlement.residency:
                # Population's name
                # print(pops)
                text_panel = font20.render(pops.name, True, DarkText)
                screen.blit(text_panel, [391, 680 + yVar + yPos])

                yPos += 30

            # White line
            pygame.draw.lines(screen, WhiteBorder, False, [(391, 702 + yVar + 30 * game_stats.i_p_index),
                                                           (480, 702 + yVar + 30 * game_stats.i_p_index)], 1)

            ### Resources
            # Only shows player's resources
            if game_stats.tile_ownership == game_stats.player_power:
                # Property
                text_panel = font20.render("Property:", True, TitleText)
                screen.blit(text_panel, [510, 654 + yVar])

                # Resources in reserve
                # print(TileObj.lot.residency[game_stats.i_p_index])
                if len(settlement.residency[game_stats.i_p_index].reserve) > 0:
                    yPos = 0
                    for resource in settlement.residency[game_stats.i_p_index].reserve:
                        text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True, DarkText)
                        screen.blit(text_panel, [510, 677 + yVar + yPos])

                        yPos += 15

                # Produced resources
                text_panel = font20.render("Produced:", True, TitleText)
                screen.blit(text_panel, [625, 654 + yVar])

                # Records from last turn
                if len(settlement.residency[game_stats.i_p_index].records_gained) > 0:
                    yPos = 0
                    for resource in settlement.residency[game_stats.i_p_index].records_gained:
                        text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True, DarkText)
                        screen.blit(text_panel, [625, 677 + yVar + yPos])

                        yPos += 15

                # Sold resources
                text_panel = font20.render("Sold:", True, TitleText)
                screen.blit(text_panel, [740, 654 + yVar])

                # Records from last turn
                if len(settlement.residency[game_stats.i_p_index].records_sold) > 0:
                    yPos = 0
                    for resource in settlement.residency[game_stats.i_p_index].records_sold:
                        text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True, DarkText)
                        screen.blit(text_panel, [740, 677 + yVar + yPos])

                        yPos += 15

                # Bought resources
                text_panel = font20.render("Bought:", True, TitleText)
                screen.blit(text_panel, [855, 654 + yVar])

                # Records from last turn
                if len(settlement.residency[game_stats.i_p_index].records_bought) > 0:
                    yPos = 0
                    for resource in settlement.residency[game_stats.i_p_index].records_bought:
                        text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True, DarkText)
                        screen.blit(text_panel, [855, 677 + yVar + yPos])

                        yPos += 15

                # Consumed resources
                text_panel = font20.render("Consumed:", True, TitleText)
                screen.blit(text_panel, [970, 654 + yVar])

                # Records from last turn
                if len(settlement.residency[game_stats.i_p_index].records_consumed) > 0:
                    yPos = 0
                    for resource in settlement.residency[game_stats.i_p_index].records_consumed:
                        text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True, DarkText)
                        screen.blit(text_panel, [970, 677 + yVar + yPos])

                        yPos += 15

        else:
            # If object is not a city
            yVar2 += 30
            text_panel = font20.render(TileObj.lot.obj_typ, True, TitleText)
            screen.blit(text_panel, [205, 684 + yVar + yVar2])

            # If object is facility, then show its name
            if TileObj.lot.obj_typ == "Facility":
                yVar2 += 30
                text_panel = font20.render(TileObj.lot.obj_name, True, TitleText)
                screen.blit(text_panel, [205, 684 + yVar + yVar2])

            if TileObj.lot.obj_typ == "Facility":
                ### Population information
                text_panel = font20.render("Population", True, TitleText)
                screen.blit(text_panel, [391, 654 + yVar])

                yPos = 0
                for pops in TileObj.lot.residency:
                    # Population's name
                    # print(pops)
                    text_panel = font20.render(pops.name, True, DarkText)
                    screen.blit(text_panel, [391, 680 + yVar + yPos])

                    yPos += 30

                # White line
                pygame.draw.lines(screen, WhiteBorder, False, [(391, 702 + yVar + 30 * game_stats.i_p_index),
                                                               (480, 702 + yVar + 30 * game_stats.i_p_index)], 1)

                ### Resources
                # Only shows player's resources
                if game_stats.tile_ownership == game_stats.player_power:
                    # Property
                    text_panel = font20.render("Property:", True, TitleText)
                    screen.blit(text_panel, [510, 654 + yVar])

                    # Resources in reserve
                    # print(TileObj.lot.residency[game_stats.i_p_index])
                    if len(TileObj.lot.residency[game_stats.i_p_index].reserve) > 0:
                        yPos = 0
                        for resource in TileObj.lot.residency[game_stats.i_p_index].reserve:
                            text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True, DarkText)
                            screen.blit(text_panel, [510, 677 + yVar + yPos])

                            yPos += 15

                    # Produced resources
                    text_panel = font20.render("Produced:", True, TitleText)
                    screen.blit(text_panel, [625, 654 + yVar])

                    # Records from last turn
                    if len(TileObj.lot.residency[game_stats.i_p_index].records_gained) > 0:
                        yPos = 0
                        for resource in TileObj.lot.residency[game_stats.i_p_index].records_gained:
                            text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True, DarkText)
                            screen.blit(text_panel, [625, 677 + yVar + yPos])

                            yPos += 15

                    # Sold resources
                    text_panel = font20.render("Sold:", True, TitleText)
                    screen.blit(text_panel, [740, 654 + yVar])

                    # Records from last turn
                    if len(TileObj.lot.residency[game_stats.i_p_index].records_sold) > 0:
                        yPos = 0
                        for resource in TileObj.lot.residency[game_stats.i_p_index].records_sold:
                            text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True,
                                                             DarkText)
                            screen.blit(text_panel, [740, 677 + yVar + yPos])

                            yPos += 15

                    # Bought resources
                    text_panel = font20.render("Bought:", True, TitleText)
                    screen.blit(text_panel, [855, 654 + yVar])

                    # Records from last turn
                    if len(TileObj.lot.residency[game_stats.i_p_index].records_bought) > 0:
                        yPos = 0
                        for resource in TileObj.lot.residency[game_stats.i_p_index].records_bought:
                            text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True,
                                                             DarkText)
                            screen.blit(text_panel, [855, 677 + yVar + yPos])

                            yPos += 15

                    # Consumed resources
                    text_panel = font20.render("Consumed:", True, TitleText)
                    screen.blit(text_panel, [970, 654 + yVar])

                    # Records from last turn
                    if len(TileObj.lot.residency[game_stats.i_p_index].records_consumed) > 0:
                        yPos = 0
                        for resource in TileObj.lot.residency[game_stats.i_p_index].records_consumed:
                            text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True,
                                                             DarkText)
                            screen.blit(text_panel, [970, 677 + yVar + yPos])

                            yPos += 15


def army_exchange_panel(screen):
    # Second army standing for exchange
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 380 + yVar], [639, 380 + yVar], [639, 619 + yVar], [200, 619 + yVar]])

    # Ownership
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_second_army:

            if army.owner == "Neutral":
                text_panel = font20.render("Neutral", True, TitleText)
                screen.blit(text_panel, [240, 384 + yVar])
            else:
                for power in game_obj.game_powers:
                    if power.name == army.owner:
                        # Country's name
                        text_panel = font20.render(power.name, True, TitleText)
                        screen.blit(text_panel, [240, 384 + yVar])

                        # Flag
                        pygame.draw.polygon(screen, FlagColors[power.f_color],
                                            [[205, 384 + yVar], [235, 384 + yVar], [235, 395 + yVar],
                                             [205, 395 + yVar]])
                        pygame.draw.polygon(screen, FlagColors[power.s_color],
                                            [[205, 396 + yVar], [235, 396 + yVar], [235, 406 + yVar],
                                             [205, 406 + yVar]])

    movement_points_left = -1
    least_max_movement_points = -1

    # Display units
    y2 = -180
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_second_army:

            # Units
            if len(army.units) > 0:
                number = 0
                for unit in army.units:
                    x_pos = 380 + math.floor(number % 5) * 52
                    y_pos = 559 + yVar + math.floor(number / 5) * 57
                    # New code
                    side = "_l"
                    if army.right_side:
                        side = "_r"

                    if unit.crew[0].img_width > 44 or unit.crew[0].img_height > 44:
                        army_img = game_stats.gf_regiment_dict[unit.img_source + "/"
                                                               + unit.img + side]
                        if unit.crew[0].img_width > 44:
                            proportion = 44 / unit.crew[0].img_width
                            army_img = pygame.transform.scale(army_img,
                                                              (44,
                                                               int(unit.crew[0].img_height * proportion)))
                            x_offset = 3
                            y_offset = (48 - (unit.crew[0].img_height * proportion)) / 2
                        else:
                            proportion = 44 / unit.crew[0].img_height
                            army_img = pygame.transform.scale(army_img,
                                                              (int(unit.crew[0].img_width * proportion),
                                                               44))
                            x_offset = (48 - (unit.crew[0].img_width * proportion)) / 2
                            y_offset = 3
                    else:
                        army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + side]
                        x_offset = unit.x_offset
                        y_offset = unit.y_offset

                    # army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + side]
                    screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset + y2])

                    # Number of creatures
                    number_of_creatures = str(len(unit.crew)) + "/" + str(unit.rows * unit.number)
                    text_panel = arial_font14.render(number_of_creatures, True, DarkText)
                    screen.blit(text_panel, [x_pos + 12, y_pos + 42 + y2])

                    if int(number) in game_stats.second_army_exchange_list:
                        pygame.draw.polygon(screen, ApproveElementsColor,
                                            [[x_pos + 6, y_pos + 57 + y2],
                                             [x_pos + 37, y_pos + 57 + y2],
                                             [x_pos + 22, y_pos + 63 + y2]])

                    number += 1

                    # Update movement points information
                    if movement_points_left < 0:
                        movement_points_left = int(unit.movement_points)
                    elif unit.movement_points < movement_points_left:
                        movement_points_left = int(unit.movement_points)

                    if least_max_movement_points < 0:
                        least_max_movement_points = int(unit.max_movement_points)
                    elif unit.max_movement_points < least_max_movement_points:
                        least_max_movement_points = int(unit.max_movement_points)

    # Movement points bar
    xVar = int(movement_points_left / least_max_movement_points * 80)
    pygame.draw.polygon(screen, ApproveFieldColor,
                        [[203, 414 + yVar], [203 + xVar, 414 + yVar], [203 + xVar, 436 + yVar],
                         [203, 436 + yVar]])
    pygame.draw.polygon(screen, ApproveElementsColor,
                        [[203, 414 + yVar], [283, 414 + yVar], [283, 436 + yVar], [203, 436 + yVar]], 3)

    # Complete exchange
    pygame.draw.polygon(screen, CancelElementsColor,
                        [[203, 595 + yVar], [290, 595 + yVar], [290, 617 + yVar], [203, 617 + yVar]], 2)

    text_NewGame1 = font20.render("Complete", True, DarkText)
    screen.blit(text_NewGame1, [207, 594 + yVar])


def quest_log_panel(screen):
    # Draw top left panel with interface to interact with realm's quest # x: 1 -> 34
    pygame.draw.polygon(screen, MainMenuColor,
                        [[34, 80], [679, 80], [679, 540], [34, 540]])

    # Close quest log window
    pygame.draw.polygon(screen, CancelFieldColor, [[655, 85], [674, 85], [674, 104], [655, 104]])
    pygame.draw.polygon(screen, CancelElementsColor, [[655, 85], [674, 85], [674, 104], [655, 104]], 2)
    pygame.draw.line(screen, CancelElementsColor, [658, 88], [671, 101], 2)
    pygame.draw.line(screen, CancelElementsColor, [658, 101], [671, 88], 2)

    # Buttons - quests log interface area
    x2 = 140
    # Quests messages
    x1 = 38
    pygame.draw.polygon(screen, FillButton,
                        [[x1, 85], [x1 + x2, 85], [x1 + x2, 104], [x1, 104]])
    if game_stats.quest_area == "Quest messages":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[x1, 85], [x1 + x2, 85], [x1 + x2, 104], [x1, 104]], 2)

    text_panel1 = font16.render("Quest messages", True, DarkText)
    screen.blit(text_panel1, [x1 + 19, 85])

    # Diplomatic messages
    x1 = 188
    pygame.draw.polygon(screen, FillButton,
                        [[x1, 85], [x1 + x2, 85], [x1 + x2, 104], [x1, 104]])
    if game_stats.quest_area == "Diplomatic messages":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[x1, 85], [x1 + x2, 85], [x1 + x2, 104], [x1, 104]], 2)

    text_panel1 = font16.render("Diplomatic messages", True, DarkText)
    screen.blit(text_panel1, [x1 + 4, 85])

    # Draw area content
    det_quest_log.area_management(screen)


def diplomacy_panel(screen):
    power = game_stats.realm_inspection

    # Draw top left panel with interface to participate in diplomacy
    pygame.draw.polygon(screen, MainMenuColor,
                        [[34, 80], [679, 80], [679, 540], [34, 540]])

    # Buttons - diplomacy interface area
    # Close diplomacy window
    pygame.draw.polygon(screen, CancelFieldColor, [[655, 85], [674, 85], [674, 104], [655, 104]])
    pygame.draw.polygon(screen, CancelElementsColor, [[655, 85], [674, 85], [674, 104], [655, 104]], 2)
    pygame.draw.line(screen, CancelElementsColor, [658, 88], [671, 101], 2)
    pygame.draw.line(screen, CancelElementsColor, [658, 101], [671, 88], 2)

    # Draw area content
    det_diplomacy.area_management(screen, power)


def war_panel(screen):
    # Draw top left panel with interface to interact with selected war
    pygame.draw.polygon(screen, MainMenuColor,
                        [[34, 80], [679, 80], [679, 540], [34, 540]])

    # Buttons - war interface area
    # Close war window
    pygame.draw.polygon(screen, CancelFieldColor, [[655, 85], [674, 85], [674, 104], [655, 104]])
    pygame.draw.polygon(screen, CancelElementsColor, [[655, 85], [674, 85], [674, 104], [655, 104]], 2)
    pygame.draw.line(screen, CancelElementsColor, [658, 88], [671, 101], 2)
    pygame.draw.line(screen, CancelElementsColor, [658, 101], [671, 88], 2)

    # Draw war interface
    det_war.draw_war(screen)


def game_board_screen(screen):
    screen.fill(MapLimitColor)  # background

    draw_tiles(screen)  # Draw tiles

    yVar = game_stats.game_window_height - 800

    ## Buttons

    # Exit
    pygame.draw.polygon(screen, FillButton, [[1150, 10], [1250, 10], [1250, 32], [1150, 32]])
    pygame.draw.polygon(screen, BorderNewGameColor, [[1150, 10], [1250, 10], [1250, 32], [1150, 32]], 3)

    text_NewGame1 = font20.render("Exit", True, TitleText)
    screen.blit(text_NewGame1, [1180, 10])

    # Save
    pygame.draw.polygon(screen, FillButton, [[1040, 10], [1140, 10], [1140, 32], [1040, 32]])
    pygame.draw.polygon(screen, BorderNewGameColor, [[1040, 10], [1140, 10], [1140, 32], [1040, 32]], 3)

    text_NewGame1 = font20.render("Save", True, TitleText)
    screen.blit(text_NewGame1, [1070, 10])

    # Next turn - hourglass icon
    # print("Hourglass")
    if not game_stats.turn_hourglass:
        hourglass_img = game_stats.gf_misc_img_dict["Icons/hourglass_false"]
    else:
        hourglass_img = game_stats.gf_misc_img_dict["Icons/hourglass_true"]
    screen.blit(hourglass_img, (1005, 5))

    # Calendar
    pygame.draw.polygon(screen, MainMenuColorDark1, [[910, 7], [1000, 7], [1000, 55], [910, 55]])
    text_NewGame2 = font20.render("Year", True, TitleText)
    screen.blit(text_NewGame2, [913, 8])
    text_NewGame2 = font20.render(str(game_stats.game_year), True, TitleText)
    screen.blit(text_NewGame2, [980, 8])
    text_NewGame2 = font20.render("Month", True, TitleText)
    screen.blit(text_NewGame2, [913, 32])
    text_NewGame2 = font20.render(str(game_stats.game_month), True, TitleText)
    screen.blit(text_NewGame2, [980, 32])

    # Players realms available resources
    treasury = None
    for realm in game_obj.game_powers:
        # print(str(realm.name))
        # print(str(game_stats.player_power))
        if realm.name == game_stats.player_power:
            # print(str(treasury))
            treasury = realm.coffers
            break

    # Left ribbon menu
    pygame.draw.polygon(screen, MainMenuColorDark1, [[0, 0], [31, 0], [31, 119], [0, 119]])

    # Button - realm
    icon_img = game_stats.gf_misc_img_dict["Icons/crown"]
    screen.blit(icon_img, (4, 4))

    # Button - tasks
    if game_stats.new_tasks:
        icon_img = game_stats.gf_misc_img_dict["Icons/new_task_scroll"]
        screen.blit(icon_img, (4, 29))
    else:
        icon_img = game_stats.gf_misc_img_dict["Icons/old_task_scroll"]
        screen.blit(icon_img, (4, 29))

    # Button - Diplomacy
    icon_img = game_stats.gf_misc_img_dict["Icons/diplomacy"]
    screen.blit(icon_img, (4, 54))

    # Top ribbon
    pygame.draw.polygon(screen, MainMenuColorDark1, [[41, 0], [600, 0], [600, 20], [41, 20]])

    if len(treasury) > 0:
        x_shift = 80
        x_points = 0
        for resource in treasury:
            # Resource icon
            # print(str(resource[0]))
            icon_img = game_stats.gf_misc_img_dict[resources_icons[resource[0]]]
            screen.blit(icon_img, (46 + x_shift * x_points, 4))

            # Resource quantity
            text_NewGame2 = font16.render(str(resource[1]), True, DarkText)
            screen.blit(text_NewGame2, (66 + x_shift * x_points, 1))

            x_points += 1

    # War symbols
    for num in range(0, 4):
        # if num < 5:
        note_index = num + game_stats.war_notifications_index
        if note_index < len(game_stats.ongoing_wars):
            x = 15 + num * 43 + 6
            y = 750 + yVar
            pygame.draw.polygon(screen, FlagColors[game_stats.ongoing_wars[note_index][0]],
                                [[x, y], [x + 29, y],
                                 [x + 29, y + 11], [x, y + 11]])
            pygame.draw.polygon(screen, FlagColors[game_stats.ongoing_wars[note_index][1]],
                                [[x, y + 12], [x + 29, y + 12],
                                 [x + 29, y + 22], [x, y + 22]])

            icon_img = game_stats.gf_misc_img_dict["Icons/sword_and_axe_icon"]
            screen.blit(icon_img, (15 + num * 43, 765 + yVar))

    if len(game_stats.ongoing_wars) > 4:
        icon_img = game_stats.gf_misc_img_dict["Icons/chevron_left"]
        screen.blit(icon_img, (2, 762 + yVar))

        icon_img = game_stats.gf_misc_img_dict["Icons/chevron_right"]
        screen.blit(icon_img, (187, 762 + yVar))

    # Timer time
    if game_stats.show_time:
        text_NewGame2 = font20.render(str(math.floor(game_stats.passed_time / 1000)), True, TitleText)
        screen.blit(text_NewGame2, [400, 30])
        text_NewGame2 = font20.render(str(game_stats.display_time), True, TitleText)
        screen.blit(text_NewGame2, [400, 70])

    # Information panel
    # Displayed when player makes left click on game map choosing army, settlement or facility

    if game_stats.selected_object != "":
        info_panels[game_stats.selected_object](screen)

    ## Panels
    # print("game_board_panel - " + game_stats.game_board_panel)
    if game_stats.game_board_panel != "":
        if game_stats.game_board_panel in draw_panel:
            draw_panel[game_stats.game_board_panel](screen)
        else:
            draw_panel_ext[game_stats.game_board_panel](screen)

    ## Right window with information
    if game_stats.right_window != "":
        draw_right_window[game_stats.right_window](screen)

    ## Banners
    # Pause
    if game_stats.pause_status:
        text_panel = font20.render("Pause", True, TitleText)
        screen.blit(text_panel, [50, 64])

    # # FPS
    # clock = pygame.time.Clock()
    # fps = clock.get_fps()
    # text_panel = font20.render(str(fps), True, TitleText)
    # screen.blit(text_panel, [10, 44])
    if game_stats.fps_status:
        text_panel = font20.render(str(game_stats.fps), True, TitleText)
        screen.blit(text_panel, [50, 84])


draw_panel = {"begin battle panel": begin_battle_panel,
              "settlement panel": settlement_panel,
              "army exchange panel": army_exchange_panel,
              "quest log panel": quest_log_panel,
              "settlement blockade panel": settlement_blockade_panel,
              "realm panel": realm_panel,
              "diplomacy panel": diplomacy_panel,
              "war panel": war_panel,
              "autobattle conclusion panel": win_autobattle_conclusion.autobattle_conclusion_panel}

draw_panel_ext = {  # Bonus
    "mythic monolith event panel": mythic_monolith_win.mythic_monolith_draw_panel,
    "stone circle event panel": stone_circle_win.stone_circle_draw_panel,
    "scholar's tower event panel": scholars_tower_win.scholars_tower_draw_panel,
    "stone well event panel": stone_well_win.stone_well_draw_panel,
    "burial mound event panel": burial_mound_win.burial_mound_draw_panel,
    "angler's cabin event panel": anglers_cabin_win.anglers_cabin_draw_panel,
    # Lair
    "runaway serfs refuge event panel": runaway_serfs_refuge_win.runaway_serfs_refuge_draw_panel,
    "treasure tower event panel": treasure_tower_win.treasure_tower_draw_panel,
    "lair of grey dragons event panel": lair_of_grey_dragons_win.lair_of_grey_dragons_draw_panel,
    # Battle result lair
    "runaway serfs refuge result panel": runaway_serfs_refuge_result_win.runaway_serfs_refuge_result_draw_panel,
    "treasure tower result panel": treasure_tower_result_win.treasure_tower_result_draw_panel,
    "lair of grey dragons result panel": lair_of_grey_dragons_result_win.lair_of_grey_dragons_result_draw_panel,
    "slay the grey dragon result panel": slay_the_grey_dragon_result_win.slay_the_grey_dragon_result_draw_panel,
    # Quest result message
    "poachers in royal forest result panel": poachers_in_royal_forest_result_win.poachers_in_royal_forest_result_draw_panel}

info_panels = {"Army": army_panel,
               "Tile": tile_obj_panel,
               "Settlement": settlement_info_panel}

draw_right_window = {"Building upgrade information": rw_upgrade_building.draw_upgrade_info,
                     "Building information": rw_building.draw_building_info,
                     "New regiment information": rw_new_regiment_information.new_regiment_info,
                     "New hero skill tree": rw_new_hero_skill_tree.skill_tree_info,
                     "Hero window": rw_hero_window.draw_hero_window}
