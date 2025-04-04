## Among Myth and Wonder
## sc_battle

import math
import pygame.draw
import pygame.font
import pygame.mouse

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Content import objects_img_catalog
from Content import terrain_seasons
from Content import siege_warfare_catalog

from Resources import game_obj
from Resources import game_stats
from Resources import common_selects
from Resources.Game_Graphics import graphics_obj

from Screens.Sc_Battle import anim_battle_effects
from Screens.Sc_Battle import anim_battle_unit_action
from Screens.Sc_Battle import anim_battle_message
from Screens.Sc_Battle import draw_creatures_funs

from Screens.Sc_Battle_Windows import abilities_menu, battle_regiment_information

pygame.init()


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
    battle = game_stats.present_battle

    for TileObj in battle.battle_map:
        x = int(TileObj.posxy[0])
        y = int(TileObj.posxy[1])
        x -= int(battle.battle_pov[0])
        y -= int(battle.battle_pov[1])

        if 0 < x <= 14 and 0 < y <= 8:
            # print("battle.terrain " + battle.terrain)
            # print("battle.conditions " + battle.conditions)
            # Draw tiles 4 times by 48x48 pixels to form 96x96 squares
            terrain_img = game_stats.gf_terrain_dict[battle.conditions]
            screen.blit(terrain_img, ((x - 1) * 96, (y - 1) * 96))
            screen.blit(terrain_img, ((x - 1) * 96 + 48, (y - 1) * 96))
            screen.blit(terrain_img, ((x - 1) * 96, (y - 1) * 96 + 48))
            screen.blit(terrain_img, ((x - 1) * 96 + 48, (y - 1) * 96 + 48))

            # Border line
            terrain_img = game_stats.gf_terrain_dict["Terrains/border_96_96_170"]
            screen.blit(terrain_img, ((x - 1) * 96, (y - 1) * 96))

            # Obstacles
            if TileObj.map_object:
                if TileObj.map_object.obj_type == "Obstacle":
                    for item in TileObj.map_object.disposition:
                        obj_cal = objects_img_catalog.object_calendar[TileObj.map_object.obj_name]
                        season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.game_month]

                        obj_img = game_stats.gf_obstacle_dict[obj_cal[season] + "_0" + item[2]]
                        screen.blit(obj_img, ((x - 1) * 96 + item[0] - obj_img.get_width() / 2,
                                              (y - 1) * 96 + item[1] - obj_img.get_height() / 2))

                # Structures
                elif TileObj.map_object.obj_type == "Structure":
                    x1 = TileObj.map_object.disposition[0]
                    y1 = TileObj.map_object.disposition[1]
                    obj_img = game_stats.gf_obstacle_dict[TileObj.map_object.obj_name]
                    screen.blit(obj_img, ((x - 1) * 96 + x1, (y - 1) * 96 + y1))

            # Highlight active unit with green border for human player
            if battle.realm_in_control == game_stats.player_power:
                if battle.queue[0].obj_type == "Regiment" and battle.ready_to_act:
                    if TileObj.posxy == tuple(battle.queue[0].position):
                        # print("Success TileObj.posxy - " + str(TileObj.posxy))
                        highlight_border = anim_battle_effects.border_blipping(LimeBorder)

                        points = [(1, 1), (94, 1), (94, 94), (1, 94)]
                        points2 = [(x - 1) * 96, (y - 1) * 96]
                        draw_lines_alpha(screen, highlight_border, True, points, points2)

            # Highlight with light green color movement grid
            if battle.realm_in_control == game_stats.player_power:
                if battle.movement_grid is not None and battle.ready_to_act:
                    if [int(TileObj.posxy[0]), int(TileObj.posxy[1])] in battle.movement_grid:
                        draw_rect_alpha(screen, GreenGrid, ((x - 1) * 96, (y - 1) * 96, 96, 96))

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
                                    ((x - 1) * 96, (y - 1) * 96, 96, 96))

            # Siege tower docked to the wall
            if TileObj.siege_tower_deployed:
                machine_img = game_stats.gf_regiment_dict['img/Creatures/siege_machines/siege_tower_r']
                screen.blit(machine_img,
                            ((x - 1) * 96 + 66,
                             (y - 1) * 96 + 5))

            # Siege machines
            for equipment in TileObj.siege_machines:
                side = "_l"
                if equipment[2]:
                    side = "_r"
                machine_position = [(x - 1) * 96 + equipment[1][0], (y - 1) * 96 + equipment[1][1]]
                machine_img = game_stats.gf_regiment_dict[
                    siege_warfare_catalog.siege_machine_img[equipment[0]] + side]
                screen.blit(machine_img,
                            (machine_position[0],
                             machine_position[1]))
            # Units
            # print("# Units")
            if TileObj.army_id:
                # print(str(TileObj.posxy))
                focus = TileObj.army_id
                army = common_selects.select_army_by_id(focus)
                # Player should see only his army at formation stage
                if (army.owner == game_stats.player_power and battle.stage == "Formation") or \
                        battle.stage != "Formation":

                    unit = army.units[TileObj.unit_index]

                    # Draw direction lines
                    draw_direction_lines(screen, battle, unit.direction, x, y, unit.position)

                    # Draw creatures
                    draw_creatures_funs.draw_creatures(screen, unit, x, y, army.owner, TileObj.unit_index, battle,
                                                       TileObj.posxy)

            if TileObj.passing_army_id:
                focus = TileObj.passing_army_id
                army = common_selects.select_army_by_id(focus)
                # Player should see only his army at formation stage
                if (army.owner == game_stats.player_power and battle.stage == "Formation") or \
                        battle.stage != "Formation":
                    unit = army.units[TileObj.passing_unit_index]

                    # Draw direction lines
                    draw_direction_lines(screen, battle, unit.direction, x, y, unit.position)

                    # Draw creatures
                    draw_creatures_funs.draw_creatures(screen, unit, x, y, army.owner, TileObj.passing_unit_index,
                                                       battle, TileObj.posxy)


