## Miracle battles!

import pygame.draw, pygame.font


WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]


tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)


def runaway_serfs_refuge_draw_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 430], [481, 430]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 400], [491, 400]])

    text_panel1 = tnr_font18.render("Runaway serfs refuge", True, DarkText)
    screen.blit(text_panel1, [550, 102])

    message = ["Your army has reached a remote village.",
               "It seems to be a refuge fro runaway serfs,",
               "who got tired of injustice and working",
               "for their rightful lords.",
               "Harsh life on frontier without protection",
               "of knights forced them to form a small",
               "militia of their own.",
               "After seeing approaching columns of your army,",
               "villagers are running around and screaming in fear.",
               "These serfs are preparing themselves",
               "to resist your forces and protect their new free life."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    text_panel1 = tnr_font18.render("Prize:", True, DarkText)
    screen.blit(text_panel1, [500, 148 + y_shift * y_points])

    icon_img = pygame.image.load('img/Icons/resource_food.png')
    icon_img.set_colorkey(WhiteColor)
    screen.blit(icon_img, (500, 169 + y_shift * y_points))

    text_panel1 = arial_font14.render("Food", True, DarkText)
    screen.blit(text_panel1, [523, 169 + y_shift * y_points])

    icon_img = pygame.image.load('img/Icons/resource_wood.png')
    icon_img.set_colorkey(WhiteColor)
    screen.blit(icon_img, (500, 189 + y_shift * y_points))

    text_panel1 = arial_font14.render("Wood", True, DarkText)
    screen.blit(text_panel1, [523, 189 + y_shift * y_points])

    pygame.draw.polygon(screen, FillButton,
                        [[561, 406], [620, 406], [620, 426], [561, 426]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[561, 406], [620, 406], [620, 426], [561, 426]], 2)

    text_panel1 = arial_font14.render("Fight", True, DarkText)
    screen.blit(text_panel1, [575, 408])

    pygame.draw.polygon(screen, FillButton,
                        [[661, 406], [720, 406], [720, 426], [661, 426]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[661, 406], [720, 406], [720, 426], [661, 426]], 2)

    text_panel1 = arial_font14.render("Retreat", True, DarkText)
    screen.blit(text_panel1, [667, 408])
