## Miracle battles!


import pygame.draw, pygame.font, math
from Resources import game_stats
from Content import terrain_catalog
from Content import faction_names
from Content import alinement_info
from Content import city_catalog
from Content import units_info
from Content import objects_img_catalog
from Content import terrain_seasons
from Content import facility_catalog

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
              "BlackHooves": BlackHoovesColor}

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
        for TileObj in game_stats.level_map:
            x = TileObj.posxy[0]
            y = TileObj.posxy[1]
            x -= int(game_stats.pov_pos[0])
            y -= int(game_stats.pov_pos[1])

            if x > 0 and y > 0 and x <= 27 and y <= math.ceil(game_stats.game_window_height):

                terrain_img = pygame.image.load('img/Terrains/'
                                                + terrain_catalog.terrain_calendar[TileObj.terrain][
                                                    game_stats.LE_month] + '.png')
                screen.blit(terrain_img, ((x - 1) * 48 + 1, (y - 1) * 48 + 1))

                # Roads
                if TileObj.road is not None:
                    # Central piece
                    if TileObj.road.material == "Earthen":
                        road_central_piece = pygame.image.load('img/Roads/Earthen_m_m_plains.png')
                        screen.blit(road_central_piece, ((x - 1) * 48 + 22, (y - 1) * 48 + 22))
                    # West piece
                    if TileObj.road.material == "Earthen":
                        if TileObj.road.l_m:
                            road_l_m_piece = pygame.image.load('img/Roads/Earthen_l_m_plains.png')
                            screen.blit(road_l_m_piece, ((x - 1) * 48 + 1, (y - 1) * 48 + 22))
                    # East piece
                    if TileObj.road.material == "Earthen":
                        if TileObj.road.r_m:
                            road_r_m_piece = pygame.image.load('img/Roads/Earthen_r_m_plains.png')
                            screen.blit(road_r_m_piece, ((x - 1) * 48 + 28, (y - 1) * 48 + 22))
                    # North piece
                    if TileObj.road.material == "Earthen":
                        if TileObj.road.m_t:
                            road_m_t_piece = pygame.image.load('img/Roads/Earthen_m_t_plains.png')
                            screen.blit(road_m_t_piece, ((x - 1) * 48 + 22, (y - 1) * 48 + 1))
                    # South piece
                    if TileObj.road.material == "Earthen":
                        if TileObj.road.m_b:
                            road_m_b_piece = pygame.image.load('img/Roads/Earthen_m_b_plains.png')
                            screen.blit(road_m_b_piece, ((x - 1) * 48 + 22, (y - 1) * 48 + 28))
                    # North-east piece
                    if TileObj.road.material == "Earthen":
                        if TileObj.road.r_t:
                            road_r_t_piece = pygame.image.load('img/Roads/Earthen_r_t_plains.png')
                            road_r_t_piece.set_colorkey(WhiteColor)
                            screen.blit(road_r_t_piece, ((x - 1) * 48 + 26, (y - 1) * 48 + 1))
                    # South-west piece
                    if TileObj.road.material == "Earthen":
                        if TileObj.road.l_b:
                            road_l_b_piece = pygame.image.load('img/Roads/Earthen_l_b_plains.png')
                            road_l_b_piece.set_colorkey(WhiteColor)
                            screen.blit(road_l_b_piece, ((x - 1) * 48 - 2, (y - 1) * 48 + 26))
                    # North-west piece
                    if TileObj.road.material == "Earthen":
                        if TileObj.road.l_t:
                            road_l_t_piece = pygame.image.load('img/Roads/Earthen_l_t_plains.png')
                            road_l_t_piece.set_colorkey(WhiteColor)
                            screen.blit(road_l_t_piece, ((x - 1) * 48 - 2, (y - 1) * 48 + 1))
                    # South-east piece
                    if TileObj.road.material == "Earthen":
                        if TileObj.road.r_b:
                            road_r_b_piece = pygame.image.load('img/Roads/Earthen_r_b_plains.png')
                            road_r_b_piece.set_colorkey(WhiteColor)
                            screen.blit(road_r_b_piece, ((x - 1) * 48 + 26, (y - 1) * 48 + 26))

                # Border line
                pygame.draw.polygon(screen, TileBorder,
                                    [[(x - 1) * 48 + 1, (y - 1) * 48 + 1], [(x - 1) * 48 + 48, (y - 1) * 48 + 1],
                                     [(x - 1) * 48 + 48, (y - 1) * 48 + 48], [(x - 1) * 48 + 1, (y - 1) * 48 + 48]], 1)

        for TileObj in game_stats.level_map:
            x = TileObj.posxy[0]
            y = TileObj.posxy[1]
            x -= int(game_stats.pov_pos[0])
            y -= int(game_stats.pov_pos[1])

            if x > 0 and y > 0 and x <= 27 and y <= math.ceil(game_stats.game_window_height):

                # Cities
                if TileObj.lot is not None:
                    if TileObj.lot == "City":
                        for city in game_stats.editor_cities:
                            if city.city_id == TileObj.city_id:
                                city_img = pygame.image.load('img/Cities/' +
                                                             city_catalog.city_cat[city.alignment] +
                                                             '.png')
                                city_img.set_colorkey(WhiteColor)
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
                                obj_img = pygame.image.load('img/' +
                                                            TileObj.lot.img_path + obj_cal[season] +
                                                            '.png')
                                obj_img.set_colorkey(WhiteColor)
                                screen.blit(obj_img, ((x - 1) * 48 + item[0], (y - 1) * 48 + item[1]))

                        elif TileObj.lot.obj_typ == "Facility":
                            # if TileObj.city_id is None:
                            for item in TileObj.lot.disposition:
                                obj_img = pygame.image.load('img/' +
                                                            TileObj.lot.img_path + TileObj.lot.img_name +
                                                            '.png')
                                obj_img.set_colorkey(WhiteColor)
                                screen.blit(obj_img, ((x - 1) * 48 + item[0], (y - 1) * 48 + item[1]))

                # Armies
                if TileObj.army_id is not None:
                    focus = TileObj.army_id

                    for army in game_stats.editor_armies:
                        if army.army_id == focus:
                            if army.hero_id is None:
                                if len(army.units) > 0 and army.leader is not None:
                                    unit = army.units[army.leader]
                                    # print('img/Creatures/' +str(unit.img_source) + str(unit.img) + '.png')
                                    army_img = pygame.image.load(
                                        'img/Creatures/' + str(unit.img_source) + "/" + str(unit.img) + '.png')
                                    army_img.set_colorkey(WhiteColor)
                                    screen.blit(army_img, ((x - 1) * 48 + unit.x_offset, (y - 1) * 48 + unit.y_offset))
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