def draw_direction_lines(screen, b, direction, x, y, check_position):
    # Animation coordinates
    x2 = 0
    y2 = 0
    if b.tile_trail is not None and check_position == b.queue[0].position:
        # if len(b.tile_trail) > 0:
        # print("b.tile_trail[0] - " + str(b.tile_trail[0]))
        # print("b.battle_pov - " + str(b.battle_pov))
        spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
        new_x = int(b.tile_trail[0][0]) - int(b.battle_pov[0])
        new_y = int(b.tile_trail[0][1]) - int(b.battle_pov[1])
        x2 = (new_x - int(x)) * spread
        y2 = (new_y - int(y)) * spread
    if direction == "E":
        # print("x " + str(x) + " y " + str(y))
        points = [(96, 3), (98, 48), (98, 49), (96, 94)]
        points2 = [(x - 1 + x2) * 96, (y - 1 + y2) * 96]  # [(x - 1) * 96, (y - 1) * 96]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "W":
        # print("x " + str(x) + " y " + str(y))
        points = [(2, 3), (0, 48), (0, 49), (2, 94)]
        points2 = [(x - 1 + x2) * 96 - 2, (y - 1 + y2) * 96]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "N":
        # print("x " + str(x) + " y " + str(y))
        points = [(3, 2), (48, 0), (49, 0), (94, 2)]
        points2 = [(x - 1 + x2) * 96, (y - 1 + y2) * 96 - 2]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "S":
        # print("x " + str(x) + " y " + str(y))
        points = [(3, 96), (48, 98), (49, 98), (94, 96)]
        points2 = [(x - 1 + x2) * 96, (y - 1 + y2) * 96]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "NE":
        # print("x " + str(x) + " y " + str(y))
        points = [(50, 2), (98, 0), (96, 48)]
        points2 = [(x - 1 + x2) * 96, (y - 1 + y2) * 96 - 2]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "SE":
        # print("x " + str(x) + " y " + str(y))
        points = [(96, 50), (98, 98), (50, 96)]
        points2 = [(x - 1 + x2) * 96, (y - 1 + y2) * 96]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "SW":
        # print("x " + str(x) + " y " + str(y))
        points = [(2, 50), (0, 98), (48, 96)]
        points2 = [(x - 1 + x2) * 96 - 2, (y - 1 + y2) * 96]
        draw_lines_alpha(screen, LightYellow, False, points, points2)

    elif direction == "NW":
        # print("x " + str(x) + " y " + str(y))
        points = [(2, 48), (0, 0), (48, 2)]
        points2 = [(x - 1 + x2) * 96 - 2, (y - 1 + y2) * 96 - 2]
        draw_lines_alpha(screen, LightYellow, False, points, points2)


