## Among Myth and Wonder
## sc_settings

import pygame.draw, pygame.font

from Screens.colors_catalog import *

pygame.init()

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)
font20 = pygame.font.SysFont('timesnewroman', 20)


def settings_screen(screen):
    screen.fill(NewGameColor)  # background

    ## Decorative lines
    pygame.draw.line(screen, LineMainMenuColor1, [145, 170], [470, 170], 5)

    ## Settings

    # Resolution
    text_settings2 = font26.render("Resolution", True, TitleText)
    screen.blit(text_settings2, [180, 180])

    text_settings3 = font20.render("1280 X 800", True, TitleText)
    screen.blit(text_settings3, [180, 232])

    pygame.draw.polygon(screen, BorderNewGameColor, [[160, 230], [300, 230], [300, 256], [160, 256]], 3)

    text_settings4 = font20.render("1280 X 700", True, TitleText)
    screen.blit(text_settings4, [180, 272])

    pygame.draw.polygon(screen, BorderNewGameColor, [[160, 270], [300, 270], [300, 296], [160, 296]], 3)

    ## Buttons

    # Return to Main Menu
    text_settings1 = font26.render("Return to Main Menu", True, TitleText)
    screen.blit(text_settings1, [200, 102])

    pygame.draw.polygon(screen, BorderNewGameColor, [[160, 100], [460, 100], [460, 132], [160, 132]], 3)
