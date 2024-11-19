## Among Myth and Wonder
## info_panel_army

import pygame.draw
import math

from Screens.colors_catalog import *
from Screens.fonts_catalog import *
from Screens.Interface_Elements import buttons

from Resources import graphics_classes
from Resources import game_stats
from Resources import common_selects

from Screens import draw_movement_arrows


class Army_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        self.army = common_selects.select_army_by_id(game_stats.selected_army)
        self.power = common_selects.select_realm_by_name(self.army.owner)

    def draw_panel(self, screen):
        yVar = game_stats.game_window_height - 800
        self.draw_movement_arrows_method(screen)
        self.draw_border_line(screen)
        self.draw_panel_background(screen, yVar)
        self.draw_army_button(screen, yVar)
        self.draw_army_info(screen, yVar)
        self.draw_hero_info(screen, yVar)
        self.draw_units(screen, yVar)

    def draw_movement_arrows_method(self, screen):
        # Draw movement arrows
        if len(self.army.path_arrows) > 0:
            draw_movement_arrows.arrow_icon(screen, self.army.route, self.army.path_arrows)

    def draw_border_line(self, screen):
        # Border line around selected army
        x = int(self.army.posxy[0]) - int(game_stats.pov_pos[0])
        y = int(self.army.posxy[1]) - int(game_stats.pov_pos[1])
        pygame.draw.polygon(screen, WhiteBorder,
                            [[(x - 1) * 48, (y - 1) * 48], [(x - 1) * 48 + 47, (y - 1) * 48],
                             [(x - 1) * 48 + 47, (y - 1) * 48 + 47], [(x - 1) * 48, (y - 1) * 48 + 47]], 1)

    def draw_panel_background(self, screen, yVar):
        # Lower panel
        pygame.draw.polygon(screen, MainMenuColor,
                            [[200, 650 + yVar], [1080, 650 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    def draw_army_button(self, screen, yVar):
        # Army button
        pygame.draw.polygon(screen, FieldColor,
                            [[200, 627 + yVar], [260, 627 + yVar], [260, 649 + yVar], [200, 649 + yVar]])
        if game_stats.selected_object == "Army":
            color1 = HighlightOption
        else:
            color1 = LineMainMenuColor1
        pygame.draw.polygon(screen, color1,
                            [[200, 627 + yVar], [260, 627 + yVar], [260, 649 + yVar], [200, 649 + yVar]], 3)
        text_panel5 = tnr_font20.render("Army", True, DarkText)
        screen.blit(text_panel5, [206, 627 + yVar])

    def draw_army_info(self, screen, yVar):
        self.draw_ownership_info(screen, yVar)

    def draw_ownership_info(self, screen, yVar):
        # Ownership
        if self.army.owner == "Neutral":
            text_panel = tnr_font18.render("Neutral", True, TitleText)
            screen.blit(text_panel, [240, 654 + yVar])
        else:
            power = common_selects.select_realm_by_name(self.army.owner)
            # Country's name
            text_panel = tnr_font18.render(power.name, True, TitleText)
            screen.blit(text_panel, [240, 654 + yVar])

            # Flag
            pygame.draw.polygon(screen, FlagColors[power.f_color],
                                [[205, 654 + yVar], [235, 654 + yVar], [235, 664 + yVar],
                                 [205, 664 + yVar]])
            pygame.draw.polygon(screen, FlagColors[power.s_color],
                                [[205, 665 + yVar], [235, 665 + yVar], [235, 674 + yVar],
                                 [205, 674 + yVar]])

    def draw_hero_info(self, screen, yVar):
        # Hero
        if self.army.hero is not None:
            # Name
            text_panel = tnr_font18.render(self.army.hero.name, True, TitleText)
            screen.blit(text_panel, [288, 721 + yVar])

            # Class
            text_panel = tnr_font16.render(self.army.hero.hero_class, True, DarkText)
            screen.blit(text_panel, [288, 741 + yVar])

            # Level
            text_panel = tnr_font16.render("Level " + str(self.army.hero.level), True, DarkText)
            screen.blit(text_panel, [288, 761 + yVar])

            # Hero image
            img = self.army.hero.img
            source = self.army.hero.img_source
            # Previous code
            # army_img = pygame.image.load('img/Heroes/' + str(source) + "/" + str(img) + '.png')
            # army_img.set_colorkey(WhiteColor)
            x_offset = self.army.hero.x_offset
            y_offset = self.army.hero.y_offset
            side = "_l"
            if self.army.right_side:
                side = "_r"
            # New code
            army_img = game_stats.gf_hero_dict[source + "/" + img + side]
            screen.blit(army_img, (203 + x_offset, 718 + yVar + y_offset))

            # Open hero window
            buttons.element_button(screen, "Hero", "tnr_font16", "DarkText", None, "HighlightOption", 203, 776 + yVar,
                                   50, 18, 10, 1, 2)
            # border_color = HighlightOption
            # pygame.draw.polygon(screen, border_color,
            #                     [[203, 776 + yVar], [253, 776 + yVar], [253, 794 + yVar], [203, 794 + yVar]], 2)
            # text_panel1 = tnr_font16.render("Hero", True, DarkText)
            # screen.blit(text_panel1, [213, 777 + yVar])

            # New attribute or skill points are available
            if self.army.hero.new_attribute_points > 0 or self.army.hero.new_skill_points > 0:
                icon_img = game_stats.gf_misc_img_dict["Icons/plus_sign_24_2"]
                # army_img.set_colorkey(WhiteColor)
                screen.blit(icon_img, (258, 774 + yVar))

    def draw_units(self, screen, yVar):
        movement_points_left = -1
        least_max_movement_points = -1
        # Display units
        side = "_l"
        if self.army.right_side:
            side = "_r"

        # Units
        if len(self.army.units) > 0:
            number = 0
            for unit in self.army.units:
                x_pos = 430 + math.floor(number % 10) * 52
                y_pos = 654 + yVar + math.floor(number / 10) * 57
                # New code
                if unit.img_width > 44 or unit.img_height > 44:
                    army_img = game_stats.gf_regiment_dict[unit.img_source + "/"
                                                           + unit.img + side]
                    if unit.img_width > 44:
                        proportion = 44 / unit.img_width
                        army_img = pygame.transform.scale(army_img,
                                                          (44,
                                                           int(unit.img_height * proportion)))
                        x_offset = 3
                        y_offset = (48 - (unit.img_height * proportion)) / 2
                    else:
                        proportion = 44 / unit.img_height
                        army_img = pygame.transform.scale(army_img,
                                                          (int(unit.img_width * proportion),
                                                           44))
                        x_offset = (48 - (unit.img_width * proportion)) / 2
                        y_offset = 3
                else:
                    army_img = game_stats.gf_regiment_dict[unit.img_source + "/" + unit.img + side]
                    x_offset = unit.x_offset
                    y_offset = unit.y_offset

                screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])
                # screen.blit(army_img, [x_pos + unit.x_offset, y_pos + unit.y_offset])

                # Number of creatures
                number_of_creatures = str(len(unit.crew)) + "/" + str(unit.rows * unit.number)
                text_panel = arial_font14.render(number_of_creatures, True, DarkText)
                screen.blit(text_panel, [x_pos + 12, y_pos + 42])

                if int(number) in game_stats.first_army_exchange_list:
                    pygame.draw.polygon(screen, ApproveElementsColor,
                                        [[x_pos + unit.x_offset - 10, y_pos + unit.y_offset - 3],
                                         [x_pos + unit.x_offset + 21, y_pos + unit.y_offset - 3],
                                         [x_pos + unit.x_offset + 6, y_pos + unit.y_offset - 9]])

                number += 1

                # Update movement points information
                if movement_points_left < 0:
                    movement_points_left = int(unit.movement_points)
                elif unit.movement_points < movement_points_left:
                    movement_points_left = int(unit.movement_points)

                if least_max_movement_points < 0:
                    least_max_movement_points = int(unit.max_movement_points)
                elif unit.max_movement_points < least_max_movement_points:
                    least_max_movement_points = int(unit.max_movement_points)

        self.draw_movement_bar(screen, least_max_movement_points, movement_points_left, yVar)

    def draw_movement_bar(self, screen, least_max_movement_points, movement_points_left, yVar):
        # Not the best way to design additional points from skills
        if self.army.hero is not None:
            for skill in self.army.hero.skills:
                for effect in skill.effects:
                    if effect.application == "Movement points":
                        if effect.method == "addition":
                            least_max_movement_points += int(effect.quantity)

            if len(self.army.hero.inventory) > 0:
                # print("len(army.hero.inventory) > 0")
                for artifact in self.army.hero.inventory:
                    for effect in artifact.effects:
                        if effect.application == "Movement points":
                            # print("effect.application == Movement points")
                            if effect.method == "addition":
                                least_max_movement_points += int(effect.quantity)
                                # print(str(least_max_movement_points))

        # # Movement points bar
        xVar = int(movement_points_left / least_max_movement_points * 80)
        if movement_points_left > least_max_movement_points:
            xVar = 80
        pygame.draw.polygon(screen, ApproveFieldColor,
                            [[203, 684 + yVar], [203 + xVar, 684 + yVar], [203 + xVar, 706 + yVar], [203, 706 + yVar]])
        pygame.draw.polygon(screen, ApproveElementsColor,
                            [[203, 684 + yVar], [283, 684 + yVar], [283, 706 + yVar], [203, 706 + yVar]], 3)