def draw_siege_machine(screen, unit, index, row, line, side, x , y, unit_index, current_position, b, owner):
    if unit.siege_engine:
        img_width = siege_warfare_catalog.siege_machine_img_width[unit.siege_engine]
        img_height = siege_warfare_catalog.siege_machine_img_height[unit.siege_engine]

        draw = False
        if unit.direction == "E":
            if row == 1:
                if len(unit.crew) <= math.floor(unit.number / 2):
                    if index + 1 == len(unit.crew):
                        draw = True
                else:
                    if index + 1 == math.floor(unit.number / 2):
                        draw = True
                        # print(str(index))

                if draw:
                    machine_position = [(x - 1) * 96 + 90 - img_width,
                                        (y - 1) * 96 + 60 - img_height]

                    xy_animation = [0, 0]

                    if b.primary == "Rotate":
                        xy_animation = anim_battle_unit_action.machine_rotate(b, unit_index, owner, current_position,
                                                                              machine_position, img_width, img_height)
                    elif b.primary == "Move":
                        xy_animation = anim_battle_unit_action.machine_march(b, unit_index, current_position,
                                                                             machine_position, owner, img_width,
                                                                             img_height)

                    machine_img = game_stats.gf_regiment_dict[siege_warfare_catalog.siege_machine_img[unit.siege_engine]
                                                              + side]
                    screen.blit(machine_img,
                                (machine_position[0] + xy_animation[0],
                                 machine_position[1] + xy_animation[1]))

        elif unit.direction == "W":
            if row == 1:
                if len(unit.crew) <= math.floor(unit.number / 2):
                    if index + 1 == len(unit.crew):
                        draw = True
                else:
                    if index + 1 == math.floor(unit.number / 2):
                        draw = True
                        # print(str(index))

                if draw:
                    machine_position = [(x - 1) * 96 + 7,
                                        (y - 1) * 96 + 60 - img_height]

                    xy_animation = [0, 0]

                    if b.primary == "Rotate":
                        xy_animation = anim_battle_unit_action.machine_rotate(b, unit_index, owner, current_position,
                                                                              machine_position, img_width, img_height)
                    elif b.primary == "Move":
                        xy_animation = anim_battle_unit_action.machine_march(b, unit_index, current_position,
                                                                             machine_position, owner, img_width,
                                                                             img_height)

                    machine_img = game_stats.gf_regiment_dict[siege_warfare_catalog.siege_machine_img[unit.siege_engine]
                                                              + side]
                    screen.blit(machine_img,
                                (machine_position[0] + xy_animation[0],
                                 machine_position[1] + xy_animation[1]))

        elif unit.direction == "N":
            if row == 1:
                if len(unit.crew) <= unit.number:
                    if index + 1 == len(unit.crew):
                        draw = True
                else:
                    if index + 1 == unit.number:
                        draw = True
                        # print(str(index))

                if draw:
                    machine_position = [(x - 1) * 96 + 49 - (img_width / 2),
                                        (y - 1) * 96 + 35 - img_height]

                    xy_animation = [0, 0]

                    if b.primary == "Rotate":
                        xy_animation = anim_battle_unit_action.machine_rotate(b, unit_index, owner, current_position,
                                                                              machine_position, img_width, img_height)
                    elif b.primary == "Move":
                        xy_animation = anim_battle_unit_action.machine_march(b, unit_index, current_position,
                                                                             machine_position, owner, img_width,
                                                                             img_height)

                    machine_img = game_stats.gf_regiment_dict[siege_warfare_catalog.siege_machine_img[unit.siege_engine]
                                                              + side]
                    screen.blit(machine_img,
                                (machine_position[0] + xy_animation[0],
                                 machine_position[1] + xy_animation[1]))

        elif unit.direction == "S":
            if row == 1:
                if len(unit.crew) <= unit.number:
                    if index + 1 == len(unit.crew):
                        draw = True
                else:
                    if index + 1 == unit.number:
                        draw = True
                        # print(str(index))

                if draw:
                    machine_position = [(x - 1) * 96 + 49 - (img_width / 2),
                                        (y - 1) * 96 + 81 - img_height]

                    xy_animation = [0, 0]

                    if b.primary == "Rotate":
                        xy_animation = anim_battle_unit_action.machine_rotate(b, unit_index, owner, current_position,
                                                                              machine_position, img_width, img_height)
                    elif b.primary == "Move":
                        xy_animation = anim_battle_unit_action.machine_march(b, unit_index, current_position,
                                                                             machine_position, owner, img_width,
                                                                             img_height)

                    machine_img = game_stats.gf_regiment_dict[siege_warfare_catalog.siege_machine_img[unit.siege_engine]
                                                              + side]
                    screen.blit(machine_img,
                                (machine_position[0] + xy_animation[0],
                                 machine_position[1] + xy_animation[1]))

        elif unit.direction == "NE":
            if row == 1:
                if len(unit.crew) <= math.floor(unit.number / 2):
                    if index + 1 == len(unit.crew):
                        draw = True
                else:
                    if index + 1 == math.floor(unit.number / 2):
                        draw = True
                        # print(str(index))

                if draw:
                    machine_position = [(x - 1) * 96 + 65 - (img_width / 2),
                                        (y - 1) * 96 + 28 - img_height]

                    xy_animation = [0, 0]

                    if b.primary == "Rotate":
                        xy_animation = anim_battle_unit_action.machine_rotate(b, unit_index, owner, current_position,
                                                                              machine_position, img_width, img_height)
                    elif b.primary == "Move":
                        xy_animation = anim_battle_unit_action.machine_march(b, unit_index, current_position,
                                                                             machine_position, owner, img_width,
                                                                             img_height)

                    machine_img = game_stats.gf_regiment_dict[siege_warfare_catalog.siege_machine_img[unit.siege_engine]
                                                              + side]
                    screen.blit(machine_img,
                                (machine_position[0] + xy_animation[0],
                                 machine_position[1] + xy_animation[1]))

        elif unit.direction == "NW":
            if row == 1:
                if len(unit.crew) <= math.floor(unit.number / 2):
                    if index + 1 == len(unit.crew):
                        draw = True
                else:
                    if index + 1 == math.floor(unit.number / 2):
                        draw = True
                        # print(str(index))

                if draw:
                    machine_position = [(x - 1) * 96 + 32 - (img_width / 2),
                                        (y - 1) * 96 + 28 - img_height]

                    xy_animation = [0, 0]

                    if b.primary == "Rotate":
                        xy_animation = anim_battle_unit_action.machine_rotate(b, unit_index, owner, current_position,
                                                                              machine_position, img_width, img_height)
                    elif b.primary == "Move":
                        xy_animation = anim_battle_unit_action.machine_march(b, unit_index, current_position,
                                                                             machine_position, owner, img_width,
                                                                             img_height)

                    machine_img = game_stats.gf_regiment_dict[siege_warfare_catalog.siege_machine_img[unit.siege_engine]
                                                              + side]
                    screen.blit(machine_img,
                                (machine_position[0] + xy_animation[0],
                                 machine_position[1] + xy_animation[1]))

        elif unit.direction == "SE":
            if row == 1:
                if len(unit.crew) <= math.ceil(unit.number / 2):
                    if index + 1 == len(unit.crew):
                        draw = True
                else:
                    if index + 1 == math.ceil(unit.number / 2):
                        draw = True
                        # print(str(index))

                if draw:
                    machine_position = [(x - 1) * 96 + 65 - (img_width / 2),
                                        (y - 1) * 96 + 75 - img_height]

                    xy_animation = [0, 0]

                    if b.primary == "Rotate":
                        xy_animation = anim_battle_unit_action.machine_rotate(b, unit_index, owner, current_position,
                                                                              machine_position, img_width, img_height)
                    elif b.primary == "Move":
                        xy_animation = anim_battle_unit_action.machine_march(b, unit_index, current_position,
                                                                             machine_position, owner, img_width,
                                                                             img_height)

                    machine_img = game_stats.gf_regiment_dict[siege_warfare_catalog.siege_machine_img[unit.siege_engine]
                                                              + side]
                    screen.blit(machine_img,
                                (machine_position[0] + xy_animation[0],
                                 machine_position[1] + xy_animation[1]))

        elif unit.direction == "SW":
            if row == 1:
                if len(unit.crew) <= math.ceil(unit.number / 2):
                    if index + 1 == len(unit.crew):
                        draw = True
                else:
                    if index + 1 == math.ceil(unit.number / 2):
                        draw = True
                        # print(str(index))

                if draw:
                    machine_position = [(x - 1) * 96 + 32 - (img_width / 2),
                                        (y - 1) * 96 + 75 - img_height]

                    xy_animation = [0, 0]

                    if b.primary == "Rotate":
                        xy_animation = anim_battle_unit_action.machine_rotate(b, unit_index, owner, current_position,
                                                                              machine_position, img_width, img_height)
                    elif b.primary == "Move":
                        xy_animation = anim_battle_unit_action.machine_march(b, unit_index, current_position,
                                                                             machine_position, owner, img_width,
                                                                             img_height)

                    machine_img = game_stats.gf_regiment_dict[siege_warfare_catalog.siege_machine_img[unit.siege_engine]
                                                              + side]
                    screen.blit(machine_img,
                                (machine_position[0] + xy_animation[0],
                                 machine_position[1] + xy_animation[1]))


