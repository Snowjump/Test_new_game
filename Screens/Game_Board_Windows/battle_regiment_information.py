## Among Myth and Wonder
    ## battle_regiment_information

import pygame.draw
import pygame.font

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Screens.Interface_Elements import buttons
from Resources import game_stats


def regiment_info_window(screen, b):
    pygame.draw.polygon(screen, MainMenuColor, [[642, 70], [1278, 70], [1278, 600], [642, 600]])

    # Switch detailed regiment information
    buttons.element_button(screen, "i", "arial_font16", "DarkText", "RockTunel", "LineMainMenuColor1",
                           1230, 85, 19, 19, 9, 2, 2)

    # Close settlement window
    buttons.element_close_button(screen, "CancelFieldColor", "CancelElementsColor", "CancelElementsColor",
                                 1254, 85, 19, 19, 2, 2)

    # Regiment's information
    regiment_information_draw(screen, b)

    # Attacks and fight abilities
    ybase = 365
    attacks_abilities_information_draw(screen, b, ybase)

    # Top right side
    # Special tags
    special_tags_draw(screen, b)

    # Skills information
    ybase = 205
    skills_information_draw(screen, b, ybase)

    # Effects
    ybase = 365
    effects_information_draw(screen, b, ybase)

    # Abilities
    ybase = 505
    abilities_information_draw(screen, b, ybase)


def regiment_information_draw(screen, b):
    # Flag
    if b.unit_info.first_color is not None:
        pygame.draw.polygon(screen, FlagColors[b.unit_info.first_color],
                            [[646, 75], [677, 75], [677, 86], [646, 86]])
        pygame.draw.polygon(screen, FlagColors[b.unit_info.second_color],
                            [[646, 87], [677, 87], [677, 98], [646, 98]])

    # Regiment's name
    text_panel = tnr_font20.render(b.unit_info.regiment_name, True, TitleText)
    screen.blit(text_panel, [682, 75])

    # Engaged status
    text_status = "Disengaged"
    if b.unit_info.engaged:
        text_status = "Engaged"
    text_panel = arial_font16.render(text_status, True, TitleText)
    screen.blit(text_panel, [646, 105])

    # Routing
    if b.unit_info.deserted:
        text_panel = arial_font16.render("Routing", True, TitleText)
        screen.blit(text_panel, [682, 105])

    # Amount
    text_panel = arial_font16.render("Amount - " + str(b.unit_info.amount), True, TitleText)
    screen.blit(text_panel, [646, 125])

    # Total HP left
    text_panel = arial_font16.render("Hit points - " + str(b.unit_info.total_HP), True, TitleText)
    screen.blit(text_panel, [646, 145])

    # Current morale
    text_panel = arial_font16.render("Morale - " + str(b.unit_info.morale), True, TitleText)
    screen.blit(text_panel, [646, 165])

    # Base health of single creature
    text = "Max health - " + str(b.unit_info.health)
    if game_stats.detailed_regiment_info:
        text += "   (" + str(b.unit_info.base_health) + " + " + str(b.unit_info.health - b.unit_info.base_health) + ")"
    text_panel = arial_font16.render(text, True, TitleText)
    screen.blit(text_panel, [646, 185])

    # Leadership
    text_panel = arial_font16.render("Leadership - " + str(b.unit_info.leadership), True, TitleText)
    screen.blit(text_panel, [646, 205])

    # Regiment's experience
    text_panel = arial_font16.render("Experience - " + str(b.unit_info.experience), True, TitleText)
    screen.blit(text_panel, [646, 225])

    # Speed
    text_panel = arial_font16.render("Speed - " + str(b.unit_info.speed), True, TitleText)
    screen.blit(text_panel, [646, 245])

    # Armour
    text = "Armour - " + str(b.unit_info.final_armour)
    if game_stats.detailed_regiment_info:
        text += "   (" + str(b.unit_info.armour) + " + " + str(b.unit_info.final_armour - b.unit_info.armour) + ")"
    text_panel = arial_font16.render(text, True, TitleText)
    screen.blit(text_panel, [646, 265])

    # Defence
    text = "Defence - " + str(b.unit_info.final_defence)
    if game_stats.detailed_regiment_info:
        text += "   (" + str(b.unit_info.defence) + " + " + str(b.unit_info.final_defence - b.unit_info.defence) + ")"
    text_panel = arial_font16.render(text, True, TitleText)
    screen.blit(text_panel, [646, 285])

    # Magic power
    if b.unit_info.magic_power > 0:
        text_panel = arial_font16.render("Magic power - " + str(b.unit_info.magic_power), True, TitleText)
        screen.blit(text_panel, [646, 305])

        # Mana reserve
        text_panel = arial_font16.render("Mana reserve - " + str(b.unit_info.mana_reserve) + "/"
                                         + str(b.unit_info.max_mana_reserve), True, TitleText)
        screen.blit(text_panel, [646, 325])


