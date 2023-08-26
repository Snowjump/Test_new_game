## Miracle battles

import random

from Resources import game_stats


def runaway_serfs_refuge_reward(army):
    prize = [int(game_stats.reward_id_counter), []]
    prize_item1 = ["Food", 750]
    prize_item2 = ["Wood", 500]
    prize_item1 = adjust_prize(prize_item1, army.hero)
    prize_item2 = adjust_prize(prize_item2, army.hero)
    prize[1].append(prize_item1)
    prize[1].append(prize_item2)

    return prize


def treasure_tower_reward(army):
    prize = [int(game_stats.reward_id_counter), []]
    prize_item1 = ["Florins", 1200]
    prize_item1 = adjust_prize(prize_item1, army.hero)
    prize[1].append(prize_item1)
    # "Champion's lance", "Priest's old hat", "Lucky coin purse", "Sword of haste"
    prize[1].append([random.choice(["Champion's lance", "Priest's old hat", "Lucky coin purse", "Sword of haste"])])

    return prize


def lair_of_grey_dragons_reward(army):
    prize = [int(game_stats.reward_id_counter), []]
    prize[1].append(["Regiment", "Grey drakes", "Neutrals"])

    # prize[1].append(["Regiment", "Bandit archers", "Neutrals"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Grey dragon", "Neutrals"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    #
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Grey dragon", "Neutrals"])
    # prize[1].append(["Regiment", "Grey dragon", "Neutrals"])
    #
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Grey dragon", "Neutrals"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    #
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Grey dragon", "Neutrals"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])
    # prize[1].append(["Regiment", "Knights", "Knight Lords"])

    return prize


def adjust_prize(item, hero):
    bonus_quantity = 0
    # Check artifacts
    if len(hero.inventory) > 0:
        for artifact in hero.inventory:
            for effect in artifact.effects:
                if effect.application == "Resources bonus":
                    if item[0] in effect.application_tags:
                        if effect.method == "addition":
                            bonus_quantity += int(effect.quantity)

    return [str(item[0]), int(item[1] + bonus_quantity)]


reward_scripts = {"Runaway serfs refuge reward" : runaway_serfs_refuge_reward,
                  "Treasure tower reward": treasure_tower_reward,
                  "Lair of grey dragons reward": lair_of_grey_dragons_reward}
