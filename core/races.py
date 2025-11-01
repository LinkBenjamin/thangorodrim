from enum import Enum

# The Race enum provides the list of character races you can play as.

class Race(Enum):
    # Label, Health Die, Race Bonuses
    HUMAN = ("Human", "1d8", {})
    ELF = ("Elf", "1d8", {"intelligence":2,"dexterity":2,"constitution":1})
    DWARF = ("Dwarf", "1d10", {"strength":2,"intelligence":1,"dexterity":2,"constitution":1})
    DUNADAN = ("Dunadan", "1d10", {"strength":1,"intelligence":1,"dexterity":1,"constitution":1})
    HOBBIT = ("Hobbit", "1d6", {"strength":-2,"dexterity":2})

    def __init__(self, label, health_die, race_bonus):
        self.label = label
        self.health_die = health_die
        self.bonuses = race_bonus
