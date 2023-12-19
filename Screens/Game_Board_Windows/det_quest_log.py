## Among Myth and Wonder

import pygame.draw
import pygame.font

from Resources import game_stats

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]

FieldColor2 = [0xBE, 0xB0, 0xA2]

font20 = pygame.font.SysFont('timesnewroman', 20)

arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)

ScarletColor = [0xFF, 0x24, 0x00]
CopperColor = [0xE9, 0x75, 0x00]
NightBlueColor = [0x19, 0x2F, 0xF0]
MoonColor = [0xD2, 0xD6, 0xFA]
BullBrownColor = [0x40, 0x21, 0x02]
BlackHoovesColor = [0x0A, 0x06, 0x02]
RoyalPurple = [0x8B, 0x00, 0x8B]
GoldColor = [0xFF, 0xD7, 0x00]
TribesTide = [0x00, 0x64, 0x00]
ForestGreen = [0x22, 0x8B, 0x22]
MaroonColor = [0x80, 0x00, 0x00]
SlateGray = [0x70, 0x80, 0x90]

FlagColors = {"Scarlet": ScarletColor,
              "Copper": CopperColor,
              "NightBlue": NightBlueColor,
              "Moon": MoonColor,
              "BullBrown": BullBrownColor,
              "BlackHooves": BlackHoovesColor,
              "RoyalPurple": RoyalPurple,
              "GoldColor": GoldColor,
              "TribesTide": TribesTide,
              "ForestGreen": ForestGreen,
              "MaroonColor": MaroonColor,
              "SlateGray": SlateGray}


def area_management(screen):
    if game_stats.quest_area == "Quest messages":
        ## Quests
        draw_quest_area(screen)
    if game_stats.quest_area == "Diplomatic messages":
        ## Diplomatic notifications
        draw_diplomatic_messages_area(screen)


def draw_quest_area(screen):
    # Background
    x1 = 36
    x2 = 236
    pygame.draw.polygon(screen, FieldColor2,
                        [[x1, 143],
                         [x1 + x2, 143],
                         [x1 + x2, 538],
                         [x1, 538]])

    x1 = 277
    x2 = 400
    pygame.draw.polygon(screen, FieldColor2,
                        [[x1, 143],
                         [x1 + x2, 143],
                         [x1 + x2, 538],
                         [x1, 538]])

    # Player's realm
    quest_log = game_stats.selected_quest_messages

    y_base = 143

    # Quest log
    text_panel = font20.render("Quest log", True, DarkText)
    screen.blit(text_panel, [48, y_base])
    y_base += 26

    # Quest messages
    y_shift = 20
    y_points = 0
    for quest_message in quest_log:
        # Message icon
        if quest_message.message_type == "Dilemma":
            icon_img = game_stats.gf_misc_img_dict['Icons/scales_icon']
            screen.blit(icon_img, (38, y_base + y_shift * y_points))
        elif quest_message.message_type == "Quest":
            icon_img = game_stats.gf_misc_img_dict["Icons/wind_rose_icon"]
            screen.blit(icon_img, (38, y_base + y_shift * y_points))

        # Quest name
        text_panel1 = arial_font14.render(quest_message.name, True, DarkText)
        screen.blit(text_panel1, [56, y_base + y_shift * y_points])

        y_points += 1

    y_base = 143

    # Message details
    text_panel = font20.render("Quest message", True, DarkText)
    screen.blit(text_panel, [289, y_base])
    y_base += 24

    if game_stats.quest_message_index is not None:
        message = quest_log[game_stats.quest_message_index]
        # Quest name
        text_panel1 = font20.render(message.name, True, TitleText)
        screen.blit(text_panel1, [281, y_base])

        game_stats.quest_message_panel(screen, message)


def draw_diplomatic_messages_area(screen):
    # Background
    x1 = 36
    x2 = 236
    pygame.draw.polygon(screen, FieldColor2,
                        [[x1, 143],
                         [x1 + x2, 143],
                         [x1 + x2, 538],
                         [x1, 538]])

    x1 = 277
    x2 = 400
    pygame.draw.polygon(screen, FieldColor2,
                        [[x1, 143],
                         [x1 + x2, 143],
                         [x1 + x2, 538],
                         [x1, 538]])

    # Player's realm
    notification_log = game_stats.selected_diplomatic_notifications

    y_base = 143

    # Notifications title
    text_panel = font20.render("Notifications", True, DarkText)
    screen.blit(text_panel, [48, y_base])
    y_base += 26

    # Notifications
    x_base = 56
    y_shift = 20
    y_points = 0

    for notification in notification_log:
        # Message icon
        icon_img = game_stats.gf_misc_img_dict[notification_icons_dict[notification.subject]]
        screen.blit(icon_img, (38, y_base + y_shift * y_points))

        # Flag
        pygame.draw.polygon(screen, FlagColors[notification.f_color_from],
                            [[x_base, y_base + y_shift * y_points],
                             [x_base + 12, y_base + y_shift * y_points],
                             [x_base + 12, y_base + y_shift * y_points + 5],
                             [x_base, y_base + y_shift * y_points + 5]])
        pygame.draw.polygon(screen, FlagColors[notification.s_color_from],
                            [[x_base, y_base + y_shift * y_points + 6],
                             [x_base + 12, y_base + y_shift * y_points + 6],
                             [x_base + 12, y_base + y_shift * y_points + 10],
                             [x_base, y_base + y_shift * y_points + 10]])

        # Subject
        text_panel1 = arial_font14.render(notification.subject, True, DarkText)
        screen.blit(text_panel1, [71, y_base + y_shift * y_points - 2])

        y_points += 1

    y_base = 143

    # Message details
    text_panel = font20.render("Diplomatic message", True, DarkText)
    screen.blit(text_panel, [289, y_base])
    y_base += 24

    if game_stats.diplomatic_message_index is not None:
        message = notification_log[game_stats.diplomatic_message_index]
        # Quest name
        text_panel1 = font20.render(message.subject, True, TitleText)
        screen.blit(text_panel1, [281, y_base])

        game_stats.diplomatic_message_panel(screen)


notification_icons_dict = {"Declaration of war" : "Icons/sword_and_axe_icon_14_x_12",
                           "White peace" : "Icons/white_peace",
                           "Capitulation offer" : "Icons/capitulation"}
