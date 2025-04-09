## Among Myth and Wonder
## game_stats

# Software versioning
version_major = 0
version_minor = 3
version_micro = 10

# Essential information
author = "Snowjump"
app_name = "Among Myth and Wonder"

time_counted = 0
fps = 0.0
fps_status = True

# screen constants
current_screen = "Entrance Menu"

# Temporary
# sprite objects
gf_menus_art = {}
gf_misc_img_dict = {}
gf_terrain_dict = {}
gf_road_dict = {}
gf_settlement_dict = {}
gf_obstacle_dict = {}
gf_facility_dict = {}
gf_exploration_dict = {}
gf_regiment_dict = {}
gf_hero_dict = {}
gf_building_dict = {}
gf_skills_dict = {}
gf_artifact_dict = {}
gf_battle_effects_dict = {}

screen_to_draw = "main_menu_screen"

window_to_draw = None

mouse_position = ()

pov_pos = [0, 0]
game_window_width = 1280
game_window_height = 700

# Buttons and keys
mouse_button1_pressed = False
mouse_button3_pressed = False
key_pressed = False

# Typing
input_text = ""
record_text = False  # Either True or False, to copy keys into input_text
create_level_input_text = ""

# Levels selection
levels_list = []  # List of level files in folder
level_index = None  # int: Index of selected level from levels_list
start_level_total_realms = 0  # Total number of realms in level
start_level_playable_realms = 0  # Number of playable realms in level
start_level_selected_realm = None  # Selected playable realm
level_info = None  # Contains an object with an information about save file

# Create level
new_level_width = 9
new_level_height = 9
new_level_name = "New name"

level_width = ""  # The one in box-field
level_height = ""  # The one in box-field
level_name = ""  # The one in box-field
type_LE_month = ""  # The one in box-field

active_width_field = False
active_height_field = False
active_name_field = False
active_starting_month_field = False

# Level editor
level_map = []  # Contains tiles objects
LE_borders_map = []  # Contains information about realm borders on map tiles
LE_year = 0
LE_month = 5
LE_level_type = "Skirmish"

edit_instrument = ""
selected_tile = []
saved_selected_tile = []  # Sometimes it's needed to remember last selected tile
level_editor_panel = ""
level_editor_left_panel = ""
brush = "Plain"
brush_size = 1
brush_shape = 1
object_category = ""
lower_panel = ""  # Variable calls panel with detailed information
powers_l_p_index = 0
power_short_index = 0
unit_short_index = 0
facility_short_index = 0
lot_information = None  # Used to show information about population
population_l_p_index = 0  # Index of population in lower panel
faction_l_p_index = 0  # Index of faction in lower panel

# Editor variables
map_operations = True  # Permit to use keys to perform actions around the map
editor_powers = []
editor_cities = []
editor_armies = []
LE_cities_id_counter = 0
LE_army_id_counter = 0
LE_hero_id_counter = 0
LE_population_id_counter = 0
LE_faction_id_counter = 0
new_city_name = ""
new_country_name = ""
active_city_name_field = False
active_country_name_field = False
option_box_alinement_index = 0
option_box_first_color_index = 0
option_box_second_color_index = 0
city_allegiance = "Neutral"  # Option box that shows to whom would belong new city
army_allegiance = "Neutral"  # Option box that shows to whom would belong new army
selected_city_id = 0  # What city selected or created in this moment
last_city_id = 0  # Sometimes it needed to be saved and used later
delete_option = False  # toggle ability to delete units

boxed_city_name = ""  # The one in box-field
boxed_country_name = ""  # The one in box-field

settlement_option_view = "Population"
power_option_view = "Realm leader"
realm_leader_white_line = ""
realm_leader_traits_list = []
realm_leader_traits_index = 0
picked_leader_trait = ""

# available_traits_list = []

# Game stats
game_type = "singleplayer"  # Very important, if human player begin battle, when on global map game pause and wait until
# battle is concluded
level_type = None  # str: "Skirmish"
strategy_mode = True  # Very important, when on - all events work on global map
pause_status = True
pause_last_status = True
day = 0
hours = 0
minutes = 0
passed_time = 0
start_time = 0
last_start = 0
temp_time_passed = 0
count_started = False
display_time = 0
last_change = 0

game_year = 0
game_month = 0
turn_hourglass = False
show_time = False

cities_id_counter = 0
army_id_counter = 0
population_id_counter = 0
hero_id_counter = 0
reward_id_counter = 0

cur_level_width = 0
cur_level_height = 0
map_positions = []

# vision mode
border_vision = False
grid_vision = True

current_level_name = ""
player_power = ""
perspective = ""
game_board_panel = ""

details_panel_mode = ""  # Needed for lower information panel
event_panel_win = None
event_panel_det = None
rw_panel_det = None
button_pressed = False  # For mouse clicks to avoid mix up between window clicks and map clicks

location_factions = []  # List contains names of factions in particular tile
locations_colors = []  # List contains faction colors in particular tile
white_index = None  # In the information panel draw white rectangle around selected character

