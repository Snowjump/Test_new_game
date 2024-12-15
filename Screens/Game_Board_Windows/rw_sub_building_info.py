## Among Myth and Wonder
## rw_sub_building_info

import pygame.font

from Resources import game_stats

from Screens.colors_catalog import *
from Screens.fonts_catalog import *


def building_effects_list(screen, y_points):
    y_shift = 20
    if len(game_stats.rw_object.provided_effects) > 0:
        for effect in game_stats.rw_object.provided_effects:
            text = effect.name + "   " + effect.scale_type
            text_panel1 = arial_font14.render(text, True, DarkText)
            screen.blit(text_panel1, [650, 135 + y_shift * y_points])

            y_points += 1

            if effect.ef_type == "Population":
                for pop_ef in effect.content:
                    if pop_ef.application == "Production":
                        for res in pop_ef.bonus:
                            text = pop_ef.pops + ": "
                            if pop_ef.operator == "Addition":
                                text += "+" + str(res[1]) + " " + str(res[0]) + " production"
                            text_panel1 = arial_font14.render(text, True, DarkText)
                            screen.blit(text_panel1, [650, 135 + y_shift * y_points])
                            y_points += 1

                    elif pop_ef.application == "Tax":
                        for res in pop_ef.bonus:
                            text = pop_ef.pops + ": "
                            if pop_ef.operator == "Addition":
                                text += "+" + str(res[1]) + " " + str(res[0]) + " tax"
                            text_panel1 = arial_font14.render(text, True, DarkText)
                            screen.blit(text_panel1, [650, 135 + y_shift * y_points])
                            y_points += 1

            elif effect.ef_type == "Control":
                for cont_ef in effect.content:
                    if cont_ef.application == "Control":
                        text = cont_ef.realm_type + " "
                        if cont_ef.operator == "Addition":
                            text += "+" + str(cont_ef.bonus)
                        text += " control"
                        text_panel1 = arial_font14.render(text, True, DarkText)
                        screen.blit(text_panel1, [650, 135 + y_shift * y_points])
                        y_points += 1

    return y_points


def recruitment_list(screen, y_points):
    y_shift = 20
    if game_stats.rw_object.recruitment:
        for unit in game_stats.rw_object.recruitment:
            # Capacity
            text = "Recruit up to "
            if unit.hiring_capacity == 1:
                text += " 1 " + unit.unit_name + " regiment"
            else:
                text += str(unit.hiring_capacity) + " " + unit.unit_name + " regiments"

            text_panel1 = arial_font14.render(text, True, DarkText)
            screen.blit(text_panel1, [650, 135 + y_shift * y_points])
            y_points += 1

            # Replenishment
            text = "Replenishment in "
            if unit.replenishment_rate == 1:
                text += "1 turn"
            else:
                text += str(unit.replenishment_rate) + " turns"

            text_panel1 = arial_font14.render(text, True, DarkText)
            screen.blit(text_panel1, [650, 135 + y_shift * y_points])
            y_points += 1

    return y_points
