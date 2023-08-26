## Miracle battles!

import pygame.draw
import pygame.font

from Resources import game_stats

from Content import artifact_assortment
from Content import artifact_imgs_cat
from Content import artifact_information
from Content import skills_curriculum
from Content import hero_skill_catalog
from Content import hero_skill_information

WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
LineMainMenuColor1 = [0x60, 0x60, 0x60]
FillButton = [0xD8, 0xBD, 0xA2]

HighlightOption = [0x00, 0xCC, 0xCC]

DarkText = [0x11, 0x11, 0x11]
ApproveFieldColor = [0x00, 0x99, 0x00]
BasicColor = [0x7C, 0xFC, 0x00]

tnr_font16 = pygame.font.SysFont('timesnewroman', 16)
tnr_font14 = pygame.font.SysFont('timesnewroman', 14)

arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)
arial_font12 = pygame.font.SysFont('arial', 12)


def draw_kl_artifact_market(screen):
    details_artifact_market(screen, "KL artifact market")


def draw_kl_school_of_magic(screen):
    details_school_of_magic(screen, "KL School of magic")


# Common details
def details_artifact_market(screen, building):
    text_panel1 = tnr_font16.render("For sale", True, DarkText)
    screen.blit(text_panel1, [650, 128])

    assortment = artifact_assortment.stock_by_place[building]

    x_shift = 45
    x_points = 0
    for artifact in assortment:
        x = x_shift * x_points

        # Border
        border_color = DarkText
        if game_stats.selected_artifact_info is not None:
            if artifact == game_stats.selected_artifact_info.name \
                    and game_stats.artifact_focus is None:
                border_color = ApproveFieldColor
        pygame.draw.polygon(screen, border_color, [[650 + x, 148],
                                                   [691 + x, 148],
                                                   [691 + x, 189],
                                                   [650 + x, 189]], 1)

        # Background
        img = game_stats.gf_misc_img_dict["Icons/paper_square_40"]
        screen.blit(img, [651 + x, 149])

        # Artifact image
        img = game_stats.gf_artifact_dict[artifact_imgs_cat.imgs_catalog[artifact]]
        screen.blit(img, [651 + x, 149])

        x_points += 1

    if game_stats.selected_artifact_info is not None:
        text_panel1 = arial_font16.render(game_stats.selected_artifact_info.name, True, DarkText)
        screen.blit(text_panel1, [930, 85])

        y_shift = 20
        y_points = 0
        for line in artifact_information.artifact_desc[game_stats.selected_artifact_info.name]:
            text_panel1 = arial_font14.render(line, True, DarkText)
            screen.blit(text_panel1, [930, 103 + y_shift * y_points])

            y_points += 1

        # Price
        text_panel1 = arial_font16.render("Price", True, DarkText)
        screen.blit(text_panel1, [651, 194])

        # Florins icon
        icon_img = game_stats.gf_misc_img_dict["resource_florins"]
        icon_img.set_colorkey(WhiteColor)
        screen.blit(icon_img, (691, 196))

        # Value
        text_panel1 = arial_font16.render(str(game_stats.selected_artifact_info.price), True, DarkText)
        screen.blit(text_panel1, [710, 194])

    # Button - buy artifact for hero
    pygame.draw.polygon(screen, FillButton,
                        [[651, 217], [790, 217], [790, 237], [651, 237]])
    color1 = LineMainMenuColor1
    if game_stats.enough_resources_to_pay and game_stats.hero_in_settlement and not game_stats.inventory_is_full:
        if not game_stats.already_has_an_artifact:
            color1 = HighlightOption
    pygame.draw.polygon(screen, color1, [[651, 217], [790, 217], [790, 237], [651, 237]], 2)

    text_panel1 = arial_font14.render("Buy artifact for hero", True, DarkText)
    screen.blit(text_panel1, [660, 220])

    # Button - buy artifact for realm
    pygame.draw.polygon(screen, FillButton,
                        [[651, 247], [790, 247], [790, 267], [651, 267]])
    if game_stats.enough_resources_to_pay:
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[651, 247], [790, 247], [790, 267], [651, 267]], 2)

    text_panel1 = arial_font14.render("Buy artifact for realm", True, DarkText)
    screen.blit(text_panel1, [656, 250])

    # Hero's inventory
    text_panel1 = arial_font16.render("Hero's inventory", True, DarkText)
    screen.blit(text_panel1, [651, 273])

    if game_stats.hero_inventory is not None:
        x_shift = 45
        x_points = 0
        for artifact in game_stats.hero_inventory:
            x = x_shift * x_points

            # Border
            border_color = DarkText
            if game_stats.selected_artifact_info is not None:
                if artifact.name == game_stats.selected_artifact_info.name \
                        and game_stats.artifact_focus == "Hero's inventory":
                    border_color = ApproveFieldColor
            pygame.draw.polygon(screen, border_color, [[650 + x, 293],
                                                       [691 + x, 293],
                                                       [691 + x, 334],
                                                       [650 + x, 334]], 1)

            # Background
            img = game_stats.gf_misc_img_dict["Icons/paper_square_40"]
            screen.blit(img, [651 + x, 294])

            # Artifact image
            img = game_stats.gf_artifact_dict[artifact.img]
            screen.blit(img, [651 + x, 294])

            x_points += 1

    # Realm's artifact collection
    text_panel1 = arial_font16.render("Realm's artifact collection", True, DarkText)
    screen.blit(text_panel1, [651, 340])

    x_shift = 45
    x_points = 0
    for artifact in game_stats.realm_artifact_collection:
        x = x_shift * x_points

        # Border
        border_color = DarkText
        if game_stats.selected_artifact_info is not None:
            if artifact.name == game_stats.selected_artifact_info.name \
                    and game_stats.artifact_focus == "Realm's artifact collection":
                border_color = ApproveFieldColor
        pygame.draw.polygon(screen, border_color, [[650 + x, 360],
                                                   [691 + x, 360],
                                                   [691 + x, 401],
                                                   [650 + x, 401]], 1)

        # Background
        img = game_stats.gf_misc_img_dict["Icons/paper_square_40"]
        screen.blit(img, [651 + x, 361])

        # Artifact image
        img = game_stats.gf_artifact_dict[artifact.img]
        screen.blit(img, [651 + x, 361])

        x_points += 1


