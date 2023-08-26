## Miracle battles!
# Select and print quest message

import pygame.draw
import pygame.font

from Resources import game_stats

LineMainMenuColor1 = [0x60, 0x60, 0x60]

DarkText = [0x11, 0x11, 0x11]

FillButton = [0xD8, 0xBD, 0xA2]

tnr_font16 = pygame.font.SysFont('timesnewroman', 16)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)
arial_font13 = pygame.font.SysFont('arial', 13)


def forrest_law_message(screen, quest):
    message = ["Maybe due to severe weather conditions this season",
               "or harsh treatment by lords, but more and more",
               "peasants flock to royal forest in search of food and wood.",
               "Foresters report of increasing number of trespassers,",
               "who hunt noble game, fish in forest lakes and ponds,",
               "cut trees and clear shrubs for firewood or building needs.",
               "Some of the foresters have been even attacked with",
               "arrows and hounds, when your royal servants tried",
               "to apprehend offenders.",
               "This situation requires your involvement."]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 380
    x_base = 281
    y_up = 20
    x_up = 140
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Upheld the forest law", True, DarkText)
    screen.blit(text_panel1, [x_base + 9, y_base + 3])

    text_panel1 = arial_font13.render("Peasant estate -1", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base - 6])

    icon_img = pygame.image.load('Img/Icons/bad_loyalty_icon.png')
    screen.blit(icon_img, (x_base + x_up + 112, y_base - 5))

    text_panel1 = arial_font13.render("for 8 turns", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 131, y_base - 6])

    text_panel1 = arial_font13.render("No peasant recruitment for 8 turns", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 14])

    # Black line
    pygame.draw.line(screen, DarkText, [281, y_base + y_up + 13], [669, y_base + y_up + 13], 1)

    y_base += y_up + 25

    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Be lenient on poaching", True, DarkText)
    screen.blit(text_panel1, [x_base + 5, y_base + 3])

    text_panel1 = arial_font13.render("Small poachers' army appears", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base - 6])

    text_panel1 = arial_font13.render("Nobility estate -1", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 14])

    icon_img = pygame.image.load('Img/Icons/bad_loyalty_icon.png')
    screen.blit(icon_img, (x_base + x_up + 110, y_base + 13))

    text_panel1 = arial_font13.render("for 6 turns", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 129, y_base + 14])


def rule_of_monastic_life_message(screen, quest):
    message = ["Several clerics are very vocal in complaints about",
               "state of spiritual life of local monasteries.",
               "It seems many monks are impudently ignore precepts",
               "set by Rule of Monastic life. They avoid manual labour,",
               "do not perform prayer services in full capacity, but",
               "rather pursue pleasures of worldly life and personal",
               "ambitions. Their behaviour invoke disdain towards them",
               "and holy church among local populace. Nobles either",
               "grumble or exploit current situation. Some clerics inclined",
               "this defiance to the Rule is a threat to authority of",
               "the clergy. Perhaps it is a time to get involved."]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 398
    x_base = 281
    y_up = 20
    x_up = 140
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Ignore disorder", True, DarkText)
    screen.blit(text_panel1, [x_base + 19, y_base + 3])

    # Temporary effect, should be changed later to something more meaningful
    text_panel1 = arial_font13.render("Battle monks recruitment +2 turns", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 3])

    # Black line
    pygame.draw.line(screen, DarkText, [281, y_base + y_up + 13], [669, y_base + y_up + 13], 1)

    y_base += y_up + 25

    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Aid reformation", True, DarkText)
    screen.blit(text_panel1, [x_base + 15, y_base + 3])

    text_panel1 = arial_font13.render("Knight Lords culture level +1", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base - 6])

    text_panel1 = arial_font13.render("Clergy estate -1", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 14])

    icon_img = pygame.image.load('Img/Icons/bad_loyalty_icon.png')
    screen.blit(icon_img, (x_base + x_up + 107, y_base + 13))

    text_panel1 = arial_font13.render("for 8 turns", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 126, y_base + 14])


