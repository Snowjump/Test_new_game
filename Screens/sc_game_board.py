## Among Myth and Wonder
## sc_game_board

import math
import pygame.transform
import pygame.draw
import pygame.font

from Screens.colors_catalog import *
from Screens.fonts_catalog import *
from Screens.draw_alpha_funs import *

from Resources import game_obj
from Resources import game_stats
from Resources.Game_Graphics import graphics_obj
from Resources import common_selects

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

from Screens.Interface_Elements import buttons

from Screens.Sc_Game_Board import draw_tiles_funs

# Ask someone how to do it better
from Screens.Panels.Bonus_panels import mythic_monolith_win
from Screens.Panels.Bonus_panels import stone_circle_win
from Screens.Panels.Bonus_panels import scholars_tower_win
from Screens.Panels.Bonus_panels import stone_well_win
from Screens.Panels.Bonus_panels import burial_mound_win
from Screens.Panels.Bonus_panels import anglers_cabin_win
from Screens.Panels.Bonus_panels import champions_tent_win
from Screens.Panels.Bonus_panels import leshys_hut_win
from Screens.Panels.Lair_panels import runaway_serfs_refuge_win
from Screens.Panels.Lair_panels import treasure_tower_win
from Screens.Panels.Lair_panels import lair_of_grey_dragons_win

from Screens.Panels.Result_panels import runaway_serfs_refuge_result_win
from Screens.Panels.Result_panels import treasure_tower_result_win
from Screens.Panels.Result_panels import lair_of_grey_dragons_result_win

from Screens.Panels.Quest_result_panels import poachers_in_royal_forest_result_win
from Screens.Panels.Quest_result_panels import slay_the_grey_dragon_result_win

pygame.init()


