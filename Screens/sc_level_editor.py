## Miracle battles!
## sc_level_editor

import pygame.draw, pygame.font, math
from Resources import game_stats
from Resources import faction_classes
from Content import terrain_catalog
from Content import faction_names
from Content import alinement_info
from Content import city_catalog
from Content import units_info
from Content import objects_img_catalog
from Content import terrain_seasons
from Content import facility_catalog
from Content import exploration_catalog
from Content import realm_leader_traits

pygame.init()

WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
NewGameColor = [0x8D, 0x86, 0x86]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]

BorderNewGameColor = [0xDA, 0xAE, 0x83]
FillButton = [0xD8, 0xBD, 0xA2]
HighlightBorder = [0xF7, 0x82, 0x0C]
FieldColor = [0xA0, 0xA0, 0xA0]
ApproveFieldColor = [0x00, 0x99, 0x00]
ApproveElementsColor = [0x00, 0x66, 0x00]
CancelFieldColor = [0xFF, 0x00, 0x00]
CancelElementsColor = [0x99, 0x00, 0x00]
arrow_green = (0, 102, 0, 180)

MapLimitColor = [0xDE, 0xB8, 0x87]  # DEB887
TileBorder = [11, 11, 11, 200]  # 0x0B, 0x0B, 0x0B
WhiteBorder = [249, 238, 227, 200]
OwnControlZone = [51, 255, 255, 100]
DiffControlZone = [255, 255, 102, 100]

Plain_Summer_Color = [0x4C, 0x99, 0x00]
Plain_Autumn_Color = [0xFD, 0xE1, 0x2A]
Plain_Early_Winter_Color = [0x1B, 0x40, 0x2A]
Plain_Winter_Color = [0xE6, 0xEB, 0xF7]
Plain_Spring_Color = [0x2B, 0xB7, 0x42]
Northland_Winter_Color = [0xF3, 0xF3, 0xF3]
Northland_Melting_Spring_Color = [0x70, 0x90, 0x9F]
Northland_Spring_Color = [0x44, 0xA8, 0x76]
Northland_Summer_Color = [0x35, 0x86, 0x1D]
Northland_Autumn_Color = [0xB8, 0xBD, 0x28]
Northland_Early_Winter_Color = [0x5E, 0x49, 0x17]
Northland_Winter_Color = [0x5E, 0x49, 0x17]

Earthen_Road = [0xA4, 0x81, 0x6E]

RockTunel = [0x89, 0x89, 0x89]
MonolithTunel = [0x24, 0x27, 0x3D]

HighlightOption = [0x00, 0xCC, 0xCC]
HighlightRemoval = [0xFF, 0x1A, 0x1A]

FlagpoleColor = (139, 105, 12, 160)
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

TerrainColors = {"Plain_Summer": Plain_Summer_Color,
                 "Plain_Autumn": Plain_Autumn_Color,
                 "Plain_Early_Winter": Plain_Early_Winter_Color,
                 "Plain_Winter": Plain_Winter_Color,
                 "Plain_Spring": Plain_Spring_Color,
                 "Northlands_Winter": Northland_Winter_Color,
                 "Northlands_Melting_Spring": Northland_Melting_Spring_Color,
                 "Northlands_Spring": Northland_Spring_Color,
                 "Northlands_Summer": Northland_Summer_Color,
                 "Northlands_Autumn": Northland_Autumn_Color,
                 "Northlands_Early_Winter": Northland_Early_Winter_Color}

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
font12 = pygame.font.SysFont('timesnewroman', 10)


# Function to draw transparent rectangle
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_tiles(screen):
    if len(game_stats.level_map) > 0:
        for x in range(0, 27):
            for y in range(0, math.ceil(game_stats.game_window_height / 48)):
                num_x = x + game_stats.pov_pos[0]
                num_y = y + game_stats.pov_pos[1]
                if 0 < num_x <= game_stats.new_level_width and 0 < num_y <= game_stats.new_level_height:
                    TileNum = (num_y - 1) * game_stats.new_level_width + num_x - 1
                    TileObj = game_stats.level_map[TileNum]

                    # Terrain
                    terrain_img = game_stats.gf_terrain_dict[TileObj.conditions]
                    screen.blit(terrain_img, ((x - 1) * 48 + 1, (y - 1) * 48 + 1))

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

                    # Border line
                    pygame.draw.polygon(screen, TileBorder,
                                        [[(x - 1) * 48 + 1, (y - 1) * 48 + 1], [(x - 1) * 48 + 48, (y - 1) * 48 + 1],
                                         [(x - 1) * 48 + 48, (y - 1) * 48 + 48], [(x - 1) * 48 + 1, (y - 1) * 48 + 48]], 1)

        for x in range(0, 27):
            for y in range(0, math.ceil(game_stats.game_window_height / 48)):
                num_x = x + game_stats.pov_pos[0]
                num_y = y + game_stats.pov_pos[1]
                if 0 < num_x <= game_stats.new_level_width and 0 < num_y <= game_stats.new_level_height:
                    TileNum = (num_y - 1) * game_stats.new_level_width + num_x - 1
                    TileObj = game_stats.level_map[TileNum]

                    # Cities
                    if TileObj.lot is not None:
                        if TileObj.lot == "City":
                            for city in game_stats.editor_cities:
                                if city.city_id == TileObj.city_id:
                                    city_img = game_stats.gf_settlement_dict[city_catalog.city_cat[city.alignment]]
                                    screen.blit(city_img, ((x - 1) * 48 + 1, (y - 1) * 48 + 1))

                                    # Name
                                    indent = int(len(city.name) * 2)
                                    text_panel1 = font12.render(city.name, True, TitleText)
                                    screen.blit(text_panel1, ((x - 1) * 48 + 24 - indent, (y - 1) * 48 + 50))

                                    # Flag
                                    if city.owner != "Neutral":
                                        for power in game_stats.editor_powers:
                                            if city.owner == power.name:
                                                pygame.draw.polygon(screen, FlagpoleColor,
                                                                    ([(x - 1) * 48 + 3, (y - 1) * 48 + 32],
                                                                     [(x - 1) * 48 + 4, (y - 1) * 48 + 32],
                                                                     [(x - 1) * 48 + 4, (y - 1) * 48 + 48],
                                                                     [(x - 1) * 48 + 3, (y - 1) * 48 + 48]))
                                                pygame.draw.polygon(screen, FlagColors[power.f_color],
                                                                    ([(x - 1) * 48 + 5, (y - 1) * 48 + 32],
                                                                     [(x - 1) * 48 + 11, (y - 1) * 48 + 32],
                                                                     [(x - 1) * 48 + 11, (y - 1) * 48 + 36],
                                                                     [(x - 1) * 48 + 5, (y - 1) * 48 + 36]))
                                                pygame.draw.polygon(screen, FlagColors[power.s_color],
                                                                    ([(x - 1) * 48 + 5, (y - 1) * 48 + 37],
                                                                     [(x - 1) * 48 + 11, (y - 1) * 48 + 37],
                                                                     [(x - 1) * 48 + 11, (y - 1) * 48 + 41],
                                                                     [(x - 1) * 48 + 5, (y - 1) * 48 + 41]))
                        else:
                            if TileObj.lot.obj_typ == "Obstacle":
                                for item in TileObj.lot.disposition:
                                    obj_cal = objects_img_catalog.object_calendar[TileObj.lot.obj_name]
                                    season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.LE_month]
                                    obj_img = game_stats.gf_obstacle_dict[obj_cal[season] + "_0" + item[2]]
                                    screen.blit(obj_img, ((x - 1) * 48 + item[0] - obj_img.get_width()/2,
                                                          (y - 1) * 48 + item[1] - obj_img.get_height()/2))

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

                    # Armies
                    if TileObj.army_id is not None:
                        focus = TileObj.army_id

                        for army in game_stats.editor_armies:
                            if army.army_id == focus:
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
                                        # print(army_img.get_alpha())  # Check alpha channel on image
                                        # x_num = 0
                                        # while x_num < 5:
                                        #     y_num = 0
                                        #     while y_num < 4:
                                        #         screen.blit(army_img,
                                        #                     ((x - 1) * 48 + 5 + (86 / 5) * x_num,
                                        #                      (y - 1) * 48 + 4 + (88 / 4) * y_num))
                                        #         y_num += 1
                                        #     x_num += 1
                                    else:
                                        text_panel1 = font12.render("No units", True, CancelFieldColor)
                                        screen.blit(text_panel1, ((x - 1) * 48 + 5, (y - 1) * 48 + 19))

                                    if army.owner != "Neutral":  # Draw flag
                                        for power in game_stats.editor_powers:
                                            if army.owner == power.name:
                                                pygame.draw.polygon(screen, FlagpoleColor,
                                                                    ([(x - 1) * 48 + 3,
                                                                      (y - 1) * 48 + 32],
                                                                     [(x - 1) * 48 + 4,
                                                                      (y - 1) * 48 + 32],
                                                                     [(x - 1) * 48 + 4 ,
                                                                      (y - 1) * 48 + 48 ],
                                                                     [(x - 1) * 48 + 3,
                                                                      (y - 1) * 48 + 48]))
                                                pygame.draw.polygon(screen, FlagColors[power.f_color],
                                                                    ([(x - 1) * 48 + 5,
                                                                      (y - 1) * 48 + 32],
                                                                     [(x - 1) * 48 + 11,
                                                                      (y - 1) * 48 + 32],
                                                                     [(x - 1) * 48 + 11,
                                                                      (y - 1) * 48 + 36],
                                                                     [(x - 1) * 48 + 5,
                                                                      (y - 1) * 48 + 36]))
                                                pygame.draw.polygon(screen, FlagColors[power.s_color],
                                                                    ([(x - 1) * 48 + 5,
                                                                      (y - 1) * 48 + 37],
                                                                     [(x - 1) * 48 + 11,
                                                                      (y - 1) * 48 + 37],
                                                                     [(x - 1) * 48 + 11,
                                                                      (y - 1) * 48 + 41],
                                                                     [(x - 1) * 48 + 5,
                                                                      (y - 1) * 48 + 41]))


