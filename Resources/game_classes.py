## Among Myth and Wonder
## game_classes

import pygame.draw
from Resources import diplomacy_classes
from Strategy_AI import strategy_AI_classes


class Realm:  # player's information
    def __init__(self, name, f_color, s_color, alignment, coffers, leader):
        self.name = name
        self.f_color = f_color
        self.s_color = s_color
        self.alignment = alignment
        self.status = True
        self.known_map = []  # List of lists [int x, int y]
        self.turn_completed = False
        self.coffers = coffers  # List - Information about obtained resources for the ruler
        self.building_priority_queue = []  # Realm's queue for preparing resources among for building structures
        self.artifact_collection = []
        self.reward_IDs = []  # List of IDs for rewards
        self.quests_messages = []
        self.leader = leader  # Realm leader
        self.contacts = []  # Contacted realms, required to participate in diplomacy. List of str(names)
        self.relations = diplomacy_classes.Realm_Relations()
        self.diplomatic_messages = []
        self.AI_player = True  # Would be changed to False if human choose to play this realm
        self.AI_cogs = AI_cognition()
        self.playable = False  # By default a realm is not playable by a human player, unless switched to True in
        # level editor


class Roadway:  # main class for road improvements on tiles for faster armies movements
    def __init__(self, material, speed):
        self.material = material
        self.speed = speed
        # road connection with nearby tiles
        self.l_m = False
        self.r_m = False
        self.m_t = False
        self.m_b = False
        self.r_t = False
        self.l_b = False
        self.r_b = False
        self.l_t = False


class Tile:  # main class for tile cells
    def __init__(self, position, terrain, conditions):
        self.posxy = position
        self.terrain = terrain
        self.conditions = conditions
        self.road = None  # Place for roadway class object
        self.travel = True
        self.lot = None
        self.city_id = None
        self.army_id = None


class Settlement:  # main class for cities that control surrounding lands and let hire heroes and armies
    def __init__(self, position, location, city_id, name, alignment, owner, factions, buildings,
                 new_quest_message_countdown):
        self.posxy = position
        self.location = location
        self.city_id = city_id
        self.name = name
        self.alignment = alignment
        self.owner = owner
        self.control_zone = []  # List of Int - tile numbers in game_obj.game_map
        self.obj_typ = "Settlement"
        self.property = []  # TileNum - facility type map objects that belong to this settlement
        self.factions = factions
        self.residency = []  # List with population class objects
        self.inner_market = []
        self.previous_inner_market = []
        self.market_demand = []
        self.buildings = buildings  # List of development plots with or without built structures in settlement
        self.records_turnover_tax = 0  # Records of taxes on trade to realm (in florins)
        self.records_local_fees = []  # Records of fees paid with produced resources by local population
        self.control = []  # List of lists with [realm type, int value of control]
        self.local_effects = []  # Effects that influence settlement and region
        self.new_quest_message_countdown = new_quest_message_countdown
        self.defences = []
        self.siege = None  # Blockade class object is stored here
        self.military_occupation = None  # Either None or list: [first color, second color, name of occupying realm]


class Map_Object:  # main class for objects of nature, landscape and obstacles
    def __init__(self, position, location, obj_name, img_path, obj_typ, disposition, properties):
        self.posxy = position
        self.location = location
        self.obj_name = obj_name
        self.img_path = img_path
        self.obj_typ = obj_typ
        self.disposition = disposition  # List of coordinates to ut numeral instances of same object
        self.properties = properties


class Object_Properties:
    def __init__(self, img_name, obj_script, wait_time):
        self.img_name = img_name
        self.hero_list = []  # List with Heroes IDs
        self.obj_script = obj_script  # Script for encounter with an army
        self.army_id = None
        self.need_replenishment = False
        self.waiting_time_for_replenishment = wait_time  # Standard needed time before replenishment
        self.time_left_before_replenishment = 0  # Decreasing after activation
        self.storage = []  # Could contain objects for quest if needed


class Object_Surface:
    def __init__(self, obj_funs, obj_button_zone, square, click_scripts):
        self.obj_funs = obj_funs
        self.obj_button_zone = obj_button_zone
        self.square = square
        self.click_scripts = click_scripts  # script address


