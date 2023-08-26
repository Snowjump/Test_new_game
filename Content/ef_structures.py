## Miracle battles

from Resources import campaign_effect_classes

## Dictionaries

# Population bonuses
pop_bonus = {"Watermill_production" : campaign_effect_classes.Population_Effect("Artisans",
                                                                                "Production",
                                                                                [["Armament", 200],
                                                                                 ["Tools", 200]],
                                                                                "Addition"),
             "Watermill_tax" : campaign_effect_classes.Population_Effect("Artisans",
                                                                         "Tax",
                                                                         [["Armament", 200]],
                                                                         "Addition")}


# Control bonuses
control_bonus = {"Knight_lords_control_1" : campaign_effect_classes.Control_Effect("Knight Lords",
                                                                                   "Control",
                                                                                   1,
                                                                                   "Addition")}


# Knight lords
fill_ef_KL = {"Earth rampart" : [],
              "Palisade" : [],
              "Watermill" : [campaign_effect_classes.Building_Effect("Watermill industry",
                                                                     "Settlement",
                                                                     "Population",
                                                                     [pop_bonus["Watermill_production"],
                                                                      pop_bonus["Watermill_tax"]])],
              "Cathedral" : [campaign_effect_classes.Building_Effect("Cathedral influence",
                                                                     "Settlement",
                                                                     "Control",
                                                                     [control_bonus["Knight_lords_control_1"]])],
              "KL artifact market" : [],
              "School of magic" : [],
              "Town council" : [],
              "Town armory" : [],
              "Blacksmith guild" : [],
              "Armour district" : [],
              "Lord's court" : [],
              "Town convent" : [],
              "Monastery" : [],
              "Court bestiary" : [],
              "Pegasus stables" : [],
              "Engineering guild" : []}

# Nature keepers
fill_ef_NK = {}

# Dictionary catalog
ef_structures_cat = {"Knight Lords": fill_ef_KL,
                     "Nature Keepers": fill_ef_NK}
