## Among Myth and Wonder
## ability_classes


class Hero_Ability:
    def __init__(self, name, img, img_source, school, action, ai_tags, target, mana_cost, anim_effect):
        self.name = name
        self.img = img
        self.img_source = img_source
        self.school = school  # Ability school
        self.action = action  # List
        self.ai_tags = ai_tags  # Helps Ai choose between abilities
        # Targets: single_ally, single_enemy, all_units, all_own_units, all_enemy_units,
        # area_ally, area_enemy
        self.target = target
        self.mana_cost = mana_cost
        self.anim_effect = anim_effect


class Ability_Action:
    def __init__(self, application, quantity, method, quality, ability_tags, script):
        self.application = application
        self.quantity = quantity  # Calculation function from catalog, returns list with information
        self.method = method
        self.quality = quality
        self.ability_tags = ability_tags
        self.script = script  # Name of script from abilities catalog