def favor_abbeys_lands_message(screen, quest):
    message = ["As you were looking for means to get support",
               "of one influential local lord, your highness timely",
               "has been informed that the person in question desires",
               "to get some land holdings belonging to a local abbey.",
               "As a ruler it is in your right and power to transfer of",
               "said land holding from an abbey to a lord.",
               "Certainly local abbot would be displeased, but that's",
               "the most wonderful purpose of clergy - to use their riches",
               "to achieve your political goals."]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 380
    x_base = 281
    y_up = 20
    x_up = 150
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Grant land holdings", True, DarkText)
    screen.blit(text_panel1, [x_base + 17, y_base + 3])

    text_panel1 = arial_font13.render("Nobility estate +2", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base - 6])

    icon_img = pygame.image.load('Img/Icons/good_loyalty_icon.png')
    screen.blit(icon_img, (x_base + x_up + 114, y_base - 5))

    text_panel1 = arial_font13.render("for 8 turns", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 133, y_base - 6])

    text_panel1 = arial_font13.render("Clergy estate -1", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 14])

    icon_img = pygame.image.load('Img/Icons/bad_loyalty_icon.png')
    screen.blit(icon_img, (x_base + x_up + 104, y_base + 13))

    text_panel1 = arial_font13.render("for 12 turns", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 123, y_base + 14])

    # Black line
    pygame.draw.line(screen, DarkText, [281, y_base + y_up + 13], [669, y_base + y_up + 13], 1)

    y_base += y_up + 25

    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Pass on this opportunity", True, DarkText)
    screen.blit(text_panel1, [x_base + 5, y_base + 3])

    text_panel1 = arial_font13.render("Nothing happens", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 1])


def monastery_school_message(screen, quest):
    message = ["Once again clerics ask for your support to open",
               "monastery school as a base for education of monks, priests,",
               "preachers and clergymen with an office positions in church.",
               "This is not an easy endeavour, since good education",
               "requires presence of already educated teacher loyal to",
               "teachings of Church of Salvation, expensive supply of",
               "writing materials and impressive library of texts and",
               "even books. Unfortunately, local clergy is shorthanded",
               "in ability to acquire all of this at once.",
               "They won't succeed without your aid and donation."]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 380
    x_base = 281
    y_up = 20
    x_up = 150
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base + 14], [x_base + x_up, y_base + 14],
                         [x_base + x_up, y_base + y_up + 14], [x_base, y_base + y_up + 14]])
    pygame.draw.polygon(screen, LineMainMenuColor1,
                        [[x_base, y_base + 14], [x_base + x_up, y_base + 14],
                         [x_base + x_up, y_base + y_up + 14], [x_base, y_base + y_up + 14]], 2)

    text_panel1 = arial_font13.render("Support school", True, DarkText)
    screen.blit(text_panel1, [x_base + 30, y_base + 16])

    text_panel1 = arial_font13.render("New Priests of Salvation heroes", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base - 6])

    text_panel1 = arial_font13.render("starting level +1", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 14])

    text_panel1 = arial_font13.render("Florins -5000", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 34])

    # Black line
    pygame.draw.line(screen, DarkText, [281, y_base + y_up + 33], [669, y_base + y_up + 33], 1)

    y_base += y_up + 25 + 14

    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Disregard request", True, DarkText)
    screen.blit(text_panel1, [x_base + 24, y_base + 3])

    text_panel1 = arial_font13.render("Nothing happens", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 1])


def grey_dragon_slayer_message(screen, quest):
    message = ["Sire, the dragon is here!",
               "Peasants have seen it flying in the skies under grey wings.",
               "That nefarious creature already got a taste,",
               "for a livestock, and even stealing a cattle.",
               "Fortunately, this beast had not started any fires yet.",
               "Nobles are rumbling, they expect a swift action from",
               "you as a honourable protector of these pure lands."]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 326
    x_base = 281
    y_up = 20
    x_up = 150
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base + 14], [x_base + x_up, y_base + 14],
                         [x_base + x_up, y_base + y_up + 14], [x_base, y_base + y_up + 14]])
    pygame.draw.polygon(screen, LineMainMenuColor1,
                        [[x_base, y_base + 14], [x_base + x_up, y_base + 14],
                         [x_base + x_up, y_base + y_up + 14], [x_base, y_base + y_up + 14]], 2)

    text_panel1 = arial_font13.render("Track the dragon", True, DarkText)
    screen.blit(text_panel1, [x_base + 30, y_base + 17])

    text_panel1 = arial_font13.render("Grey dragon appears", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base - 4])

    text_panel1 = arial_font13.render("Nobility estate -1", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 16])

    icon_img = pygame.image.load('Img/Icons/bad_loyalty_icon.png')
    screen.blit(icon_img, (x_base + x_up + 112, y_base + 15))

    text_panel1 = arial_font13.render("Peasant estate -1", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 36])

    icon_img = pygame.image.load('Img/Icons/bad_loyalty_icon.png')
    screen.blit(icon_img, (x_base + x_up + 112, y_base + 35))

    if "Leader trait - Hunter" in game_stats.dilemma_additional_options:
        # Black line
        pygame.draw.line(screen, DarkText, [281, y_base + y_up + 33], [669, y_base + y_up + 33], 1)

        y_base += y_up + 25 + 14 + 5

        pygame.draw.polygon(screen, FillButton,
                            [[x_base, y_base], [x_base + x_up, y_base],
                             [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
        pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

        text_panel1 = arial_font13.render("Send huntsmen", True, DarkText)
        screen.blit(text_panel1, [x_base + 24, y_base + 3])

        text_panel1 = arial_font13.render("Ruler's trait — Hunter", True, DarkText)
        screen.blit(text_panel1, [x_base + x_up + 9, y_base - 6])

        text_panel1 = arial_font13.render("The dragon is hunted down", True, DarkText)
        screen.blit(text_panel1, [x_base + x_up + 9, y_base + 14])


def dwarven_caravan_message(screen, quest):
    message = ["Dwarven caravan of merchants reached your lands.",
               "These freeguild independent dwarves who live in remote",
               "lands without rulers once in awhile leave their",
               "settlements, traveling in trader caravans selling",
               "few months worth of work artisan goods and most",
               "importantly fine dwarven armour and weapons.",
               "Perhaps your highness would like to refill armoury."]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 380
    x_base = 281
    y_up = 20
    x_up = 150
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Trade with dwarfs", True, DarkText)
    screen.blit(text_panel1, [x_base + 22, y_base + 3])

    text_panel1 = arial_font13.render("Florins -2500", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base - 6])

    text_panel1 = arial_font13.render("Armament +2500", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 14])

    # Black line
    pygame.draw.line(screen, DarkText, [281, y_base + y_up + 13], [669, y_base + y_up + 13], 1)

    y_base += y_up + 25

    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Dwarfs spend money", True, DarkText)
    screen.blit(text_panel1, [x_base + 11, y_base + 3])

    text_panel1 = arial_font13.render("Local merchants earn 250 Florins", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 11, y_base + 3])


