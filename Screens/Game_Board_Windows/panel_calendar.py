## Among Myth and Wonder
## panel_calendar

import pygame.draw

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources import graphics_classes
from Resources import game_stats


class Calendar_Panel(graphics_classes.Panel):
    def draw_panel(self, screen):
        # print(self.name + " draw_panel")
        self.draw_calendar_background(screen)
        self.draw_calendar(screen)
        self.draw_hourglass(screen)

    def draw_calendar_background(self, screen):
        background_img = game_stats.gf_misc_img_dict["Icons/grey_background_90_48"]
        screen.blit(background_img, (910, 7))

    def draw_calendar(self, screen):
        # Calendar
        text_NewGame2 = tnr_font20.render("Year", True, TitleText)
        screen.blit(text_NewGame2, [913, 8])
        text_NewGame2 = tnr_font20.render(str(game_stats.game_year), True, TitleText)
        screen.blit(text_NewGame2, [980, 8])
        text_NewGame2 = tnr_font20.render("Month", True, TitleText)
        screen.blit(text_NewGame2, [913, 32])
        text_NewGame2 = tnr_font20.render(str(game_stats.game_month), True, TitleText)
        screen.blit(text_NewGame2, [980, 32])

    def draw_hourglass(self, screen):
        if not game_stats.turn_hourglass:
            hourglass_img = game_stats.gf_misc_img_dict["Icons/hourglass_false"]
        else:
            hourglass_img = game_stats.gf_misc_img_dict["Icons/hourglass_true"]
        screen.blit(hourglass_img, (1005, 5))

