## Among Myth and Wonder
## panel_battle_actions

import pygame.draw

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources.Game_Graphics import graphics_classes
from Resources import game_stats


class Battle_Actions_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        self.yVar = game_stats.game_window_height - 800

    def draw_panel(self, screen):
        b = game_stats.present_battle
        if b.realm_in_control == game_stats.player_power and b.ready_to_act:
            self.draw_wait_button(screen, b)
            self.draw_defence_button(screen, b)
            self.draw_attack_method_button(screen, b)

    def draw_wait_button(self, screen, b):
        # Lets a regiment or a hero spent 0,5 time
        pygame.draw.polygon(screen, FieldColor, [[235, 740 + self.yVar], [357, 740 + self.yVar],
                                                 [357, 765 + self.yVar], [235, 765 + self.yVar]])
        if b.realm_in_control == game_stats.player_power:
            color = HighlightOption
        else:
            color = LineMainMenuColor1
        pygame.draw.polygon(screen, color, [[235, 740 + self.yVar], [357, 740 + self.yVar],
                                            [357, 765 + self.yVar], [235, 765 + self.yVar]], 3)

        text_NewGame1 = tnr_font20.render("Wait (Q)", True, TitleText)
        screen.blit(text_NewGame1, [275, 741 + self.yVar])

        hourglass_img = game_stats.gf_misc_img_dict["Icons/battle_hourglass"]
        screen.blit(hourglass_img, (240, 742 + self.yVar))

    def draw_defence_button(self, screen, b):
        if b.queue[0].obj_type == "Regiment":
            pygame.draw.polygon(screen, FieldColor, [[235, 770 + self.yVar], [357, 770 + self.yVar],
                                                     [357, 795 + self.yVar], [235, 795 + self.yVar]])
            if b.realm_in_control == game_stats.player_power:
                color = HighlightOption
            else:
                color = LineMainMenuColor1
            pygame.draw.polygon(screen, color, [[235, 770 + self.yVar], [357, 770 + self.yVar],
                                                [357, 795 + self.yVar], [235, 795 + self.yVar]], 3)

            text_NewGame1 = tnr_font20.render("Defend (E)", True, TitleText)
            screen.blit(text_NewGame1, [265, 771 + self.yVar])

            shield_img = game_stats.gf_misc_img_dict["Icons/battle_shield"]
            screen.blit(shield_img, (240, 772 + self.yVar))

    def draw_attack_method_button(self, screen, b):
        # Changes between attack methods if possible
        if b.queue[0].obj_type == "Regiment" and b.ready_to_act:
            pygame.draw.polygon(screen, FieldColor, [[923, 740 + self.yVar], [1100, 740 + self.yVar],
                                                     [1100, 795 + self.yVar], [923, 795 + self.yVar]])
            pygame.draw.polygon(screen, LineMainMenuColor1, [[923, 740 + self.yVar], [1100, 740 + self.yVar],
                                                             [1100, 795 + self.yVar], [923, 795 + self.yVar]], 3)

            attack_method = b.attack_name
            text_NewGame1 = tnr_font20.render(attack_method, True, TitleText)
            screen.blit(text_NewGame1, [982, 755 + self.yVar])

            attack_img = game_stats.gf_misc_img_dict["Icons/" + attack_method]
            screen.blit(attack_img, (925, 742 + self.yVar))

            # Next attack type or ability button
            pygame.draw.polygon(screen, FieldColor, [[1103, 740 + self.yVar], [1195, 740 + self.yVar],
                                                     [1195, 795 + self.yVar], [1103, 795 + self.yVar]])
            pygame.draw.polygon(screen, LineMainMenuColor1, [[1103, 740 + self.yVar], [1195, 740 + self.yVar],
                                                             [1195, 795 + self.yVar], [1103, 795 + self.yVar]], 3)

            arrow_img = game_stats.gf_misc_img_dict["Icons/arrow_next_full"]
            screen.blit(arrow_img, (1105, 742 + self.yVar))

            text_NewGame1 = tnr_font20.render("(R)", True, TitleText)
            screen.blit(text_NewGame1, [1165, 755 + self.yVar])

        elif b.queue[0].obj_type == "Hero":
            pygame.draw.polygon(screen, FieldColor, [[923, 740 + self.yVar], [1100, 740 + self.yVar],
                                                     [1100, 795 + self.yVar], [923, 795 + self.yVar]])
            pygame.draw.polygon(screen, LineMainMenuColor1, [[923, 740 + self.yVar], [1100, 740 + self.yVar],
                                                             [1100, 795 + self.yVar], [923, 795 + self.yVar]], 3)

            text_NewGame1 = tnr_font20.render("Abilities", True, TitleText)
            screen.blit(text_NewGame1, [990, 755 + self.yVar])

            icon_img = game_stats.gf_misc_img_dict["Icons/abilities_icon"]
            screen.blit(icon_img, (927, 752 + self.yVar))
