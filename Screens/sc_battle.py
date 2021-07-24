## Miracle battles!

import math
import pygame.draw
import pygame.font
import pygame.mouse

from Content import terrain_catalog
from Content import objects_img_catalog
from Content import terrain_seasons

from Resources import game_obj
from Resources import game_stats
from Screens import anim_battle_effects
from Screens import anim_battle_unit_action

pygame.init()

WhiteColor = [255, 255, 255]
RedColor = [255, 0, 0]
BlueColor = [0, 0, 255, 65]
DeepBlueColor = [0, 0, 255, 255]
GreenColor = [0, 255, 0, 65]
DeepGreenColor = [0, 255, 0, 255]
PinkColor = [255, 0, 255, 65]
DeepPinkColor = [255, 0, 255, 255]
GreenGrid = [178, 255, 102, 70]

MainMenuColor = [0x9F, 0x97, 0x97]
LineMainMenuColor1 = [0x60, 0x60, 0x60]
LightBackground = [198, 186, 186]

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]
SecondaryText = [0xB8, 0xFF, 0x9A]
AttentionText = [232, 142, 6]

BorderNewGameColor = [0xDA, 0xAE, 0x83]
FillButton = [0xD8, 0xBD, 0xA2]
HighlightBorder = [0xF7, 0x82, 0x0C]
FieldColor = [0xA0, 0xA0, 0xA0]
HighlightOption = [0x00, 0xCC, 0xCC]
HighlightRemoval = [0xFF, 0x1A, 0x1A]

RockTunel = [0x89, 0x89, 0x89]

FlagpoleColor = (139, 105, 12, 160)

MapLimitColor = [0x83, 0x62, 0x42]  # DEB887
TileBorder = [11, 11, 11, 200]  # 0x0B, 0x0B, 0x0B
WhiteBorder = [249, 238, 227, 200]
TileCover = [25, 0, 51, 120]
LightYellow = [255, 255, 255, 160]
LimeBorder = [102, 255, 102, 220]

ScarletColor = [0xFF, 0x24, 0x00]
CopperColor = [0xE9, 0x75, 0x00]
NightBlueColor = [0x19, 0x2F, 0xF0]
MoonColor = [0xD2, 0xD6, 0xFA]
BullBrownColor = [0x40, 0x21, 0x02]
BlackHoovesColor = [0x0A, 0x06, 0x02]

FlagColors = {"Scarlet": ScarletColor,
              "Copper": CopperColor,
              "NightBlue": NightBlueColor,
              "Moon": MoonColor,
              "BullBrown": BullBrownColor,
              "BlackHooves": BlackHoovesColor}

font20 = pygame.font.SysFont('timesnewroman', 20)
font8 = pygame.font.SysFont('arial', 8)
font10 = pygame.font.SysFont('arial', 10)


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_lines_alpha(surface, color, closed, points, points2):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x + 4, max_y - min_y + 1)
    # print("Points " + str(points))
    # print("min_x - " + str(min_x) + " min_y - " + str(min_y))
    # print("target_rect: " + str(target_rect))
    # print(str(target_rect.size))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    # print(str(shape_surf))
    # print(str(surface))
    # pygame.draw.lines(shape_surf, color, False, points, 5)
    # surface.blit(shape_surf, target_rect)
    # draw_surf = pygame.Surface((240, 240), pygame.SRCALPHA)
    # print("GreenColor - " + str((min_x + 70, min_y + 150)) + " " + str((min_x + 170, min_y + 250)))
    # pygame.draw.line(draw_surf, GreenColor, (min_x + 70, min_y + 150), (min_x + 170, min_y + 250), 6)
    # print("DeepGreenColor - " + str((min_x + 40, min_y + 50)) + " " + str((min_x + 140, min_y + 150)))
    # pygame.draw.line(draw_surf, DeepGreenColor, (min_x + 40, min_y + 50), (min_x + 140, min_y + 150), 6)
    # surface.blit(draw_surf, (points2[0], points2[1]))

    # draw_surf2 = pygame.Surface((200, 200), pygame.SRCALPHA)
    # pygame.draw.line(draw_surf2, BlueColor, (50, 150), (150, 250), 6)
    # pygame.draw.line(draw_surf2, DeepBlueColor, (20, 50), (120, 150), 6)
    # surface.blit(draw_surf2, (0, 0))

    draw_surf3 = pygame.Surface((100, 100), pygame.SRCALPHA)  # 100, 100 target_rect[2], target_rect[3]
    # print("BlueColor - " + str((min_x + 70, min_y + 150)) + " " + str((min_x + 170, min_y + 250)))
    # pygame.draw.line(draw_surf3, PinkColor, (10, 20), (160, 40), 6)
    # print("DeepBlueColor - " + str((min_x + 40, min_y + 50)) + " " + str((min_x + 140, min_y + 150)))
    # pygame.draw.line(draw_surf3, DeepPinkColor, (30, 40), (140, 50), 6)

    pygame.draw.lines(draw_surf3, color, closed, points, 3)
    surface.blit(draw_surf3, (points2[0], points2[1]))


