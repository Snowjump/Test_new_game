## Miracle battles

import pygame.draw
from Resources import game_stats

arrow_green = (0, 102, 0, 180)
arrow_burgundy = (102, 0, 0, 180)


arrow_color = {"Arrow_green" : arrow_green,
               "Arrow_burgundy" : arrow_burgundy}


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def arrow_icon(screen, route, arrows):
    order = 0
    # print("It works")

    for arrow in route:
        x = int(arrow[0])
        y = int(arrow[1])
        x -= int(game_stats.pov_pos[0])
        y -= int(game_stats.pov_pos[1])
        # print("Arrow " + str(arrows[order][0]) + " - [" + str(x) + ", " + str(y) + "] ")

        if arrows[order][0] == "NW":
            draw_polygon_alpha(screen, arrow_color[arrows[order][1]],
                               ([(x - 1) * 48 + 38, (y - 1) * 48 + 32], [(x - 1) * 48 + 30, (y - 1) * 48 + 23],
                                [(x - 1) * 48 + 33, (y - 1) * 48 + 18],
                                [(x - 1) * 48 + 14, (y - 1) * 48 + 14],
                                [(x - 1) * 48 + 18, (y - 1) * 48 + 33],
                                [(x - 1) * 48 + 23, (y - 1) * 48 + 30], [(x - 1) * 48 + 32, (y - 1) * 48 + 38]))

        elif arrows[order][0] == "N":
            draw_polygon_alpha(screen, arrow_color[arrows[order][1]],
                               ([(x - 1) * 48 + 20, (y - 1) * 48 + 36], [(x - 1) * 48 + 20, (y - 1) * 48 + 27],
                                [(x - 1) * 48 + 14, (y - 1) * 48 + 27],
                                [(x - 1) * 48 + 24, (y - 1) * 48 + 12], [(x - 1) * 48 + 25, (y - 1) * 48 + 12],
                                [(x - 1) * 48 + 35, (y - 1) * 48 + 27],
                                [(x - 1) * 48 + 29, (y - 1) * 48 + 27], [(x - 1) * 48 + 29, (y - 1) * 48 + 36]))

        elif arrows[order][0] == "NE":
            draw_polygon_alpha(screen, arrow_color[arrows[order][1]],
                               ([(x - 1) * 48 + 11, (y - 1) * 48 + 32], [(x - 1) * 48 + 19, (y - 1) * 48 + 23],
                                [(x - 1) * 48 + 16, (y - 1) * 48 + 18],
                                [(x - 1) * 48 + 35, (y - 1) * 48 + 14],
                                [(x - 1) * 48 + 31, (y - 1) * 48 + 33],
                                [(x - 1) * 48 + 26, (y - 1) * 48 + 30], [(x - 1) * 48 + 17, (y - 1) * 48 + 38]))

        elif arrows[order][0] == "E":
            draw_polygon_alpha(screen, arrow_color[arrows[order][1]],
                               ([(x - 1) * 48 + 12, (y - 1) * 48 + 20], [(x - 1) * 48 + 21, (y - 1) * 48 + 20],
                                [(x - 1) * 48 + 21, (y - 1) * 48 + 14],
                                [(x - 1) * 48 + 36, (y - 1) * 48 + 24], [(x - 1) * 48 + 36, (y - 1) * 48 + 25],
                                [(x - 1) * 48 + 21, (y - 1) * 48 + 35],
                                [(x - 1) * 48 + 21, (y - 1) * 48 + 29], [(x - 1) * 48 + 12, (y - 1) * 48 + 29]))

        elif arrows[order][0] == "W":
            draw_polygon_alpha(screen, arrow_color[arrows[order][1]],
                               ([(x - 1) * 48 + 36, (y - 1) * 48 + 20], [(x - 1) * 48 + 27, (y - 1) * 48 + 20],
                                [(x - 1) * 48 + 27, (y - 1) * 48 + 14],
                                [(x - 1) * 48 + 12, (y - 1) * 48 + 24], [(x - 1) * 48 + 12, (y - 1) * 48 + 25],
                                [(x - 1) * 48 + 27, (y - 1) * 48 + 35],
                                [(x - 1) * 48 + 27, (y - 1) * 48 + 29], [(x - 1) * 48 + 36, (y - 1) * 48 + 29]))

        elif arrows[order][0] == "SW":
            draw_polygon_alpha(screen, arrow_color[arrows[order][1]],
                               ([(x - 1) * 48 + 38, (y - 1) * 48 + 17], [(x - 1) * 48 + 30, (y - 1) * 48 + 26],
                                [(x - 1) * 48 + 33, (y - 1) * 48 + 31],
                                [(x - 1) * 48 + 14, (y - 1) * 48 + 35],
                                [(x - 1) * 48 + 18, (y - 1) * 48 + 16],
                                [(x - 1) * 48 + 23, (y - 1) * 48 + 19], [(x - 1) * 48 + 32, (y - 1) * 48 + 11]))

        elif arrows[order][0] == "S":
            draw_polygon_alpha(screen, arrow_color[arrows[order][1]],
                               ([(x - 1) * 48 + 20, (y - 1) * 48 + 12], [(x - 1) * 48 + 20, (y - 1) * 48 + 21],
                                [(x - 1) * 48 + 14, (y - 1) * 48 + 21],
                                [(x - 1) * 48 + 24, (y - 1) * 48 + 36], [(x - 1) * 48 + 25, (y - 1) * 48 + 36],
                                [(x - 1) * 48 + 35, (y - 1) * 48 + 21],
                                [(x - 1) * 48 + 29, (y - 1) * 48 + 21], [(x - 1) * 48 + 29, (y - 1) * 48 + 12]))

        elif arrows[order][0] == "SE":
            draw_polygon_alpha(screen, arrow_color[arrows[order][1]],
                               ([(x - 1) * 48 + 11, (y - 1) * 48 + 17], [(x - 1) * 48 + 19, (y - 1) * 48 + 26],
                                [(x - 1) * 48 + 16, (y - 1) * 48 + 31],
                                [(x - 1) * 48 + 35, (y - 1) * 48 + 35],
                                [(x - 1) * 48 + 31, (y - 1) * 48 + 16],
                                [(x - 1) * 48 + 26, (y - 1) * 48 + 19], [(x - 1) * 48 + 17, (y - 1) * 48 + 11]))

        order += 1
