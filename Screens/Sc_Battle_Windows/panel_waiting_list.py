## Among Myth and Wonder
## panel_waiting_list

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Screens.Interface_Elements import buttons

from Resources.Game_Graphics import graphics_classes
from Resources import game_stats
from Resources import common_selects


class Waiting_List_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        self.yVar = game_stats.game_window_height - 800

    def draw_panel(self, screen):
        b = game_stats.present_battle
        self.draw_selected_regiment_for_relocation(screen, b)
        if b.waiting_list:
            self.draw_ribbon_background(screen)
            self.draw_list(screen, b)

    def draw_ribbon_background(self, screen):
        background_img = game_stats.gf_misc_img_dict["Icons/paper_3_square_560_x_60"]
        screen.blit(background_img, (361, 741 + self.yVar))

        buttons.element_arrow_button(screen, "Left", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                     360, 740 + self.yVar, 20, 60, 3, 2, 1, 19)
        buttons.element_arrow_button(screen, "Right", "RockTunel", "LineMainMenuColor1", "LineMainMenuColor1",
                                     900, 740 + self.yVar, 20, 60, 3, 2, 1, 19)

    def draw_list(self, screen, b):
        # Units
        player_id = int(b.defender_id)
        if b.attacker_realm == game_stats.player_power:
            player_id = int(b.attacker_id)

        a = common_selects.select_army_by_id(player_id)

        number = 0
        for unit in b.waiting_list:
            side = "_l"
            if a.right_side:
                side = "_r"
            if b.waiting_index <= number <= 9 + b.waiting_index:
                x_pos = 380 + (number - b.waiting_index) * 52
                y_pos = 744 + self.yVar

                if a.units[unit].crew[0].img_width > 44 or a.units[unit].crew[0].img_height > 44:
                    army_img = game_stats.gf_regiment_dict[a.units[unit].img_source + "/" + a.units[unit].img + side]
                    if a.units[unit].crew[0].img_width > 44:
                        proportion = 44 / a.units[unit].crew[0].img_width
                        army_img = pygame.transform.scale(army_img,
                                                          (44,
                                                           int(a.units[unit].crew[0].img_height * proportion)))
                        x_offset = 3
                        y_offset = (48 - (a.units[unit].crew[0].img_height * proportion)) / 2
                    else:
                        proportion = 44 / a.units[unit].crew[0].img_height
                        army_img = pygame.transform.scale(army_img,
                                                          (int(a.units[unit].crew[0].img_width * proportion),
                                                           44))
                        x_offset = (48 - (a.units[unit].crew[0].img_width * proportion)) / 2
                        y_offset = 3
                else:
                    army_img = game_stats.gf_regiment_dict[a.units[unit].img_source + "/" + a.units[unit].img + side]
                    x_offset = a.units[unit].x_offset
                    y_offset = a.units[unit].y_offset

                screen.blit(army_img, [x_pos + x_offset, y_pos + y_offset])

                # Highlight selected unit card
                if b.unit_card != -1:
                    if 0 <= b.unit_card - b.waiting_index <= 9:
                        unit_pos = 380 + int(b.unit_card - b.waiting_index) * 52
                        pygame.draw.polygon(screen, WhiteBorder,
                                            [[unit_pos + 1, 741 + self.yVar],
                                             [unit_pos + 52, 741 + self.yVar],
                                             [unit_pos + 52, 799 + self.yVar],
                                             [unit_pos + 1, 799 + self.yVar]], 1)

                # Number of creatures in regiment
                text_panel = arial_font8.render(str(len(a.units[unit].crew)) + "/"
                                                + str(a.units[unit].number * a.units[unit].rows), True, DarkText)
                screen.blit(text_panel, [384 + (number - b.waiting_index) * 52, 744 + self.yVar])

            number += 1

    def draw_selected_regiment_for_relocation(self, screen, b):
        if b.selected_unit != -1:
            tile = b.battle_map[b.selected_unit]
            x = int(tile.posxy[0])
            y = int(tile.posxy[1])
            x -= int(b.battle_pov[0])
            y -= int(b.battle_pov[1])

            pygame.draw.polygon(screen, WhiteBorder,
                                [[(x - 1) * 96, (y - 1) * 96],
                                 [(x - 1) * 96 + 95, (y - 1) * 96],
                                 [(x - 1) * 96 + 95, (y - 1) * 96 + 95],
                                 [(x - 1) * 96, (y - 1) * 96 + 95]], 1)
