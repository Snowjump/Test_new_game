## Miracle battles!

import math
import pygame.draw, pygame.font

from Resources import game_stats
from Content import unit_img_catalog


WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]
ApproveElementsColor = [0x00, 0x66, 0x00]

DarkText = [0x11, 0x11, 0x11]


tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)


def lair_of_grey_dragons_result_draw_panel(screen):
    # [[200, 380 + yVar], [639, 380 + yVar], [639, 619 + yVar], [200, 619 + yVar]]
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 505], [481, 505]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 475], [491, 475]])

    text_panel1 = tnr_font18.render("Lair of grey dragons", True, DarkText)
    screen.blit(text_panel1, [560, 102])

    message = ["At last all grey dragons have been slayed.",
               "After short search in dreadful lair",
               "you found some unhatched eggs.",
               "It's your chance to get a few obeying drakes",
               "to strengthen your forces with firebreathing beasts."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    text_panel1 = tnr_font18.render("Prize:", True, DarkText)
    screen.blit(text_panel1, [500, 148 + y_shift * y_points])

    y_height = 20

    number = 0
    for reward in game_stats.reward_for_demonstration:
        if reward[0] == "Regiment":
            side = "_r"
            x_pos = 493 + math.floor(number % 5) * 52
            y_pos = 149 + y_shift * y_points + y_height + math.floor(number / 5) * 57
            # print(reward[1] + " - " + str(x_pos) + ", " + str(y_pos))

            culture = unit_img_catalog.units_img_dict_by_alignment[reward[2]]
            unit_info = culture[reward[1]]
            # army_img = game_stats.gf_regiment_dict[unit_info[1] + "/" + unit_info[0] + side]

            if unit_info[2] > 44 or unit_info[3] > 44:
                army_img = game_stats.gf_regiment_dict[unit_info[1] + "/" + unit_info[0] + side]
                if unit_info[2] > 44:
                    proportion = 44 / unit_info[2]
                    army_img = pygame.transform.scale(army_img,
                                                      (44,
                                                       int(unit_info[3] * proportion)))
                    x_offset = 3
                    y_offset = (48 - (unit_info[3] * proportion)) / 2
                else:
                    proportion = 44 / unit_info[3]
                    army_img = pygame.transform.scale(army_img,
                                                      (int(unit_info[2] * proportion),
                                                       44))
                    x_offset = (48 - (unit_info[2] * proportion)) / 2
                    y_offset = 3
            else:
                army_img = game_stats.gf_regiment_dict[unit_info[1] + "/" + unit_info[0] + side]
                x_offset = (48 - unit_info[2]) / 2
                y_offset = (48 - unit_info[3]) / 2

            screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])

            if int(number) in game_stats.second_army_exchange_list:
                pygame.draw.polygon(screen, ApproveElementsColor,
                                    [[x_pos + 6, y_pos + 48],
                                     [x_pos + 37, y_pos + 48],
                                     [x_pos + 22, y_pos + 54]])

            number += 1

    pygame.draw.polygon(screen, FillButton,
                        [[611, 481], [670, 481], [670, 501], [611, 501]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[611, 481], [670, 481], [670, 501], [611, 501]], 2)

    text_panel1 = arial_font14.render("Close", True, DarkText)
    screen.blit(text_panel1, [623, 484])