def attacks_abilities_information_draw(screen, b, ybase):
    # Buttons - previous and next attack
    buttons.element_arrow_button(screen, "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 646, ybase, 18, 18, 1, 2)

    buttons.element_arrow_button(screen, "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 786, ybase, 18, 18, 1, 2)

    # Attack name
    text_panel = arial_font16.render(str(b.attack_info.attack_name), True, TitleText)
    screen.blit(text_panel, [672, ybase])

    if b.attack_info.attack_name != "Abilities":
        # Attack type
        text_panel = arial_font16.render(str(b.attack_info.attack_type), True, TitleText)
        screen.blit(text_panel, [646, ybase + 20])

        # Damage
        dmg_text = str(b.attack_info.min_dmg)
        if b.attack_info.min_dmg < b.attack_info.max_dmg:
            dmg_text += " - " + str(b.attack_info.max_dmg)
        text_panel = arial_font16.render("Damage - " + dmg_text, True, TitleText)
        screen.blit(text_panel, [646, ybase + 40])

        # Mastery level
        text_panel = arial_font16.render("Mastery - " + str(b.attack_info.mastery), True, TitleText)
        screen.blit(text_panel, [646, ybase + 60])

        # Effective range
        if b.attack_info.effective_range > 0:
            text_panel = arial_font16.render("Effective range - " + str(b.attack_info.effective_range), True, TitleText)
            screen.blit(text_panel, [646, ybase + 80])

            # Range limit
            text_panel = arial_font16.render("Range limit - " + str(b.attack_info.range_limit), True, TitleText)
            screen.blit(text_panel, [646, ybase + 100])

        # Tags
        text_panel = arial_font16.render("Tags:", True, TitleText)
        screen.blit(text_panel, [646, ybase + 120])
        if len(b.attack_info.tags) > 0:
            y_add = 0
            for tag in b.attack_info.tags:
                text_panel = arial_font16.render(str(tag), True, TitleText)
                screen.blit(text_panel, [646, ybase + 140 + y_add * 20])
                y_add += 1

    else:
        # Abilities
        for ability in b.unit_info.abilities:
            # Ability name
            ybase += 20
            text_panel = arial_font16.render(str(ability), True, TitleText)
            screen.blit(text_panel, [646, ybase])


def special_tags_draw(screen, b):
    text_panel = arial_font16.render("Special tags:", True, TitleText)
    screen.blit(text_panel, [1020, 85])

    y_tag = 0
    y_shift = 20
    for tag in b.unit_info.reg_tags:
        text_panel = arial_font16.render(tag.capitalize(), True, TitleText)
        screen.blit(text_panel, [1020, 105 + y_shift * y_tag])

        y_tag += 1


def skills_information_draw(screen, b, ybase):
    # Buttons - previous and next skill
    buttons.element_arrow_button(screen, "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 1020, ybase, 18, 18, 1, 2)

    buttons.element_arrow_button(screen, "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 1200, ybase, 18, 18, 1, 2)

    # Skills
    text_panel = arial_font16.render("Skills:", True, TitleText)
    screen.blit(text_panel, [1020, ybase - 20])

    if b.skill_info is not None:
        # Skill name
        text_panel = arial_font16.render(b.skill_info.skill_name, True, TitleText)
        screen.blit(text_panel, [1046, ybase])

        # Skill application
        text_panel = arial_font16.render(b.skill_info.application, True, TitleText)
        screen.blit(text_panel, [1020, ybase + 20])

        # Value
        text_panel = arial_font16.render(b.skill_info.value_text, True, TitleText)
        screen.blit(text_panel, [1020, ybase + 40])

        # Skill tags
        if len(b.skill_info.skill_tags) > 0:
            y_add = 0
            for tag in b.skill_info.skill_tags:
                text_panel = arial_font16.render(str(tag), True, TitleText)
                screen.blit(text_panel, [1020, ybase + 60 + y_add * 20])
                y_add += 1


def effects_information_draw(screen, b, ybase):
    text_panel = arial_font16.render("Effects:", True, TitleText)
    screen.blit(text_panel, [1020, ybase -20])

    # Buttons - previous and next effect
    buttons.element_arrow_button(screen, "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 1020, ybase, 18, 18, 1, 2)

    buttons.element_arrow_button(screen, "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 1200, ybase, 18, 18, 1, 2)

    if b.effect_info is not None:
        # Effect name
        text_panel = arial_font16.render(b.effect_info.effect_name, True, TitleText)
        screen.blit(text_panel, [1046, ybase])

        # Duration of effect
        text_panel = arial_font16.render(b.effect_info.time_text, True, TitleText)
        screen.blit(text_panel, [1020, ybase + 20])

        # Status information
        y_add = 0
        for status in b.effect_info.status_list:
            value = ""
            if status.quantity is not None:
                value = str(status.quantity) + " " + str(status.method)
            elif status.quality is not None:
                value = str(status.quality)
            text_panel = arial_font16.render(status.application + " " + value, True, TitleText)
            screen.blit(text_panel, [1020, ybase + 40 + y_add * 20])
            y_add += 1


def abilities_information_draw(screen, b, ybase):
    # Buttons - previous and next ability
    buttons.element_arrow_button(screen, "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 1020, ybase, 18, 18, 1, 2)

    buttons.element_arrow_button(screen, "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 1200, ybase, 18, 18, 1, 2)

    # Abilities
    text_panel = arial_font16.render("Abilities:", True, TitleText)
    screen.blit(text_panel, [1020, ybase - 20])

    if b.ability_info is not None:
        # Ability name
        text_panel = arial_font16.render(b.ability_info, True, TitleText)
        screen.blit(text_panel, [1046, ybase])

        # Ability description
        for text_line in b.ability_description:
            ybase += 20
            text_panel = arial_font16.render(text_line, True, TitleText)
            screen.blit(text_panel, [1020, ybase])
