"""
Tests for the core.die.Die.roll function.

These unit tests verify:
- deterministic behavior when randint is patched,
- handling of invalid die expressions,
- validation of zero/negative dice and sides,
- respect for the `minimum_value` parameter when rolling.
"""
from unittest.mock import patch, call
import pytest
from core.die import Die, InvalidDieExpression

@patch('core.die.random.randint')
def test_die_roll_fixed(mock_randint):
    """Ensure Die.roll returns the expected total and list of individual rolls
    when the RNG is patched to return a fixed sequence (simulates a 4d6 roll)."""
    mock_randint.side_effect = [3, 4, 5, 6] # simulated 4d6 roll
    total, rolls = Die.roll("4d6")

    assert rolls == [3, 4, 5, 6]
    assert total == 18

@patch('core.die.random.randint')
def test_die_roll_invalid(mock_randint):
    """Verify that malformed die expressions raise ValueError."""
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
    """Ensure expressions with zero or negative dice/sides raise InvalidDieExpression."""
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
    """Check that the minimum_value parameter is passed through to randint and
    that the correct number of calls and argument lists are used."""
    mock_randint.side_effect = [3, 3, 3]
    total, rolls = Die.roll("3d6", minimum_value=3)

    assert rolls == [3, 3, 3]
    assert total == 9
    assert mock_randint.call_count == 3
    assert mock_randint.call_args_list == [call(3, 6), call(3, 6), call(3, 6)]