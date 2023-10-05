## Miracle battles!
## update_gf_menus

import pygame.draw

from Resources import game_stats

WhiteColor = (255, 255, 255)


def update_menus_art():
    game_stats.gf_menus_art = {}

    ## Entrance menu
    # Picture - sinister_figure_in_the_woods
    menus_art_img = pygame.image.load('img/Arts/sinister_figure_in_the_woods.png')
    game_stats.gf_menus_art["Arts/sinister_figure_in_the_woods"] = menus_art_img

    ## Create level menu
    # Picture - storm_in_the_ocean
    menus_art_img = pygame.image.load('img/Arts/storm_in_the_ocean.png')
    game_stats.gf_menus_art["Arts/storm_in_the_ocean"] = menus_art_img

