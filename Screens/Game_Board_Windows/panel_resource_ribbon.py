## Among Myth and Wonder
## panel_resource_ribbon

import pygame.draw

from Screens.colors_catalog import *
from Screens.fonts_catalog import *
from Screens.resource_icons_catalog import *

from Resources import graphics_classes
from Resources import graphics_obj
from Resources import game_stats


class Resource_Ribbon(graphics_classes.Panel):
    def draw_panel(self, screen):
        # print(self.name + " draw_panel")
        self.draw_ribbon_background(screen)
        self.draw_resources(screen)

    def draw_ribbon_background(self, screen):
        # print(self.name + " draw_ribbon_background")
        # pygame.draw.polygon(screen, MainMenuColorDark1, [[41, 0], [600, 0], [600, 30], [41, 30]])
        background_img = game_stats.gf_misc_img_dict["Icons/grey_background_559_30"]
        screen.blit(background_img, (41, 0))

    def draw_resources(self, screen):
        x_shift = 80
        x_points = 0
        for resource in graphics_obj.resource_ribbon:
            # Resource icon
            # print(str(resource[0]))
            icon_img = game_stats.gf_misc_img_dict[resources_icons[resource.name]]
            screen.blit(icon_img, (46 + x_shift * x_points, 8))

            # Resource quantity
            text_line = tnr_font14.render(str(resource.quantity), True, DarkText)
            screen.blit(text_line, (68 + x_shift * x_points, 1))

            # Estimated change of quantity in next turn
            text = str(resource.delta)
            text_color = DarkText
            if resource.delta > 0:
                text_color = ApproveElementsColor
                text = "+" + text
            elif resource.delta < 0:
                text_color = CancelElementsColor
                text = "-" + text
            text_line = tnr_font14.render(text, True, text_color)
            screen.blit(text_line, (69 + x_shift * x_points, 16))

            x_points += 1

