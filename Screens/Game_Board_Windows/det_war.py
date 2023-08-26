## Miracle battles!
## det_war

import math
import pygame.draw
import pygame.font

from Resources import game_stats

LineMainMenuColor1 = [0x60, 0x60, 0x60]

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]

FillButton = [0xD8, 0xBD, 0xA2]
ApproveFieldColor = [0x00, 0x99, 0x00]
ApproveElementsColor = [0x00, 0x66, 0x00]

# Fonts
font16 = pygame.font.SysFont('timesnewroman', 16)
font14 = pygame.font.SysFont('timesnewroman', 14)

ScarletColor = [0xFF, 0x24, 0x00]
CopperColor = [0xE9, 0x75, 0x00]
NightBlueColor = [0x19, 0x2F, 0xF0]
MoonColor = [0xD2, 0xD6, 0xFA]
BullBrownColor = [0x40, 0x21, 0x02]
BlackHoovesColor = [0x0A, 0x06, 0x02]
RoyalPurple = [0x8B, 0x00, 0x8B]
GoldColor = [0xFF, 0xD7, 0x00]
TribesTide = [0x00, 0x64, 0x00]
ForestGreen = [0x22, 0x8B, 0x22]
MaroonColor = [0x80, 0x00, 0x00]
SlateGray = [0x70, 0x80, 0x90]

FlagColors = {"Scarlet": ScarletColor,
              "Copper": CopperColor,
              "NightBlue": NightBlueColor,
              "Moon": MoonColor,
              "BullBrown": BullBrownColor,
              "BlackHooves": BlackHoovesColor,
              "RoyalPurple": RoyalPurple,
              "GoldColor": GoldColor,
              "TribesTide": TribesTide,
              "ForestGreen": ForestGreen,
              "MaroonColor": MaroonColor,
              "SlateGray": SlateGray}


