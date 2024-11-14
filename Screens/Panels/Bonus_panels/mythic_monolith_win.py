## Among Myth and Wonder
## mythic_monolith_win

import pygame.draw, pygame.font

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]


tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
arial_font16 = pygame.font.SysFont('arial', 16)


def mythic_monolith_draw_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 400], [481, 400]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 370], [491, 370]])

    text_panel1 = tnr_font18.render("Mythic monolith", True, DarkText)
    screen.blit(text_panel1, [580, 102])

    message = ["You encounter mysterious monolith.",
               "Its surface is inscrypted with words",
               "in unfamiliar language.",
               "The longer you look, the more your",
               "mind get filled with new knowledge.",
               "It seems you can't turn away you gaze,",
               "just until there is no more knowledge",
               "left to feed you mind.",
               "In the end there is nothing else",
               "you could do with this artifact."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    text_panel1 = tnr_font18.render("Exp +1000", True, DarkText)
    screen.blit(text_panel1, [500, 150 + y_shift * y_points])

    pygame.draw.polygon(screen, FillButton,
                        [[611, 376], [670, 376], [670, 396], [611, 396]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[611, 376], [670, 376], [670, 396], [611, 396]], 2)

    text_panel1 = arial_font16.render("Close", True, DarkText)
    screen.blit(text_panel1, [621, 378])

