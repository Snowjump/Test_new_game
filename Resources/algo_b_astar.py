## Miracle battles

from Resources import game_stats
from Resources import game_obj
import math
import copy

# inspired by https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# Algorithm for finding shortest path towards enemy or tile in battle
def b_astar(travel_agent, start, end, destination, b):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    ##    print("Start node added " + str(start_node.position))

    # Loop until you find the end
    while len(open_list) > 0:


        # Get the current node
        current_node = open_list[0]



        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # listik = []
        # for i in open_list:
        #     listik.append(i.position)
        # closed_listik = []
        # for i in closed_list:
        #     closed_listik.append(i.position)
        #
        # print("Another attempt for " + str(current_node.position) + ", len - " +
        #       str(len(open_list)) + " list is " + str(listik))
        # print("closed_list len - " + str(len(closed_list)) + " list is " + str(closed_listik))

        # if current_node.parent is not None:
        #     print("Current node " + str(current_node.position) + " with F - " + str(current_node.f) + " and parent - "
        #     + str(current_node.parent.position))
        # else:
        #     print("Current node " + str(current_node.position) + " with F - " + str(current_node.f))

        # Found the goal
        if current_node == end_node:
            prefinal_node = copy.deepcopy(current_node.parent)
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            print("Final path is " + str(path))
            return prefinal_node, path[::-1]  # Return reversed path

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
            if node_position[0] > game_stats.battle_width or node_position[0] < 1 \
                    or node_position[1] > game_stats.battle_height or node_position[1] < 1:
                continue

            # Make sure walkable terrain
            TileNum = (node_position[1] - 1) * game_stats.battle_width + node_position[0] - 1
            # print("Testing tile [" + str(node_position[0]) + "; " + str(node_position[1]) + "] - " + str(TileNum))

            if b.battle_map[TileNum].army_id is not None and node_position != end:
                # Army can't pass through other armies
                # Except if this is a target
                continue

            elif b.battle_map[TileNum].obstacle is not None:  # Army can't pass through obstacles
                continue

            # Check while moving diagonally no obstacles located in nearby tiles
            elif new_position in [[-1, -1], [1, -1], [-1, 1], [1, 1]]:  # Diagonal movement
                nearby_position1 = [current_node.position[0] + new_position[0], current_node.position[1]]
                nearby_position2 = [current_node.position[0], current_node.position[1] + new_position[1]]
                TileNum1 = (nearby_position1[1] - 1) * game_stats.battle_width + nearby_position1[0] - 1
                TileNum2 = (nearby_position2[1] - 1) * game_stats.battle_width + nearby_position2[0] - 1
                if b.battle_map[TileNum1].army_id is not None or b.battle_map[TileNum2].army_id is not None:
                    continue
                elif b.battle_map[TileNum1].obstacle is not None or b.battle_map[TileNum2].obstacle is not None:
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
                child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + (
                            (child.position[1] - end_node.position[1]) ** 2))
                child.f = child.g + child.h
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
                        # print("Both true " + str(child.position))
                        append_true = False
                        continue
                    elif child == open_node and child.g < open_node.g:
                        # print("Even better " + str(child.position))
                        open_list.remove(open_node)
                        continue

                    ##            print("Added child " + str(child.position) + " and F - " + str(child.f))
                    # Add the child to the open list
                if append_true:
                    # print("Append child " + str(child.position) + " : f - " + str(child.f) + " = g - " + str(child.g)
                    #       + " + h - " + str(child.h))
                    open_list.append(child)

    return None
