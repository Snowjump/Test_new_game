## Among Myth and Wonder

import math

import pygame.draw
import pygame.font

from Resources import game_stats

WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]

FillButton = [0xD8, 0xBD, 0xA2]
ApproveFieldColor = [0x00, 0x99, 0x00]
ApproveElementsColor = [0x00, 0x66, 0x00]
CancelElementsColor = [0x99, 0x00, 0x00]
FieldColor2 = [0xBE, 0xB0, 0xA2]

RockTunel = [0x89, 0x89, 0x89]

HighlightOption = [0x00, 0xCC, 0xCC]

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

# Fonts
font16 = pygame.font.SysFont('timesnewroman', 16)
font14 = pygame.font.SysFont('timesnewroman', 14)


def area_management(screen, power):
    ## Own realm's diplomatic relations
    draw_own_realm_s_diplomatic_relations(screen, power)

    ## Contacted realms
    draw_contacted_realms(screen, power)

    ## Selected realm's diplomatic relations
    draw_selected_realms_diplomatic_relations(screen)

    if game_stats.diplomacy_area == "Diplomatic actions" and game_stats.contact_inspection is not None:
        ## Diplomatic actions
        draw_diplomatic_actions(screen, power)

    elif game_stats.diplomacy_area == "Declaration of war":
        ## Declaration of war
        draw_declaration_of_war(screen)

    elif game_stats.diplomacy_area == "Sue for peace":
        ## Ongoing war
        draw_sue_for_peace(screen, power)

    elif game_stats.diplomacy_area == "Draft a peace offer":
        ## Draft a peace offer
        draw_draft_a_peace_offer(screen, power)

    elif game_stats.diplomacy_area == "Threaten":
        ## Threaten a realm
        draw_threaten(screen, power)


def draw_own_realm_s_diplomatic_relations(screen, power):
    ## Own realm's diplomatic relations
    pygame.draw.polygon(screen, FieldColor2,
                        [[39, 165], [269, 165], [269, 316], [39, 316]])

    # Flag
    x = 41
    y = 83
    pygame.draw.polygon(screen, FlagColors[power.f_color],
                        [[x, y], [x + 22, y],
                         [x + 22, y + 8], [x, y + 8]])
    pygame.draw.polygon(screen, FlagColors[power.s_color],
                        [[x, y + 9], [x + 22, y + 9],
                         [x + 22, y + 16], [x, y + 16]])

    text_panel = font16.render(power.name, True, TitleText)
    screen.blit(text_panel, [68, 83])

    icon_img = game_stats.gf_misc_img_dict["Icons/masks"]
    screen.blit(icon_img, (42, 102))

    text_panel = font16.render(power.alignment, True, TitleText)
    screen.blit(text_panel, [68, 105])

    icon_img = game_stats.gf_misc_img_dict["Icons/crown_bigger"]
    screen.blit(icon_img, (39, 125))

    text_panel = font16.render(power.leader.name, True, TitleText)
    screen.blit(text_panel, [68, 129])

    if len(power.leader.behavior_traits) > 0:
        text_panel = font14.render(power.leader.behavior_traits[0], True, DarkText)
        screen.blit(text_panel, [42, 148])

        if len(power.leader.behavior_traits) > 1:
            text_panel = font14.render(power.leader.behavior_traits[1], True, DarkText)
            screen.blit(text_panel, [145, 148])

    # Relations
    icon_img = game_stats.gf_misc_img_dict["Icons/sword_and_axe_icon_14_x_12"]
    screen.blit(icon_img, (41, 166))

    x_base = 59
    x_shift = 14
    x_num = 0
    y_base = 166
    y_shift = 14
    y_num = 0
    if len(power.relations.at_war) > 14:
        x_shift = (14 * 14) / len(power.relations.at_war)
    for realm in power.relations.at_war:
        # print("realm - " + str(power.name))
        # print("diplomacy_panel - " + str(realm[0]) + " " + str(realm[1]) + " " + str(realm[2]))
        pygame.draw.polygon(screen, FlagColors[realm[0]],
                            [[x_base + x_shift * x_num, y_base + y_shift * y_num + 1],
                             [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 1],
                             [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 6],
                             [x_base + x_shift * x_num, y_base + y_shift * y_num + 6]])
        pygame.draw.polygon(screen, FlagColors[realm[1]],
                            [[x_base + x_shift * x_num, y_base + y_shift * y_num + 7],
                             [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 7],
                             [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 11],
                             [x_base + x_shift * x_num, y_base + y_shift * y_num + 11]])

        # pygame.draw.polygon(screen, FlagColors[realm[0]],
        #                     [[x_base + x_shift * x_num, y_base + y_shift * y_num + 30],
        #                      [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 30],
        #                      [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 76],
        #                      [x_base + x_shift * x_num, y_base + y_shift * y_num + 76]])

        x_num += 1

    y_num += 1