class Facility:  # main class for facilities that belong to settlements in whose control zone they exist
    def __init__(self, position, location, obj_name, img_path, img_name, obj_typ, disposition, alignment,
                 thematic_name):
        self.posxy = position
        self.location = location
        self.obj_name = obj_name  # Common name to describe its use
        self.thematic_name = thematic_name  # Flavour name for demonstration
        self.img_path = img_path
        self.img_name = img_name
        self.obj_typ = obj_typ
        self.disposition = disposition
        self.alignment = alignment
        self.residency = []  # List with population class objects


class Development_Plot:  # main class for piece of land, that could have structure built upon it
    def __init__(self, screen_position, structure, status, upgrade):
        self.screen_position = screen_position  # Position of development plot on settlement screen interface
        self.structure = structure
        self.status = status  # Empty when no structure exist, Building when structure is being built, Built when
        # structure is ready to operate
        self.upgrade = upgrade
        self.collected_resources = []  # Collected resources for building this structure
        self.priority = None  # Int number or None - priority number in realm for collecting resources
        # before construction


class Army:  # main class for armies that consist of from 1 up to 20 units and could have a hero
    def __init__(self, position, location, army_id, owner, right_side):
        self.posxy = position  # [x, y]
        self.location = location  # int(TileNum)
        self.army_id = army_id
        self.owner = owner
        self.right_side = right_side  # True or False
        self.hero = None
        self.units = []
        self.leader = None
        self.route = []
        self.path_arrows = []
        self.action = "Stand"  # Stand, Ready to move, Moving, Routing, Fighting, Besieging, Besieged
        self.shattered = "Stable"
        self.event = None


class Regiment:  # main class for creatures that serves as units for fighting in land battles
    def __init__(self, name, rank, img, img_source, x_offset, y_offset, speed, img_width, img_height, base_HP,
                 max_mana_reserve, base_magic_power, number, rows, reg_tags, crew, attacks, armour, defence,
                 base_leadership, skills, cost, abilities):
        self.name = name
        self.rank = rank  # Demonstrates importance of unit in army, what determines which unit would be shown on map
        self.img = img
        self.img_source = img_source
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.img_width = img_width
        self.img_height = img_height
        self.right_side = True  # True - right direction, False - left direction
        self.reg_tags = reg_tags  # List of regiment tags
        # Parameters
        self.movement_points = 800
        self.max_movement_points = 800
        self.speed = speed  # Movement range in battle
        self.base_HP = base_HP  # Value of full health for creatures in this regiment
        self.max_HP = None  # Value of full health for creatures in this regiment with applied bonuses in battle
        self.experience = 0
        self.number = number  # Number of creatures in row
        self.rows = rows  # Number of rows
        self.crew = crew  # List of creatures that fill regiment
        self.cemetery = []  # Where dead creatures get put from crew
        self.position = None  # Position on battlefield
        self.direction = None  # In what direction regiment is oriented on battlefield
        self.attacks = attacks  # List of attacks consisting of Strike class objects
        self.engaged = False
        self.armour = armour
        self.defence = defence
        self.counterattack = 1
        self.effects = []  # Different effects during the battle
        self.skills = skills  # Just various skills used by regiment in a form of list with skill objects
        self.base_leadership = base_leadership  # Regiment base leadership
        self.leadership = 0.0  # Regiment's maximum morale based on its leadership and various bonuses
        self.morale = 0.0  # Regiment's morale, if it gets lower than 0, then regiment will route in battle
        self.deserted = False
        self.cost = cost  # List of lists with cost per creature [str - resource, int - amount]
        self.initiative = 0.0  # This variable modifies regiment's next action time if needed
        self.max_mana_reserve = max_mana_reserve
        self.mana_reserve = 0
        self.base_magic_power = base_magic_power
        self.magic_power = 0
        self.abilities = abilities  # List of ability names
        self.siege_engine = None
        self.in_air = False  # For animation in battle, should be lifted higher if regiment is flying


class Strike:  # main class for attacks performed by regiments
    def __init__(self, name, attack_type, tags, min_dmg, max_dmg, mastery, effective_range, range_limit):
        self.name = name
        self.attack_type = attack_type
        self.tags = tags  # List of tags
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.mastery = mastery
        self.effective_range = effective_range
        self.range_limit = range_limit


class Creature:  # main class for creature that fill regiment units in land battles
    def __init__(self, name, img, img_source, img_width, img_height, HP):
        self.name = name
        self.img = img
        self.img_source = img_source
        self.img_width = img_width
        self.img_height = img_height
        self.HP = HP  # Hit points - creature's health
        self.alive = True  # Status used during battle