def create_city_lower_panel(screen, focus):
    # print("selected_city_id - " + str(game_stats.selected_city_id))
    if game_stats.edit_instrument in ["draw control zone", "remove control zone"]:
        for TileObj in game_stats.level_map:
            x = TileObj.posxy[0]
            y = TileObj.posxy[1]
            x -= int(game_stats.pov_pos[0])
            y -= int(game_stats.pov_pos[1])

            if 0 < x <= 27 and 0 < y <= math.ceil(game_stats.game_window_height):
                if TileObj.city_id == game_stats.last_city_id:
                    draw_rect_alpha(screen, OwnControlZone,
                                    ((x - 1) * 48 + 1, (y - 1) * 48 + 1, 48, 48))
                elif TileObj.city_id is not None:
                    if TileObj.city_id != game_stats.last_city_id:
                        draw_rect_alpha(screen, DiffControlZone,
                                        ((x - 1) * 48 + 1, (y - 1) * 48 + 1, 48, 48))

    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 600 + yVar], [1080, 600 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    the_city = None
    for city in game_stats.editor_cities:
        if city.city_id == focus:
            the_city = city

    # City's name
    text_panel = font20.render(the_city.name, True, TitleText)
    screen.blit(text_panel, [210, 604 + yVar])

    # Alignment
    text_panel = font20.render(the_city.alignment, True, TitleText)
    screen.blit(text_panel, [210, 634 + yVar])

    if the_city.owner == "Neutral":
        text_panel = font20.render("Neutral", True, TitleText)
        screen.blit(text_panel, [240, 664 + yVar])
    else:
        for power in game_stats.editor_powers:
            if power.name == the_city.owner:
                # Country's name
                text_panel = font20.render(power.name, True, TitleText)
                screen.blit(text_panel, [240, 664 + yVar])

                # Flag
                pygame.draw.polygon(screen, FlagColors[power.f_color],
                                    [[205, 664 + yVar], [235, 664 + yVar], [235, 675 + yVar],
                                     [205, 675 + yVar]])
                pygame.draw.polygon(screen, FlagColors[power.s_color],
                                    [[205, 676 + yVar], [235, 676 + yVar], [235, 686 + yVar],
                                     [205, 686 + yVar]])

    # Delete city
    pygame.draw.polygon(screen, CancelFieldColor,
                        [[202, 694 + yVar], [260, 694 + yVar], [260, 715 + yVar], [202, 715 + yVar]])
    pygame.draw.polygon(screen, CancelElementsColor,
                        [[202, 694 + yVar], [260, 694 + yVar], [260, 715 + yVar], [202, 715 + yVar]], 3)
    text_panel = font20.render("Delete", True, DarkText)
    screen.blit(text_panel, [205, 694 + yVar])

    # Control zone
    pygame.draw.polygon(screen, FieldColor,
                        [[202, 724 + yVar], [270, 724 + yVar], [270, 745 + yVar], [202, 745 + yVar]])
    if game_stats.edit_instrument == "draw control zone":
        color1 = HighlightOption
    elif game_stats.edit_instrument == "remove control zone":
        color1 = CancelElementsColor
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1,
                        [[202, 724 + yVar], [270, 724 + yVar], [270, 745 + yVar], [202, 745 + yVar]], 3)
    text_panel = font20.render("Control", True, DarkText)
    screen.blit(text_panel, [205, 724 + yVar])

    # Buildings
    pygame.draw.polygon(screen, FieldColor,
                        [[202, 754 + yVar], [285, 754 + yVar], [285, 775 + yVar], [202, 775 + yVar]])
    if game_stats.level_editor_left_panel == "building menu left panel":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1,
                        [[202, 754 + yVar], [285, 754 + yVar], [285, 775 + yVar], [202, 775 + yVar]], 3)
    text_panel = font20.render("Buildings", True, DarkText)
    screen.blit(text_panel, [205, 754 + yVar])

    # Button - Population view
    pygame.draw.polygon(screen, FillButton,
                        [[355, 603 + yVar], [493, 603 + yVar], [493, 625 + yVar], [355, 625 + yVar]])
    if game_stats.settlement_option_view == "Population":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[355, 603 + yVar], [493, 603 + yVar], [493, 625 + yVar], [355, 625 + yVar]], 3)
    text_panel1 = font20.render("Population", True, DarkText)
    screen.blit(text_panel1, [380, 603 + yVar])

    # Button - Factions view
    pygame.draw.polygon(screen, FillButton,
                        [[503, 603 + yVar], [641, 603 + yVar], [641, 625 + yVar], [503, 625 + yVar]])
    if game_stats.settlement_option_view == "Factions":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[503, 603 + yVar], [641, 603 + yVar], [641, 625 + yVar], [503, 625 + yVar]], 3)
    text_panel1 = font20.render("Factions", True, DarkText)
    screen.blit(text_panel1, [533, 603 + yVar])

    if game_stats.settlement_option_view == "Population":
        yPos = 0
        for pops in the_city.residency:
            # Population's name
            text_panel = font20.render(pops.name, True, DarkText)
            screen.blit(text_panel, [360, 664 + yVar + yPos])

            yPos += 30

        # White line
        pygame.draw.lines(screen, WhiteBorder, False, [(360, 686 + yVar + 30 * game_stats.population_l_p_index),
                                                       (450, 686 + yVar + 30 * game_stats.population_l_p_index)], 1)

        # Property
        text_panel = font20.render("Property:", True, TitleText)
        screen.blit(text_panel, [480, 634 + yVar])

        yPos = 0
        for resource in the_city.residency[game_stats.population_l_p_index].reserve:
            # Resources
            text_panel = font16.render(resource[0] + " - " + str(resource[1]), True, DarkText)
            screen.blit(text_panel, [480, 664 + yVar + yPos])

            yPos += 27

        # Faction membership
        text_panel = font20.render("Faction:", True, TitleText)
        screen.blit(text_panel, [610, 634 + yVar])

        pop_name = the_city.residency[game_stats.population_l_p_index].name
        text_panel = font16.render(faction_classes.pop_membership[pop_name], True, DarkText)
        screen.blit(text_panel, [610, 664 + yVar])

    elif game_stats.settlement_option_view == "Factions":
        yPos = 0
        for faction in the_city.factions:
            # Faction's name
            text_panel = font20.render(faction.title_name, True, DarkText)
            screen.blit(text_panel, [360, 664 + yVar + yPos])

            yPos += 30

        # White line
        pygame.draw.lines(screen, WhiteBorder, False, [(360, 686 + yVar + 30 * game_stats.faction_l_p_index),
                                                       (620, 686 + yVar + 30 * game_stats.faction_l_p_index)], 1)

        # Population
        text_panel = font20.render("Population:", True, TitleText)
        screen.blit(text_panel, [630, 634 + yVar])

        yPos = 0
        for pop_info in the_city.factions[game_stats.faction_l_p_index].members:
            # Population's name
            text_panel = font16.render(pop_info[1] + " - " + str(pop_info[0]), True, DarkText)
            screen.blit(text_panel, [630, 664 + yVar + yPos])
            yPos += 27