def draw_tiles(screen):
    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:

            for TileObj in battle.battle_map:
                x = int(TileObj.posxy[0])
                y = int(TileObj.posxy[1])
                x -= int(battle.battle_pov[0])
                y -= int(battle.battle_pov[1])

                if 0 < x <= 14 and 0 < y <= 8:
                    # print("battle.terrain " + battle.terrain)
                    # print("battle.conditions " + battle.conditions)
                    # Draw tiles 4 times by 48x48 pixels to form 96x96 squares
                    terrain_img = pygame.image.load('img/Terrains/' + battle.conditions + '.png')
                    screen.blit(terrain_img, ((x - 1) * 96 + 1, (y - 1) * 96 + 1))

                    terrain_img = pygame.image.load('img/Terrains/' + battle.conditions + '.png')
                    screen.blit(terrain_img, ((x - 1) * 96 + 49, (y - 1) * 96 + 1))

                    terrain_img = pygame.image.load('img/Terrains/' + battle.conditions + '.png')
                    screen.blit(terrain_img, ((x - 1) * 96 + 1, (y - 1) * 96 + 49))

                    terrain_img = pygame.image.load('img/Terrains/' + battle.conditions + '.png')
                    screen.blit(terrain_img, ((x - 1) * 96 + 49, (y - 1) * 96 + 49))

                    # Border line
                    pygame.draw.polygon(screen, TileBorder,
                                        [[(x - 1) * 96 + 1, (y - 1) * 96 + 1], [(x - 1) * 96 + 96, (y - 1) * 96 + 1],
                                         [(x - 1) * 96 + 96, (y - 1) * 96 + 96], [(x - 1) * 96 + 1, (y - 1) * 96 + 96]],
                                        1)

                    # Obstacles
                    if TileObj.obstacle is not None:
                        for item in TileObj.obstacle.disposition:
                            obj_cal = objects_img_catalog.object_calendar[TileObj.obstacle.obj_name]
                            season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.game_month]
                            obj_img = pygame.image.load('img/' +
                                                        TileObj.obstacle.img_path + obj_cal[season] +
                                                        '.png')
                            obj_img.set_colorkey(WhiteColor)
                            screen.blit(obj_img, ((x - 1) * 96 + item[0], (y - 1) * 96 + item[1]))

                    # Highlight selected unit with white border
                    if TileObj.posxy == battle.selected_unit_alt:
                        # print("Success TileObj.posxy - " + str(TileObj.posxy))
                        pygame.draw.polygon(screen, WhiteBorder,
                                            [[(x - 1) * 96 + 1, (y - 1) * 96 + 1],
                                             [(x - 1) * 96 + 96, (y - 1) * 96 + 1],
                                             [(x - 1) * 96 + 96, (y - 1) * 96 + 96],
                                             [(x - 1) * 96 + 1, (y - 1) * 96 + 96]], 1)

                    # Highlight active unit with green border for human player
                    if battle.realm_in_control == game_stats.player_power:
                        if battle.queue[0].obj_type == "Regiment" and battle.ready_to_act:
                            if TileObj.posxy == tuple(battle.queue[0].position):
                                # print("Success TileObj.posxy - " + str(TileObj.posxy))
                                global LimeBorder
                                LimeBorder = anim_battle_effects.border_blipping(LimeBorder)
                                # pygame.draw.polygon(screen, LimeBorder,
                                #                     [[(x - 1) * 96 + 1, (y - 1) * 96 + 1],
                                #                      [(x - 1) * 96 + 96, (y - 1) * 96 + 1],
                                #                      [(x - 1) * 96 + 96, (y - 1) * 96 + 96],
                                #                      [(x - 1) * 96 + 1, (y - 1) * 96 + 96]], 1)

                                points = [(1, 1), (96, 1), (96, 96), (1, 96)]
                                points2 = [(x - 1) * 96, (y - 1) * 96]
                                draw_lines_alpha(screen, LimeBorder, True, points, points2)

                    # Highlight with light green color movement grid
                    if battle.realm_in_control == game_stats.player_power:
                        if battle.movement_grid is not None:
                            if [int(TileObj.posxy[0]), int(TileObj.posxy[1])] in battle.movement_grid:
                                draw_rect_alpha(screen, GreenGrid, ((x - 1) * 96 + 1, (y - 1) * 96 + 1, 96, 96))

            for TileObj in battle.battle_map:
                x = TileObj.posxy[0]
                y = TileObj.posxy[1]
                x -= int(battle.battle_pov[0])
                y -= int(battle.battle_pov[1])

                if 0 < x <= 14 and 0 < y <= math.ceil(game_stats.game_window_height):
                    # Cover tiles with dark color in preparation stage
                    if battle.stage == "Formation":
                        if battle.cover_map[0] <= TileObj.posxy[0] <= battle.cover_map[2] and \
                                battle.cover_map[1] <= TileObj.posxy[1] <= battle.cover_map[3]:

                            draw_rect_alpha(screen, TileCover,
                                            ((x - 1) * 96 + 1, (y - 1) * 96 + 1, 96, 96))

                    # Units
                    # print("# Units")
                    if TileObj.army_id is not None:
                        # print(str(TileObj.posxy))
                        focus = TileObj.army_id
                        for army in game_obj.game_armies:
                            if army.army_id == focus:
                                # Player should see only his army at formation stage
                                if (army.owner == game_stats.player_power and battle.stage == "Formation") or \
                                        battle.stage != "Formation":

                                    unit = army.units[TileObj.unit_index]

                                    # Draw direction lines
                                    draw_direction_lines(screen, unit.direction, x, y)

                                    # army_img = pygame.image.load(
                                    #     'img/Creatures/' + str(unit.img_source) + "/" + str(unit.img) + '.png')
                                    # army_img.set_colorkey(WhiteColor)
                                    # screen.blit(army_img,
                                    #             ((x - 1) * 96,
                                    #              (y - 1) * 96))

                                    # Draw creatures
                                    draw_creatures(screen, unit, x, y, army.owner, TileObj.unit_index, battle,
                                                   TileObj.posxy)


