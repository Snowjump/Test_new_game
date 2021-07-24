## Miracle battles

import random, pygame, math

from Resources import game_stats
from Resources import game_classes
from Content import terrain_catalog


def new_game():
    game_stats.map_operations = True
    game_stats.active_name_field = False
    game_stats.pov_pos = [0, 0]
    game_stats.edit_instrument = "select"
    game_stats.selected_tile = []
    game_stats.faction_num = 0
    game_stats.cities_id_counter = 0
    game_stats.lv_year = 0
    game_stats.lv_month = 5

    # Create level map
    tile_cells = game_stats.new_level_width * game_stats.new_level_height
    print("Number of tile cells - " + str(tile_cells) + " with width "
          + str(game_stats.new_level_width) + " and height " + str(game_stats.new_level_height))
    tile_number = 1

    while tile_number <= tile_cells:
        x = int(tile_number % game_stats.new_level_width)
        if x == 0:
            x = int(game_stats.new_level_width)
        y = int(math.ceil(tile_number / game_stats.new_level_width))
        game_stats.level_map.append(game_classes.Tile((x, y), "Plain",
                                                      terrain_catalog.terrain_calendar["Plain"][game_stats.LE_month]))
        print("x, y - " + str(x) + " " + str(y))
        tile_number += 1