def draw_tiles(screen):
    if game_obj.game_map:
        # Draw tiles, roads and separation borders
        draw_tiles_funs.draw_terrain(screen)

        # Draw realm borders
        draw_tiles_funs.draw_border(screen)

        # Draw objects on tiles
        draw_tiles_funs.draw_map_objects(screen)


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
        text_panel1 = tnr_font20.render(title_text, True, TitleText)
        screen.blit(text_panel1, [550 - len(title_text), 103])

    # Button - play battle
    pygame.draw.polygon(screen, FillButton, [[590, 138], [690, 138], [690, 160], [590, 160]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[590, 138], [690, 138], [690, 160], [590, 160]], 3)
    text_panel5 = tnr_font20.render("Play battle", True, DarkText)
    screen.blit(text_panel5, [595, 138])

    # Button - autobattle
    pygame.draw.polygon(screen, FillButton, [[590, 168], [690, 168], [690, 190], [590, 190]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[590, 168], [690, 168], [690, 190], [590, 190]], 3)
    text_panel5 = tnr_font20.render("Autobattle", True, DarkText)
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
    the_settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)

    pygame.draw.polygon(screen, Board1, [[121, 70], [1159, 70], [1159, 500], [121, 500]])

    pygame.draw.polygon(screen, Board2, [[128, 336], [637, 336], [637, 490], [128, 490]])
    pygame.draw.polygon(screen, Board2, [[643, 336], [1152, 336], [1152, 490], [643, 490]])

    pygame.draw.polygon(screen, Board2, [[811, 120], [1152, 120], [1152, 298], [811, 298]])

    # Battle title
    title_text = "Blockade of " + game_stats.blockaded_settlement_name
    text_panel1 = tnr_font20.render(title_text, True, TitleText)
    screen.blit(text_panel1, [575 - len(title_text), 73])

    # Close settlement siege window
    if game_stats.besieged_by_human or (not game_stats.besieged_by_human and not game_stats.siege_assault):
        pygame.draw.polygon(screen, CancelFieldColor, [[1135, 75], [1154, 75], [1154, 94], [1135, 94]])
        pygame.draw.polygon(screen, CancelElementsColor, [[1135, 75], [1154, 75], [1154, 94], [1135, 94]], 2)
        pygame.draw.line(screen, CancelElementsColor, [1138, 78], [1151, 91], 2)
        pygame.draw.line(screen, CancelElementsColor, [1138, 91], [1151, 78], 2)

    # Siege duration
    text_panel5 = tnr_font16.render("Siege duration:", True, DarkText)
    screen.blit(text_panel5, [128, 95])

    duration_img = game_stats.gf_misc_img_dict["Icons/duration_icon"]
    screen.blit(duration_img, (128, 114))

    duration_text = None
    if the_settlement.siege.time_passed == 1:
        duration_text = "1 turn"
    else:
        duration_text = str(the_settlement.siege.time_passed) + " turns"
    text_panel5 = tnr_font16.render(duration_text, True, DarkText)
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
    text_panel5 = tnr_font20.render(text, True, DarkText)
    screen.blit(text_panel5, [133 + x, y_base + y_shift * y_num])
    y_num += 1

    # Button - Autobattle
    pygame.draw.polygon(screen, FillButton, [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                                             [238, y_base + y_shift * y_num + 22],
                                             [128, y_base + y_shift * y_num + 22]])
    pygame.draw.polygon(screen, color1, [[128, y_base + y_shift * y_num], [238, y_base + y_shift * y_num],
                                         [238, y_base + y_shift * y_num + 22], [128, y_base + y_shift * y_num + 22]], 3)
    text_panel5 = tnr_font20.render("Autobattle", True, DarkText)
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
        text_panel5 = tnr_font20.render("Encircle", True, DarkText)
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
        text_panel5 = tnr_font20.render("Retreat", True, DarkText)
        screen.blit(text_panel5, [155, y_base + y_shift * y_num])

        # Display defensive structures
        text_panel5 = tnr_font20.render("Defences", True, DarkText)
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
    text_panel5 = tnr_font16.render(supplies_msg, True, DarkText)
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
                text_panel5 = tnr_font16.render(gate_msg, True, DarkText)
                screen.blit(text_panel5, [256 + 25 - (len(gate_msg) * 4), 228])

        if total_wal_sections > 0:
            # Number message
            number_msg = str(unbroken_wall_sections) + "/" + str(total_wal_sections)
            text_panel5 = tnr_font16.render(number_msg, True, DarkText)
            screen.blit(text_panel5, [326 + num * 52 + 25 - (len(number_msg) * 4), 164])

    y_base = 95
    y_shift = 44
    circle_radius = 9

    # Display siege engines
    text_panel5 = tnr_font20.render("Siege engines", True, DarkText)
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
        text_panel = tnr_font20.render(str(the_settlement.siege.trebuchets_ordered), True, DarkText)
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
    text_panel = tnr_font20.render(text_line, True, DarkText)
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
        text_panel = tnr_font20.render(str(the_settlement.siege.siege_towers_ordered), True, DarkText)
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
    text_panel = tnr_font20.render(text_line, True, DarkText)
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
        text_panel = tnr_font20.render(str(the_settlement.siege.battering_rams_ordered), True, DarkText)
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
    text_panel = tnr_font20.render(text_line, True, DarkText)
    screen.blit(text_panel, [752, y_base + y_shift * 2 + 10])

    # Siege log
    text_panel5 = tnr_font20.render("Events log", True, DarkText)
    screen.blit(text_panel5, [935, 95])

    y_base = 123
    y_shift = 16
    y_num = 0
    for text_log in the_settlement.siege.siege_log:
        text_panel = tnr_font16.render(text_log, True, DarkText)
        screen.blit(text_panel, [821, y_base + y_shift * y_num])
        y_num += 1

    # Display units
    for army in game_obj.game_armies:
        if army.army_id == game_stats.attacker_army_id:  # Attacker
            if army.owner == "Neutral":
                text_panel = tnr_font20.render("Neutral", True, DarkText)
                screen.blit(text_panel, [351, 312])
            else:
                for power in game_obj.game_powers:
                    if power.name == army.owner:
                        x_cor = 351
                        y_cor = 312
                        # Country's name
                        text_panel = tnr_font20.render(power.name, True, DarkText)
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
                text_panel = tnr_font20.render("Neutral", True, DarkText)
                screen.blit(text_panel, [841, 312])
            else:
                for power in game_obj.game_powers:
                    if power.name == army.owner:
                        x_cor = 841
                        y_cor = 312
                        # Country's name
                        text_panel = tnr_font20.render(power.name, True, DarkText)
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


