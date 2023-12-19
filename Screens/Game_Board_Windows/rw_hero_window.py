## Among Myth and Wonder
## rw_hero_window

import pygame.draw
import pygame.font

from Resources import game_stats

from Content import battle_attributes_catalog
from Content import hero_skill_information
from Content import hero_skill_catalog
from Content import artifact_information

WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]
WhiteBorder = [249, 238, 227, 200]
ApproveFieldColor = [0x00, 0x99, 0x00]

LineMainMenuColor1 = [0x60, 0x60, 0x60]
FillButton = [0xD8, 0xBD, 0xA2]
FieldColor = [0xA0, 0xA0, 0xA0]
SkillField = [0xBA, 0xBA, 0xBA]

HighlightOption = [0x00, 0xCC, 0xCC]
RockTunel = [0x89, 0x89, 0x89]

CancelFieldColor = [0xFF, 0x00, 0x00]
CancelElementsColor = [0x99, 0x00, 0x00]

BasicColor = [0x7C, 0xFC, 0x00]
AdvancedColor = [0x22, 0x71, 0xB3]
ExpertColor = [0x99, 0x66, 0xCC]
PerkColor = [0xD7, 0x6E, 0x00]

skills_color = {"Basic" : BasicColor,
                "Advanced" : AdvancedColor,
                "Expert" : ExpertColor,
                "Perk" : PerkColor}


tnr_font20 = pygame.font.SysFont('timesnewroman', 20)
tnr_font16 = pygame.font.SysFont('timesnewroman', 16)
tnr_font14 = pygame.font.SysFont('timesnewroman', 14)

arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)
arial_font13 = pygame.font.SysFont('arial', 13)
arial_font12 = pygame.font.SysFont('arial', 12)