def battle_end_window(screen, b):
    pygame.draw.polygon(screen, Board1, [[130, 100], [1150, 100], [1150, 400], [130, 400]])

    # Result
    text_panel1 = tnr_font20.render(b.battle_end_message, True, TitleText)
    screen.blit(text_panel1, [620 - len(b.battle_end_message), 103])

    # Attacker
    text_panel1 = tnr_font20.render(b.attacker_realm, True, TitleText)
    screen.blit(text_panel1, [430 - len(b.attacker_realm), 133])

    # Defender
    text_panel1 = tnr_font20.render(b.defender_realm, True, TitleText)
    screen.blit(text_panel1, [850 - len(b.defender_realm), 133])

    # Earned experience
    if game_stats.player_power != b.defeated_side:
        text_panel1 = tnr_font20.render("Experience +" + str(b.earned_experience), True, TitleText)
        screen.blit(text_panel1, [580, 163])

    # Display units
    attacker = None
    defender = None
    for army in game_obj.game_armies:
        if army.army_id == game_stats.attacker_army_id:  # Attacker
            attacker = army
        elif army.army_id == game_stats.defender_army_id:  # Defender
            defender = army

    # Attacker units
    if len(attacker.units) > 0:
        number = 0
        for unit in attacker.units:
            x_pos = 145 + math.floor(number % 10) * 50
            y_pos = 198 + math.floor(number / 10) * 80
            # print(str(x_pos))

            if len(unit.crew) > 0:
                img_width = unit.crew[0].img_width
                img_height = unit.crew[0].img_height
            else:
                img_width = unit.cemetery[0].img_width
                img_height = unit.cemetery[0].img_height

            if img_width > 44 or img_height > 44:
                army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                if img_width > 44:
                    proportion = 44 / img_width
                    army_img = pygame.transform.scale(army_img,
                                                      (44,
                                                       int(img_height * proportion)))
                    x_offset = 3
                    y_offset = (48 - (img_height * proportion)) / 2
                else:
                    proportion = 44 / img_height
                    army_img = pygame.transform.scale(army_img,
                                                      (int(img_width * proportion),
                                                       44))
                    x_offset = (48 - (img_width * proportion)) / 2
                    y_offset = 3
            else:
                army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                x_offset = unit.x_offset
                y_offset = unit.y_offset

            screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])

            amount_text = str(len(unit.crew)) + "/" + str(unit.number * unit.rows)
            text_panel1 = arial_font14.render(amount_text, True, TitleText)
            screen.blit(text_panel1, [x_pos + 5, y_pos + 50])

            if unit.deserted:
                # print("Attention")
                text_panel1 = arial_font14.render("Routed", True, TitleText)
                screen.blit(text_panel1, [x_pos + 5, y_pos + 70])

            number += 1

    # Defender units
    if len(defender.units) > 0:
        number = 0
        for unit in defender.units:
            x_pos = 145 + math.floor(number % 10) * 50 + 510
            y_pos = 198 + math.floor(number / 10) * 80
            # print(str(x_pos))

            if len(unit.crew) > 0:
                img_width = unit.crew[0].img_width
                img_height = unit.crew[0].img_height
            else:
                img_width = unit.cemetery[0].img_width
                img_height = unit.cemetery[0].img_height

            if img_width > 44 or img_height > 44:
                army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                if img_width > 44:
                    proportion = 44 / img_width
                    army_img = pygame.transform.scale(army_img,
                                                      (44,
                                                       int(img_height * proportion)))
                    x_offset = 3
                    y_offset = (48 - (img_height * proportion)) / 2
                else:
                    proportion = 44 / img_height
                    army_img = pygame.transform.scale(army_img,
                                                      (int(img_width * proportion),
                                                       44))
                    x_offset = (48 - (img_width * proportion)) / 2
                    y_offset = 3
            else:
                army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                x_offset = unit.x_offset
                y_offset = unit.y_offset

            screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])

            amount_text = str(len(unit.crew)) + "/" + str(unit.number * unit.rows)
            text_panel1 = arial_font14.render(amount_text, True, TitleText)
            screen.blit(text_panel1, [x_pos + 5, y_pos + 50])

            if unit.deserted:
                # print("Attention")
                text_panel1 = arial_font14.render("Routed", True, TitleText)
                screen.blit(text_panel1, [x_pos + 5, y_pos + 70])

            number += 1

    # Button - End
    # pygame.draw.polygon(screen, FillButton, [[590, 138], [690, 138], [690, 160], [590, 160]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[590, 135], [690, 135], [690, 157], [590, 157]], 3)
    text_panel5 = tnr_font20.render("End", True, TitleText)
    screen.blit(text_panel5, [625, 135])


