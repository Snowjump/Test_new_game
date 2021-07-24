## Miracle battles!


import pygame.draw, pygame.font
from Resources import game_stats
pygame.init()

NewGameColor = [0x8D, 0x86, 0x86]

TitleText = [0xFF, 0xFF, 0x99]

BorderNewGameColor = [0xDA, 0xAE, 0x83]


# Fonts
font26 = pygame.font.SysFont('timesnewroman', 26)
font20 = pygame.font.SysFont('timesnewroman', 20)

def new_game_screen(screen):

    screen.fill(NewGameColor) # background

    # Title

    text_NewGame1 = font26.render("NEW GAME", True, TitleText)
    screen.blit(text_NewGame1, [335, 40])

    # Choose your character

    text_NewGame2 = font20.render("Test level", True, TitleText)
    screen.blit(text_NewGame2, [80, 85])


    ## Buttons

    # Exit

    text_NewGame2 = font26.render("Return to Main Menu", True, TitleText)
    screen.blit(text_NewGame2, [290, 515])

    pygame.draw.polygon(screen, BorderNewGameColor, [[250, 513], [550, 513], [550, 545], [250, 545]],3)

    # Start New Game

    text_NewGame3 = font26.render("Start", True, TitleText)
    screen.blit(text_NewGame3, [374, 445])

    pygame.draw.polygon(screen, BorderNewGameColor, [[250, 443], [550, 443], [550, 475], [250, 475]],3)