def create_city_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 400], [1040, 400]])

    # White border around selected tile
    x2 = int(game_stats.selected_tile[0])
    y2 = int(game_stats.selected_tile[1])
    x2 -= int(game_stats.pov_pos[0])
    y2 -= int(game_stats.pov_pos[1])
    # Border line
    pygame.draw.polygon(screen, WhiteBorder,
                        [[(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 1], [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 1],
                         [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 48], [(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 48]], 1)

    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    # Label - City name
    text_panel1 = font20.render("City name:", True, TitleText)
    screen.blit(text_panel1, [1060, 74])

    # Result text - name of new city
    text_panel2 = font20.render(str(game_stats.new_city_name), True, TitleText)
    screen.blit(text_panel2, [1060, 104])

    # Name field

    pygame.draw.polygon(screen, FieldColor, [[1044, 134], [1184, 134], [1184, 166], [1044, 166]])
    if game_stats.active_city_name_field == False:
        pygame.draw.polygon(screen, BorderNewGameColor, [[1044, 134], [1184, 134], [1184, 166], [1044, 166]], 3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[1044, 134], [1184, 134], [1184, 166], [1044, 166]], 3)

    if game_stats.active_city_name_field == True:
        if len(game_stats.input_text) > 0:
            if game_stats.input_text != game_stats.boxed_city_name:
                game_stats.boxed_city_name = str(game_stats.input_text)
    text_panel3 = font20.render(str(game_stats.boxed_city_name), True, TitleText)
    screen.blit(text_panel3, [1054, 136])

    # Approve city name field

    pygame.draw.polygon(screen, ApproveFieldColor, [[1194, 134], [1226, 134], [1226, 166], [1194, 166]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[1194, 134], [1226, 134], [1226, 166], [1194, 166]], 3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(1198, 150), (1206, 162), (1221, 138)], 3)

    # Cancel city name field

    pygame.draw.polygon(screen, CancelFieldColor, [[1234, 134], [1266, 134], [1266, 166], [1234, 166]])
    pygame.draw.polygon(screen, CancelElementsColor, [[1234, 134], [1266, 134], [1266, 166], [1234, 166]], 3)
    pygame.draw.line(screen, CancelElementsColor, [1237, 138], [1263, 162], 3)
    pygame.draw.line(screen, CancelElementsColor, [1237, 162], [1263, 138], 3)

    # Label - Alignment
    text_panel4 = font20.render("Alignment:", True, TitleText)
    screen.blit(text_panel4, [1060, 174])

    # Option box - Alignment
    pygame.draw.polygon(screen, FieldColor, [[1044, 204], [1266, 204], [1266, 226], [1044, 226]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1044, 204], [1266, 204], [1266, 226], [1044, 226]], 3)
    text_panel5 = font20.render(alinement_info.alinements_list[game_stats.option_box_alinement_index], True, DarkText)
    screen.blit(text_panel5, [1050, 204])

    # Button - Next alignment from a list
    pygame.draw.polygon(screen, FillButton, [[1180, 174], [1266, 174], [1266, 196], [1180, 196]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1180, 174], [1266, 174], [1266, 196], [1180, 196]], 3)
    text_panel6 = font20.render("Next", True, DarkText)
    screen.blit(text_panel6, [1200, 174])

    # Label - Country name
    text_panel7 = font20.render("Country:", True, TitleText)
    screen.blit(text_panel7, [1060, 234])

    if len(game_stats.editor_powers) > 0:
        pygame.draw.polygon(screen, FlagColors[game_stats.editor_powers[game_stats.powers_l_p_index].f_color],
                            [[1044, 264], [1066, 264], [1066, 275], [1044, 275]])
        pygame.draw.polygon(screen, FlagColors[game_stats.editor_powers[game_stats.powers_l_p_index].s_color],
                            [[1044, 276], [1066, 276], [1066, 286], [1044, 286]])

    # Option box - Country
    pygame.draw.polygon(screen, FieldColor, [[1070, 264], [1266, 264], [1266, 286], [1070, 286]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1070, 264], [1266, 264], [1266, 286], [1070, 286]], 3)
    if len(game_stats.editor_powers) > 0:
        text_panel8 = font20.render(game_stats.editor_powers[game_stats.powers_l_p_index].name, True, DarkText)
        screen.blit(text_panel8, [1075, 264])

    # Buttons - previous and next country to choose

    pygame.draw.polygon(screen, RockTunel, [[1214, 234], [1236, 234], [1236, 256], [1214, 256]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1214, 234], [1236, 234], [1236, 256], [1214, 256]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1232, 238), (1218, 245), (1232, 252)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 234], [1266, 234], [1266, 256], [1244, 256]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 234], [1266, 234], [1266, 256], [1244, 256]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 238), (1262, 245), (1248, 252)], 2)

    # Button - City's allegiance
    pygame.draw.polygon(screen, FillButton, [[1044, 294], [1140, 294], [1140, 316], [1044, 316]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1044, 294], [1140, 294], [1140, 316], [1044, 316]], 3)
    text_panel9 = font20.render(game_stats.city_allegiance, True, DarkText)
    screen.blit(text_panel9, [1060, 294])

    # Button - Create city
    pygame.draw.polygon(screen, FillButton,
                        [[1148, 294], [1266, 294], [1266, 316], [1148, 316]])
    if game_stats.level_map[TileNum].lot is None and game_stats.new_city_name != "":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[1148, 294], [1266, 294], [1266, 316], [1148, 316]], 3)
    text_panel1 = font20.render("Create city", True, DarkText)
    screen.blit(text_panel1, [1158, 294])

    # Lower panel with detailed information about city
    if game_stats.lower_panel == "create city lower panel":
        create_city_lower_panel(screen, game_stats.selected_city_id)


def building_menu_left_panel(screen):
    # Draw top left panel with interface to interact with settlement buildings
    pygame.draw.polygon(screen, MainMenuColor,
                        [[1, 80], [639, 80], [639, 430], [1, 430]])

    # Buttons - settlement interface area
    # Close settlement window
    pygame.draw.polygon(screen, CancelFieldColor, [[615, 85], [634, 85], [634, 104], [615, 104]])
    pygame.draw.polygon(screen, CancelElementsColor, [[615, 85], [634, 85], [634, 104], [615, 104]], 2)
    pygame.draw.line(screen, CancelElementsColor, [618, 88], [631, 101], 2)
    pygame.draw.line(screen, CancelElementsColor, [618, 101], [631, 88], 2)

    settlement = None
    for city in game_stats.editor_cities:
        if city.city_id == game_stats.selected_city_id:
            settlement = city
            break

    for plot in settlement.buildings:
        xy = plot.screen_position

        # Draw only 4 rows of plot at a time
        if game_stats.building_row_index < xy[1] <= game_stats.building_row_index + 3:
            x1 = 5 + 153 * (xy[0] - 1)
            x2 = x1 + 143
            y1 = 112 + 108 * (xy[1] - 1 - game_stats.building_row_index)
            y2 = y1 + 100
            x3 = x1 + 5
            y3 = y1 + 78

            pygame.draw.polygon(screen, FillButton,
                                [[x1, y1],
                                 [x2, y1],
                                 [x2, y2 - 26],
                                 [x1, y2 - 26]])
            pygame.draw.polygon(screen, FieldColor,
                                [[x1, y1 + 75],
                                 [x2, y1 + 75],
                                 [x2, y2],
                                 [x1, y2]])
            pygame.draw.polygon(screen, LineMainMenuColor1,
                                [[x1, y1],
                                 [x2, y1],
                                 [x2, y2],
                                 [x1, y2]],
                                2)

            pygame.draw.polygon(screen, LineMainMenuColor1,
                                [[x1, y1 + 75],
                                 [x2, y1 + 75]],
                                1)

            pygame.draw.polygon(screen, LineMainMenuColor1,
                                [[x1 + 35, y1 + 75],
                                 [x1 + 35, y2]],
                                1)

            # Buttons - previous and next building row
            pygame.draw.polygon(screen, RockTunel, [[615, 112], [634, 112], [634, 131], [615, 131]])
            pygame.draw.polygon(screen, LineMainMenuColor1, [[615, 112], [634, 112], [634, 131], [615, 131]], 2)
            pygame.draw.lines(screen, LineMainMenuColor1, False, [(619, 128), (625, 115), (631, 128)], 2)

            pygame.draw.polygon(screen, RockTunel, [[615, 407], [634, 407], [634, 426], [615, 426]])
            pygame.draw.polygon(screen, LineMainMenuColor1, [[615, 407], [634, 407], [634, 426], [615, 426]], 2)
            pygame.draw.lines(screen, LineMainMenuColor1, False, [(619, 410), (625, 424), (631, 410)], 2)

            # Upgrade icon in lower part of structure card
            if plot.upgrade is not None:
                pygame.draw.polygon(screen, arrow_green,
                                    [[x3 + 8, y3 + 20],
                                     [x3 + 8, y3 + 15],
                                     [x3 + 2, y3 + 15],
                                     [x3 + 12, y3],
                                     [x3 + 13, y3],
                                     [x3 + 23, y3 + 15],
                                     [x3 + 17, y3 + 15],
                                     [x3 + 17, y3 + 20]])

            # Buildings title
            if plot.structure is None:
                text_panel1 = font12.render("Empty", True, DarkText)
                screen.blit(text_panel1, [x1 + 55, y1 + 3])
            else:
                # Buildings title
                y_shift = 10
                y_points = 0
                for text_line in plot.structure.title_name:
                    text_panel1 = font12.render(str(text_line), True, DarkText)
                    screen.blit(text_panel1, [x1 + 55, y1 + 3 + y_shift * y_points])
                    y_points += 1

                # Draw existing buildings in structure card
                # Icon image
                structure_img = game_stats.gf_building_dict[plot.structure.name]
                screen.blit(structure_img, (x1 + 3, y1 + 3))


