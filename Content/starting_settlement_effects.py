## Among Myth and Wonder

from Resources import campaign_effect_classes


# Control bonuses
control_bonus = {"Knight_lords_control_4" : campaign_effect_classes.Control_Effect("Knight Lords",
                                                                                   "Control",
                                                                                   4,
                                                                                   "Addition")}

alignment_base_control = {"Knight Lords" : campaign_effect_classes.Settlement_Effect("Base Knight Lords control",
                                                                     "Settlement",
                                                                     "Control",
                                                                     [control_bonus["Knight_lords_control_4"]],
                                                                     True)}