def draw_direction_lines(screen, direction, x, y):
    if direction == "E":
        # print("x " + str(x) + " y " + str(y))
        points = [(96, 3), (98, 48), (98, 49), (96, 94)]  # [(96, 3), (98, 48), (98, 49), (96, 94)]
        # [(0, 0), (2, 45), (2, 46), (0, 91)]
        points2 = [(x - 1) * 96, (y - 1) * 96]  # [(x - 1) * 96, (y - 1) * 96]
        # [(x - 1) * 96 + 96, (y - 1) * 96 + 3]
        # print("Points: " + str(points))
        # points = [(25, 0), (50, 25), (25, 50), (0, 25)]
        # pygame.draw.lines(screen, LightYellow, False, points)
        # pygame.draw.lines(screen, LightYellow, False, points, 2)
        # pygame.draw.line(screen, RedColor, ((x - 1) * 96 + 96, (y - 1) * 96 + 1),
        # ((x - 1) * 96 + 96, (y - 1) * 96 + 96))
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "W":
        # print("x " + str(x) + " y " + str(y))
        points = [(2, 3), (0, 48), (0, 49), (2, 94)]
        points2 = [(x - 1) * 96 - 2, (y - 1) * 96]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "N":
        # print("x " + str(x) + " y " + str(y))
        points = [(3, 2), (48, 0), (49, 0), (94, 2)]
        points2 = [(x - 1) * 96, (y - 1) * 96 - 2]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "S":
        # print("x " + str(x) + " y " + str(y))
        points = [(3, 96), (48, 98), (49, 98), (94, 96)]
        points2 = [(x - 1) * 96, (y - 1) * 96]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "NE":
        # print("x " + str(x) + " y " + str(y))
        points = [(50, 2), (98, 0), (96, 48)]
        points2 = [(x - 1) * 96, (y - 1) * 96 - 2]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "SE":
        # print("x " + str(x) + " y " + str(y))
        points = [(96, 50), (98, 98), (50, 96)]
        points2 = [(x - 1) * 96, (y - 1) * 96]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "SW":
        # print("x " + str(x) + " y " + str(y))
        points = [(2, 50), (0, 98), (48, 96)]
        points2 = [(x - 1) * 96 - 2, (y - 1) * 96]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "NW":
        # print("x " + str(x) + " y " + str(y))
        points = [(2, 48), (0, 0), (48, 2)]
        points2 = [(x - 1) * 96 - 2, (y - 1) * 96 - 2]
        draw_lines_alpha(screen, LightYellow, False, points, points2)