def population_lower_panel(screen):
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[400, 600 + yVar], [880, 600 + yVar], [880, 800 + yVar], [400, 800 + yVar]])

    # Population
    text_panel = font20.render("Population", True, TitleText)
    screen.blit(text_panel, [410, 604 + yVar])

    yPos = 0
    for pops in game_stats.lot_information.residency:
        # Population's name
        # print(pops)
        text_panel = font20.render(pops.name, True, DarkText)
        screen.blit(text_panel, [410, 634 + yVar + yPos])

        yPos += 30

    # White line
    pygame.draw.lines(screen, WhiteBorder, False, [(410, 656 + yVar + 30 * game_stats.population_l_p_index),
                                                   (500, 656 + yVar + 30 * game_stats.population_l_p_index)], 1)

    # Property
    text_panel = font20.render("Property:", True, TitleText)
    screen.blit(text_panel, [530, 604 + yVar])

    yPos = 0
    if len(game_stats.lot_information.residency) > 0:
        for resource in game_stats.lot_information.residency[game_stats.population_l_p_index].reserve:
            text_panel = font20.render(resource[0] + " - " + str(resource[1]), True, DarkText)
            screen.blit(text_panel, [530, 634 + yVar + yPos])

            yPos += 30


def powers_lower_panel(screen):
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 600 + yVar], [1080, 600 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    power = game_stats.editor_powers[game_stats.powers_l_p_index]

    # Country's name
    text_panel = font20.render(power.name, True, TitleText)
    screen.blit(text_panel, [210, 604 + yVar])

    # Flag
    pygame.draw.polygon(screen, FlagColors[power.f_color],
                        [[205, 634 + yVar], [235, 634 + yVar], [235, 645 + yVar], [205, 645 + yVar]])
    pygame.draw.polygon(screen, FlagColors[power.s_color],
                        [[205, 646 + yVar], [235, 646 + yVar], [235, 656 + yVar], [205, 656 + yVar]])

    # Alignment
    text_panel = font20.render(power.alignment, True, TitleText)
    screen.blit(text_panel, [245, 634 + yVar])

    # Delete country
    pygame.draw.polygon(screen, CancelFieldColor,
                        [[205, 664 + yVar], [263, 664 + yVar], [263, 685 + yVar], [205, 685 + yVar]])
    pygame.draw.polygon(screen, CancelElementsColor,
                        [[205, 664 + yVar], [263, 664 + yVar], [263, 685 + yVar], [205, 685 + yVar]], 3)
    text_panel = font20.render("Delete", True, DarkText)
    screen.blit(text_panel, [208, 664 + yVar])

    x_pos = 274
    y_pos = 664
    # Playable toggle
    border_color = CancelElementsColor
    if power.playable:
        border_color = HighlightOption
    pygame.draw.polygon(screen, FieldColor,
                        [[x_pos, y_pos + yVar], [x_pos + 76, y_pos + yVar],
                         [x_pos + 76, y_pos + 21 + yVar], [x_pos, y_pos + 21 + yVar]])
    pygame.draw.polygon(screen, border_color,
                        [[x_pos, y_pos + yVar], [x_pos + 76, y_pos + yVar],
                         [x_pos + 76, y_pos + 21 + yVar], [x_pos, y_pos + 21 + yVar]], 3)
    text_panel = font20.render("Playable", True, DarkText)
    screen.blit(text_panel, [x_pos + 3, y_pos + yVar])

    # Option box - Realm leader
    pygame.draw.polygon(screen, FieldColor,
                        [[205, 694 + yVar], [270, 694 + yVar], [270, 716 + yVar], [205, 716 + yVar]])
    pygame.draw.polygon(screen, LineMainMenuColor1,
                        [[205, 694 + yVar], [270, 694 + yVar], [270, 716 + yVar], [205, 716 + yVar]], 3)
    text_panel5 = font20.render("Leader", True, DarkText)
    screen.blit(text_panel5, [210, 694 + yVar])

    # Realm leader details
    text_panel = font20.render(power.leader.name, True, TitleText)
    screen.blit(text_panel, [401, 604 + yVar])

    # Traits
    y_base = 626 + yVar
    y_shift = 19
    y_num = 0

    # Speciality trait
    text_panel = font16.render("Speciality trait", True, TitleText)
    screen.blit(text_panel, [401, y_base + y_shift * y_num])
    y_num += 1

    y_num += 1

    # Behavior traits
    text_panel = font16.render("Behavior traits", True, TitleText)
    screen.blit(text_panel, [401, y_base + y_shift * y_num])
    y_num += 1

    text_panel = font16.render(power.leader.behavior_traits[0], True, DarkText)
    screen.blit(text_panel, [401, y_base + y_shift * y_num])
    if game_stats.realm_leader_white_line == "First behavior trait":
        pygame.draw.lines(screen, WhiteBorder, False, [(401, y_base + y_shift * y_num + 17),
                                                       (470, y_base + y_shift * y_num + 17)], 1)
    y_num += 1

    text_panel = font16.render(power.leader.behavior_traits[1], True, DarkText)
    screen.blit(text_panel, [401, y_base + y_shift * y_num])
    if game_stats.realm_leader_white_line == "Second behavior trait":
        pygame.draw.lines(screen, WhiteBorder, False, [(401, y_base + y_shift * y_num + 17),
                                                       (470, y_base + y_shift * y_num + 17)], 1)
    y_num += 1

    # Available traits
    text_panel = font20.render("Available traits", True, TitleText)
    screen.blit(text_panel, [621, 604 + yVar])

    # Traits
    y_base = 626 + yVar
    y_shift = 19
    y_num = 0

    for num in range(0, 9):
        if num + game_stats.realm_leader_traits_index + 1 <= len(game_stats.realm_leader_traits_list):
            trait = game_stats.realm_leader_traits_list[num + game_stats.realm_leader_traits_index]
            text_panel = font16.render(trait, True, DarkText)
            screen.blit(text_panel, [646, y_base + y_shift * y_num])
            y_num += 1

    # Buttons - previous and next available trait
    x_base = 621
    x_shift = 19
    y_base = 628 + yVar
    y_shift = 19
    pygame.draw.polygon(screen, RockTunel, [[x_base, y_base], [x_base + x_shift, y_base],
                                            [x_base + x_shift, y_base + y_shift], [x_base, y_base + y_shift]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_shift, y_base],
                                                     [x_base + x_shift, y_base + y_shift],
                                                     [x_base, y_base + y_shift]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(x_base + 4, y_base + 16),
                                                          (x_base + 10, y_base + 3),
                                                          (x_base + 16, y_base + 16)], 2)

    y_base = 775 + yVar
    pygame.draw.polygon(screen, RockTunel, [[x_base, y_base], [x_base + x_shift, y_base],
                                            [x_base + x_shift, y_base + y_shift], [x_base, y_base + y_shift]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_shift, y_base],
                                                     [x_base + x_shift, y_base + y_shift],
                                                     [x_base, y_base + y_shift]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(x_base + 4, y_base + 3),
                                                          (x_base + 10, y_base + 17),
                                                          (x_base + 16, y_base + 3)], 2)

    # Picked trait
    if game_stats.picked_leader_trait != "":
        text_panel = font20.render(game_stats.picked_leader_trait, True, TitleText)
        screen.blit(text_panel, [781, 604 + yVar])

        # Trait description
        y_base = 626 + yVar
        y_shift = 19
        y_num = 0

        if game_stats.realm_leader_white_line == "First behavior trait" \
            or game_stats.realm_leader_white_line == "Second behavior trait":
            if game_stats.picked_leader_trait in realm_leader_traits.behavior_traits_desc_dict:
                for text_line in realm_leader_traits.behavior_traits_desc_dict[game_stats.picked_leader_trait]:
                    text_panel = font16.render(text_line, True, DarkText)
                    screen.blit(text_panel, [781, y_base + y_shift * y_num])
                    y_num += 1

        # Button - Assign leader trait
        pygame.draw.polygon(screen, FieldColor,
                            [[781, 768 + yVar], [846, 768 + yVar], [846, 790 + yVar], [781, 790 + yVar]])
        pygame.draw.polygon(screen, LineMainMenuColor1,
                            [[781, 768 + yVar], [846, 768 + yVar], [846, 790 + yVar], [781, 790 + yVar]], 3)
        text_panel5 = font20.render("Assign", True, DarkText)
        screen.blit(text_panel5, [786, 768 + yVar])