class Land_Battle:  # class keeps information about outgoing battle
    def __init__(self, battle_id, attacker_id, attacker_realm, defender_id, defender_realm, terrain, conditions,
                 battle_type, battle_map, battle_pov, cover_map, starting_attacking_positions,
                 starting_defending_positions, result_script, available_siege_towers, available_battering_rams):
        self.button_pressed = False
        self.battle_id = battle_id
        self.attacker_id = attacker_id  # Army ID
        self.attacker_realm = attacker_realm  # Name of a realm
        self.defender_id = defender_id  # Army ID
        self.defender_realm = defender_realm  # Name of a realm
        self.realm_in_control = None  # Name of a realm - every time a queue card called, one of fighting players takes
        # control of battlefield if needed
        self.enemy = None  # Opposite of realm in control
        self.enemy_army_id = None  # ID of army that belong to realm that is opposite to realm in control
        self.terrain = terrain
        self.conditions = conditions
        self.battle_type = battle_type
        self.battle_map = battle_map
        self.battle_pov = battle_pov
        self.stage = "Formation"
        self.cover_map = cover_map
        self.starting_attacking_positions = starting_attacking_positions
        self.starting_defending_positions = starting_defending_positions
        self.selected_tile = []
        self.selected_unit = -1  # Index of tile with selected regiment
        # -1 means that no regiment is selected at this moment
        self.selected_unit_alt = ()  # (x, y) position format
        self.waiting_list = []  # In formation stage, list contains units that yet need to be positioned on map
        self.waiting_index = 0
        self.unit_card = -1  # Index of unit card in waiting list
        self.preparation_siege_machine = None
        self.queue = []
        self.queue_index = 0
        self.AI_ready = False
        self.ready_to_act = False  # Needed for animation
        self.attack_type_index = 0  # Used when player is changing attack methods
        self.attack_type_in_use = ""
        self.attack_name = ""
        self.cur_effective_range = 0
        self.cur_range_limit = 0
        self.earned_experience = 0  # Calculated after completing battle
        self.result_script = result_script  # From game_stats.battle_result_script

        # Siege machines
        self.available_siege_towers = available_siege_towers
        self.available_battering_rams = available_battering_rams
        self.available_equipment = []  # Show equipment at one particular tile

        self.movement_grid = None  # Calculated before regiment movement in a form of list with [x, y] coordinates
        self.path = None  # Bunch of nodes
        self.tile_trail = None  # Reversed path toward destination for moving unit
        self.primary = None  # Battle order for unit to perform an action
        self.secondary = None  # Next battle order for unit to perform an action
        self.move_figure = None  # For flying
        self.anim_message = None  # Text on battlefield
        self.move_destination = None  # Where unit is going
        self.target_destination = None  # Whom unit going to hit
        self.move_back_destination = None  # Where unit is returning after hit and run or hit and fly attack
        self.changed_direction = None  # Unit changes its direction when it has to shoot
        self.attacking_rotate = []  # List of units from army whose unit is attacking in melee right now
        self.defending_rotate = []  # List of units from army whose unit is being attacked in melee right now
        self.perform_attack = []  # List of indexes that indicates which creatures from regiment will perform attack
        self.dealt_damage = 0  # Total amount of damage dealt during one attack by regiment
        self.killed_creatures = 0
        self.damage_msg_position = []  # Around which unit should message pop up

        self.battle_stop = False  # Turn to True when battle is over
        self.battle_end_message = ""  # Illustrated on Battle end window
        self.defeated_side = None

        self.battle_window = None  # Additional window to draw and operate in battle
        self.unit_info = None  # When player performs right click on any regiment, this variable gets an object with
        # an information about this regiment

        # Regiment information window variables
        self.regiment_attack_type_index = 0
        self.attack_info = None  # When player performs right click on any regiment, this variable gets an object with
        # an information about this regiment's attack
        self.regiment_skills_index = 0
        self.skill_info = None  # When player performs right click on any regiment, this variable gets an object with
        # an information about this regiment's skill
        self.regiment_effects_index = 0
        self.effect_info = None  # When player performs right click on any regiment, this variable gets an object with
        # an information about this regiment's effect that currently affects it
        self.effect_status_index = 0
        self.regiment_abilities_index = 0
        self.ability_info = None  # When player performs right click on any regiment, this variable gets a name of
        # this regiment's ability

        # Abilities menu window variables
        self.list_of_schools = []
        self.list_of_abilities = []
        self.school_index = 0
        self.ability_index = 0
        self.selected_school = None
        self.selected_ability = None
        self.available_mana_reserve = None
        self.ability_description = None

        # Effects
        self.positions_list = []

        # Cursor function
        self.cursor_function = None

        # Time constants
        self.battle_last_start = 0
        self.battle_temp_time_passed = 0
        self.battle_passed_time = 0
        self.battle_display_time = 0
        self.battle_last_change = 0