def draw_creatures(screen, unit, x, y, owner, unit_index, b, current_position):

    if unit.direction == "E":
        total = len(unit.crew)
        index = 0
        while index <= total - 1:

            row = math.ceil((index + 1) / unit.number)
            if (index + 1) % unit.number == 0:
                line = unit.number
            else:
                line = (index + 1) % unit.number

            creature_position = [(x - 1) * 96 + 4 + 90 - unit.crew[index].img_width -
                                 (row - 1) * ((90 - unit.crew[index].img_width) / (unit.rows - 1)),
                                 (y - 1) * 96 + 4 + 90 - unit.crew[index].img_height -
                                 (unit.number - line) * ((90 - unit.crew[index].img_height) / (unit.number - 1))]

            xy_animation = [0, 0]
            if b.primary == "Rotate":
                xy_animation = anim_battle_unit_action.unit_rotate(b, unit_index, owner, current_position,
                                                                   creature_position, unit.number, row, line,
                                                                   unit.crew[index].img_width,
                                                                   unit.crew[index].img_height, unit.rows)
            elif b.primary == "Move":
                xy_animation = anim_battle_unit_action.unit_march(b, unit_index, current_position, creature_position,
                                                                  unit.number, row, line, unit.crew[index].img_width,
                                                                  unit.crew[index].img_height, unit.rows, owner)

            army_img = pygame.image.load(
                'img/Creatures/' + str(unit.crew[index].img_source) + "/" + str(unit.crew[index].img) + '.png')
            army_img.set_colorkey(WhiteColor)
            screen.blit(army_img,
                        (creature_position[0] + xy_animation[0],
                         creature_position[1] + xy_animation[1]))

            index += 1

    elif unit.direction == "W":
        total = len(unit.crew)
        index = 0
        while index <= total - 1:
            row = math.ceil((index + 1) / unit.number)
            if (index + 1) % unit.number == 0:
                line = unit.number
            else:
                line = (index + 1) % unit.number

            creature_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                 (row - 1) * ((90 - unit.crew[index].img_width) / (unit.rows - 1)),
                                 (y - 1) * 96 + 4 + 90 - unit.crew[index].img_height -
                                 (unit.number - line) * ((90 - unit.crew[index].img_height) / (unit.number - 1))]

            xy_animation = [0, 0]
            if b.primary == "Rotate":
                xy_animation = anim_battle_unit_action.unit_rotate(b, unit_index, owner, current_position,
                                                                   creature_position, unit.number, row, line,
                                                                   unit.crew[index].img_width,
                                                                   unit.crew[index].img_height, unit.rows)
            elif b.primary == "Move":
                xy_animation = anim_battle_unit_action.unit_march(b, unit_index, current_position, creature_position,
                                                                  unit.number, row, line, unit.crew[index].img_width,
                                                                  unit.crew[index].img_height, unit.rows, owner)

            army_img = pygame.image.load(
                'img/Creatures/' + str(unit.crew[index].img_source) + "/" + str(unit.crew[index].img) + '.png')
            army_img.set_colorkey(WhiteColor)
            screen.blit(army_img,
                        (creature_position[0] + xy_animation[0],
                         creature_position[1] + xy_animation[1]))

            index += 1

    elif unit.direction == "N":
        total = len(unit.crew)
        index = 0
        while index <= total - 1:
            row = math.ceil((index + 1) / unit.number)
            if (index + 1) % unit.number == 0:
                line = unit.number
            else:
                line = (index + 1) % unit.number

            creature_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                 (unit.number - line) * ((90 - unit.crew[index].img_width) / (unit.number - 1)),
                                 (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                                 (row - 1) * ((90 - unit.crew[index].img_height) / (unit.rows - 1))]

            xy_animation = [0, 0]
            if b.primary == "Rotate":
                xy_animation = anim_battle_unit_action.unit_rotate(b, unit_index, owner, current_position,
                                                                   creature_position, unit.number, row, line,
                                                                   unit.crew[index].img_width,
                                                                   unit.crew[index].img_height, unit.rows)
            elif b.primary == "Move":
                xy_animation = anim_battle_unit_action.unit_march(b, unit_index, current_position, creature_position,
                                                                  unit.number, row, line, unit.crew[index].img_width,
                                                                  unit.crew[index].img_height, unit.rows, owner)

            army_img = pygame.image.load(
                'img/Creatures/' + str(unit.crew[index].img_source) + "/" + str(unit.crew[index].img) + '.png')
            army_img.set_colorkey(WhiteColor)
            screen.blit(army_img,
                        (creature_position[0] + xy_animation[0],
                         creature_position[1] + xy_animation[1]))

            index += 1

    elif unit.direction == "S":
        total = len(unit.crew)
        index = int(len(unit.crew) - 1)
        while index >= 0:
            row = math.ceil((index + 1) / unit.number)
            if (index + 1) % unit.number == 0:
                line = unit.number
            else:
                line = (index + 1) % unit.number

            creature_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                 (unit.number - line) * ((90 - unit.crew[index].img_width) / (unit.number - 1)),
                                 (y - 1) * 96 + 4 + 90 - unit.crew[index].img_height -
                                 (row - 1) * ((90 - unit.crew[index].img_height) / (unit.rows - 1))]

            xy_animation = [0, 0]
            if b.primary == "Rotate":
                xy_animation = anim_battle_unit_action.unit_rotate(b, unit_index, owner, current_position,
                                                                   creature_position, unit.number, row, line,
                                                                   unit.crew[index].img_width,
                                                                   unit.crew[index].img_height, unit.rows)
            elif b.primary == "Move":
                xy_animation = anim_battle_unit_action.unit_march(b, unit_index, current_position, creature_position,
                                                                  unit.number, row, line, unit.crew[index].img_width,
                                                                  unit.crew[index].img_height, unit.rows, owner)

            army_img = pygame.image.load(
                'img/Creatures/' + str(unit.crew[index].img_source) + "/" + str(unit.crew[index].img) + '.png')
            army_img.set_colorkey(WhiteColor)
            screen.blit(army_img,
                        (creature_position[0] + xy_animation[0],
                         creature_position[1] + xy_animation[1]))

            index -= 1

    elif unit.direction == "NE":
        total = len(unit.crew)
        index = 0
        while index <= total - 1:
            row = math.ceil((index + 1) / unit.number)
            if (index + 1) % unit.number == 0:
                line = unit.number
            else:
                line = (index + 1) % unit.number

            creature_position = [(x - 1) * 96 + 48 - (unit.crew[index].img_width / 2) -
                                 (row - 1) * (48 / (unit.rows - 1)) + (line - 1) * (40 / (unit.number - 1)),
                                 (y - 1) * 96 + 48 - (unit.crew[index].img_height / 2) -
                                 (unit.number - line) * (48 / (unit.number - 1)) +
                                 (row - 1) * (40 / (unit.rows - 1))]

            xy_animation = [0, 0]
            if b.primary == "Rotate":
                xy_animation = anim_battle_unit_action.unit_rotate(b, unit_index, owner, current_position,
                                                                   creature_position, unit.number, row, line,
                                                                   unit.crew[index].img_width,
                                                                   unit.crew[index].img_height, unit.rows)
            elif b.primary == "Move":
                xy_animation = anim_battle_unit_action.unit_march(b, unit_index, current_position, creature_position,
                                                                  unit.number, row, line, unit.crew[index].img_width,
                                                                  unit.crew[index].img_height, unit.rows, owner)

            army_img = pygame.image.load(
                'img/Creatures/' + str(unit.crew[index].img_source) + "/" + str(unit.crew[index].img) + '.png')
            army_img.set_colorkey(WhiteColor)
            screen.blit(army_img,
                        (creature_position[0] + xy_animation[0],
                         creature_position[1] + xy_animation[1]))

            index += 1

    elif unit.direction == "NW":
        total = len(unit.crew)
        index = 0
        while index <= total - 1:
            row = math.ceil((index + 1) / unit.number)
            if (index + 1) % unit.number == 0:
                line = unit.number
            else:
                line = (index + 1) % unit.number

            creature_position = [(x - 1) * 96 + 48 - (unit.crew[index].img_width / 2) +
                                 (row - 1) * (48 / (unit.rows - 1)) - (line - 1) * (40 / (unit.number - 1)),
                                 (y - 1) * 96 + 48 - (unit.crew[index].img_height / 2) -
                                 (unit.number - line) * (48 / (unit.number - 1)) +
                                 (row - 1) * (40 / (unit.rows - 1))]

            xy_animation = [0, 0]
            if b.primary == "Rotate":
                xy_animation = anim_battle_unit_action.unit_rotate(b, unit_index, owner, current_position,
                                                                   creature_position, unit.number, row, line,
                                                                   unit.crew[index].img_width,
                                                                   unit.crew[index].img_height, unit.rows)
            elif b.primary == "Move":
                xy_animation = anim_battle_unit_action.unit_march(b, unit_index, current_position, creature_position,
                                                                  unit.number, row, line, unit.crew[index].img_width,
                                                                  unit.crew[index].img_height, unit.rows, owner)

            army_img = pygame.image.load(
                'img/Creatures/' + str(unit.crew[index].img_source) + "/" + str(unit.crew[index].img) + '.png')
            army_img.set_colorkey(WhiteColor)
            screen.blit(army_img,
                        (creature_position[0] + xy_animation[0],
                         creature_position[1] + xy_animation[1]))

            index += 1

    elif unit.direction == "SE":
        total = len(unit.crew)
        index = int(len(unit.crew) - 1)
        while index >= 0:
            row = math.ceil((index + 1) / unit.number)
            if (index + 1) % unit.number == 0:
                line = unit.number
            else:
                line = (index + 1) % unit.number

            creature_position = [(x - 1) * 96 + 48 - (unit.crew[index].img_width / 2) -
                                 (row - 1) * (48 / (unit.rows - 1)) + (line - 1) * (40 / (unit.number - 1)),
                                 (y - 1) * 96 + 48 - (unit.crew[index].img_height / 2) +
                                 (unit.number - line) * (48 / (unit.number - 1)) -
                                 (row - 1) * (40 / (unit.rows - 1))]

            xy_animation = [0, 0]
            if b.primary == "Rotate":
                xy_animation = anim_battle_unit_action.unit_rotate(b, unit_index, owner, current_position,
                                                                   creature_position, unit.number, row, line,
                                                                   unit.crew[index].img_width,
                                                                   unit.crew[index].img_height, unit.rows)
            elif b.primary == "Move":
                xy_animation = anim_battle_unit_action.unit_march(b, unit_index, current_position, creature_position,
                                                                  unit.number, row, line, unit.crew[index].img_width,
                                                                  unit.crew[index].img_height, unit.rows, owner)

            army_img = pygame.image.load(
                'img/Creatures/' + str(unit.crew[index].img_source) + "/" + str(unit.crew[index].img) + '.png')
            army_img.set_colorkey(WhiteColor)
            screen.blit(army_img,
                        (creature_position[0] + xy_animation[0],
                         creature_position[1] + xy_animation[1]))

            index -= 1

    elif unit.direction == "SW":
        total = len(unit.crew)
        index = int(len(unit.crew) - 1)
        while index >= 0:
            row = math.ceil((index + 1) / unit.number)
            if (index + 1) % unit.number == 0:
                line = unit.number
            else:
                line = (index + 1) % unit.number

            creature_position = [(x - 1) * 96 + 48 - (unit.crew[index].img_width / 2) +
                                 (row - 1) * (48 / (unit.rows - 1)) - (line - 1) * (40 / (unit.number - 1)),
                                 (y - 1) * 96 + 48 - (unit.crew[index].img_height / 2) +
                                 (unit.number - line) * (48 / (unit.number - 1)) -
                                 (row - 1) * (40 / (unit.rows - 1))]

            xy_animation = [0, 0]
            if b.primary == "Rotate":
                xy_animation = anim_battle_unit_action.unit_rotate(b, unit_index, owner, current_position,
                                                                   creature_position, unit.number, row, line,
                                                                   unit.crew[index].img_width,
                                                                   unit.crew[index].img_height, unit.rows)
            elif b.primary == "Move":
                xy_animation = anim_battle_unit_action.unit_march(b, unit_index, current_position, creature_position,
                                                                  unit.number, row, line, unit.crew[index].img_width,
                                                                  unit.crew[index].img_height, unit.rows, owner)

            army_img = pygame.image.load(
                'img/Creatures/' + str(unit.crew[index].img_source) + "/" + str(unit.crew[index].img) + '.png')
            army_img.set_colorkey(WhiteColor)
            screen.blit(army_img,
                        (creature_position[0] + xy_animation[0],
                         creature_position[1] + xy_animation[1]))

            index -= 1

    if owner != "Neutral":  # Draw flag
        for power in game_obj.game_powers:
            if owner == power.name:
                xy_animation = [0, 0]  # Temporary, delete this when animation would be implemented
                pygame.draw.polygon(screen, FlagpoleColor,
                                    ([(x - 1) * 96 + 3 + xy_animation[0],
                                      (y - 1) * 96 + 80 + xy_animation[1]],
                                     [(x - 1) * 96 + 4 + xy_animation[0],
                                      (y - 1) * 96 + 80 + xy_animation[1]],
                                     [(x - 1) * 96 + 4 + xy_animation[0],
                                      (y - 1) * 96 + 96 + xy_animation[1]],
                                     [(x - 1) * 96 + 3 + xy_animation[0],
                                      (y - 1) * 96 + 96 + xy_animation[1]]))
                pygame.draw.polygon(screen, FlagColors[power.f_color],
                                    ([(x - 1) * 96 + 5 + xy_animation[0],
                                      (y - 1) * 96 + 80 + xy_animation[1]],
                                     [(x - 1) * 96 + 11 + xy_animation[0],
                                      (y - 1) * 96 + 80 + xy_animation[1]],
                                     [(x - 1) * 96 + 11 + xy_animation[0],
                                      (y - 1) * 96 + 84 + xy_animation[1]],
                                     [(x - 1) * 96 + 5 + xy_animation[0],
                                      (y - 1) * 96 + 84 + xy_animation[1]]))
                pygame.draw.polygon(screen, FlagColors[power.s_color],
                                    ([(x - 1) * 96 + 5 + xy_animation[0],
                                      (y - 1) * 96 + 84 + xy_animation[1]],
                                     [(x - 1) * 96 + 11 + xy_animation[0],
                                      (y - 1) * 96 + 84 + xy_animation[1]],
                                     [(x - 1) * 96 + 11 + xy_animation[0],
                                      (y - 1) * 96 + 89 + xy_animation[1]],
                                     [(x - 1) * 96 + 5 + xy_animation[0],
                                      (y - 1) * 96 + 89 + xy_animation[1]]))

    # Blink rad color over unit during fight
    if b.primary == "Melee attack" or b.primary == "Counterattack" or b.primary == "Ranged attack":
        anim_battle_effects.damage_dealt_red(screen, b, owner, unit_index, current_position)


