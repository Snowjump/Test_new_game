## Miracle battles!

import pygame.draw
import pygame.font

from Resources import game_stats

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

resources_icons = {"Florins" : "resource_florins",
                   "Food" : "resource_food",
                   "Wood" : "resource_wood",
                   "Metals" : "resource_metals",
                   "Stone" : "resource_stone",
                   "Armament" : "resource_armament",
                   "Tools" : "resource_tools",
                   "Ingredients" : "resource_ingredients"}


def draw_upgrade_info(screen):
    # Draw top right panel with information about building upgrade
    pygame.draw.polygon(screen, MainMenuColor,
                        [[642, 80], [1278, 80], [1278, 530], [642, 540]])

    # Background
    pygame.draw.polygon(screen, FillButton,
                        [[646, 85],
                         [946, 85],
                         [946, 350],
                         [646, 350]])

    pygame.draw.polygon(screen, FillButton,
                        [[950, 85],
                         [1250, 85],
                         [1250, 350],
                         [950, 350]])

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
    y_points = building_effects_list(screen, y_points)
    y_points = recruitment_list(screen, y_points)

    ## Right side
    # Turns to complete building
    # Duration icon
    time_img = game_stats.gf_misc_img_dict["Icons/duration_icon"]
    screen.blit(time_img, (956, 91))

    text = ""
    number = game_stats.rw_object.construction_time
    if number == 1:
        text = str(number) + " turn to complete building"
    else:
        text = str(number) + " turns to complete building"
    text_panel1 = tnr_font16.render(text, True, DarkText)
    screen.blit(text_panel1, [972, 88])

    # Building cost
    text_panel1 = arial_font16.render("Building cost:", True, DarkText)
    screen.blit(text_panel1, [956, 110])

    y_shift = 18
    y_points = 0
    for res in game_stats.rw_object.construction_cost:
        # Resource icon
        icon_img = game_stats.gf_misc_img_dict[resources_icons[res[0]]]
        screen.blit(icon_img, (956, 130 + y_shift * y_points))

        text_panel1 = arial_font12.render(str(res[1]) + " " + str(res[0]), True, DarkText)
        screen.blit(text_panel1, [975, 131 + y_shift * y_points])
        y_points += 1

    # Required buildings in settlement
    if len(game_stats.rw_object.required_buildings) > 0:
        new_position = 130 + y_shift * y_points
        text_panel1 = arial_font16.render("Required buildings in settlement:", True, DarkText)
        screen.blit(text_panel1, [956, new_position])

        y_shift = 20
        y_points = 0
        for tag in game_stats.rw_object.required_buildings:
            text_panel1 = arial_font16.render(tag, True, DarkText)
            screen.blit(text_panel1, [956, new_position + 20 + y_shift * y_points])
            y_points += 1


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

    return y_points


def recruitment_list(screen, y_points):
    y_shift = 20
    if len(game_stats.rw_object.recruitment) > 0:
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
