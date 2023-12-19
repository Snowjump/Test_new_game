## det_settlement_heroes
## Among Myth and Wonder

import pygame.draw
import pygame.font

from Resources import game_stats
from Resources import game_obj
from Content import new_heroes_catalog
from Content import starting_skills

WhiteColor = [255, 255, 255]

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]

LineMainMenuColor1 = [0x60, 0x60, 0x60]
FillButton = [0xD8, 0xBD, 0xA2]
FieldColor = [0xA0, 0xA0, 0xA0]
HighlightOption = [0x00, 0xCC, 0xCC]
RockTunel = [0x89, 0x89, 0x89]

tnr_font26 = pygame.font.SysFont('timesnewroman', 26)
tnr_font20 = pygame.font.SysFont('timesnewroman', 20)
arial_font20 = pygame.font.SysFont('arial', 20)
arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)
arial_font13 = pygame.font.SysFont('arial', 13)


def draw_heroes(screen, settlement):
    # Background
    pygame.draw.polygon(screen, FillButton,
                        [[283, 111],
                         [637, 111],
                         [637, 538],
                         [283, 538]])

    # x = int(game_stats.selected_tile[0])
    # y = int(game_stats.selected_tile[1])
    # TileNum = (y - 1) * game_stats.cur_level_width + x - 1
    TileNum = settlement.location

    # units_length = 0
    no_hero_in_army = False
    for army in game_obj.game_armies:
        if army.army_id == game_obj.game_map[TileNum].army_id:
            # units_length = len(army.units)
            if army.hero is None:
                no_hero_in_army = True
            break

    # Basic heroes category
    text_panel1 = tnr_font20.render("Basic heroes", True, TitleText)
    screen.blit(text_panel1, [16, 116])

    pygame.draw.line(screen, DarkText, [3, 137], [257, 137], 2)

    y_points = 0
    y_shift = 52

    for hero in new_heroes_catalog.heroes_classes_dict_by_alignment[settlement.alignment]:
        # Background
        pygame.draw.polygon(screen, FillButton,
                            [[54, 141 + y_shift * y_points],
                             [257, 141 + y_shift * y_points],
                             [257, 188 + y_shift * y_points],
                             [54, 188 + y_shift * y_points]])

        # Hero's icon
        back_img = game_stats.gf_misc_img_dict["Icons/paper_3_square_48"]
        screen.blit(back_img, [3, 141 + y_shift * y_points])

        hero_info = new_heroes_catalog.heroes_img_dict_by_alignment[settlement.alignment][hero]
        # Previous code
        # hero_img = pygame.image.load(
        #     'img/Heroes/' + str(hero_info[1]) + "/" + str(hero_info[0]) + '.png')
        # hero_img.set_colorkey(WhiteColor)
        hero_img = game_stats.gf_hero_dict[hero_info[1] + "/" + hero_info[0] + "_r"]
        screen.blit(hero_img, [3 + (hero_info[2]), 141 + y_shift * y_points + (hero_info[3])])

        # Hero class name
        text_panel1 = arial_font20.render(hero, True, DarkText)
        screen.blit(text_panel1, [58, 152 + y_shift * y_points])

        y_points += 1

    if game_stats.hero_for_hire is not None:
        # Button - skill tree
        pygame.draw.polygon(screen, FillButton,
                            [[286, 112], [396, 112], [396, 132], [286, 132]])
        pygame.draw.polygon(screen, LineMainMenuColor1, [[286, 112], [396, 112], [396, 132], [286, 132]], 2)

        text_panel1 = arial_font14.render("Skill tree", True, DarkText)
        screen.blit(text_panel1, [314, 115])

        # Button - hire hero

        color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, FillButton,
                            [[406, 112], [516, 112], [516, 132], [406, 132]])
        # if units_length > 4 and no_hero_in_army and game_stats.enough_resources_to_pay:
        if no_hero_in_army and game_stats.enough_resources_to_pay:
            color1 = HighlightOption
        else:
            color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, color1, [[406, 112], [516, 112], [516, 132], [406, 132]], 2)

        text_panel1 = arial_font14.render("Hire hero", True, DarkText)
        screen.blit(text_panel1, [433, 115])

        # Hero class
        text = str(game_stats.hero_for_hire[0])
        text_panel1 = arial_font14.render(text, True, DarkText)
        screen.blit(text_panel1, [286, 135])

        # Level
        text = "Level 1"
        text_panel1 = arial_font14.render(text, True, DarkText)
        screen.blit(text_panel1, [286, 155])

        # Battle attributes
        text = "Battle attributes:"
        text_panel1 = arial_font14.render(text, True, DarkText)
        screen.blit(text_panel1, [286, 175])

        # Magic power
        text = "Magic power " + str(game_stats.hero_for_hire[1])
        text_panel1 = arial_font14.render(text, True, DarkText)
        screen.blit(text_panel1, [286, 195])

        # Knowledge
        text = "Knowledge " + str(game_stats.hero_for_hire[2])
        text_panel1 = arial_font14.render(text, True, DarkText)
        screen.blit(text_panel1, [286, 215])

        # Attributes
        if len(game_stats.hero_for_hire[4]) > 0:
            attributes = game_stats.hero_for_hire[8]

            y_points2 = 0
            y_shift2 = 20

            for pack in attributes:
                # Background
                length = len(pack.attribute_list) - 1
                pygame.draw.polygon(screen, FieldColor,
                                    [[285, 236 + y_shift2 * y_points2],
                                     [450, 236 + y_shift2 * y_points2],
                                     [450, 254 + y_shift2 * y_points2 + length * 20],
                                     [285, 254 + y_shift2 * y_points2 + length * 20]])

                att_num = 0
                for att in pack.attribute_list:

                    text = str(att.tag.capitalize()) + ": " + str(att.stat) + " +" + str(att.value)
                    text_panel1 = arial_font13.render(text, True, DarkText)
                    screen.blit(text_panel1, [286, 238 + y_shift2 * y_points2 + att_num * y_shift2])

                    att_num += 1

                y_points2 += 1

        # Black vertical line
        pygame.draw.line(screen, LineMainMenuColor1, [453, 175], [453, 315], 1)

        # Battle attributes
        text = "Starting skills:"
        text_panel1 = arial_font14.render(text, True, DarkText)
        screen.blit(text_panel1, [457, 175])

        # First skill
        pygame.draw.polygon(screen, FieldColor,
                            [[456, 196],
                             [613, 196],
                             [613, 214],
                             [456, 214]])

        if not starting_skills.locked_first_skill_check[game_stats.hero_for_hire[0]]:
            text = starting_skills.starting_skills_by_class[game_stats.hero_for_hire[0]][
                game_stats.first_starting_skill]

            # Next first skill
            pygame.draw.polygon(screen, RockTunel, [[615, 196], [634, 196], [634, 196 + 18], [615, 196 + 18]])
            pygame.draw.polygon(screen, LineMainMenuColor1,
                                [[615, 196], [634, 196], [634, 196 + 18], [615, 196 + 18]],
                                1)
            pygame.draw.lines(screen, LineMainMenuColor1, False, [(618, 196 + 2), (631, 196 + 9), (618, 196 + 15)], 2)

        else:
            text = starting_skills.locked_first_skill_by_class[game_stats.hero_for_hire[0]]
        text_panel1 = arial_font13.render(text, True, DarkText)
        screen.blit(text_panel1, [458, 198])

        # Second skill
        pygame.draw.polygon(screen, FieldColor,
                            [[456, 216],
                             [613, 216],
                             [613, 234],
                             [456, 234]])

        text = starting_skills.starting_skills_by_class[game_stats.hero_for_hire[0]][game_stats.second_starting_skill]
        text_panel1 = arial_font13.render(text, True, DarkText)
        screen.blit(text_panel1, [458, 218])

        # Next second skill
        pygame.draw.polygon(screen, RockTunel, [[615, 216], [634, 216], [634, 216 + 18], [615, 216 + 18]])
        pygame.draw.polygon(screen, LineMainMenuColor1,
                            [[615, 216], [634, 216], [634, 216 + 18], [615, 216 + 18]],
                            1)
        pygame.draw.lines(screen, LineMainMenuColor1, False, [(618, 216 + 2), (631, 216 + 9), (618, 216 + 15)], 2)
