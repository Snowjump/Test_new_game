## Miracle battles

class army_roles:
    def __init__(self, army_id, army_role, army_size):
        self.army_id = army_id
        ## Army role: (str)
        # Idle - stays still
        # Nothing to do - keep standing still
        # Conquest - looks for nearby enemies, prioritises settlements over armies
        # Advance - enemy army - goes to battle enemy army
        # Advance - enemy settlement - goes to capture unoccupied enemy settlement
        # Advance - liberate settlement - goes to capture occupied own settlement
        # Adventure - explore territory around settlement
        # Exploration - explore territories in neutral lands
        # Travel to settlement - go to closest own settlement
        self.army_role = army_role
        ## Status: (str)
        # Start - at the beginning of round
        # Finished - no movement points left
        self.status = "Start"
        # Int(1): Small - rank 35
        # Int(2): Medium - rank 90
        # Int(3): Large - rank > 144
        self.army_size = army_size
        # Most AI settlements should have a dedicated army that will operate nearby
        self.base_of_operation = 0  # City_id
        self.target_army_id = 0  # 0 is False and means there is no target
        self.target_city_id = 0  # 0 is False and means there is no target


class AI_economy:
    def __init__(self):
        self.new_round = True
        # One turn expected standard income by resource
        self.florins_income = 0
        self.food_income = 0
        self.wood_income = 0
        self.metals_income = 0
        self.stone_income = 0
        self.ingredients_income = 0
        self.armament_income = 0
        self.tools_income = 0
        #~~~#
        self.florins_expenses = 0
        self.food_expenses = 0
        self.wood_expenses = 0
        self.metals_expenses = 0
        self.stone_expenses = 0
        self.ingredients_expenses = 0
        self.armament_expenses = 0
        self.tools_expenses = 0
