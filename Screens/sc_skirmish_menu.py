## Miracle battles!
## sc_skirmish_menu

import pygame.draw, pygame.font
from Resources import game_stats
pygame.init()

MainMenuColor = [0x9F, 0x97, 0x97]
NewGameColor = [0x8D, 0x86, 0x86]

TitleText = [0xFF, 0xFF, 0x99]

RockTunel = [0x89, 0x89, 0x89]
LineMainMenuColor1 = [0x60, 0x60, 0x60]
WhiteBorder = [249, 238, 227, 200]
BorderNewGameColor = [0xDA, 0xAE, 0x83]

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
font26 = pygame.font.SysFont('timesnewroman', 26)
font20 = pygame.font.SysFont('timesnewroman', 20)
font18 = pygame.font.SysFont('timesnewroman', 18)


def skirmish_menu_screen(screen):

    screen.fill(NewGameColor)  # background

    # Title

    text_NewGame1 = font26.render("SKIRMISH", True, TitleText)
    screen.blit(text_NewGame1, [335, 40])

    # Levels list
    x = 78
    y = 83
    pygame.draw.polygon(screen, MainMenuColor, [[x, y], [x + 224, y], [x + 224, y + 320], [x, y + 320]])

    # text_NewGame2 = font20.render("Test level", True, TitleText)
    # screen.blit(text_NewGame2, [80, 85])
    x = 80
    y = 85
    underline_number = 0
    for level_title in game_stats.levels_list:
        text_NewGame2 = font20.render(level_title, True, TitleText)
        screen.blit(text_NewGame2, [x, y])

        # Grey underlines
        pygame.draw.lines(screen, NewGameColor, False, [(x, 85 + underline_number * 24 + 22),
                                                       (x + 220, 85 + underline_number * 24 + 22)], 1)
        underline_number += 1
        y += 24

    # White line
    pygame.draw.lines(screen, WhiteBorder, False, [(x, 85 + game_stats.level_index * 24 + 22),
                                                   (x + 220, 85 + game_stats.level_index * 24 + 22)], 1)

    ## Level information
    # Details
    x = 400
    y = 85
    text_NewGame2 = font20.render(game_stats.levels_list[game_stats.level_index], True, TitleText)
    screen.blit(text_NewGame2, [x, y])

    y += 24
    text_NewGame2 = font18.render("Objectives:", True, TitleText)
    screen.blit(text_NewGame2, [x, y])

    y += 22
    text_NewGame2 = font18.render("Neither lords, nor their servants", True, TitleText)
    screen.blit(text_NewGame2, [x, y])

    y += 22
    text_NewGame2 = font18.render("shall know your mercy", True, TitleText)
    screen.blit(text_NewGame2, [x, y])

    y += 22
    text_NewGame2 = font18.render("Conquer all other realms", True, TitleText)
    screen.blit(text_NewGame2, [x, y])

    # To the right
    # Choose a realm
    x = 800
    y = 85
    text_skirmish = str(game_stats.start_level_playable_realms) + " playable realms out of " +\
        str(game_stats.start_level_total_realms) + " realms total"

    text_NewGame2 = font18.render(text_skirmish, True, TitleText)
    screen.blit(text_NewGame2, [x, y])

    # Choose a realm to play
    y += 24
    pygame.draw.polygon(screen, RockTunel, [[x, y], [x + 19, y], [x + 19, y + 18], [x, y + 18]])
    pygame.draw.polygon(screen, LineMainMenuColor1,
                        [[x, y], [x + 19, y], [x + 19, y + 18], [x, y + 18]],
                        1)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(x + 16, y + 2),
                                                          (x + 3, y + 9),
                                                          (x + 16, y + 15)], 2)

    x += 21
    pygame.draw.polygon(screen, RockTunel, [[x, y], [x + 19, y], [x + 19, y + 18], [x, y + 18]])
    pygame.draw.polygon(screen, LineMainMenuColor1,
                        [[x, y], [x + 19, y], [x + 19, y + 18], [x, y + 18]],
                        1)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(x + 3, y + 2),
                                                          (x + 16, y + 9),
                                                          (x + 3, y + 15)], 2)

    # Flag
    x += 25
    pygame.draw.polygon(screen, FlagColors[game_stats.start_level_selected_realm.f_color],
                        [[x, y], [x + 22, y],
                         [x + 22, y + 8], [x, y + 8]])
    pygame.draw.polygon(screen, FlagColors[game_stats.start_level_selected_realm.s_color],
                        [[x, y + 9], [x + 22, y + 9],
                         [x + 22, y + 16], [x, y + 16]])

    x += 27
    y -= 1
    text_skirmish = game_stats.start_level_selected_realm.name
    text_NewGame2 = font18.render(text_skirmish, True, TitleText)
    screen.blit(text_NewGame2, [x, y])

    x -= 27
    y += 22
    text_skirmish = game_stats.start_level_selected_realm.alignment
    text_NewGame2 = font18.render(text_skirmish, True, TitleText)
    screen.blit(text_NewGame2, [x, y])

    ## Buttons
    # Exit

    text_NewGame2 = font26.render("Return to Main Menu", True, TitleText)
    screen.blit(text_NewGame2, [290, 515])

    pygame.draw.polygon(screen, BorderNewGameColor, [[250, 513], [550, 513], [550, 545], [250, 545]], 3)

    # Start New Game

    text_NewGame3 = font26.render("Start", True, TitleText)
    screen.blit(text_NewGame3, [374, 445])

    pygame.draw.polygon(screen, BorderNewGameColor, [[250, 443], [550, 443], [550, 475], [250, 475]], 3)