def draw_hero_window(screen):
    hero = game_stats.rw_object
    # Draw top right panel with information about hero
    pygame.draw.polygon(screen, MainMenuColor, [[642, 80], [1278, 80], [1278, 540], [642, 540]])

    # Background
    pygame.draw.polygon(screen, FillButton, [[644, 111], [1276, 111], [1276, 538], [644, 538]])

    # Close skill tree window
    pygame.draw.polygon(screen, CancelFieldColor, [[1254, 85], [1273, 85], [1273, 104], [1254, 104]])
    pygame.draw.polygon(screen, CancelElementsColor, [[1254, 85], [1273, 85], [1273, 104], [1254, 104]], 2)
    pygame.draw.line(screen, CancelElementsColor, [1257, 88], [1270, 101], 2)
    pygame.draw.line(screen, CancelElementsColor, [1257, 101], [1270, 88], 2)

    # Header - Hero class and name
    text_panel = tnr_font20.render(hero.hero_class + " " + hero.name, True, TitleText)
    screen.blit(text_panel, [646, 87])

    # Border
    pygame.draw.polygon(screen, MainMenuColor, [[660, 126], [709, 126], [709, 175], [660, 175]], 1)
    # Background for image
    img = game_stats.gf_misc_img_dict["Icons/paper_2_square_48"]
    screen.blit(img, [661, 127])
    # Hero image
    img = game_stats.gf_hero_dict[str(hero.img_source) + "/" + str(hero.img) + "_r"]
    screen.blit(img, [661 + hero.x_offset, 127 + hero.y_offset])
    # screen.blit(img, [661, 131])
    # screen.blit(img, [661 + 7, 131 + 1])

    # Level
    text_panel1 = tnr_font14.render("Level " + str(hero.level), True, DarkText)
    screen.blit(text_panel1, [730, 113])

    # Experience
    text_panel1 = tnr_font14.render("Experience " + str(hero.experience), True, DarkText)
    screen.blit(text_panel1, [730, 131])

    # New attribute points
    text = "0"
    if hero.new_attribute_points > 0:
        text = "+" + str(hero.new_attribute_points)
    text_panel1 = tnr_font14.render("New attribute points " + text, True, DarkText)
    screen.blit(text_panel1, [730, 149])

    # New skill points
    text = "0"
    if hero.new_skill_points > 0:
        text = "+" + str(hero.new_skill_points)
    text_panel1 = tnr_font14.render("New skill points " + text, True, DarkText)
    screen.blit(text_panel1, [730, 167])

    # Battle attributes
    text_panel1 = tnr_font14.render("Battle attributes:", True, DarkText)
    screen.blit(text_panel1, [648, 191])

    # Magic power
    text_panel1 = tnr_font14.render("Magic power " + str(hero.magic_power), True, DarkText)
    screen.blit(text_panel1, [648, 211])

    # Knowledge
    total_knowledge = int(hero.knowledge)
    bonus_knowledge = 0
    if len(hero.inventory) > 0:
        for artifact in hero.inventory:
            for effect in artifact.effects:
                if effect.application == "Knowledge":
                    if effect.method == "addition":
                        total_knowledge += int(effect.quantity)
                        bonus_knowledge += int(effect.quantity)
    text = "Knowledge "
    if bonus_knowledge == 0:
        text += str(total_knowledge)
    else:
        text += str(total_knowledge) + " (+" + str(bonus_knowledge) + ")"
    text_panel1 = tnr_font14.render(text, True, DarkText)
    screen.blit(text_panel1, [648, 231])

    # Mana
    text_panel1 = tnr_font14.render("Mana " + str(hero.mana_reserve) + "/" +
                                    str(hero.max_mana_reserve), True, DarkText)
    screen.blit(text_panel1, [648, 251])

    # Button - skills option
    pygame.draw.polygon(screen, FillButton,
                        [[864, 112], [960, 112], [960, 132], [864, 132]])
    if game_stats.hero_information_option == "Skills":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[864, 112], [960, 112], [960, 132], [864, 132]], 2)

    text_panel1 = tnr_font16.render("Skills", True, DarkText)
    screen.blit(text_panel1, [895, 113])

    # Button - new attributes tree option
    pygame.draw.polygon(screen, FillButton,
                        [[864, 137], [960, 137], [960, 157], [864, 157]])
    if game_stats.hero_information_option == "Attributes tree":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[864, 137], [960, 137], [960, 157], [864, 157]], 2)

    text_panel1 = tnr_font16.render("Attributes tree", True, DarkText)
    screen.blit(text_panel1, [869, 138])

    # Button - Inventory of artifacts option
    pygame.draw.polygon(screen, FillButton,
                        [[864, 162], [960, 162], [960, 182], [864, 182]])
    if game_stats.hero_information_option == "Inventory":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[864, 162], [960, 162], [960, 182], [864, 182]], 2)

    text_panel1 = tnr_font16.render("Inventory", True, DarkText)
    screen.blit(text_panel1, [885, 163])

    # Button - Abilities
    pygame.draw.polygon(screen, FillButton,
                        [[864, 187], [960, 187], [960, 207], [864, 207]])
    if game_stats.hero_information_option == "Abilities":
        color1 = HighlightOption
    else:
        color1 = LineMainMenuColor1
    pygame.draw.polygon(screen, color1, [[864, 187], [960, 187], [960, 207], [864, 207]], 2)

    text_panel1 = tnr_font16.render("Abilities", True, DarkText)
    screen.blit(text_panel1, [888, 188])

    # Hero’s battle attributes
    y_points2 = 0
    y_shift2 = 20

    for pack in hero.attributes_list:
        # Background
        length = len(pack.attribute_list) - 1
        pygame.draw.polygon(screen, FieldColor,
                            [[646, 271 + y_shift2 * y_points2],
                             [838, 271 + y_shift2 * y_points2],
                             [838, 289 + y_shift2 * y_points2 + length * 20],
                             [646, 289 + y_shift2 * y_points2 + length * 20]])

        att_num = 0
        for att in pack.attribute_list:
            text = str(att.tag.capitalize()) + ": " + str(att.stat) + " +" + str(att.value)
            text_panel1 = arial_font12.render(text, True, DarkText)
            screen.blit(text_panel1, [648, 274 + y_shift2 * y_points2 + att_num * y_shift2])

            att_num += 1

        y_points2 += 1

    # Buttons - previous and next row of attributes
    pygame.draw.polygon(screen, RockTunel, [[841, 271], [860, 271], [860, 290], [841, 290]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[841, 271], [860, 271], [860, 290], [841, 290]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(845, 287), (851, 274), (857, 287)], 2)

    pygame.draw.polygon(screen, RockTunel, [[841, 517], [860, 517], [860, 536], [841, 536]])
    pygame.draw.polygon(screen, LineMainMenuColor1, [[841, 517], [860, 517], [860, 536], [841, 536]], 2)
    pygame.draw.lines(screen, LineMainMenuColor1, False, [(845, 520), (851, 534), (857, 520)], 2)

    # Skills and perks
    if game_stats.hero_information_option == "Skills":
        y_shift = 45
        y_points = 0
        for skill in hero.skills:
            # y = y_shift * y_points
            y = y_shift * skill.screen_position[1]
            x = y_shift * skill.screen_position[0]
            # x = 0
            # x_points = 0
            # y_points2 = 0
            # y2 = 0
            # if skill.skill_type == "Perk":
            #     y2_counting = True
            #     x_counting = True
            #     for skill2 in hero.skills:
            #         if skill2.skill_type == "Skill":
            #             if skill2.theme == skill.theme:
            #                 y2_counting = False
            #             else:
            #                 if y2_counting:
            #                     y_points2 += 1
            #         else:
            #             if skill2.theme == skill.theme:
            #                 if skill2.name == skill.name:
            #                     x_counting = False
            #                     x_points += 1
            #                 else:
            #                     if x_counting:
            #                         x_points += 1
            #
            #     x = x_points * y_shift
            #     y2 = y_points2 * y_shift
            #     y = 0

            # Border
            pygame.draw.polygon(screen, skills_color[skill.skill_level], [[864 + x, 271 + y],
                                                                          [905 + x, 271 + y],
                                                                          [905 + x, 312 + y],
                                                                          [864 + x, 312 + y]], 1)

            # Background
            img = game_stats.gf_misc_img_dict["Icons/paper_square_40"]
            screen.blit(img, [865 + x, 272 + y])

            # Skill or perk image
            img = game_stats.gf_skills_dict[skill.img]
            screen.blit(img, [865 + x, 272 + y])

            y_points += 1

        # pygame.draw.polygon(screen, SkillField,
        #                     [[1039, 272 + y],
        #                      [1180, 272 + y],
        #                      [1180, 311 + y],
        #                      [1039, 311 + y]])

        if game_stats.selected_skill_info is not None:
            text_panel1 = arial_font16.render(game_stats.selected_skill_info.name, True, DarkText)
            screen.blit(text_panel1, [1041, 272])

            y_shift3 = 20
            y_points3 = 0
            for line in hero_skill_information.skill_desc[game_stats.selected_skill_info.name]:
                text_panel1 = arial_font14.render(line, True, DarkText)
                screen.blit(text_panel1, [1041, 290 + y_shift3 * y_points3])

                y_points3 += 1

        # Button - New skills
        pygame.draw.polygon(screen, FillButton,
                            [[1041, 515], [1130, 515], [1130, 535], [1041, 535]])
        if hero.new_skill_points > 0:
            color1 = HighlightOption
        else:
            color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, color1, [[1041, 515], [1130, 515], [1130, 535], [1041, 535]], 2)

        text_panel1 = tnr_font16.render("New skills", True, DarkText)
        screen.blit(text_panel1, [1053, 517])

    # Attributes tree
    elif game_stats.hero_information_option == "Attributes tree":
        # Buttons - previous and next level
        ybase = 271
        pygame.draw.polygon(screen, RockTunel, [[864, ybase], [883, ybase], [883, ybase + 19], [864, ybase + 19]])
        pygame.draw.polygon(screen, LineMainMenuColor1,
                            [[864, ybase], [883, ybase], [883, ybase + 19], [864, ybase + 19]],
                            2)
        pygame.draw.lines(screen, LineMainMenuColor1, False, [(880, ybase + 3), (868, ybase + 10), (880, ybase + 16)],
                          2)

        pygame.draw.polygon(screen, RockTunel, [[1254, ybase], [1273, ybase], [1273, ybase + 19], [1254, ybase + 19]])
        pygame.draw.polygon(screen, LineMainMenuColor1,
                            [[1254, ybase], [1273, ybase], [1273, ybase + 19], [1254, ybase + 19]],
                            2)
        pygame.draw.lines(screen, LineMainMenuColor1, False,
                          [(1257, ybase + 3), (1269, ybase + 10), (1257, ybase + 16)], 2)

        # level N
        text_panel = tnr_font20.render("Level " + str(game_stats.skill_tree_level_index + 1), True, TitleText)
        screen.blit(text_panel, [940, 269])

        # level N + 1
        text_panel = tnr_font20.render("Level " + str(game_stats.skill_tree_level_index + 2), True, TitleText)
        screen.blit(text_panel, [1120, 269])

        # 1 row of battle attributes
        y_points2 = 0
        y_shift2 = 20
        pack_num = 0

        for pack in battle_attributes_catalog.basic_heroes_attributes[hero.hero_class][
            game_stats.skill_tree_level_index - 1]:
            # Background
            # print("skill_tree_level_index " + str(game_stats.skill_tree_level_index) +
            #       " attribute_points_used " + str(hero.attribute_points_used))

            length = len(pack.attribute_list) - 1
            pygame.draw.polygon(screen, FieldColor,
                                [[864, 293 + y_shift2 * y_points2],
                                 [1066, 293 + y_shift2 * y_points2],
                                 [1066, 293 + 18 + y_shift2 * y_points2 + length * 20],
                                 [864, 293 + 18 + y_shift2 * y_points2 + length * 20]])

            if hero.new_attribute_points > 0 and game_stats.skill_tree_level_index == hero.attribute_points_used:
                color = TitleText
                if game_stats.selected_new_attribute is not None:
                    if game_stats.selected_new_attribute == pack_num:
                        color = HighlightOption
                pygame.draw.polygon(screen, color,
                                    [[864, 293 + y_shift2 * y_points2],
                                     [1066, 293 + y_shift2 * y_points2],
                                     [1066, 293 + 18 + y_shift2 * y_points2 + length * 20],
                                     [864, 293 + 18 + y_shift2 * y_points2 + length * 20]], 1)

            att_num = 0
            for att in pack.attribute_list:
                text = str(att.tag.capitalize()) + ": " + str(att.stat) + " +" + str(att.value)
                text_panel1 = arial_font12.render(text, True, DarkText)
                screen.blit(text_panel1, [866, 296 + y_shift2 * y_points2 + att_num * y_shift2])

                att_num += 1

            y_points2 += 1
            pack_num += 1

        # 2 row of battle attributes
        y_points2 = 0
        y_shift2 = 20

        for pack in battle_attributes_catalog.basic_heroes_attributes[hero.hero_class][
            game_stats.skill_tree_level_index]:
            # Background
            length = len(pack.attribute_list) - 1
            pygame.draw.polygon(screen, FieldColor,
                                [[1072, 293 + y_shift2 * y_points2],
                                 [1274, 293 + y_shift2 * y_points2],
                                 [1274, 293 + 18 + y_shift2 * y_points2 + length * 20],
                                 [1072, 293 + 18 + y_shift2 * y_points2 + length * 20]])

            att_num = 0
            for att in pack.attribute_list:
                text = str(att.tag.capitalize()) + ": " + str(att.stat) + " +" + str(att.value)
                text_panel1 = arial_font12.render(text, True, DarkText)
                screen.blit(text_panel1, [1074, 296 + y_shift2 * y_points2 + att_num * y_shift2])

                att_num += 1

            y_points2 += 1

        # Button - Confirm new attribute selection
        pygame.draw.polygon(screen, FillButton,
                            [[1001, 515], [1130, 515], [1130, 535], [1001, 535]])
        if game_stats.selected_new_attribute is not None:
            pygame.draw.polygon(screen, HighlightOption, [[1001, 515], [1130, 515], [1130, 535], [1001, 535]], 2)
            text_panel1 = arial_font14.render("Confirm selection", True, DarkText)
            screen.blit(text_panel1, [1015, 516])

    # New skills and perks
    elif game_stats.hero_information_option == "New skills":
        text_panel1 = arial_font14.render("Choose one skill or perk", True, DarkText)
        screen.blit(text_panel1, [870, 272])

        y_shift = 45
        y_points = 0
        for skill in hero.new_skills:
            y = y_shift * y_points

            # Border
            skill_level = hero_skill_catalog.hero_skill_data[skill][3]
            color = skills_color[skill_level]
            if game_stats.selected_new_skill is not None:
                if game_stats.selected_new_skill == skill:
                    color = TitleText
            pygame.draw.polygon(screen, color, [[864, 291 + y],
                                                [905, 291 + y],
                                                [905, 332 + y],
                                                [864, 332 + y]], 1)

            # Background
            img = game_stats.gf_misc_img_dict["Icons/paper_square_40"]
            screen.blit(img, [865, 292 + y])

            # Skill or perk image
            skill_img = hero_skill_catalog.hero_skill_data[skill][0]
            img = game_stats.gf_skills_dict[skill_img]
            screen.blit(img, [865, 292 + y])

            y_points += 1

        if game_stats.selected_new_skill is not None:
            text_panel1 = arial_font14.render(game_stats.selected_new_skill, True, DarkText)
            screen.blit(text_panel1, [1041, 272])

            y_shift3 = 20
            y_points3 = 0
            for line in hero_skill_information.skill_desc[game_stats.selected_new_skill]:
                text_panel1 = arial_font14.render(line, True, DarkText)
                screen.blit(text_panel1, [1041, 290 + y_shift3 * y_points3])

                y_points3 += 1

        # Button - Confirm new skill
        pygame.draw.polygon(screen, FillButton,
                            [[1001, 515], [1130, 515], [1130, 535], [1001, 535]])
        if game_stats.selected_new_skill is not None:
            color = HighlightOption
        else:
            color = LineMainMenuColor1
        pygame.draw.polygon(screen, color, [[1001, 515], [1130, 515], [1130, 535], [1001, 535]], 2)
        text_panel1 = arial_font14.render("Confirm selection", True, DarkText)
        screen.blit(text_panel1, [1015, 516])

    # Inventory of artifacts
    elif game_stats.hero_information_option == "Inventory":
        text_panel1 = arial_font16.render("Hero's artifacts", True, DarkText)
        screen.blit(text_panel1, [864, 271])

        y_shift = 45
        y_points = 0
        for artifact in hero.inventory:
            y = y_shift * y_points

            # Border
            border_color = DarkText
            if game_stats.selected_artifact_info is not None:
                if artifact.name == game_stats.selected_artifact_info.name \
                        and game_stats.artifact_focus == "Hero's inventory":
                    border_color = ApproveFieldColor
            pygame.draw.polygon(screen, border_color, [[864 + y, 291],
                                                       [905 + y, 291],
                                                       [905 + y, 332],
                                                       [864 + y, 332]], 1)

            # Background
            img = game_stats.gf_misc_img_dict["Icons/paper_square_40"]
            screen.blit(img, [865 + y, 292])

            # Artifact image
            img = game_stats.gf_artifact_dict[artifact.img]
            screen.blit(img, [865 + y, 292])

            y_points += 1

        # Realm's artifact collection
        text_panel1 = arial_font16.render("Realm's artifact collection", True, DarkText)
        screen.blit(text_panel1, [864, 336])

        x_shift = 45
        x_points = 0
        num = 1
        for artifact in game_stats.realm_artifact_collection:
            x = x_shift * x_points

            # Border
            border_color = DarkText
            if game_stats.selected_artifact_info is not None:
                if artifact.name == game_stats.selected_artifact_info.name \
                        and game_stats.artifact_focus == "Realm's artifact collection":
                    border_color = ApproveFieldColor
            pygame.draw.polygon(screen, border_color, [[864 + x, 356],
                                                       [905 + x, 356],
                                                       [905 + x, 397],
                                                       [864 + x, 397]], 1)

            # Background
            img = game_stats.gf_misc_img_dict["Icons/paper_square_40"]
            screen.blit(img, [865 + x, 357])

            # Artifact image
            img = game_stats.gf_artifact_dict[artifact.img]
            screen.blit(img, [865 + x, 357])

            x_points += 1
            num += 1
            if num > 4:
                break

        if game_stats.selected_artifact_info is not None:
            # Artifact name
            text_panel1 = arial_font16.render(game_stats.selected_artifact_info.name, True, DarkText)
            screen.blit(text_panel1, [1061, 272])

            # Description
            y_shift3 = 20
            y_points3 = 0
            for line in artifact_information.artifact_desc[game_stats.selected_artifact_info.name]:
                text_panel1 = arial_font14.render(line, True, DarkText)
                screen.blit(text_panel1, [1061, 290 + y_shift3 * y_points3])

                y_points3 += 1

            # Button - remove artifact
            pygame.draw.polygon(screen, FillButton,
                                [[864, 491], [965, 491], [965, 511], [864, 511]])
            if game_stats.artifact_focus == "Hero's inventory":
                color1 = HighlightOption
            else:
                color1 = LineMainMenuColor1
            pygame.draw.polygon(screen, color1, [[864, 491], [965, 491], [965, 511], [864, 511]], 2)

            text_panel1 = arial_font16.render("Remove artifact", True, DarkText)
            screen.blit(text_panel1, [868, 492])

            # Button - equip new artifact
            pygame.draw.polygon(screen, FillButton,
                                [[864, 516], [965, 516], [965, 536], [864, 536]])
            if game_stats.artifact_focus == "Realm's artifact collection":
                color1 = HighlightOption
            else:
                color1 = LineMainMenuColor1
            pygame.draw.polygon(screen, color1, [[864, 516], [965, 516], [965, 536], [864, 536]], 2)

            text_panel1 = arial_font16.render("Equip artifact", True, DarkText)
            screen.blit(text_panel1, [878, 517])
