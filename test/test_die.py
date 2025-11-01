from unittest.mock import patch, call
import pytest
from core.die import Die, InvalidDieExpression

@patch('core.die.random.randint')
def test_die_roll_fixed(mock_randint):
    mock_randint.side_effect = [3, 4, 5, 6] # simulated 4d6 roll
    total, rolls = Die.roll("4d6")

    assert rolls == [3, 4, 5, 6]
    assert total == 18

@patch('core.die.random.randint')
def test_die_roll_invalid(mock_randint):
    with pytest.raises(ValueError):
        Die.roll('abcd')
    with pytest.raises(ValueError):
        Die.roll('4x6')
    with pytest.raises(ValueError):
        Die.roll('d6')
    with pytest.raises(ValueError):
        Die.roll('6')

@patch('core.die.random.randint')
def test_die_roll_invalid_numbers(mock_randint):
    # zero or negative dice/sides raise InvalidDieExpression
    with pytest.raises(InvalidDieExpression):
        Die.roll("0d6")
    with pytest.raises(InvalidDieExpression):
        Die.roll("4d0")
    with pytest.raises(InvalidDieExpression):
        Die.roll("-1d6")
    with pytest.raises(InvalidDieExpression):
        Die.roll("4d-6")

@patch('core.die.random.randint')
def test_die_roll_minimum_value_respected(mock_randint):
    mock_randint.side_effect = [3, 3, 3]
    total, rolls = Die.roll("3d6", minimum_value=3)

    assert rolls == [3, 3, 3]
    assert total == 9
    assert mock_randint.call_count == 3
    assert mock_randint.call_args_list == [call(3, 6), call(3, 6), call(3, 6)]