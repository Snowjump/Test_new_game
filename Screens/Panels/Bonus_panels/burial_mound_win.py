## Among Myth and Wonder

import pygame.draw, pygame.font

from Resources import game_stats
from Resources import game_obj

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]


tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)


def burial_mound_draw_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 430], [481, 430]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 400], [491, 400]])

    text_panel1 = tnr_font18.render("Burial mound", True, DarkText)
    screen.blit(text_panel1, [550, 102])

    lot = None
    TileNum = None
    # print(str(game_stats.selected_object))
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:
            TileNum = army.location
            break
    lot = game_obj.game_map[TileNum].lot
    message = []
    if not lot.properties.time_left_before_replenishment:
        message = ["In quite remote place, you find burial mound.",
                   "Desolate and old, must be belonged",
                   "to forgotten noble family",
                   "that nobody remember anymore.",
                   "No one left to protest if you plunder this barrow.",
                   "After spending some time excavating the mound",
                   "your troops unearthed something valuable.",
                   "For a minute you having your doubts",
                   "perhaps what belongs to the dead",
                   "must stay with them forever.",
                   "Unless you are not afraid to be cursed."]
    else:
        message = ["In quite remote place, you find burial mound.",
                   "Desolate and old, must be belonged",
                   "to forgotten noble family",
                   "that nobody remember anymore.",
                   "No one left to protest if you plunder this barrow.",
                   "After spending some time excavating the mound",
                   "your troops didn't find anything interesting.",
                   "It seems this place has been already raided.",
                   "Perhaps nobody could rest in peace",
                   "without being robbed in your own burial.",
                   "Finally, you give command for your troops",
                   "to pack up and leave this cursed place."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    if not lot.properties.time_left_before_replenishment:
        text_panel1 = tnr_font18.render("Prize:", True, DarkText)
        screen.blit(text_panel1, [500, 148 + y_shift * y_points])

        text_panel1 = arial_font14.render("Cursed artifact?", True, DarkText)
        screen.blit(text_panel1, [500, 169 + y_shift * y_points])

        pygame.draw.polygon(screen, FillButton,
                            [[561, 406], [620, 406], [620, 426], [561, 426]])
        pygame.draw.polygon(screen, LineMainMenuColor1, [[561, 406], [620, 406], [620, 426], [561, 426]], 2)

        text_panel1 = arial_font16.render("Take it", True, DarkText)
        screen.blit(text_panel1, [573, 407])

        pygame.draw.polygon(screen, FillButton,
                            [[661, 406], [720, 406], [720, 426], [661, 426]])
        pygame.draw.polygon(screen, LineMainMenuColor1, [[661, 406], [720, 406], [720, 426], [661, 426]], 2)

        text_panel1 = arial_font16.render("Leave", True, DarkText)
        screen.blit(text_panel1, [673, 407])

    else:
        pygame.draw.polygon(screen, FillButton,
                            [[611, 406], [670, 406], [670, 426], [611, 426]])
        pygame.draw.polygon(screen, LineMainMenuColor1, [[611, 406], [670, 406], [670, 426], [611, 426]], 2)

        text_panel1 = arial_font16.render("Close", True, DarkText)
        screen.blit(text_panel1, [626, 407])