def siege_equipment_menu_window(screen, b):
    pygame.draw.polygon(screen, MainMenuColor, [[441, 201], [840, 201], [840, 500], [441, 500]])

    # Close window button
    pygame.draw.polygon(screen, CancelFieldColor, [[816, 206], [835, 206], [835, 225], [816, 225]])
    pygame.draw.polygon(screen, CancelElementsColor, [[816, 206], [835, 206], [835, 225], [816, 225]], 2)
    pygame.draw.line(screen, CancelElementsColor, [819, 209], [832, 222], 2)
    pygame.draw.line(screen, CancelElementsColor, [819, 222], [832, 209], 2)

    y_base = 204
    y_shift = 60
    y_num = 0
    for equipment in b.available_equipment:
        img_width = siege_warfare_catalog.siege_machine_img_width[equipment[0]]
        img_height = siege_warfare_catalog.siege_machine_img_height[equipment[0]]
        side = "_l"
        if equipment[2]:
            side = "_r"
        machine_img = game_stats.gf_regiment_dict[siege_warfare_catalog.siege_machine_img[equipment[0]] + side]
        screen.blit(machine_img, [480 - img_width/2, y_base + y_shift * y_num + 30 - img_height/2])

        text_label = tnr_font20.render(equipment[0], True, TitleText)
        screen.blit(text_label, [520, y_base + y_shift * y_num + 17])

        pygame.draw.polygon(screen, LineMainMenuColor1, [[756, y_base + y_shift * y_num + 1],
                                                         [813, y_base + y_shift * y_num + 1],
                                                         [813, y_base + y_shift * y_num + 57],
                                                         [756, y_base + y_shift * y_num + 57]], 1)

        icon_img = game_stats.gf_misc_img_dict["Icons/pick_up_siege_machine"]
        screen.blit(icon_img, (760, y_base + y_shift * y_num + 3))

        y_num += 1


