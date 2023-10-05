## Miracle battles
## quest_logic

import random

from Strategy_AI import AI_dilemma_options
from Strategy_AI import AI_quest_options


# class Dilemma_Option:
#     def __init__(self, name):
#         self.name = name


def manage_messages(realm):
    # print("")
    # print(realm.name + " - manage_messages()")
    for message in realm.quests_messages:
        if message.message_type == "Dilemma":
            options_list, weights_list = AI_dilemma_options.options_dict[message.name](realm)
            if len(options_list) > 0:
                print("len(dilemma options_list) = " + str(len(options_list)))
            random.choices(options_list, weights=weights_list)[0](realm, message)

            # collect_options(realm, message)

        elif message.message_type == "Quest":
            if message.name in AI_quest_options.options_dict:
                options_list, weights_list = AI_quest_options.options_dict[message.name](realm)
                if len(options_list) > 0:
                    print("len(quest options_list) = " + str(len(options_list)))
                random.choices(options_list, weights=weights_list)[0](realm, message)

    # print("")


# def collect_options(realm, message):
#     options_list, weights_list = AI_dilemma_options.options_dict[message.name](realm)
#     random.choices(options_list, weights=weights_list)[0](realm, message)
