## Among Myth and Wonder

# Set of scripts to define how population buy products from the inner market

import math


def local_sales(sales_pops, settlement):
    # List of products and corresponding prices that merchants put on sale on the inner market
    # print("")
    # print("local_sales()")
    global prices
    settlement.inner_market = []
    # print("pops.reserve - " + str(sales_pops.reserve))
    for product in sales_pops.reserve:
        if product[0] != "Florins":
            # [Pop id, product name, quantity for sale, price]
            settlement.inner_market.append([int(sales_pops.population_id), str(product[0]),
                                            int(product[1]), float(prices[product[0]])])

    print("local_sales() - settlement.inner_market - " + str(settlement.inner_market))


def put_orders_to_buy(pops, basket, settlement):
    means = 0
    funds = 0
    for resources in pops.reserve:
        if resources[0] == "Florins":
            means = int(resources[1])

    # print("starting means: " + str(means))

    # First priority are consumption needs
    expected_expanses = 0
    short_list = []
    for needs in basket:
        if needs[2] == "Consumption need":
            for product in settlement.inner_market:
                if product[1] == needs[0]:
                    # if means - funds > int(math.ceil(needs[1] * product[3])):
                    expected_expanses += int(math.ceil(needs[1] * product[3]))
                    # [product name, quantity to buy, price, total expanses]
                    short_list.append([str(product[1]), int(needs[1]),
                                       float(product[3]), int(math.ceil(needs[1] * product[3]))])

    if expected_expanses > means:
        if means > 0:
            overcost_ratio = expected_expanses/means
            for needs in short_list:
                needs[1] = int(math.floor(needs[1]/overcost_ratio))

                # [Pop id, product name, quantity to buy, price, total expanses]
                settlement.market_demand.append([int(pops.population_id), str(needs[0]), int(needs[1]),
                                                 float(needs[2]), int(math.ceil(needs[1] * needs[2]))])

                means -= int(math.ceil(needs[1] * needs[2]))
    else:
        for needs in short_list:
            # [Pop id, product name, quantity to buy, price, total expanses]
            settlement.market_demand.append([int(pops.population_id), str(needs[0]), int(needs[1]),
                                             float(needs[2]), int(math.ceil(needs[1] * needs[2]))])

            means -= int(math.ceil(needs[1] * needs[2]))

    # print("1) market_demand: " + str(settlement.market_demand) + " means: " + str(means))

    # Second priority are production needs
    expected_expanses = 0
    short_list = []
    for needs in basket:
        if needs[2] == "Production need":
            for product in settlement.inner_market:
                if product[1] == needs[0]:
                    expected_expanses += int(math.ceil(needs[1] * product[3]))
                    # [product name, quantity to buy, price, total expanses]
                    short_list.append([str(product[1]), int(needs[1]),
                                       float(product[3]), int(math.ceil(needs[1] * product[3]))])

    if expected_expanses > means:
        if means > 0:
            overcost_ratio = expected_expanses / means
            for needs in short_list:
                needs[1] = int(math.floor(needs[1] / overcost_ratio))
                # print(str("Need - " + needs[0]) + " - " + str(needs[1]))

                if needs[1] > 0:  # To avoid empty records
                    # [Pop id, product name, quantity to buy, price, total expanses]
                    settlement.market_demand.append([int(pops.population_id), str(needs[0]), int(needs[1]),
                                                     float(needs[2]), int(math.ceil(needs[1] * needs[2]))])

                    means -= int(math.ceil(needs[1] * needs[2]))
    else:
        for needs in short_list:
            # [Pop id, product name, quantity to buy, price, total expanses]
            settlement.market_demand.append([int(pops.population_id), str(needs[0]), int(needs[1]),
                                             float(needs[2]), int(math.ceil(needs[1] * needs[2]))])

            means -= int(math.ceil(needs[1] * needs[2]))

    # print("2) market_demand: " + str(settlement.market_demand) + " means: " + str(means))


def adjust_orders(settlement):
    # print("")
    # print("adjust_orders()")
    # print("str(len(settlement.market_demand)) - " + str(len(settlement.market_demand)))
    # print("settlement.market_demand: " + str(settlement.market_demand))

    for product in settlement.inner_market:
        # print("Product from settlement.inner_market - " + str(product))
        orders_qty = 0
        # while len(settlement.market_demand) > 0:
        for order in settlement.market_demand:
            # order = settlement.market_demand[0]
            # print("order - " + str(order))

            # for product in settlement.inner_market:
            if product[1] == order[1]:
                # print("appropriate order - " + str(order))
                orders_qty += int(order[2])

            # settlement.market_demand.remove(order)
            # print("settlement.market_demand: " + str(settlement.market_demand))

        qty_ratio = 1.0
        if orders_qty > product[2]:
            # decrease quantity of product in buying orders of population
            # therefore all product sales will be spread more evenly between all population
            qty_ratio = int(orders_qty)/int(product[2])

        for order in settlement.market_demand:
            if product[1] == order[1]:
                order[2] = int(math.floor(order[2] / qty_ratio))
                # print("order - " + str(order))

    # print("")
    # print("final settlement.market_demand: " + str(settlement.market_demand))


