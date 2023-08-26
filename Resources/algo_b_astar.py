## Miracle battles

from Resources import game_stats
from Resources import game_obj
from Content import movement_catalog
import math
import copy

# inspired by https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, MP=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

        self.MP = MP

    def __eq__(self, other):
        return self.position == other.position


# Algorithm for finding shortest path towards enemy or tile in battle
def b_astar(travel_agent, start, end, destination, base_MP, b, mode):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    left_border = 1
    right_border = int(game_stats.battle_width)
    prefinal = True

    # Check if regiment should be routing
    # Then expand its borders for movement
    for army in game_obj.game_armies:
        if army.army_id == b.queue[0].army_id:
            unit = army.units[b.queue[0].number]

            if unit.morale <= 0.0:
                left_border = 0
                right_border = int(game_stats.battle_width) + 1
                prefinal = False

    # Create start and end node
    start_node = Node(None, start, base_MP)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end, 0)
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
            if prefinal:
                return_node = copy.deepcopy(current_node.parent)
            else:
                return_node = copy.deepcopy(current_node)
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            print("algo_b_astar .. Final path is " + str(path))
            return return_node, path[::-1]  # Return reversed path

        # Generate children
        children = []
        # print("current_node - [" + str(current_node.position[0]) + "; " + str(current_node.position[1]) + "]")
        for new_position in [[-1, -1], [0, -1], [1, -1], [-1, 0],
                             [1, 0], [-1, 1], [0, 1], [1, 1]]:  # Adjacent squares

            # Get node position
            node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

            # Get direction
            direction = show_direction(current_node.position, node_position)

            # Get moving points
            MP = float(current_node.MP)
            new_g = 0

            # Make sure it isn't a parent node
            # print("list(node_position) - " + str(list(node_position)))
            # print("list(current_node.parent) - " + str(current_node.parent))
            if current_node.parent is not None:
                if list(node_position) == list(current_node.parent.position):
                    continue
            # Make sure within range
            if node_position[0] > right_border or node_position[0] < left_border \
                    or node_position[1] > game_stats.battle_height or node_position[1] < 1:
                continue

            # Make sure traversable terrain
            TileNum = (node_position[1] - 1) * game_stats.battle_width + node_position[0] - 1
            CurTileNum = (current_node.position[1] - 1) * game_stats.battle_width + current_node.position[0] - 1
            # print("Testing tile [" + str(node_position[0]) + "; " + str(node_position[1]) + "] - " + str(TileNum))

            waste = False
            if node_position[0] != left_border and node_position[0] != right_border:
                if b.battle_map[TileNum].map_object is not None:
                    if b.battle_map[TileNum].map_object.obj_type == "Structure":
                        name = b.battle_map[TileNum].map_object.obj_name
                        if direction in movement_catalog.waste_movement_dict[name]:
                            waste = True

            if game_stats.battle_width >= node_position[0] >= 1 \
                    and game_stats.battle_height >= node_position[1] >= 1:

                if mode == "March":
                    # Marching puts limitations

                    if b.battle_map[TileNum].army_id is not None and node_position != end:
                        # Army can't pass through other armies
                        # Except if this is a target
                        continue

                    elif b.battle_map[TileNum].map_object is not None:  # Army can't pass through obstacles
                        if not b.battle_map[TileNum].map_object.travel:
                            continue
                        elif b.battle_map[TileNum].map_object.obj_type == "Structure":
                            name = b.battle_map[TileNum].map_object.obj_name
                            # print(name + " - " + (str(node_position)))
                            if direction in movement_catalog.block_movement_dict[name]:
                                # Path blocked by defensive structure (like a wall) on a side of target
                                # print(str(direction) + " in  " + str(movement_catalog.block_movement_dict[name]))
                                if blocked_by_the_gate(name, direction, b):
                                    # print(str(current_node.position) + " -> " +
                                    #       str(node_position) + " blocked_by_the_gate on a side of target")
                                    continue
                                elif blocked_by_the_wall(name, direction, CurTileNum, b):
                                    continue

                    elif b.battle_map[CurTileNum].map_object is not None:
                        if b.battle_map[CurTileNum].map_object.obj_type == "Structure":
                            CurDirection = show_direction(node_position, current_node.position)
                            name = b.battle_map[CurTileNum].map_object.obj_name
                            if CurDirection in movement_catalog.block_movement_dict[name]:
                                # Path blocked by defensive structure (like a wall) on a side of current position
                                if blocked_by_the_gate(name, CurDirection, b):
                                    # print(str(current_node.position) + " -> " +
                                    #       str(node_position) + " blocked_by_the_gate on a side of current position")
                                    continue
                                elif blocked_by_the_wall(name, CurDirection, TileNum, b):
                                    continue

                    # Check while moving diagonally no obstacles located in nearby tiles
                    elif new_position in [[-1, -1], [1, -1], [-1, 1], [1, 1]]:  # Diagonal movement
                        nearby_position1 = [current_node.position[0] + new_position[0], current_node.position[1]]
                        nearby_position2 = [current_node.position[0], current_node.position[1] + new_position[1]]
                        if (game_stats.battle_width >= nearby_position1[0] >= 1) and \
                                (game_stats.battle_width >= nearby_position2[0] >= 1):
                            TileNum1 = (nearby_position1[1] - 1) * game_stats.battle_width + nearby_position1[0] - 1
                            TileNum2 = (nearby_position2[1] - 1) * game_stats.battle_width + nearby_position2[0] - 1
                            if b.battle_map[TileNum1].army_id is not None or b.battle_map[TileNum2].army_id is not None:
                                continue
                            else:
                                diagonal_obstacles = False
                                if b.battle_map[TileNum1].map_object is not None:
                                    if not b.battle_map[TileNum1].map_object.travel:
                                        diagonal_obstacles = True
                                if b.battle_map[TileNum2].map_object is not None:
                                    if not b.battle_map[TileNum2].map_object.travel:
                                        diagonal_obstacles = True
                                if diagonal_obstacles:
                                    continue

                    if waste:
                        new_g = float(MP)
                        MP = 0
                    else:
                        step = math.sqrt(((node_position[0] - current_node.position[0]) ** 2) + (
                                (node_position[1] - current_node.position[1]) ** 2))
                        if MP >= step:
                            new_g = float(step)
                            MP = MP - step
                        else:
                            new_g = float(step)
                            MP = base_MP - step

            # Create new node
            new_node = Node(current_node, node_position, MP)
            new_node.g = new_g

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
                # waste = False
                # TileNum = (child.position[1] - 1) * game_stats.battle_width + child.position[0] - 1
                # if child.position[0] != left_border and child.position[0] != right_border:
                #     if b.battle_map[TileNum].map_object is not None:
                #         if b.battle_map[TileNum].map_object.obj_type == "Structure":
                #             direction = show_direction(current_node.position, child.position)
                #             name = b.battle_map[TileNum].map_object.obj_name
                #             if direction in movement_catalog.waste_movement_dict[name]:
                #                 waste = True

                child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2))
                child.f = child.g + child.h

                # if waste:
                #     if current_node.g + (math.sqrt(((child.position[0] - current_node.position[0]) ** 2) + (
                #             (child.position[1] - current_node.position[1]) ** 2))) > MP:
                #         continue
                #     else:
                #         child.g = current_node.g + (MP - current_node.g)
                #         # ?
                #         child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + (
                #                 (child.position[1] - end_node.position[1]) ** 2))
                #         child.f = child.g + child.h
                # else:
                #     child.g = current_node.g + (math.sqrt(((child.position[0] - current_node.position[0]) ** 2) + (
                #                 (child.position[1] - current_node.position[1]) ** 2)))
                #     child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + (
                #             (child.position[1] - end_node.position[1]) ** 2))
                #     child.f = child.g + child.h

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

    return None, None


