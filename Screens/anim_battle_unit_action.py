## Miracle battles

from Resources import game_stats
import math


def unit_march(b, unit_index, parent, creature_position, number, row, line, width, height, rows, owner):
    if unit_index == b.queue[0].number and owner == b.queue[0].owner:
        # print("b.tile_trail - " + str(b.tile_trail))
        child = list(b.tile_trail[0])
        x = int(child[0]) - int(b.battle_pov[0])
        y = int(child[1]) - int(b.battle_pov[1])

        new_direction = ""
        if parent[0] == child[0]:
            if parent[1] > child[1]:
                new_direction = "N"
            elif parent[1] < child[1]:
                new_direction = "S"
        elif parent[0] > child[0]:
            if parent[1] > child[1]:
                new_direction = "NW"
            elif parent[1] < child[1]:
                new_direction = "SW"
            elif parent[1] == child[1]:
                new_direction = "W"
        elif parent[0] < child[0]:
            if parent[1] > child[1]:
                new_direction = "NE"
            elif parent[1] < child[1]:
                new_direction = "SE"
            elif parent[1] == child[1]:
                new_direction = "E"

        if new_direction == "E":
            new_position = [(x - 1) * 96 + 4 + 90 - width - (row - 1) * ((90 - width) / (rows - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / (number - 1))]

        elif new_direction == "W":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (row - 1) * ((90 - width) / (rows - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / (number - 1))]

        elif new_direction == "N":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (number - line) * ((90 - width) / (number - 1)),
                            (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                            (row - 1) * ((90 - height) / (rows - 1))]

        elif new_direction == "S":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (number - line) * ((90 - width) / (number - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (row - 1) * ((90 - height) / (rows - 1))]

        elif new_direction == "NE":
            new_position = [(x - 1) * 96 + 48 - (width / 2) -
                            (row - 1) * (48 / (rows - 1)) + (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) -
                            (number - line) * (48 / (number - 1)) +
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "NW":
            new_position = [(x - 1) * 96 + 48 - (width / 2) +
                            (row - 1) * (48 / (rows - 1)) - (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) -
                            (number - line) * (48 / (number - 1)) +
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "SE":
            new_position = [(x - 1) * 96 + 48 - (width / 2) -
                            (row - 1) * (48 / (rows - 1)) + (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) +
                            (number - line) * (48 / (number - 1)) -
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "SW":
            new_position = [(x - 1) * 96 + 48 - (width / 2) +
                            (row - 1) * (48 / (rows - 1)) - (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) +
                            (number - line) * (48 / (number - 1)) -
                            (row - 1) * (40 / (rows - 1))]

        x = (new_position[0] - creature_position[0])
        y = (new_position[1] - creature_position[1])
        spread = (b.battle_display_time/1000 - b.battle_last_change) / 1
        # print(str(abs((spread * 1000) % 500 - 250)))
        # print(str(((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12))
        # 0 - 500
        # -250 - 250
        # 250 - 0 - 250
        # 0 - 250 - 0
        # 0 - 1 - 0
        # 0 - -12 - 0
        k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12
        return [x * spread, y * spread + k]
    else:
        return [0, 0]


def unit_rotate(b, unit_index, owner, current_position, creature_position, number, row, line, width, height, rows):
    if unit_index in b.attacking_rotate and owner == b.queue[0].owner:
        child = list(b.target_destination)

        parent = list(current_position)
        x = int(parent[0]) - int(b.battle_pov[0])
        y = int(parent[1]) - int(b.battle_pov[1])

        new_direction = ""
        if parent[0] == child[0]:
            if parent[1] > child[1]:
                new_direction = "N"
            elif parent[1] < child[1]:
                new_direction = "S"
        elif parent[0] > child[0]:
            if parent[1] > child[1]:
                new_direction = "NW"
            elif parent[1] < child[1]:
                new_direction = "SW"
            elif parent[1] == child[1]:
                new_direction = "W"
        elif parent[0] < child[0]:
            if parent[1] > child[1]:
                new_direction = "NE"
            elif parent[1] < child[1]:
                new_direction = "SE"
            elif parent[1] == child[1]:
                new_direction = "E"

        if new_direction == "E":
            new_position = [(x - 1) * 96 + 4 + 90 - width - (row - 1) * ((90 - width) / (rows - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / (number - 1))]

        elif new_direction == "W":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (row - 1) * ((90 - width) / (rows - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / (number - 1))]

        elif new_direction == "N":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (number - line) * ((90 - width) / (number - 1)),
                            (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                            (row - 1) * ((90 - height) / (rows - 1))]

        elif new_direction == "S":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (number - line) * ((90 - width) / (number - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (row - 1) * ((90 - height) / (rows - 1))]

        elif new_direction == "NE":
            new_position = [(x - 1) * 96 + 48 - (width / 2) -
                            (row - 1) * (48 / (rows - 1)) + (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) -
                            (number - line) * (48 / (number - 1)) +
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "NW":
            new_position = [(x - 1) * 96 + 48 - (width / 2) +
                            (row - 1) * (48 / (rows - 1)) - (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) -
                            (number - line) * (48 / (number - 1)) +
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "SE":
            new_position = [(x - 1) * 96 + 48 - (width / 2) -
                            (row - 1) * (48 / (rows - 1)) + (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) +
                            (number - line) * (48 / (number - 1)) -
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "SW":
            new_position = [(x - 1) * 96 + 48 - (width / 2) +
                            (row - 1) * (48 / (rows - 1)) - (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) +
                            (number - line) * (48 / (number - 1)) -
                            (row - 1) * (40 / (rows - 1))]

        x = (new_position[0] - creature_position[0])
        y = (new_position[1] - creature_position[1])
        spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
        # print(str(abs((spread * 1000) % 500 - 250)))
        # print(str(((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12))
        # 0 - 500
        # -250 - 250
        # 250 - 0 - 250
        # 0 - 250 - 0
        # 0 - 1 - 0
        # 0 - -12 - 0
        k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12
        return [x * spread, y * spread + k]

    elif unit_index in b.defending_rotate and owner == b.enemy:
        child = list(b.queue[0].position)

        parent = list(current_position)
        x = int(parent[0]) - int(b.battle_pov[0])
        y = int(parent[1]) - int(b.battle_pov[1])

        new_direction = ""
        if parent[0] == child[0]:
            if parent[1] > child[1]:
                new_direction = "N"
            elif parent[1] < child[1]:
                new_direction = "S"
        elif parent[0] > child[0]:
            if parent[1] > child[1]:
                new_direction = "NW"
            elif parent[1] < child[1]:
                new_direction = "SW"
            elif parent[1] == child[1]:
                new_direction = "W"
        elif parent[0] < child[0]:
            if parent[1] > child[1]:
                new_direction = "NE"
            elif parent[1] < child[1]:
                new_direction = "SE"
            elif parent[1] == child[1]:
                new_direction = "E"

        if new_direction == "E":
            new_position = [(x - 1) * 96 + 4 + 90 - width - (row - 1) * ((90 - width) / (rows - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / (number - 1))]

        elif new_direction == "W":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (row - 1) * ((90 - width) / (rows - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / (number - 1))]

        elif new_direction == "N":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (number - line) * ((90 - width) / (number - 1)),
                            (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                            (row - 1) * ((90 - height) / (rows - 1))]

        elif new_direction == "S":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (number - line) * ((90 - width) / (number - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (row - 1) * ((90 - height) / (rows - 1))]

        elif new_direction == "NE":
            new_position = [(x - 1) * 96 + 48 - (width / 2) -
                            (row - 1) * (48 / (rows - 1)) + (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) -
                            (number - line) * (48 / (number - 1)) +
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "NW":
            new_position = [(x - 1) * 96 + 48 - (width / 2) +
                            (row - 1) * (48 / (rows - 1)) - (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) -
                            (number - line) * (48 / (number - 1)) +
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "SE":
            new_position = [(x - 1) * 96 + 48 - (width / 2) -
                            (row - 1) * (48 / (rows - 1)) + (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) +
                            (number - line) * (48 / (number - 1)) -
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "SW":
            new_position = [(x - 1) * 96 + 48 - (width / 2) +
                            (row - 1) * (48 / (rows - 1)) - (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) +
                            (number - line) * (48 / (number - 1)) -
                            (row - 1) * (40 / (rows - 1))]

        x = (new_position[0] - creature_position[0])
        y = (new_position[1] - creature_position[1])
        spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
        # print(str(abs((spread * 1000) % 500 - 250)))
        # print(str(((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12))
        # 0 - 500
        # -250 - 250
        # 250 - 0 - 250
        # 0 - 250 - 0
        # 0 - 1 - 0
        # 0 - -12 - 0
        k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12
        return [x * spread, y * spread + k]

    elif b.secondary == "Ranged attack" and unit_index == b.queue[0].number and owner == b.realm_in_control:
        new_direction = str(b.changed_direction)
        parent = list(current_position)
        x = int(parent[0]) - int(b.battle_pov[0])
        y = int(parent[1]) - int(b.battle_pov[1])

        if new_direction == "E":
            new_position = [(x - 1) * 96 + 4 + 90 - width - (row - 1) * ((90 - width) / (rows - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / (number - 1))]

        elif new_direction == "W":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (row - 1) * ((90 - width) / (rows - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / (number - 1))]

        elif new_direction == "N":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (number - line) * ((90 - width) / (number - 1)),
                            (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                            (row - 1) * ((90 - height) / (rows - 1))]

        elif new_direction == "S":
            new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                            (number - line) * ((90 - width) / (number - 1)),
                            (y - 1) * 96 + 4 + 90 - height - (row - 1) * ((90 - height) / (rows - 1))]

        elif new_direction == "NE":
            new_position = [(x - 1) * 96 + 48 - (width / 2) -
                            (row - 1) * (48 / (rows - 1)) + (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) -
                            (number - line) * (48 / (number - 1)) +
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "NW":
            new_position = [(x - 1) * 96 + 48 - (width / 2) +
                            (row - 1) * (48 / (rows - 1)) - (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) -
                            (number - line) * (48 / (number - 1)) +
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "SE":
            new_position = [(x - 1) * 96 + 48 - (width / 2) -
                            (row - 1) * (48 / (rows - 1)) + (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) +
                            (number - line) * (48 / (number - 1)) -
                            (row - 1) * (40 / (rows - 1))]

        elif new_direction == "SW":
            new_position = [(x - 1) * 96 + 48 - (width / 2) +
                            (row - 1) * (48 / (rows - 1)) - (line - 1) * (40 / (number - 1)),
                            (y - 1) * 96 + 48 - (height / 2) +
                            (number - line) * (48 / (number - 1)) -
                            (row - 1) * (40 / (rows - 1))]

        x = (new_position[0] - creature_position[0])
        y = (new_position[1] - creature_position[1])
        spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
        # print(str(abs((spread * 1000) % 500 - 250)))
        # print(str(((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12))
        # 0 - 500
        # -250 - 250
        # 250 - 0 - 250
        # 0 - 250 - 0
        # 0 - 1 - 0
        # 0 - -12 - 0
        k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12
        return [x * spread, y * spread + k]

    else:
        return [0, 0]
