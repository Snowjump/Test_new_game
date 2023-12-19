## Among Myth and Wonder

# Scripts to govern how population consume goods to fulfill their basic needs
# BN - stands for basic needs

def consumption(pops, goods):
    if len(pops.reserve) > 0:
        for product in goods:
            no_product = True

            for resource in pops.reserve:

                if product[0] == resource[0]:
                    # Found product in population reserves
                    # print("Available product " + str(resource))
                    consumed_all = False
                    no_product = False
                    amount_to_record = 0
                    if product[1] > resource[1]:
                        consumed_all = True
                        amount_to_record = -1 * int(resource[1])
                    elif product[1] == resource[1]:
                        consumed_all = True
                        amount_to_record = -1 * int(product[1])
                    else:
                        resource[1] -= int(product[1])
                        amount_to_record = -1 * int(product[1])

                    if consumed_all:
                        pops.reserve.remove(resource)

                    # Record consumption
                    no_record = True
                    for record in pops.records_consumed:
                        if product[0] == record[0]:
                            no_record = False
                            record[1] += int(amount_to_record)

                    if no_record:
                        pops.records_consumed.append([str(product[0]), int(amount_to_record)])


# Production methods
def nobles_BN_gold_deposit(pops):
    pass


def nobles_BN_arable_land(pops):
    pass


def nobles_BN_logging_camp(pops):
    pass


def nobles_BN_stone_quarry(pops):
    pass


def nobles_BN_metal_mine(pops):
    pass


def serfs_BN_gold_deposit(BN_pops):
    consumption(BN_pops, [["Food", 100]])


def serfs_BN_arable_land(BN_pops):
    pass


def serfs_BN_logging_camp(BN_pops):
    consumption(BN_pops, [["Food", 100]])


def serfs_BN_stone_quarry(BN_pops):
    consumption(BN_pops, [["Food", 100]])


def serfs_BN_metal_mine(BN_pops):
    consumption(BN_pops, [["Food", 100]])


def clergy_BN_abbey(BN_pops):
    pass
    # Old
    # consumption(BN_pops, [["Food", 100]])


def artisans_BN_settlement(BN_pops):
    consumption(BN_pops, [["Food", 200]])


def merchants_BN_settlement(BN_pops):
    pass


# Dictionary catalogs
nobles_BN_cat = {"Gold deposit" : nobles_BN_gold_deposit,
                 "Arable land" : nobles_BN_arable_land,
                 "Logging camp" : nobles_BN_logging_camp,
                 "Stone quarry" : nobles_BN_stone_quarry,
                 "Metal mine" : nobles_BN_metal_mine}

serfs_BN_cat = {"Gold deposit" : serfs_BN_gold_deposit,
                "Arable land" : serfs_BN_arable_land,
                "Logging camp" : serfs_BN_logging_camp,
                "Stone quarry" : serfs_BN_stone_quarry,
                "Metal mine" : serfs_BN_metal_mine}

artisans_BN_cat = {"Settlement" : artisans_BN_settlement}

merchants_BN_cat = {"Settlement" : merchants_BN_settlement}

clergy_BN_cat = {"Magic source" : clergy_BN_abbey}

pops_to_facility_cat = {"Serfs" : serfs_BN_cat,
                        "Nobles" : nobles_BN_cat,
                        "Artisans" : artisans_BN_cat,
                        "Merchants" : merchants_BN_cat,
                        "Clergy" : clergy_BN_cat}
