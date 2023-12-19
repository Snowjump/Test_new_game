## Among Myth and Wonder

import pygame.draw
import pygame.font

from Resources import game_stats
from Resources import game_obj

WhiteColor = [255, 255, 255]

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]

WhiteBorder = [249, 238, 227, 200]

LineMainMenuColor1 = [0x60, 0x60, 0x60]
FillButton = [0xD8, 0xBD, 0xA2]
FieldColor = [0xA0, 0xA0, 0xA0]
HighlightOption = [0x00, 0xCC, 0xCC]
RockTunel = [0x89, 0x89, 0x89]

tnr_font26 = pygame.font.SysFont('timesnewroman', 26)
tnr_font20 = pygame.font.SysFont('timesnewroman', 20)
tnr_font18 = pygame.font.SysFont('timesnewroman', 20)
tnr_font16 = pygame.font.SysFont('timesnewroman', 16)
arial_font20 = pygame.font.SysFont('arial', 20)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)


def draw_economy(screen, settlement):
    # Black line
    pygame.draw.line(screen, DarkText, [3, 109], [637, 109], 2)

    # Buttons - subsection buttons
    # Button - Overview subsection
    pygame.draw.polygon(screen, FillButton,
                        [[5, 114], [110, 114], [110, 133], [5, 133]])
    if game_stats.settlement_subsection == "Overview":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[5, 114], [110, 114], [110, 133], [5, 133]], 2)

    text_panel1 = tnr_font16.render("Overview", True, DarkText)
    screen.blit(text_panel1, [25, 114])

    # Button - Population subsection
    pygame.draw.polygon(screen, FillButton,
                        [[120, 114], [225, 114], [225, 133], [120, 133]])
    if game_stats.settlement_subsection == "Population":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[120, 114], [225, 114], [225, 133], [120, 133]], 2)

    text_panel1 = tnr_font16.render("Population", True, DarkText)
    screen.blit(text_panel1, [140, 114])

    # Button - Local market subsection
    pygame.draw.polygon(screen, FillButton,
                        [[235, 114], [340, 114], [340, 133], [235, 133]])
    if game_stats.settlement_subsection == "Local market":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[235, 114], [340, 114], [340, 133], [235, 133]], 2)

    text_panel1 = tnr_font16.render("Local market", True, DarkText)
    screen.blit(text_panel1, [245, 114])

    # Button - Trade routes subsection
    pygame.draw.polygon(screen, FillButton,
                        [[350, 114], [455, 114], [455, 133], [350, 133]])
    if game_stats.settlement_subsection == "Trade routes":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[350, 114], [455, 114], [455, 133], [350, 133]], 2)

    text_panel1 = tnr_font16.render("Trade routes", True, DarkText)
    screen.blit(text_panel1, [363, 114])

    # Black line
    pygame.draw.line(screen, DarkText, [3, 138], [637, 138], 2)

    # Overview subsection
    if game_stats.settlement_subsection == "Overview":
        # Left side - province economy
        # Background
        pygame.draw.polygon(screen, FillButton,
                            [[3, 143],
                             [221, 143],
                             [221, 538],
                             [3, 538]])

        pygame.draw.polygon(screen, FillButton,
                            [[224, 143],
                             [637, 143],
                             [637, 538],
                             [224, 538]])

        y_base = 143

        # Domain overview
        text_panel = tnr_font20.render("Domain overview", True, DarkText)
        screen.blit(text_panel, [20, y_base])
        y_base += 24

        turnover_tax_value = 0
        gold_mining_fee = 0
        # Total local income
        text_panel = tnr_font16.render("Total local income:", True, DarkText)
        screen.blit(text_panel, [5, y_base])

        income = 0
        for res in game_stats.province_records:
            if res[0] == "Florins":
                income += int(res[1])
                gold_mining_fee = int(res[1])
            elif res[0] == "Turnover tax":
                income += int(res[1])
                turnover_tax_value = int(res[1])
        text_panel = arial_font14.render("Florins   " + str(income), True, DarkText)
        screen.blit(text_panel, [130, y_base])
        y_base += 20

        # Trade tax
        text_panel = tnr_font16.render("Trade tax:", True, DarkText)
        screen.blit(text_panel, [5, y_base])

        text_panel = arial_font14.render("(+) Florins   " + str(turnover_tax_value), True, DarkText)
        screen.blit(text_panel, [72, y_base])
        y_base += 20

        # Gold mining fee
        text_panel = tnr_font16.render("Gold mining fee:", True, DarkText)
        screen.blit(text_panel, [5, y_base])

        text_panel = arial_font14.render("(+) Florins   " + str(gold_mining_fee), True, DarkText)
        screen.blit(text_panel, [115, y_base])
        y_base += 20

        # Local fees
        text_panel = tnr_font16.render("Local fees:", True, DarkText)
        screen.blit(text_panel, [5, y_base])
        y_base += 20

        for res in game_stats.province_records:
            if res[0] != "Florins" and res[0] != "Turnover tax":
                text_panel = arial_font14.render(res[0] + "   " + str(res[1]), True, DarkText)
                screen.blit(text_panel, [5, y_base])
                y_base += 20

        # Right side - population economy
        y_base = 143

        # Domain overview
        text_panel = tnr_font20.render("Population overview", True, DarkText)
        screen.blit(text_panel, [340, y_base])
        y_base += 24

        # Produced goods by population
        text_panel = tnr_font16.render("Produced and", True, DarkText)
        screen.blit(text_panel, [226, y_base])
        y_base += 16
        text_panel = tnr_font16.render("obtained goods:", True, DarkText)
        screen.blit(text_panel, [226, y_base])
        y_base += 20

        for res in game_stats.allocated_gains_records:
            text_panel = arial_font14.render(res[0] + "   " + str(res[1]), True, DarkText)
            screen.blit(text_panel, [226, y_base])
            y_base += 20

        # Sold goods
        y_base = 178
        text_panel = tnr_font16.render("Sold goods:", True, DarkText)
        screen.blit(text_panel, [376, y_base])
        y_base += 25

        for res in game_stats.allocated_sold_records:
            text_panel = arial_font14.render(res[0] + "   " + str(res[1]), True, DarkText)
            screen.blit(text_panel, [376, y_base])
            y_base += 20

        # Bought goods
        y_base = 178
        text_panel = tnr_font16.render("Bought goods:", True, DarkText)
        screen.blit(text_panel, [516, y_base])
        y_base += 25

        for res in game_stats.allocated_bought_records:
            text_panel = arial_font14.render(res[0] + "   " + str(res[1]), True, DarkText)
            screen.blit(text_panel, [516, y_base])
            y_base += 20

    # Population subsection
    elif game_stats.settlement_subsection == "Population":
        # Buttons - previous and next population
        pygame.draw.polygon(screen, RockTunel, [[206, 143], [225, 143], [225, 162], [206, 162]])
        pygame.draw.polygon(screen, LineMainMenuColor1, [[206, 143], [225, 143], [225, 162], [206, 162]], 2)
        pygame.draw.lines(screen, LineMainMenuColor1, False, [(210, 159), (216, 146), (222, 159)], 2)

        pygame.draw.polygon(screen, RockTunel, [[206, 517], [225, 517], [225, 536], [206, 536]])
        pygame.draw.polygon(screen, LineMainMenuColor1, [[206, 517], [225, 517], [225, 536], [206, 536]], 2)
        pygame.draw.lines(screen, LineMainMenuColor1, False, [(210, 520), (216, 534), (222, 520)], 2)

        # Background
        pygame.draw.polygon(screen, FillButton,
                            [[229, 143],
                             [637, 143],
                             [637, 538],
                             [229, 538]])

        # Population cards
        y_shift = 44
        y_points = 0
        num = 0
        for pops in settlement.residency:  # Settlement
            if game_stats.pops_card_index <= num < game_stats.pops_card_index + 9:
                # Background
                pygame.draw.polygon(screen, FillButton,
                                    [[3, 143 + y_shift * y_points],
                                     [200, 143 + y_shift * y_points],
                                     [200, 180 + y_shift * y_points],
                                     [3, 180 + y_shift * y_points]])

                # White border for selected population card
                if num == game_stats.population_subsection_index:
                    pygame.draw.polygon(screen, WhiteBorder, [[3, 143 + y_shift * y_points],
                                                              [199, 143 + y_shift * y_points],
                                                              [199, 179 + y_shift * y_points],
                                                              [3, 179 + y_shift * y_points]], 2)

                # Population's name
                text_panel1 = arial_font20.render(pops.name, True, DarkText)
                screen.blit(text_panel1, [7, 142 + y_shift * y_points])

                # Facility
                text_panel1 = arial_font16.render("Settlement", True, DarkText)
                screen.blit(text_panel1, [7, 162 + y_shift * y_points])

                y_points += 1

            num += 1

        for TileNum in settlement.property:  # Facilities

            TileObj = game_obj.game_map[TileNum]
            for pops in TileObj.lot.residency:
                if game_stats.pops_card_index <= num < game_stats.pops_card_index + 9:
                    # Background
                    pygame.draw.polygon(screen, FillButton,
                                        [[3, 143 + y_shift * y_points],
                                         [200, 143 + y_shift * y_points],
                                         [200, 180 + y_shift * y_points],
                                         [3, 180 + y_shift * y_points]])

                    # White border for selected population card
                    if num == game_stats.population_subsection_index:
                        pygame.draw.polygon(screen, WhiteBorder, [[3, 143 + y_shift * y_points],
                                                                  [199, 143 + y_shift * y_points],
                                                                  [199, 179 + y_shift * y_points],
                                                                  [3, 179 + y_shift * y_points]], 2)

                    # Population's name
                    text_panel1 = arial_font20.render(pops.name, True, DarkText)
                    screen.blit(text_panel1, [7, 142 + y_shift * y_points])

                    # Facility
                    text_panel1 = arial_font16.render(TileObj.lot.thematic_name, True, DarkText)
                    screen.blit(text_panel1, [7, 162 + y_shift * y_points])

                    y_points += 1

                num += 1

        if game_stats.pops_details is not None:
            y_base = 143

            # Property
            text_panel = tnr_font18.render("Property:", True, DarkText)
            screen.blit(text_panel, [232, y_base])
            y_base += 4

            # Resources in reserve
            if len(game_stats.pops_details.reserve) > 0:
                for resource in game_stats.pops_details.reserve:
                    y_base += 16
                    text_panel = arial_font14.render(resource[0] + "   " + str(resource[1]), True, DarkText)
                    screen.blit(text_panel, [232, y_base])
            else:
                y_base += 16

            # Produced resources
            y_base += 16
            text_panel = tnr_font18.render("Produced:", True, DarkText)
            screen.blit(text_panel, [232, y_base])
            y_base += 4

            # Records from last turn
            if len(game_stats.pops_details.records_gained) > 0:
                for resource in game_stats.pops_details.records_gained:
                    y_base += 16
                    text_panel = arial_font14.render(resource[0] + "   " + str(resource[1]), True, DarkText)
                    screen.blit(text_panel, [232, y_base])
            else:
                y_base += 16

            # Sold resources
            y_base += 16
            text_panel = tnr_font18.render("Sold:", True, DarkText)
            screen.blit(text_panel, [232, y_base])
            y_base += 4

            # Records from last turn
            if len(game_stats.pops_details.records_sold) > 0:
                for resource in game_stats.pops_details.records_sold:
                    y_base += 16
                    text_panel = arial_font14.render(resource[0] + "   " + str(resource[1]), True, DarkText)
                    screen.blit(text_panel, [232, y_base])
            else:
                y_base += 16

            # Bought resources
            y_base += 16
            text_panel = tnr_font18.render("Bought:", True, DarkText)
            screen.blit(text_panel, [232, y_base])
            y_base += 4

            # Records from last turn
            if len(game_stats.pops_details.records_bought) > 0:
                for resource in game_stats.pops_details.records_bought:
                    y_base += 16
                    text_panel = arial_font14.render(resource[0] + "   " + str(resource[1]), True, DarkText)
                    screen.blit(text_panel, [232, y_base])
            else:
                y_base += 16

            # Consumed resources
            y_base += 16
            text_panel = tnr_font18.render("Consumed:", True, DarkText)
            screen.blit(text_panel, [232, y_base])
            y_base += 4

            # Records from last turn
            if len(game_stats.pops_details.records_consumed) > 0:
                for resource in game_stats.pops_details.records_consumed:
                    y_base += 16
                    text_panel = arial_font14.render(resource[0] + "   " + str(resource[1]), True, DarkText)
                    screen.blit(text_panel, [232, y_base])

    # Local market subsection
    elif game_stats.settlement_subsection == "Local market":
        # Background
        pygame.draw.polygon(screen, FillButton,
                            [[3, 143],
                             [637, 143],
                             [637, 538],
                             [3, 538]])

        y_base = 143

        # Requested goods by population
        text_panel = tnr_font16.render("Goods sold", True, DarkText)
        screen.blit(text_panel, [5, y_base])
        y_base += 16
        text_panel = tnr_font16.render("by population:", True, DarkText)
        screen.blit(text_panel, [5, y_base])
        y_base += 20
        for res in game_stats.allocated_sold_records:
            text_panel = arial_font14.render(res[0] + "   " + str(res[1]), True, DarkText)
            screen.blit(text_panel, [5, y_base])
            y_base += 20

        y_base = 143

        # Requested goods by population
        text_panel = tnr_font16.render("Requested goods", True, DarkText)
        screen.blit(text_panel, [135, y_base])
        y_base += 16
        text_panel = tnr_font16.render("by population:", True, DarkText)
        screen.blit(text_panel, [135, y_base])
        y_base += 20
        for res in game_stats.allocated_requested_goods_records:
            text_panel = arial_font14.render(res[0] + "   " + str(res[1]), True, DarkText)
            screen.blit(text_panel, [135, y_base])
            y_base += 20

        y_base = 143

        # Requested goods by population
        text_panel = tnr_font16.render("Bought goods", True, DarkText)
        screen.blit(text_panel, [280, y_base])
        y_base += 16
        text_panel = tnr_font16.render("by population:", True, DarkText)
        screen.blit(text_panel, [280, y_base])
        y_base += 20
        for res in game_stats.allocated_bought_records:
            text_panel = arial_font14.render(res[0] + "   " + str(res[1]), True, DarkText)
            screen.blit(text_panel, [280, y_base])
            y_base += 20

        y_base = 143

        # Requested goods by population
        text_panel = tnr_font16.render("Sale offer", True, DarkText)
        screen.blit(text_panel, [410, y_base])
        y_base += 16
        text_panel = tnr_font16.render("by merchants:", True, DarkText)
        screen.blit(text_panel, [410, y_base])
        y_base += 20
        for res in settlement.previous_inner_market:
            text_panel = arial_font14.render(res[1] + "   " + str(res[2]), True, DarkText)
            screen.blit(text_panel, [410, y_base])
            y_base += 20
