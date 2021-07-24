## Miracle battles!

import math
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
from Resources import game_obj
from Resources import game_stats
from Screens import draw_movement_arrows
from Screens import anim_army_move

pygame.init()

WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
NewGameColor = [0x8D, 0x86, 0x86]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

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

MatterColors = {"Rock": RockColor,
                "Monolith": MonolithColor}

TunelColors = {"Rock": RockTunel,
               "Monolith": MonolithTunel}

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
font8 = pygame.font.SysFont('arial', 8)


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
        # First step is to find player's realm and copy its discovered map
        map_to_display = []
        for power in game_obj.game_powers:
            if power.name == game_stats.perspective:
                map_to_display = power.known_map

        for TileObj in game_obj.game_map:
            x = TileObj.posxy[0]
            y = TileObj.posxy[1]
            x -= int(game_stats.pov_pos[0])
            y -= int(game_stats.pov_pos[1])

            if 0 < x <= 27 and 0 < y <= math.ceil(game_stats.game_window_height):

                # Draw only discovered tiles
                if [TileObj.posxy[0], TileObj.posxy[1]] in map_to_display:

                    terrain_img = pygame.image.load('img/Terrains/'
                                                    + terrain_catalog.terrain_calendar[TileObj.terrain][
                                                        game_stats.game_month] + '.png')
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
                                         [(x - 1) * 48 + 48, (y - 1) * 48 + 48], [(x - 1) * 48 + 1, (y - 1) * 48 + 48]],
                                        1)

                # Draw undiscovered tiles as dark purple tiles
                else:
                    pygame.draw.polygon(screen, UndiscoveredTile,
                                        [[(x - 1) * 48 + 1, (y - 1) * 48 + 1], [(x - 1) * 48 + 48, (y - 1) * 48 + 1],
                                         [(x - 1) * 48 + 48, (y - 1) * 48 + 48], [(x - 1) * 48 + 1, (y - 1) * 48 + 48]])

        for TileObj in game_obj.game_map:
            x = TileObj.posxy[0]
            y = TileObj.posxy[1]
            x -= int(game_stats.pov_pos[0])
            y -= int(game_stats.pov_pos[1])

            if 0 < x <= 27 and 0 < y <= math.ceil(game_stats.game_window_height):

                if [TileObj.posxy[0], TileObj.posxy[1]] in map_to_display:

                    # Cities
                    if TileObj.lot is not None:
                        if TileObj.lot == "City":
                            for city in game_obj.game_cities:
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
                                        for power in game_obj.game_powers:
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
                            # Objects
                            if TileObj.lot.obj_typ == "Obstacle":
                                for item in TileObj.lot.disposition:
                                    obj_cal = objects_img_catalog.object_calendar[TileObj.lot.obj_name]
                                    season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.game_month]
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

                        for army in game_obj.game_armies:
                            if army.army_id == focus:
                                if army.hero_id is None:
                                    if len(army.units) > 0 and army.leader is not None:
                                        xy_animation = [0, 0]
                                        if army.action == "Move":
                                            xy_animation = anim_army_move.army_march(army.route[0], army.posxy)

                                        unit = army.units[army.leader]
                                        # print('img/Creatures/' +str(unit.img_source) + str(unit.img) + '.png')
                                        army_img = pygame.image.load(
                                            'img/Creatures/' + str(unit.img_source) + "/" + str(unit.img) + '.png')
                                        army_img.set_colorkey(WhiteColor)
                                        screen.blit(army_img,
                                                    ((x - 1) * 48 + unit.x_offset + xy_animation[0],
                                                     (y - 1) * 48 + unit.y_offset + xy_animation[1]))

                                        if army.owner != "Neutral":  # Draw flag
                                            for power in game_obj.game_powers:
                                                if army.owner == power.name:
                                                    pygame.draw.polygon(screen, FlagpoleColor,
                                                                        ([(x - 1) * 48 + 3 + xy_animation[0],
                                                                          (y - 1) * 48 + 32 + xy_animation[1]],
                                                                         [(x - 1) * 48 + 4 + xy_animation[0],
                                                                          (y - 1) * 48 + 32 + xy_animation[1]],
                                                                         [(x - 1) * 48 + 4 + xy_animation[0],
                                                                          (y - 1) * 48 + 48 + xy_animation[1]],
                                                                         [(x - 1) * 48 + 3 + xy_animation[0],
                                                                          (y - 1) * 48 + 48 + xy_animation[1]]))
                                                    pygame.draw.polygon(screen, FlagColors[power.f_color],
                                                                        ([(x - 1) * 48 + 5 + xy_animation[0],
                                                                          (y - 1) * 48 + 32 + xy_animation[1]],
                                                                         [(x - 1) * 48 + 11 + xy_animation[0],
                                                                          (y - 1) * 48 + 32 + xy_animation[1]],
                                                                         [(x - 1) * 48 + 11 + xy_animation[0],
                                                                          (y - 1) * 48 + 36 + xy_animation[1]],
                                                                         [(x - 1) * 48 + 5 + xy_animation[0],
                                                                          (y - 1) * 48 + 36 + xy_animation[1]]))
                                                    pygame.draw.polygon(screen, FlagColors[power.s_color],
                                                                        ([(x - 1) * 48 + 5 + xy_animation[0],
                                                                          (y - 1) * 48 + 37 + xy_animation[1]],
                                                                         [(x - 1) * 48 + 11 + xy_animation[0],
                                                                          (y - 1) * 48 + 37 + xy_animation[1]],
                                                                         [(x - 1) * 48 + 11 + xy_animation[0],
                                                                          (y - 1) * 48 + 41 + xy_animation[1]],
                                                                         [(x - 1) * 48 + 5 + xy_animation[0],
                                                                          (y - 1) * 48 + 41 + xy_animation[1]]))


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

    # Material
    text_panel = font20.render(game_obj.game_map[TileNum - 1].matter, True, TitleText)
    screen.blit(text_panel, [210, 604 + yVar])

    # Tunels
    if game_obj.game_map[TileNum - 1].tunnels:
        text_panel = font20.render("Tunels", True, TitleText)
        screen.blit(text_panel, [210, 634 + yVar])

    # Caves
    if game_obj.game_map[TileNum - 1].cave:
        text_panel = font20.render("Caves", True, TitleText)
        screen.blit(text_panel, [210, 664 + yVar])

    # Natural feature
    if game_obj.game_map[TileNum - 1].natural_feature is not None:
        text_panel = font20.render(game_obj.game_map[TileNum - 1].natural_feature.name, True, TitleText)
        screen.blit(text_panel, [210, 694 + yVar])

    # Cut mashrooms
    if game_obj.game_map[TileNum - 1].natural_feature is not None:
        if game_obj.game_map[TileNum - 1].natural_feature.name == "Mashroom garden":
            for fac in game_obj.game_factions:
                if fac.name == game_stats.player_faction:
                    pygame.draw.polygon(screen, FillButton,
                                        [[210, 754 + yVar], [310, 754 + yVar], [310, 776 + yVar], [210, 776 + yVar]])
                    if xy_pos in fac.con_plans.cutting_plans:
                        color2 = LimeBorder
                        text = "Cutting"
                    elif xy_pos in fac.con_plans.cutting_plans_inf:
                        color2 = LimeBorder
                        text = "Cutting ∞"
                    else:
                        color2 = LineMainMenuColor1
                        text = "Cutting"
                    pygame.draw.polygon(screen, color2,
                                        [[210, 754 + yVar], [310, 754 + yVar], [310, 776 + yVar], [210, 776 + yVar]], 3)
                    text_panel1 = font20.render(text, True, TitleText)
                    screen.blit(text_panel1, [214, 754 + yVar])

    # Output
    text_panel = font20.render("Output", True, TitleText)
    screen.blit(text_panel, [400, 604 + yVar])

    if len(game_obj.game_map[TileNum - 1].output) > 0:
        shelf = []
        for resource in game_obj.game_map[TileNum - 1].output:
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
                screen.blit(text_panel, [400 + math.floor(number / 6) * 120, 634 + (number - 1) % 6 * 30 + yVar])


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
    pygame.draw.polygon(screen, MainMenuColor, [[380, 100], [900, 100], [900, 400], [380, 400]])

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
                    x_pos = 405 + math.floor(number % 5) * 50
                    y_pos = 198 + math.floor(number / 10) * 50

                    army_img = pygame.image.load(
                        'img/Creatures/' + str(unit.img_source) + "/" + str(unit.img) + '.png')
                    army_img.set_colorkey(WhiteColor)
                    screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

                    number += 1

        elif army.army_id == game_stats.defender_army_id:  # Defender

            # Units
            if len(army.units) > 0:
                number = 0
                for unit in army.units:
                    x_pos = 645 + math.floor(number % 5) * 50
                    y_pos = 198 + math.floor(number / 10) * 50

                    army_img = pygame.image.load(
                        'img/Creatures/' + str(unit.img_source) + "/" + str(unit.img) + '.png')
                    army_img.set_colorkey(WhiteColor)
                    screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

                    number += 1


