## Among Myth and Wonder
## draw_creatures_funs

import math

from Screens.colors_catalog import *

from Screens import sc_battle

from Screens.Sc_Battle import anim_battle_unit_action
from Screens.Sc_Battle import anim_battle_effects

from Screens.Interface_Elements import flags

from Resources import game_stats
from Resources import common_selects

from Content import ability_catalog


def draw_creatures(screen, unit, x, y, owner, unit_index, b, current_position):
    side = "_l"
    if unit.right_side:
        side = "_r"

    div_row = unit.rows - 1
    if div_row == 0:
        div_row = 1

    div_number = unit.number - 1
    if div_number == 0:
        div_number = 1

    x_appendix = 0
    y_appendix = 0

    direction_dict[unit.direction](screen, unit, x, y, owner, unit_index, b, current_position, side, div_row,
                                   div_number, x_appendix, y_appendix)

    # Draw flag
    if owner != "Neutral":
        power = common_selects.select_realm_by_name(owner)
        xy_animation = [0, 0]  # Temporary, delete this if animation would be implemented

        if b.tile_trail is not None and unit.position == b.queue[0].position:
            # print("x - " + str(x) + ", y - " + str(y))
            spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
            new_x = int(b.tile_trail[0][0]) - int(b.battle_pov[0])
            new_y = int(b.tile_trail[0][1]) - int(b.battle_pov[1])
            xy_animation[0] = (new_x - int(x)) * spread * 96
            xy_animation[1] = (new_y - int(y)) * spread * 96
            # print("b.tile_trail - " + str(b.tile_trail))
            # print("xy_animation - " + str(xy_animation))

        xb = (x - 1) * 96
        yb = (y - 1) * 96
        flags.battlefield_flag(screen, xb, yb, xy_animation[0], xy_animation[1], FlagpoleColor,
                               FlagColors[power.f_color], FlagColors[power.s_color])

    # Blink red color over unit during fight
    if b.primary in ["Melee attack", "Counterattack", "Ranged attack"]:
        anim_battle_effects.damage_dealt_red(screen, b, current_position)

    # Blink white during buffing cast
    elif b.primary == "Pass" or b.primary == "Pass1":
        # print("Pass")
        if ability_catalog.ability_cat[b.selected_ability].anim_effect == "buff":
            # print("buff")
            # print("current_position - " + str(current_position))
            # print("b.selected_tile - " + str(b.selected_tile))
            if list(current_position) == b.selected_tile:
                # print("current_position - " + str(current_position))
                anim_battle_effects.white_buff_effect(screen, b, current_position)

        elif ability_catalog.ability_cat[b.selected_ability].anim_effect == "damage spell":
            if list(current_position) == b.selected_tile:
                anim_battle_effects.spell_effect(screen, b, current_position)


def facing_east(screen, unit, x, y, owner, unit_index, b, current_position, side, div_row, div_number,
                x_appendix, y_appendix):
    total = len(unit.crew)
    index = 0
    while index <= total - 1:
        row = math.ceil((index + 1) / unit.number)
        if (index + 1) % unit.number == 0:
            line = unit.number
        else:
            line = (index + 1) % unit.number

        if unit.number == 1:
            y_appendix = 48 - unit.crew[index].img_height / 2
        else:
            x_appendix = (row - 1) * ((90 - unit.crew[index].img_width) / div_row)
            y_appendix = (unit.number - line) * ((90 - unit.crew[index].img_height) / div_number)

        creature_position = [(x - 1) * 96 + 4 + 90 - unit.crew[index].img_width - x_appendix,
                             (y - 1) * 96 + 4 + 90 - unit.crew[index].img_height - y_appendix]

        xy_animation = animate(unit, owner, index, unit_index, b, current_position, creature_position, row, line)
        draw_single_creature(screen, creature_position, xy_animation, unit, index, side)

        sc_battle.draw_siege_machine(screen, unit, index, row, line, side, x, y, unit_index, current_position, b, owner)
        index += 1