class Battle_Tile:  # main class for tile cells in battlefield
    def __init__(self, position, terrain, conditions):
        self.posxy = position
        self.terrain = terrain
        self.conditions = conditions
        self.unit_index = None
        self.army_id = None
        self.passing_unit_index = None  # For regiments that travel over this tile
        self.passing_army_id = None  # For regiments that travel over this tile
        self.map_object = None
        self.graveyard = []
        self.aura_effects = []
        self.siege_machines = []  # List of lists: [name of siege engine, [coordinates on tile],
        # right side (True or False)]
        self.siege_tower_deployed = False


class Battle_Map_Object:  # class for interactive objects on battle map
    def __init__(self, obj_name, img_path, obj_type, disposition, travel, properties):
        self.obj_name = obj_name
        self.img_path = img_path
        self.obj_type = obj_type  # Obstacle, Structure
        self.disposition = disposition  # List of list for obstacles, single list for structures
        self.travel = travel
        self.properties = properties  # None for obstacles, effect_classes.Battle_Structure_Properties for structures


class Grave:  # main class for dead regiments in battlefield, created at Battle_Tile.graveyard
    def __init__(self, unit_index, army_id):
        self.unit_index = unit_index
        self.army_id = army_id


class Queue_Card:  # class for tracking position of regiment in time queue
    def __init__(self, time_act, obj_type, army_id, owner, number, position, img_source, img, f_color, s_color,
                 x_offset, y_offset, img_width, img_height, title):
        self.time_act = time_act
        self.obj_type = obj_type
        self.army_id = army_id
        self.owner = owner
        self.number = number  # Index of unit in army
        self.position = position
        self.img_source = img_source
        self.img = img
        self.f_color = f_color
        self.s_color = s_color
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.img_width = img_width
        self.img_height = img_height
        self.title = title  # Needed for queue card of acting effects


class Regiment_Info_Card:  # Contain information about regiment that was clicked on with right mouse button
    def __init__(self, regiment_name, first_color, second_color, amount, total_HP, morale, health, experience, speed,
                 leadership, engaged, deserted, attacks_amount, armour, final_armour, defence, final_defence, reg_tags,
                 magic_power, mana_reserve, max_mana_reserve, abilities):
        self.regiment_name = regiment_name
        self.first_color = first_color
        self.second_color = second_color
        self.amount = amount
        self.total_HP = total_HP
        self.morale = morale
        self.health = health
        self.experience = experience
        self.speed = speed
        self.leadership = leadership
        self.engaged = engaged
        self.deserted = deserted
        self.attacks_amount = attacks_amount
        self.armour = armour
        self.final_armour = final_armour  # After applying effects
        self.defence = defence
        self.final_defence = final_defence  # After applying effects
        self.reg_tags = reg_tags  # List of regiment's tags
        self.magic_power = magic_power
        self.mana_reserve = mana_reserve
        self.max_mana_reserve = max_mana_reserve
        self.abilities = abilities


class Attack_Info_Card:  # Contain information about regiment's attack for information window about regiment
    def __init__(self, attack_name, attack_type, min_dmg, max_dmg, mastery, effective_range, range_limit, tags):
        self.attack_name = attack_name
        self.attack_type = attack_type
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.mastery = mastery
        self.effective_range = effective_range
        self.range_limit = range_limit
        self.tags = tags


class Skill_Info_Card:  # Contain information about regiment's skill for information window about regiment
    def __init__(self, skill_name, application, value_text, skill_tags):
        self.skill_name = skill_name
        self.application = application
        self.value_text = value_text
        self.skill_tags = skill_tags


class Effect_Info_Card:  # Contain information about regiment's skill for information window about regiment
    def __init__(self, effect_name, time_text, status_list):
        self.effect_name = effect_name
        self.time_text = time_text
        self.status_list = status_list


class Attribute_Package:
    def __init__(self, attribute_list, package_name=None):
        self.attribute_list = attribute_list
        self.package_name = package_name