def mining_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 400], [1040, 400]])

    pygame.draw.polygon(screen, TunelCommonColor, [[1044, 74], [1150, 74], [1150, 96], [1044, 96]])
    if game_stats.brush == "Tunels":
        color2 = HighlightOption
    else:
        color2 = LineMainMenuColor1
    pygame.draw.polygon(screen, color2, [[1044, 74], [1150, 74], [1150, 96], [1044, 96]], 3)
    text_panel1 = font20.render("Tunels", True, TitleText)
    screen.blit(text_panel1, [1070, 74])

    pygame.draw.polygon(screen, TunelCommonColor, [[1160, 74], [1240, 74], [1240, 96], [1160, 96]])
    if game_stats.brush == "Remove tunels":
        color2 = HighlightRemoval
    else:
        color2 = LineMainMenuColor1
    pygame.draw.polygon(screen, color2, [[1160, 74], [1240, 74], [1240, 96], [1160, 96]], 3)
    text_panel1 = font20.render("Remove", True, TitleText)
    screen.blit(text_panel1, [1168, 74])

    pygame.draw.polygon(screen, CaveCommonColor, [[1044, 104], [1150, 104], [1150, 126], [1044, 126]])
    if game_stats.brush == "Cave":
        color2 = HighlightOption
    else:
        color2 = LineMainMenuColor1
    pygame.draw.polygon(screen, color2, [[1044, 104], [1150, 104], [1150, 126], [1044, 126]], 3)
    text_panel1 = font20.render("Cave", True, TitleText)
    screen.blit(text_panel1, [1070, 104])

    pygame.draw.polygon(screen, CaveCommonColor, [[1160, 104], [1240, 104], [1240, 126], [1160, 126]])
    if game_stats.brush == "Remove cave":
        color2 = HighlightRemoval
    else:
        color2 = LineMainMenuColor1
    pygame.draw.polygon(screen, color2, [[1160, 104], [1240, 104], [1240, 126], [1160, 126]], 3)
    text_panel1 = font20.render("Remove", True, TitleText)
    screen.blit(text_panel1, [1168, 104])


