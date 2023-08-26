## Miracle battles

from Resources import game_stats
import math


def movement_animation(b, x, y):
    if b.move_figure is None:
        # Marching
        # x = (new_position[0] - creature_position[0])
        # y = (new_position[1] - creature_position[1])
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
        # Flying
        # x = (new_position[0] - creature_position[0])
        # y = (new_position[1] - creature_position[1])
        spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
        elevation = 50
        if b.move_figure == "takeoff":
            if spread * 1000 <= 500:
                elevation = 50 * ((spread * 1000) / 500)
                # print(str(elevation) + "   " + str(spread))
        elif b.move_figure == "landing":
            if spread * 1000 > 500:
                elevation = 50 - 50 * ((spread * 1000) % 500 / 500)

        elif b.move_figure == "1 tile hop":
            if spread * 1000 <= 500:
                elevation = 50 * ((spread * 1000) / 500)
            else:
                elevation = 50 - 50 * ((spread * 1000) % 500 / 500)
                # print(str(elevation) + "   " + str(spread))

        # print((spread * 1000) % 500)
        k = ((500 - abs(spread * 1000 - 500)) / 500) * -16

        return [x * spread, y * spread + k - elevation]


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

        div_row = rows - 1
        if div_row == 0:
            div_row = 1

        div_number = number - 1
        if div_number == 0:
            div_number = 1

        if new_direction == "E":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + 90 - width,
                                (y - 1) * 96 + 4 + 90 - height - (48 - height / 2)]
            else:
                new_position = [(x - 1) * 96 + 4 + 90 - width - (row - 1) * ((90 - width) / div_row),
                                (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / div_number)]

        elif new_direction == "W":
            if number == 1:
                new_position = [(x - 1) * 96 + 4,
                                (y - 1) * 96 + 4 + 90 - height - (48 - height / 2)]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (row - 1) * ((90 - width) / div_row),
                                (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / div_number)]

        elif new_direction == "N":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + (48 - width / 2),
                                (y - 1) * 96 + 4]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (number - line) * ((90 - width) / div_number),
                                (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                                (row - 1) * ((90 - height) / div_row)]

        elif new_direction == "S":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + (48 - width / 2),
                                (y - 1) * 96 + 4 + 90 - height]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (number - line) * ((90 - width) / div_number),
                                (y - 1) * 96 + 4 + 90 - height - (row - 1) * ((90 - height) / div_row)]

        elif new_direction == "NE":
            if number == 1:
                new_position = [(x - 1) * 96 + 48,
                                (y - 1) * 96 + 48 - height]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) -
                                (row - 1) * (48 / div_row) + (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) -
                                (number - line) * (48 / div_number) + (row - 1) * (40 / div_row)]

        elif new_direction == "NW":
            if number == 1:
                new_position = [(x - 1) * 96 + 48 - width,
                                (y - 1) * 96 + 48 - height]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) +
                                (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) -
                                (number - line) * (48 / div_number) + (row - 1) * (40 / div_row)]

        elif new_direction == "SE":
            if number == 1:
                new_position = [(x - 1) * 96 + 48,
                                (y - 1) * 96 + 48]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) -
                                (row - 1) * (48 / div_row) + (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) +
                                (number - line) * (48 / div_number) - (row - 1) * (40 / div_row)]

        elif new_direction == "SW":
            if number == 1:
                new_position = [(x - 1) * 96 + 48 - width,
                                (y - 1) * 96 + 48]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) +
                                (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) +
                                (number - line) * (48 / div_number) - (row - 1) * (40 / div_row)]

        x = (new_position[0] - creature_position[0])
        y = (new_position[1] - creature_position[1])
        # spread = (b.battle_display_time/1000 - b.battle_last_change) / 1
        # # print(str(abs((spread * 1000) % 500 - 250)))
        # # print(str(((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12))
        # # 0 - 500
        # # -250 - 250
        # # 250 - 0 - 250
        # # 0 - 250 - 0
        # # 0 - 1 - 0
        # # 0 - -12 - 0
        # k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12
        # return [x * spread, y * spread + k]

        return movement_animation(b, x, y)
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

        div_row = rows - 1
        if div_row == 0:
            div_row = 1

        div_number = number - 1
        if div_number == 0:
            div_number = 1

        if new_direction == "E":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + 90 - width,
                                (y - 1) * 96 + 4 + 90 - height - (48 - height / 2)]
            else:
                new_position = [(x - 1) * 96 + 4 + 90 - width - (row - 1) * ((90 - width) / div_row),
                                (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / div_number)]

        elif new_direction == "W":
            if number == 1:
                new_position = [(x - 1) * 96 + 4,
                                (y - 1) * 96 + 4 + 90 - height - (48 - height / 2)]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (row - 1) * ((90 - width) / div_row),
                                (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / div_number)]

        elif new_direction == "N":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + (48 - width / 2),
                                (y - 1) * 96 + 4]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (number - line) * ((90 - width) / div_number),
                                (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                                (row - 1) * ((90 - height) / div_row)]

        elif new_direction == "S":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + (48 - width / 2),
                                (y - 1) * 96 + 4 + 90 - height]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (number - line) * ((90 - width) / div_number),
                                (y - 1) * 96 + 4 + 90 - height - (row - 1) * ((90 - height) / div_row)]

        elif new_direction == "NE":
            if number == 1:
                new_position = [(x - 1) * 96 + 48,
                                (y - 1) * 96 + 48 - height]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) -
                                (row - 1) * (48 / div_row) + (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) -
                                (number - line) * (48 / div_number) + (row - 1) * (40 / div_row)]

        elif new_direction == "NW":
            if number == 1:
                new_position = [(x - 1) * 96 + 48 - width,
                                (y - 1) * 96 + 48 - height]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) +
                                (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) -
                                (number - line) * (48 / div_number) + (row - 1) * (40 / div_row)]

        elif new_direction == "SE":
            if number == 1:
                new_position = [(x - 1) * 96 + 48,
                                (y - 1) * 96 + 48]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) -
                                (row - 1) * (48 / div_row) + (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) +
                                (number - line) * (48 / div_number) - (row - 1) * (40 / div_row)]

        elif new_direction == "SW":
            if number == 1:
                new_position = [(x - 1) * 96 + 48 - width,
                                (y - 1) * 96 + 48]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) +
                                (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) +
                                (number - line) * (48 / div_number) - (row - 1) * (40 / div_row)]

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

        div_row = rows - 1
        if div_row == 0:
            div_row = 1

        div_number = number - 1
        if div_number == 0:
            div_number = 1

        if new_direction == "E":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + 90 - width,
                                (y - 1) * 96 + 4 + 90 - height - (48 - height / 2)]
            else:
                new_position = [(x - 1) * 96 + 4 + 90 - width - (row - 1) * ((90 - width) / div_row),
                                (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / div_number)]

        elif new_direction == "W":
            if number == 1:
                new_position = [(x - 1) * 96 + 4,
                                (y - 1) * 96 + 4 + 90 - height - (48 - height / 2)]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (row - 1) * ((90 - width) / div_row),
                                (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / div_number)]

        elif new_direction == "N":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + (48 - width / 2),
                                (y - 1) * 96 + 4]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (number - line) * ((90 - width) / div_number),
                                (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                                (row - 1) * ((90 - height) / div_row)]

        elif new_direction == "S":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + (48 - width / 2),
                                (y - 1) * 96 + 4 + 90 - height]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (number - line) * ((90 - width) / div_number),
                                (y - 1) * 96 + 4 + 90 - height - (row - 1) * ((90 - height) / div_row)]

        elif new_direction == "NE":
            if number == 1:
                new_position = [(x - 1) * 96 + 48,
                                (y - 1) * 96 + 48 - height]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) -
                                (row - 1) * (48 / div_row) + (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) -
                                (number - line) * (48 / div_number) + (row - 1) * (40 / div_row)]

        elif new_direction == "NW":
            if number == 1:
                new_position = [(x - 1) * 96 + 48 - width,
                                (y - 1) * 96 + 48 - height]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) +
                                (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) -
                                (number - line) * (48 / div_number) + (row - 1) * (40 / div_row)]

        elif new_direction == "SE":
            if number == 1:
                new_position = [(x - 1) * 96 + 48,
                                (y - 1) * 96 + 48]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) -
                                (row - 1) * (48 / div_row) + (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) +
                                (number - line) * (48 / div_number) - (row - 1) * (40 / div_row)]

        elif new_direction == "SW":
            if number == 1:
                new_position = [(x - 1) * 96 + 48 - width,
                                (y - 1) * 96 + 48]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) +
                                (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) +
                                (number - line) * (48 / div_number) - (row - 1) * (40 / div_row)]

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

        div_row = rows - 1
        if div_row == 0:
            div_row = 1

        div_number = number - 1
        if div_number == 0:
            div_number = 1

        if new_direction == "E":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + 90 - width,
                                (y - 1) * 96 + 4 + 90 - height - (48 - height / 2)]
            else:
                new_position = [(x - 1) * 96 + 4 + 90 - width - (row - 1) * ((90 - width) / div_row),
                                (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / div_number)]

        elif new_direction == "W":
            if number == 1:
                new_position = [(x - 1) * 96 + 4,
                                (y - 1) * 96 + 4 + 90 - height - (48 - height / 2)]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (row - 1) * ((90 - width) / div_row),
                                (y - 1) * 96 + 4 + 90 - height - (number - line) * ((90 - height) / div_number)]

        elif new_direction == "N":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + (48 - width / 2),
                                (y - 1) * 96 + 4]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (number - line) * ((90 - width) / div_number),
                                (y - 1) * 96 + 4 +  # 90 - unit.crew[index].img_height -
                                (row - 1) * ((90 - height) / div_row)]

        elif new_direction == "S":
            if number == 1:
                new_position = [(x - 1) * 96 + 4 + (48 - width / 2),
                                (y - 1) * 96 + 4 + 90 - height]
            else:
                new_position = [(x - 1) * 96 + 4 +  # unit.crew[index].img_width +
                                (number - line) * ((90 - width) / div_number),
                                (y - 1) * 96 + 4 + 90 - height - (row - 1) * ((90 - height) / div_row)]

        elif new_direction == "NE":
            if number == 1:
                new_position = [(x - 1) * 96 + 48,
                                (y - 1) * 96 + 48 - height]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) -
                                (row - 1) * (48 / div_row) + (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) -
                                (number - line) * (48 / div_number) + (row - 1) * (40 / div_row)]

        elif new_direction == "NW":
            if number == 1:
                new_position = [(x - 1) * 96 + 48 - width,
                                (y - 1) * 96 + 48 - height]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) +
                                (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) -
                                (number - line) * (48 / div_number) + (row - 1) * (40 / div_row)]

        elif new_direction == "SE":
            if number == 1:
                new_position = [(x - 1) * 96 + 48,
                                (y - 1) * 96 + 48]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) -
                                (row - 1) * (48 / div_row) + (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) +
                                (number - line) * (48 / div_number) - (row - 1) * (40 / div_row)]

        elif new_direction == "SW":
            if number == 1:
                new_position = [(x - 1) * 96 + 48 - width,
                                (y - 1) * 96 + 48]
            else:
                new_position = [(x - 1) * 96 + 48 - (width / 2) +
                                (row - 1) * (48 / div_row) - (line - 1) * (40 / div_number),
                                (y - 1) * 96 + 48 - (height / 2) +
                                (number - line) * (48 / div_number) - (row - 1) * (40 / div_row)]

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


