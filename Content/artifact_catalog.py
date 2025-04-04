## Among Myth and Wonder
## artifact_catalog

from Resources import artifact_classes

artifact_data = {"Champion's lance": ["Champion's lance", 'img/Artifacts/champion_lance.png',
                                      800, [],
                                      [artifact_classes.Artifact_Effect("Bonus speed",
                                                                        1,
                                                                        "addition",
                                                                        None,
                                                                        [],
                                                                        ["melee cavalry", "ranged cavalry"])]],
                 "Priest's old hat": ["Priest's old hat", 'img/Artifacts/priest_old_hat.png',
                                      1000, [],
                                      [artifact_classes.Artifact_Effect("Knowledge",
                                                                        1,
                                                                        "addition",
                                                                        None,
                                                                        [],
                                                                        [])]],
                 "Lucky coin purse": ["Lucky coin purse", 'img/Artifacts/lucky_coin_purse.png',
                                      800, [],
                                      [artifact_classes.Artifact_Effect("Resources bonus",
                                                                        200,
                                                                        "addition",
                                                                        None,
                                                                        ["Florins"],
                                                                        [])]],
                 "Sword of haste": ["Sword of haste", 'img/Artifacts/sword_of_haste.png',
                                    800, [],
                                    [artifact_classes.Artifact_Effect("Cast spells",
                                                                      None,
                                                                      None,
                                                                      None,
                                                                      ["Haste"],
                                                                      ["Divine magic"])]],
                 "Bronze spurs": ["Bronze spurs", 'img/Artifacts/bronze_spurs.png',
                                  1200, [],
                                  [artifact_classes.Artifact_Effect("Movement points",
                                                                    150,
                                                                    "addition",
                                                                    None,
                                                                    [],
                                                                    [])]],
                 "Page's chainmail": ["Page's chainmail", 'img/Artifacts/pages_chainmail.png',
                                      2000, [],
                                      [artifact_classes.Artifact_Effect("Armour",
                                                                        2,
                                                                        "addition",
                                                                        None,
                                                                        [],
                                                                        ["ranged infantry"])]],
                 "Wooden chalice": ["Wooden chalice", 'img/Artifacts/wooden_chalice.png',
                                    800, [],
                                    [artifact_classes.Artifact_Effect("Ability bonus Magic Power",
                                                                      3,
                                                                      "addition",
                                                                      None,
                                                                      [],
                                                                      ["Healing"]),
                                     artifact_classes.Artifact_Effect("Ability mana cost",
                                                                      1,
                                                                      "subtraction",
                                                                      None,
                                                                      [],
                                                                      ["Healing"])
                                     ]],
                 "Medal of honor": ["Medal of honor", 'img/Artifacts/medal_of_honor.png',
                                    2000, [],
                                    [artifact_classes.Artifact_Effect("Bonus leadership",
                                                                      1,
                                                                      "addition",
                                                                      None,
                                                                      [],
                                                                      [])]],
                 "Red sceptre": ["Red sceptre", 'img/Artifacts/red_sceptre.png',
                                 800, [],
                                 [artifact_classes.Artifact_Effect("Ability bonus Magic Power",
                                                                   3,
                                                                   "addition",
                                                                   None,
                                                                   [],
                                                                   ["Bless"]),
                                  artifact_classes.Artifact_Effect("Ability mana cost",
                                                                   1,
                                                                   "subtraction",
                                                                   None,
                                                                   [],
                                                                   ["Bless"])]],
                 "Sapphire ring": ["Sapphire ring", 'img/Artifacts/sapphire_ring.png',
                                   1000, [],
                                   [artifact_classes.Artifact_Effect("Mana replenishment",
                                                                     1,
                                                                     "addition",
                                                                     None,
                                                                     [],
                                                                     [])]],
                 "Bone wand": ["Bone wand", 'img/Artifacts/bone_wand.png',
                               1400, [],
                               [artifact_classes.Artifact_Effect("Mana replenishment",
                                                                 2,
                                                                 "addition",
                                                                 None,
                                                                 [],
                                                                 []),
                                artifact_classes.Artifact_Effect("Melee mastery",
                                                                 1,
                                                                 "subtraction",
                                                                 None,
                                                                 [],
                                                                 ["melee infantry"])]],
                 "Old dwarven chieftain's axe": ["Old dwarven chieftain's axe",
                                                 'img/Artifacts/old_dwarven_chieftains_axe.png',
                                                 2000, [],
                                                 [artifact_classes.Artifact_Effect("Melee mastery",
                                                                                   2,
                                                                                   "addition",
                                                                                   None,
                                                                                   [],
                                                                                   ["melee infantry"]),
                                                  artifact_classes.Artifact_Effect("Bonus speed",
                                                                                   1,
                                                                                   "subtraction",
                                                                                   None,
                                                                                   [],
                                                                                   ["melee infantry"])]],
                 "Grimcloud horde's staff": ["Grimcloud horde's staff",
                                             'img/Artifacts/grimcloud_hordes_staff.png',
                                             1200, [],
                                             [artifact_classes.Artifact_Effect("Ability bonus Magic Power",
                                                                               2,
                                                                               "addition",
                                                                               None,
                                                                               [],
                                                                               []),
                                              artifact_classes.Artifact_Effect("Ability mana cost",
                                                                               1,
                                                                               "addition",
                                                                               None,
                                                                               [],
                                                                               [])]],
                 "Ancient elven sceptre": ["Ancient elven sceptre",
                                           'img/Artifacts/ancient_elven_sceptre.png',
                                           1500, [],
                                           [artifact_classes.Artifact_Effect("Movement points",
                                                                             300,
                                                                             "addition",
                                                                             None,
                                                                             [],
                                                                             []),
                                            artifact_classes.Artifact_Effect("Bonus leadership",
                                                                             1,
                                                                             "subtraction",
                                                                             None,
                                                                             [],
                                                                             [])]],
                 "Broken javelin": ["Broken javelin",
                                    'img/Artifacts/broken_javelin.png',
                                    1000, [],
                                    [artifact_classes.Artifact_Effect("Attack range",
                                                                      1,
                                                                      "addition",
                                                                      None,
                                                                      [],
                                                                      ["ranged infantry"]),
                                     artifact_classes.Artifact_Effect("Defence",
                                                                      1,
                                                                      "subtraction",
                                                                      None,
                                                                      [],
                                                                      ["melee cavalry"])]],
                 "Composite bow": ["Composite bow", 'img/Artifacts/composite_bow.png',
                                   3000, [],
                                   [artifact_classes.Artifact_Effect("Initiative time reduction",
                                                                     0.15,
                                                                     "subtraction",
                                                                     None,
                                                                     ["Ranged"],
                                                                     ["ranged infantry"])]],
                 "Elven crown": ["Elven crown", 'img/Artifacts/elven_crown.png',
                                 3000, [],
                                 [artifact_classes.Artifact_Effect("Ability bonus initiative",
                                                                   0.15,
                                                                   "subtraction",
                                                                   None,
                                                                   [],
                                                                   [])]],
                 "Forgotten mask": ["Forgotten mask", 'img/Artifacts/forgotten_mask.png',
                                    3000, [],
                                    [artifact_classes.Artifact_Effect("Ability bonus Magic Power",
                                                                      2,
                                                                      "addition",
                                                                      None,
                                                                      [],
                                                                      ["caster"])]],
                 "Hat of grand wizard": ["Hat of grand wizard", 'img/Artifacts/hat_of_grand_wizard.png',
                                         3000, [],
                                         [artifact_classes.Artifact_Effect("Knowledge",
                                                                           2,
                                                                           "addition",
                                                                           None,
                                                                           [],
                                                                           [])]],
                 "Champion's sword": ["Champion's sword", 'img/Artifacts/champions_sword.png',
                                      3000, [],
                                      [artifact_classes.Artifact_Effect("Melee mastery",
                                                                        1,
                                                                        "addition",
                                                                        None,
                                                                        [],
                                                                        ["melee infantry"]),
                                       artifact_classes.Artifact_Effect("Defence",
                                                                        1,
                                                                        "addition",
                                                                        None,
                                                                        [],
                                                                        ["melee infantry"])]]
                 }