def show_direction(previous_position, new_position):
    start_direction = None
    if previous_position[0] < new_position[0]:
        if previous_position[1] < new_position[1]:
            start_direction = "NW"
        elif previous_position[1] == new_position[1]:
            start_direction = "W"
        elif previous_position[1] > new_position[1]:
            start_direction = "SW"

    elif previous_position[0] == new_position[0]:
        if previous_position[1] < new_position[1]:
            start_direction = "N"
        elif previous_position[1] > new_position[1]:
            start_direction = "S"

    elif previous_position[0] > new_position[0]:
        if previous_position[1] < new_position[1]:
            start_direction = "NE"
        elif previous_position[1] == new_position[1]:
            start_direction = "E"
        elif previous_position[1] > new_position[1]:
            start_direction = "SE"

    return start_direction


def blocked_by_the_gate(name, direction, b):
    result = False  # Movement is not blocked
    if name in movement_catalog.gates_pass_dict:
        result = True
        if direction == "W":
            if b.defender_id == b.queue[0].army_id:
                # print("Can move through the gate")
                result = False

    return result


def blocked_by_the_wall(name, direction, TileNum, b):
    result = False  # Movement is not blocked
    if name in movement_catalog.walls_block_dict:
        result = True
        if direction == "W":
            if b.battle_map[TileNum].siege_tower_deployed:
                # Siege tower is not deployed there
                result = False

    return result


# def check_flying(b, position):
#     allowed = True
#     TileNum = (position[1] - 1) * game_stats.battle_width + position[0] - 1
#
#     # Map borders limitation
#     if position[0] == int(game_stats.battle_width) + 1 or position[0] == 0:
#         print("Reached map limit - " + str(position))
#
#     else:
#         if b.battle_map[TileNum].army_id is not None:  # Army can't pass through other armies
#             allowed = False
#
#         elif b.battle_map[TileNum].map_object is not None:  # Army can't pass through obstacles
#             if not b.battle_map[TileNum].map_object.travel:
#                 allowed = False
#
#     return allowed
