## Among Myth and Wonder
## det_settlement_factions

import pygame.draw
import pygame.font

from Resources import game_stats
from Content import settlement_effects_desc

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


def draw_factions(screen, settlement):
    # Black line
    pygame.draw.line(screen, DarkText, [3, 109], [637, 109], 2)

    # Black line
    pygame.draw.line(screen, DarkText, [3, 138], [637, 138], 2)

    # Background
    pygame.draw.polygon(screen, FillButton,
                        [[3, 143],
                         [241, 143],
                         [241, 300],
                         [3, 300]])

    # pygame.draw.polygon(screen, FillButton,
    #                     [[3, 303],
    #                      [218, 303],
    #                      [218, 538],
    #                      [3, 538]])

    pygame.draw.polygon(screen, FillButton,
                        [[244, 143],
                         [400, 143],
                         [400, 538],
                         [244, 538]])

    pygame.draw.polygon(screen, FillButton,
                        [[403, 143],
                         [637, 143],
                         [637, 538],
                         [403, 538]])

    x_pos = 221
    y_pos = 303
    # Buttons - previous and next population
    pygame.draw.polygon(screen, RockTunel, [[x_pos, y_pos], [x_pos + 19, y_pos],
                                            [x_pos + 19, y_pos + 19], [x_pos, y_pos + 19]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_pos, y_pos], [x_pos + 19, y_pos],
                                                     [x_pos + 19, y_pos + 19], [x_pos, y_pos + 19]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(x_pos + 4, y_pos + 16), (x_pos + 10, y_pos + 3),
                                                          (x_pos + 16, y_pos + 16)], 2)

    pygame.draw.polygon(screen, RockTunel, [[x_pos, 517], [x_pos + 19, 517], [x_pos + 19, 536], [x_pos, 536]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_pos, 517], [x_pos + 19, 517], [x_pos + 19, 536], [x_pos, 536]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(x_pos + 4, 520), (x_pos + 10, 534), (x_pos + 16, 520)], 2)

    y_base = 143

    # Local factions
    text_panel = tnr_font20.render("Local factions", True, DarkText)
    screen.blit(text_panel, [15, y_base])
    y_base += 26

    # White line
    pygame.draw.line(screen, WhiteBorder, [5, y_base + 18 + 20 * game_stats.faction_screen_index],
                     [239, y_base + 18 + 20 * game_stats.faction_screen_index], 1)

    # Factions
    y_shift = 20
    y_points = 0
    for faction in settlement.factions:
        # Faction's loyalty
        if faction.loyalty > 0:
            icon_img = game_stats.gf_misc_img_dict["Icons/good_loyalty_icon"]
            screen.blit(icon_img, (5, y_base + y_shift * y_points))
        else:
            icon_img = game_stats.gf_misc_img_dict["Icons/bad_loyalty_icon"]
            screen.blit(icon_img, (5, y_base + y_shift * y_points))

        text_panel1 = arial_font14.render(str(faction.loyalty), True, DarkText)
        screen.blit(text_panel1, [23, y_base + y_shift * y_points])

        # Faction title
        text_panel1 = arial_font14.render(faction.title_name, True, DarkText)
        screen.blit(text_panel1, [37, y_base + y_shift * y_points])

        y_points += 1

    # Faction's population
    y_base = 306
    y_shift = 38
    y_points = 0
    num = 0
    for member in settlement.factions[game_stats.faction_screen_index].members:
        if game_stats.faction_pops_index <= num < game_stats.faction_pops_index + 6:
            # Background
            pygame.draw.polygon(screen, FillButton,
                                [[3, y_base + 1 + y_shift * y_points],
                                 [218, y_base + 1 + y_shift * y_points],
                                 [218, y_base + 35 + y_shift * y_points],
                                 [3, y_base + 35 + y_shift * y_points]])

            # Population's name
            text_panel1 = arial_font16.render(member[1], True, DarkText)
            screen.blit(text_panel1, [5, y_base + y_shift * y_points])

            # Population's location
            text_panel1 = arial_font16.render(member[3], True, DarkText)
            screen.blit(text_panel1, [5, y_base + y_shift * y_points + 17])

            y_points += 1

        num += 1

    # Control
    y_base = 143

    # Culture
    icon_img = game_stats.gf_misc_img_dict["Icons/masks"]
    screen.blit(icon_img, (248, y_base + 1))

    text_panel = tnr_font20.render("Culture", True, DarkText)
    screen.blit(text_panel, [275, y_base])
    y_base += 26

    y_shift = 20
    y_points = 0
    for culture in settlement.control:
        # Faction title
        text_panel1 = arial_font14.render(str(culture[1]) + " " + culture[0], True, DarkText)
        screen.blit(text_panel1, [248, y_base + y_shift * y_points])

        y_points += 1

    # Settlement effects
    y_base = 143

    text_panel = tnr_font20.render("Province effects", True, DarkText)
    screen.blit(text_panel, [407, y_base])
    y_base += 26

    y_shift = 18
    y_points = 0
    for effect in settlement.local_effects:
        # Description
        for text_line in settlement_effects_desc.desc_catalog[effect.name]:
            text_panel1 = arial_font14.render(text_line, True, DarkText)
            screen.blit(text_panel1, [407, y_base + y_shift * y_points])

            y_points += 1

        y_points += 1