"""
Unit tests for core.archetypes.Archetype.

These tests ensure Archetype correctly maps Race and CharacterClass
combinations to derived attributes (e.g. health_die, magic_die, etc.).
"""
from core.races import Race
from core.classes import CharacterClass

from core.archetypes import Archetype

def test_human_warrior():
    """Human Warrior should use the expected health die."""
    a = Archetype(Race.HUMAN, CharacterClass.WARRIOR)

    assert a.health_die == "1d8"
