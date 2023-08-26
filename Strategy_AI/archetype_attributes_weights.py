## Miracle battles
## archetype_attributes_weights

random_tag_weights = {"melee infantry": 1,
                      "melee cavalry": 1,
                      "ranged infantry": 1,
                      "caster": 1,
                      "hero": 1}

cavalry_focus_tag_weights = {"melee infantry": 4,
                             "melee cavalry": 10,
                             "ranged infantry": 4,
                             "caster": 2,
                             "hero": 3}

mixed_troops_tag_weights = {"melee infantry": 7,
                            "melee cavalry": 5,
                            "ranged infantry": 7,
                            "caster": 2,
                            "hero": 3}

ranged_troops_tag_weights = {"melee infantry": 4,
                             "melee cavalry": 4,
                             "ranged infantry": 10,
                             "caster": 2,
                             "hero": 3}

balanced_magic_focus_tag_weights = {"melee infantry": 3,
                                    "melee cavalry": 3,
                                    "ranged infantry": 3,
                                    "caster": 5,
                                    "hero": 8}

magic_power_focus_tag_weights = {"melee infantry": 3,
                                 "melee cavalry": 3,
                                 "ranged infantry": 3,
                                 "caster": 5,
                                 "hero": 10}

class_tag_cat = {"Random": random_tag_weights,
                 "Cavalry focus": cavalry_focus_tag_weights,
                 "Mixed troops": mixed_troops_tag_weights,
                 "Ranged troops": ranged_troops_tag_weights,
                 "Balanced magic focus": balanced_magic_focus_tag_weights,
                 "Magic power focus": magic_power_focus_tag_weights}

# ~~~~~~~~~~~~~~#
random_stat_weights = {"melee mastery": 1,
                       "defence": 1,
                       "ranged mastery": 1,
                       "armour": 1,
                       "magic power": 1,
                       "knowledge": 1}

cavalry_focus_stat_weights = {"melee mastery": 5,
                              "defence": 5,
                              "ranged mastery": 5,
                              "armour": 7,
                              "magic power": 5,
                              "knowledge": 5}

mixed_troops_stat_weights = {"melee mastery": 5,
                             "defence": 5,
                             "ranged mastery": 5,
                             "armour": 7,
                             "magic power": 5,
                             "knowledge": 5}

ranged_troops_stat_weights = {"melee mastery": 5,
                              "defence": 5,
                              "ranged mastery": 5,
                              "armour": 7,
                              "magic power": 5,
                              "knowledge": 5}

balanced_magic_focus_stat_weights = {"melee mastery": 5,
                                     "defence": 5,
                                     "ranged mastery": 5,
                                     "armour": 7,
                                     "magic power": 5,
                                     "knowledge": 5}

magic_power_focus_stat_weights = {"melee mastery": 1,
                                  "defence": 1,
                                  "ranged mastery": 1,
                                  "armour": 1,
                                  "magic power": 10,
                                  "knowledge": 3}

class_stat_cat = {"Random": random_stat_weights,
                  "Cavalry focus": cavalry_focus_stat_weights,
                  "Mixed troops": mixed_troops_stat_weights,
                  "Ranged troops": ranged_troops_stat_weights,
                  "Balanced magic focus": balanced_magic_focus_stat_weights,
                  "Magic power focus": magic_power_focus_stat_weights}
