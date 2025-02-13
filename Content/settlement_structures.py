## Among Myth and Wonder
## settlement_structures


class Structure:  # Building in settlement
    def __init__(self, name, title_name, img, construction_cost, construction_time, provided_effects, recruitment,
                 structure_tags, required_buildings, defensive_structure):
        self.name = name
        self.title_name = title_name  # List in case if title happened to be too long
        self.img = img
        self.construction_cost = construction_cost  # List of necessary resources for construction
        self.construction_time = construction_time  # Int number of turns to complete construction
        self.time_passed = 0  # Int number of turn passed so far
        self.provided_effects = provided_effects  # List of building effects that this structure provides when it built
        self.recruitment = recruitment  # Structure's ability to recruit new units
        # Either None or Hire_Unit class object
        self.fulfilled_conditions = True  # Check if tags from required_buildings exist among built structures
        self.structure_tags = structure_tags  # List
        self.required_buildings = required_buildings  # List of additional buildings needed to be present
        self.defensive_structure = defensive_structure


## Dictionaries

# Knight lords  # True - settlement starts with this structure built, False - settlement starts without it
LE_structures_KL = {"Earth rampart": ["Earth rampart", ["Earth rampart"],
                                      'Img/Structure_icons/earth_rampart_icon.png',
                                      [["Florins", 1000], ["Wood", 200]],
                                      1, False,
                                      ["Earth rampart", "Moat requisite"],
                                      [],
                                      "Earth rampart"],
                    "Palisade": ["Palisade", ["Palisade"],
                                 'Img/Structure_icons/palisade_icon.png',
                                 [["Florins", 1200], ["Wood", 800]],
                                 1, False,
                                 ["Earth rampart", "Palisade", "Moat requisite"],
                                 [],
                                 "Palisade"],
                    "KL artifact market": ["KL artifact market", ["Artifact market"],
                                           'Img/Structure_icons/artifact_market_icon.png',
                                           [["Florins", 1000], ["Wood", 200]],
                                           1, False,
                                           ["Artifact market"],
                                           [],
                                           None],
                    "School of magic": ["KL School of magic", ["School of magic"],
                                        'Img/Structure_icons/study_divine_magic_icon.png',
                                        [["Florins", 1500], ["Wood", 500], ["Stone", 300]],
                                        1, False,
                                        ["School of magic"],
                                        [],
                                        None],
                    "Wheelwright guild": ["Wheelwright guild", ["Wheelwright guild"],
                                          'Img/Structure_icons/cart_wheel_icon.png',
                                          [["Florins", 1500], ["Wood", 400]],
                                          1, False,
                                          ["Wheelwright guild"],
                                          [],
                                          None],
                    "Watermill": ["Watermill", ["Watermill"],
                                  'Img/Structure_icons/watermill_icon.png',
                                  [["Florins", 3000], ["Wood", 1000], ["Stone", 1000]],
                                  2, False,
                                  ["Watermill"],
                                  [],
                                  None],
                    "Cathedral": ["Cathedral", ["Cathedral"],
                                  'Img/Structure_icons/dome_icon.png',
                                  [["Florins", 5000], ["Wood", 1500], ["Stone", 2000]],
                                  3, False,
                                  ["Cathedral"],
                                  ["Town convent"],
                                  None],
                    "Town council": ["Town council", ["Town council"],
                                     'Img/Structure_icons/beard_icon.png',
                                     [["Florins", 100]],
                                     1, True,
                                     ["Town council"],
                                     [],
                                     None],
                    "Town hall": ["Town hall", ["Town hall"],
                                  'Img/Structure_icons/bell_icon.png',
                                  [["Florins", 1000], ["Wood", 400], ["Stone", 100]],
                                  1, False,
                                  ["Town council", "Town hall"],
                                  [],
                                  None],
                    "Town armory": ["Town armory", ["Town armory"],
                                    'Img/Structure_icons/scale_armour_icon.png',
                                    [["Florins", 1500], ["Wood", 300]],
                                    1, False,
                                    ["Town armory"],
                                    [],
                                    None],
                    "Blacksmith guild": ["Blacksmith guild", ["Blacksmith guild"],
                                         'Img/Structure_icons/chain_mail_armour_icon.png',
                                         [["Florins", 1000], ["Wood", 600]],
                                         1, False,
                                         ["Town armory", "Blacksmith guild"],
                                         [],
                                         None],
                    "Armour district": ["Armour district", ["Armour district"],
                                        'Img/Structure_icons/plated_armour_icon.png',
                                        [["Florins", 1500], ["Wood", 800]],
                                        1, False,
                                        ["Town armory", "Blacksmith guild", "Armour district"],
                                        [],
                                        None],
                    "Lord's court": ["Lord's court", ["Lord's court"],
                                     'Img/Structure_icons/lords_court_icon.png',
                                     [["Florins", 3000], ["Wood", 1500], ["Stone", 1500]],
                                     2, False,
                                     ["Lord's court"],
                                     ["Blacksmith guild"],
                                     None],
                    "Town convent": ["Town convent", ["Town convent"],
                                     'Img/Structure_icons/prayer_icon.png',
                                     [["Florins", 2500], ["Wood", 800], ["Stone", 600]],
                                     1, False,
                                     ["Town convent"],
                                     [],
                                     None],
                    "Monastery": ["Monastery", ["Monastery"],
                                  'Img/Structure_icons/hood_icon.png',
                                  [["Florins", 3000], ["Wood", 1200], ["Stone", 1000]],
                                  2, False,
                                  ["Town convent", "Monastery"],
                                  ["School of magic"],
                                  None],
                    "Court bestiary": ["Court bestiary", ["Court bestiary"],
                                       'Img/Structure_icons/eagle_head_icon.png',
                                       [["Florins", 2000], ["Wood", 1000], ["Stone", 400]],
                                       1, False,
                                       ["Court bestiary"],
                                       [],
                                       None],
                    "Pegasus stables": ["Pegasus stables", ["Pegasus stables"],
                                        'Img/Structure_icons/pegasus_icon.png',
                                        [["Florins", 2500], ["Wood", 1200], ["Stone", 600]],
                                        1, False,
                                        ["Court bestiary", "Pegasus stables"],
                                        [],
                                        None],
                    "Engineering guild": ["Engineering guild", ["Engineering guild"],
                                          'Img/Structure_icons/gear_icon.png',
                                          [["Florins", 1500], ["Wood", 800]],
                                          1, False,
                                          ["Engineering guild"],
                                          ["Blacksmith guild"],
                                          None]
                    }

# Nature keepers
LE_structures_NK = {}

# Dictionary catalog
structures_groups = {"Knight Lords": LE_structures_KL,
                     "Nature Keepers": LE_structures_NK}

# New upgrades
new_upgrades_KL = {"Earth rampart": "Palisade",
                   "Palisade": None,
                   "KL artifact market": None,
                   "KL School of magic": None,
                   "Wheelwright guild": None,
                   "Watermill": None,
                   "Cathedral": None,
                   "Town council": "Town hall",
                   "Town hall": None,
                   "Town armory": "Blacksmith guild",
                   "Blacksmith guild": "Armour district",
                   "Armour district": None,
                   "Lord's court": None,
                   "Town convent": "Monastery",
                   "Monastery": None,
                   "Court bestiary": "Pegasus stables",
                   "Pegasus stables": None,
                   "Engineering guild": None}

new_upgrades_NK = {}

# Dictionary catalog
new_upgrades_cat = {"Knight Lords": new_upgrades_KL,
                    "Nature Keepers": new_upgrades_NK}