def desolated_defences_message(screen, quest):
    message = ["My lord, we have received a request by one of your",
               "border nobles, who laments about poor conditions",
               "of owned castle. Unfortunately, it came into despair",
               "due to regular border conflicts and noble feuds.",
               "Devastated by military service your vassal has no",
               "means to maintain his castle at necessary conditions.",
               "Therefore he can’t fulfill his obligations as",
               "a defenders of his lands and your vassal.",
               "He is requesting to supply him with stone materials."]

    y_base = 191

    for text_line in message:
        text_panel1 = tnr_font16.render(text_line, True, DarkText)
        screen.blit(text_panel1, [281, y_base])

        y_base += 18

    y_base = 380
    x_base = 281
    y_up = 20
    x_up = 150
    # Buttons
    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Promise to supply", True, DarkText)
    screen.blit(text_panel1, [x_base + 20, y_base + 3])

    text_panel1 = arial_font13.render("5 turns to provide 1600 stone", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base - 6])

    text_panel1 = arial_font13.render("Nobility estate -1", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 14])

    icon_img = pygame.image.load('Img/Icons/bad_loyalty_icon.png')
    screen.blit(icon_img, (x_base + x_up + 110, y_base + 13))

    # Black line
    pygame.draw.line(screen, DarkText, [281, y_base + y_up + 13], [669, y_base + y_up + 13], 1)

    y_base += y_up + 25

    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Provide troops instead", True, DarkText)
    screen.blit(text_panel1, [x_base + 11, y_base + 3])

    text_panel1 = arial_font13.render("No men-at-arms recruitment for 10 turns", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 3])

    # Black line
    pygame.draw.line(screen, DarkText, [281, y_base + y_up + 13], [669, y_base + y_up + 13], 1)

    y_base += y_up + 25

    pygame.draw.polygon(screen, FillButton,
                        [[x_base, y_base], [x_base + x_up, y_base],
                         [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[x_base, y_base], [x_base + x_up, y_base],
                                                     [x_base + x_up, y_base + y_up], [x_base, y_base + y_up]], 2)

    text_panel1 = arial_font13.render("Reject, it is HIS duty", True, DarkText)
    screen.blit(text_panel1, [x_base + 11, y_base + 3])

    text_panel1 = arial_font13.render("Nobility estate -2", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 9, y_base + 3])

    icon_img = pygame.image.load('Img/Icons/bad_loyalty_icon.png')
    screen.blit(icon_img, (x_base + x_up + 110, y_base + 2))

    text_panel1 = arial_font13.render("for 20 turns", True, DarkText)
    screen.blit(text_panel1, [x_base + x_up + 127, y_base + 3])


message_dict = {"Forest law" : forrest_law_message,
                "Rule of Monastic Life" : rule_of_monastic_life_message,
                "Favor abbey's lands" : favor_abbeys_lands_message,
                "Monastery school" : monastery_school_message,
                "Grey dragon slayer" : grey_dragon_slayer_message,
                "Dwarven caravan" : dwarven_caravan_message,
                "Desolated defences" : desolated_defences_message}
