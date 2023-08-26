## Miracle battles!

import pygame.draw
import pygame.font

from Resources import game_stats
from Content import unit_img_catalog
from Content import enlist_regiment_prices
from Content import unit_alignment_catalog
# from Storage import create_unit

arial_font20 = pygame.font.SysFont('arial', 20)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)


resources_icons = {"Florins" : "resource_florins",
                   "Food" : "resource_food",
                   "Wood" : "resource_wood",
                   "Metals" : "resource_metalsg",
                   "Stone" : "resource_stone",
                   "Armament" : "resource_armament",
                   "Tools" : "resource_tools",
                   "Ingredients" : "resource_ingredients"}

WhiteColor = [255, 255, 255]

DarkText = [0x11, 0x11, 0x11]

WhiteBorder = [249, 238, 227, 200]

LineMainMenuColor1 = [0x60, 0x60, 0x60]

FillButton = [0xD8, 0xBD, 0xA2]

HighlightOption = [0x00, 0xCC, 0xCC]

RockTunel = [0x89, 0x89, 0x89]


def draw_units(screen, settlement):
    # Background
    pygame.draw.polygon(screen, FillButton,
                        [[283, 111],
                         [637, 111],
                         [637, 538],
                         [283, 538]])

    # Buttons - previous and next regiment
    pygame.draw.polygon(screen, RockTunel, [[260, 112], [279, 112], [279, 131], [260, 131]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[260, 112], [279, 112], [279, 131], [260, 131]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(264, 128), (270, 115), (276, 128)], 2)

    pygame.draw.polygon(screen, RockTunel, [[260, 517], [279, 517], [279, 536], [260, 536]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[260, 517], [279, 517], [279, 536], [260, 536]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(264, 520), (270, 534), (276, 520)], 2)

    alignment = settlement.alignment
    y_points = 0
    y_shift = 52

    for plot in settlement.buildings:
        if plot.structure is not None:
            if len(plot.structure.recruitment) > 0 and plot.status == "Built":
                for recruit in plot.structure.recruitment:
                    # Background
                    pygame.draw.polygon(screen, FillButton,
                                        [[54, 115 + y_shift * y_points],
                                         [257, 115 + y_shift * y_points],
                                         [257, 162 + y_shift * y_points],
                                         [54, 162 + y_shift * y_points]])

                    # Regiment's icon
                    back_img = game_stats.gf_misc_img_dict['Icons/paper_3_square_48']
                    screen.blit(back_img,
                                [3, 115 + y_shift * y_points])

                    unit_info = unit_img_catalog.units_img_dict_by_alignment[settlement.alignment][recruit.unit_name]
                    # Previous code
                    # army_img = pygame.image.load(
                    #     'img/Creatures/' + str(unit_info[1]) + "/" + str(unit_info[0]) + '.png')
                    # army_img.set_colorkey(WhiteColor)

                    # New code
                    army_img = game_stats.gf_regiment_dict[unit_info[1] + "/" + unit_info[0] + "_r"]
                    screen.blit(army_img,
                                [5 + 22 - (unit_info[2] / 2), 115 + 24 + y_shift * y_points - (unit_info[3] / 2)])

                    # Regiment's name
                    text_panel1 = arial_font20.render(recruit.unit_name, True, DarkText)
                    screen.blit(text_panel1, [58, 126 + y_shift * y_points])

                    if game_stats.unit_for_hire is not None:
                        if recruit.unit_name == game_stats.unit_for_hire.unit_name:
                            # White border
                            pygame.draw.polygon(screen, WhiteBorder, [[54, 115 + y_shift * y_points],
                                                                      [256, 115 + y_shift * y_points],
                                                                      [256, 161 + y_shift * y_points],
                                                                      [54, 161 + y_shift * y_points]], 2)
                    y_points += 1

    if game_stats.unit_for_hire is not None:
        # Button - regiment’s stats
        pygame.draw.polygon(screen, FillButton,
                            [[286, 112], [396, 112], [396, 132], [286, 132]])
        pygame.draw.polygon(screen, LineMainMenuColor1, [[286, 112], [396, 112], [396, 132], [286, 132]], 2)

        text_panel1 = arial_font14.render("Regiment’s stats", True, DarkText)
        screen.blit(text_panel1, [289, 115])

        # Button - hire regiment
        pygame.draw.polygon(screen, FillButton,
                            [[406, 112], [516, 112], [516, 132], [406, 132]])
        if game_stats.unit_for_hire.ready_units > 0 and game_stats.enough_resources_to_pay:
            color1 = HighlightOption
        else:
            color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, color1, [[406, 112], [516, 112], [516, 132], [406, 132]], 2)

        text_panel1 = arial_font14.render("Hire regiment", True, DarkText)
        screen.blit(text_panel1, [418, 115])

        # Capacity
        text = str(game_stats.unit_for_hire.ready_units) + "/" \
               + str(game_stats.unit_for_hire.hiring_capacity) \
               + " " + game_stats.unit_for_hire.unit_name
        if game_stats.unit_for_hire.ready_units == 1:
            text += " regiment ready for recruitment"
        else:
            text += " regiments ready for recruitment"

        text_panel1 = arial_font14.render(text, True, DarkText)
        screen.blit(text_panel1, [286, 135])
        # y_points += 1

        # Replenishment
        # Duration icon
        time_img = game_stats.gf_misc_img_dict["Icons/duration_icon"]
        screen.blit(time_img, (286, 156))

        text = ""
        if game_stats.unit_for_hire.replenishment_rate - game_stats.unit_for_hire.time_passed == 1:
            text += "1 turn until replenishment"
        else:
            text += str(game_stats.unit_for_hire.replenishment_rate - game_stats.unit_for_hire.time_passed)\
                    + " turns until replenishment"

        text_panel1 = arial_font14.render(text, True, DarkText)
        screen.blit(text_panel1, [301, 155])

        # Recruitment cost
        text_panel1 = arial_font14.render("Recruitment cost:", True, DarkText)
        screen.blit(text_panel1, [286, 175])

        # Upkeep cost
        text_panel1 = arial_font14.render("Upkeep cost:", True, DarkText)
        screen.blit(text_panel1, [416, 175])

        # Cost - resources
        # for unit_card in create_unit.LE_units_dict_by_alignment[alignment]:
        #     if unit_card.name == game_stats.unit_for_hire.unit_name:
        unit_card = game_stats.rw_object
        alignment = unit_alignment_catalog.alignment_dict[unit_card.name]
        y_points2 = 0
        y_shift2 = 20
        for res in enlist_regiment_prices.units_dict_by_alignment[alignment][unit_card.name]:
            # Resource icon
            icon_img = game_stats.gf_misc_img_dict[resources_icons[res[0]]]
            screen.blit(icon_img, (286, 196 + y_points2 * y_shift2))

            recruitment_cost_text = str(res[0]) + " " + str(res[1])
            text_panel1 = arial_font14.render(recruitment_cost_text, True, DarkText)
            screen.blit(text_panel1, [305, 195 + y_points2 * y_shift2])

            y_points2 += 1

        y_points2 = 0
        y_shift2 = 20
        for res in unit_card.cost:
            # Resource icon
            icon_img = game_stats.gf_misc_img_dict[resources_icons[res[0]]]
            screen.blit(icon_img, (416, 196 + y_points2 * y_shift2))

            upkeep_cost_text = str(res[0]) + " " + str(res[1] * unit_card.rows * unit_card.number)
            text_panel1 = arial_font14.render(upkeep_cost_text, True, DarkText)
            screen.blit(text_panel1, [435, 195 + y_points2 * y_shift2])

            y_points2 += 1




