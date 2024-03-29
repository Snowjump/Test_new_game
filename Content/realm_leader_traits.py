## Miracle battles

# Realm leaders possess
# 2 behavior traits (only if they are AI players)
# 2 lifestyle traits

behavior_traits_list = ["Pacifist",
                        "Isolationist",
                        "Aggressor",
                        "Expansionist",
                        "Honorable",
                        "Vindictive",
                        "Betrayer",
                        "Opportunist",
                        "Warmonger",
                        "Underling",
                        "Peacekeeper",
                        "Balance of power",
                        "Domination"]


behavior_traits_incompatibility = {"Pacifist" : ["Aggressor",
                                                 "Warmonger",
                                                 "Expansionist",
                                                 "Domination"],
                                   "Isolationist" : ["Expansionist",
                                                     "Warmonger",
                                                     "Aggressor",
                                                     "Domination"],
                                   "Aggressor" : ["Pacifist",
                                                  "Isolationist",
                                                  "Peacekeeper"],
                                   "Expansionist" : ["Pacifist",
                                                     "Isolationist",
                                                     "Peacekeeper"],
                                   "Honorable" : ["Betrayer"],
                                   "Vindictive" : [],
                                   "Betrayer" : ["Honorable"],
                                   "Opportunist" : [],
                                   "Warmonger" : ["Pacifist",
                                                  "Isolationist",
                                                  "Peacekeeper",
                                                  "Balance of power"],
                                   "Underling" : [],
                                   "Peacekeeper" : ["Aggressor",
                                                    "Warmonger",
                                                    "Expansionist",
                                                    "Domination"],
                                   "Balance of power" : ["Warmonger",
                                                         "Domination"],
                                   "Domination" : ["Pacifist",
                                                   "Isolationist",
                                                   "Peacekeeper",
                                                   "Balance of power"]}


behavior_traits_desc_dict = {"Pacifist" : ["Avoids to start wars, except to return lands",
                                           "Favours alliances and non-aggression pacts"],
                             "Isolationist" : ["Avoids to start wars, except to return lands",
                                               "Highly favours non-aggression pacts",
                                               "Doesn't favours alliances"],
                             "Aggressor" : ["Favours to start and join wars",
                                            "Slightly favours to break diplomatic truces"],
                             "Expansionist" : ["Favours to start wars for new lands"],
                             "Honorable" : ["Highly favours to fulfill  diplomatic agreements",
                                            "Avoids to break diplomatic truces"],
                             "Vindictive" : ["Highly favours to start wars over lost lands"],
                             "Betrayer" : ["Favours to break diplomatic agreements",
                                           "Favours to break diplomatic truces",
                                           "Could start wars against allies"],
                             "Opportunist" : ["Favours alliances with stronger realms",
                                              "Favours to start wars",
                                              "against realms already in wars"],
                             "Warmonger" : ["Always seek to wage war",
                                            "Favours to break diplomatic truces"],
                             "Underling" : ["Highly favours alliances with stronger realms",
                                            "Doesn't favours to start wars",
                                            "against stronger realms"],
                             "Peacekeeper" : ["Detests realms that start wars",
                                              "Favours defensive alliances",
                                              "and non-aggression pacts",
                                              "Doesn't favours military alliances"],
                             "Balance of power" : ["Avoids to start wars,",
                                                   "if already is among leaders by realm size",
                                                   "Favours to start wars against the biggest realms"],
                             "Domination" : ["Detests stronger competitors"]}


behavior_traits_nicknames = {"Pacifist" : ["the Peaceful",
                                           "the Good"],
                             "Isolationist" : ["the Shepherd",
                                               "the Iron Cage",
                                               "the Idle"],
                             "Aggressor" : ["the Conqueror",
                                            "the Bloodaxe",
                                            "the Warrior"],
                             "Expansionist" : ["the Great",
                                               "the Conqueror",
                                               "the Memorable"],
                             "Honorable" : ["the Noble",
                                            "the Good"],
                             "Vindictive" : ["the Quarrelsome",
                                             "the Vengeful"],
                             "Betrayer" : ["the Untrusted",
                                           "the Clipped",
                                           "the Kinslayer",
                                           "the Wormtongue"],
                             "Opportunist" : ["the Sneaky",
                                              "the Jaws",
                                              "the Seeker"],
                             "Warmonger" : ["the Iron",
                                            "the Mad",
                                            "the Scourge"],
                             "Underling" : ["the Meek",
                                            "the Soft",
                                            "the Whetstone",
                                            "the Lamb"],
                             "Peacekeeper" : ["the Protector",
                                              "the Vigilant",
                                              "the Lightbringer"],
                             "Balance of power" : ["the Watcher",
                                                   "the Envious",
                                                   "the All-seeing"],
                             "Domination" : ["the Great",
                                             "the Conqueror",
                                             "the Victorious"]}


neutral_nicknames = ["the Black",
                     "the Fairhair",
                     "the Short",
                     "the Grey",
                     "the Red"]


lifestyle_traits_list = ["Hunter",
                         "Sword champion",
                         "Scholar",
                         "Mystic"]

lifestyle_traits_nicknames = {"Hunter" : ["the Hunter",
                                          "the Fawler"],
                              "Sword champion" : ["the Swordsman",
                                                  "the Champion"],
                              "Scholar": ["the Scholar",
                                          "the Illuminated"],
                              "Mystic": ["the Mystic",
                                         "the Seer",
                                         "the Shrouded"]
                              }
