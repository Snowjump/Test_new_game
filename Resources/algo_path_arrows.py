## Miracle battles

from Resources import game_obj
import math


def construct_path(selected_army, route):
    for army in game_obj.game_armies:
        if army.army_id == selected_army:
            # Check movement points
            minimum_movement_points = -1
            for unit in army.units:
                if minimum_movement_points < 0:
                    minimum_movement_points = unit.movement_points
                elif unit.movement_points < minimum_movement_points:
                    minimum_movement_points = unit.movement_points

            movement_points_left = minimum_movement_points

            movement_points_limit = -1
            for unit in army.units:
                if movement_points_limit < 0:
                    movement_points_limit = unit.max_movement_points
                elif unit.max_movement_points < movement_points_limit:
                    movement_points_limit = unit.max_movement_points

            army.path_arrows = []  # Starting anew
            total_points = len(route)
            order = 0
            while order < total_points:
                if order == 0:
                    pass
                else:
                    child = route[order]
                    parent = route[order - 1]
                    distance = 100 * (math.sqrt(((child[0] - parent[0]) ** 2) + ((child[1] - parent[1]) ** 2)))

                    movement_points_left -= distance
                    # print("movement_points_left - " + str(movement_points_left)
                    #       + " distance - " + str(distance))
                    if movement_points_left >= 0:
                        color = "Arrow_green"
                        # print("Arrow is green")
                    else:
                        color = "Arrow_burgundy"
                        # print("Arrow is burgundy")

                    # Direction north...
                    if child[1] < parent[1]:
                        # Direction north-west
                        if child[0] < parent[0]:
                            army.path_arrows.append(["NW", color])
                        # Direction north straight
                        elif child[0] == parent[0]:
                            army.path_arrows.append(["N", color])
                        # Direction north-east
                        elif child[0] > parent[0]:
                            army.path_arrows.append(["NE", color])
                    # Direction east or west
                    elif child[1] == parent[1]:
                        # Direction west straight
                        if child[0] < parent[0]:
                            army.path_arrows.append(["W", color])
                        # Direction east straight
                        elif child[0] > parent[0]:
                            army.path_arrows.append(["E", color])
                    # Direction south...
                    elif child[1] > parent[1]:
                        # Direction south-west
                        if child[0] < parent[0]:
                            army.path_arrows.append(["SW", color])
                        # Direction south straight
                        elif child[0] == parent[0]:
                            army.path_arrows.append(["S", color])
                        # Direction south-east
                        elif child[0] > parent[0]:
                            army.path_arrows.append(["SE", color])

                order += 1

            # print("Arrows are ready")
