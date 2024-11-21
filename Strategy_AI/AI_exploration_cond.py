## Among Myth and Wonder
## AI_exploration_cond

# Some exploration objects requires to met specific conditions to make sense for hero to visit this place

def stone_well_conditions(army):
    # print("stone_well_conditions()")
    passed_verification = False
    if army.hero is not None:
        if army.hero.mana_reserve < army.hero.max_mana_reserve - 3:
            passed_verification = True
            print("Hero's mana reserve: " + str(army.hero.mana_reserve) + "/" + str(army.hero.max_mana_reserve))
            print("Knowledge: " + str(army.hero.knowledge))

    print("passed_verification = " + str(passed_verification))
    return passed_verification


event_conditions = {  # Bonus
    "Stone well": stone_well_conditions}
