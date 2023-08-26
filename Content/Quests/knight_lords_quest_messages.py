## Miracle battles!
# Select and print quest message

import pygame

LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]

FillButton = [0xD8, 0xBD, 0xA2]

tnr_font16 = pygame.font.SysFont('timesnewroman', 16)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)
arial_font13 = pygame.font.SysFont('arial', 13)


def poachers_in_royal_forest_message(screen, quest):
    message = ["Bands of poachers are roaming Royal forest breaking the law.",
               "This reflect in negative light on your authority, sire.",
               "Nobles get displeased with current state of affairs.",
               "Perhaps getting rid of these criminals will put nobles",
               "back in line and save the game from being hunted down."]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 290
    x_base = 281
    y_up = 20
    x_up = 115
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    icon_img = pygame.image.load('Img/Icons/magnifying_glass_icon.png')
    screen.blit(icon_img, (x_base + 2, y_base + 2))

    text_panel1 = arial_font14.render("Show on map", True, DarkText)
    screen.blit(text_panel1, [x_base + 24, y_base + 1])


def slay_the_grey_dragon_message(screen, quest):
    message = ["The Grey dragon reign free over your lands.",
               "Commoners are terrified and call for protection,",
               "while nobles making plans to slay the dragon",
               "and take all the glory for a such feat.",
               "Curiously they are not at haste though."]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 290
    x_base = 281
    y_up = 20
    x_up = 115
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    icon_img = pygame.image.load('Img/Icons/magnifying_glass_icon.png')
    screen.blit(icon_img, (x_base + 2, y_base + 2))

    text_panel1 = arial_font14.render("Show on map", True, DarkText)
    screen.blit(text_panel1, [x_base + 24, y_base + 2])


def provide_stone_to_vassal_message(screen, quest):
    message = ["You have promised to provide one of your border",
               "vassals with stone materials to restore defences",
               "of damaged castle. Your generous support will",
               "help the vassal strengthen border safety.",
               "",
               "Remaining time: " + str(quest.remaining_time)]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 330
    x_base = 281
    y_up = 20
    x_up = 115
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Provide materials", True, DarkText)
    screen.blit(text_panel1, [x_base + 7, y_base + 3])

    text_panel1 = arial_font13.render("-1600 stone", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 3])


message_dict = {"Poachers in Royal forest" : poachers_in_royal_forest_message,
                "Slay the Grey dragon" : slay_the_grey_dragon_message,
                "Provide stone to vassal" : provide_stone_to_vassal_message}
