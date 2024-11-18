## Among Myth and Wonder
## leshys_hut_win

import pygame.draw, pygame.font

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources import game_stats
from Resources import game_obj
from Resources import common_selects

from Screens.Interface_Elements import buttons


def leshys_hut_draw_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 345], [481, 345]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 315], [491, 315]])

    text_panel1 = tnr_font18.render("Leshy's hut", True, DarkText)
    screen.blit(text_panel1, [580, 102])

    message = ["In the heart of the dense forest,",
               "a gloomy glade revealed itself with",
               "an ancient hut in the middle of it.",
               "Strange curiosity pulled you to enter.",
               "Inside you are a met by a stocky old man",
               "with a bushy unkempt beard. ",
               "The host offers you to join him in",
               "a game of dice to dispel boredom.",
               "There is something ominous about him,",
               "you better not lose a game."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    text = "Play"
    buttons.element_button(screen, text, "arial_font14", "DarkText", "FillButton", "LineMainMenuColor1",
                           561, 321, 59, 20, 17, 3, 2)

    text = "Leave"
    buttons.element_button(screen, text, "arial_font14", "DarkText", "FillButton", "LineMainMenuColor1",
                           661, 321, 59, 20, 12, 3, 2)


def leshys_hut_dice_result_draw_panel(screen):
    pygame.draw.polygon(screen, MainMenuColor, [[481, 101], [800, 101], [800, 445], [481, 445]])

    pygame.draw.polygon(screen, FillButton,
                        [[491, 125], [790, 125], [790, 415], [491, 415]])

    text_panel1 = tnr_font18.render("Leshy's hut", True, DarkText)
    screen.blit(text_panel1, [580, 102])

    army = common_selects.select_army_by_id(game_stats.selected_army)
    lot = game_obj.game_map[army.location].lot

    message = []

    if lot.properties.storage[0] == 6:
        message += ["You have utterly crushed an old man",
                    "in a game of dice. He is slightly",
                    "disappointed but not agitated.",
                    "'Very well, you have earned a reward.",
                    "I will give you some of my power.'",
                    "In the blink of an eye the host disappeared.",
                    "All you have to wonder was it really",
                    "the spirit of the forest."]

    elif lot.properties.storage[0] == 5:
        message += ["You have won in a game of dice.",
                    "An old man cocks his head in surprise.",
                    "'Good game, I shall grant you some presents,",
                    "you will find a cart behind my hut.'",
                    "In the blink of an eye the host disappeared.",
                    "All you have to wonder was it really",
                    "the spirit of the forest."]

    elif lot.properties.storage[0] == 4:
        message += ["You have won in a game of dice.",
                    "An old man cocks his head in surprise.",
                    "'Good game, I will make sure you have",
                    "a lovely journey through my domain.'",
                    "In the blink of an eye the host disappeared.",
                    "All you have to wonder was it really",
                    "the spirit of the forest."]

    elif lot.properties.storage[0] == 3:
        message += ["You have lost in a game of dice.",
                    "An old man smiles mischievously.",
                    "'Maybe next time... Now you would not",
                    "object to share some strength, right?'",
                    "In the blink of an eye the host disappeared.",
                    "All you have to wonder was it really",
                    "the spirit of the forest."]

    elif lot.properties.storage[0] == 2:
        message += ["You have lost in a game of dice.",
                    "An old man smiles mischievously.",
                    "'Grand, I suppose you have to pay",
                    "your dues, I always accept coins.'",
                    "In the blink of an eye the host disappeared.",
                    "All you have to wonder was it really",
                    "the spirit of the forest."]

    elif lot.properties.storage[0] == 1:
        message += ["You are defeated in a game of dice.",
                    "An old man laughs sardonically.",
                    "'Bad luck! As a reward I will take some",
                    "of your servants, I can use new minions.'",
                    "In the blink of an eye the host disappeared.",
                    "All you have to wonder was it really",
                    "the spirit of the forest."]

    y_shift = 16
    y_points = 0
    for line in message:
        y = y_shift * y_points
        text_panel1 = tnr_font14.render(line, True, DarkText)
        screen.blit(text_panel1, [500, 130 + y])

        y_points += 1

    y_points += 1
    if lot.properties.storage[0] == 6:
        text_panel1 = tnr_font18.render("Magic power +1", True, DarkText)
        screen.blit(text_panel1, [500, 150 + y_shift * y_points])

    elif lot.properties.storage[0] == 5:
        text_panel1 = tnr_font18.render("Prize:", True, DarkText)
        screen.blit(text_panel1, [500, 129 + y_shift * y_points])

        icon_img = pygame.image.load('img/Icons/resource_food.png')
        icon_img.set_colorkey(WhiteColor)
        screen.blit(icon_img, (500, 150 + y_shift * y_points))

        text_panel1 = arial_font14.render("Food 500", True, DarkText)
        screen.blit(text_panel1, [523, 150 + y_shift * y_points])

        icon_img = pygame.image.load('img/Icons/resource_wood.png')
        icon_img.set_colorkey(WhiteColor)
        screen.blit(icon_img, (500, 150 + y_shift * y_points + 20))

        text_panel1 = arial_font14.render("Wood 1000", True, DarkText)
        screen.blit(text_panel1, [523, 150 + y_shift * y_points + 20])

    elif lot.properties.storage[0] == 4:
        text_panel1 = tnr_font18.render("Your army has replenished its energy", True, DarkText)
        screen.blit(text_panel1, [500, 150 + y_shift * y_points])

        text_panel1 = tnr_font18.render("Movement points +800", True, DarkText)
        screen.blit(text_panel1, [500, 170 + y_shift * y_points])

    elif lot.properties.storage[0] == 3:
        ability_img = pygame.image.load('Img/Icons/mana_icon.png')
        ability_img.set_colorkey(WhiteColor)
        screen.blit(ability_img, [500, 150 + y_shift * y_points])

        text_panel1 = tnr_font18.render("Your mana is drained to zero", True, DarkText)
        screen.blit(text_panel1, [524, 148 + y_shift * y_points])

    elif lot.properties.storage[0] == 2:
        text_panel1 = tnr_font18.render("Lost:", True, DarkText)
        screen.blit(text_panel1, [500, 129 + y_shift * y_points])

        icon_img = pygame.image.load('img/Icons/resource_florins.png')
        icon_img.set_colorkey(WhiteColor)
        screen.blit(icon_img, (500, 150 + y_shift * y_points))

        text_panel1 = arial_font14.render("Florins 1500", True, DarkText)
        screen.blit(text_panel1, [523, 150 + y_shift * y_points])

    elif lot.properties.storage[0] == 1:
        text_panel1 = tnr_font18.render("You lost some troops", True, DarkText)
        screen.blit(text_panel1, [500, 150 + y_shift * y_points])

    text = "Close"
    buttons.element_button(screen, text, "arial_font14", "DarkText", "FillButton", "LineMainMenuColor1",
                           611, 421, 59, 20, 12, 2, 2)
