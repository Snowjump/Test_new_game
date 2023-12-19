## Among Myth and Wonder

import pygame.draw, pygame.font

from Resources import game_obj
from Resources import game_stats

WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]
LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]


tnr_font14 = pygame.font.SysFont('timesnewroman', 14)
tnr_font18 = pygame.font.SysFont('timesnewroman', 18)
arial_font16 = pygame.font.SysFont('arial', 16)


def stone_well_draw_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 400], [481, 400]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 370], [491, 370]])

    text_panel1 = tnr_font18.render("Scholar's tower", True, DarkText)
    screen.blit(text_panel1, [580, 102])

    message = ["You lead your way toward an old stone well.",
               "It is said that this well is connected to",
               "a sacred spring that able to replenish",
               "strength and energy of anyone who will",
               "drink some water from it.",
               "You have a long way ahead so you",
               "immediately take some water from it.",
               "After a few gulps of cold water",
               "you already feel yourself refreshed",
               "and eager to continue the journey."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    max_mana = 0
    mana_reserve = 0
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:
            max_mana = int(10 * army.hero.knowledge)
            mana_reserve = int(army.hero.mana_reserve)
            break

    mana_value = 0
    if mana_reserve + (max_mana / 2) > max_mana:
        mana_value = int(max_mana - mana_reserve)
    else:
        mana_value = int(max_mana / 2)

    text = "Mana +" + str(mana_value)

    text_panel1 = tnr_font18.render(text, True, DarkText)
    screen.blit(text_panel1, [524, 148 + y_shift * y_points])

    ability_img = pygame.image.load('Img/Icons/mana_icon.png')
    ability_img.set_colorkey(WhiteColor)
    screen.blit(ability_img, [500, 150 + y_shift * y_points])

    pygame.draw.polygon(screen, FillButton,
                        [[611, 376], [670, 376], [670, 396], [611, 396]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[611, 376], [670, 376], [670, 396], [611, 396]], 2)

    text_panel1 = arial_font16.render("Close", True, DarkText)
    screen.blit(text_panel1, [626, 377])
