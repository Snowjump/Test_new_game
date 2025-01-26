## Among Myth and Wonder
## effect_classes


class Battle_Effect:
    def __init__(self, name, until_next_turn, start_time, end_time, buffs):
        self.name = name
        self.until_next_turn = until_next_turn
        self.start_time = start_time
        self.end_time = end_time
        self.buffs = buffs  # List of buffs and debuffs


class Buff:
    def __init__(self, application, quantity, method, quality):
        self.application = application
        self.quantity = quantity
        self.method = method
        self.quality = quality


# class Battle_Structure_Properties:
#     def __init__(self, waste_movement, unbroken_block_movement, effects):
#         self.unbroken = True
#         self.waste_movement = waste_movement  # List of: NW, N, NE, E, SE, S, SW, W
#         self.unbroken_block_movement = unbroken_block_movement  # List of: NW, N, NE, E, SE, S, SW, W
#         self.effects = effects  # List of Battle_Structure_Effect

class Battle_Structure_Properties:
    def __init__(self, effects):
        self.unbroken = True
        self.effects = effects  # List of Battle_Structure_Effect


class Battle_Structure_Effect:
    def __init__(self, directions, application, quantity, method, quality):
        self.directions = directions  # List of: NW, N, NE, E, SE, S, SW, W
        self.application = application
        self.quantity = quantity
        self.method = method
        self.quality = quality
