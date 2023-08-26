## Miracle battles!

import pygame.draw, pygame.font

from Resources import game_stats


WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]


tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)


resource_names = ["Florins",
                  "Food",
                  "Wood"]


resource_imgs = {"Florins" : 'img/Icons/resource_florins.png',
                  "Food" : 'img/Icons/resource_food.png',
                  "Wood" : 'img/Icons/resource_wood.png'}


def runaway_serfs_refuge_result_draw_panel(screen):

    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 430], [481, 430]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 400], [491, 400]])

    text_panel1 = tnr_font18.render("Runaway serfs refuge", True, DarkText)
    screen.blit(text_panel1, [550, 102])

    message = ["After crushing peasant resistance",
               "your troops open up barns and",
               "search houses for provision and goods."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    text_panel1 = tnr_font18.render("Prize:", True, DarkText)
    screen.blit(text_panel1, [500, 148 + y_shift * y_points])

    y_points2 = 0

    for reward in game_stats.reward_for_demonstration:
        if reward[0] in resource_names:

            icon_img = pygame.image.load(resource_imgs[reward[0]])
            icon_img.set_colorkey(WhiteColor)
            screen.blit(icon_img, (500, 169 + y_shift * y_points + 20 * y_points2))

            text_panel1 = arial_font14.render(reward[0] + " " + str(reward[1]), True, DarkText)
            screen.blit(text_panel1, [523, 169 + y_shift * y_points + 20 * y_points2])

            y_points2 += 1

    pygame.draw.polygon(screen, FillButton,
                        [[611, 406], [670, 406], [670, 426], [611, 426]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[611, 406], [670, 406], [670, 426], [611, 426]], 2)

    text_panel1 = arial_font16.render("Close", True, DarkText)
    screen.blit(text_panel1, [626, 407])
