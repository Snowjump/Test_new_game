## Among Myth and Wonder
## rw_new_regiment_information

import pygame.draw
import pygame.font

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources import game_stats
from Screens.Interface_Elements import buttons


def new_regiment_info(screen):
    u = game_stats.rw_unit_info
    a = game_stats.rw_attack_info
    s = game_stats.rw_skill_info

    # Draw top right panel with information about building upgrade
    pygame.draw.polygon(screen, MainMenuColor,
                        [[642, 80], [1278, 80], [1278, 540], [642, 540]])

    # Close settlement window
    buttons.element_close_button(screen, "CancelFieldColor", "CancelElementsColor", "CancelElementsColor",
                                 1254, 85, 19, 19, 2, 2)

    # Regiment's information
    # Regiment's name
    text_panel = tnr_font20.render(u.regiment_name, True, TitleText)
    screen.blit(text_panel, [646, 87])

    # Amount
    text_panel = arial_font16.render("Amount - " + str(u.amount), True, TitleText)
    screen.blit(text_panel, [646, 117])

    # Total HP left
    text_panel = arial_font16.render("Hit points - " + str(u.total_HP), True, TitleText)
    screen.blit(text_panel, [646, 137])

    # Base health of single creature
    text_panel = arial_font16.render("Base health - " + str(u.health), True, TitleText)
    screen.blit(text_panel, [646, 157])

    # Leadership
    text_panel = arial_font16.render("Leadership - " + str(u.leadership), True, TitleText)
    screen.blit(text_panel, [646, 177])

    # Regiment's experience
    text_panel = arial_font16.render("Experience - " + str(u.experience), True, TitleText)
    screen.blit(text_panel, [646, 197])

    # Speed
    text_panel = arial_font16.render("Speed - " + str(u.speed), True, TitleText)
    screen.blit(text_panel, [646, 217])

    # Armor
    text_panel = arial_font16.render("Armour - " + str(u.armour), True, TitleText)
    screen.blit(text_panel, [646, 237])

    # Defence
    text_panel = arial_font16.render("Defence - " + str(u.defence), True, TitleText)
    screen.blit(text_panel, [646, 257])

    ybase = 345
    # Attack
    text_panel = arial_font16.render("Attack:", True, TitleText)
    screen.blit(text_panel, [646, ybase - 20])

    # Buttons - previous and next attack
    buttons.element_arrow_button(screen, "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 646, ybase, 18, 18, 1, 2)

    buttons.element_arrow_button(screen, "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 786, ybase, 18, 18, 1, 2)

    # Attack name
    text_panel = arial_font16.render(str(a.attack_name), True, TitleText)
    screen.blit(text_panel, [672, ybase])

    # Attack type
    text_panel = arial_font16.render(str(a.attack_type), True, TitleText)
    screen.blit(text_panel, [646, ybase + 20])

    # Damage
    dmg_text = str(a.min_dmg)
    if a.min_dmg < a.max_dmg:
        dmg_text += " - " + str(a.max_dmg)
    text_panel = arial_font16.render("Damage - " + dmg_text, True, TitleText)
    screen.blit(text_panel, [646, ybase + 40])

    # Mastery level
    text_panel = arial_font16.render("Mastery - " + str(a.mastery), True, TitleText)
    screen.blit(text_panel, [646, ybase + 60])

    # Effective range
    if a.effective_range > 0:
        text_panel = arial_font16.render("Effective range - " + str(a.effective_range), True, TitleText)
        screen.blit(text_panel, [646, ybase + 80])

        # Range limit
        text_panel = arial_font16.render("Range limit - " + str(a.range_limit), True, TitleText)
        screen.blit(text_panel, [646, ybase + 100])

    # Tags
    text_panel = arial_font16.render("Tags:", True, TitleText)
    screen.blit(text_panel, [646, ybase + 120])
    if len(a.tags) > 0:
        y_add = 0
        for tag in a.tags:
            text_panel = arial_font16.render(str(tag), True, TitleText)
            screen.blit(text_panel, [646, ybase + 140 + y_add * 20])
            y_add += 1

    # Top right side
    # Special tags
    text_panel = arial_font16.render("Special tags:", True, TitleText)
    screen.blit(text_panel, [1020, 97])

    y_tag = 0
    y_shift = 20
    for tag in u.reg_tags:
        text_panel = arial_font16.render(tag.capitalize(), True, TitleText)
        screen.blit(text_panel, [1020, 117 + y_shift * y_tag])

        y_tag += 1

    ybase = 345

    # Buttons - previous and next skill
    buttons.element_arrow_button(screen, "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 1020, ybase, 18, 18, 1, 2)

    buttons.element_arrow_button(screen, "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 1200, ybase, 18, 18, 1, 2)

    # Skills
    text_panel = arial_font16.render("Skills:", True, TitleText)
    screen.blit(text_panel, [1020, ybase - 20])

    if s is not None:
        # Skill name
        text_panel = arial_font16.render(s.skill_name, True, TitleText)
        screen.blit(text_panel, [1046, ybase])

        # Skill application
        text_panel = arial_font16.render(s.application, True, TitleText)
        screen.blit(text_panel, [1020, ybase + 20])

        # Value
        text_panel = arial_font16.render(s.value_text, True, TitleText)
        screen.blit(text_panel, [1020, ybase + 40])

        # Skill tags
        if len(s.skill_tags) > 0:
            y_add = 0
            for tag in s.skill_tags:
                text_panel = arial_font16.render(str(tag), True, TitleText)
                screen.blit(text_panel, [1020, ybase + 60 + y_add * 20])
                y_add += 1

            # text_panel = arial_font16.render(str(type(s.skill_tags)), True, TitleText)
            # screen.blit(text_panel, [1020, ybase + 60 + y_add * 20])