def facing_west(screen, unit, x, y, owner, unit_index, b, current_position, side, div_row, div_number,
                x_appendix, y_appendix):
    total = len(unit.crew)
    index = 0
    while index <= total - 1:
        row = math.ceil((index + 1) / unit.number)
        if (index + 1) % unit.number == 0:
            line = unit.number
        else:
            line = (index + 1) % unit.number

        if unit.number == 1:
            y_appendix = 48 - unit.crew[index].img_height / 2
        else:
            x_appendix = (row - 1) * ((90 - unit.crew[index].img_width) / div_row)
            y_appendix = (unit.number - line) * ((90 - unit.crew[index].img_height) / div_number)

        creature_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                             x_appendix,
                             (y - 1) * 96 + 4 + 90 - unit.crew[index].img_height -
                             y_appendix]

        xy_animation = animate(unit, owner, index, unit_index, b, current_position, creature_position, row, line)
        draw_single_creature(screen, creature_position, xy_animation, unit, index, side)

        sc_battle.draw_siege_machine(screen, unit, index, row, line, side, x, y, unit_index, current_position, b, owner)
        index += 1


def facing_north(screen, unit, x, y, owner, unit_index, b, current_position, side, div_row, div_number,
                 x_appendix, y_appendix):
    total = len(unit.crew)
    index = 0
    while index <= total - 1:
        row = math.ceil((index + 1) / unit.number)
        if (index + 1) % unit.number == 0:
            line = unit.number
        else:
            line = (index + 1) % unit.number

        if unit.number == 1:
            x_appendix = 48 - unit.crew[index].img_width / 2
        else:
            x_appendix = (unit.number - line) * ((90 - unit.crew[index].img_width) / div_number)
            y_appendix = (row - 1) * ((90 - unit.crew[index].img_height) / div_row)

        creature_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                             x_appendix,
                             (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                             y_appendix]

        xy_animation = animate(unit, owner, index, unit_index, b, current_position, creature_position, row, line)
        draw_single_creature(screen, creature_position, xy_animation, unit, index, side)

        sc_battle.draw_siege_machine(screen, unit, index, row, line, side, x, y, unit_index, current_position, b, owner)
        index += 1


def facing_south(screen, unit, x, y, owner, unit_index, b, current_position, side, div_row, div_number,
                 x_appendix, y_appendix):
    index = int(len(unit.crew) - 1)
    while index >= 0:
        row = math.ceil((index + 1) / unit.number)
        if (index + 1) % unit.number == 0:
            line = unit.number
        else:
            line = (index + 1) % unit.number

        if unit.number == 1:
            x_appendix = 48 - unit.crew[index].img_width / 2
        else:
            x_appendix = (unit.number - line) * ((90 - unit.crew[index].img_width) / div_number)
            y_appendix = (row - 1) * ((90 - unit.crew[index].img_height) / div_row)

        creature_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                             x_appendix,
                             (y - 1) * 96 + 4 + 90 - unit.crew[index].img_height -
                             y_appendix]

        xy_animation = animate(unit, owner, index, unit_index, b, current_position, creature_position, row, line)
        draw_single_creature(screen, creature_position, xy_animation, unit, index, side)

        sc_battle.draw_siege_machine(screen, unit, index, row, line, side, x, y, unit_index, current_position, b, owner)
        index -= 1


def facing_north_east(screen, unit, x, y, owner, unit_index, b, current_position, side, div_row, div_number,
                      x_appendix, y_appendix):
    total = len(unit.crew)
    index = 0
    while index <= total - 1:
        row = math.ceil((index + 1) / unit.number)
        if (index + 1) % unit.number == 0:
            line = unit.number
        else:
            line = (index + 1) % unit.number

        if unit.number == 1:
            x_appendix = - (unit.crew[index].img_width / 2)
            y_appendix = unit.crew[index].img_height / 2
        else:
            x_appendix = (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number)
            y_appendix = (unit.number - line) * (48 / div_number) - (row - 1) * (40 / div_row)

        creature_position = [(x - 1) * 96 + 48 - (unit.crew[index].img_width / 2) - x_appendix,
                             (y - 1) * 96 + 48 - (unit.crew[index].img_height / 2) - y_appendix]

        xy_animation = animate(unit, owner, index, unit_index, b, current_position, creature_position, row, line)
        draw_single_creature(screen, creature_position, xy_animation, unit, index, side)

        sc_battle.draw_siege_machine(screen, unit, index, row, line, side, x, y, unit_index, current_position, b, owner)
        index += 1