def draw_contacted_realms(screen, power):
    ## Contacted realms
    pygame.draw.polygon(screen, FieldColor2,
                        [[274, 108], [439, 108], [439, 316], [274, 316]])

    text_panel = font16.render("Contacted realms", True, TitleText)
    screen.blit(text_panel, [276, 83])

    # List of contacts
    x = 276
    y_base = 110
    y_shift = 16
    y_num = 0
    for realm_num in range(0, 13):
        if realm_num + game_stats.contact_index + 1 <= len(game_stats.explored_contacts):
            realm = game_stats.explored_contacts[realm_num + game_stats.contact_index]
            pygame.draw.polygon(screen, FlagColors[realm[0]],
                                [[x, y_base + y_shift * y_num], [x + 16, y_base + y_shift * y_num],
                                 [x + 16, y_base + y_shift * y_num + 6], [x, y_base + y_shift * y_num + 6]])
            pygame.draw.polygon(screen, FlagColors[realm[1]],
                                [[x, y_base + y_shift * y_num + 7], [x + 16, y_base + y_shift * y_num + 7],
                                 [x + 16, y_base + y_shift * y_num + 12], [x, y_base + y_shift * y_num + 12]])

            text_panel = font14.render(realm[2], True, DarkText)
            screen.blit(text_panel, [296, y_base + y_shift * y_num - 1])

            y_num += 1

    # Buttons - previous and next established contacts
    x_base = 422
    x_shift = 15
    y_base = 109
    y_shift = 15
    pygame.draw.polygon(screen, RockTunel, [[x_base, y_base], [x_base + x_shift, y_base],
                                            [x_base + x_shift, y_base + y_shift], [x_base, y_base + y_shift]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_shift, y_base],
                                                     [x_base + x_shift, y_base + y_shift],
                                                     [x_base, y_base + y_shift]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(x_base + 3, y_base + 13),
                                                          (x_base + 7, y_base + 3),
                                                          (x_base + 12, y_base + 13)], 2)

    y_base = 299
    pygame.draw.polygon(screen, RockTunel, [[x_base, y_base], [x_base + x_shift, y_base],
                                            [x_base + x_shift, y_base + y_shift], [x_base, y_base + y_shift]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_shift, y_base],
                                                     [x_base + x_shift, y_base + y_shift],
                                                     [x_base, y_base + y_shift]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(x_base + 3, y_base + 3),
                                                          (x_base + 7, y_base + 13),
                                                          (x_base + 12, y_base + 3)], 2)


