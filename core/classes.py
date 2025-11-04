from enum import Enum

class CharacterClass(Enum):
    # Label, Magic Die, Class Bonuses
    BURGLAR = ("Burglar", "1d6", {"strength":-1,"intelligence":2,"dexterity":2,"constitution":-2})
    RANGER = ("Ranger", "1d8", {"intelligence":1,"dexterity":3,"constitution":2})
    WARRIOR = ("Warrior", "1d3", {"strength":3,"intelligence":-5,"constitution":3})
    WIZARD = ("Wizard", "1d10", {"strength":-2,"intelligence":5,"constitution":-2})

    def __init__(self, label, magic_die, class_bonus):
        self.label = label
        self.magic_die = magic_die
        self.bonuses = class_bonus