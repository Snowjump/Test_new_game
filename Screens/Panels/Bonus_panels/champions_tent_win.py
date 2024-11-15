## Among Myth and Wonder
## champions_tent_win

import pygame.draw, pygame.font

from Resources import game_stats
from Resources import common_selects

from Screens.Interface_Elements import buttons

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]


tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
arial_font16 = pygame.font.SysFont('arial', 16)


def champions_tent_draw_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 445], [481, 445]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 415], [491, 415]])

    text_panel1 = tnr_font18.render("Champion's tent", True, DarkText)
    screen.blit(text_panel1, [580, 102])

    message = ["You approach a knightly tent in a field.",
               "Its owner is an old nobleman who spends",
               "his days practicing the fine art of",
               "jousting with his personal retinue.",
               "Eagerly you accept his offer to",
               "joust against each other.",
               "A nobleman turned out to be a former",
               "champion, he got the better of you.",
               "Exhausted and battered you are invited",
               "to share a dinner together.",
               "Champion parts his vast knowledge",
               "of mounted warfare."]

    optional_text = ""
    # print("champions_tent_draw_panel - game_stats.selected_army: " + str(game_stats.selected_army))
    army = common_selects.select_army_by_id(game_stats.selected_army)
    if army.hero.hero_class == "Knight":
        # print(army.hero.name)
        more_message = ["As a knight his trove of experience",
                        "is invaluable for you."]
        message += more_message
        optional_text = "Exp +500"

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    text_panel1 = tnr_font18.render("Melee cavalry: defence +1", True, DarkText)
    screen.blit(text_panel1, [500, 150 + y_shift * y_points])

    y_points += 1
    text_panel1 = tnr_font18.render(optional_text, True, DarkText)
    screen.blit(text_panel1, [500, 150 + y_shift * y_points + 4])

    text = "Close"
    buttons.element_button(screen, text, "arial_font14", "DarkText", "FillButton", "LineMainMenuColor1",
                           611, 421, 59, 20, 12, 2, 2)
    # x = 611
    # y = 421
    # x_p = 59
    # y_p = 20
    # x_w = 10
    # y_w = 2
    # pygame.draw.polygon(screen, FillButton,
    #                     [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]])
    # pygame.draw.polygon(screen, LineMainMenuColor1, [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]], 2)
    #
    # text_panel1 = arial_font16.render("Close", True, DarkText)
    # screen.blit(text_panel1, [x + x_w, y + y_w])
