'''Die Class:  How to handle rolling dice'''

import random

# This is the error type if someone requests a die in the wrong format.
class InvalidDieExpression(Exception):
    pass


# The Die class doesn't store any data, just has one method: roll.
#
# Usage:
# total, roll_history = Die.roll('3d6')
# 
# Example response:
# 12, (4,2,6)
class Die:
    @staticmethod
    def roll(short_string, minimum_value=1):
        try:
            num_dice, die_sides = map(int, short_string.lower().split('d'))
            if num_dice < 1 or die_sides < 1:
                raise InvalidDieExpression("Both the number of dice and number of sides must be at least 1.")
            rolls = [random.randint(minimum_value,die_sides) for _ in range(num_dice)]
            return sum(rolls), rolls
        except ValueError:
            raise ValueError("Input must be in XdY format, e.g. '3d20'.")