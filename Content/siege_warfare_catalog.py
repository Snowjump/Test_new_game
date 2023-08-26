## Miracle battles

# List structure:
# [artillery capacity (trebuchets), battlefield machinery capacity (battering rams and siege towers),
# construction points per creature in regiment]
neutrals_units_siege_capacity = {"Simurg's anarchists" : [1, 1, 1],
                                 "Bandit archers" : [1, 0, 1],
                                 "Highway robbers" : [1, 1, 1],
                                 "Robber knights" : [0, 0, 0],
                                 "Grey dragon" : [0, 0, 0],
                                 "Grey drakes" : [0, 0, 0]}

knight_lords_units_siege_capacity = {"Peasant mob" : [1, 1, 1],
                                     "Peasant bowmen" : [1, 0, 1],
                                     "Crossbowmen" : [1, 0, 1],
                                     "Spear footmen" : [1, 1, 1],
                                     "Sword footmen" : [1, 1, 1],
                                     "Squires" : [1, 1, 1],
                                     "Knights" : [0, 0, 0],
                                     "Priests of Salvation" : [1, 0, 1],
                                     "Battle monks" : [1, 0, 1],
                                     "Griffons" : [0, 0, 0],
                                     "Pegasus knights" : [0, 0, 0],
                                     "Field ballistas" : [1, 0, 1]}

nature_keepers_units_siege_capacity = {}

units_siege_dict_by_alignment = {"Neutrals": neutrals_units_siege_capacity,
                                 "Knight Lords": knight_lords_units_siege_capacity,
                                 "Nature Keepers": nature_keepers_units_siege_capacity}

hardness_table = {"Palisade" : 2}

detailed_hardness_table = {"Palisade_gates" : 2}

name_change_after_destruction = {"Palisade_gates" : "Palisade_gates_ruins"}

path_change_after_destruction = {"Palisade_gates_ruins" : "Battle_objects/palisade_gates_destroyed"}

name_change_open_gates = {"Palisade_gates" : "Palisade_gates_opened"}

path_change_open_gates = {"Palisade_gates_opened" : "Battle_objects/palisade_gates_opened"}

position_change_open_gates = {"Palisade_gates_opened" : [-18, -40]}

# Parameters being used in sc_battle
siege_machine_img_width = {"Siege tower" : 29,
                           "Battering ram" : 62}

siege_machine_img_height = {"Siege tower" : 56,
                            "Battering ram" : 22}

siege_machine_img = {"Siege tower" : "img/Creatures/siege_machines/siege_tower",
                     "Battering ram" : "img/Creatures/siege_machines/battering_ram"}