def machine_march(b, unit_index, parent, creature_position, owner, img_width, img_height):
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

        new_position = []
        if new_direction == "E":
            new_position = [(x - 1) * 96 + 90 - img_width,
                            (y - 1) * 96 + 60 - img_height]

        elif new_direction == "W":
            new_position = [(x - 1) * 96 + 7,
                            (y - 1) * 96 + 60 - img_height]

        elif new_direction == "N":
            new_position = [(x - 1) * 96 + 49 - (img_width / 2),
                            (y - 1) * 96 + 35 - img_height]

        elif new_direction == "S":
            new_position = [(x - 1) * 96 + 49 - (img_width / 2),
                            (y - 1) * 96 + 81 - img_height]

        elif new_direction == "NE":
            new_position = [(x - 1) * 96 + 65 - (img_width / 2),
                            (y - 1) * 96 + 28 - img_height]

        elif new_direction == "NW":
            new_position = [(x - 1) * 96 + 32 - (img_width / 2),
                            (y - 1) * 96 + 28 - img_height]

        elif new_direction == "SE":
            new_position = [(x - 1) * 96 + 65 - (img_width / 2),
                            (y - 1) * 96 + 75 - img_height]

        elif new_direction == "SW":
            new_position = [(x - 1) * 96 + 32 - (img_width / 2),
                            (y - 1) * 96 + 75 - img_height]

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
        k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -6
        return [x * spread, y * spread + k]
    else:
        return [0, 0]