selected_object = ""
selected_army = -1  # Army ID needed to give movement commands. -1 is base value when no army has been selected
selected_second_army = -1  # Army ID of second army in exchange. -1 is base value when no army has been approached
selected_settlement = -1  # Settlement ID. -1 is base value when no settlement has been selected
settlement_area = ""  # In settlement window define what part of interface to show
settlement_subsection = ""  # At this moment only required for Economy area
right_window = ""  # Window with information on right side of screen
rw_object = None  # rw - right window. Could be anything needed to be investigated
building_row_index = 0  # Needed in det_settlement_building to determine which rows of buildings to draw
building_rows_amount = 0  # Needed in det_settlement_building to determine length of buildings scroll
enough_resources_to_pay = None  # True or False
hero_in_settlement = None
inventory_is_full = None
hero_inventory = None
already_has_an_artifact = None
realm_artifact_collection = None
artifact_focus = None  # Either None, or Hero's inventory, or Realm's artifact collection
info_tile = []  # [x, y] - tile's coordinates, that was selected with right click to provide information about it
right_click_pos = []  # [x, y] - mouth position during right click
tile_ownership = "Wild lands"  # Ownership of tile that was right clicked
tile_flag_colors = []  # [first color, second color] - keep information about owner's flag colors after right click
i_p_index = 0  # Information panel index - index used in information panel, to keep track which element is being studied
right_click_city = -1  # city index that was right clicked
hero_information_option = None  # Which information show in hero information window
selected_skill_info = None
selected_new_attribute = None
selected_new_skill = None
selected_artifact_info = None
hero_doesnt_know_this_skill = None
hero_doesnt_know_this_attribute = None
selected_item_price = None  # Price in florins
detailed_regiment_info = False

first_army_exchange_list = []  # List of units to exchange
second_army_exchange_list = []  # List of units to exchange

unit_for_hire = None  # Object with information about unit recruitment
rw_unit_info = None  # Object with detailed information about unit
rw_attack_info = None  # Object with detailed information about unit's attack
rw_skill_info = None  # Object with detailed information about unit's skill

hero_for_hire = None  # Object with information about hero recruitment
first_starting_skill = None  # Used by form_starting_skills_pool()
second_starting_skill = None  # Used by form_starting_skills_pool()
skill_tree_level_index = 1

province_records = None  # List with information about taxes and fees from selected province
allocated_gains_records = None  # List with information about goods produced and obtained by population
allocated_sold_records = None  # List with information about goods sold to merchants by population
allocated_bought_records = None  # List with information about goods bought by merchants
allocated_requested_goods_records = None  # List with information about goods needed for population to buy

pops_details = None  # Object with information about selected population
population_subsection_index = -1  # Index of selected population card from left column
pops_card_index = 0  # Index for scrolling population cards

faction_screen_index = 0  # Index of selected faction from upper left column
faction_pops_index = 0  # Index for scrolling faction's population

# Messages
quest_area = "Quest messages"
selected_quest_messages = None  # From realm.quests_messages
quest_message_index = None  # Index of selected quest message from left column in Quest log window panel
quest_message_panel = None
dilemma_additional_options = []  # List of strings - when dilemma requires more buttons
selected_diplomatic_notifications = None
diplomatic_message_index = None  # Index of selected diplomatic message from left column in Quest log window panel
diplomatic_message_panel = None

# Diplomacy
realm_inspection = None  # Realm object to show information about
explored_contacts = []  # List of list [first color, second color, realm name]
contact_index = 0  # For scrolling contact list
contact_inspection = None  # Contacted realm object to show information about
diplomacy_area = "Diplomatic actions"  # In settlement window defines what part of interface to show
casus_bellis = []  # Used in "Declaration of war" and "Threaten"
cb_details = []  # Used in "Declaration of war" and "Threaten"
war_goals = []  # Used in "Declaration of war" and "Threaten"
dip_summary = None  # Uses Relations_Summary class object
war_summary = None  # Uses War_Summary class object
ongoing_wars = []  # Illustrates ongoing wars for player
war_notifications_index = 0
peace_demands = []
make_demands = True  # True - if player makes demands, False - if player offer concessions to opponent
demand_details = []
claimed_demands = []
peace_offer_text = []
will_accept_white_peace = False
will_accept_peace_agreement = False
calculated_pa_cost = 0  # Calculated peace agreement cost
summary_text = []
will_accept_threat_demands = False

war_inspection = None

# Player stats
# known_map = []
reward_for_demonstration = None
new_tasks = False  # True if player received new dilemmas or quests or diplomatic messages
map_to_display = []  # List of tiles acceptable to draw in sc_game_board
display_everything = False

# Battles
present_battle = None  # Reference battle that player is playing right now
battle_id_counter = 0
battle_width = 16
battle_height = 12
battle_base_modifier = 0.2
battle_base_morale_hit = 0.2
battle_morale_base_restoration = 0.3

# Beginning of the battle information
attacker_army_id = 0
attacker_realm = ""
defender_army_id = 0
defender_realm = ""
battle_type = ""  # "Battle", "Siege", "special"
battle_terrain = ""
battle_conditions = ""
blockaded_settlement_name = ""
assault_allowed = True
besieged_by_human = True  # More activated interface options if True
siege_assault = True  # When AI proceeded from blockade to assault
battle_result_script = None  # None is standard for regular battles, but battles in lairs could give a reward after
# Ending of the battle
battle_result = ""  # 4 variations: "Attacker has won", "Defender has won", "Draw", ""
result_statement = ""  # 4 variations: "Victory", "Defeat", "Draw", ""
earned_experience = 0  # experience earned from the battle for demonstration in victory screen
attacker_army = None
defender_army = None
attacker_troops_power_level_list = []
defender_troops_power_level_list = []
attacker_no_troops_left = False
defender_no_troops_left = False
