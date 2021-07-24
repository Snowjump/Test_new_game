## Miracle battles

import pygame.draw


class Realm:  # player's information
    def __init__(self, name, f_color, s_color, alignment):
        self.name = name
        self.f_color = f_color
        self.s_color = s_color
        self.alignment = alignment
        self.status = True
        self.known_map = []
        self.turn_completed = False


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
    def __init__(self, position, location, city_id, name, alignment, owner):
        self.posxy = position
        self.location = location
        self.city_id = city_id
        self.name = name
        self.alignment = alignment
        self.owner = owner
        self.control_zone = []
        self.obj_typ = "Settlement"
        self.property = []


class Map_Object:  # main class for objects of nature, landscape and obstacles
    def __init__(self, position, location, obj_name, img_path, obj_typ, disposition):
        self.posxy = position
        self.location = location
        self.obj_name = obj_name
        self.img_path = img_path
        self.obj_typ = obj_typ
        self.disposition = disposition


class Facility:  # main class for facilities that belong to settlements in whose control zone they exist
    def __init__(self, position, location, obj_name, img_path, img_name, obj_typ, disposition, alignment):
        self.posxy = position
        self.location = location
        self.obj_name = obj_name
        self.img_path = img_path
        self.img_name = img_name
        self.obj_typ = obj_typ
        self.disposition = disposition
        self.alignment = alignment


class Army:  # main class for armies that consist of from 1 up to 20 units and could have a hero
    def __init__(self, position, location, army_id, owner):
        self.posxy = position
        self.location = location
        self.army_id = army_id
        self.owner = owner
        self.hero_id = None
        self.units = []
        self.leader = None
        self.route = []
        self.path_arrows = []
        self.action = "Stand"


class Regiment:  # main class for creatures that serves as units for fighting in land battles
    def __init__(self, name, rank, img, img_source, x_offset, y_offset, speed, base_HP, number, rows, reg_tags, crew,
                 attacks, armor, defence, base_leadership, skills):
        self.name = name
        self.rank = rank  # Demonstrates importance of unit in army, what determines which unit would be shown on map
        self.img = img
        self.img_source = img_source
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.reg_tags = reg_tags  # List of regiment tags
        # Parameters
        self.movement_points = 800
        self.max_movement_points = 800
        self.speed = speed  # Movement range in battle
        self.base_HP = base_HP  # Value of full health for creatures in this regiment
        self.experience = 0
        self.number = number  # Number of creatures in row
        self.rows = rows  # Number of rows
        self.crew = crew  # List of creatures that fill regiment
        self.cemetery = []  # Where dead creatures get put from crew
        self.position = None  # Position on battlefield
        self.direction = None  # In what direction regiment is oriented on battlefield
        self.attacks = attacks  # List of attacks consisting of Strike class objects
        self.engaged = False
        self.armor = armor
        self.defence = defence
        self.counterattack = 1
        self.effects = []  # Different effects during the battle
        self.skills = skills  # Just various skills used by regiment in a form of list with skill objects
        self.base_leadership = base_leadership  # Regiment base leadership
        self.leadership = 0.0  # Regiment's maximum morale based on its leadership and various bonuses
        self.morale = 0.0  # Regiment's morale, if it gets lower than 0, then regiment will route in battle


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
                 battle_map, battle_pov, cover_map, starting_attacking_positions, starting_defending_positions):
        self.battle_id = battle_id
        self.attacker_id = attacker_id  # Army ID
        self.attacker_realm = attacker_realm  # Name of a realm
        self.defender_id = defender_id  # Army ID
        self.defender_realm = defender_realm  # Name of a realm
        self.realm_in_control = None  # Name of a realm - every time a queue card called, one of fighting players takes
        # control of battlefield if needed
        self.enemy = None  # Opposite of realm in control
        self.enemy_army_id = None  # Id of army that belong to realm that is opposite to realm in control
        self.terrain = terrain
        self.conditions = conditions
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
        self.queue = []
        self.queue_index = 0
        self.AI_ready = False
        self.ready_to_act = False  # Needed for animation
        self.attack_type_index = 0  # Used when player is changing attack methods
        self.attack_type_in_use = ""
        self.cur_effective_range = 0
        self.cur_range_limit = 0

        self.movement_grid = None  # Calculated before regiment movement in a form of list with [x, y] coordinates
        self.path = None  # Bunch of nodes
        self.tile_trail = None  # Reversed path toward destination for moving unit
        self.primary = None  # Battle order for unit to perform an action
        self.secondary = None  # Next battle order for unit to perform an action
        self.anim_message = None  # Text on battlefield
        self.move_destination = None  # Where unit is going
        self.target_destination = None  # Whom unit going to hit
        self.changed_direction = None  # Unit changes its direction when it has to shoot
        self.attacking_rotate = []  # List of units from army whose unit is attacking in melee right now
        self.defending_rotate = []  # List of units from army whose unit is being attacked in melee right now
        self.perform_attack = []  # List of indexes that indicates which creatures from regiment will perform attack
        self.dealt_damage = 0  # Total amount of damage dealt during one attack by regiment
        self.killed_creatures = 0
        self.damage_msg_position = []  # Around which unit should message pop up

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
        self.obstacle = None
        self.graveyard = []


class Grave:  # main class for dead regiments in battlefield, created at Battle_Tile.graveyard
    def __init__(self, unit_index, army_id):
        self.unit_index = unit_index
        self.army_id = army_id


class Queue_Card:  # main class for tile cells in battlefield
    def __init__(self, time_act, obj_type, army_id, owner, number, position, img_source, img, f_color, s_color,
                 x_offset, y_offset):
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


class Battle_Map_Object:  # main class for objects of nature, landscape and obstacles in battle
    def __init__(self, obj_name, img_path, obj_typ, disposition):
        self.obj_name = obj_name
        self.img_path = img_path
        self.obj_typ = obj_typ
        self.disposition = disposition
