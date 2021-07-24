## Miracle battles


class Battle_Effect:
    def __init__(self, name, until_next_turn, time_left, buffs):
        self.name = name
        self.until_next_turn = until_next_turn
        self.time_left = time_left
        self.buffs = buffs  # List of buffs and debuffs


class Buff:
    def __init__(self, application, quantity, method, quality):
        self.application = application
        self.quantity = quantity
        self.method = method
        self.quality = quality
