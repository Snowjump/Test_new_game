## Among Myth and Wonder
## panel_vision_mode

import pygame.draw

from Screens.colors_catalog import *

from Resources import graphics_classes
from Resources import game_stats


class Vision_Mode_Panel(graphics_classes.Panel):
    def draw_panel(self, screen):
        # print(self.name + " draw_panel")
        yVar = game_stats.game_window_height - 800
        self.draw_border_vision(screen, yVar)
        self.draw_grid_vision(screen, yVar)

    def draw_border_vision(self, screen, yVar):
        x = 1259
        y = 779 + yVar
        x_p = 19
        y_p = 19
        background_img = game_stats.gf_misc_img_dict["Icons/border_vision_mode"]
        screen.blit(background_img, (x, y))

        if game_stats.border_vision:
            color = HighlightOption
            pygame.draw.polygon(screen, color, [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]], 1)

    def draw_grid_vision(self, screen, yVar):
        x = 1235
        y = 779 + yVar
        x_p = 19
        y_p = 19
        background_img = game_stats.gf_misc_img_dict["Icons/grid_vision_mode"]
        screen.blit(background_img, (x, y))

        if game_stats.grid_vision:
            color = HighlightOption
            pygame.draw.polygon(screen, color, [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]], 1)
