## Miracle battles!


import pygame.draw, pygame.font
pygame.init()

MainMenuColor = [0x9F, 0x97, 0x97]
LineMainMenuColor1 = [0x60, 0x60, 0x60]
LineMainMenuColor2 = [0xE0, 0xE0, 0xE0]

TitleText = [0xFF, 0xFF, 0x99]

BorderMainMenuColor = [0xFF, 0xCC, 0x99]

# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)
font20 = pygame.font.SysFont('timesnewroman', 20)

def main_menu_screen(screen):

    screen.fill(MainMenuColor) # background

    # Decorative lines

    pygame.draw.line(screen, LineMainMenuColor1, [30, 120], [240, 120], 10)
    pygame.draw.line(screen, LineMainMenuColor2, [30, 124], [240, 124], 3)


    pygame.draw.line(screen, LineMainMenuColor1, [600, 120], [810, 120], 10)
    pygame.draw.line(screen, LineMainMenuColor2, [600, 124], [810, 124], 3)

    pygame.draw.line(screen, LineMainMenuColor1, [30, 220], [180, 220], 6)

    pygame.draw.line(screen, LineMainMenuColor1, [660, 220], [810, 220], 6)

    # Title

    text_MainMenu1 = font26.render("MIRACLE BATTLES", True, TitleText)
    screen.blit(text_MainMenu1, [310, 100])

    ## Buttons

    # New Game

    text_MainMenu2 = font26.render("New Game", True, TitleText)
    screen.blit(text_MainMenu2, [360, 215])

    pygame.draw.polygon(screen, BorderMainMenuColor, [[270, 213], [570, 213], [570, 245], [270, 245]],3)

    # Create level

    text_MainMenu2 = font26.render("Create level", True, TitleText)
    screen.blit(text_MainMenu2, [356, 265])

    pygame.draw.polygon(screen, BorderMainMenuColor, [[270, 263], [570, 263], [570, 295], [270, 295]],3)

    # Settings

    text_MainMenu4 = font26.render("Settings", True, TitleText)
    screen.blit(text_MainMenu4, [371, 315])

    pygame.draw.polygon(screen, BorderMainMenuColor, [[270, 313], [570, 313], [570, 345], [270, 345]], 3)

    # Exit

    text_MainMenu3 = font26.render("Exit", True, TitleText)
    screen.blit(text_MainMenu3, [395, 415])

    pygame.draw.polygon(screen, BorderMainMenuColor, [[270, 413], [570, 413], [570, 445], [270, 445]],3)