def powers_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 495], [1040, 495]])

    # Label - New country name
    text_panel1 = font20.render("New country name:", True, TitleText)
    screen.blit(text_panel1, [1060, 74])

    # Result text - name of new country
    text_panel2 = font20.render(str(game_stats.new_country_name), True, TitleText)
    screen.blit(text_panel2, [1060, 104])

    # Name field

    pygame.draw.polygon(screen, FieldColor, [[1044, 134], [1184, 134], [1184, 166], [1044, 166]])
    if game_stats.active_country_name_field == False:
        pygame.draw.polygon(screen, BorderNewGameColor, [[1044, 134], [1184, 134], [1184, 166], [1044, 166]], 3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[1044, 134], [1184, 134], [1184, 166], [1044, 166]], 3)

    if game_stats.active_country_name_field == True:
        if len(game_stats.input_text) > 0:
            if game_stats.input_text != game_stats.boxed_country_name:
                game_stats.boxed_country_name = str(game_stats.input_text)
    text_panel3 = font20.render(str(game_stats.boxed_country_name), True, TitleText)
    screen.blit(text_panel3, [1054, 136])

    # Approve country name field

    pygame.draw.polygon(screen, ApproveFieldColor, [[1194, 134], [1226, 134], [1226, 166], [1194, 166]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[1194, 134], [1226, 134], [1226, 166], [1194, 166]], 3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(1198, 150), (1206, 162), (1221, 138)], 3)

    # Cancel country name field

    pygame.draw.polygon(screen, CancelFieldColor, [[1234, 134], [1266, 134], [1266, 166], [1234, 166]])
    pygame.draw.polygon(screen, CancelElementsColor, [[1234, 134], [1266, 134], [1266, 166], [1234, 166]], 3)
    pygame.draw.line(screen, CancelElementsColor, [1237, 138], [1263, 162], 3)
    pygame.draw.line(screen, CancelElementsColor, [1237, 162], [1263, 138], 3)

    # Label - Alignment
    text_panel4 = font20.render("Alignment:", True, TitleText)
    screen.blit(text_panel4, [1060, 174])

    # Option box - Alignment
    pygame.draw.polygon(screen, FieldColor, [[1044, 204], [1266, 204], [1266, 226], [1044, 226]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1044, 204], [1266, 204], [1266, 226], [1044, 226]], 3)
    text_panel5 = font20.render(alinement_info.alinements_list[game_stats.option_box_alinement_index], True, DarkText)
    screen.blit(text_panel5, [1050, 204])

    # Button - Next alignment from a list
    pygame.draw.polygon(screen, FillButton, [[1180, 174], [1266, 174], [1266, 196], [1180, 196]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1180, 174], [1266, 174], [1266, 196], [1180, 196]], 3)
    text_panel5 = font20.render("Next", True, DarkText)
    screen.blit(text_panel5, [1200, 174])

    # Label - Country's colors
    text_panel4 = font20.render("Country's colors:", True, TitleText)
    screen.blit(text_panel4, [1060, 234])

    pygame.draw.polygon(screen, FlagColors[faction_names.colors_list[game_stats.option_box_first_color_index]],
                        [[1240, 234], [1266, 234], [1266, 245], [1240, 245]])
    pygame.draw.polygon(screen, FlagColors[faction_names.colors_list[game_stats.option_box_second_color_index]],
                        [[1240, 246], [1266, 246], [1266, 256], [1240, 256]])

    # Option box - First color
    pygame.draw.polygon(screen, FieldColor, [[1044, 264], [1208, 264], [1208, 286], [1044, 286]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1044, 264], [1208, 264], [1208, 286], [1044, 286]], 3)
    text_panel5 = font20.render(faction_names.colors_list[game_stats.option_box_first_color_index], True, DarkText)
    screen.blit(text_panel5, [1050, 264])

    # Buttons - previous and next first color

    pygame.draw.polygon(screen, RockTunel, [[1214, 264], [1236, 264], [1236, 286], [1214, 286]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1214, 264], [1236, 264], [1236, 286], [1214, 286]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1232, 268), (1218, 275), (1232, 282)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 264], [1266, 264], [1266, 286], [1244, 286]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 264], [1266, 264], [1266, 286], [1244, 286]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 268), (1262, 275), (1248, 282)], 2)

    # Option box - Second color
    pygame.draw.polygon(screen, FieldColor, [[1044, 294], [1208, 294], [1208, 316], [1044, 316]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1044, 294], [1208, 294], [1208, 316], [1044, 316]], 3)
    text_panel5 = font20.render(faction_names.colors_list[game_stats.option_box_second_color_index], True, DarkText)
    screen.blit(text_panel5, [1050, 294])

    # Buttons - previous and next second color

    pygame.draw.polygon(screen, RockTunel, [[1214, 294], [1236, 294], [1236, 316], [1214, 316]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1214, 294], [1236, 294], [1236, 316], [1214, 316]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1232, 298), (1218, 305), (1232, 312)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 294], [1266, 294], [1266, 316], [1244, 316]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 294], [1266, 294], [1266, 316], [1244, 316]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 298), (1262, 305), (1248, 312)], 2)

    # Buttons - Create new country
    pygame.draw.polygon(screen, FillButton, [[1044, 324], [1266, 324], [1266, 346], [1044, 346]])
    if game_stats.new_country_name != "":
        color2 = HighlightOption
    else:
        color2 = LineMainMenuColor1
    pygame.draw.polygon(screen, color2, [[1044, 324], [1266, 324], [1266, 346], [1044, 346]], 3)
    text_panel1 = font20.render("Create new realm", True, DarkText)
    screen.blit(text_panel1, [1050, 324])

    # List of countries
    power_count = 0
    if len(game_stats.editor_powers) > 0:
        number = 1
        if len(game_stats.editor_powers) >= 3:
            number = 3
        else:
            number = len(game_stats.editor_powers)

        for position in range(1, number + 1):
            power = game_stats.editor_powers[position - 1 + game_stats.power_short_index]
            adjust = 50 * power_count

            # Name
            text_panel6 = font16.render(power.name, True, TitleText)
            screen.blit(text_panel6, [1044, 354 + adjust])

            # Flag
            pygame.draw.polygon(screen, FlagColors[power.f_color],
                                [[1044, 374 + adjust], [1064, 374 + adjust], [1064, 382 + adjust],
                                 [1044, 382 + adjust]])
            pygame.draw.polygon(screen, FlagColors[power.s_color],
                                [[1044, 383 + adjust], [1064, 383 + adjust], [1064, 391 + adjust],
                                 [1044, 391 + adjust]])

            # Alignment
            text_panel6 = font16.render(power.alignment, True, TitleText)
            screen.blit(text_panel6, [1070, 374 + adjust])

            power_count += 1  # Increase position index

        # Draw white rectangle around selected country in powers panel
        if game_stats.white_index is not None:
            pop_num = int(game_stats.white_index - game_stats.power_short_index)
            if 0 <= pop_num <= 2:
                pygame.draw.polygon(screen, WhiteBorder, [[1041, 354 + 50 * pop_num], [1242, 354 + 50 * pop_num],
                                                          [1242, 394 + 50 * pop_num], [1041, 394 + 50 * pop_num]], 1)

    # Buttons - previous and next country in list

    pygame.draw.polygon(screen, RockTunel, [[1244, 354], [1266, 354], [1266, 376], [1244, 376]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 354], [1266, 354], [1266, 376], [1244, 376]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 372), (1254, 358), (1262, 372)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 473), (1254, 487), (1262, 473)], 2)

    # Lower panel with detailed information about countries
    if game_stats.lower_panel == "powers lower panel":
        powers_lower_panel(screen)


