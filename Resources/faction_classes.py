## Miracle battles


class Faction:  # every region is populated by several factions according to its alignment
    def __init__(self, faction_id, name, title_name, base_loyalty):
        self.faction_id = faction_id
        self.name = name
        self.title_name = title_name  # Includes regional location
        self.base_loyalty = base_loyalty  # Innate value of loyalty
        self.members = []  # List [Population IDs that belong to this faction, name of population,
        # TileNum number, object (settlement or facility)]
        self.loyalty = base_loyalty


class Population:  # group of people belonging to any faction
    def __init__(self, population_id, name):
        self.population_id = int(population_id)
        self.name = str(name)
        self.reserve = []  # resources currently owned by this population
        self.surplus = None  # under development
        # records about resources transactions
        self.records_gained = []
        self.records_additional_gains = []  # Resources gained during the turn that just passed due to events and
        # actions of players
        self.records_sold = []
        self.records_bought = []
        self.records_consumed = []
        self.records_turnover = []


## Dictionaries

# Create new faction data
# Faction name, base loyalty
# Knight lords
LE_fac_KL = [["Clergy estate", 4],
             ["Nobility estate", 5],
             ["Peasant estate", 4],
             ["Burgher estate", 4]]

# Nature keepers
LE_fac_NK = ["Free folk"]

# Dictionary catalog

pop_membership = {"Clergy" : "Clergy estate",
                  "Nobles" : "Nobility estate",
                  "Serfs" : "Peasant estate",
                  "Artisans" : "Burgher estate",
                  "Merchants" : "Burgher estate"
                  }

fac_groups = {"Knight Lords": LE_fac_KL,
              "Nature Keepers": LE_fac_NK}

LE_facility_pop_KL = {"Settlement": [["Artisans", [["Wood", 400], ["Metals", 400], ["Florins", 100]]],
                                     ["Merchants", [["Florins", 9000]]]],
                      "Gold deposit": [["Serfs", [["Florins", 250]]],
                                       ["Nobles", [["Florins", 250]]]],
                      "Arable land": [["Serfs", [["Food", 100], ["Florins", 300]]],
                                      ["Nobles", [["Food", 100], ["Florins", 100]]]],
                      "Logging camp": [["Serfs", [["Wood", 200], ["Florins", 100]]],
                                       ["Nobles", []]],
                      "Stone quarry": [["Serfs", [["Stone", 200], ["Florins", 100]]],
                                       ["Nobles", []]],
                      "Metal mine": [["Serfs", [["Metals", 200], ["Florins", 100]]],
                                     ["Nobles", []]],
                      "Magic source": [["Clergy", [["Ingredients", 200], ["Florins", 100]]]]}

LE_facility_pop_NK = {"Arable land": [["Free folk", [["Food", 10], ["Florins", 10]]]]}

fac_groups_for_pop = {"Knight Lords": LE_facility_pop_KL,
                      "Nature Keepers": LE_facility_pop_NK}
