## Miracle battles

class Building_Effect:
    def __init__(self, name, scale_type, ef_type, content):
        self.name = name
        self.scale_type = scale_type  # Settlement - active in settlement, Local - active in region, Realm - active in
        # realm, Global - active for whole game
        self.ef_type = ef_type  # Effect type: Population, Control, Loyalty, New heroes
        self.content = content  # Base effect list


class Settlement_Effect:
    def __init__(self, name, scale_type, ef_type, content, duration):
        self.name = name
        self.scale_type = scale_type  # Settlement - active in settlement, Local - active in region, Realm - active in
        # realm, Global - active for whole game
        self.ef_type = ef_type  # Effect type: Population, Control, Loyalty, Replenishment
        self.content = content  # Base effect list
        self.duration = duration  # Either int number of turns or True (meaning indefinitely)


class Population_Effect:
    def __init__(self, pops, application, bonus, operator):
        self.pops = pops  # Name of population
        self.application = application  # Production, tax
        self.bonus = bonus  # For production and tax its increase or decrease in quantity of goods (list)
        self.operator = operator  # addition, -, *, /


class Control_Effect:
    def __init__(self, realm_type, application, bonus, operator):
        self.realm_type = realm_type
        self.application = application  # Control
        self.bonus = bonus  # Int
        self.operator = operator  # addition, -, *, /


class Faction_Effect:
    def __init__(self, faction, application, bonus, operator):
        self.faction = faction  # Name of faction
        self.application = application  # Loyalty
        self.bonus = bonus  # Int
        self.operator = operator  # addition, -, *, /


class Recruitment_Effect:
    def __init__(self, tags, application, bonus, operator):
        self.tags = tags  # list of tags
        self.application = application  # "Replenishment and ready"
        self.bonus = bonus  # Int
        self.operator = operator  # Banned, Subtraction, Addition, *, /


class New_Heroes_Effect:
    def __init__(self, hero_classes, application, bonus, operator):
        self.hero_classes = hero_classes  # list of classes or "all"
        self.application = application  # Level
        self.bonus = bonus  # Int
        self.operator = operator  # Addition, -, *, /