def draw_selected_realms_diplomatic_relations(screen):
    ## Selected realm's diplomatic relations
    pygame.draw.polygon(screen, FieldColor2,
                        [[444, 165], [674, 165], [674, 316], [444, 316]])

    if game_stats.contact_inspection is not None:
        # Flag
        x = 446
        y = 83
        pygame.draw.polygon(screen, FlagColors[game_stats.contact_inspection.f_color],
                            [[x, y], [x + 22, y],
                             [x + 22, y + 8], [x, y + 8]])
        pygame.draw.polygon(screen, FlagColors[game_stats.contact_inspection.s_color],
                            [[x, y + 9], [x + 22, y + 9],
                             [x + 22, y + 16], [x, y + 16]])

        text_panel = font16.render(game_stats.contact_inspection.name, True, TitleText)
        screen.blit(text_panel, [473, 83])

        icon_img = game_stats.gf_misc_img_dict["Icons/masks"]
        screen.blit(icon_img, (446, 102))

        text_panel = font16.render(game_stats.contact_inspection.alignment, True, TitleText)
        screen.blit(text_panel, [473, 105])

        icon_img = game_stats.gf_misc_img_dict["Icons/crown_bigger"]
        screen.blit(icon_img, (444, 125))

        text_panel = font16.render(game_stats.contact_inspection.leader.name, True, TitleText)
        screen.blit(text_panel, [473, 129])

        if len(game_stats.contact_inspection.leader.behavior_traits) > 0:
            text_panel = font14.render(game_stats.contact_inspection.leader.behavior_traits[0], True, DarkText)
            screen.blit(text_panel, [444, 148])

            if len(game_stats.contact_inspection.leader.behavior_traits) > 1:
                text_panel = font14.render(game_stats.contact_inspection.leader.behavior_traits[1], True, DarkText)
                screen.blit(text_panel, [550, 148])

        # Relations
        icon_img = game_stats.gf_misc_img_dict["Icons/sword_and_axe_icon_14_x_12"]
        screen.blit(icon_img, (445, 166))

        x_base = 464
        x_shift = 14
        x_num = 0
        y_base = 166
        y_shift = 14
        y_num = 0
        if len(game_stats.contact_inspection.relations.at_war) > 14:
            x_shift = (14 * 14) / len(game_stats.contact_inspection.relations.at_war)
        for realm in game_stats.contact_inspection.relations.at_war:
            pygame.draw.polygon(screen, FlagColors[realm[0]],
                                [[x_base + x_shift * x_num, y_base + y_shift * y_num + 1],
                                 [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 1],
                                 [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 6],
                                 [x_base + x_shift * x_num, y_base + y_shift * y_num + 6]])
            pygame.draw.polygon(screen, FlagColors[realm[1]],
                                [[x_base + x_shift * x_num, y_base + y_shift * y_num + 7],
                                 [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 7],
                                 [x_base + x_shift * x_num + 12, y_base + y_shift * y_num + 11],
                                 [x_base + x_shift * x_num, y_base + y_shift * y_num + 11]])
            x_num += 1

        y_num += 1


def draw_diplomatic_actions(screen, power):
    ## Diplomatic actions
    pygame.draw.polygon(screen, FieldColor2,
                        [[39, 319], [414, 319], [414, 538], [39, 538]])

    x_base = 41
    x_wide = 100
    y_base = 321
    y_height = 15
    y_shift = 19
    y_num = 0

    # Declare war or sue for peace
    y = y_base + y_shift * y_num
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y], [x_base + x_wide, y],
                         [x_base + x_wide, y + y_height], [x_base, y + y_height]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y], [x_base + x_wide, y],
                                                     [x_base + x_wide, y + y_height], [x_base, y + y_height]], 2)

    if game_stats.dip_summary.ongoing_war:
        text_panel1 = font14.render("Sue for peace", True, DarkText)
        screen.blit(text_panel1, [x_base + 13, y])
    else:
        text_panel1 = font14.render("Declare war", True, DarkText)
        screen.blit(text_panel1, [x_base + 17, y])

    y_num += 1

    # Threaten
    color = LineMainMenuColor1
    if game_stats.dip_summary.ongoing_war:
        color = CancelElementsColor

    y = y_base + y_shift * y_num
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y], [x_base + x_wide, y],
                         [x_base + x_wide, y + y_height], [x_base, y + y_height]])
    pygame.draw.polygon(screen, color, [[x_base, y], [x_base + x_wide, y],
                                        [x_base + x_wide, y + y_height], [x_base, y + y_height]], 2)

    text_panel1 = font14.render("Threaten", True, DarkText)
    screen.blit(text_panel1, [x_base + 27, y])

    y_num += 1

    ## Diplomatic relations with selected realm
    pygame.draw.polygon(screen, FieldColor2,
                        [[419, 319], [674, 319], [674, 538], [419, 538]])