def battle_screen(screen):
    yVar = game_stats.game_window_height - 800

    screen.fill(MapLimitColor)  # background

    draw_tiles(screen)  # Draw tiles

    b = game_stats.present_battle

    for obj in graphics_obj.battle_objects:
        obj.draw_panel(screen)
        for button in obj.buttons:
            button.draw_button(screen)
        # print(obj.name)

    if b.stage == "Formation":
        # print(str(b.stage))
        # Start battle button
        pygame.draw.polygon(screen, FillButton, [[580, 10], [700, 10], [700, 32], [580, 32]])
        pygame.draw.polygon(screen, BorderNewGameColor, [[580, 10], [700, 10], [700, 32], [580, 32]], 3)

        text_NewGame1 = tnr_font20.render("Start battle", True, TitleText)
        screen.blit(text_NewGame1, [595, 10])

        # Draw reserve of siege machines
        if b.battle_type == "Siege":
            border_color = LineMainMenuColor1
            if b.preparation_siege_machine == "Siege tower":
                border_color = HighlightOption
            pygame.draw.polygon(screen, RockTunel, [[1, 677 + yVar], [90, 677 + yVar],
                                                    [90, 736 + yVar], [1, 736 + yVar]])
            pygame.draw.polygon(screen, border_color, [[1, 677 + yVar], [90, 677 + yVar],
                                                       [90, 736 + yVar], [1, 736 + yVar]], 2)

            machine_img = game_stats.gf_regiment_dict["img/Creatures/siege_machines/siege_tower_r"]
            screen.blit(machine_img, [26, 679 + yVar])

            x_pos = 76
            if b.available_siege_towers >= 10:
                x_pos = 69
            text_NewGame1 = tnr_font20.render(str(b.available_siege_towers), True, TitleText)
            screen.blit(text_NewGame1, [x_pos, 699 + yVar])

            border_color = LineMainMenuColor1
            if b.preparation_siege_machine == "Battering ram":
                border_color = HighlightOption
            pygame.draw.polygon(screen, RockTunel, [[1, 739 + yVar], [90, 739 + yVar],
                                                    [90, 798 + yVar], [1, 798 + yVar]])
            pygame.draw.polygon(screen, border_color, [[1, 739 + yVar], [90, 739 + yVar],
                                                       [90, 798 + yVar], [1, 798 + yVar]], 2)

            machine_img = game_stats.gf_regiment_dict["img/Creatures/siege_machines/battering_ram_r"]
            screen.blit(machine_img, [4, 764 + yVar])

            x_pos = 76
            if b.available_battering_rams >= 10:
                x_pos = 69
            text_NewGame1 = tnr_font20.render(str(b.available_battering_rams), True, TitleText)
            screen.blit(text_NewGame1, [x_pos, 761 + yVar])

    elif b.stage == "Fighting":
        unit = None

        # Pick up or drop siege machine button
        if b.battle_type == "Siege":
            if b.realm_in_control == game_stats.player_power:
                if b.queue[0].obj_type == "Regiment" and b.ready_to_act:
                    army = common_selects.select_army_by_id(b.queue[0].army_id)
                    unit = army.units[b.queue[0].number]
                    # print("Regiment - " + unit.name)
                    draw_button = False
                    drop_sm = False
                    if unit.siege_engine:
                        draw_button = True
                        drop_sm = True
                    else:
                        TileNum = (b.queue[0].position[1] - 1) * game_stats.battle_width\
                                  + b.queue[0].position[0] - 1
                        if len(b.battle_map[TileNum].siege_machines) > 0:
                            draw_button = True
                            drop_sm = False

                    if draw_button:
                        pygame.draw.polygon(screen, FieldColor, [[74, 740 + yVar], [231, 740 + yVar],
                                                                 [231, 795 + yVar], [74, 795 + yVar]])
                        pygame.draw.polygon(screen, LineMainMenuColor1, [[74, 740 + yVar], [231, 740 + yVar],
                                                                         [231, 795 + yVar], [74, 795 + yVar]],
                                            3)

                        text_NewGame1 = tnr_font20.render("Equipment", True, TitleText)
                        screen.blit(text_NewGame1, [134, 755 + yVar])

                        icon = "Icons/pick_up_siege_machine"
                        if drop_sm:
                            icon = "Icons/drop_siege_machine"
                        icon_img = game_stats.gf_misc_img_dict[icon]
                        screen.blit(icon_img, (77, 742 + yVar))

        # Attack method button
        # Changes between attack methods if possible
        pygame.mouse.set_visible(True)
        if b.realm_in_control == game_stats.player_power:
            if b.queue[0].obj_type == "Regiment" and b.ready_to_act:
                change_cursor(screen, b, unit)

        if b.anim_message:
            anim_battle_message.manage_messages(screen, b)
            # anim_battle_effects.message_float(screen, b)

    # Draw additional window
    if b.battle_window:
        additional_windows[b.battle_window](screen, b)

    if game_stats.fps_status:
        text_panel = tnr_font20.render(str(game_stats.fps), True, TitleText)
        screen.blit(text_panel, [10, 4])


