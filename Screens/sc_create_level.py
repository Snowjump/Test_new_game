## Among Myth and Wonder
## sc_create_level

import pygame.draw, pygame.font

from Screens.colors_catalog import *

from Resources import game_stats

pygame.init()

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)
font20 = pygame.font.SysFont('timesnewroman', 20)


def create_level_screen(screen):
    screen.fill(NewGameColor)  # background

    # Title

    text_NewGame1 = font26.render("CREATE LEVEL", True, TitleText)
    screen.blit(text_NewGame1, [340, 40])

    # Map properties

    # Level width
    x_pos = 50
    y_pos = 85

    text_NewGame2 = font20.render("Level width", True, TitleText)
    screen.blit(text_NewGame2, [x_pos + 10, y_pos])

    y_pos += 23

    text_NewGame3 = font20.render(str(game_stats.new_level_width), True, TitleText)
    screen.blit(text_NewGame3, [x_pos + 10, y_pos])

    y_pos += 23

    # Width field

    pygame.draw.polygon(screen, FieldColor, [[x_pos, y_pos], [x_pos + 70, y_pos],
                                             [x_pos + 70, y_pos + 32], [x_pos, y_pos + 32]])
    if not game_stats.active_width_field:
        pygame.draw.polygon(screen, BorderNewGameColor, [[x_pos, y_pos], [x_pos + 70, y_pos],
                                                         [x_pos + 70, y_pos + 32], [x_pos, y_pos + 32]], 3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[x_pos, y_pos], [x_pos + 70, y_pos],
                                                      [x_pos + 70, y_pos + 32], [x_pos, y_pos + 32]], 3)

    if game_stats.active_width_field:
        if len(game_stats.create_level_input_text) > 0:
            if game_stats.create_level_input_text != game_stats.level_width:
                game_stats.level_width = str(game_stats.create_level_input_text)
    text_NewGame4 = font20.render(str(game_stats.level_width), True, TitleText)
    screen.blit(text_NewGame4, [x_pos + 10, y_pos + 5])

    # Approve field 1

    pygame.draw.polygon(screen, ApproveFieldColor, [[x_pos + 80, y_pos], [x_pos + 112, y_pos],
                                                    [x_pos + 112, y_pos + 32], [x_pos + 80, y_pos + 32]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[x_pos + 80, y_pos], [x_pos + 112, y_pos],
                                                       [x_pos + 112, y_pos + 32], [x_pos + 80, y_pos + 32]], 3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(x_pos + 84, y_pos + 16),
                                                            (x_pos + 92, y_pos + 28),
                                                            (x_pos + 107, y_pos + 4)], 3)

    # Cancel field 1

    pygame.draw.polygon(screen, CancelFieldColor, [[x_pos + 120, y_pos], [x_pos + 152, y_pos],
                                                   [x_pos + 152, y_pos + 32], [x_pos + 120, y_pos + 32]])
    pygame.draw.polygon(screen, CancelElementsColor, [[x_pos + 120, y_pos], [x_pos + 152, y_pos],
                                                      [x_pos + 152, y_pos + 32], [x_pos + 120, y_pos + 32]], 3)
    pygame.draw.line(screen, CancelElementsColor, [x_pos + 123, y_pos + 4], [x_pos + 149, y_pos + 28], 3)
    pygame.draw.line(screen, CancelElementsColor, [x_pos + 123, y_pos + 28], [x_pos + 149, y_pos + 4], 3)

    y_pos += 55

    # Level height

    text_NewGame5 = font20.render("Level height", True, TitleText)
    screen.blit(text_NewGame5, [x_pos + 10, y_pos])

    y_pos += 23

    text_NewGame6 = font20.render(str(game_stats.new_level_height), True, TitleText)
    screen.blit(text_NewGame6, [x_pos + 10, y_pos])

    y_pos += 23

    # Height field

    pygame.draw.polygon(screen, FieldColor, [[x_pos, y_pos], [x_pos + 70, y_pos],
                                             [x_pos + 70, y_pos + 32], [x_pos, y_pos + 32]])
    if not game_stats.active_height_field:
        pygame.draw.polygon(screen, BorderNewGameColor, [[x_pos, y_pos], [x_pos + 70, y_pos],
                                                         [x_pos + 70, y_pos + 32], [x_pos, y_pos + 32]], 3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[x_pos, y_pos], [x_pos + 70, y_pos],
                                                      [x_pos + 70, y_pos + 32], [x_pos, y_pos + 32]], 3)

    if game_stats.active_height_field:
        if len(game_stats.create_level_input_text) > 0:
            if game_stats.create_level_input_text != game_stats.level_height:
                game_stats.level_height = str(game_stats.create_level_input_text)
    text_NewGame7 = font20.render(str(game_stats.level_height), True, TitleText)
    screen.blit(text_NewGame7, [x_pos + 10, y_pos + 5])

    # Approve field 2

    pygame.draw.polygon(screen, ApproveFieldColor, [[x_pos + 80, y_pos], [x_pos + 112, y_pos],
                                                    [x_pos + 112, y_pos + 32], [x_pos + 80, y_pos + 32]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[x_pos + 80, y_pos], [x_pos + 112, y_pos],
                                                       [x_pos + 112, y_pos + 32], [x_pos + 80, y_pos + 32]], 3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(x_pos + 84, y_pos + 16),
                                                            (x_pos + 92, y_pos + 28),
                                                            (x_pos + 107, y_pos + 4)], 3)

    # Cancel field 2

    pygame.draw.polygon(screen, CancelFieldColor, [[x_pos + 120, y_pos], [x_pos + 152, y_pos],
                                                   [x_pos + 152, y_pos + 32], [x_pos + 120, y_pos + 32]])
    pygame.draw.polygon(screen, CancelElementsColor, [[x_pos + 120, y_pos], [x_pos + 152, y_pos],
                                                      [x_pos + 152, y_pos + 32], [x_pos + 120, y_pos + 32]], 3)
    pygame.draw.line(screen, CancelElementsColor, [x_pos + 123, y_pos + 4], [x_pos + 149, y_pos + 28], 3)
    pygame.draw.line(screen, CancelElementsColor, [x_pos + 123, y_pos + 28], [x_pos + 149, y_pos + 4], 3)

    y_pos += 55

    # Level name

    text_NewGame8 = font20.render("Level name", True, TitleText)
    screen.blit(text_NewGame8, [x_pos + 10, y_pos])

    y_pos += 23

    text_NewGame9 = font20.render(str(game_stats.new_level_name), True, TitleText)
    screen.blit(text_NewGame9, [x_pos + 10, y_pos])

    y_pos += 23

    # Name field

    pygame.draw.polygon(screen, FieldColor, [[x_pos, y_pos], [x_pos + 220, y_pos],
                                             [x_pos + 220, y_pos + 32], [x_pos, y_pos + 32]])
    if not game_stats.active_name_field:
        pygame.draw.polygon(screen, BorderNewGameColor, [[x_pos, y_pos], [x_pos + 220, y_pos],
                                                         [x_pos + 220, y_pos + 32], [x_pos, y_pos + 32]], 3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[x_pos, y_pos], [x_pos + 220, y_pos],
                                                      [x_pos + 220, y_pos + 32], [x_pos, y_pos + 32]], 3)

    if game_stats.active_name_field:
        if len(game_stats.create_level_input_text) > 0:
            if game_stats.create_level_input_text != game_stats.level_name:
                game_stats.level_name = str(game_stats.create_level_input_text)
    text_NewGame10 = font20.render(str(game_stats.level_name), True, TitleText)
    screen.blit(text_NewGame10, [x_pos + 10, y_pos + 5])

    # Approve field 3

    pygame.draw.polygon(screen, ApproveFieldColor, [[x_pos + 230, y_pos], [x_pos + 262, y_pos],
                                                    [x_pos + 262, y_pos + 32], [x_pos + 230, y_pos + 32]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[x_pos + 230, y_pos], [x_pos + 262, y_pos],
                                                       [x_pos + 262, y_pos + 32], [x_pos + 230, y_pos + 32]], 3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(x_pos + 234, y_pos + 16),
                                                            (x_pos + 242, y_pos + 28),
                                                            (x_pos + 257, y_pos + 4)], 3)

    # Cancel field 3

    pygame.draw.polygon(screen, CancelFieldColor, [[x_pos + 270, y_pos], [x_pos + 302, y_pos],
                                                   [x_pos + 302, y_pos + 32], [x_pos + 270, y_pos + 32]])
    pygame.draw.polygon(screen, CancelElementsColor, [[x_pos + 270, y_pos], [x_pos + 302, y_pos],
                                                      [x_pos + 302, y_pos + 32], [x_pos + 270, y_pos + 32]], 3)
    pygame.draw.line(screen, CancelElementsColor, [x_pos + 273, y_pos + 4], [x_pos + 299, y_pos + 28], 3)
    pygame.draw.line(screen, CancelElementsColor, [x_pos + 273, y_pos + 28], [x_pos + 299, y_pos + 4], 3)

    # Starting month
    x_pos = 360
    y_pos = 85

    text_NewGame11 = font20.render("Starting month", True, TitleText)
    screen.blit(text_NewGame11, [x_pos + 10, y_pos])

    y_pos += 23

    text_NewGame12 = font20.render(str(game_stats.LE_month), True, TitleText)
    screen.blit(text_NewGame12, [x_pos + 10, y_pos])

    # Month field
    y_pos += 23

    pygame.draw.polygon(screen, FieldColor, [[x_pos, y_pos], [x_pos + 70, y_pos],
                                             [x_pos + 70, y_pos + 32], [x_pos, y_pos + 32]])
    if not game_stats.active_starting_month_field:
        pygame.draw.polygon(screen, BorderNewGameColor, [[x_pos, y_pos], [x_pos + 70, y_pos],
                                                         [x_pos + 70, y_pos + 32], [x_pos, y_pos + 32]], 3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[x_pos, y_pos], [x_pos + 70, y_pos],
                                                      [x_pos + 70, y_pos + 32], [x_pos, y_pos + 32]], 3)

    if game_stats.active_starting_month_field:
        if len(game_stats.create_level_input_text) > 0:
            if game_stats.create_level_input_text != game_stats.type_LE_month:
                game_stats.type_LE_month = str(game_stats.create_level_input_text)
    text_NewGame13 = font20.render(str(game_stats.type_LE_month), True, TitleText)
    screen.blit(text_NewGame13, [x_pos + 10, y_pos + 5])

    # Approve field 4

    pygame.draw.polygon(screen, ApproveFieldColor, [[x_pos + 80, y_pos], [x_pos + 112, y_pos],
                                                    [x_pos + 112, y_pos + 32], [x_pos + 80, y_pos + 32]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[x_pos + 80, y_pos], [x_pos + 112, y_pos],
                                                       [x_pos + 112, y_pos + 32], [x_pos + 80, y_pos + 32]], 3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(x_pos + 84, y_pos + 16),
                                                            (x_pos + 92, y_pos + 28),
                                                            (x_pos + 107, y_pos + 4)], 3)

    # Cancel field 4

    pygame.draw.polygon(screen, CancelFieldColor, [[x_pos + 120, y_pos], [x_pos + 152, y_pos],
                                                   [x_pos + 152, y_pos + 32], [x_pos + 120, y_pos + 32]])
    pygame.draw.polygon(screen, CancelElementsColor, [[x_pos + 120, y_pos], [x_pos + 152, y_pos],
                                                      [x_pos + 152, y_pos + 32], [x_pos + 120, y_pos + 32]], 3)
    pygame.draw.line(screen, CancelElementsColor, [x_pos + 123, y_pos + 4], [x_pos + 149, y_pos + 28], 3)
    pygame.draw.line(screen, CancelElementsColor, [x_pos + 123, y_pos + 28], [x_pos + 149, y_pos + 4], 3)

    y_pos += 55

    # Level type
    text_NewGame11 = font20.render("Level type", True, TitleText)
    screen.blit(text_NewGame11, [x_pos + 10, y_pos])

    y_pos += 23

    # Would be more in the future
    text_NewGame12 = font20.render(game_stats.LE_level_type, True, TitleText)
    screen.blit(text_NewGame12, [x_pos + 10, y_pos])

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

    pygame.draw.polygon(screen, HighlightBorder, [[x_pos, y_pos], [x_pos + 160, y_pos],
                                                  [x_pos + 160, y_pos + 32], [x_pos, y_pos + 32]], 3)

    screen.blit(text_NewGame2, [x_pos + 24, y_pos + 2])

    # Load level
    y_pos += 55
    text_NewGame2 = font26.render("Load level", True, TitleText)

    pygame.draw.polygon(screen, BorderNewGameColor, [[x_pos, y_pos], [x_pos + 160, y_pos],
                                                  [x_pos + 160, y_pos + 32], [x_pos, y_pos + 32]], 3)

    screen.blit(text_NewGame2, [x_pos + 22, y_pos + 2])

    # Art picture
    picture_img = game_stats.gf_menus_art["Arts/storm_in_the_ocean"]
    picture_img = pygame.transform.scale(picture_img,
                                         (306, 546))
    screen.blit(picture_img, (901, 61))