def facing_north_west(screen, unit, x, y, owner, unit_index, b, current_position, side, div_row, div_number,
                      x_appendix, y_appendix):
    total = len(unit.crew)
    index = 0
    while index <= total - 1:
        row = math.ceil((index + 1) / unit.number)
        if (index + 1) % unit.number == 0:
            line = unit.number
        else:
            line = (index + 1) % unit.number

        if unit.number == 1:
            x_appendix = - (unit.crew[index].img_width / 2)
            y_appendix = unit.crew[index].img_height / 2
        else:
            x_appendix = (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number)
            y_appendix = (unit.number - line) * (48 / div_number) - (row - 1) * (40 / div_row)

        creature_position = [(x - 1) * 96 + 48 - (unit.crew[index].img_width / 2) + x_appendix,
                             (y - 1) * 96 + 48 - (unit.crew[index].img_height / 2) - y_appendix]

        xy_animation = animate(unit, owner, index, unit_index, b, current_position, creature_position, row, line)
        draw_single_creature(screen, creature_position, xy_animation, unit, index, side)

        sc_battle.draw_siege_machine(screen, unit, index, row, line, side, x, y, unit_index, current_position, b, owner)
        index += 1


def facing_south_east(screen, unit, x, y, owner, unit_index, b, current_position, side, div_row, div_number,
                      x_appendix, y_appendix):
    index = int(len(unit.crew) - 1)
    while index >= 0:
        row = math.ceil((index + 1) / unit.number)
        if (index + 1) % unit.number == 0:
            line = unit.number
        else:
            line = (index + 1) % unit.number

        if unit.number == 1:
            x_appendix = - (unit.crew[index].img_width / 2)
            y_appendix = unit.crew[index].img_height / 2
        else:
            x_appendix = (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number)
            y_appendix = (unit.number - line) * (48 / div_number) - (row - 1) * (40 / div_row)

        creature_position = [(x - 1) * 96 + 48 - (unit.crew[index].img_width / 2) - x_appendix,
                             (y - 1) * 96 + 48 - (unit.crew[index].img_height / 2) + y_appendix]

        xy_animation = animate(unit, owner, index, unit_index, b, current_position, creature_position, row, line)
        draw_single_creature(screen, creature_position, xy_animation, unit, index, side)

        sc_battle.draw_siege_machine(screen, unit, index, row, line, side, x, y, unit_index, current_position, b, owner)
        index -= 1


def facing_south_west(screen, unit, x, y, owner, unit_index, b, current_position, side, div_row, div_number,
                      x_appendix, y_appendix):
    index = int(len(unit.crew) - 1)
    while index >= 0:
        row = math.ceil((index + 1) / unit.number)
        if (index + 1) % unit.number == 0:
            line = unit.number
        else:
            line = (index + 1) % unit.number

        if unit.number == 1:
            x_appendix = unit.crew[index].img_width / 2
            y_appendix = unit.crew[index].img_height / 2
        else:
            x_appendix = (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number)
            y_appendix = (unit.number - line) * (48 / div_number) - (row - 1) * (40 / div_row)

        creature_position = [(x - 1) * 96 + 48 - (unit.crew[index].img_width / 2) + x_appendix,
                             (y - 1) * 96 + 48 - (unit.crew[index].img_height / 2) + y_appendix]

        xy_animation = animate(unit, owner, index, unit_index, b, current_position, creature_position, row, line)
        draw_single_creature(screen, creature_position, xy_animation, unit, index, side)

        sc_battle.draw_siege_machine(screen, unit, index, row, line, side, x, y, unit_index, current_position, b, owner)
        index -= 1


def animate(unit, owner, index, unit_index, b, current_position, creature_position, row, line):
    xy_animation = [0, 0]
    if b.primary == "Rotate":
        xy_animation = anim_battle_unit_action.unit_rotate(b, unit, unit_index, owner, current_position,
                                                           creature_position, unit.number, row, line,
                                                           unit.crew[index].img_width,
                                                           unit.crew[index].img_height, unit.rows)
    elif b.primary == "Move":
        xy_animation = anim_battle_unit_action.unit_march(b, unit_index, current_position,
                                                          creature_position, unit.number, row, line,
                                                          unit.crew[index].img_width,
                                                          unit.crew[index].img_height, unit.rows,
                                                          owner)
    elif b.primary == "Hit from above":
        xy_animation = anim_battle_unit_action.unit_nosedive(b, unit_index, owner)
    return xy_animation


def draw_single_creature(screen, creature_position, xy_animation, unit, index, side):
    army_img = game_stats.gf_regiment_dict[unit.crew[index].img_source + "/" + unit.crew[index].img + side]
    screen.blit(army_img,
                (creature_position[0] + xy_animation[0],
                 creature_position[1] + xy_animation[1]))


direction_dict = {"E": facing_east,
                  "W": facing_west,
                  "N": facing_north,
                  "S": facing_south,
                  "NE": facing_north_east,
                  "NW": facing_north_west,
                  "SE": facing_south_east,
                  "SW": facing_south_west}
