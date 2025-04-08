## Among Myth and Wonder
## save_classes

import datetime

from Resources import game_stats
from Resources import game_obj


class Save_File:
    def __init__(self):
        # Meta data
        self.timestamp = datetime.datetime.now()
        # Game version when save was created
        self.game_version_micro = None  # int
        self.game_version_minor = None  # int
        self.game_version_major = None  # int
        # Level parameters
        self.level_type = None  # str
        self.level_name = None  # str
        self.game_year = None  # int
        self.game_month = None  # int
        self.cur_level_width = None  # int
        self.cur_level_height = None  # int
        # ID counters
        self.cities_id_counter = None  # str
        self.army_id_counter = None  # str
        self.population_id_counter = None  # str
        self.hero_id_counter = None  # str
        self.reward_id_counter = None  # str

        self.player_power = None  # str
        self.pov_pos = None  # list: [int, int]

        # Objects
        self.game_powers = None  # list: [Realm...]
        self.bin_realms = None  # list: [Realm...]
        self.game_map = None  # list: [Tile...]
        self.borders_map = None  # list: [Realm_Borders...]
        self.game_cities = None  # list: [Settlement...]
        self.game_armies = None  # list: [Army...]
        self.game_wars = None  # list: [War...]
        self.ongoing_wars = None  # list: [list[f_color, s_color, name]...]

    def fill_in_the_information(self):
        # Game version when save was created
        self.game_version_micro = game_stats.version_micro  # int
        self.game_version_minor = game_stats.version_minor  # int
        self.game_version_major = game_stats.version_major  # int
        # Level parameters
        self.level_type = game_stats.level_type  # str
        self.level_name = game_stats.current_level_name  # str
        self.game_year = game_stats.game_year  # int
        self.game_month = game_stats.game_month  # int
        self.cur_level_width = game_stats.cur_level_width  # int
        self.cur_level_height = game_stats.cur_level_height  # int
        # ID counters
        self.cities_id_counter = game_stats.cities_id_counter  # str
        self.army_id_counter = game_stats.army_id_counter  # str
        self.population_id_counter = game_stats.population_id_counter  # str
        self.hero_id_counter = game_stats.hero_id_counter  # str
        self.reward_id_counter = game_stats.reward_id_counter  # str

        self.player_power = game_stats.player_power  # str
        self.pov_pos = game_stats.pov_pos  # list: [int, int]

        # Objects
        self.game_powers = game_obj.game_powers  # list: [Realm...]
        self.bin_realms = game_obj.bin_realms  # list: [Realm...]
        self.game_map = game_obj.game_map  # list: [Tile...]
        self.borders_map = game_obj.borders_map  # list: [Realm_Borders...]
        self.game_cities = game_obj.game_cities  # list: [Settlement...]
        self.game_armies = game_obj.game_armies  # list: [Army...]
        self.game_wars = game_obj.game_wars  # list: [War...]
        self.ongoing_wars = game_stats.ongoing_wars  # list: [list[f_color, s_color, name]...]
