from core.races import Race
from core.classes import CharacterClass

from core.archetypes import Archetype

def test_human_warrior():
    a = Archetype(Race.HUMAN, CharacterClass.WARRIOR)

    assert a.health_die == "1d8"
