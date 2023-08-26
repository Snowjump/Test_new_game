## Miracle battles

from Resources import game_stats
from Resources import game_obj
from Content import exploration_catalog

import math

# inspired by https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0

    def __eq__(self, other):
        return self.position == other.position


def routeing_astar(travel_agent, start, MP, friendly_cities, hostile_cities, known_map):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    ##    print("Start node added " + str(start_node.position))

    # Loop until you find the end
    while len(open_list) > 0:
        listik = []
        for i in open_list:
            listik.append(i.position)
        # print("Another attempt - len - " + str(len(open_list)) + " list is " + str(listik))

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        # for index, item in enumerate(open_list):
        #     if item.f < current_node.f:
        #         current_node = item
        #         current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # if current_node.parent is not None:
        #     print("Current node " + str(current_node.position) + " with F - " + str(current_node.f) + " and parent - "
        #     + str(current_node.parent.position))
        # else:
        #     print("Current node " + str(current_node.position) + " with F - " + str(current_node.f))

        # Found the goal
        # if current_node == end_node:
        #     path = []
        #     current = current_node
        #     while current is not None:
        #         path.append(current.position)
        #         current = current.parent
        #     print("Final path is " + str(path))
        #     return path[::-1]  # Return reversed path

        # Generate children
        children = []
        # print("current_node - [" + str(current_node.position[0]) + "; " + str(current_node.position[1]) + "]")
        for new_position in [[-1, -1], [0, -1], [1, -1], [-1, 0],
                             [1, 0], [-1, 1], [0, 1], [1, 1]]:  # Adjacent squares

            # Get node position
            node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

            # Make sure it isn't a parent node
            # print("list(node_position) - " + str(list(node_position)))
            # print("list(current_node.parent) - " + str(current_node.parent))
            if current_node.parent is not None:
                if list(node_position) == list(current_node.parent.position):
                    continue

            # Make sure within range
            if node_position[0] > game_stats.cur_level_width or node_position[0] < 1 \
                    or node_position[1] > game_stats.cur_level_height or node_position[1] < 1:
                continue

            # Make sure walkable terrain
            TileNum = (node_position[1] - 1) * game_stats.cur_level_width + node_position[0] - 1
            # print("Testing tile [" + str(node_position[0]) + "; " + str(node_position[1]) + "] - " + str(TileNum))

            new_range = (current_node.g + (math.sqrt(((node_position[0] - current_node.position[0]) ** 2) + (
                    (node_position[1] - current_node.position[1]) ** 2)))) * 100

            if new_range > MP:
                continue

            if node_position in known_map:
                if not game_obj.game_map[TileNum].travel:  # No obstacles
                    continue

                if game_obj.game_map[TileNum].city_id is not None:
                    # Forbidden territory
                    if game_obj.game_map[TileNum].city_id not in friendly_cities \
                            and game_obj.game_map[TileNum].city_id not in hostile_cities:
                        continue

                if game_obj.game_map[TileNum].army_id is not None:  # Army can't pass through other armies
                    continue

                if game_obj.game_map[TileNum].lot is not None:
                    if game_obj.game_map[TileNum].lot == "City":  # Army can't pass through settlement
                        continue
                    # For now army can’t pass through facilities and exploration objects
                    # may reconsider later
                    elif game_obj.game_map[TileNum].lot.obj_typ == "Facility" or \
                            game_obj.game_map[TileNum].lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                        continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
            # print("Child " + str(node_position) + " added to children " + str(len(children)))

        # Loop through children
        for child in children:
            # print("Loop through children - " + str(child.position))

            closed_list_status = True  # Not in closed list yet
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    # print("Closed list len - " + str(len(closed_list)) + ", child - " + str(child.position))
                    closed_list_status = False
                    continue

            if closed_list_status:

                # Create the f, g, and h values
                child.g = current_node.g + (math.sqrt(((child.position[0] - current_node.position[0]) ** 2) + (
                            (child.position[1] - current_node.position[1]) ** 2)))

                # print("Child " + str(child.position) + " : f - " + str(child.f) + " = g - " + str(child.g) + " + h - "
                #       + str(child.h))

                append_true = True
                # print("open_list - " + str(len(open_list)))
                # Child is already in the open list
                for open_node in open_list:
                    # print("child.g " + str(child.position) + " g - " + str(child.g) + " and open_node.g "
                    #       + str(open_node.position) + " g - " + str(open_node.g))
                    # if child == open_node:
                    #     print("child == open_node is True")
                    # if child.g > open_node.g:
                    #     print("child.g > open_node.g is True")
                    if child == open_node and child.g >= open_node.g:
                        # print("Both true")
                        append_true = False
                        continue
                    elif child == open_node and child.g < open_node.g:
                        # print("Even better")
                        open_list.remove(open_node)
                        continue

                    ##            print("Added child " + str(child.position) + " and F - " + str(child.f))
                    # Add the child to the open list
                if append_true:
                    # print("Append child " + str(child.position) + " : f - " + str(child.f) + " = g - " + str(child.g)
                    #       + " + h - " + str(child.h))
                    open_list.append(child)

    if len(open_list) == 0:
        path = list(closed_list)
        # current = current_node
        # while current is not None:
        #     path.append(current.position)
        #     current = current.parent
        # print("Final path is " + str(len(path)))
        grid_map = []
        for one_node in path:
            if one_node.position != start:
                grid_map.append(one_node.position)
        # print("All tiles: " + str(grid_map))
        return path, grid_map  # Return whole path
