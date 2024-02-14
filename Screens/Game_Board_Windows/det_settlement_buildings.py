## Among Myth and Wonder
## det_settlement_buildings

import math
import pygame.draw
import pygame.font

from Resources import game_stats
from Resources import common_selects

arrow_green = (0, 102, 0, 180)
arrow_burgundy = (102, 0, 0, 180)

DarkText = [0x11, 0x11, 0x11]

LineMainMenuColor1 = [0x60, 0x60, 0x60]

FillButton = [0xD8, 0xBD, 0xA2]
FieldColor = [0xA0, 0xA0, 0xA0]
ApproveFieldColor = [0x00, 0x99, 0x00]

RockTunel = [0x89, 0x89, 0x89]

font16 = pygame.font.SysFont('arial', 16)
font14 = pygame.font.SysFont('arial', 14)
font12 = pygame.font.SysFont('arial', 12)


def draw_structures(screen, settlement):
    # Buttons - previous and next building row
    pygame.draw.polygon(screen, RockTunel, [[615, 112], [634, 112], [634, 131], [615, 131]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[615, 112], [634, 112], [634, 131], [615, 131]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(619, 128), (625, 115), (631, 128)], 2)

    pygame.draw.polygon(screen, RockTunel, [[615, 517], [634, 517], [634, 536], [615, 536]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[615, 517], [634, 517], [634, 536], [615, 536]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(619, 520), (625, 534), (631, 520)], 2)

    # Scroll
    y1 = 132 + int(game_stats.building_row_index * (383 / game_stats.building_rows_amount))
    y2 = int(383 / game_stats.building_rows_amount * 4)
    pygame.draw.polygon(screen, RockTunel, [[615, y1], [634, y1], [634, y1 + y2], [615, y1 + y2]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[615, y1], [634, y1], [634, y1 + y2], [615, y1 + y2]], 2)

    treasury = common_selects.select_treasury_by_realm_name(settlement.owner)

    for plot in settlement.buildings:
        xy = plot.screen_position
        # Draw only 4 rows of plot at a time
        if game_stats.building_row_index < xy[1] <= game_stats.building_row_index + 4:

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

            # Upgrade icon in lower part of structure card
            arrow_color = arrow_burgundy
            enough = True

            if plot.upgrade and treasury:
                if len(treasury) > 0:
                    for res1 in plot.upgrade.construction_cost:
                        available = False
                        for res2 in treasury:
                            if res1[0] == res2[0]:
                                if res1[1] <= res2[1]:
                                    pass
                                else:
                                    enough = False
                                available = True

                        if not available:
                            enough = False
                else:
                    enough = False

                if enough and plot.upgrade.fulfilled_conditions:
                    arrow_color = arrow_green

                pygame.draw.polygon(screen, arrow_color,
                                    [[x3 + 8, y3 + 20],
                                     [x3 + 8, y3 + 15],
                                     [x3 + 2, y3 + 15],
                                     [x3 + 12, y3],
                                     [x3 + 13, y3],
                                     [x3 + 23, y3 + 15],
                                     [x3 + 17, y3 + 15],
                                     [x3 + 17, y3 + 20]])
            else:
                pass
                # No upgrade for this structure

            # Buildings title
            if plot.structure is None:
                text_panel1 = font12.render("Empty", True, DarkText)
                screen.blit(text_panel1, [x1 + 45, y1 + 5])
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

            # Build and upgrade space in lower zone of structure card

            y_shift = 10
            y_points = 0
            if plot.upgrade is not None:
                # Buildings title
                for text_line in plot.upgrade.title_name:
                    text_panel1 = font12.render(str(text_line), True, DarkText)
                    screen.blit(text_panel1, [x1 + 45, y1 + 77 + y_shift * y_points])
                    y_points += 1
            elif plot.status == "Building":
                # Building progress - how many turn left to complete construction
                progress = math.floor(plot.structure.time_passed / plot.structure.construction_time)

                pygame.draw.polygon(screen, ApproveFieldColor,
                                    [[x1 + 36, y1 + 76],
                                     [x1 + 36 + progress * (x2 - 1 - x1 - 35), y1 + 76],
                                     [x1 + 36 + progress * (x2 - 1 - x1 - 35),  y2 - 1],
                                     [x1 + 36, y2 - 1]])

                message = " turns left"
                if plot.structure.construction_time - plot.structure.time_passed == 1:
                    message = " turn left"

                # Duration icon
                time_img = game_stats.gf_misc_img_dict["Icons/duration_icon"]
                screen.blit(time_img, (x1 + 54, y1 + 80))

                text_panel1 = font14.render(str(plot.structure.construction_time - plot.structure.time_passed)
                                            + message, True, DarkText)
                screen.blit(text_panel1, [x1 + 74, y1 + 78])
