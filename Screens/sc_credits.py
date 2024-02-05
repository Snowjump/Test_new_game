## Among Myth and Wonder
## sc_credits

import pygame.draw, pygame.font

from Screens.colors_catalog import *

pygame.init()

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)
font24 = pygame.font.SysFont('timesnewroman', 24)
font20 = pygame.font.SysFont('timesnewroman', 20)


def credits_screen(screen):
    screen.fill(MainMenuColor)  # background

    ## Buttons

    # Return to Main Menu
    draw_button(screen, "Return to Main Menu", TitleText, BorderNewGameColor, 40, 31, 31, 300, 32)
    # text_settings1 = font26.render("Return to Main Menu", True, TitleText)
    # screen.blit(text_settings1, [200, 102])
    #
    # pygame.draw.polygon(screen, BorderNewGameColor, [[160, 100], [460, 100], [460, 132], [160, 132]], 3)

    # List of credits
    x_pos = 51
    y_pos = 91

    # Created by
    text_MainMenu1 = font24.render("CREATED BY", True, TitleText)
    screen.blit(text_MainMenu1, [x_pos, y_pos])
    y_pos += 29

    text_MainMenu2 = font20.render("Svyatoslav Pogorelov", True, TitleText)
    screen.blit(text_MainMenu2, [x_pos, y_pos])
    y_pos += 39

    # 3rd party assets
    text_MainMenu1 = font24.render("3RD PARTY ASSETS", True, TitleText)
    screen.blit(text_MainMenu1, [x_pos, y_pos])
    y_pos += 29

    text_MainMenu2 = font20.render("Sound library – Nathan Gibson", True, TitleText)
    screen.blit(text_MainMenu2, [x_pos, y_pos])
    y_pos += 24

    text_MainMenu2 = font20.render("https://nathangibson.myportfolio.com", True, TitleText)
    screen.blit(text_MainMenu2, [x_pos, y_pos])
    y_pos += 48

    text_MainMenu2 = font20.render("Sound library – Pupaya", True, TitleText)
    screen.blit(text_MainMenu2, [x_pos, y_pos])
    y_pos += 24

    text_MainMenu2 = font20.render("https://pupaya.itch.io/fantasy-audio-bundle", True, TitleText)
    screen.blit(text_MainMenu2, [x_pos, y_pos])
    y_pos += 48

    text_MainMenu2 = font20.render("Sound library – GameSounds.xyz", True, TitleText)
    screen.blit(text_MainMenu2, [x_pos, y_pos])
    y_pos += 24

    text_MainMenu2 = font20.render("https://gamesounds.xyz/", True, TitleText)
    screen.blit(text_MainMenu2, [x_pos, y_pos])
    y_pos += 48

    text_MainMenu2 = font20.render("Sound library – Sonniss", True, TitleText)
    screen.blit(text_MainMenu2, [x_pos, y_pos])
    y_pos += 24

    text_MainMenu2 = font20.render("https://sonniss.com/", True, TitleText)
    screen.blit(text_MainMenu2, [x_pos, y_pos])
    y_pos += 48


def draw_button(screen, text_line, text_color, border_color, text_indent, x_pos, y_pos, length, height):
    text_settings1 = font26.render(text_line, True, text_color)
    screen.blit(text_settings1, [x_pos + text_indent, y_pos + 2])

    pygame.draw.polygon(screen, border_color, [[x_pos, y_pos],
                                               [x_pos + length, y_pos],
                                               [x_pos + length, y_pos + height],
                                               [x_pos, y_pos + height]],
                        3)
