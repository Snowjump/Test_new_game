## Miracle battles!


# screen constants
current_screen = "Entrance Menu"


screen_to_draw = "main_menu_screen"

window_to_draw = None

mouse_position = ()

pov_pos = [0, 0]
game_window_width = 1280
game_window_height = 700

# Typing
input_text = ""

# Create level
new_level_width = 9
new_level_height = 9
new_level_name = "New name"

level_width = "" # The one in box-field
level_height = "" # The one in box-field
level_name = "" # The one in box-field
type_LE_month = "" # The one in box-field

active_width_field = False
active_height_field = False
active_name_field = False
active_starting_month_field = False

# Level editor
level_map = [] # Contains tiles objects
LE_year = 0
LE_month = 5

edit_instrument = ""
selected_tile = []
saved_selected_tile = [] # Sometimes it's needed to remember last selected tile
level_editor_panel = ""
brush = "Plain"
brush_size = 1
object_category = ""
lower_panel = "" # Variable calls panel with detailed information
powers_l_p_index = 0
power_short_index = 0
unit_short_index = 0
facility_short_index = 0


# Editor variables
map_operations = True # Permit to use keys to perform actions around the map
editor_powers = []
editor_cities = []
editor_armies = []
LE_cities_id_counter = 0
LE_army_id_counter = 0
new_city_name = ""
new_country_name = ""
active_city_name_field = False
active_country_name_field = False
option_box_alinement_index = 0
option_box_first_color_index = 0
option_box_second_color_index = 0
city_allegiance = "Neutral" # Option box that shows to whom would belong new city
army_allegiance = "Neutral" # Option box that shows to whom would belong new army
last_city_id = 0 # Sometimes it needed to be saved and used later
delete_option = False # toggle ability to delete units

boxed_city_name = "" # The one in box-field
boxed_country_name = "" # The one in box-field

# Game stats
game_type = "singleplayer"  # Very important, if human player begin battle, then on global map game pause and wait until
# battle is concluded
strategy_mode = True  # Very important, when on - all events work on global map
pause_status = True
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

cur_level_width = 0
cur_level_height = 0


current_level_name = ""
player_power = ""
perspective = ""
game_board_panel = ""

details_panel_mode = ""

location_factions = []  # List contains names of factions in particular tile
locations_colors = []  # List contains faction colors in particular tile
white_index = None  # In the information panel draw white rectangle around selected character

selected_object = ""
selected_army = -1  # Army ID needed to give movement commands. -1 is base value when no army has been selected

# Player stats
known_map = []

# Battles
battle_id_counter = 0
battle_width = 16
battle_height = 12
battle_base_modifier = 0.2
battle_base_morale_hit = 0.2
battle_morale_base_restoration = 0.3
# Beginning of battle information
attacker_army_id = 0
attacker_realm = ""
defender_army_id = 0
defender_realm = ""
battle_type = ""
battle_terrain = ""
battle_conditions = ""
