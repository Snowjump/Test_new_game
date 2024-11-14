## Among Myth and Wonder
## rw_building

import pygame.draw
import pygame.font

from Resources import game_stats

from Screens.Game_Board_Windows import rw_sub_building_info
from Screens.Game_Board_Windows import building_special_interface

WhiteColor = [255, 255, 255]

MainMenuColor = [0x9F, 0x97, 0x97]
FillButton = [0xD8, 0xBD, 0xA2]

DarkText = [0x11, 0x11, 0x11]

CancelFieldColor = [0xFF, 0x00, 0x00]
CancelElementsColor = [0x99, 0x00, 0x00]

tnr_font16 = pygame.font.SysFont('timesnewroman', 16)

arial_font16 = pygame.font.SysFont('arial', 16)
arial_font14 = pygame.font.SysFont('arial', 14)
arial_font12 = pygame.font.SysFont('arial', 12)

resources_icons = {"Florins" : "resource_florins.png",
                   "Food" : "resource_food.png",
                   "Wood" : "resource_wood.png",
                   "Metals" : "resource_metals.png",
                   "Stone" : "resource_stone.png",
                   "Armament" : "resource_armament.png",
                   "Tools" : "resource_tools.png",
                   "Ingredients" : "resource_ingredients"}


def draw_building_info(screen):
    # Draw top right panel with information about building upgrade
    pygame.draw.polygon(screen, MainMenuColor,
                        [[642, 80], [1278, 80], [1278, 540], [642, 540]])

    # Background
    pygame.draw.polygon(screen, FillButton,
                        [[646, 85],
                         [1250, 85],
                         [1250, 420],
                         [646, 420]])

    # Close settlement window
    pygame.draw.polygon(screen, CancelFieldColor, [[1254, 85], [1273, 85], [1273, 104], [1254, 104]])
    pygame.draw.polygon(screen, CancelElementsColor, [[1254, 85], [1273, 85], [1273, 104], [1254, 104]], 2)
    pygame.draw.line(screen, CancelElementsColor, [1257, 88], [1270, 101], 2)
    pygame.draw.line(screen, CancelElementsColor, [1257, 101], [1270, 88], 2)

    ## Left side
    # Icon image
    structure_img = game_stats.gf_building_dict[game_stats.rw_object.name]
    screen.blit(structure_img, (650, 87))

    # Structure title
    text = ""
    for title_part in game_stats.rw_object.title_name:
        text += str(title_part) + " "
    text_panel1 = tnr_font16.render(text, True, DarkText)
    screen.blit(text_panel1, [705, 88])

    # Structure abilities
    y_points = 0
    y_points = rw_sub_building_info.building_effects_list(screen, y_points)
    y_points = rw_sub_building_info.recruitment_list(screen, y_points)

    # Special interface
    name = ""
    # for line in game_stats.rw_object.title_name:
    #     name += line
    # if name in special_structures:
    #     building_special_interface.structure_cat[special_structures[name]](screen)
    name = game_stats.rw_object.name
    if name in special_structures:
        building_special_interface.structure_cat[special_structures[name]](screen)


# def building_effects_list(screen, y_points):
#     # print("building_effects_list")
#     y_shift = 20
#     if len(game_stats.rw_object.provided_effects) > 0:
#         for effect in game_stats.rw_object.provided_effects:
#             text = effect.name + "   " + effect.scale_type
#             text_panel1 = arial_font14.render(text, True, DarkText)
#             screen.blit(text_panel1, [650, 135 + y_shift * y_points])
#
#             y_points += 1
#             print(effect.ef_type)
#
#             if effect.ef_type == "Population":
#                 for pop_ef in effect.content:
#                     if pop_ef.application == "Production":
#                         for res in pop_ef.bonus:
#                             text = pop_ef.pops + ": "
#                             if pop_ef.operator == "Addition":
#                                 text += "+" + str(res[1]) + " " + str(res[0]) + " production"
#                             text_panel1 = arial_font14.render(text, True, DarkText)
#                             screen.blit(text_panel1, [650, 135 + y_shift * y_points])
#                             y_points += 1
#
#                     elif pop_ef.application == "Tax":
#                         for res in pop_ef.bonus:
#                             text = pop_ef.pops + ": "
#                             if pop_ef.operator == "Addition":
#                                 text += "+" + str(res[1]) + " " + str(res[0]) + " tax"
#                             text_panel1 = arial_font14.render(text, True, DarkText)
#                             screen.blit(text_panel1, [650, 135 + y_shift * y_points])
#                             y_points += 1
#
#             elif effect.ef_type == "Control":
#                 for cont_ef in effect.content:
#                     if cont_ef.application == "Control":
#                         text = cont_ef.realm_type + " "
#                         if cont_ef.operator == "Addition":
#                             text += "+" + str(cont_ef.bonus)
#                         text += " control"
#                         text_panel1 = arial_font14.render(text, True, DarkText)
#                         screen.blit(text_panel1, [650, 135 + y_shift * y_points])
#                         y_points += 1
#
#     return y_points
#
#
# def recruitment_list(screen, y_points):
#     y_shift = 20
#     if len(game_stats.rw_object.recruitment) > 0:
#         for unit in game_stats.rw_object.recruitment:
#             # Capacity
#             text = str(unit.ready_units) + "/" + str(unit.hiring_capacity) + " " + unit.unit_name
#             if unit.ready_units == 1:
#                 text += " regiment ready for recruitment"
#             else:
#                 text += " regiments ready for recruitment"
#
#             text_panel1 = arial_font14.render(text, True, DarkText)
#             screen.blit(text_panel1, [650, 135 + y_shift * y_points])
#             y_points += 1
#
#             # Replenishment
#             # Duration icon
#             time_img = game_stats.gf_misc_img_dict["Icons/duration_icon"]
#             screen.blit(time_img, (650, 136 + y_shift * y_points))
#
#             text = ""
#             if unit.replenishment_rate - unit.time_passed == 1:
#                 text += "1 turn until replenishment"
#             else:
#                 text += str(unit.replenishment_rate - unit.time_passed) + " turns until replenishment"
#
#             text_panel1 = arial_font14.render(text, True, DarkText)
#             screen.blit(text_panel1, [665, 135 + y_shift * y_points])
#             y_points += 1
#
#     return y_points


special_structures = {"KL artifact market" : "KL artifact market",
                      "KL School of magic" : "KL School of magic"}
