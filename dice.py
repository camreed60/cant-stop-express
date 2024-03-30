"""PA dice exercise.

Name: Camndon Reed
Date: 3/19/2024
"""


import random


def roll_dice(num_dice=5, sides=0):
    """Roll a number of dice with a given seed.

    Args:
        num_dice (int) : the number of dice to be rolled
        sides (int) : the seed

    Returns:
        list_vals (list) : the results of each dice roll
    """
    list_vals = []
    if num_dice not in range(1, 11):
        list_vals.append(6)

    if sides is None:
        random.seed()
    else:
        random.seed(sides)

    if num_dice in range(1, 11):
        for i in range(num_dice):
            list_vals.append(random.randint(1, 6))
    return list_vals


def are_valid(results):
    """Check a returned list of dice for validity.

    Args:
        results (list) : the list of dice to be checked

    returns:
        bool : wether the list is valid or not
    """
    if results is None:
        return False

    if len(results) not in range(1, 11):
        return False
    for i in results:
        if i not in range(1, 7):
            return False
    return True
