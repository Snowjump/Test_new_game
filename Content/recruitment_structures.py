## Miracle battles

class Hire_Unit:
    def __init__(self, unit_name, hiring_capacity, ready_units, replenishment_rate):
        self.unit_name = unit_name
        self.hiring_capacity = hiring_capacity
        self.ready_units = ready_units
        self.replenishment_rate = replenishment_rate
        self.time_passed = 0


def prepare_recruitment(unit_list):
    recruitment_list = []
    for lodger in unit_list:
        recruitment_list.append(Hire_Unit(str(lodger[0]),
                                          int(lodger[1]),
                                          int(lodger[2]),
                                          int(lodger[3])))

    return recruitment_list

## Dictionaries


# Knight lords
# [unit_name, hiring_capacity, ready_units, replenishment_rate]
LE_structures_KL = {"Earth rampart" : [],
                    "Palisade" : [],
                    "KL artifact market" : [],
                    "School of magic": [],
                    "Watermill" : [],
                    "Cathedral" : [],
                    "Town council": [["Peasant mob", 2, 1, 1],
                                     ["Peasant bowmen", 2, 1, 1]],
                    "Town hall": [["Peasant mob", 3, 1, 1],
                                  ["Peasant bowmen", 3, 1, 1]],
                    "Town armory" : [["Crossbowmen", 2, 1, 1], ["Spear footmen", 2, 1, 1]],
                    "Blacksmith guild" : [["Crossbowmen", 3, 1, 1], ["Spear footmen", 3, 1, 1],
                                          ["Sword footmen", 2, 1, 1]],
                    "Armour district" : [["Crossbowmen", 3, 1, 1], ["Spear footmen", 3, 1, 1],
                                         ["Sword footmen", 3, 1, 1], ["Squires", 2, 1, 1]],
                    "Lord's court" : [["Knights", 2, 1, 2]],
                    "Town convent" : [["Priests of Salvation", 2, 1, 1]],
                    "Monastery" : [["Priests of Salvation", 3, 1, 1], ["Battle monks", 2, 1, 2]],
                    "Court bestiary" : [["Griffons", 2, 1, 1]],
                    "Pegasus stables" : [["Griffons", 3, 1, 1], ["Pegasus knights", 2, 1, 2]],
                    "Engineering guild" : [["Field ballistas", 2, 1, 2]]
                    }

# Nature keepers
LE_structures_NK = {}


unit_tags = {"Peasant mob" : ["Peasant mob", "melee", "melee infantry", "peasant"],
             "Peasant bowmen" : ["Peasant bowmen", "ranged", "ranged infantry", "peasant"],
             "Crossbowmen" : ["Crossbowmen", "ranged", "ranged infantry", "men-at-arms"],
             "Spear footmen" : ["Spear footmen", "melee", "melee infantry", "men-at-arms"],
             "Sword footmen" : ["Sword footmen", "melee", "melee infantry", "men-at-arms"],
             "Squires" : ["Squires", "melee", "melee infantry", "men-at-arms"],
             "Knights" : ["Knights", "melee", "melee cavalry"],
             "Priests of Salvation" : ["Priests of Salvation", "caster"],
             "Battle monks" : ["Battle monks", "hybrid", "hybrid infantry"],
             "Griffons" : ["Griffons", "melee", "monster"],
             "Pegasus knights" : ["Pegasus knights", "melee", "melee cavalry"],
             "Field ballistas" : ["Field ballistas", "ranged", "machines"]}


# Dictionary catalog
structures_groups = {"Knight Lords": LE_structures_KL,
                     "Nature Keepers": LE_structures_NK}
