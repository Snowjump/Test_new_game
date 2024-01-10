## Among Myth and Wonder
## win_autobattle_conclusion

import math
import pygame.draw
import pygame.font

from Resources import game_stats

LineMainMenuColor1 = [0x60, 0x60, 0x60]

Board1 = [0x8A, 0xAA, 0xE5]  # Light blue
Board2 = [0x8A, 0xB9, 0xE5]  # More light blue

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]

FillButton = [0xD8, 0xBD, 0xA2]

font20 = pygame.font.SysFont('timesnewroman', 20)
font16 = pygame.font.SysFont('timesnewroman', 16)
font14 = pygame.font.SysFont('timesnewroman', 14)

arial_font14 = pygame.font.SysFont('arial', 14)


def autobattle_conclusion_panel(screen):
    # print("autobattle_conclusion_panel()")
    pygame.draw.polygon(screen, Board1, [[380, 100], [900, 100], [900, 440], [380, 440]])

    pygame.draw.polygon(screen, Board2, [[388, 196], [637, 196], [637, 432], [388, 432]])
    pygame.draw.polygon(screen, Board2, [[643, 196], [892, 196], [892, 432], [643, 432]])

    title_text = game_stats.result_statement
    text_panel1 = font20.render(title_text, True, TitleText)
    screen.blit(text_panel1, [618 - len(title_text), 103])

    # Attacker
    text_panel1 = font20.render(game_stats.attacker_realm, True, TitleText)
    screen.blit(text_panel1, [420 - len(game_stats.attacker_realm), 133])

    # Defender
    text_panel1 = font20.render(game_stats.defender_realm, True, TitleText)
    screen.blit(text_panel1, [750 - len(game_stats.defender_realm), 133])

    # Earned experience
    if game_stats.earned_experience > 0:
        text_panel1 = font20.render("Experience +" + str(game_stats.earned_experience), True, TitleText)
        screen.blit(text_panel1, [580, 163])

    # Attacker units
    if len(game_stats.attacker_army.units) > 0:
        number = 0
        for unit in game_stats.attacker_army.units:
            x_pos = 388 + math.floor(number % 5) * 50 - 2
            y_pos = 198 + math.floor(number / 5) * 55
            # print(str(x_pos))

            if len(unit.crew) > 0:
                img_width = unit.crew[0].img_width
                img_height = unit.crew[0].img_height
            else:
                img_width = unit.cemetery[0].img_width
                img_height = unit.cemetery[0].img_height

            if img_width > 44 or img_height > 44:
                army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                if img_width > 44:
                    proportion = 44 / img_width
                    army_img = pygame.transform.scale(army_img,
                                                      (44,
                                                       int(img_height * proportion)))
                    x_offset = 3
                    y_offset = (48 - (img_height * proportion)) / 2
                else:
                    proportion = 44 / img_height
                    army_img = pygame.transform.scale(army_img,
                                                      (int(img_width * proportion),
                                                       44))
                    x_offset = (48 - (img_width * proportion)) / 2
                    y_offset = 3
            else:
                army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                x_offset = unit.x_offset
                y_offset = unit.y_offset

            screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])

            # army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
            # screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

            amount_text = str(len(unit.crew)) + "/" + str(unit.number * unit.rows)
            text_panel1 = arial_font14.render(amount_text, True, TitleText)
            screen.blit(text_panel1, [x_pos + 5, y_pos + 46])

            if unit.deserted:
                # print("Attention")
                text_panel1 = arial_font14.render("Routed", True, TitleText)
                screen.blit(text_panel1, [x_pos + 5, y_pos + 70])

            number += 1

    # Defender units
    if len(game_stats.defender_army.units) > 0:
        number = 0
        for unit in game_stats.defender_army.units:
            x_pos = 643 + math.floor(number % 5) * 50 - 2
            y_pos = 198 + math.floor(number / 5) * 55
            # print(str(x_pos))

            if len(unit.crew) > 0:
                img_width = unit.crew[0].img_width
                img_height = unit.crew[0].img_height
            else:
                img_width = unit.cemetery[0].img_width
                img_height = unit.cemetery[0].img_height

            if img_width > 44 or img_height > 44:
                army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                if img_width > 44:
                    proportion = 44 / img_width
                    army_img = pygame.transform.scale(army_img,
                                                      (44,
                                                       int(img_height * proportion)))
                    x_offset = 3
                    y_offset = (48 - (img_height * proportion)) / 2
                else:
                    proportion = 44 / img_height
                    army_img = pygame.transform.scale(army_img,
                                                      (int(img_width * proportion),
                                                       44))
                    x_offset = (48 - (img_width * proportion)) / 2
                    y_offset = 3
            else:
                army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_r"]
                x_offset = unit.x_offset
                y_offset = unit.y_offset

            screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])

            # army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + "_l"]
            # screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

            amount_text = str(len(unit.crew)) + "/" + str(unit.number * unit.rows)
            text_panel1 = arial_font14.render(amount_text, True, TitleText)
            screen.blit(text_panel1, [x_pos + 5, y_pos + 46])

            if unit.deserted:
                # print("Attention")
                text_panel1 = arial_font14.render("Routed", True, TitleText)
                screen.blit(text_panel1, [x_pos + 5, y_pos + 70])

            number += 1

    # Button - Close panel
    pygame.draw.polygon(screen, FillButton, [[590, 138], [690, 138], [690, 160], [590, 160]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[590, 138], [690, 138], [690, 160], [590, 160]], 3)
    text_panel5 = font20.render("Close", True, DarkText)
    screen.blit(text_panel5, [618, 138])