def draw_declaration_of_war(screen):
    ## Declaration of war
    pygame.draw.polygon(screen, FieldColor2,
                        [[39, 319], [674, 319], [674, 538], [39, 538]])

    # Return back
    pygame.draw.polygon(screen, FillButton,
                        [[117, 535 - 15], [117 + 99, 535 - 15],
                         [117 + 99, 535], [117, 535]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[117, 535 - 15], [117 + 99, 535 - 15],
                                                     [117 + 99, 535], [117, 535]], 2)

    text_panel1 = font14.render("Return back", True, DarkText)
    screen.blit(text_panel1, [117 + 18, 535 - 15])

    # Declare war
    color1 = CancelElementsColor
    if game_stats.war_goals:
        color1 = HighlightOption
    pygame.draw.polygon(screen, FillButton,
                        [[457, 535 - 15], [457 + 99, 535 - 15],
                         [457 + 99, 535], [457, 535]])
    pygame.draw.polygon(screen, color1, [[457, 535 - 15], [457 + 99, 535 - 15],
                                         [457 + 99, 535], [457, 535]], 2)

    text_panel1 = font14.render("Declare war", True, DarkText)
    screen.blit(text_panel1, [457 + 18, 535 - 15])

    ## Casus belli
    text_panel = font16.render("Select a casus belli:", True, TitleText)
    screen.blit(text_panel, [41, 321])

    x_base = 41
    y_base = 339
    y_shift = 17
    y_num = 0
    for cb in game_stats.casus_bellis:
        text_panel = font16.render(cb, True, DarkText)
        screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
        y_num += 1

    pygame.draw.line(screen, MainMenuColor, [166, 341], [166, 515], 2)

    text_panel = font16.render("Details:", True, TitleText)
    screen.blit(text_panel, [171, 321])

    if game_stats.cb_details:
        x_base = 171
        y_base = 339
        y_shift = 17
        y_num = 0
        for item in game_stats.cb_details:
            icon_img = game_stats.gf_misc_img_dict["Icons/accept_icon"]
            screen.blit(icon_img, (x_base, y_base + y_shift * y_num + 2))

            text_panel = font16.render(item[0], True, DarkText)
            screen.blit(text_panel, [x_base + 17, y_base + y_shift * y_num])
            y_num += 1

    pygame.draw.line(screen, MainMenuColor, [296, 341], [296, 515], 2)

    text_panel = font16.render("Declared war goals:", True, TitleText)
    screen.blit(text_panel, [301, 321])

    if game_stats.war_goals:
        x_base = 301
        y_base = 339
        y_shift = 17
        y_num = 0
        cb = None
        for goal in game_stats.war_goals:
            if cb is None:
                text_panel = font16.render(goal[2], True, DarkText)
                screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
                y_num += 1
                cb = goal[2]

            elif cb != goal[2]:
                text_panel = font16.render(goal[2], True, DarkText)
                screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
                y_num += 1
                cb = goal[2]

            icon_img = game_stats.gf_misc_img_dict["Icons/cancel_icon"]
            screen.blit(icon_img, (x_base, y_base + y_shift * y_num + 2))

            text_panel = font16.render(goal[0], True, DarkText)
            screen.blit(text_panel, [x_base + 17, y_base + y_shift * y_num])
            y_num += 1


