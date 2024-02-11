## Among Myth and Wonder
## panel_left_ribbon_menu

import pygame.draw

from Resources import graphics_classes
from Resources import game_stats


class Left_Ribbon_Menu(graphics_classes.Panel):
    def draw_panel(self, screen):
        self.draw_ribbon_background(screen)
        self.draw_buttons(screen)

    def draw_ribbon_background(self, screen):
        background_img = game_stats.gf_misc_img_dict["Icons/grey_background_32_120"]
        screen.blit(background_img, (0, 0))

    def draw_buttons(self, screen):
        # Button - realm
        icon_img = game_stats.gf_misc_img_dict["Icons/crown"]
        screen.blit(icon_img, (4, 4))

        # Button - tasks
        if game_stats.new_tasks:
            icon_img = game_stats.gf_misc_img_dict["Icons/new_task_scroll"]
            screen.blit(icon_img, (4, 29))
        else:
            icon_img = game_stats.gf_misc_img_dict["Icons/old_task_scroll"]
            screen.blit(icon_img, (4, 29))

        # Button - Diplomacy
        icon_img = game_stats.gf_misc_img_dict["Icons/diplomacy"]
        screen.blit(icon_img, (4, 54))
