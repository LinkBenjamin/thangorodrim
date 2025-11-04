"""Unit tests for the Player class.

This module verifies core Player behaviors:
- loading a Player from a saved JSON file,
- computing current carry weight from equipment and inventory,
- creating a new Player via Player.new_player with sensible defaults
  (ability rolls, derived hit/magic points, archetype selection).

Tests rely on the sample data file `testdata/aragorn.json` located in the same
directory as this test module.
"""

import json
import os

from core.player import Player

ARAGORN_DATA_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'aragorn.json')

def test_player_carry_weight():
    '''Verify that the Player calculates the correct carry
       weight'''
    player = Player.from_file(ARAGORN_DATA_FILE)
    assert player.current_carry_weight() == 0    

def test_player_init_from_file():
    '''A Player object may be initialized direct from a file, 
       such as in the case of a saved game being reloaded

    Uses the Aragorn sample data file which should contain no items, so the expected
    carry weight is zero.
    '''
    player = Player.from_file(ARAGORN_DATA_FILE)
    assert player.current_carry_weight() == 0    

def test_player_init_from_file():
    """Load a Player from JSON and verify basic fields.

    Confirms that Player.from_file correctly populates attributes such as player_name.
    """
    player = Player.from_file(ARAGORN_DATA_FILE)

    expected_name = "Aragorn"

    assert player.player_name == "Aragorn", f"Expected character name to be {expected_name}, but got {player.player_name}."


def test_auto_roller():
    """Verify Player.new_player generates a valid starting character.

    Confirms:
    - provided name, race and class are preserved,
    - level starts at 1 with zero experience,
    - archetype-derived dice (health_die, magic_die) match expected values
      for the given race/class combinations.
    """
    
    player = Player.new_player(name="Bilbo", race="HOBBIT", character_class="BURGLAR")

    expected_name = "Bilbo"
    expected_experience = 0
    expected_level = 1

    assert player.player_name == "Bilbo", f"Expected character name to be {expected_name}, but got {player.player_name}."
    assert player.experience == 0, f"Expected experience to be {expected_experience}, but got {player.experience}."
    assert player.level == 1, f"Expected level to be {expected_level}, but got {player.level}."
    assert player.archetype.health_die == '1d6'
    assert player.archetype.magic_die == '1d6'

    player = Player.new_player(name="Aragorn", race="DUNADAN", character_class="RANGER")

    expected_name = "Aragorn"
    expected_experience = 0
    expected_level = 1

    assert player.player_name == "Aragorn", f"Expected character name to be {expected_name}, but got {player.player_name}."
    assert player.experience == 0, f"Expected experience to be {expected_experience}, but got {player.experience}."
    assert player.level == 1, f"Expected level to be {expected_level}, but got {player.level}."
    assert player.archetype.health_die == '1d10'
    assert player.archetype.magic_die == '1d8'