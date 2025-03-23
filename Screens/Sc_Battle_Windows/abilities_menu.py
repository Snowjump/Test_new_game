## Among Myth and Wonder
## abilities_menu

import pygame.draw

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Screens.Interface_Elements import buttons

from Resources import game_stats

from Content.Abilities import ability_catalog


def abilities_menu_window(screen, b):
    pygame.draw.polygon(screen, MainMenuColor, [[181, 101], [1100, 101], [1100, 600], [181, 600]])

    # Close window button
    buttons.element_close_button(screen, "CancelFieldColor", "CancelElementsColor", "CancelElementsColor",
                                 1076, 106, 19, 19, 2, 2)

    # Ability school list
    ability_school_draw(screen, b)

    # Ability selection list
    ability_selection_draw(screen, b)

    # Ability description
    ability_description_draw(screen, b)

    # Ability execution
    ability_execution(screen, b)


def ability_school_draw(screen, b):
    text_panel1 = tnr_font20.render("Ability school", True, TitleText)
    screen.blit(text_panel1, [188, 103])

    y_points = 0
    y_shift = 44

    for school in b.list_of_schools:
        # Background
        pygame.draw.polygon(screen, FillButton,
                            [[232, 128 + y_shift * y_points],
                             [430, 128 + y_shift * y_points],
                             [430, 167 + y_shift * y_points],
                             [232, 167 + y_shift * y_points]])

        if b.selected_school == school:
            # White border
            pygame.draw.polygon(screen, WhiteBorder, [[232, 128 + y_shift * y_points],
                                                      [430, 128 + y_shift * y_points],
                                                      [430, 167 + y_shift * y_points],
                                                      [232, 167 + y_shift * y_points]], 2)

        # School's icon
        back_img = game_stats.gf_misc_img_dict["Icons/paper_3_square_40"]
        screen.blit(back_img, [188, 128 + y_shift * y_points])

        school_img = game_stats.gf_misc_img_dict["Schools/" + school_imgs[school]]
        screen.blit(school_img, [188, 128 + y_shift * y_points])

        # School name
        text_panel1 = arial_font20.render(school, True, DarkText)
        screen.blit(text_panel1, [236, 135 + y_shift * y_points])

        y_points += 1

    # Buttons - previous and next ability school
    buttons.element_arrow_button(screen, "Up", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 432, 128, 19, 19, 1, 2)

    buttons.element_arrow_button(screen, "Down", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 432, 579, 19, 19, 1, 2)


def ability_selection_draw(screen, b):
    text_panel1 = tnr_font20.render("Abilities", True, TitleText)
    screen.blit(text_panel1, [456, 103])

    y_points = 0
    y_shift = 44

    for ability_name in b.list_of_abilities:
        # Background
        pygame.draw.polygon(screen, FillButton,
                            [[500, 128 + y_shift * y_points],
                             [698, 128 + y_shift * y_points],
                             [698, 167 + y_shift * y_points],
                             [500, 167 + y_shift * y_points]])

        if b.selected_ability == ability_name:
            # White border
            pygame.draw.polygon(screen, WhiteBorder, [[500, 128 + y_shift * y_points],
                                                      [698, 128 + y_shift * y_points],
                                                      [698, 167 + y_shift * y_points],
                                                      [500, 167 + y_shift * y_points]], 2)

        # Ability's icon
        back_img = game_stats.gf_misc_img_dict["Icons/paper_3_square_40"]
        screen.blit(back_img, [456, 128 + y_shift * y_points])

        img = ability_catalog.ability_cat[ability_name].img
        img_source = ability_catalog.ability_cat[ability_name].img_source
        ability_img = game_stats.gf_misc_img_dict[img_source + img]
        screen.blit(ability_img, [456, 128 + y_shift * y_points])

        # Ability name
        text_panel1 = arial_font20.render(ability_name, True, DarkText)
        screen.blit(text_panel1, [504, 135 + y_shift * y_points])

        y_points += 1

    # Buttons - previous and next ability
    buttons.element_arrow_button(screen, "Up", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 700, 128, 19, 19, 2, 2)

    buttons.element_arrow_button(screen, "Down", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                 700, 579, 19, 19, 2, 2)


def ability_description_draw(screen, b):
    text_panel1 = tnr_font20.render("Description", True, TitleText)
    screen.blit(text_panel1, [728, 103])

    y_points2 = 0
    y_shift2 = 20

    for text_line in b.ability_description:
        text_panel1 = arial_font14.render(text_line, True, DarkText)
        screen.blit(text_panel1, [728, 127 + y_points2 * y_shift2])

        y_points2 += 1


def ability_execution(screen, b):
    # Button - Execute
    border_color = "LineMainMenuColor1"
    if b.available_mana_reserve >= b.ability_mana_cost:
        border_color = "HighlightOption"
    buttons.element_button(screen, "Execute", "arial_font16", "DarkText", "FillButton", border_color, 970, 106,
                           100, 19, 25, 1, 2)

    text_panel1 = arial_font16.render("Execute", True, DarkText)
    screen.blit(text_panel1, [995, 107])

    text_panel1 = arial_font16.render("Mana reserve", True, TitleText)
    screen.blit(text_panel1, [971, 128])

    ability_img = game_stats.gf_misc_img_dict["Icons/mana_icon"]
    screen.blit(ability_img, [971, 149])

    text_panel1 = arial_font16.render(str(b.available_mana_reserve), True, TitleText)
    screen.blit(text_panel1, [995, 148])

    text_panel1 = arial_font16.render("Mana cost", True, TitleText)
    screen.blit(text_panel1, [971, 169])

    ability_img = game_stats.gf_misc_img_dict["Icons/mana_icon"]
    screen.blit(ability_img, [971, 190])

    text_panel1 = arial_font16.render(str(b.ability_mana_cost), True, TitleText)
    screen.blit(text_panel1, [995, 189])

    text_panel1 = arial_font16.render("Initiative cost", True, TitleText)
    screen.blit(text_panel1, [971, 210])

    ability_img = game_stats.gf_misc_img_dict["Icons/duration_icon"]
    screen.blit(ability_img, [974, 231])

    text_panel1 = arial_font16.render(str(b.initiative_cost), True, TitleText)
    screen.blit(text_panel1, [995, 230])


school_imgs = {"Overall" : "everything",
               "Tactics" : "tactics",
               "Divine" : "divine",
               "Elemental" : "elemental"}
