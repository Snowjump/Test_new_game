## Miracle battles!

class Realm_Relations:  # Keep information about diplomatic relations
    def __init__(self):
        self.at_war = []  # List of hostile realms: Lists with str(first color), str(second color), str(name)


class War:  # main class for ongoing wars
    def __init__(self, initiator, initiator_f_color, initiator_s_color, respondent, respondent_f_color,
                 respondent_s_color, war_goals, max_war_enthusiasm):
        self.initiator = initiator  # Realm name
        self.initiator_f_color = initiator_f_color
        self.initiator_s_color = initiator_s_color
        self.initiator_battle_victories = 0
        self.respondent = respondent  # Realm name
        self.respondent_f_color = respondent_f_color
        self.respondent_s_color = respondent_s_color
        self.respondent_battle_victories = 0
        self.war_goals = war_goals
        self.max_war_enthusiasm = max_war_enthusiasm
        self.war_duration = 0


class Relations_Summary:  # Used in diplomacy screen in diplomatic actions area
    def __init__(self, ongoing_war):
        self.ongoing_war = ongoing_war  # True or false


class War_Summary:  # Used in diplomacy screen in diplomatic actions area
    def __init__(self, war_goals, max_war_enthusiasm, own_realm_war_enthusiasm, opponent_war_enthusiasm,
                 own_realm_battle_victories, opponent_battle_victories, own_realm_captured_provinces,
                 opponent_captured_provinces, war_duration, player_is_initiator):
        self.war_goals = war_goals  # List
        self.max_war_enthusiasm = max_war_enthusiasm
        self.own_realm_war_enthusiasm = own_realm_war_enthusiasm
        self.opponent_war_enthusiasm = opponent_war_enthusiasm
        self.own_realm_battle_victories = own_realm_battle_victories
        self.opponent_battle_victories = opponent_battle_victories
        self.own_realm_captured_provinces = own_realm_captured_provinces
        self.opponent_captured_provinces = opponent_captured_provinces
        self.war_duration = war_duration  # Int - counting from 0
        self.player_is_initiator = player_is_initiator  # True if player is an initiator


class Diplomatic_Message:
    def __init__(self, dm_from, dm_to, subject, contents, f_color_from=None, s_color_from=None):
        self.dm_from = dm_from  # Realm name
        self.dm_to = dm_to  # Realm name
        self.subject = subject  # Str
        self.contents = contents  # List
        self.discard = False  # True or False status (should be discarded when True)
        self.f_color_from = f_color_from
        self.s_color_from = s_color_from