def details_school_of_magic(screen, building):
    text_panel1 = tnr_font16.render("Skills", True, DarkText)
    screen.blit(text_panel1, [650, 128])

    curriculum = skills_curriculum.curriculum_by_school[building]

    x_shift = 45
    x_points = 0

    for skill in curriculum:
        x = x_shift * x_points

        # Border
        border_color = BasicColor
        if game_stats.selected_new_skill is not None:
            if skill == game_stats.selected_new_skill.name:
                border_color = ApproveFieldColor
        pygame.draw.polygon(screen, border_color, [[650 + x, 148],
                                                   [691 + x, 148],
                                                   [691 + x, 189],
                                                   [650 + x, 189]], 1)

        # Background
        img = game_stats.gf_misc_img_dict["Icons/paper_square_40"]
        screen.blit(img, [651 + x, 149])

        # Artifact image
        skill_img = hero_skill_catalog.hero_skill_data[skill][0]
        img = game_stats.gf_skills_dict[skill_img]
        screen.blit(img, [651 + x, 149])

        x_points += 1

    if game_stats.selected_new_skill is not None:
        text_panel1 = arial_font16.render(game_stats.selected_new_skill.name, True, DarkText)
        screen.blit(text_panel1, [930, 85])

        y_shift = 20
        y_points = 0
        for line in hero_skill_information.skill_desc[game_stats.selected_new_skill.name]:
            text_panel1 = arial_font14.render(line, True, DarkText)
            screen.blit(text_panel1, [930, 103 + y_shift * y_points])

            y_points += 1

    # Price
    text_panel1 = arial_font16.render("Price", True, DarkText)
    screen.blit(text_panel1, [651, 194])

    # Florins icon
    icon_img = game_stats.gf_misc_img_dict["resource_florins"]
    screen.blit(icon_img, (691, 196))

    # Value
    text_panel1 = arial_font16.render(str(2000), True, DarkText)
    screen.blit(text_panel1, [710, 194])

    # Button - buy artifact for hero
    pygame.draw.polygon(screen, FillButton,
                        [[651, 217], [760, 217], [760, 237], [651, 237]])
    color1 = LineMainMenuColor1
    if game_stats.enough_resources_to_pay and game_stats.hero_in_settlement \
            and game_stats.selected_new_skill is not None and game_stats.hero_doesnt_know_this_skill:
        color1 = HighlightOption
    pygame.draw.polygon(screen, color1, [[651, 217], [760, 217], [760, 237], [651, 237]], 2)

    text_panel1 = arial_font14.render("Learn new skill", True, DarkText)
    screen.blit(text_panel1, [660, 220])


structure_cat = {"KL artifact market": draw_kl_artifact_market,
                 "KL School of magic": draw_kl_school_of_magic}
