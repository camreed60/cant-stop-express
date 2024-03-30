"""Cantstopx.py this will play the game Can't Stop Express.

@author: Camndon Reed
@version: 3-27-24
"""
import dice

# Quantity under 4  = -200 5 = 0, over 5 = n-5 * scoring factor
# .                 0 .  1 . 2 . 3 . 4 . 5 . 6 . 7 . 8   9   10
# Map of scoring to numbers
# SCORING_FACTOR = [100, 70, 60, 50, 40, 30, 40, 50, 60, 70, 100]
# NUMBERS =        [2,    3,  4,  5,  6,  7,  8,  9, 10, 11,  12]
SCORING_FACTOR = [100, 70, 60, 50, 40, 30, 40, 50, 60, 70, 100]
NUMBERS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Number of dice matches to reach to start positive scoring
SCORE_COUNT = 5
# Max number of dice total count for a row.
SCORE_COUNT_MAX = 10
# Number at which we end the game when one of the
# 5th dice hits this count.  Real game is 8.
FIFTH_MAX = 8
# Count max items - for first and second keepers,ie 11225 max 2 pairs.
COUNT_MAX = 2


def set_fifth_die(fifth_dice, rolls, die_value, fifth_count, rnd):   
    """Set fifth dice and return status.

    Details fifth dice element adjusted or new if one was added.
    This takes in the given parameters to determine what fifth dice value was
    added(first time should return a string-init as in intial.) or which
    count was added to(if fifth_dice were 1, 5, 2 and you added another 2 then
    adjust the first count[2] to be one more than it was) The return status
    string should be first - third to indicate which element was
    then add a -init if this is a new entry(ie. round 1-3), else invalid call.

    Args:
        fifth_dice(list): fifth dice values
        rolls(list): list of rolls
        die_value(int): current die working with.
        fifth_count(list): 3 counts of fifth dice.
        rnd(int): round of game

    Returns:
        status(str): String status applied: new, first, second or third.
    """
    if fifth_dice is None or fifth_count is None or rolls is None or die_value is None:
        return "invalid call"
    if rnd is None:
        return "invalid call"
    if len(fifth_dice) != 3 or len(fifth_count) != 3:
        return "invalid call"
    if min(fifth_count) < 0 or (min(fifth_dice) < 0):
        return "invalid call"

    if fifth_dice.count(0) > 0:
        if die_value in fifth_dice:
            return "invalid call"
        else:
            if fifth_dice[0] == 0:
                fifth_dice[0] = die_value 
                fifth_count[0] += 1
                return "first-init"
            elif fifth_dice[1] == 0:
                fifth_dice[1] = die_value
                fifth_count[1] += 1
                return "second-init"
            elif fifth_dice[2] == 0:
                fifth_dice[2] = die_value
                fifth_count[2] += 1
                return "third-init"         
    else:
        if die_value not in fifth_dice:
            return "invalid call"
        for i, val in enumerate(fifth_dice):
            if val == die_value:
                fifth_count[i] += 1
                return ["first", "second", "third"][i]
    return "invalid call"
        

def valid_keeper_format(keep_string):  
    """Check for 1.1.2.2.5 format in input.

    You must have 2 ones, 2 twos, 1 five and 4 periods delimiting the choice.
    The periods must be used as delimiters.

    Args:
        keep_string(str): input string for validation

    Returns:
        valid_format(bool): True if valid, False otherwise.
    """
    valid_format = True
    if len(keep_string) != 9:
        valid_format = False
    elif keep_string.count("1") != 2 or keep_string.count("2") != 2:
        valid_format = False
    elif keep_string.count("5") != 1 or keep_string.count(".") != 4:
        valid_format = False
    for i in keep_string:
        if (keep_string.index(i) % 2) != 0:
            if i != ".":
                valid_format = False
    return valid_format


def validate_keepers(rnd, keepers, rolls, counts, fifth_counts, fifth_dice):
    """Check keepers for valid keepers based on other rules.

    For round 1-3 keepers must be unique, then must use an existing
    one for rounds after 3. Returns should be a set with the first element
    a boolean if the keepers are invalid(True) or valid(False) as we
    are using these for validation, then the second element of the return
    will be a String message for the
    Error type:
    1) Keeper must be unique in round 1-3:if the keeper is not unique and round < 4
    2) You must select a fifth dice in the list: if if the round > 3 and the player
    tried to select a non-existing keeper and could select and existing one.
    3) Fifth Max Reached: if the max value of fifth count has been exceeded.
    4) Valid Roll: if the roll is valid.
    5) Nothing - Any other case / default case

    Args:
        rnd(int): round number
        keepers(list): list of keeper selections
        rolls(list): dice rolled
        counts(list): dice value counts
        fifth_counts(list): counts for fifth dice
        fifth_dice(list): values of fifth dice.

    Returns:
        invalidation(bool): True if invalid, False otherwise.
        msg(str): String message for error you are seeing.
    """
    if rnd < 4:
        if rolls[keepers.index("5")] in fifth_dice: 
            return True, "Keeper must be unique in round 1-3" 
    else:
        if rolls[keepers.index("5")] not in fifth_dice:
            return True, "You must select a fifth dice in the list"
    for i in fifth_counts:
        if i >= 8:
            return True, "Fifth Max Reached"
    return False, "Valid Roll"
    