def draw_war(screen):
    war = game_stats.war_inspection
    at = game_stats.realm_inspection  # Realm that declared the war
    df = game_stats.contact_inspection  # Realm that was attacked

    ## Initiator
    # pygame.draw.polygon(screen, FieldColor2,
    #                     [[39, 165], [269, 165], [269, 316], [39, 316]])

    # Flag
    x = 41
    y = 83
    pygame.draw.polygon(screen, FlagColors[at.f_color],
                        [[x, y], [x + 22, y],
                         [x + 22, y + 8], [x, y + 8]])
    pygame.draw.polygon(screen, FlagColors[at.s_color],
                        [[x, y + 9], [x + 22, y + 9],
                         [x + 22, y + 16], [x, y + 16]])

    text_panel = font16.render(at.name, True, TitleText)
    screen.blit(text_panel, [68, 83])

    icon_img = game_stats.gf_misc_img_dict["Icons/masks"]
    screen.blit(icon_img, (42, 102))

    text_panel = font16.render(at.alignment, True, TitleText)
    screen.blit(text_panel, [68, 105])

    icon_img = game_stats.gf_misc_img_dict["Icons/crown_bigger"]
    screen.blit(icon_img, (39, 125))

    text_panel = font16.render(at.leader.name, True, TitleText)
    screen.blit(text_panel, [68, 129])

    if len(at.leader.behavior_traits) > 0:
        text_panel = font14.render(at.leader.behavior_traits[0], True, DarkText)
        screen.blit(text_panel, [42, 148])

        if len(at.leader.behavior_traits) > 1:
            text_panel = font14.render(at.leader.behavior_traits[1], True, DarkText)
            screen.blit(text_panel, [145, 148])

    ## Central column
    x_base = 281

    text_panel = font16.render("Duration " + str(war.war_duration), True, DarkText)
    screen.blit(text_panel, [x_base, 83])

    text_panel = font16.render("War enthusiasm", True, TitleText)
    screen.blit(text_panel, [x_base, 102])

    x = 281
    y_base = 121
    y_shift = 17
    y_num = 0

    y = y_base + y_shift * y_num + 3
    pygame.draw.polygon(screen, FlagColors[at.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[at.s_color],
                        [[x, y + 7], [x + 16, y + 7],
                         [x + 16, y + 12], [x, y + 12]])

    # Progress bar
    max_we = game_stats.war_summary.max_war_enthusiasm
    x = x_base + 19
    accumulated_we = game_stats.war_summary.own_realm_war_enthusiasm
    xVar = int(accumulated_we / max_we * 90)
    if accumulated_we > max_we:
        xVar = 90
    pygame.draw.polygon(screen, ApproveFieldColor,
                        [[x, y], [x + xVar, y], [x + xVar, y + 12], [x, y + 12]])
    pygame.draw.polygon(screen, ApproveElementsColor,
                        [[x, y], [x + 90, y], [x + 90, y + 12], [x, y + 12]], 1)

    text_panel = font14.render(str(accumulated_we) + "/" + str(max_we), True, DarkText)
    screen.blit(text_panel, [x_base + 113, y_base + y_shift * y_num + 1])

    y_num += 1
    y = y_base + y_shift * y_num + 3
    x = 281
    pygame.draw.polygon(screen, FlagColors[df.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[df.s_color],
                        [[x, y + 7], [x + 16, y + 7],
                         [x + 16, y + 12], [x, y + 12]])

    # Progress bar
    x = x_base + 19
    accumulated_we = game_stats.war_summary.opponent_war_enthusiasm
    xVar = int(accumulated_we / max_we * 90)
    pygame.draw.polygon(screen, ApproveFieldColor,
                        [[x, y], [x + xVar, y], [x + xVar, y + 12], [x, y + 12]])
    pygame.draw.polygon(screen, ApproveElementsColor,
                        [[x, y], [x + 90, y], [x + 90, y + 12], [x, y + 12]], 1)

    text_panel = font14.render(str(accumulated_we) + "/" + str(max_we), True, DarkText)
    screen.blit(text_panel, [x_base + 113, y_base + y_shift * y_num + 1])
    y_num += 1

    text_panel = font16.render("Battle victories", True, TitleText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    y = y_base + y_shift * y_num + 3
    x = x_base
    pygame.draw.polygon(screen, FlagColors[at.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[at.s_color],
                        [[x, y + 7], [x + 16, y + 7],
                         [x + 16, y + 12], [x, y + 12]])

    orbv = game_stats.war_summary.own_realm_battle_victories
    obv = game_stats.war_summary.opponent_battle_victories
    perc = 0.00
    if orbv + obv != 0:
        perc = math.floor((orbv / (orbv + obv)) * 100)
    text_panel = font14.render(str(orbv) + "  (" + str(perc) + "%) victories", True, DarkText)
    screen.blit(text_panel, [x_base + 27, y_base + y_shift * y_num + 1])
    y_num += 1

    y = y_base + y_shift * y_num + 3
    x = x_base
    pygame.draw.polygon(screen, FlagColors[df.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[df.s_color],
                        [[x, y + 7], [x + 16, y + 7],
                         [x + 16, y + 12], [x, y + 12]])

    orbv = game_stats.war_summary.own_realm_battle_victories
    obv = game_stats.war_summary.opponent_battle_victories
    perc = 0.00
    if orbv + obv != 0:
        perc = math.floor((obv / (orbv + obv)) * 100)
    text_panel = font14.render(str(obv) + "  (" + str(perc) + "%) victories", True, DarkText)
    screen.blit(text_panel, [x_base + 27, y_base + y_shift * y_num + 1])
    y_num += 1

    text_panel = font16.render("Captured provinces:", True, TitleText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    y = y_base + y_shift * y_num + 3
    x = x_base
    pygame.draw.polygon(screen, FlagColors[at.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[at.s_color],
                        [[x, y + 7], [x + 16, y + 7],
                         [x + 16, y + 12], [x, y + 12]])

    captured_provinces = game_stats.war_summary.own_realm_captured_provinces
    text_panel = font14.render(str(captured_provinces) + " provinces", True, DarkText)
    screen.blit(text_panel, [x_base + 27, y_base + y_shift * y_num + 1])
    y_num += 1

    y = y_base + y_shift * y_num + 3
    x = x_base
    pygame.draw.polygon(screen, FlagColors[df.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[df.s_color],
                        [[x, y + 7], [x + 16, y + 7],
                         [x + 16, y + 12], [x, y + 12]])

    captured_provinces = game_stats.war_summary.opponent_captured_provinces
    text_panel = font14.render(str(captured_provinces) + " provinces", True, DarkText)
    screen.blit(text_panel, [x_base + 27, y_base + y_shift * y_num + 1])
    y_num += 1

    # Button - Sue for peace
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y], [x_base + 114, y],
                         [x_base + 114, y + 15], [x_base, y + 15]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y], [x_base + 114, y],
                                                     [x_base + 114, y + 15], [x_base, y + 15]], 2)

    text_panel1 = font14.render("Sue for peace", True, DarkText)
    screen.blit(text_panel1, [x_base + 21, y])

    ## Respondent
    # pygame.draw.polygon(screen, FieldColor2,
    #                     [[444, 165], [674, 165], [674, 316], [444, 316]])

    # Flag
    x = 446
    y = 83
    pygame.draw.polygon(screen, FlagColors[df.f_color],
                        [[x, y], [x + 22, y],
                         [x + 22, y + 8], [x, y + 8]])
    pygame.draw.polygon(screen, FlagColors[df.s_color],
                        [[x, y + 9], [x + 22, y + 9],
                         [x + 22, y + 16], [x, y + 16]])

    text_panel = font16.render(df.name, True, TitleText)
    screen.blit(text_panel, [473, 83])

    icon_img = game_stats.gf_misc_img_dict["Icons/masks"]
    screen.blit(icon_img, (446, 102))

    text_panel = font16.render(df.alignment, True, TitleText)
    screen.blit(text_panel, [473, 105])

    icon_img = game_stats.gf_misc_img_dict["Icons/crown_bigger"]
    screen.blit(icon_img, (444, 125))

    text_panel = font16.render(df.leader.name, True, TitleText)
    screen.blit(text_panel, [473, 129])

    if len(df.leader.behavior_traits) > 0:
        text_panel = font14.render(df.leader.behavior_traits[0], True, DarkText)
        screen.blit(text_panel, [444, 148])

        if len(df.leader.behavior_traits) > 1:
            text_panel = font14.render(df.leader.behavior_traits[1], True, DarkText)
            screen.blit(text_panel, [550, 148])