def machine_rotate(b, unit_index, owner, current_position, creature_position, img_width, img_height):
    new_position = []
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
            new_position = [(x - 1) * 96 + 90 - img_width,
                            (y - 1) * 96 + 60 - img_height]

        elif new_direction == "W":
            new_position = [(x - 1) * 96 + 7,
                            (y - 1) * 96 + 60 - img_height]

        elif new_direction == "N":
            new_position = [(x - 1) * 96 + 49 - (img_width / 2),
                            (y - 1) * 96 + 35 - img_height]

        elif new_direction == "S":
            new_position = [(x - 1) * 96 + 49 - (img_width / 2),
                            (y - 1) * 96 + 81 - img_height]

        elif new_direction == "NE":
            new_position = [(x - 1) * 96 + 65 - (img_width / 2),
                            (y - 1) * 96 + 28 - img_height]

        elif new_direction == "NW":
            new_position = [(x - 1) * 96 + 32 - (img_width / 2),
                            (y - 1) * 96 + 28 - img_height]

        elif new_direction == "SE":
            new_position = [(x - 1) * 96 + 65 - (img_width / 2),
                            (y - 1) * 96 + 75 - img_height]

        elif new_direction == "SW":
            new_position = [(x - 1) * 96 + 32 - (img_width / 2),
                            (y - 1) * 96 + 75 - img_height]

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
        k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -6
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
            new_position = [(x - 1) * 96 + 90 - img_width,
                            (y - 1) * 96 + 60 - img_height]

        elif new_direction == "W":
            new_position = [(x - 1) * 96 + 7,
                            (y - 1) * 96 + 60 - img_height]

        elif new_direction == "N":
            new_position = [(x - 1) * 96 + 49 - (img_width / 2),
                            (y - 1) * 96 + 35 - img_height]

        elif new_direction == "S":
            new_position = [(x - 1) * 96 + 49 - (img_width / 2),
                            (y - 1) * 96 + 81 - img_height]

        elif new_direction == "NE":
            new_position = [(x - 1) * 96 + 65 - (img_width / 2),
                            (y - 1) * 96 + 28 - img_height]

        elif new_direction == "NW":
            new_position = [(x - 1) * 96 + 32 - (img_width / 2),
                            (y - 1) * 96 + 28 - img_height]

        elif new_direction == "SE":
            new_position = [(x - 1) * 96 + 65 - (img_width / 2),
                            (y - 1) * 96 + 75 - img_height]

        elif new_direction == "SW":
            new_position = [(x - 1) * 96 + 32 - (img_width / 2),
                            (y - 1) * 96 + 75 - img_height]

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
        k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -6
        return [x * spread, y * spread + k]

    elif b.secondary == "Ranged attack" and unit_index == b.queue[0].number and owner == b.realm_in_control:
        new_direction = str(b.changed_direction)
        parent = list(current_position)
        x = int(parent[0]) - int(b.battle_pov[0])
        y = int(parent[1]) - int(b.battle_pov[1])

        if new_direction == "E":
            new_position = [(x - 1) * 96 + 90 - img_width,
                            (y - 1) * 96 + 60 - img_height]

        elif new_direction == "W":
            new_position = [(x - 1) * 96 + 7,
                            (y - 1) * 96 + 60 - img_height]

        elif new_direction == "N":
            new_position = [(x - 1) * 96 + 49 - (img_width / 2),
                            (y - 1) * 96 + 35 - img_height]

        elif new_direction == "S":
            new_position = [(x - 1) * 96 + 49 - (img_width / 2),
                            (y - 1) * 96 + 81 - img_height]

        elif new_direction == "NE":
            new_position = [(x - 1) * 96 + 65 - (img_width / 2),
                            (y - 1) * 96 + 28 - img_height]

        elif new_direction == "NW":
            new_position = [(x - 1) * 96 + 32 - (img_width / 2),
                            (y - 1) * 96 + 28 - img_height]

        elif new_direction == "SE":
            new_position = [(x - 1) * 96 + 65 - (img_width / 2),
                            (y - 1) * 96 + 75 - img_height]

        elif new_direction == "SW":
            new_position = [(x - 1) * 96 + 32 - (img_width / 2),
                            (y - 1) * 96 + 75 - img_height]

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
        k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -6
        return [x * spread, y * spread + k]

    else:
        return [0, 0]


def unit_nosedive(b, unit_index, owner):
    if unit_index == b.queue[0].number and owner == b.queue[0].owner and b.move_figure == "nosedive":
        # This regiment is striking enemy from above
        spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
        elevation = 50

        if spread * 1000 <= 500:
            elevation = 50 - 50 * ((spread * 1000) / 500)
            # pass
        else:
            elevation = -50 + 50 * ((spread * 1000) / 500)
            # pass

        k = ((500 - abs(spread * 1000 - 500)) / 500) * -24  # -24 not too big amplitude

        # print("nosedive " + str(spread) + "   " + str(k) + "   " + str(elevation) + " = " + str(k - elevation))

        return [0, k - elevation]

    else:
        return [0, 0]