def get_keepers(rnd, rolls, counts, fifth_counts, fifth_dice):
    """Get input of keeper values and continue until valid.

    This will return a list like: [1, 1, 2, 2, 5].
    You must continue prompting the user to:
    "Choose a valid set of dice to keep(i.e. 1.1.2.2.5): "
    until a valid set of keepers has been entered.
    Hint: you should use the valid_keeper_format function to validate
    this.
    Then print to the user:
    Valid format for keepers:1.1.2.2.5
    where the data after the colon is the keeper string that the user entered.
    You should then call the validate_keepers function to validate that the
    selected keepers are valid.  Then print the message returned from validate_keepers
    If they are valid,  return these keepers as a list.
    i.e.[1, 1, 2, 2, 5] otherwise keep asking for keeper values until you get valid
    ones.
    
    Args:
        rnd(int): round number
        rolls(list): dice rolls
        counts(list): dice value counts
        fifth_counts(list): counts for fifth dice
        fifth_dice(list): values for fifth dice

    Returns:
        keepers(list): list of valid keepers to use in next step.
    """
    keepers_str = input("Choose a valid set of dice to keep(i.e. 1.1.2.2.5): ")
    while True:
        result = valid_keeper_format(keepers_str)
        if result is True:
            break
        else:
            keepers_str = input("Choose a valid set of dice to keep(i.e. 1.1.2.2.5): ")
    print(f"Valid format for keepers:{keepers_str}")
    keepers = keepers_str.split(".")  # Convert string to list
    print(validate_keepers(rnd, keepers, rolls, counts, fifth_counts, fifth_dice))
    return keepers


def score_keepers(rolls, keepers, counts, scores): 
    """Score keeper values into scores list.

    Scoring is as follows: if the counts for a number value 2-12
    is > SCORE_COUNT(5 for typical game) then score is the count above 5 times
    the scoring factor constant for that number value(see above constants)
    Note: If you have reached the scoring max you get no more points but can still
    select a number. If you have not reached the SCORE_COUNT -200 for any
    selected dice value.

    Args:
        rolls(list): list of dice rolls.
        keepers(list): keeper dice to score.
        counts(list): counts of dice rolled.
        scores(list): list of scores for nums 2-12.

    Returns:
        scored(tuple): first pair total, second pair total, fifth dice face value
    """
    first_pair = 0
    second_pair = 0
    fifth_dice = 0
    for i, val in enumerate(keepers):
        if val == "1":
            first_pair += rolls[i]
        elif val == "2":
            second_pair += rolls[i]
        else:
            fifth_dice = rolls[i]
    counts[first_pair - 2] += 1
    counts[second_pair - 2] += 1
    if counts[first_pair - 2] < 5:
        scores[first_pair - 2] = -200
    elif counts[first_pair] == 5:
        scores[first_pair - 2] = 0
    else:
        scores[first_pair - 2] = (counts[first_pair - 2] - 5) * SCORING_FACTOR[first_pair - 2]
    if counts[second_pair - 2] < 5:
        scores[second_pair - 2] = -200
    elif counts[second_pair] == 5:
        scores[second_pair - 2] = 0
    else:
        scores[second_pair - 2] = (counts[second_pair - 2] - 5) * SCORING_FACTOR[second_pair - 2]   
    return first_pair, second_pair, fifth_dice


def print_scoreboard(counts, scores, fifth_dice, fifth_count, rnd):
    """Print out the scoreboard after each round.

    Scoreboard has a header and should line up summary lines with header.
    See specification for layout of scoreboard.

    Args:
        counts(list): list of counts for dice values.
        scores(list): scores for each dice value.
        fifth_dice(list): list of fifth dice choices[1-3].
        fifth_count(list): count of fifth_dice elements.
        rnd(int): Round number

    Returns:
        scoreboard(str): string of scoreboard.
    """
    list_nums = [100, 70, 60, 50, 40, 30, 40, 50, 60, 70, 100]
    scoreboard = f"POINTS |  #  | COUNT | SCORE - Round:{rnd}\n"
    for i in range(2, 13):
        scoreboard += f" {list_nums[i-2]:4}    {i:2} {counts[i-2]:5}   {scores[i-2]:5}\n"
    scoreboard += "FIFTH DICE/COUNT:\n"
    for i in range(2):
        scoreboard += f"{fifth_dice[i]} {fifth_count[i]}\n"
    scoreboard += f"{fifth_dice[2]} {fifth_count[2]}"
    return scoreboard


def play_game():
    """Play the game of Can't Stop Express."""
    # DO NOT EDIT THIS FUNCTION
    # Initialize Variables for each new game
    playing = True
    rnd = 0
    fifth_dice = [0, 0, 0]
    fifth_count = [0, 0, 0]
    # Setup Counts and scores
    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print("CAN\'T STOP EXPRESS:\n")
    board = print_scoreboard(counts, scores, fifth_dice, fifth_count, rnd)
    print(board)
    while playing:
        rnd += 1
        rolls = dice.roll_dice()
        print("You rolled:\n", rolls)
        keepers = get_keepers(rnd, rolls, counts, fifth_count, fifth_dice)
        scored = score_keepers(rolls, keepers, counts, scores)
        print("You kept:", scored)
        # print("***: ", scored[2])
        fifth_die = set_fifth_die(fifth_dice, rolls,
                                  int(scored[2]), fifth_count, rnd)
        print("Fifth die:", fifth_die)
        # board = print_scoreboard(rolls, counts, scores,
        # fifth_dice, fifth_count)
        # print(board)
        # End of loop determination if any fifth
        # die counts are up to the FIFTH_MAX.
        # Determine if we want to keep playing or does it end.
        playing = (fifth_count[0] < FIFTH_MAX and
                   fifth_count[1] < FIFTH_MAX and
                   fifth_count[2] < FIFTH_MAX)
        # End in one round for testing:   playing = False
        board = print_scoreboard(counts, scores, fifth_dice, fifth_count, rnd)
        print(board)
        print("Total score: ", sum(scores))
    print("-----")


play_game()
    