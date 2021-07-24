## Miracle battles!


import pygame.draw, pygame.font
from Resources import game_stats

pygame.init()

NewGameColor = [0x8D, 0x86, 0x86]

TitleText = [0xFF, 0xFF, 0x99]

BorderNewGameColor = [0xDA, 0xAE, 0x83]
HighlightBorder = [0xF7, 0x82, 0x0C]
FieldColor = [0xA0, 0xA0, 0xA0]
ApproveFieldColor = [0x00, 0x99, 0x00]
ApproveElementsColor = [0x00, 0x66, 0x00]
CancelFieldColor = [0xFF, 0x00, 0x00]
CancelElementsColor = [0x99, 0x00, 0x00]

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)
font20 = pygame.font.SysFont('timesnewroman', 20)


def create_level_screen(screen):

    screen.fill(NewGameColor) # background

    # Title

    text_NewGame1 = font26.render("CREATE LEVEL", True, TitleText)
    screen.blit(text_NewGame1, [340, 40])

    # Map properties

    # Level width

    text_NewGame2 = font20.render("Level width", True, TitleText)
    screen.blit(text_NewGame2, [260, 85])

    text_NewGame3 = font20.render(str(game_stats.new_level_width), True, TitleText)
    screen.blit(text_NewGame3, [260, 108])

    # Width field

    pygame.draw.polygon(screen, FieldColor, [[250, 131], [320, 131], [320, 163], [250, 163]])
    if game_stats.active_width_field == False:
        pygame.draw.polygon(screen, BorderNewGameColor, [[250, 131], [320, 131], [320, 163], [250, 163]],3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[250, 131], [320, 131], [320, 163], [250, 163]],3)

    if game_stats.active_width_field == True:
        if len(game_stats.input_text) > 0:
            if game_stats.input_text != game_stats.level_width:
                game_stats.level_width = str(game_stats.input_text)
    text_NewGame4 = font20.render(str(game_stats.level_width), True, TitleText)
    screen.blit(text_NewGame4, [260, 133])

    # Approve field 1

    pygame.draw.polygon(screen, ApproveFieldColor, [[330, 131], [362, 131], [362, 163], [330, 163]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[330, 131], [362, 131], [362, 163], [330, 163]],3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(334, 147), (342, 159), (357, 135)], 3)

    # Cancel field 1

    pygame.draw.polygon(screen, CancelFieldColor, [[370, 131], [402, 131], [402, 163], [370, 163]])
    pygame.draw.polygon(screen, CancelElementsColor, [[370, 131], [402, 131], [402, 163], [370, 163]],3)
    pygame.draw.line(screen, CancelElementsColor, [373, 135], [399, 159], 3)
    pygame.draw.line(screen, CancelElementsColor, [373, 159], [399, 135], 3)

    # Level height

    text_NewGame5 = font20.render("Level height", True, TitleText)
    screen.blit(text_NewGame5, [260, 186])

    text_NewGame6 = font20.render(str(game_stats.new_level_height), True, TitleText)
    screen.blit(text_NewGame6, [260, 209])

    # Height field

    pygame.draw.polygon(screen, FieldColor, [[250, 232], [320, 232], [320, 264], [250, 264]])
    if game_stats.active_height_field == False:
        pygame.draw.polygon(screen, BorderNewGameColor, [[250, 232], [320, 232], [320, 264], [250, 264]],3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[250, 232], [320, 232], [320, 264], [250, 264]],3)

    if game_stats.active_height_field == True:
        if len(game_stats.input_text) > 0:
            if game_stats.input_text != game_stats.level_height:
                game_stats.level_height = str(game_stats.input_text)
    text_NewGame7 = font20.render(str(game_stats.level_height), True, TitleText)
    screen.blit(text_NewGame7, [260, 234])

    # Approve field 2

    pygame.draw.polygon(screen, ApproveFieldColor, [[330, 232], [362, 232], [362, 264], [330, 264]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[330, 232], [362, 232], [362, 264], [330, 264]],3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(334, 248), (342, 260), (357, 236)], 3)

    # Cancel field 2

    pygame.draw.polygon(screen, CancelFieldColor, [[370, 232], [402, 232], [402, 264], [370, 264]])
    pygame.draw.polygon(screen, CancelElementsColor, [[370, 232], [402, 232], [402, 264], [370, 264]],3)
    pygame.draw.line(screen, CancelElementsColor, [373, 236], [399, 260], 3)
    pygame.draw.line(screen, CancelElementsColor, [373, 260], [399, 236], 3)

    # Level name

    text_NewGame8 = font20.render("Level name", True, TitleText)
    screen.blit(text_NewGame8, [260, 287])

    text_NewGame9 = font20.render(str(game_stats.new_level_name), True, TitleText)
    screen.blit(text_NewGame9, [260, 310])

    # Name field

    pygame.draw.polygon(screen, FieldColor, [[250, 333], [470, 333], [470, 365], [250, 365]])
    if game_stats.active_name_field == False:
        pygame.draw.polygon(screen, BorderNewGameColor, [[250, 333], [470, 333], [470, 365], [250, 365]],3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[250, 333], [470, 333], [470, 365], [250, 365]],3)

    if game_stats.active_name_field == True:
        if len(game_stats.input_text) > 0:
            if game_stats.input_text != game_stats.level_name:
                game_stats.level_name = str(game_stats.input_text)
    text_NewGame10 = font20.render(str(game_stats.level_name), True, TitleText)
    screen.blit(text_NewGame10, [260, 335])

    # Approve field 3

    pygame.draw.polygon(screen, ApproveFieldColor, [[480, 333], [512, 333], [512, 365], [480, 365]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[480, 333], [512, 333], [512, 365], [480, 365]],3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(484, 349), (492, 361), (507, 337)], 3)

    # Cancel field 3

    pygame.draw.polygon(screen, CancelFieldColor, [[520, 333], [552, 333], [552, 365], [520, 365]])
    pygame.draw.polygon(screen, CancelElementsColor, [[520, 333], [552, 333], [552, 365], [520, 365]],3)
    pygame.draw.line(screen, CancelElementsColor, [523, 337], [549, 361], 3)
    pygame.draw.line(screen, CancelElementsColor, [523, 361], [549, 337], 3)

    # Starting month

    text_NewGame11 = font20.render("Starting month", True, TitleText)
    screen.blit(text_NewGame11, [580, 85])

    text_NewGame12 = font20.render(str(game_stats.LE_month), True, TitleText)
    screen.blit(text_NewGame12, [580, 108])

    # Month field

    pygame.draw.polygon(screen, FieldColor, [[570, 131], [640, 131], [640, 163], [570, 163]])
    if game_stats.active_starting_month_field == False:
        pygame.draw.polygon(screen, BorderNewGameColor, [[570, 131], [640, 131], [640, 163], [570, 163]], 3)
    else:
        pygame.draw.polygon(screen, HighlightBorder, [[570, 131], [640, 131], [640, 163], [570, 163]], 3)

    if game_stats.active_starting_month_field == True:
        if len(game_stats.input_text) > 0:
            if game_stats.input_text != game_stats.type_LE_month:
                game_stats.type_LE_month = str(game_stats.input_text)
    text_NewGame13 = font20.render(str(game_stats.type_LE_month), True, TitleText)
    screen.blit(text_NewGame13, [580, 133])

    # Approve field 4

    pygame.draw.polygon(screen, ApproveFieldColor, [[650, 131], [682, 131], [682, 163], [650, 163]])
    pygame.draw.polygon(screen, ApproveElementsColor, [[650, 131], [682, 131], [682, 163], [650, 163]], 3)
    pygame.draw.lines(screen, ApproveElementsColor, False, [(654, 147), (662, 159), (677, 135)], 3)

    # Cancel field 4

    pygame.draw.polygon(screen, CancelFieldColor, [[690, 131], [722, 131], [722, 163], [690, 163]])
    pygame.draw.polygon(screen, CancelElementsColor, [[690, 131], [722, 131], [722, 163], [690, 163]], 3)
    pygame.draw.line(screen, CancelElementsColor, [693, 135], [719, 159], 3)
    pygame.draw.line(screen, CancelElementsColor, [693, 159], [719, 135], 3)

    ## Buttons

    # Return to Main Menu

    text_NewGame2 = font26.render("Return to Main Menu", True, TitleText)
    screen.blit(text_NewGame2, [290, 515])

    pygame.draw.polygon(screen, BorderNewGameColor, [[250, 513], [550, 513], [550, 545], [250, 545]],3)

    # Start editor

    text_NewGame11 = font26.render("Start editor", True, TitleText)
    screen.blit(text_NewGame11, [335, 460])

    pygame.draw.polygon(screen, BorderNewGameColor, [[250, 458], [550, 458], [550, 490], [250, 490]],3)