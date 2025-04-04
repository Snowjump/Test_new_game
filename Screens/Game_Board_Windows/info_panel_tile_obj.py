## Among Myth and Wonder
## info_panel_tile_obj

import pygame.draw

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources.Game_Graphics import graphics_classes
from Resources import game_stats
from Resources import game_obj
from Resources import common_selects


class Tile_Obj_Panel(graphics_classes.Panel):
    def __init__(self, name):
        super().__init__(name)
        self.yVar2 = 0

    def draw_panel(self, screen):
        yVar = game_stats.game_window_height - 800
        self.yVar2 = 0
        x = int(game_stats.info_tile[0])
        y = int(game_stats.info_tile[1])
        tile_num = (y - 1) * game_stats.cur_level_width + x - 1
        tile_obj = game_obj.game_map[tile_num]
        x = x - int(game_stats.pov_pos[0])
        y = y - int(game_stats.pov_pos[1])

        self.draw_border_line(screen, x, y)
        self.draw_panel_background(screen, yVar)
        self.draw_terrain_information(screen, yVar, tile_obj)
        self.draw_lot_object_information(screen, yVar, tile_obj)

    def draw_border_line(self, screen, x, y):
        # Border line around selected tile
        pygame.draw.polygon(screen, WhiteBorder,
                            [[(x - 1) * 48, (y - 1) * 48], [(x - 1) * 48 + 47, (y - 1) * 48],
                             [(x - 1) * 48 + 47, (y - 1) * 48 + 47], [(x - 1) * 48, (y - 1) * 48 + 47]], 1)

    def draw_panel_background(self, screen, yVar):
        # Lower panel
        pygame.draw.polygon(screen, MainMenuColor,
                            [[200, 650 + yVar], [1080, 650 + yVar], [1080, 800 + yVar], [200, 800 + yVar]])

    def draw_terrain_information(self, screen, yVar, tile_obj):
        self.draw_ownership_info(screen, yVar)
        self.draw_terrain_type_info(screen, yVar, tile_obj)
        self.draw_road_info(screen, yVar, tile_obj)

    def draw_ownership_info(self, screen, yVar):
        # Ownership
        if game_stats.tile_ownership == "Wild lands":
            text_panel = tnr_font18.render("Wild lands", True, TitleText)
            screen.blit(text_panel, [205, 654 + yVar])
        elif game_stats.tile_ownership == "Neutral lands":
            text_panel = tnr_font18.render("Neutral lands", True, TitleText)
            screen.blit(text_panel, [205, 654 + yVar])
        else:
            # Country's name
            text_panel = tnr_font18.render(game_stats.tile_ownership, True, TitleText)
            screen.blit(text_panel, [240, 654 + yVar])

            # Flag
            pygame.draw.polygon(screen, FlagColors[game_stats.tile_flag_colors[0]],
                                [[205, 654 + yVar], [235, 654 + yVar], [235, 665 + yVar],
                                 [205, 665 + yVar]])
            pygame.draw.polygon(screen, FlagColors[game_stats.tile_flag_colors[1]],
                                [[205, 666 + yVar], [235, 666 + yVar], [235, 676 + yVar],
                                 [205, 676 + yVar]])

    def draw_terrain_type_info(self, screen, yVar, tile_obj):
        # Terrain type
        text_panel = tnr_font20.render(tile_obj.terrain, True, TitleText)
        screen.blit(text_panel, [205, 684 + yVar])

    def draw_road_info(self, screen, yVar, tile_obj):
        # Road information
        if tile_obj.road:
            self.yVar2 += 30
            text_panel = tnr_font20.render(tile_obj.road.material, True, TitleText)
            screen.blit(text_panel, [205, 684 + yVar + self.yVar2])
            # print("draw_road_info y - " + str(684 + yVar + self.yVar2))

    def draw_lot_object_information(self, screen, yVar, tile_obj):
        ### Lot object information
        if tile_obj.lot:
            if tile_obj.lot == "City":
                self.draw_settlement_information(screen, yVar)
            else:
                self.draw_lot_information(screen, yVar, tile_obj)

    def draw_settlement_information(self, screen, yVar):
        # Object is a settlement
        self.yVar2 += 30
        text_panel = tnr_font20.render("Settlement", True, TitleText)
        screen.blit(text_panel, [205, 684 + yVar + self.yVar2])
        # print("draw_settlement_information y - " + str(684 + yVar + self.yVar2))

        settlement = common_selects.select_settlement_by_id(game_stats.right_click_city)

        self.draw_population(screen, yVar, settlement.residency)
        self.draw_population_resources(screen, yVar, settlement.residency)

    def draw_lot_information(self, screen, yVar, tile_obj):
        # Object type
        self.yVar2 += 30
        text_panel = tnr_font20.render(tile_obj.lot.obj_typ, True, TitleText)
        screen.blit(text_panel, [205, 684 + yVar + self.yVar2])

        if tile_obj.lot.obj_typ == "Facility":
            self.draw_facility_information(screen, yVar, tile_obj)

    def draw_facility_information(self, screen, yVar, tile_obj):
        self.draw_facility_name(screen, yVar, tile_obj)
        self.draw_population(screen, yVar, tile_obj.lot.residency)
        self.draw_population_resources(screen, yVar, tile_obj.lot.residency)

    def draw_facility_name(self, screen, yVar, tile_obj):
        self.yVar2 += 30
        text_panel = tnr_font20.render(tile_obj.lot.obj_name, True, TitleText)
        screen.blit(text_panel, [205, 684 + yVar + self.yVar2])

    def draw_population(self, screen, yVar, residency):
        ### Population information
        text_panel = tnr_font20.render("Population", True, TitleText)
        screen.blit(text_panel, [391, 654 + yVar])

        yPos = 0
        for pops in residency:
            # Population's name
            # print(pops)
            text_panel = tnr_font20.render(pops.name, True, DarkText)
            screen.blit(text_panel, [391, 680 + yVar + yPos])

            yPos += 30

        # White line
        pygame.draw.lines(screen, WhiteBorder, False, [(391, 702 + yVar + 30 * game_stats.i_p_index),
                                                       (480, 702 + yVar + 30 * game_stats.i_p_index)], 1)

    def draw_population_resources(self, screen, yVar, residency):
        ### Resources
        # Only shows player's resources
        if game_stats.tile_ownership == game_stats.player_power:
            # Property
            text_panel = tnr_font20.render("Property:", True, TitleText)
            screen.blit(text_panel, [510, 654 + yVar])

            # Resources in reserve
            # print(TileObj.lot.residency[game_stats.i_p_index])
            if len(residency[game_stats.i_p_index].reserve) > 0:
                yPos = 0
                for resource in residency[game_stats.i_p_index].reserve:
                    text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True, DarkText)
                    screen.blit(text_panel, [510, 677 + yVar + yPos])

                    yPos += 15

            # Produced resources
            text_panel = tnr_font20.render("Produced:", True, TitleText)
            screen.blit(text_panel, [625, 654 + yVar])

            # Records from last turn
            if len(residency[game_stats.i_p_index].records_gained) > 0:
                yPos = 0
                for resource in residency[game_stats.i_p_index].records_gained:
                    text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True, DarkText)
                    screen.blit(text_panel, [625, 677 + yVar + yPos])

                    yPos += 15

            # Sold resources
            text_panel = tnr_font20.render("Sold:", True, TitleText)
            screen.blit(text_panel, [740, 654 + yVar])

            # Records from last turn
            if len(residency[game_stats.i_p_index].records_sold) > 0:
                yPos = 0
                for resource in residency[game_stats.i_p_index].records_sold:
                    text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True,
                                                     DarkText)
                    screen.blit(text_panel, [740, 677 + yVar + yPos])

                    yPos += 15

            # Bought resources
            text_panel = tnr_font20.render("Bought:", True, TitleText)
            screen.blit(text_panel, [855, 654 + yVar])

            # Records from last turn
            if len(residency[game_stats.i_p_index].records_bought) > 0:
                yPos = 0
                for resource in residency[game_stats.i_p_index].records_bought:
                    text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True,
                                                     DarkText)
                    screen.blit(text_panel, [855, 677 + yVar + yPos])

                    yPos += 15

            # Consumed resources
            text_panel = tnr_font20.render("Consumed:", True, TitleText)
            screen.blit(text_panel, [970, 654 + yVar])

            # Records from last turn
            if len(residency[game_stats.i_p_index].records_consumed) > 0:
                yPos = 0
                for resource in residency[game_stats.i_p_index].records_consumed:
                    text_panel = arial_font14.render(resource[0] + "  " + str(resource[1]), True,
                                                     DarkText)
                    screen.blit(text_panel, [970, 677 + yVar + yPos])

                    yPos += 15