def draft_panel(screen):
    yVar = game_stats.game_window_height - 800

    pygame.draw.polygon(screen, MainMenuColor,
                        [[400, 600 + yVar], [880, 600 + yVar], [880, 800 + yVar], [400, 800 + yVar]])

    # Title and building's name
    text_panel = font20.render("Materials required to construct  " + str(game_stats.construct), True, TitleText)
    screen.blit(text_panel, [410, 604 + yVar])

    # Materials
    shelf = []
    for resource in building_drafts.required_materials[game_stats.construct]:
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
            text_panel = font20.render(str(resource[1]) + " X " + str(resource[0]), True, SecondaryText)
            screen.blit(text_panel, [410 + math.floor(number / 6) * 120, 634 + (number - 1) % 6 * 30 + yVar])


def build_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[1040, 70], [1270, 70], [1270, 400], [1040, 400]])

    pygame.draw.polygon(screen, CaveCommonColor, [[1044, 74], [1200, 74], [1200, 96], [1044, 96]])
    if game_stats.brush == "Cancel building":
        color2 = HighlightOption
    else:
        color2 = LineMainMenuColor1
    pygame.draw.polygon(screen, color2, [[1044, 74], [1200, 74], [1200, 96], [1044, 96]], 3)
    text_panel1 = font20.render("Cancel building", True, TitleText)
    screen.blit(text_panel1, [1057, 74])

    text_panel1 = font20.render("Structures to build", True, TitleText)
    screen.blit(text_panel1, [1045, 104])

    text_panel1 = font20.render("Starting structures:", True, TitleText)
    screen.blit(text_panel1, [1045, 134])

    text_panel1 = font20.render("Campfire", True, SecondaryText)
    screen.blit(text_panel1, [1045, 164])
    if game_stats.construct == "Campfire":
        pygame.draw.line(screen, WhiteBorder, [1044, 187], [1265, 187])

    text_panel1 = font20.render("Trade post", True, SecondaryText)
    screen.blit(text_panel1, [1045, 194])

    text_panel1 = font20.render("Available structures:", True, TitleText)
    screen.blit(text_panel1, [1045, 224])

    if game_stats.construct != "":
        draft_panel(screen)


