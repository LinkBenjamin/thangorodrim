'''The Player class'''

import json
from math import floor
from core.die import Die
from core.archetypes import Archetype
from core.races import Race
from core.classes import CharacterClass

class Player:
    def __init__(self, player_data):
        '''Base Constructor (expects a complete player_data dictionary)'''
        self.player_name = player_data['name']
        self.level = player_data['level']
        self.experience = player_data['experience']
        self.archetype = Archetype(race=Race[player_data['race']],char_class=CharacterClass[player_data['character_class']])

        self.max_hit_points = player_data['max_hit_points']
        self.current_hit_points = player_data['current_hit_points']
        self.max_magic_points = player_data['max_magic_points']
        self.current_magic_points = player_data['current_magic_points']
        self.max_carrying_capacity = player_data['max_carry']

        self.strength = player_data['strength']
        self.intelligence = player_data['intelligence']
        self.dexterity = player_data['dexterity']
        self.constitution = player_data['constitution']

        self.helmet = player_data['helmet']
        self.armor = player_data['armor']
        self.boots = player_data['boots']
        self.neck = player_data['neck']
        self.finger = player_data['finger']
        self.shield = player_data['shield']
        self.weapon = player_data['weapon']
        self.quiver = player_data['quiver']

        self.inventory = player_data['inventory']

    # --- FACTORY CONSTRUCTORS ---

    @classmethod
    def from_file(cls, filepath):
        '''Load player data from a JSON file'''
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(data)
    
    @classmethod
    def from_json(cls, data):
        '''Initialize from an existing JSON object or dictionary'''
        return cls(data)
    
    @classmethod
    def new_player(cls, name, character_class, race):
        """Create a new player from string inputs, with calculated defaults."""

        archetype = Archetype(race=Race[race],char_class=CharacterClass[character_class])

        strength, _ = Die.roll('4d5')
        intelligence, _ = Die.roll('4d5')
        dexterity, _ = Die.roll('4d5')
        constitution, _ = Die.roll('4d5')

        max_hp = cls.set_hit_points(cls, 1, constitution, archetype.health_die)
        max_mp = cls.set_magic_points(cls, 1, intelligence,archetype.magic_die)
        max_carry = cls.set_carry(cls, 1, strength)

        player_data = {
            'name': name,
            'level': 1,
            'experience': 0,
            'race': race,
            'character_class': character_class,

            # Derived / default values
            'max_hit_points': max_hp,
            'current_hit_points': max_hp,
            'max_magic_points': max_mp,
            'current_magic_points': max_mp,
            'max_carry': max_carry,

            # Simple defaults or random generation
            'strength': strength,
            'intelligence': intelligence,
            'dexterity': dexterity,
            'constitution': constitution,

            # Empty equipment/inventory
            'helmet': None,
            'armor': None,
            'boots': None,
            'neck': None,
            'finger': None,
            'shield': None,
            'weapon': None,
            'quiver': None,
            'inventory': [],
        }

        return cls(player_data)
    
    # --- STAT METHODS ---

    def set_hit_points(self, new_level, constitution, base_die):
        """
        Incrementally increases HP up to `new_level` based on Constitution and dice rolls.
        Uses the Die class for randomness: total, rolls = Die.roll(base_die)

        If called when the player already has HP from previous levels, it only rolls
        for levels that haven't been accounted for yet.
        """
        con_mod = floor((constitution - 10) / 2)
        starting_level = getattr(self, "level", 0)
        total_hp = getattr(self, "max_hit_points", 0)

        # Only roll for levels gained beyond current level
        for _ in range(starting_level + 1, new_level + 1):
            total, _ = Die.roll(base_die)
            hp_gain = max(1, total + con_mod)
            total_hp += hp_gain

        self.level = new_level
        self.max_hit_points = total_hp
        # Heal player to full on level-up
        self.current_hit_points = total_hp

    def set_magic_points(self, new_level, intelligence, base_die):
        """
        Incrementally increases MP up to `new_level` based on Intelligence and dice rolls.
        Uses the Die class for randomness: total, rolls = Die.roll(base_die)

        If called when the player already has MP from previous levels, it only rolls
        for levels that haven't been accounted for yet.
        """
        int_mod = floor((intelligence - 10) / 2)
        starting_level = getattr(self, "level", 0)
        total_mp = getattr(self, "max_magic_points", 0)

        # Only roll for levels gained beyond current level
        for _ in range(starting_level + 1, new_level + 1):
            total, _ = Die.roll(base_die)
            mp_gain = max(1, total + int_mod)
            total_mp += mp_gain

        self.level = new_level
        self.max_magic_points = total_mp
        # Reset Magic points on a level up
        self.current_magic_points = total_mp

    def set_carry(self, new_level, strength):
        computed = self.calculate_max_carry(new_level,strength)
        try:
            self.max_carrying_capacity = computed
        except Exception:
            pass
        return computed

    # --- GAMEPLAY METHODS ---

    def move(self, direction, speed):
        pass

    def equip(self, item):
        pass

    def melee_attack(self):
        pass

    def ranged_attack(self):
        pass

    def use_magic(self):
        pass

    def pick_up(self, item):
        pass

    def drop(self, item):
        pass

    def _calculate_weight_(self):
        pass

    # --- HELPER METHODS ---

    @staticmethod
    def calculate_max_carry(new_level, strength):
        '''
        Helper method to calculate max carry weight
        '''

        base = 50 + max(0, int(strength)) * 10
        level = max(1, int(new_level))
        level_multiplier = 1.0 + 0.03 * (level - 1)
        final = base * level_multiplier
        final = max(50, final)
        final = min(500, final)
        return int(floor(final))