class Battle_Attribute:
    def __init__(self, tag, stat, value, name=None):
        self.tag = tag
        self.stat = stat
        self.value = value
        self.name = name


class Hero:
    def __init__(self, hero_id, name, hero_class, level, experience, magic_power, knowledge, attributes_list, img,
                 img_source, x_offset, y_offset, starting_skills, max_mana_reserve, mana_reserve):
        self.hero_id = hero_id
        self.name = name
        self.hero_class = hero_class
        # Archetype is used by AI players to determine how to develop a hero
        # It decides what skills, perks and attributes to take
        self.archetype = None
        self.level = level
        self.experience = experience
        self.magic_power = magic_power
        self.knowledge = knowledge
        self.attributes_list = attributes_list  # Attribute_Package objects
        self.img = img
        self.img_source = img_source
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.skills = starting_skills
        self.abilities = []  # list of abilities
        self.max_mana_reserve = max_mana_reserve
        self.mana_reserve = mana_reserve
        self.new_attribute_points = 0
        self.new_skill_points = 0
        self.new_skills = []  # Keep selection of new skills for hero
        self.attribute_points_used = 1
        self.inventory = []  # Equipped artifacts - maximum number is 4
        self.initiative = 0.0  # Next active time of hero after using ability


class Quest_Message:
    def __init__(self, name, settlement_location, settlement_name, message_type, alignment, target_type, target_id,
                 remaining_time):
        self.name = name
        self.settlement_location = settlement_location
        self.settlement_name = settlement_name
        self.message_type = message_type  # Could be: Dilemma, Quest
        self.alignment = alignment
        self.target_type = target_type  # Could be: None, Army
        self.target_id = target_id  # Either None or Id of target army
        self.remaining_time = remaining_time  # Either None or Int to countdown when quest would be failed


class Post_Battle_Event:
    def __init__(self, name, settlement_location, realm_name):
        self.name = name  # Name of quest
        self.settlement_location = settlement_location
        self.realm_name = realm_name  # Name of realm that has a quest related to this battle


class Blockade:
    def __init__(self, attacker_id, attacker_realm, supplies, time_passed, trebuchets_max_quantity,
                 siege_towers_max_quantity, battering_rams_max_quantity):
        self.attacker_id = attacker_id  # id of enemy army that besieged this settlement
        self.attacker_realm = attacker_realm  # Realm name
        self.supplies = supplies  # Number of turns left without attrition damage to garrison
        self.time_passed = time_passed  # Number of turns passed since beginning of blockade
        self.trebuchets_ordered = 0
        self.trebuchets_ready = 0
        self.trebuchets_max_quantity = trebuchets_max_quantity
        self.trebuchets_construction_points_leftover = 0
        self.siege_towers_ordered = 0
        self.siege_towers_ready = 0
        self.siege_towers_max_quantity = siege_towers_max_quantity
        self.siege_towers_construction_points_leftover = 0
        self.battering_rams_ordered = 0
        self.battering_rams_ready = 0
        self.battering_rams_max_quantity = battering_rams_max_quantity
        self.battering_rams_construction_points_leftover = 0
        self.construction_orders = []  # Lists [siege machine name, construction points spent]
        self.siege_log = []  # Siege log contains string messages about siege events


class Realm_Leader:
    def __init__(self, name, behavior_traits, lifestyle_traits):
        self.name = name  # Name of the leader
        self.behavior_traits = behavior_traits
        self.lifestyle_traits = lifestyle_traits


class AI_cognition:
    def __init__(self):
        # Stages: "Diplomacy", "Economy", "Manage armies", "Finished turn"
        self.cognition_stage = "Diplomacy"
        self.army_roles = []  # Filled with strategy_AI_classes.army_roles objects
        self.economy_cogs = strategy_AI_classes.AI_economy()
        self.exploration_targets = []  # List of lists [int x, int y]


class LE_regiment_card:
    def __init__(self, name, img_source, img, x_offset, y_offset, rank):
        self.name = name
        self.img_source = img_source
        self.img = img
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.rank = rank


class Autobattle_Regiment_Card:
    def __init__(self, index, name, starting_power_level, power_level, morale):
        self.index = index  # (int) index of regiments in army.units
        self.name = name
        self.starting_power_level = starting_power_level  # (float)
        self.power_level = power_level  # (float)
        self.morale = morale  # (float)
        self.status = "Fighting"  # (str): Fighting, Routing, Routed
        self.receiving_damage = 0.0  # (float)