def brush_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 400], [1040, 400]])

    if len(game_stats.selected_tile) > 0:
        # Index of selected tile in map list
        x = int(game_stats.selected_tile[0])
        y = int(game_stats.selected_tile[1])
        TileNum = (y - 1) * game_stats.new_level_width + x - 1

    # Label - Brush size
    text_panel1 = font20.render("Brush size", True, TitleText)
    screen.blit(text_panel1, [1075, 74])

    # Brush size buttons
    pygame.draw.polygon(screen, FillButton,
                        [[1044, 104], [1111, 104], [1111, 126], [1044, 126]])
    if game_stats.brush_size == 1:
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[1044, 104], [1111, 104], [1111, 126], [1044, 126]], 3)
    text_panel1 = font20.render("1x1", True, DarkText)
    screen.blit(text_panel1, [1064, 104])

    pygame.draw.polygon(screen, FillButton,
                        [[1121, 104], [1188, 104], [1188, 126], [1121, 126]])
    if game_stats.brush_size == 2:
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[1121, 104], [1188, 104], [1188, 126], [1121, 126]], 3)
    text_panel1 = font20.render("3x3", True, DarkText)
    screen.blit(text_panel1, [1141, 104])

    pygame.draw.polygon(screen, FillButton,
                        [[1198, 104], [1265, 104], [1265, 126], [1198, 126]])
    if game_stats.brush_size == 3:
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[1198, 104], [1265, 104], [1265, 126], [1198, 126]], 3)
    text_panel1 = font20.render("5x5", True, DarkText)
    screen.blit(text_panel1, [1218, 104])

    # Terrain buttons
    pygame.draw.polygon(screen, TerrainColors[terrain_catalog.terrain_calendar["Plain"][game_stats.LE_month]],
                        [[1044, 134], [1150, 134], [1150, 156], [1044, 156]])
    if game_stats.brush == "Plain":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[1044, 134], [1150, 134], [1150, 156], [1044, 156]], 3)
    text_panel1 = font20.render("Plain", True, DarkText)
    screen.blit(text_panel1, [1075, 134])

    pygame.draw.polygon(screen, TerrainColors[terrain_catalog.terrain_calendar["Northlands"][game_stats.LE_month]],
                        [[1160, 134], [1266, 134], [1266, 156], [1160, 156]])
    if game_stats.brush == "Northlands":
        color2 = HighlightOption
    else:
        color2 = LineMainMenuColor1
    pygame.draw.polygon(screen, color2, [[1160, 134], [1266, 134], [1266, 156], [1160, 156]], 3)
    text_panel1 = font20.render("Northlands", True, DarkText)
    screen.blit(text_panel1, [1166, 134])


def roads_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 400], [1040, 400]])

    # Label - Road types
    text_panel1 = font20.render("Road types", True, TitleText)
    screen.blit(text_panel1, [1075, 74])

    # Road buttons
    pygame.draw.polygon(screen, Earthen_Road,
                        [[1044, 104], [1150, 104], [1150, 126], [1044, 126]])
    if game_stats.brush == "Earthen":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[1044, 104], [1150, 104], [1150, 126], [1044, 126]], 3)
    text_panel1 = font20.render("Earthen", True, DarkText)
    screen.blit(text_panel1, [1070, 104])

    # Remove roads button
    pygame.draw.polygon(screen, CancelFieldColor,
                        [[1160, 104], [1266, 104], [1266, 126], [1160, 126]])
    if game_stats.brush == "Remove road":
        color1 = HighlightOption
    else:
        color1 = CancelElementsColor
    pygame.draw.polygon(screen, color1, [[1160, 104], [1266, 104], [1266, 126], [1160, 126]], 3)
    text_panel1 = font20.render("Remove", True, DarkText)
    screen.blit(text_panel1, [1178, 104])


def create_army_lower_panel(screen, focus):
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 600 + yVar], [1080, 600 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    # Delete unit
    pygame.draw.polygon(screen, FieldColor,
                        [[202, 634 + yVar], [300, 634 + yVar], [300, 655 + yVar], [202, 655 + yVar]])

    if game_stats.delete_option:
        color1 = HighlightOption
    else:
        color1 = CancelElementsColor
    pygame.draw.polygon(screen, color1,
                        [[202, 634 + yVar], [300, 634 + yVar], [300, 655 + yVar], [202, 655 + yVar]], 3)
    text_panel = font20.render("Delete unit", True, DarkText)
    screen.blit(text_panel, [205, 634 + yVar])

    for army in game_stats.editor_armies:
        if army.army_id == focus:
            # Neutrals label
            if army.owner == "Neutrals":
                text_panel = font20.render("Neutrals", True, TitleText)
                screen.blit(text_panel, [210, 604 + yVar])
            else:
                for power in game_stats.editor_powers:
                    if power.name == army.owner:
                        # Country's name
                        text_panel = font20.render(power.name, True, TitleText)
                        screen.blit(text_panel, [210, 604 + yVar])

            # Units
            if len(army.units) > 0:
                number = 0
                for unit in army.units:
                    x_pos = 430 + math.floor(number / 5) * 160
                    y_pos = 604 + yVar + (number % 5) * 26
                    text_panel6 = font16.render(unit.name, True, TitleText)
                    screen.blit(text_panel6, [x_pos, y_pos])

                    number += 1


def create_army_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 495], [1040, 495]])

    # White border around selected tile
    x2 = int(game_stats.selected_tile[0])
    y2 = int(game_stats.selected_tile[1])
    x2 -= int(game_stats.pov_pos[0])
    y2 -= int(game_stats.pov_pos[1])

    # Border line
    pygame.draw.polygon(screen, WhiteBorder,
                        [[(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 1], [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 1],
                         [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 48], [(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 48]], 1)

    # Index of selected tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.new_level_width + x - 1

    # Button - Army's allegiance
    pygame.draw.polygon(screen, FillButton, [[1044, 74], [1150, 74], [1150, 96], [1044, 96]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1044, 74], [1150, 74], [1150, 96], [1044, 96]], 3)
    text_panel9 = font20.render(game_stats.army_allegiance, True, DarkText)
    screen.blit(text_panel9, [1060, 74])

    if len(game_stats.editor_powers) > 0:
        pygame.draw.polygon(screen, FlagColors[game_stats.editor_powers[game_stats.powers_l_p_index].f_color],
                            [[1044, 104], [1066, 104], [1066, 115], [1044, 115]])
        pygame.draw.polygon(screen, FlagColors[game_stats.editor_powers[game_stats.powers_l_p_index].s_color],
                            [[1044, 116], [1066, 116], [1066, 126], [1044, 126]])

    # Option box - Country
    pygame.draw.polygon(screen, FieldColor, [[1070, 104], [1266, 104], [1266, 126], [1070, 126]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1070, 104], [1266, 104], [1266, 126], [1070, 126]], 3)
    if len(game_stats.editor_powers) > 0:
        text_panel8 = font20.render(game_stats.editor_powers[game_stats.powers_l_p_index].name, True, DarkText)
        screen.blit(text_panel8, [1075, 104])

    # Buttons - previous and next country to choose

    pygame.draw.polygon(screen, RockTunel, [[1214, 74], [1236, 74], [1236, 96], [1214, 96]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1214, 74], [1236, 74], [1236, 96], [1214, 96]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1232, 78), (1218, 85), (1232, 92)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 74], [1266, 74], [1266, 96], [1244, 96]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 74], [1266, 74], [1266, 96], [1244, 96]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 78), (1262, 85), (1248, 92)], 2)

    # Button - Create a new army
    pygame.draw.polygon(screen, FieldColor, [[1044, 134], [1150, 134], [1150, 156], [1044, 156]])
    if game_stats.level_map[TileNum].army_id is None:
        color1 = HighlightOption
    else:
        color1 = CancelElementsColor
    pygame.draw.polygon(screen, color1, [[1044, 134], [1150, 134], [1150, 156], [1044, 156]], 3)
    text_panel = font20.render("Create", True, DarkText)
    screen.blit(text_panel, [1070, 134])

    # Button - Delete selected army
    pygame.draw.polygon(screen, CancelFieldColor, [[1160, 134], [1266, 134], [1266, 156], [1160, 156]])
    pygame.draw.polygon(screen, CancelElementsColor, [[1160, 134], [1266, 134], [1266, 156], [1160, 156]], 3)
    text_panel = font20.render("Delete", True, DarkText)
    screen.blit(text_panel, [1188, 134])

    # Button - Choose hero
    pygame.draw.polygon(screen, FieldColor, [[1044, 164], [1150, 164], [1150, 186], [1044, 186]])
    if game_stats.level_map[TileNum].army_id is None:
        color1 = HighlightOption
    else:
        color1 = CancelElementsColor
    pygame.draw.polygon(screen, color1, [[1044, 164], [1150, 164], [1150, 186], [1044, 186]], 3)
    text_panel = font20.render("Hero", True, DarkText)
    screen.blit(text_panel, [1080, 164])

    # Button - Move army
    pygame.draw.polygon(screen, FieldColor, [[1160, 164], [1266, 164], [1266, 186], [1160, 186]])
    if game_stats.level_map[TileNum].army_id is None:
        color1 = HighlightOption
    else:
        color1 = CancelElementsColor
    pygame.draw.polygon(screen, color1, [[1160, 164], [1266, 164], [1266, 186], [1160, 186]], 3)
    text_panel = font20.render("Move", True, DarkText)
    screen.blit(text_panel, [1190, 164])

    # Label - New unit alignment
    text_panel4 = font20.render("New unit alignment", True, TitleText)
    screen.blit(text_panel4, [1044, 194])

    # Button - Next alignment from a list
    pygame.draw.polygon(screen, FillButton, [[1212, 194], [1266, 194], [1266, 216], [1212, 216]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1212, 194], [1266, 194], [1266, 216], [1212, 216]], 3)
    text_panel5 = font20.render("Next", True, DarkText)
    screen.blit(text_panel5, [1220, 194])

    # Option box - Alignment
    pygame.draw.polygon(screen, FieldColor, [[1044, 224], [1266, 224], [1266, 246], [1044, 246]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1044, 224], [1266, 224], [1266, 246], [1044, 246]], 3)
    text_panel5 = font20.render(alinement_info.advanced_alinements_list[game_stats.option_box_alinement_index],
                                True, DarkText)
    screen.blit(text_panel5, [1050, 224])

    # List of units
    unit_count = 0
    alignment = str(alinement_info.advanced_alinements_list[game_stats.option_box_alinement_index])
    units_list = list(units_info.LE_units_dict_by_alinement[alignment])
    if len(units_list) > 0:
        number = 1
        if len(units_list) >= 9:
            number = 9
        else:
            number = len(units_list)

        for position in range(1, number + 1):
            unit_name = units_list[position - 1 + game_stats.unit_short_index]
            adjust = 26 * unit_count

            # Name
            text_panel6 = font16.render(unit_name, True, TitleText)
            screen.blit(text_panel6, [1044, 254 + adjust])

            unit_count += 1  # Increase position index

            pygame.draw.lines(screen, WhiteBorder, False, [(1044, 275 + adjust), (1240, 275 + adjust)], 2)

    # Buttons - previous and next unit in list

    pygame.draw.polygon(screen, RockTunel, [[1244, 254], [1266, 254], [1266, 276], [1244, 276]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 254], [1266, 254], [1266, 276], [1244, 276]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 272), (1254, 258), (1262, 272)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 473), (1254, 487), (1262, 473)], 2)

    # Lower panel with detailed information about city
    if game_stats.lower_panel == "create army lower panel":
        create_army_lower_panel(screen, game_stats.level_map[TileNum].army_id)


