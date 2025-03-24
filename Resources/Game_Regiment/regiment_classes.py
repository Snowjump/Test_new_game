## Among Myth and Wonder
## regiment_classes

import math

from Resources import game_stats


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
        self.position = None  # Position on battlefield - list of int
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

    def simple_change_morale(self, value):
        # For source agnostic changes
        if self.morale + value > self.leadership:
            self.morale = float(self.leadership)
        else:
            self.morale = float(math.ceil((self.morale + value) * 100)) / 100

    def reduce_morale(self, b, before_HP, angle):
        # For being intentionally hit by different kinds of attacks
        angle_modifier = {"Front right": 100.0,
                          "Right flank": 125.0,
                          "Rear right": 150.0,
                          "Rear": 150.0,
                          "Rear left": 150.0,
                          "Left flank": 125.0,
                          "Front left": 100.0,
                          "Front": 100.0,
                          "Ranged": 100.0,
                          "Spell": 100.0,
                          "Above": 133.0}

        total_HP = self.rows * self.number * self.base_HP
        print("before_HP - " + str(before_HP) + "; total_HP - " + str(total_HP) + "; b.dealt_damage - " + str(
            b.dealt_damage))
        damage_fraction = (b.dealt_damage / 2) / before_HP + (b.dealt_damage / 2) / total_HP
        morale_hit = float(math.ceil(damage_fraction / game_stats.battle_base_morale_hit * angle_modifier[angle])) / 100
        # print("angle_modifier - " + str(angle_modifier[angle]) + " damage_fraction - " + str(damage_fraction) +
        #       " morale_hit - " + str(morale_hit) + " b.dealt_damage - " + str(b.dealt_damage))
        self.morale -= morale_hit
        self.morale = float(int(self.morale * 100)) / 100


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