def draw_waiting_list(screen, b):
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, LightBackground,
                        [[360, 740 + yVar], [920, 740 + yVar], [920, 800 + yVar], [360, 800 + yVar]])

    # Arrows
    pygame.draw.polygon(screen, RockTunel, [[360, 740 + yVar], [380, 740 + yVar], [380, 800 + yVar], [360, 800 + yVar]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[360, 740 + yVar], [380, 740 + yVar],
                                                     [380, 800 + yVar], [360, 800 + yVar]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(376, 762 + yVar), (364, 770 + yVar), (376, 778 + yVar)], 2)

    pygame.draw.polygon(screen, RockTunel, [[900, 740 + yVar], [920, 740 + yVar], [920, 800 + yVar], [900, 800 + yVar]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[900, 740 + yVar], [920, 740 + yVar],
                                                     [920, 800 + yVar], [900, 800 + yVar]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(904, 762 + yVar), (916, 770 + yVar), (904, 778 + yVar)], 2)

    # Units
    if b.attacker_realm == game_stats.player_power:
        player_id = int(b.attacker_id)
    else:
        player_id = int(b.defender_id)

    for army in game_obj.game_armies:
        if army.army_id == player_id:
            a = army

    number = 0
    for unit in b.waiting_list:
        if b.waiting_index <= number <= 9 + b.waiting_index:
            x_pos = 380 + (number - b.waiting_index) * 52
            y_pos = 744 + yVar

            army_img = pygame.image.load(
                'img/Creatures/' + str(a.units[unit].img_source) + "/" + str(a.units[unit].img) + '.png')
            army_img.set_colorkey(WhiteColor)
            screen.blit(army_img, [x_pos + a.units[unit].x_offset, y_pos + a.units[unit].y_offset])

            # Highlight selected unit card
            if b.unit_card != -1:
                if 0 <= b.unit_card - b.waiting_index <= 9:
                    unit_pos = 380 + int(b.unit_card - b.waiting_index) * 52
                    pygame.draw.polygon(screen, WhiteBorder,
                                        [[unit_pos + 1, 740 + yVar],
                                         [unit_pos + 52, 740 + yVar],
                                         [unit_pos + 52, 800 + yVar],
                                         [unit_pos + 1, 800 + yVar]], 1)

            # Number of creatures in regiment
            text_panel = font8.render(str(len(a.units[unit].crew)) + "/"
                                      + str(a.units[unit].number * a.units[unit].rows), True, DarkText)
            screen.blit(text_panel, [384 + (number - b.waiting_index) * 52, 744 + yVar])

        number += 1