def settlement_panel(screen):
    # Draw top left panel with interface to interact with settlement mechanics
    pygame.draw.polygon(screen, MainMenuColor, [[1, 80], [639, 80], [639, 540], [1, 540]])

    # Buttons - settlement interface area
    # Building
    pygame.draw.polygon(screen, FillButton, [[5, 85], [110, 85], [110, 104], [5, 104]])
    if game_stats.settlement_area == "Building":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[5, 85], [110, 85], [110, 104], [5, 104]], 2)

    icon_img = game_stats.gf_misc_img_dict["Icons/building_icon"]
    screen.blit(icon_img, (11, 88))

    text_panel1 = tnr_font16.render("Building", True, DarkText)
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

    text_panel1 = tnr_font16.render("Recruiting", True, DarkText)
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

    text_panel1 = tnr_font16.render("Heroes", True, DarkText)
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

    text_panel1 = tnr_font16.render("Economy", True, DarkText)
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

    text_panel1 = tnr_font16.render("Factions", True, DarkText)
    screen.blit(text_panel1, [495, 85])

    # Close settlement window
    buttons.element_close_button(screen, "CancelFieldColor", "CancelElementsColor", "CancelElementsColor",
                                 615, 85, 19, 19, 2, 2)

    settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)

    # Draw area content
    detail_functions_voc = {"Building": det_settlement_buildings.draw_structures,
                            "Recruiting": det_settlement_recruiting.draw_units,
                            "Heroes": det_settlement_heroes.draw_heroes,
                            "Economy": det_settlement_economy.draw_economy,
                            "Factions": det_settlement_factions.draw_factions}

    detail_functions_voc[game_stats.settlement_area](screen, settlement)


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

    text_panel = tnr_font20.render(power.name, True, TitleText)
    screen.blit(text_panel, [75, 85])

    icon_img = game_stats.gf_misc_img_dict["Icons/masks"]
    screen.blit(icon_img, (41, 109))

    text_panel = tnr_font20.render(power.alignment, True, TitleText)
    screen.blit(text_panel, [75, 110])

    icon_img = game_stats.gf_misc_img_dict["Icons/crown_bigger"]
    screen.blit(icon_img, (39, 134))

    text_panel = tnr_font20.render(power.leader.name, True, TitleText)
    screen.blit(text_panel, [75, 135])

    # Traits
    x_base = 38
    y_base = 160
    y_shift = 19
    y_num = 0

    # Speciality trait
    text_panel = tnr_font16.render("Speciality trait", True, TitleText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    y_num += 1

    # Behavior traits
    text_panel = tnr_font16.render("Behavior traits", True, TitleText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    text_panel = tnr_font16.render(power.leader.behavior_traits[0], True, DarkText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    if len(power.leader.behavior_traits) > 1:
        text_panel = tnr_font16.render(power.leader.behavior_traits[1], True, DarkText)
        screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    # Lifestyle traits
    text_panel = tnr_font16.render("Lifestyle traits", True, TitleText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    text_panel = tnr_font16.render(power.leader.lifestyle_traits[0], True, DarkText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    text_panel = tnr_font16.render(power.leader.lifestyle_traits[1], True, DarkText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1


def army_exchange_panel(screen):
    # Second army standing for exchange
    yVar = game_stats.game_window_height - 800
    pygame.draw.polygon(screen, MainMenuColor,
                        [[200, 380 + yVar], [639, 380 + yVar], [639, 619 + yVar], [200, 619 + yVar]])

    # Ownership
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_second_army:

            if army.owner == "Neutral":
                text_panel = tnr_font20.render("Neutral", True, TitleText)
                screen.blit(text_panel, [240, 384 + yVar])
            else:
                power = common_selects.select_realm_by_name(army.owner)
                # Country's name
                text_panel = tnr_font20.render(power.name, True, TitleText)
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
    army = common_selects.select_army_by_id(game_stats.selected_second_army)
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
    buttons.element_button(screen, "Complete", "tnr_font18", "DarkText", None, "CancelElementsColor",
                           203, 595 + yVar, 77, 18, 4, -1, 2)
    # pygame.draw.polygon(screen, CancelElementsColor,
    #                     [[203, 595 + yVar], [290, 595 + yVar], [290, 617 + yVar], [203, 617 + yVar]], 2)
    #
    # text_NewGame1 = tnr_font20.render("Complete", True, DarkText)
    # screen.blit(text_NewGame1, [207, 594 + yVar])


def quest_log_panel(screen):
    # Draw top left panel with interface to interact with realm's quest # x: 1 -> 34
    pygame.draw.polygon(screen, MainMenuColor, [[34, 80], [679, 80], [679, 540], [34, 540]])

    # Close quest log window
    buttons.element_close_button(screen, "CancelFieldColor", "CancelElementsColor", "CancelElementsColor",
                                 655, 85, 19, 19, 2, 2)

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

    text_panel1 = tnr_font16.render("Quest messages", True, DarkText)
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

    text_panel1 = tnr_font16.render("Diplomatic messages", True, DarkText)
    screen.blit(text_panel1, [x1 + 4, 85])

    # Draw area content
    det_quest_log.area_management(screen)


def diplomacy_panel(screen):
    power = game_stats.realm_inspection

    # Draw top left panel with interface to participate in diplomacy
    pygame.draw.polygon(screen, MainMenuColor, [[34, 80], [679, 80], [679, 540], [34, 540]])

    # Buttons - diplomacy interface area
    # Close diplomacy window
    buttons.element_close_button(screen, "CancelFieldColor", "CancelElementsColor", "CancelElementsColor",
                                 655, 85, 19, 19, 2, 2)

    # Draw area content
    det_diplomacy.area_management(screen, power)


def war_panel(screen):
    # Draw top left panel with interface to interact with selected war
    pygame.draw.polygon(screen, MainMenuColor, [[34, 80], [679, 80], [679, 540], [34, 540]])

    # Buttons - war interface area
    # Close war window
    buttons.element_close_button(screen, "CancelFieldColor", "CancelElementsColor", "CancelElementsColor",
                                 655, 85, 19, 19, 2, 2)

    # Draw war interface
    det_war.draw_war(screen)


def game_board_screen(screen):
    screen.fill(MapLimitColor)  # background

    draw_tiles(screen)  # Draw tiles

    yVar = game_stats.game_window_height - 800

    ## Buttons
    for obj in graphics_obj.game_board_objects:
        obj.draw_panel(screen)
        # print(obj.name)

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
        text_NewGame2 = tnr_font20.render(str(math.floor(game_stats.passed_time / 1000)), True, TitleText)
        screen.blit(text_NewGame2, [400, 30])
        text_NewGame2 = tnr_font20.render(str(game_stats.display_time), True, TitleText)
        screen.blit(text_NewGame2, [400, 70])

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
        text_panel = tnr_font20.render("Pause", True, TitleText)
        screen.blit(text_panel, [50, 64])

    # FPS
    if game_stats.fps_status:
        text_panel = tnr_font20.render(str(game_stats.fps), True, TitleText)
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
    "champion's tent event panel": champions_tent_win.champions_tent_draw_panel,
    "leshy's hut event panel": leshys_hut_win.leshys_hut_draw_panel,
    "leshy's hut dice results event panel": leshys_hut_win.leshys_hut_dice_result_draw_panel,
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

draw_right_window = {"Building upgrade information": rw_upgrade_building.draw_upgrade_info,
                     "Building information": rw_building.draw_building_info,
                     "New regiment information": rw_new_regiment_information.new_regiment_info,
                     "New hero skill tree": rw_new_hero_skill_tree.skill_tree_info,
                     "Hero window": rw_hero_window.draw_hero_window}