def change_cursor(screen, b, unit):
    # if not pygame.mouse.get_visible():

    x = math.ceil((game_stats.mouse_position[0] + 1) / 96)
    y = math.ceil((game_stats.mouse_position[1] + 1) / 96)
    x = int(x) + int(b.battle_pov[0])
    y = int(y) + int(b.battle_pov[1])

    TileNum = (y - 1) * game_stats.battle_width + x - 1

    if b.attacker_realm == b.realm_in_control:
        enemy = b.defender_id
    else:
        enemy = b.attacker_id

    if 0 < x <= game_stats.battle_width and 0 < y <= game_stats.battle_height:
        siege_action_icon = ""
        if unit is not None:
            print("Regiment - " + unit.name)
            if unit.siege_engine is not None:
                if unit.siege_engine == "Battering ram":
                    # print("Regiment is carrying battering ram")
                    if b.battle_map[TileNum].map_object is not None:
                        if b.battle_map[TileNum].map_object.obj_name in ["Palisade_gates"]:
                            siege_action_icon = "Battering ram"
                elif unit.siege_engine == "Siege tower":
                    if b.battle_map[TileNum].map_object is not None:
                        if b.battle_map[TileNum].map_object.obj_name in ["Palisade_bottom", "Palisade"]:
                            siege_action_icon = "Siege tower"

        if siege_action_icon == "Battering ram":
            pygame.mouse.set_visible(False)
            break_gates_img = game_stats.gf_misc_img_dict["Icons/break_gates"]
            offset = (list(game_stats.mouse_position)[0] - 45, list(game_stats.mouse_position)[1] - 12)
            screen.blit(break_gates_img, offset)

        elif siege_action_icon == "Siege tower":
            pygame.mouse.set_visible(False)
            break_gates_img = game_stats.gf_misc_img_dict["Icons/wall_contact"]
            offset = (list(game_stats.mouse_position)[0] - 46, list(game_stats.mouse_position)[1] - 23)
            screen.blit(break_gates_img, offset)

        elif b.battle_map[TileNum].army_id == enemy:
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
                    ranged_attack_img = game_stats.gf_misc_img_dict["Icons/broken_ranged_attack"]
                    screen.blit(ranged_attack_img, game_stats.mouse_position)
                else:
                    # print("3. distance " + str(distance) + " <= b.cur_effective_range " + str(b.cur_effective_range))
                    pygame.mouse.set_visible(False)
                    ranged_attack_img = game_stats.gf_misc_img_dict["Icons/ranged_attack"]
                    screen.blit(ranged_attack_img, game_stats.mouse_position)

            elif b.attack_type_in_use == "Melee":
                x2 = game_stats.mouse_position[0] % 96
                y2 = game_stats.mouse_position[1] % 96
                # print("x, y - " + str([x2, y2]))
                if b.attack_name == "Hit and fly":
                    pygame.mouse.set_visible(False)
                    melee_attack_img = game_stats.gf_misc_img_dict["Icons/Hit and fly"]
                    screen.blit(melee_attack_img, (list(game_stats.mouse_position)[0] - 45,
                                                   list(game_stats.mouse_position)[1]))
                else:
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
                        melee_attack_img = game_stats.gf_misc_img_dict["Icons/" + word]
                        screen.blit(melee_attack_img, offset)
        else:
            pygame.mouse.set_visible(True)


school_imgs = {"Overall" : "everything",
               "Tactics" : "tactics",
               "Divine" : "divine",
               "Elemental" : "elemental"}

additional_windows = {"Regiment info" : battle_regiment_information.regiment_info_window,
                      "Battle end window" : battle_end_window,
                      "Abilities menu" : abilities_menu.abilities_menu_window,
                      "Siege equipment menu" : siege_equipment_menu_window}