def draw_queue(screen, b):
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, LightBackground,
                        [[360, 740 + yVar], [920, 740 + yVar], [920, 800 + yVar], [360, 800 + yVar]])

    # Arrows
    pygame.draw.polygon(screen, RockTunel, [[360, 740 + yVar], [380, 740 + yVar], [380, 800 + yVar], [360, 800 + yVar]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[360, 740 + yVar], [380, 740 + yVar],
                                                     [380, 800 + yVar], [360, 800 + yVar]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(376, 762 + yVar), (364, 770 + yVar), (376, 778 + yVar)], 2)

    pygame.draw.polygon(screen, RockTunel, [[900, 740 + yVar], [920, 740 + yVar], [920, 800 + yVar], [900, 800 + yVar]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[900, 740 + yVar], [920, 740 + yVar],
                                                     [920, 800 + yVar], [900, 800 + yVar]], 3)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(904, 762 + yVar), (916, 770 + yVar), (904, 778 + yVar)], 2)

    number = 0
    for card in b.queue:
        if card.obj_type == "Regiment":
            if b.queue_index <= number <= 9 + b.queue_index:
                x_pos = 380 + (number - b.queue_index) * 52
                y_pos = 744 + yVar

                card_img = pygame.image.load('img/Creatures/' + str(card.img_source) + "/" + str(card.img) + '.png')
                card_img.set_colorkey(WhiteColor)
                screen.blit(card_img, [x_pos + card.x_offset, y_pos + card.y_offset])

                # # Highlight selected unit card
                # if b.unit_card != -1:
                #     if 0 <= b.unit_card - b.waiting_index <= 9:
                #         unit_pos = 380 + int(b.unit_card - b.waiting_index) * 52
                #         pygame.draw.polygon(screen, WhiteBorder,
                #                             [[unit_pos + 1, 740 + yVar],
                #                              [unit_pos + 52, 740 + yVar],
                #                              [unit_pos + 52, 800 + yVar],
                #                              [unit_pos + 1, 800 + yVar]], 1)

                # Number of creatures in regiment

                for army in game_obj.game_armies:
                    if army.army_id == card.army_id:
                        a = army
                text_panel = font10.render(str(len(a.units[card.number].crew)) + "/"
                                           + str(a.units[card.number].number * a.units[card.number].rows),
                                           True, DarkText)
                screen.blit(text_panel, [384 + (number - b.queue_index) * 52, 742 + yVar])

                # Regiment's morale
                text_panel = font10.render(str(a.units[card.number].morale), True, DarkText)
                screen.blit(text_panel, [x_pos + 4, y_pos + 8])

                if card.f_color is not None:  # Draw flag
                    pygame.draw.polygon(screen, FlagpoleColor,
                                        ([x_pos + 3, y_pos + 44],
                                         [x_pos + 4, y_pos + 44],
                                         [x_pos + 4, y_pos + 60],
                                         [x_pos + 3, y_pos + 60]))
                    pygame.draw.polygon(screen, FlagColors[card.f_color],
                                        ([x_pos + 5, y_pos + 44],
                                         [x_pos + 11, y_pos + 44],
                                         [x_pos + 11, y_pos + 48],
                                         [x_pos + 5, y_pos + 48]))
                    pygame.draw.polygon(screen, FlagColors[card.s_color],
                                        ([x_pos + 5, y_pos + 48],
                                         [x_pos + 11, y_pos + 48],
                                         [x_pos + 11, y_pos + 53],
                                         [x_pos + 5, y_pos + 53]))

                # Act time
                text_panel = font10.render(str(b.queue[number - b.queue_index].time_act), True, DarkText)
                screen.blit(text_panel, [396 + (number - b.queue_index) * 52, 788 + yVar])

            number += 1


