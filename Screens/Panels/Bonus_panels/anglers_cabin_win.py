## Among Myth and Wonder

import pygame.draw, pygame.font

from Resources import game_stats
from Resources import game_obj
from Content import artifact_imgs_cat

WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]


tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)


def anglers_cabin_draw_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 460], [481, 460]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 430], [491, 430]])

    text_panel1 = tnr_font18.render("Angler's cabin", True, DarkText)
    screen.blit(text_panel1, [550, 102])

    lot = None
    TileNum = None
    # print(str(game_stats.selected_object))
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:
            TileNum = army.location
            break
    lot = game_obj.game_map[TileNum].lot

    message = ["As you were passing a cabin by a lake",
               "a man stepped out outside and called you.",
               "'Hey, come on in, I have something valuable",
               "to offer for you, I promise you won't regret.'",
               "When you joined him in cabin, this man explained",
               "that he is an angler and just recently found",
               "a rare item in a lake. Naturally he concluded",
               "that you are a kind of person that might",
               "find it quite useful in your adventures.",
               "For a right price he is ready to give it away.",
               "For some reason, it feels dangerous try",
               "to simply rob this angler."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    text_panel1 = tnr_font18.render("Cost:", True, DarkText)
    screen.blit(text_panel1, [500, 129 + y_shift * y_points])

    icon_img = pygame.image.load('img/Icons/resource_florins.png')
    icon_img.set_colorkey(WhiteColor)
    screen.blit(icon_img, (500, 150 + y_shift * y_points))

    text_panel1 = arial_font14.render("Florins 3000", True, DarkText)
    screen.blit(text_panel1, [523, 150 + y_shift * y_points])

    text_panel1 = tnr_font18.render("Prize:", True, DarkText)
    screen.blit(text_panel1, [500, 169 + y_shift * y_points])

    # Border
    pygame.draw.polygon(screen, DarkText, [[500, 190 + y_shift * y_points],
                                           [541, 190 + y_shift * y_points],
                                           [541, 232 + y_shift * y_points],
                                           [500, 232 + y_shift * y_points]], 1)

    # Background
    img = pygame.image.load('Img/Icons/paper_square_40.png')
    img.set_colorkey(WhiteColor)
    screen.blit(img, [501, 191 + y_shift * y_points])

    icon_img = pygame.image.load(artifact_imgs_cat.imgs_catalog[lot.properties.storage[0][0]])
    icon_img.set_colorkey(WhiteColor)
    screen.blit(icon_img, (501, 191 + y_shift * y_points))

    text_panel1 = arial_font14.render(str(lot.properties.storage[0][0]), True, DarkText)
    screen.blit(text_panel1, [544, 191 + y_shift * y_points])

    pygame.draw.polygon(screen, FillButton,
                        [[561, 436], [620, 436], [620, 456], [561, 456]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[561, 436], [620, 436], [620, 456], [561, 456]], 2)

    text_panel1 = arial_font16.render("Purchase", True, DarkText)
    screen.blit(text_panel1, [564, 437])

    pygame.draw.polygon(screen, FillButton,
                        [[661, 436], [720, 436], [720, 456], [661, 456]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[661, 436], [720, 436], [720, 456], [661, 456]], 2)

    text_panel1 = arial_font16.render("Close", True, DarkText)
    screen.blit(text_panel1, [674, 437])
