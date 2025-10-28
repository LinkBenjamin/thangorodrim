'''Items.py'''

class Item:
    def __init__(self, item_data):
        self.name = item_data['name']
        self.type = item_data['type']
        self.value = item_data['value']
        self.weight = item_data['weight']
        
class Weapon(Item):
    def __init__(self, item_data, weapon_data):
        super().__init__(item_data)

        self.damage = weapon_data['damage']
        self.durability = weapon_data['durability']
        self.condition = weapon_data['condition']

class Armor(Item):
    def __init__(self, item_data, armor_data):
        super().__init__(item_data)

        self.armor_class = armor_data['armor_class']