def battle_screen(screen):
    yVar = game_stats.game_window_height - 800

    screen.fill(MapLimitColor)  # background

    draw_tiles(screen)  # Draw tiles

    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:
            b = battle

    if b.stage == "Formation":
        # Start battle button
        pygame.draw.polygon(screen, FillButton, [[580, 10], [700, 10], [700, 32], [580, 32]])
        pygame.draw.polygon(screen, BorderNewGameColor, [[580, 10], [700, 10], [700, 32], [580, 32]], 3)

        text_NewGame1 = font20.render("Start battle", True, TitleText)
        screen.blit(text_NewGame1, [595, 10])

        # Waiting list lower panel
        if len(b.waiting_list) > 0:
            draw_waiting_list(screen, b)

    elif b.stage == "Fighting":
        draw_queue(screen, b)

        # Wait button
        # Let regiment or hero spent 0,5 time
        pygame.draw.polygon(screen, FieldColor, [[235, 740 + yVar], [357, 740 + yVar],
                                                 [357, 765 + yVar], [235, 765 + yVar]])
        if b.realm_in_control == game_stats.player_power:
            color = HighlightOption
        else:
            color = LineMainMenuColor1
        pygame.draw.polygon(screen, color, [[235, 740 + yVar], [357, 740 + yVar],
                                            [357, 765 + yVar], [235, 765 + yVar]], 3)

        text_NewGame1 = font20.render("Wait (Q)", True, TitleText)
        screen.blit(text_NewGame1, [275, 741 + yVar])

        hourglass_img = pygame.image.load('img/Icons/battle_hourglass.png')
        hourglass_img.set_colorkey(WhiteColor)
        screen.blit(hourglass_img, (240, 742 + yVar))

        # Defence button
        # Let regiment increase its defence parameter and spent 1.0 time
        pygame.draw.polygon(screen, FieldColor, [[235, 770 + yVar], [357, 770 + yVar],
                                                 [357, 795 + yVar], [235, 795 + yVar]])
        if b.realm_in_control == game_stats.player_power:
            color = HighlightOption
        else:
            color = LineMainMenuColor1
        pygame.draw.polygon(screen, color, [[235, 770 + yVar], [357, 770 + yVar],
                                            [357, 795 + yVar], [235, 795 + yVar]], 3)

        text_NewGame1 = font20.render("Defend (E)", True, TitleText)
        screen.blit(text_NewGame1, [265, 771 + yVar])

        shield_img = pygame.image.load('img/Icons/battle_shield.png')
        shield_img.set_colorkey(WhiteColor)
        screen.blit(shield_img, (240, 772 + yVar))

        # Attack method button
        # Change between attack methods if possible
        if b.realm_in_control == game_stats.player_power:
            if b.queue[0].obj_type == "Regiment" and b.ready_to_act:
                change_cursor(screen, b)

                pygame.draw.polygon(screen, FieldColor, [[923, 740 + yVar], [1100, 740 + yVar],
                                                         [1100, 795 + yVar], [923, 795 + yVar]])
                pygame.draw.polygon(screen, LineMainMenuColor1, [[923, 740 + yVar], [1100, 740 + yVar],
                                                                 [1100, 795 + yVar], [923, 795 + yVar]], 3)

                attack_method = b.attack_type_in_use
                text_NewGame1 = font20.render(attack_method, True, TitleText)
                screen.blit(text_NewGame1, [985, 755 + yVar])

                shield_img = pygame.image.load('img/Icons/' + attack_method + '.png')
                shield_img.set_colorkey(WhiteColor)
                screen.blit(shield_img, (925, 742 + yVar))
            else:
                pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(True)

        if b.anim_message is not None:
            anim_battle_effects.message_float(screen, b)


