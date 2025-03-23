## Among Myth and Wonder
## panel_battle_queue

import pygame.draw
import pygame.font

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Screens.Interface_Elements import buttons
from Screens.Interface_Elements import flags

from Resources import graphics_classes
from Resources import game_stats
from Resources import common_selects


class Battle_Queue_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        self.yVar = game_stats.game_window_height - 800

    def draw_panel(self, screen):
        self.draw_ribbon_background(screen)
        self.draw_queue(screen)

    def draw_ribbon_background(self, screen):
        background_img = game_stats.gf_misc_img_dict["Icons/paper_3_square_560_x_60"]
        screen.blit(background_img, (361, 741 + self.yVar))

        buttons.element_arrow_button(screen, "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                     360, 740 + self.yVar, 20, 60, 3, 2, 1, 19)
        buttons.element_arrow_button(screen, "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                     900, 740 + self.yVar, 20, 60, 3, 2, 1, 19)

    def draw_queue(self, screen):
        b = game_stats.present_battle
        number = 0
        for card in b.queue:
            if card.obj_type == "Regiment":
                if b.queue_index <= number <= 9 + b.queue_index:
                    x_pos = 380 + (number - b.queue_index) * 52
                    y_pos = 744 + self.yVar

                    a = common_selects.select_army_by_id(card.army_id)

                    side = "_l"
                    if a.army_id == b.attacker_id:
                        side = "_r"

                    if card.img_width > 44 or card.img_height > 44:
                        card_img = game_stats.gf_regiment_dict[card.img_source + "/" + card.img + side]
                        if card.img_width > 44:
                            proportion = 44 / card.img_width
                            card_img = pygame.transform.scale(card_img,
                                                              (44,
                                                               int(card.img_height * proportion)))
                            x_offset = 3
                            y_offset = (48 - (card.img_height * proportion)) / 2
                        else:
                            proportion = 44 / card.img_height
                            card_img = pygame.transform.scale(card_img,
                                                              (int(card.img_width * proportion),
                                                               44))
                            x_offset = (48 - (card.img_width * proportion)) / 2
                            y_offset = 3
                    else:
                        card_img = game_stats.gf_regiment_dict[card.img_source + "/" + card.img + side]
                        x_offset = card.x_offset
                        y_offset = card.y_offset

                    screen.blit(card_img, [x_pos + x_offset, y_pos + y_offset])

                    # # Highlight selected unit card
                    # if b.unit_card != -1:
                    #     if 0 <= b.unit_card - b.waiting_index <= 9:
                    #         unit_pos = 380 + int(b.unit_card - b.waiting_index) * 52
                    #         pygame.draw.polygon(screen, WhiteBorder,
                    #                             [[unit_pos + 1, 740 + yVar],
                    #                              [unit_pos + 52, 740 + yVar],
                    #                              [unit_pos + 52, 800 + yVar],
                    #                              [unit_pos + 1, 800 + yVar]], 1)

                    # Number of creatures in regiment
                    text_panel = arial_font10.render(str(len(a.units[card.number].crew)) + "/"
                                                     + str(a.units[card.number].number * a.units[card.number].rows),
                                                     True, DarkText)
                    screen.blit(text_panel, [384 + (number - b.queue_index) * 52, 742 + self.yVar])

                    # Regiment's morale
                    text_panel = arial_font10.render(str(a.units[card.number].morale), True, DarkText)
                    screen.blit(text_panel, [x_pos + 4, y_pos + 8])

                    if card.f_color:  # Draw flag
                        flags.card_flag(screen, x_pos, y_pos, FlagpoleColor,
                                        FlagColors[card.f_color], FlagColors[card.s_color])

                    # Act time
                    text_panel = arial_font10.render(str(b.queue[number - b.queue_index].time_act), True, DarkText)
                    screen.blit(text_panel, [400 + (number - b.queue_index) * 52, 788 + self.yVar])

                number += 1

            if card.obj_type == "Effect":
                if b.queue_index <= number <= 9 + b.queue_index:
                    x_pos = 380 + (number - b.queue_index) * 52
                    y_pos = 744 + self.yVar

                    card_img = game_stats.gf_misc_img_dict[card.img_source + "/" + card.img]
                    screen.blit(card_img, [x_pos + card.x_offset, y_pos + card.y_offset])

                    # Act time
                    text_panel = arial_font10.render(str(b.queue[number - b.queue_index].time_act), True, DarkText)
                    screen.blit(text_panel, [396 + (number - b.queue_index) * 52, 788 + self.yVar])

                number += 1

            if card.obj_type == "Hero":
                if b.queue_index <= number <= 9 + b.queue_index:
                    x_pos = 380 + (number - b.queue_index) * 52
                    y_pos = 744 + self.yVar

                    a = common_selects.select_army_by_id(card.army_id)

                    side = "_l"
                    if a.army_id == b.attacker_id:
                        side = "_r"

                    card_img = game_stats.gf_hero_dict[card.img_source + "/" + card.img + side]
                    screen.blit(card_img, [x_pos + card.x_offset, y_pos + card.y_offset])

                    # Act time
                    text_panel = arial_font10.render(str(b.queue[number - b.queue_index].time_act), True, DarkText)
                    screen.blit(text_panel, [396 + (number - b.queue_index) * 52, 788 + self.yVar])

                    if card.f_color:  # Draw flag
                        flags.card_flag(screen, x_pos, y_pos, FlagpoleColor,
                                        FlagColors[card.f_color], FlagColors[card.s_color])

                number += 1
