## Among Myth and Wonder
## panel_selected_targets_counter

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources.Game_Graphics import graphics_classes
from Resources import game_stats

from Resources.Abilities import game_ability

from Content.Abilities import ability_catalog


class Selected_Targets_Counter_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        # Create new button
        self.add_confirmation_button()

    def draw_panel(self, screen):
        b = game_stats.present_battle
        self.draw_counter_text(screen, b)
        self.draw_borders_around_selected_targets(screen, b)

    def draw_counter_text(self, screen, b):
        text_panel = arial_font18.render("Selected targets " + str(len(b.ability_targets)) + "/"
                                         + str(b.total_targets), True, TitleText)
        screen.blit(text_panel, [550, 50])

    def draw_borders_around_selected_targets(self, screen, b):
        for target in b.ability_targets:
            x = int(target[0])
            y = int(target[1])
            x -= int(b.battle_pov[0])
            y -= int(b.battle_pov[1])

            pygame.draw.polygon(screen, WhiteBorder,
                                [[(x - 1) * 96, (y - 1) * 96],
                                 [(x - 1) * 96 + 95, (y - 1) * 96],
                                 [(x - 1) * 96 + 95, (y - 1) * 96 + 95],
                                 [(x - 1) * 96, (y - 1) * 96 + 95]], 1)

    def add_confirmation_button(self):
        yVar = game_stats.game_window_height - 800
        new_button = graphics_classes.Battle_Text_Button("Confirm target selection button", confirm_target_selection,
                                                         "Confirm targets", "tnr_font20", "TitleText", "FieldColor",
                                                         "LineMainMenuColor1", 550, 700 + yVar, 150, 30, 10, 5, 3)
        self.buttons.append(new_button)


def confirm_target_selection():
    b = game_stats.present_battle
    print("confirm_target_selection()")
    if not b.ability_targets:
        print("Required to select at least one target")
    else:
        ability = ability_catalog.ability_cat[b.selected_ability]
        game_ability.execute_ability(b, ability)
