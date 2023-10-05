## Miracle battles
## AI_quest_options

from Resources import game_obj


def remove_quest_message(realm, message):
    for quest_message in realm.quests_messages:
        if quest_message.name == message.name:
            realm.quests_messages.remove(quest_message)
            break

    print(realm.name + ": len(realm.quests_messages) - " + str(len(realm.quests_messages)))


def AI_provide_stone_to_vassal(realm, message):
    print(message.name)

    the_settlement = None
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_obj.game_map[message.settlement_location].city_id:
            the_settlement = settlement
            # print(the_settlement.name)
            break

    enough_resources = False
    for res in realm.coffers:
        if res[0] == "Stone":
            if res[1] >= 1600:
                res[1] -= 1600
                enough_resources = True
            break

    if enough_resources:
        for effect in the_settlement.local_effects:
            if effect.name == "Vassal awaits for stone":
                the_settlement.local_effects.remove(effect)
                break

        for faction in the_settlement.factions:
            if faction.name == "Nobility estate":
                faction.loyalty += 1
                break

        remove_quest_message(realm, message)


## Options
def provide_stone_to_vassal_options(realm):
    options_list = [AI_provide_stone_to_vassal]
    weights_list = [10]
    return options_list, weights_list


options_dict = {"Provide stone to vassal" : provide_stone_to_vassal_options}