def draw_sue_for_peace(screen, power):
    ## Ongoing war
    pygame.draw.polygon(screen, FieldColor2,
                        [[39, 319], [674, 319], [674, 538], [39, 538]])

    ## Objectives
    x_base = 41
    x = 58

    text_panel = font16.render("Objectives:", True, TitleText)
    screen.blit(text_panel, [x_base, 320])

    y_base = 339
    y_shift = 17
    y_num = 0

    for goal in game_stats.war_summary.war_goals:
        icon_img = game_stats.gf_misc_img_dict[goal[1]]
        screen.blit(icon_img, (x_base, y_base + y_shift * y_num + 2))

        y = y_base + y_shift * y_num + 3

        pygame.draw.polygon(screen, FlagColors[goal[3]],
                            [[x, y], [x + 16, y],
                             [x + 16, y + 6], [x, y + 6]])
        pygame.draw.polygon(screen, FlagColors[goal[4]],
                            [[x, y + 7], [x + 16, y + 7],
                             [x + 16, y + 12], [x, y + 12]])

        text_panel = font14.render("(" + str(goal[5]) + ") " + goal[6], True, DarkText)
        screen.blit(text_panel, [x_base + 37, y_base + y_shift * y_num + 1])
        y_num += 1

    pygame.draw.line(screen, MainMenuColor, [231, 341], [231, 515], 2)

    ## War progress
    x_base = 236
    text_panel = font16.render("War enthusiasm", True, TitleText)
    screen.blit(text_panel, [x_base, 320])

    x = 236
    y_base = 339
    y_shift = 17
    y_num = 0

    y = y_base + y_shift * y_num + 3
    pygame.draw.polygon(screen, FlagColors[power.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[power.s_color],
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
    x = 236
    pygame.draw.polygon(screen, FlagColors[game_stats.contact_inspection.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[game_stats.contact_inspection.s_color],
                        [[x, y + 7], [x + 16, y + 7],
                         [x + 16, y + 12], [x, y + 12]])

    # Progress bar
    x = x_base + 19
    accumulated_we = game_stats.war_summary.opponent_war_enthusiasm
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

    text_panel = font16.render("Battle victories", True, TitleText)
    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
    y_num += 1

    y = y_base + y_shift * y_num + 3
    x = x_base
    pygame.draw.polygon(screen, FlagColors[power.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[power.s_color],
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
    pygame.draw.polygon(screen, FlagColors[game_stats.contact_inspection.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[game_stats.contact_inspection.s_color],
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
    pygame.draw.polygon(screen, FlagColors[power.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[power.s_color],
                        [[x, y + 7], [x + 16, y + 7],
                         [x + 16, y + 12], [x, y + 12]])

    captured_provinces = game_stats.war_summary.own_realm_captured_provinces
    text_panel = font14.render(str(captured_provinces) + " provinces", True, DarkText)
    screen.blit(text_panel, [x_base + 27, y_base + y_shift * y_num + 1])
    y_num += 1

    y = y_base + y_shift * y_num + 3
    x = x_base
    pygame.draw.polygon(screen, FlagColors[game_stats.contact_inspection.f_color],
                        [[x, y], [x + 16, y],
                         [x + 16, y + 6], [x, y + 6]])
    pygame.draw.polygon(screen, FlagColors[game_stats.contact_inspection.s_color],
                        [[x, y + 7], [x + 16, y + 7],
                         [x + 16, y + 12], [x, y + 12]])

    captured_provinces = game_stats.war_summary.opponent_captured_provinces
    text_panel = font14.render(str(captured_provinces) + " provinces", True, DarkText)
    screen.blit(text_panel, [x_base + 27, y_base + y_shift * y_num + 1])
    y_num += 1

    pygame.draw.line(screen, MainMenuColor, [396, 341], [396, 515], 2)

    ## Buttons
    x_base = 401
    x = 401
    y_base = 339
    y_shift = 20
    y_num = 0

    y = y_base + y_shift * y_num

    # Return back
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y], [x_base + 114, y],
                         [x_base + 114, y + 15], [x_base, y + 15]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y], [x_base + 114, y],
                                                     [x_base + 114, y + 15], [x_base, y + 15]], 2)

    text_panel1 = font14.render("Return back", True, DarkText)
    screen.blit(text_panel1, [x_base + 24, y])
    y_num += 1

    # Draft a peace offer
    y = y_base + y_shift * y_num
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y], [x_base + 114, y],
                         [x_base + 114, y + 15], [x_base, y + 15]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y], [x_base + 114, y],
                                                     [x_base + 114, y + 15], [x_base, y + 15]], 2)

    text_panel1 = font14.render("Draft a peace offer", True, DarkText)
    screen.blit(text_panel1, [x_base + 4, y])
    y_num += 1


