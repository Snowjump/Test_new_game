## Among Myth and Wonder
## skill_classes


class Battle_Skill:
    def __init__(self, name, application, quantity, method, quality, skill_tags):
        self.name = name
        self.application = application
        self.quantity = quantity
        self.method = method
        self.quality = quality
        self.skill_tags = skill_tags  # List of tags, should be an empty list [], if none tags are assigned
        self.keep_details = []  # Some skills need to keep track of what happened


class Hero_Skill:
    def __init__(self, name, img, skill_type, next_level, skill_level, theme, tags, prerequisites, effects,
                 screen_position):
        self.name = name
        self.img = img
        self.skill_type = skill_type  # Basic skill or perk (str): Skill; Perk
        self.next_level = next_level
        self.skill_level = skill_level  # (str): Basic; Advanced; Expert; Perk
        self.theme = theme  # Needed for illustration new skills and perks
        self.tags = tags  # List
        self.prerequisites = prerequisites  # List
        self.effects = effects  # List of effects
        self.screen_position = screen_position  # Position on hero's screen


class Skill_Effect:
    def __init__(self, application, quantity, method, quality, skill_tags, other_tags):
        self.application = application
        self.quantity = quantity
        self.method = method
        self.quality = quality
        self.skill_tags = skill_tags
        self.other_tags = other_tags