def objects_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 495], [1040, 495]])

    if len(game_stats.selected_tile) > 0:
        # Index of selected tile in map list
        x = int(game_stats.selected_tile[0])
        y = int(game_stats.selected_tile[1])
        TileNum = (y - 1) * game_stats.new_level_width + x - 1

    # Remove object button
    pygame.draw.polygon(screen, CancelFieldColor,
                        [[1044, 74], [1175, 74], [1175, 96], [1044, 96]])
    if game_stats.brush == "Remove object":
        color1 = HighlightOption
    else:
        color1 = CancelElementsColor
    pygame.draw.polygon(screen, color1, [[1044, 74], [1175, 74], [1175, 96], [1044, 96]], 3)
    text_panel1 = font20.render("Remove object", True, DarkText)
    screen.blit(text_panel1, [1050, 74])

    # Buttons - terrain objects categories
    pygame.draw.polygon(screen, FillButton,
                        [[1044, 104], [1150, 104], [1150, 126], [1044, 126]])
    if game_stats.object_category == "Forest":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[1044, 104], [1150, 104], [1150, 126], [1044, 126]], 3)
    text_panel1 = font20.render("Forest", True, DarkText)
    screen.blit(text_panel1, [1070, 104])

    pygame.draw.polygon(screen, FillButton,
                        [[1160, 104], [1266, 104], [1266, 126], [1160, 126]])
    if game_stats.object_category == "Trees":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[1160, 104], [1266, 104], [1266, 126], [1160, 126]], 3)
    text_panel1 = font20.render("Trees", True, DarkText)
    screen.blit(text_panel1, [1192, 104])

    # Delimiter line
    pygame.draw.lines(screen, WhiteBorder, False, [(1044, 159), (1266, 159)], 2)

    # Buttons - objects

    # If category is "Forest"
    if game_stats.object_category == "Forest":
        # Button - Oak forest
        pygame.draw.polygon(screen, FillButton,
                            [[1044, 164], [1150, 164], [1150, 186], [1044, 186]])
        if game_stats.brush == "Obj - Oak forest":
            color1 = HighlightOption
        else:
            color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, color1, [[1044, 164], [1150, 164], [1150, 186], [1044, 186]], 3)
        text_panel1 = font20.render("Oak", True, DarkText)
        screen.blit(text_panel1, [1075, 164])

        # Button - Birch forest
        pygame.draw.polygon(screen, FillButton,
                            [[1160, 164], [1266, 164], [1266, 186], [1160, 186]])
        if game_stats.brush == "Obj - Birch forest":
            color1 = HighlightOption
        else:
            color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, color1, [[1160, 164], [1266, 164], [1266, 186], [1160, 186]], 3)
        text_panel1 = font20.render("Birch", True, DarkText)
        screen.blit(text_panel1, [1192, 164])

    # If category is "Trees"
    elif game_stats.object_category == "Trees":
        # Button - Oak trees
        pygame.draw.polygon(screen, FillButton,
                            [[1044, 164], [1150, 164], [1150, 186], [1044, 186]])
        if game_stats.brush == "Obj - Oak trees":
            color1 = HighlightOption
        else:
            color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, color1, [[1044, 164], [1150, 164], [1150, 186], [1044, 186]], 3)
        text_panel1 = font20.render("Oak", True, DarkText)
        screen.blit(text_panel1, [1079, 164])

        # Button - Birch forest
        pygame.draw.polygon(screen, FillButton,
                            [[1160, 164], [1266, 164], [1266, 186], [1160, 186]])
        if game_stats.brush == "Obj - Birch trees":
            color1 = HighlightOption
        else:
            color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, color1, [[1160, 164], [1266, 164], [1266, 186], [1160, 186]], 3)
        text_panel1 = font20.render("Birch", True, DarkText)
        screen.blit(text_panel1, [1192, 164])


def facility_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 495], [1040, 495]])

    # White border around selected tile
    x2 = int(game_stats.selected_tile[0])
    y2 = int(game_stats.selected_tile[1])
    x2 -= int(game_stats.pov_pos[0])
    y2 -= int(game_stats.pov_pos[1])

    # Border line
    pygame.draw.polygon(screen, WhiteBorder,
                        [[(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 1], [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 1],
                         [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 48], [(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 48]], 1)

    if len(game_stats.selected_tile) > 0:
        # Index of selected tile in map list
        x = int(game_stats.selected_tile[0])
        y = int(game_stats.selected_tile[1])
        TileNum = (y - 1) * game_stats.new_level_width + x - 1

    # Remove facility button
    pygame.draw.polygon(screen, CancelFieldColor,
                        [[1044, 74], [1185, 74], [1185, 96], [1044, 96]])
    pygame.draw.polygon(screen, CancelElementsColor, [[1044, 74], [1185, 74], [1185, 96], [1044, 96]], 3)
    text_panel1 = font20.render("Remove facility", True, DarkText)
    screen.blit(text_panel1, [1050, 74])

    # Delimeter line
    pygame.draw.lines(screen, WhiteBorder, False, [(1044, 99), (1266, 99)], 2)

    # List of facilities
    facility_count = 0
    facility_list = list(facility_catalog.LE_facility_list)
    if len(facility_list) > 0:
        number = 1
        if len(facility_list) >= 8:
            number = 8
        else:
            number = len(facility_list)

        for position in range(1, number + 1):
            facility_name = facility_list[position - 1 + game_stats.facility_short_index]
            adjust = 30 * facility_count

            # Facility name
            pygame.draw.polygon(screen, FillButton,
                                [[1044, 104 + adjust], [1240, 104 + adjust],
                                 [1240, 126 + adjust], [1044, 126 + adjust]])
            pygame.draw.polygon(screen, LineMainMenuColor1,
                                [[1044, 104 + adjust], [1240, 104 + adjust],
                                 [1240, 126 + adjust], [1044, 126 + adjust]], 3)
            text_panel1 = font20.render(facility_name, True, DarkText)
            screen.blit(text_panel1, [1090, 104 + adjust])

            facility_count += 1  # Increase position index

    # Buttons - previous and next facility in list

    pygame.draw.polygon(screen, RockTunel, [[1244, 104], [1266, 104], [1266, 126], [1244, 126]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 104], [1266, 104], [1266, 126], [1244, 126]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 122), (1254, 108), (1262, 122)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 473), (1254, 487), (1262, 473)], 2)

    # Lower panel with detailed information about population
    if game_stats.lower_panel == "population lower panel":
        population_lower_panel(screen)