def draw_draft_a_peace_offer(screen, power):
    ## Draft a peace offer
    pygame.draw.polygon(screen, FieldColor2,
                        [[39, 319], [674, 319], [674, 538], [39, 538]])

    # Return back
    pygame.draw.polygon(screen, FillButton,
                        [[117, 535 - 15], [117 + 99, 535 - 15],
                         [117 + 99, 535], [117, 535]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[117, 535 - 15], [117 + 99, 535 - 15],
                                                     [117 + 99, 535], [117, 535]], 2)

    text_panel1 = font14.render("Return back", True, DarkText)
    screen.blit(text_panel1, [117 + 18, 535 - 15])

    # Change between making demands or concessions
    text_line = "Make concessions"
    x3 = 6
    if game_stats.make_demands:
        pass
    else:
        text_line = "Make demands"
        x3 = 14

    x1 = 256
    x2 = 110
    pygame.draw.polygon(screen, FillButton,
                        [[x1, 535 - 15], [x1 + x2, 535 - 15],
                         [x1 + x2, 535], [x1, 535]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x1, 535 - 15], [x1 + x2, 535 - 15],
                                                     [x1 + x2, 535], [x1, 535]], 2)

    text_panel1 = font14.render(text_line, True, DarkText)
    screen.blit(text_panel1, [x1 + x3, 535 - 15])

    # Propose peace
    text_line = "Propose peace agreement"
    color1 = CancelElementsColor
    x3 = 4
    if game_stats.claimed_demands:
        if game_stats.will_accept_peace_agreement:
            color1 = HighlightOption
    else:
        text_line = "Propose white peace"
        x3 = 18
        if game_stats.will_accept_white_peace:
            color1 = HighlightOption

    x1 = 407
    x2 = 149
    pygame.draw.polygon(screen, FillButton,
                        [[x1, 535 - 15], [x1 + x2, 535 - 15],
                         [x1 + x2, 535], [x1, 535]])
    pygame.draw.polygon(screen, color1, [[x1, 535 - 15], [x1 + x2, 535 - 15],
                                         [x1 + x2, 535], [x1, 535]], 2)

    text_panel1 = font14.render(text_line, True, DarkText)
    screen.blit(text_panel1, [x1 + x3, 535 - 15])

    if game_stats.make_demands:
        ## Make demands
        ## Select a demand
        text_panel = font16.render("Select a demand:", True, TitleText)
        screen.blit(text_panel, [41, 321])

        x_base = 41
        y_base = 339
        y_shift = 17
        y_num = 0
        for demand in game_stats.peace_demands:
            text_panel = font16.render(demand, True, DarkText)
            screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
            y_num += 1

        pygame.draw.line(screen, MainMenuColor, [166, 341], [166, 515], 2)

        text_panel = font16.render("Details:", True, TitleText)
        screen.blit(text_panel, [171, 321])

        ## Demand details
        if game_stats.demand_details:
            x_base = 171
            y_base = 339
            y_shift = 17
            y_num = 0
            for item in game_stats.demand_details:
                y = y_base + y_shift * y_num

                icon_img = game_stats.gf_misc_img_dict["Icons/accept_icon"]
                screen.blit(icon_img, (x_base, y + 2))

                if item[1] is not None:
                    # if item[1] == "Icons/captured_province":
                    icon_img = game_stats.gf_misc_img_dict[item[1]]
                    screen.blit(icon_img, (x_base + 17, y + 2))

                text_panel = font16.render(item[2], True, DarkText)
                screen.blit(text_panel, [x_base + 35, y])
                y_num += 1

        pygame.draw.line(screen, MainMenuColor, [336, 341], [336, 515], 2)

        text_panel = font16.render("Demands:", True, TitleText)
        screen.blit(text_panel, [341, 321])

        if game_stats.claimed_demands:
            x_base = 341
            y_base = 339
            y_shift = 17
            y_num = 0
            cb = None
            for demand in game_stats.claimed_demands:
                if cb is None:
                    text_panel = font16.render(demand[0], True, DarkText)
                    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
                    y_num += 1
                    cb = demand[0]

                elif cb != demand[0]:
                    text_panel = font16.render(demand[0], True, DarkText)
                    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
                    y_num += 1
                    cb = demand[0]

                icon_img = game_stats.gf_misc_img_dict["Icons/cancel_icon"]
                screen.blit(icon_img, (x_base, y_base + y_shift * y_num + 2))

                text_panel = font16.render(demand[2], True, DarkText)
                screen.blit(text_panel, [x_base + 17, y_base + y_shift * y_num])
                y_num += 1

        pygame.draw.line(screen, MainMenuColor, [486, 341], [486, 515], 2)

    else:
        ## Make concessions
        ## Select a concession
        text_panel = font16.render("Select a concession:", True, TitleText)
        screen.blit(text_panel, [41, 321])

        x_base = 41
        y_base = 339
        y_shift = 17
        y_num = 0
        for concession in game_stats.peace_demands:
            text_panel = font16.render(concession, True, DarkText)
            screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
            y_num += 1

        pygame.draw.line(screen, MainMenuColor, [166, 341], [166, 515], 2)

        text_panel = font16.render("Details:", True, TitleText)
        screen.blit(text_panel, [171, 321])

        ## Concession details
        if game_stats.demand_details:
            x_base = 171
            y_base = 339
            y_shift = 17
            y_num = 0
            for item in game_stats.demand_details:
                y = y_base + y_shift * y_num

                icon_img = game_stats.gf_misc_img_dict["Icons/accept_icon"]
                screen.blit(icon_img, (x_base, y + 2))

                if item[1] is not None:
                    if item[1] == "Icons/captured_province":
                        icon_img = game_stats.gf_misc_img_dict[item[1]]
                        screen.blit(icon_img, (x_base + 18, y + 2))

                text_panel = font16.render(item[2], True, DarkText)
                screen.blit(text_panel, [x_base + 34, y])
                y_num += 1

        pygame.draw.line(screen, MainMenuColor, [336, 341], [336, 515], 2)

        text_panel = font16.render("Concessions:", True, TitleText)
        screen.blit(text_panel, [341, 321])

        if game_stats.claimed_demands:
            x_base = 341
            y_base = 339
            y_shift = 17
            y_num = 0
            cb = None
            for concession in game_stats.claimed_demands:
                if cb is None:
                    text_panel = font16.render(concession[0], True, DarkText)
                    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
                    y_num += 1
                    cb = concession[0]

                elif cb != concession[0]:
                    text_panel = font16.render(concession[0], True, DarkText)
                    screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
                    y_num += 1
                    cb = concession[0]

                icon_img = game_stats.gf_misc_img_dict["Icons/cancel_icon"]
                screen.blit(icon_img, (x_base, y_base + y_shift * y_num + 2))

                text_panel = font16.render(concession[2], True, DarkText)
                screen.blit(text_panel, [x_base + 17, y_base + y_shift * y_num])
                y_num += 1

        pygame.draw.line(screen, MainMenuColor, [486, 341], [486, 515], 2)

    if game_stats.claimed_demands:
        if game_stats.make_demands:
            ## Make demands
            # Peace agreement proposition
            # Declare victory
            text_panel = font16.render("Victory", True, TitleText)
            screen.blit(text_panel, [491, 321])
            text_panel = font14.render("Acceptance:", True, DarkText)
            screen.blit(text_panel, [491, 339])

            y_base = 356
            y_shift = 16
            y_num = 0
            for text_line in game_stats.peace_offer_text:
                text_panel = font14.render(text_line, True, DarkText)
                screen.blit(text_panel, [491, y_base + y_shift * y_num])
                y_num += 1

        else:
            ## Make concessions
            # Peace agreement proposition
            # Declare capitulation
            text_panel = font16.render("Capitulation", True, TitleText)
            screen.blit(text_panel, [491, 321])
            text_panel = font14.render("Acceptance:", True, DarkText)
            screen.blit(text_panel, [491, 339])

            y_base = 356
            y_shift = 16
            y_num = 0
            for text_line in game_stats.peace_offer_text:
                text_panel = font14.render(text_line, True, DarkText)
                screen.blit(text_panel, [491, y_base + y_shift * y_num])
                y_num += 1

    else:
        # White peace proposition
        text_panel = font16.render("White peace", True, TitleText)
        screen.blit(text_panel, [491, 321])
        text_panel = font14.render("Acceptance:", True, DarkText)
        screen.blit(text_panel, [491, 339])

        y_base = 356
        y_shift = 16
        y_num = 0
        for text_line in game_stats.peace_offer_text:
            text_panel = font14.render(text_line, True, DarkText)
            screen.blit(text_panel, [491, y_base + y_shift * y_num])
            y_num += 1


