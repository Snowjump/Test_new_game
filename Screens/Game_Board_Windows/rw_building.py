## Among Myth and Wonder
## rw_building

import pygame.draw
import pygame.font

from Resources import game_stats

from Screens.Game_Board_Windows import rw_sub_building_info
from Screens.Game_Board_Windows import building_special_interface

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Screens.Interface_Elements import buttons


# resources_icons = {"Florins" : "resource_florins.png",
#                    "Food" : "resource_food.png",
#                    "Wood" : "resource_wood.png",
#                    "Metals" : "resource_metals.png",
#                    "Stone" : "resource_stone.png",
#                    "Armament" : "resource_armament.png",
#                    "Tools" : "resource_tools.png",
#                    "Ingredients" : "resource_ingredients"}


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
    buttons.element_close_button(screen, "CancelFieldColor", "CancelElementsColor", "CancelElementsColor",
                                 1254, 85, 19, 19, 2, 2)

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
    name = game_stats.rw_object.name
    if name in special_structures:
        building_special_interface.structure_cat[special_structures[name]](screen)


special_structures = {"KL artifact market" : "KL artifact market",
                      "KL School of magic" : "KL School of magic",
                      "Wheelwright guild" : "Wheelwright guild"}
