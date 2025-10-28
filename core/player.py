'''The Player class'''

import json

class Player:
    def __init__(self, player_data):
        '''Base Constructor (expects a complete player_data dictionary)'''
        self.player_name = player_data['name']
        self.level = player_data['level']
        self.experience = player_data['experience']
        self.character_class = player_data['character_class']
        self.race = player_data['race']

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
        '''Auto-roll a new character'''
        pass

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
