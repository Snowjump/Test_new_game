## Miracle battles!

import pygame.draw, pygame.font

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]


tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)


def poachers_in_royal_forest_result_draw_panel(screen):

    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 430], [481, 430]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 400], [491, 400]])

    text_panel1 = tnr_font18.render("Poachers in Royal forest", True, DarkText)
    screen.blit(text_panel1, [550, 102])

    text_panel1 = tnr_font18.render("Task completed", True, TitleText)
    screen.blit(text_panel1, [565, 126])

    message = ["Last vile band of peasants was thrown out",
               "of Royal forest, should be a lesson to others.",
               "Now you can return to hunting once again."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 150 + y])

        y_points += 1

    pygame.draw.polygon(screen, FillButton,
                        [[611, 406], [670, 406], [670, 426], [611, 426]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[611, 406], [670, 406], [670, 426], [611, 426]], 2)

    text_panel1 = arial_font14.render("Close", True, DarkText)
    screen.blit(text_panel1, [626, 409])