def draw_threaten(screen, power):
    ## Threaten target
    pygame.draw.polygon(screen, FieldColor2,
                        [[39, 319], [674, 319], [674, 538], [39, 538]])

    # Return back
    pygame.draw.polygon(screen, FillButton,
                        [[117, 535 - 15], [117 + 99, 535 - 15],
                         [117 + 99, 535], [117, 535]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[117, 535 - 15], [117 + 99, 535 - 15],
                                                     [117 + 99, 535], [117, 535]], 2)

    text_panel1 = font14.render("Return back", True, DarkText)
    screen.blit(text_panel1, [117 + 18, 535 - 15])

    # Send threat
    color1 = CancelElementsColor
    if game_stats.war_goals and game_stats.will_accept_threat_demands:
        color1 = HighlightOption
    pygame.draw.polygon(screen, FillButton,
                        [[457, 535 - 15], [457 + 99, 535 - 15],
                         [457 + 99, 535], [457, 535]])
    pygame.draw.polygon(screen, color1, [[457, 535 - 15], [457 + 99, 535 - 15],
                                         [457 + 99, 535], [457, 535]], 2)

    text_panel1 = font14.render("Send threat", True, DarkText)
    screen.blit(text_panel1, [457 + 18, 535 - 15])

    ## Demands
    text_panel = font16.render("Select a demand:", True, TitleText)
    screen.blit(text_panel, [41, 321])

    x_base = 41
    y_base = 339
    y_shift = 17
    y_num = 0
    for demand in game_stats.casus_bellis:
        text_panel = font16.render(demand, True, DarkText)
        screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
        y_num += 1

    pygame.draw.line(screen, MainMenuColor, [166, 341], [166, 515], 2)

    text_panel = font16.render("Details:", True, TitleText)
    screen.blit(text_panel, [171, 321])

    if game_stats.cb_details:
        x_base = 171
        y_base = 339
        y_shift = 17
        y_num = 0
        for item in game_stats.cb_details:
            icon_img = game_stats.gf_misc_img_dict["Icons/accept_icon"]
            screen.blit(icon_img, (x_base, y_base + y_shift * y_num + 2))

            text_panel = font16.render(item[0], True, DarkText)
            screen.blit(text_panel, [x_base + 17, y_base + y_shift * y_num])
            y_num += 1

    pygame.draw.line(screen, MainMenuColor, [296, 341], [296, 515], 2)

    text_panel = font16.render("Declared demands:", True, TitleText)
    screen.blit(text_panel, [301, 321])

    if game_stats.war_goals:
        x_base = 301
        y_base = 339
        y_shift = 17
        y_num = 0
        threat = None
        for demand in game_stats.war_goals:
            if threat is None:
                text_panel = font16.render(demand[2], True, DarkText)
                screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
                y_num += 1
                threat = demand[2]

            elif threat != demand[2]:
                text_panel = font16.render(demand[2], True, DarkText)
                screen.blit(text_panel, [x_base, y_base + y_shift * y_num])
                y_num += 1
                threat = demand[2]

            icon_img = game_stats.gf_misc_img_dict["Icons/cancel_icon"]
            screen.blit(icon_img, (x_base, y_base + y_shift * y_num + 2))

            text_panel = font16.render(demand[0], True, DarkText)
            screen.blit(text_panel, [x_base + 17, y_base + y_shift * y_num])
            y_num += 1

    pygame.draw.line(screen, MainMenuColor, [486, 341], [486, 515], 2)

    # Conditions
    text_panel = font16.render("Conditions", True, TitleText)
    screen.blit(text_panel, [491, 321])
    text_panel = font14.render("Acceptance:", True, DarkText)
    screen.blit(text_panel, [491, 339])

    y_base = 356
    y_shift = 16
    y_num = 0
    for text_line in game_stats.summary_text:
        text_panel = font14.render(text_line, True, DarkText)
        screen.blit(text_panel, [491, y_base + y_shift * y_num])
        y_num += 1
