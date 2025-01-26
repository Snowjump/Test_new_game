## Among Myth and Wonder
## algo_borders

import pygame

from Screens.colors_catalog import *

from Resources import algo_square_range
from Resources import common_selects
from Resources import game_stats
from Resources import game_obj


class Realm_Borders:
    def __init__(self, f_color, s_color, nw=None, n=None, ne=None, e=None, se=None, s=None, sw=None, w=None):
        self.f_color = f_color  # str - first color
        self.s_color = s_color  # str - second color
        self.ne = ne  # north-east
        self.n = n  # north
        self.nw = nw  # north-west
        self.e = e  # east
        self.se = se  # south-east
        self.s = s  # south
        self.sw = sw  # south-west
        self.w = w  # west


def refresh_borders(tiles_list, erase_borders=False):
    print("")
    print("refresh_borders()")
    # tiles_list consist of integers with numbers of tiles
    realms_list = {}
    for location in tiles_list:
        print(game_stats.current_screen + "; location - " + str(location))
        tile = None
        city_location = "game_cities"
        power_location = "game_powers"
        # rm = []
        # print("rm id - " + str(id(rm)))
        if game_stats.current_screen in ["Level Editor", "Load Level Into Editor"]:
            # print(str(game_stats.LE_borders_map[location]) + " " + str(id(game_stats.LE_borders_map[location])))
            tile = game_stats.level_map[location]
            # rm.append(game_stats.LE_borders_map[location])
            # print(str(game_stats.LE_borders_map[location]) + " " + str(rm))
            # print(str(id(game_stats.LE_borders_map[location])) + " " + str(id(rm)))
            city_location = "editor_cities"
            power_location = "editor_powers"
        elif game_stats.current_screen in ["New Game", "Game Board", "Skirmish", "Battle"]:
            tile = game_obj.game_map[location]

        # print("Tile position - " + str(tile.posxy) + "; type - " + str(type(rm)))

        if tile.city_id:
            print("tile.posxy - " + str(tile.posxy) + " tile.city_id - " + str(tile.city_id))
            settlement = common_selects.select_settlement_by_id(tile.city_id, location=city_location)
            if tile.city_id not in realms_list:
                realm = common_selects.select_realm_by_name(settlement.owner, location=power_location)
                print("Realm: " + str(realm))
                if realm is None:
                    # Neutral settlement
                    realms_list[tile.city_id] = ["Neutral", "NeutralDarkGrey", "NeutralDarkRed"]
                else:
                    # Regular settlement that belong to a realm
                    realms_list[tile.city_id] = [realm.name, realm.f_color, realm.s_color]

            parameters = realms_list[tile.city_id]
            # f_color = str(parameters[1])
            # s_color = str(parameters[2])
            # print(FlagColors[parameters[1]])
            color_name1 = FlagColors[parameters[1]] + [120]
            color_name2 = FlagColors[parameters[2]] + [120]
            # print(parameters[1] + " " + str(color_name1) + "; " + parameters[2] + " " + str(color_name2))
            f_color = pygame.Color(color_name1[0], color_name1[1], color_name1[2], color_name1[3])
            s_color = pygame.Color(color_name2[0], color_name2[1], color_name2[2], color_name2[3])
            nw = True
            n = True
            ne = True
            e = True
            se = True
            s = True
            sw = True
            w = True
            # print(f_color)

            bordering_tiles = algo_square_range.within_square_range(tile.posxy, 1, True)
            for btl in bordering_tiles:
                # btl - bordering tile location - int
                bt = None  # bordering tile - Tile object
                if game_stats.current_screen in ["Level Editor", "Load Level Into Editor"]:
                    bt = game_stats.level_map[btl]
                elif game_stats.current_screen in ["New Game", "Game Board", "Skirmish", "Battle"]:
                    bt = game_obj.game_map[btl]

                print("bt.posxy - " + str(bt.posxy) + " bt.city_id - " + str(bt.city_id))

                if bt.city_id:
                    bt_settlement = common_selects.select_settlement_by_id(bt.city_id, location=city_location)
                    # if bt_settlement.owner == settlement.owner:
                    if bt_settlement.city_id == settlement.city_id:
                        print("btl - " + str(btl) + " city_id - " + str(bt_settlement.city_id) +
                              "; location - " + str(location) + " city_id - " + str(settlement.city_id))
                        if bt.posxy[0] < tile.posxy[0]:
                            if bt.posxy[1] < tile.posxy[1]:
                                nw = False
                            elif bt.posxy[1] == tile.posxy[1]:
                                w = False
                            elif bt.posxy[1] > tile.posxy[1]:
                                sw = False
                        elif bt.posxy[0] == tile.posxy[0]:
                            if bt.posxy[1] < tile.posxy[1]:
                                n = False
                            elif bt.posxy[1] > tile.posxy[1]:
                                s = False
                        elif bt.posxy[0] > tile.posxy[0]:
                            if bt.posxy[1] < tile.posxy[1]:
                                ne = False
                            elif bt.posxy[1] == tile.posxy[1]:
                                e = False
                            elif bt.posxy[1] > tile.posxy[1]:
                                se = False

            if n:
                nw = True
                ne = True
            if e:
                ne = True
                se = True
            if s:
                se = True
                sw = True
            if w:
                sw = True
                nw = True

            # rm = 1
            if game_stats.current_screen in ["Level Editor", "Load Level Into Editor"]:
                # rm = game_stats.LE_borders_map[location]
                # rm = Realm_Borders(f_color, s_color, nw, n, ne, e, se, s, sw, w)
                game_stats.LE_borders_map[location] = Realm_Borders(f_color, s_color, nw, n, ne, e, se, s, sw, w)
                # print(str(game_stats.LE_borders_map[location]))
            else:
                game_obj.borders_map[location] = Realm_Borders(f_color, s_color, nw, n, ne, e, se, s, sw, w)
            # game_stats.LE_borders_map[location] = Realm_Borders(f_color, s_color, nw, n, ne, e, se, s, sw, w)
            # print("rm type - " + str(type(rm)))
            # print("rm.n - " + str(rm.n))
        else:
            if erase_borders:
                if game_stats.current_screen in ["Level Editor", "Load Level Into Editor"]:
                    game_stats.LE_borders_map[location] = None
        # print("Tile position - " + str(tile.posxy) + "; type - " + str(type(rm)) + "; id - " + str(id(rm)))
        # print(str(game_stats.LE_borders_map[location]) + " " + str(id(game_stats.LE_borders_map[location])))

    # for i in tiles_list:
    #     rb = game_stats.LE_borders_map[i]
    #     print("rb type - " + str(type(rb)))


def collect_surrounding_tiles(control_zone_list):
    print("control_zone_list: " + str(control_zone_list))
    tiles_list = list(control_zone_list)
    for tile in control_zone_list:
        posxy = []
        if game_stats.current_screen in ["Level Editor", "Load Level Into Editor"]:
            posxy = game_stats.level_map[tile].posxy
        else:
            posxy = game_obj.game_map[tile].posxy
        surrounding_tiles = algo_square_range.within_square_range(posxy, 1, True)
        for surrounding_tile in surrounding_tiles:
            tiles_list.append(int(surrounding_tile))
    print("tiles_list: " + str(tiles_list))
    return tiles_list
