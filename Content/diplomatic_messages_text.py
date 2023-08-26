## Miracle battles

import pygame.draw
import pygame.font

from Resources import game_stats

LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]

FillButton = [0xD8, 0xBD, 0xA2]

tnr_font16 = pygame.font.SysFont('timesnewroman', 16)
arial_font16 = pygame.font.SysFont('arial', 16)


def declaration_of_war_text(screen):
    notification_log = game_stats.selected_diplomatic_notifications
    letter = notification_log[game_stats.diplomatic_message_index]
    y_base = 191

    text = "Realm of " + letter.dm_from
    text_panel1 = tnr_font16.render(text, True, DarkText)
    screen.blit(text_panel1, [281, y_base])
    y_base += 18

    text_panel1 = tnr_font16.render("has declared war on you", True, DarkText)
    screen.blit(text_panel1, [281, y_base])
    y_base += 26

    text_panel1 = tnr_font16.render("Their war goals:", True, DarkText)
    screen.blit(text_panel1, [281, y_base])
    y_base += 18

    for war_goal in letter.contents:
        icon_img = game_stats.gf_misc_img_dict[war_goal_icon_dict[war_goal[2]]]
        screen.blit(icon_img, (281, y_base + 2))

        text_panel1 = tnr_font16.render(war_goal[2] + " - " + war_goal[0], True, DarkText)
        screen.blit(text_panel1, [298, y_base])

        y_base += 18

    y_base = 512
    x_base = 422
    y_up = 20
    x_up = 110
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font16.render("Acknowledge", True, DarkText)
    screen.blit(text_panel1, [x_base + 8, y_base + 1])


def white_peace_proposition_text(screen):
    notification_log = game_stats.selected_diplomatic_notifications
    letter = notification_log[game_stats.diplomatic_message_index]
    y_base = 191

    text = "Realm of " + letter.dm_from
    text_panel1 = tnr_font16.render(text, True, DarkText)
    screen.blit(text_panel1, [281, y_base])
    y_base += 18

    text_panel1 = tnr_font16.render("has offered to end war with White peace", True, DarkText)
    screen.blit(text_panel1, [281, y_base])
    y_base += 26

    text_panel1 = tnr_font16.render("Both side cease fighting", True, DarkText)
    screen.blit(text_panel1, [281, y_base])
    y_base += 18

    text_panel1 = tnr_font16.render("without imposing any terms on one another", True, DarkText)
    screen.blit(text_panel1, [281, y_base])
    y_base += 18

    y_base = 512
    x_base = 357
    y_up = 20
    x_up = 110
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font16.render("Accept", True, DarkText)
    screen.blit(text_panel1, [x_base + 30, y_base + 1])

    x_base = 487
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font16.render("Decline", True, DarkText)
    screen.blit(text_panel1, [x_base + 28, y_base + 1])


def capitulation_proposition_text(screen):
    notification_log = game_stats.selected_diplomatic_notifications
    letter = notification_log[game_stats.diplomatic_message_index]
    y_base = 191

    x_base = 281
    text = "Realm of " + letter.dm_from
    text_panel1 = tnr_font16.render(text, True, DarkText)
    screen.blit(text_panel1, [x_base, y_base])
    y_base += 18

    text_panel1 = tnr_font16.render("has proposed terms of their capitulation:", True, DarkText)
    screen.blit(text_panel1, [x_base, y_base])
    y_base += 26

    for concession in letter.contents:
        if concession[1] is not None:
            # if item[1] == "Icons/captured_province":
            icon_img = game_stats.gf_misc_img_dict[item[1]]
            screen.blit(icon_img, (x_base, y + 2))

        text_panel1 = tnr_font16.render(concession[0], True, DarkText)
        screen.blit(text_panel1, [x_base + 18, y_base])
        y_base += 18

    y_base = 512
    x_base = 357
    y_up = 20
    x_up = 110
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font16.render("Accept", True, DarkText)
    screen.blit(text_panel1, [x_base + 30, y_base + 1])

    x_base = 487
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font16.render("Decline", True, DarkText)
    screen.blit(text_panel1, [x_base + 28, y_base + 1])


text_dict = {"Declaration of war" : declaration_of_war_text,
             "White peace" : white_peace_proposition_text,
             "Capitulation offer" : capitulation_proposition_text}

war_goal_icon_dict = {"Conquest" : "Icons/captured_province",
                      "Tribute" : "Icons/coins_tribute"}
