## Among Myth and Wonder
## sc_load_level_into_editor

import pygame.draw, pygame.font

from Screens.colors_catalog import *

from Resources import game_stats

pygame.init()
# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)
font20 = pygame.font.SysFont('timesnewroman', 20)


def load_level_edit_screen(screen):
    screen.fill(NewGameColor)  # background

    # Title

    text_NewGame1 = font26.render("CREATE LEVEL", True, TitleText)
    screen.blit(text_NewGame1, [340, 40])

    # Levels list
    x = 78
    y = 83
    pygame.draw.polygon(screen, MainMenuColor, [[x, y], [x + 224, y], [x + 224, y + 320], [x, y + 320]])

    x = 80
    y = 85
    underline_number = 0
    for level_title in game_stats.levels_list:
        text_NewGame2 = font20.render(level_title, True, TitleText)
        screen.blit(text_NewGame2, [x, y])

        # Grey underlines
        pygame.draw.lines(screen, NewGameColor, False, [(x, 85 + underline_number * 24 + 22),
                                                        (x + 220, 85 + underline_number * 24 + 22)], 1)
        underline_number += 1
        y += 24

    # White line
    pygame.draw.lines(screen, WhiteBorder, False, [(x, 85 + game_stats.level_index * 24 + 22),
                                                   (x + 220, 85 + game_stats.level_index * 24 + 22)], 1)

    ## Level information
    # Details
    x = 400
    y = 85
    text_NewGame2 = font20.render(game_stats.levels_list[game_stats.level_index], True, TitleText)
    screen.blit(text_NewGame2, [x, y])

    ## Buttons

    # Return to Main Menu

    text_NewGame2 = font26.render("Return to Main Menu", True, TitleText)
    screen.blit(text_NewGame2, [290, 515])

    pygame.draw.polygon(screen, BorderNewGameColor, [[250, 513], [550, 513], [550, 545], [250, 545]], 3)

    # Start editor

    text_NewGame11 = font26.render("Start editor", True, TitleText)
    screen.blit(text_NewGame11, [335, 460])

    pygame.draw.polygon(screen, BorderNewGameColor, [[250, 458], [550, 458], [550, 490], [250, 490]], 3)

    # New level
    x_pos = 670
    y_pos = 131
    text_NewGame2 = font26.render("New level", True, TitleText)

    pygame.draw.polygon(screen, BorderNewGameColor, [[x_pos, y_pos], [x_pos + 160, y_pos],
                                                     [x_pos + 160, y_pos + 32], [x_pos, y_pos + 32]], 3)

    screen.blit(text_NewGame2, [x_pos + 24, y_pos + 2])

    # Load level
    y_pos += 55
    text_NewGame2 = font26.render("Load level", True, TitleText)

    pygame.draw.polygon(screen, HighlightBorder, [[x_pos, y_pos], [x_pos + 160, y_pos],
                                                  [x_pos + 160, y_pos + 32], [x_pos, y_pos + 32]], 3)

    screen.blit(text_NewGame2, [x_pos + 22, y_pos + 2])

    # Art picture
    picture_img = game_stats.gf_menus_art["Arts/storm_in_the_ocean"]
    picture_img = pygame.transform.scale(picture_img,
                                         (306, 546))
    screen.blit(picture_img, (901, 61))
