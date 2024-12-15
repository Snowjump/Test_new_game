## Among Myth and Wonder
## settlement_defences

from Resources import game_stats


class Defensive_Structures():  # Siege defences
    def __init__(self, name, def_objects, provide_wall):
        self.name = name
        self.def_objects = def_objects
        self.provide_wall = provide_wall


class Defensive_Object():
    def __init__(self, section_name, section_type, state):
        self.section_name = section_name
        self.section_type = section_type  # Barrier, Wall, Gate, Tower
        self.state = state  # Indestructible, Unbroken, Broken, Opened


def construct_earth_rampart(settlement):
    def_objects = []
    for y in range(1, game_stats.battle_height + 1):
        def_objects.append(Defensive_Object("Earth rampart", "Barrier", "Indestructible"))
    settlement.defences.append(Defensive_Structures("Earth rampart",
                                                    def_objects,
                                                    False))


def construct_palisade(settlement):
    def_objects = []
    for y in range(1, int(game_stats.battle_height / 2)):
        def_objects.append(Defensive_Object("Palisade wall section", "Wall", "Unbroken"))
        print(str(y))

    def_objects.append(Defensive_Object("Palisade gate", "Gate", "Unbroken"))

    for y in range(int(game_stats.battle_height / 2 + 1), game_stats.battle_height + 1):
        def_objects.append(Defensive_Object("Palisade wall section", "Wall", "Unbroken"))
        print(str(y))

    print(str(len(def_objects)) + " objects")

    settlement.defences.append(Defensive_Structures("Palisade",
                                                    def_objects,
                                                    True))

    for def_structure in settlement.defences:
        if def_structure.name == "Earth rampart":
            settlement.defences.remove(def_structure)
            break


defence_scripts = {"Earth rampart" : construct_earth_rampart,
                   "Palisade" : construct_palisade}
