## Among Myth and Wonder
## rw_new_hero_skill_tree

import pygame.draw
import pygame.font

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Screens.Interface_Elements import buttons

from Resources import game_stats
from Content import battle_attributes_catalog


# MainMenuColor = [0x9F, 0x97, 0x97]
#
# TitleText = [0xFF, 0xFF, 0x99]
# DarkText = [0x11, 0x11, 0x11]
#
# LineMainMenuColor1 = [0x60, 0x60, 0x60]
# FillButton = [0xD8, 0xBD, 0xA2]
# FieldColor = [0xA0, 0xA0, 0xA0]
#
# CancelFieldColor = [0xFF, 0x00, 0x00]
# CancelElementsColor = [0x99, 0x00, 0x00]
#
# RockTunel = [0x89, 0x89, 0x89]

# tnr_font20 = pygame.font.SysFont('timesnewroman', 20)
#
# arial_font16 = pygame.font.SysFont('arial', 16)
# arial_font14 = pygame.font.SysFont('arial', 14)


def skill_tree_info(screen):
    # Draw top right panel with abilities skill tree for new hero
    pygame.draw.polygon(screen, MainMenuColor,
                        [[642, 80], [1278, 80], [1278, 540], [642, 540]])

    # Background
    pygame.draw.polygon(screen, FillButton,
                        [[644, 111], [1276, 111], [1276, 538], [644, 538]])

    # Hero class
    text_panel = tnr_font20.render(game_stats.hero_for_hire[0] + " skill tree", True, TitleText)
    screen.blit(text_panel, [646, 87])

    # Close skill tree window
    buttons.element_close_button(screen, "CancelFieldColor", "CancelElementsColor", "CancelElementsColor",
                                 1254, 85, 19, 19, 2, 2)

    # Buttons - previous and next level
    ybase = 117
    buttons.element_arrow_button(screen, "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 646, ybase, 19, 19, 2, 2)
    buttons.element_arrow_button(screen, "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 1254, ybase, 19, 19, 2, 2)
    # pygame.draw.polygon(screen, RockTunel, [[646, ybase], [665, ybase], [665, ybase + 19], [646, ybase + 19]])
    # pygame.draw.polygon(screen, LineMainMenuColor1, [[646, ybase], [665, ybase], [665, ybase + 19], [646, ybase + 19]],
    #                     2)
    # pygame.draw.lines(screen, LineMainMenuColor1, False, [(662, ybase + 3), (650, ybase + 10), (662, ybase + 16)], 2)
    #
    # pygame.draw.polygon(screen, RockTunel, [[1254, ybase], [1273, ybase], [1273, ybase + 19], [1254, ybase + 19]])
    # pygame.draw.polygon(screen, LineMainMenuColor1, [[1254, ybase], [1273, ybase], [1273, ybase + 19], [1254, ybase + 19]],
    #                     2)
    # pygame.draw.lines(screen, LineMainMenuColor1, False, [(1257, ybase + 3), (1269, ybase + 10), (1257, ybase + 16)], 2)

    # level N
    text_panel = tnr_font20.render("Level " + str(game_stats.skill_tree_level_index + 1), True, TitleText)
    screen.blit(text_panel, [711, 115])

    # level N + 1
    text_panel = tnr_font20.render("Level " + str(game_stats.skill_tree_level_index + 2), True, TitleText)
    screen.blit(text_panel, [924, 115])

    # level N + 2
    text_panel = tnr_font20.render("Level " + str(game_stats.skill_tree_level_index + 3), True, TitleText)
    screen.blit(text_panel, [1137, 115])

    # 1 row of battle attributes
    y_points2 = 0
    y_shift2 = 20

    for pack in battle_attributes_catalog.basic_heroes_attributes[game_stats.hero_for_hire[0]][
        game_stats.skill_tree_level_index - 1]:
        # Background
        length = len(pack.attribute_list) - 1
        pygame.draw.polygon(screen, FieldColor,
                            [[646, 141 + y_shift2 * y_points2],
                             [848, 141 + y_shift2 * y_points2],
                             [848, 159 + y_shift2 * y_points2 + length * 20],
                             [646, 159 + y_shift2 * y_points2 + length * 20]])

        att_num = 0
        for att in pack.attribute_list:
            text = str(att.tag.capitalize()) + ": " + str(att.stat) + " +" + str(att.value)
            text_panel1 = arial_font12.render(text, True, DarkText)
            screen.blit(text_panel1, [648, 144 + y_shift2 * y_points2 + att_num * y_shift2])

            att_num += 1

        y_points2 += 1

    # 2 row of battle attributes
    y_points2 = 0
    y_shift2 = 20

    for pack in battle_attributes_catalog.basic_heroes_attributes[game_stats.hero_for_hire[0]][
        game_stats.skill_tree_level_index]:
        # Background
        length = len(pack.attribute_list) - 1
        pygame.draw.polygon(screen, FieldColor,
                            [[859, 141 + y_shift2 * y_points2],
                             [1061, 141 + y_shift2 * y_points2],
                             [1061, 159 + y_shift2 * y_points2 + length * 20],
                             [859, 159 + y_shift2 * y_points2 + length * 20]])

        att_num = 0
        for att in pack.attribute_list:
            text = str(att.tag.capitalize()) + ": " + str(att.stat) + " +" + str(att.value)
            text_panel1 = arial_font12.render(text, True, DarkText)
            screen.blit(text_panel1, [861, 144 + y_shift2 * y_points2 + att_num * y_shift2])

            att_num += 1

        y_points2 += 1

    # 3 row of battle attributes
    y_points2 = 0
    y_shift2 = 20

    for pack in battle_attributes_catalog.basic_heroes_attributes[game_stats.hero_for_hire[0]][
        game_stats.skill_tree_level_index + 1]:
        # Background
        length = len(pack.attribute_list) - 1
        pygame.draw.polygon(screen, FieldColor,
                            [[1072, 141 + y_shift2 * y_points2],
                             [1274, 141 + y_shift2 * y_points2],
                             [1274, 159 + y_shift2 * y_points2 + length * 20],
                             [1072, 159 + y_shift2 * y_points2 + length * 20]])

        att_num = 0
        for att in pack.attribute_list:
            text = str(att.tag.capitalize()) + ": " + str(att.stat) + " +" + str(att.value)
            text_panel1 = arial_font12.render(text, True, DarkText)
            screen.blit(text_panel1, [1074, 144 + y_shift2 * y_points2 + att_num * y_shift2])

            att_num += 1

        y_points2 += 1