def army_panel(screen):
    # White border around selected tile
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:
            x2 = int(army.posxy[0])
            y2 = int(army.posxy[1])
            x2 -= int(game_stats.pov_pos[0])
            y2 -= int(game_stats.pov_pos[1])

            # Draw movement arrows
            if len(army.route) > 0:
                draw_movement_arrows.arrow_icon(screen, army.route, army.path_arrows)

            # Border line
            pygame.draw.polygon(screen, WhiteBorder,
                                [[(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 1], [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 1],
                                 [(x2 - 1) * 48 + 48, (y2 - 1) * 48 + 48], [(x2 - 1) * 48 + 1, (y2 - 1) * 48 + 48]], 1)

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

    movement_points_left = -1
    least_max_movement_points = -1
    # Display units
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:

            # Units
            if len(army.units) > 0:
                number = 0
                for unit in army.units:
                    x_pos = 430 + math.floor(number % 10) * 52
                    y_pos = 654 + yVar + math.floor(number / 10) * 52

                    army_img = pygame.image.load(
                        'img/Creatures/' + str(unit.img_source) + "/" + str(unit.img) + '.png')
                    army_img.set_colorkey(WhiteColor)
                    screen.blit(army_img,
                                [x_pos + unit.x_offset, y_pos + unit.y_offset])

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
    xVar = int(movement_points_left/least_max_movement_points * 80)
    pygame.draw.polygon(screen, ApproveFieldColor,
                        [[203, 684 + yVar], [203 + xVar, 684 + yVar], [203 + xVar, 706 + yVar], [203, 706 + yVar]])
    pygame.draw.polygon(screen, ApproveElementsColor,
                        [[203, 684 + yVar], [283, 684 + yVar], [283, 706 + yVar], [203, 706 + yVar]], 3)


def game_board_screen(screen):
    screen.fill(MapLimitColor)  # background

    draw_tiles(screen)  # Draw tiles

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
    if not game_stats.turn_hourglass:
        hourglass_img = pygame.image.load('img/Icons/hourglass_false.png')
    else:
        hourglass_img = pygame.image.load('img/Icons/hourglass_true.png')
    hourglass_img.set_colorkey(WhiteColor)
    screen.blit(hourglass_img, (1005, 5))

    # Calendar
    pygame.draw.polygon(screen, MainMenuColor, [[910, 7], [1000, 7], [1000, 55], [910, 55]])
    text_NewGame2 = font20.render("Year", True, TitleText)
    screen.blit(text_NewGame2, [913, 8])
    text_NewGame2 = font20.render(str(game_stats.game_year), True, TitleText)
    screen.blit(text_NewGame2, [980, 8])
    text_NewGame2 = font20.render("Month", True, TitleText)
    screen.blit(text_NewGame2, [913, 32])
    text_NewGame2 = font20.render(str(game_stats.game_month), True, TitleText)
    screen.blit(text_NewGame2, [980, 32])

    # Mining
    if game_stats.edit_instrument == "mining":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[1150, 40], [1250, 40], [1250, 62], [1150, 62]])
    pygame.draw.polygon(screen, color, [[1150, 40], [1250, 40], [1250, 62], [1150, 62]], 3)

    text_NewGame2 = font20.render("Mining", True, TitleText)
    screen.blit(text_NewGame2, [1170, 40])

    # Building
    if game_stats.edit_instrument == "build":
        color = HighlightOption
    else:
        color = BorderNewGameColor
    pygame.draw.polygon(screen, FillButton, [[1040, 40], [1140, 40], [1140, 62], [1040, 62]])
    pygame.draw.polygon(screen, color, [[1040, 40], [1140, 40], [1140, 62], [1040, 62]], 3)

    text_NewGame2 = font20.render("Build", True, TitleText)
    screen.blit(text_NewGame2, [1070, 40])

    ## Panels
    if game_stats.game_board_panel != "":
        draw_panel[game_stats.game_board_panel](screen)

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


draw_panel = {"begin battle panel": begin_battle_panel,
              "mining panel": mining_panel,
              "build panel": build_panel}

info_panels = {"Army": army_panel}