def change_cursor(screen, b):
    # if not pygame.mouse.get_visible():

    x = math.ceil(game_stats.mouse_position[0] / 96)
    y = math.ceil(game_stats.mouse_position[1] / 96)
    x = int(x) + int(b.battle_pov[0])
    y = int(y) + int(b.battle_pov[1])

    TileNum = (y - 1) * game_stats.battle_width + x - 1

    if b.attacker_realm == b.realm_in_control:
        enemy = b.defender_id
    else:
        enemy = b.attacker_id

    if 0 < x <= game_stats.battle_width and 0 < y <= game_stats.battle_height:
        if b.battle_map[TileNum].army_id == enemy:

            if b.attack_type_in_use == "Ranged":
                distance = (math.sqrt(((b.battle_map[TileNum].posxy[0] - b.queue[0].position[0]) ** 2) + (
                           (b.battle_map[TileNum].posxy[1] - b.queue[0].position[1]) ** 2)))
                # print("Distance - " + str(distance))
                if distance > b.cur_range_limit:
                    # print("1. distance " + str(distance) + " > b.cur_range_limit " + str(b.cur_range_limit))
                    pass
                elif distance > b.cur_effective_range:
                    # print("2. distance " + str(distance) + " > b.cur_effective_range " + str(b.cur_effective_range))
                    pygame.mouse.set_visible(False)
                    ranged_attack_img = pygame.image.load('img/Icons/broken_ranged_attack.png')
                    ranged_attack_img.set_colorkey(WhiteColor)
                    screen.blit(ranged_attack_img, game_stats.mouse_position)
                else:
                    # print("3. distance " + str(distance) + " <= b.cur_effective_range " + str(b.cur_effective_range))
                    pygame.mouse.set_visible(False)
                    ranged_attack_img = pygame.image.load('img/Icons/ranged_attack.png')
                    ranged_attack_img.set_colorkey(WhiteColor)
                    screen.blit(ranged_attack_img, game_stats.mouse_position)

            elif b.attack_type_in_use == "Melee":
                x2 = game_stats.mouse_position[0] % 96
                y2 = game_stats.mouse_position[1] % 96
                # print("x, y - " + str([x2, y2]))
                check = False
                if x2 < 32:
                    if y2 < 32:
                        word = "melee_attack_nw"
                        offset = (list(game_stats.mouse_position)[0] - 46, list(game_stats.mouse_position)[1] - 46)
                    elif 32 <= y2 < 64:
                        word = "melee_attack_w"
                        offset = (list(game_stats.mouse_position)[0] - 55, list(game_stats.mouse_position)[1] - 9)
                    elif 64 <= y2:
                        word = "melee_attack_sw"
                        offset = (list(game_stats.mouse_position)[0] - 46, list(game_stats.mouse_position)[1])
                elif 32 <= x2 < 64:
                    if y2 < 32:
                        word = "melee_attack_n"
                        offset = (list(game_stats.mouse_position)[0] - 9, list(game_stats.mouse_position)[1] - 55)
                    elif 32 <= y2 < 64:
                        check = True
                    elif 64 <= y2:
                        word = "melee_attack_s"
                        offset = (list(game_stats.mouse_position)[0] - 9, list(game_stats.mouse_position)[1])
                elif 64 <= x2 < 96:
                    if y2 < 32:
                        word = "melee_attack_ne"
                        offset = (list(game_stats.mouse_position)[0], list(game_stats.mouse_position)[1] - 46)
                    elif 32 <= y2 < 64:
                        word = "melee_attack_e"
                        offset = (list(game_stats.mouse_position)[0], list(game_stats.mouse_position)[1] - 9)
                    elif 64 <= y2:
                        word = "melee_attack_se"
                        offset = (list(game_stats.mouse_position)[0], list(game_stats.mouse_position)[1])
                if check:
                    pygame.mouse.set_visible(True)
                else:
                    pygame.mouse.set_visible(False)
                    melee_attack_img = pygame.image.load('img/Icons/' + word + '.png')
                    melee_attack_img.set_colorkey(WhiteColor)
                    screen.blit(melee_attack_img, offset)
        else:
            pygame.mouse.set_visible(True)