def fulfill_orders(pops, settlement, trader, realm_treasury):
    # print("")
    # print("fulfill_orders()")
    for order in settlement.market_demand:
        if order[0] == pops.population_id:
            tax_sum = math.ceil(int(order[4]) * 0.02)
            money_transfer = int(order[4]) - tax_sum
            turnover_tax(tax_sum, realm_treasury, settlement)

            print("Before: pops.reserve - " + str(pops.reserve))
            # print("order[1] - " + str(order[1]) + " for " + str(money_transfer) + " florins")
            print(str(order[2]) + " " + str(order[1]) + " for " + str(money_transfer) + " florins")

            # Buyer
            no_resources = True
            ended_money = False
            for product in pops.reserve:

                # Transfer resources
                if product[0] == order[1]:
                    # print("product[0] - " + str(product[0]))
                    no_resources = False
                    product[1] += int(order[2])
                    print(str(product[0]) + " - " + str(product[1]))
                    pops.records_bought.append([str(order[1]), int(order[2])])
                # Deduct money
                elif product[0] == "Florins":
                    # print("product[0] - " + str(product[0]))
                    product[1] -= money_transfer
                    print(str(product[0]) + " - " + str(product[1]))
                    if product[1] == 0:
                        ended_money = True

            if no_resources:
                pops.reserve.append([str(order[1]), int(order[2])])
                pops.records_bought.append([str(order[1]), int(order[2])])

            if ended_money:
                for product in pops.reserve:
                    if product[0] == "Florins":
                        pops.reserve.remove(product)

            # print("After: pops.reserve - " + str(pops.reserve))

            # Seller
            ended_resources = False
            no_money = True
            for product in trader.reserve:
                # Take away resources
                if product[0] == order[1]:
                    product[1] -= int(order[2])
                    if product[1] == 0:
                        ended_resources = True
                # Pay money to seller
                elif product[0] == "Florins":
                    no_money = False
                    product[1] += money_transfer

            if ended_resources:
                for product in trader.reserve:
                    if product[0] == order[1]:
                        trader.reserve.remove(product)

            if no_money:
                trader.reserve.append(["Florins", int(money_transfer)])

            # print("seller.reserve - " + str(trader.reserve))

            no_money_record = True
            # print(str(trader.records_bought))
            if len(trader.records_bought) == 0:
                trader.records_bought.append(["Florins", int(money_transfer)])
                no_money_record = False
            else:
                for product1 in trader.records_bought:
                    if product1[0] == "Florins":
                        no_money_record = False
                        product1[1] += int(money_transfer)
                        break
            if no_money_record:
                trader.records_bought.append(["Florins", int(money_transfer)])

            # Records about sold products by trader
            no_product_record = True
            for product1 in trader.records_bought:
                if product1[0] == order[1]:
                    no_product_record = False
                    product1[1] -= int(order[2])
                    break

            if no_product_record:
                trader.records_bought.append([str(order[1]), -1 * int(order[2])])


def turnover_tax(tax_sum, realm_treasury, settlement):
    settlement.records_turnover_tax += int(tax_sum)
    # print("buy_resources - turnover tax: " + str(settlement.records_turnover_tax))
    # Pay taxes on trade to realm
    if len(realm_treasury) > 0:
        no_money = True
        for res in realm_treasury:
            if res[0] == "Florins":
                res[1] += int(tax_sum)
                # print("Florins in treasury: " + str(res[1]))
                no_money = False
                break

        if no_money:
            realm_treasury.append(["Florins", int(tax_sum)])
            # print("Florins in treasury: " + str(tax_sum))


# Selling methods
def nobles_buy_resources_gold_deposit(buying_pops, settlement, for_order):
    if for_order:
        pass
    else:
        return []


def nobles_buy_resources_arable_land(buying_pops, settlement, for_order):
    if for_order:
        pass
    else:
        return []


def nobles_buy_resources_logging_camp(buying_pops, settlement, for_order):
    if for_order:
        pass
    else:
        return []


def nobles_buy_resources_stone_quarry(buying_pops, settlement, for_order):
    if for_order:
        pass
    else:
        return []


