from core.races import Race
from core.classes import CharacterClass
from collections import Counter

class Archetype:
    def __init__(self, race: Race, char_class: CharacterClass):
        self.race = race
        self.char_class = char_class

    @property
    def health_die(self):
        return self.race.health_die

    @property
    def magic_die(self):
        return self.char_class.magic_die

    @property
    def bonuses(self):
        c1 = Counter(self.race.bonuses)
        c2 = Counter(self.char_class.bonuses)
        return dict(c1 + c2)
        
    def __repr__(self):
        return f"{self.race.label} {self.char_class.label}"
