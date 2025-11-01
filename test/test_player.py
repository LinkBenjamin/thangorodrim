'''Test Suite for Player Class'''

import json
import os

from core.player import Player

ARAGORN_DATA_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'aragorn.json')

def test_player_init_from_file():
    '''A Player object may be initialized direct from a file, 
       such as in the case of a saved game being reloaded'''

    player = Player.from_file(ARAGORN_DATA_FILE)

    expected_name = "Aragorn"

    assert player.player_name == "Aragorn", f"Expected character name to be {expected_name}, but got {player.player_name}."


def test_auto_roller():
    '''A Player object may be initialized with a call to the
       constructor with the character's name, race, and class,
       and it will roll or calculate all the other values.'''
    
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