def exploration_objects_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 495], [1040, 495]])

    # Remove object button
    pygame.draw.polygon(screen, CancelFieldColor,
                        [[1044, 74], [1175, 74], [1175, 96], [1044, 96]])
    if game_stats.brush == "Remove object":
        color1 = HighlightOption
    else:
        color1 = CancelElementsColor
    pygame.draw.polygon(screen, color1, [[1044, 74], [1175, 74], [1175, 96], [1044, 96]], 3)
    text_panel1 = font20.render("Remove object", True, DarkText)
    screen.blit(text_panel1, [1050, 74])

    # Buttons - previous and next objects group
    pygame.draw.polygon(screen, RockTunel, [[1044, 104], [1066, 104], [1066, 126], [1044, 126]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1044, 104], [1066, 104], [1066, 126], [1044, 126]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1062, 108), (1048, 115), (1062, 122)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 104], [1266, 104], [1266, 126], [1244, 126]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 104], [1266, 104], [1266, 126], [1244, 126]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 108), (1262, 115), (1248, 122)], 2)

    # Buttons - terrain objects categories
    pygame.draw.polygon(screen, FillButton,
                        [[1070, 104], [1240, 104], [1240, 126], [1070, 126]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1070, 104], [1240, 104], [1240, 126], [1070, 126]], 3)
    text_panel1 = font20.render(str(game_stats.object_category), True, DarkText)
    screen.blit(text_panel1, [1110, 104])

    # Delimiter line
    pygame.draw.lines(screen, WhiteBorder, False, [(1044, 129), (1266, 129)], 2)

    # Buttons - previous and next object in list

    pygame.draw.polygon(screen, RockTunel, [[1244, 134], [1266, 134], [1266, 156], [1244, 156]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 134], [1266, 134], [1266, 156], [1244, 156]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 152), (1254, 138), (1262, 152)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 473), (1254, 487), (1262, 473)], 2)

    y_shift = 30
    y_points = 0
    # Explorable objects
    for obj in exploration_catalog.groups_cat[game_stats.object_category]:
        y = y_shift * y_points
        pygame.draw.polygon(screen, FillButton,
                            [[1044, 134 + y], [1238, 134 + y], [1238, 156 + y], [1044, 156 + y]])
        if game_stats.brush == obj:
            color1 = HighlightOption
        else:
            color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, color1, [[1044, 134 + y], [1238, 134 + y], [1238, 156 + y], [1044, 156 + y]], 2)
        text_panel1 = font20.render(obj, True, DarkText)
        screen.blit(text_panel1, [1052, 134 + y])

        y_points += 1


def level_editor_screen(screen):
    screen.fill(MapLimitColor)  # background

    draw_tiles(screen)  # Draw tiles

    # Top ribbon
    pygame.draw.polygon(screen, MainMenuColor, [[41, 0], [600, 0], [600, 20], [41, 20]])

    text_NewGame1 = font16.render("Brush", True, DarkText)
    screen.blit(text_NewGame1, (42, 1))

    if game_stats.brush_shape == 1:
        color1 = WhiteColor
    else:
        color1 = DarkText
    pygame.draw.rect(screen, color1, (86, 5, 13, 13), 1)

    if game_stats.brush_shape == 2:
        color1 = WhiteColor
    else:
        color1 = DarkText
    pygame.draw.circle(screen, color1, (113, 11), 7, 1)

    if game_stats.brush_size == 1:
        color1 = WhiteColor
    else:
        color1 = DarkText
    text_NewGame1 = font16.render("1x1", True, color1)
    screen.blit(text_NewGame1, (126, 1))

    if game_stats.brush_size == 2:
        color1 = WhiteColor
    else:
        color1 = DarkText
    text_NewGame1 = font16.render("2x2", True, color1)
    screen.blit(text_NewGame1, (156, 1))

    if game_stats.brush_size == 3:
        color1 = WhiteColor
    else:
        color1 = DarkText
    text_NewGame1 = font16.render("3x3", True, color1)
    screen.blit(text_NewGame1, (186, 1))

    if game_stats.brush_size == 4:
        color1 = WhiteColor
    else:
        color1 = DarkText
    text_NewGame1 = font16.render("4x4", True, color1)
    screen.blit(text_NewGame1, (216, 1))

    ## Buttons

    # Exit
    pygame.draw.polygon(screen, FillButton, [[1150, 10], [1250, 10], [1250, 32], [1150, 32]])
    pygame.draw.polygon(screen, BorderNewGameColor, [[1150, 10], [1250, 10], [1250, 32], [1150, 32]], 3)

    text_NewGame1 = font20.render("Exit", True, TitleText)
    screen.blit(text_NewGame1, [1180, 10])

    # Brush
    if game_stats.edit_instrument == "brush":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[1150, 40], [1250, 40], [1250, 62], [1150, 62]])
    pygame.draw.polygon(screen, color, [[1150, 40], [1250, 40], [1250, 62], [1150, 62]], 3)

    text_NewGame2 = font20.render("Brush", True, TitleText)
    screen.blit(text_NewGame2, [1180, 40])

    # Roads
    if game_stats.edit_instrument == "road":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[1040, 40], [1140, 40], [1140, 62], [1040, 62]])
    pygame.draw.polygon(screen, color, [[1040, 40], [1140, 40], [1140, 62], [1040, 62]], 3)

    text_NewGame2 = font20.render("Roads", True, TitleText)
    screen.blit(text_NewGame2, [1065, 40])

    # Army
    if game_stats.edit_instrument == "create army":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[930, 40], [1030, 40], [1030, 62], [930, 62]])
    pygame.draw.polygon(screen, color, [[930, 40], [1030, 40], [1030, 62], [930, 62]], 3)

    text_NewGame2 = font20.render("Army", True, TitleText)
    screen.blit(text_NewGame2, [960, 40])

    # Save
    pygame.draw.polygon(screen, FillButton, [[1040, 10], [1140, 10], [1140, 32], [1040, 32]])
    pygame.draw.polygon(screen, BorderNewGameColor, [[1040, 10], [1140, 10], [1140, 32], [1040, 32]], 3)

    text_NewGame1 = font20.render("Save", True, TitleText)
    screen.blit(text_NewGame1, [1070, 10])

    # City
    if game_stats.edit_instrument == "create city":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[930, 10], [1030, 10], [1030, 32], [930, 32]])
    pygame.draw.polygon(screen, color, [[930, 10], [1030, 10], [1030, 32], [930, 32]], 3)

    text_NewGame2 = font20.render("City", True, TitleText)
    screen.blit(text_NewGame2, [964, 10])

    # Powers
    if game_stats.level_editor_panel == "powers panel":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[820, 10], [920, 10], [920, 32], [820, 32]])
    pygame.draw.polygon(screen, color, [[820, 10], [920, 10], [920, 32], [820, 32]], 3)

    text_NewGame2 = font20.render("Powers", True, TitleText)
    screen.blit(text_NewGame2, [840, 10])

    # Objects of nature, landscape and obstacles
    if game_stats.level_editor_panel == "objects panel":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[820, 40], [920, 40], [920, 62], [820, 62]])
    pygame.draw.polygon(screen, color, [[820, 40], [920, 40], [920, 62], [820, 62]], 3)

    text_NewGame2 = font20.render("Objects", True, TitleText)
    screen.blit(text_NewGame2, [838, 40])

    # Facility
    if game_stats.edit_instrument == "create facility":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[710, 10], [810, 10], [810, 32], [710, 32]])
    pygame.draw.polygon(screen, color, [[710, 10], [810, 10], [810, 32], [710, 32]], 3)

    text_NewGame2 = font20.render("Facility", True, TitleText)
    screen.blit(text_NewGame2, [730, 10])

    # Exploration
    if game_stats.level_editor_panel == "exploration objects panel":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[710, 40], [810, 40], [810, 62], [710, 62]])
    pygame.draw.polygon(screen, color, [[710, 40], [810, 40], [810, 62], [710, 62]], 3)

    text_NewGame2 = font20.render("Exploration", True, TitleText)
    screen.blit(text_NewGame2, [713, 40])

    ## Panels
    if game_stats.level_editor_panel != "":
        draw_panel[game_stats.level_editor_panel](screen)

    ## Left panels
    if game_stats.level_editor_left_panel != "":
        if game_stats.level_editor_left_panel in draw_left_panel:
            draw_left_panel[game_stats.level_editor_left_panel](screen)


draw_panel = {"brush panel" : brush_panel,
              "roads panel" : roads_panel,
              "create city panel" : create_city_panel,
              "powers panel" : powers_panel,
              "create army panel" : create_army_panel,
              "objects panel" : objects_panel,
              "create facility panel" : facility_panel,
              "exploration objects panel" : exploration_objects_panel}

draw_left_panel = {"building menu left panel" : building_menu_left_panel}