def create_city_lower_panel(screen, focus):
    if game_stats.edit_instrument == "draw control zone":
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

    for city in game_stats.editor_cities:
        if city.city_id == focus:

            # City's name
            text_panel = font20.render(city.name, True, TitleText)
            screen.blit(text_panel, [210, 604 + yVar])

            # Alignment
            text_panel = font20.render(city.alignment, True, TitleText)
            screen.blit(text_panel, [210, 634 + yVar])

            if city.owner == "Neutral":
                text_panel = font20.render("Neutral", True, TitleText)
                screen.blit(text_panel, [240, 664 + yVar])
            else:
                for power in game_stats.editor_powers:
                    if power.name == city.owner:
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
    else:
        color1 = CancelElementsColor
    pygame.draw.polygon(screen, color1,
                        [[202, 724 + yVar], [270, 724 + yVar], [270, 745 + yVar], [202, 745 + yVar]], 3)
    text_panel = font20.render("Control", True, DarkText)
    screen.blit(text_panel, [205, 724 + yVar])


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
        create_city_lower_panel(screen, game_stats.level_map[TileNum].city_id)


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
                        [[202, 664 + yVar], [260, 664 + yVar], [260, 685 + yVar], [202, 685 + yVar]])
    pygame.draw.polygon(screen, CancelElementsColor,
                        [[202, 664 + yVar], [260, 664 + yVar], [260, 685 + yVar], [202, 685 + yVar]], 3)
    text_panel = font20.render("Delete", True, DarkText)
    screen.blit(text_panel, [205, 664 + yVar])


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
            if pop_num >= 0 and pop_num <= 2:
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
    if game_stats.delete_option == True:
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
        if len(units_list) >= 6:
            number = 6
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

    # Delimeter line
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
        screen.blit(text_panel1, [1075, 164])


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

    # List of units
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

    # Buttons - previous and next unit in list

    pygame.draw.polygon(screen, RockTunel, [[1244, 104], [1266, 104], [1266, 126], [1244, 126]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 104], [1266, 104], [1266, 126], [1244, 126]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 122), (1254, 108), (1262, 122)], 2)

    pygame.draw.polygon(screen, RockTunel, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[1244, 469], [1266, 469], [1266, 491], [1244, 491]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(1248, 473), (1254, 487), (1262, 473)], 2)


def level_editor_screen(screen):
    screen.fill(MapLimitColor)  # background

    draw_tiles(screen)  # Draw tiles

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

    ## Panels
    if game_stats.level_editor_panel != "":
        draw_panel[game_stats.level_editor_panel](screen)


draw_panel = {"brush panel": brush_panel,
              "roads panel": roads_panel,
              "create city panel": create_city_panel,
              "powers panel": powers_panel,
              "create army panel": create_army_panel,
              "objects panel": objects_panel,
              "create facility panel": facility_panel}
