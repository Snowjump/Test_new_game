## Miracle battles!

import pygame.draw, pygame.font

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]


tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
arial_font16 = pygame.font.SysFont('arial', 16)


def stone_circle_draw_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 430], [481, 430]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 400], [491, 400]])

    text_panel1 = tnr_font18.render("Stone circle", True, DarkText)
    screen.blit(text_panel1, [580, 102])

    message = ["This Stone circle is known",
               "among locals as source of power.",
               "From time to time mystics gather here",
               "to perform occult rites.",
               "Soon as you enter Stone circle",
               "you started too feel strange energy",
               "dwelling in this place ready to break out.",
               "You invoke your knowledge to perform",
               "a ritual of your own to get in contact",
               "with this peculiar energy.",
               "Quite soon you feel that energy has",
               "left this place for a time,",
               "while you seems to be successfully",
               "filled with new powers."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    text_panel1 = tnr_font18.render("Magic power +1", True, DarkText)
    screen.blit(text_panel1, [500, 150 + y_shift * y_points])

    pygame.draw.polygon(screen, FillButton,
                        [[611, 406], [670, 406], [670, 426], [611, 426]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[611, 406], [670, 406], [670, 426], [611, 426]], 2)

    text_panel1 = arial_font16.render("Close", True, DarkText)
    screen.blit(text_panel1, [626, 407])