def nobles_buy_resources_metal_mine(buying_pops, settlement, for_order):
    if for_order:
        pass
    else:
        return []


def serfs_buy_resources_gold_deposit(buying_pops, settlement, for_order):
    if for_order:
        put_orders_to_buy(buying_pops, [["Tools", 100, "Production need"]], settlement)
    else:
        return [["Tools", 100, "Production need"]]


def serfs_buy_resources_arable_land(buying_pops, settlement, for_order):
    # print("serfs_buy_resources_arable_land")
    if for_order:
        put_orders_to_buy(buying_pops, [["Tools", 100, "Production need"]], settlement)
    else:
        return [["Tools", 100, "Production need"]]


def serfs_buy_resources_logging_camp(buying_pops, settlement, for_order):
    if for_order:
        put_orders_to_buy(buying_pops, [["Food", 100, "Consumption need"], ["Tools", 100, "Production need"]], settlement)
    else:
        return [["Food", 100, "Consumption need"], ["Tools", 100, "Production need"]]


def serfs_buy_resources_stone_quarry(buying_pops, settlement, for_order):
    if for_order:
        put_orders_to_buy(buying_pops, [["Food", 100, "Consumption need"], ["Tools", 100, "Production need"]], settlement)
    else:
        return [["Food", 100, "Consumption need"], ["Tools", 100, "Production need"]]


def serfs_buy_resources_metal_mine(buying_pops, settlement, for_order):
    if for_order:
        put_orders_to_buy(buying_pops, [["Food", 100, "Consumption need"], ["Tools", 100, "Production need"]], settlement)
    else:
        return [["Food", 100, "Consumption need"], ["Tools", 100, "Production need"]]


def clergy_buy_resources_abbey(buying_pops, settlement, for_order):
    if for_order:
        pass
    else:
        return []

    # Old
    # if for_order:
    #     put_orders_to_buy(buying_pops, [["Food", 100, "Consumption need"]], settlement)
    # else:
    #     return [["Food", 100, "Consumption need"]]


def artisans_buy_resources_settlement(buying_pops, settlement, for_order):
    if for_order:
        put_orders_to_buy(buying_pops, [["Food", 200, "Consumption need"], ["Metals", 400, "Production need"],
                          ["Wood", 400, "Production need"]], settlement)
    else:
        # print(buying_pops.name)
        return [["Food", 200, "Consumption need"], ["Metals", 400, "Production need"],
                ["Wood", 400, "Production need"]]


def merchants_buy_resources_settlement(buying_pops, settlement, for_order):
    if for_order:
        pass
    else:
        return []


# Putting to sale resources that were bought from population during previous stage of trading
def artisans_sale(sales_pops, settlement):
    pass


def merchants_sale(sales_pops, settlement):
    # Merchants selling resources in the inner market for Knight Lords
    local_sales(sales_pops, settlement)


# Dictionary catalogs

nobles_buy_resources_cat = {"Gold deposit" : nobles_buy_resources_gold_deposit,
                            "Arable land" : nobles_buy_resources_arable_land,
                            "Logging camp" : nobles_buy_resources_logging_camp,
                            "Stone quarry" : nobles_buy_resources_stone_quarry,
                            "Metal mine" : nobles_buy_resources_metal_mine}

serfs_buy_resources_cat = {"Gold deposit" : serfs_buy_resources_gold_deposit,
                           "Arable land" : serfs_buy_resources_arable_land,
                           "Logging camp" : serfs_buy_resources_logging_camp,
                           "Stone quarry" : serfs_buy_resources_stone_quarry,
                           "Metal mine" : serfs_buy_resources_metal_mine}

artisans_buy_resources_cat = {"Settlement" : artisans_buy_resources_settlement}

merchants_buy_resources_cat = {"Settlement" : merchants_buy_resources_settlement}

clergy_buy_resources_cat = {"Magic source" : clergy_buy_resources_abbey}

pops_to_facility_cat = {"Serfs" : serfs_buy_resources_cat,
                        "Nobles" : nobles_buy_resources_cat,
                        "Artisans" : artisans_buy_resources_cat,
                        "Merchants" : merchants_buy_resources_cat,
                        "Clergy" : clergy_buy_resources_cat}

# Put to sale
pops_sales_cat = {"Artisans" : artisans_sale,
                  "Merchants" : merchants_sale}

prices = {"Food" : 1.2,
          "Wood" : 1.2,
          "Metals" : 1.2,
          "Stone" : 1.2,
          "Armament" : 1.5,
          "Tools" : 1.5,
          "Ingredients" : 1.2}
