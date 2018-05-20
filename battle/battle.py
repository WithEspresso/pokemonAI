from battle.pokemonmove import calculate_damage
from showdownNavigator.pokewebdriver import ShowdownDriver


def get_index_of_best_move(attacking, defending, web=None, weather=None):
    """
    Returns the index of the best damaging move.
    :param attacking:   The attacking pokemon.
    :param defending:   The defending pokemon.
    :return:    The index of the best damaging move as an integer.
    """
    moveset = None
    if web is not None:
        moveset = web.get_moves()
        print("Moveset is: " + str(moveset))
    else:
        moveset = attacking.get_moveset()
    best_move = None
    best_damage = 0
    best_index = -1
    index = 0
    for move in moveset:
        damage = calculate_damage(attacking, defending, move)
        print(str(move) + " will do " + str(damage))
        if damage > best_damage:
            best_damage = damage
            best_move = move
            best_index = index
        index += 1
    print("Best move is: " + str(best_move))
    return best_index


def calculate_best_damage(attacking, defending, web=None, weather=None):
    """
    Returns the index of the best damaging move.
    :param attacking:   The attacking pokemon.
    :param defending:   The defending pokemon.
    :return:    The index of the best damaging move as an integer.
    """
    moveset = None
    # Case where the attacking Pokemon is on our side.
    if web is not None:
        moveset = web.get_moves()
        print("Moveset is: " + str(moveset))
    # Case where the opponent's pokemon is attacking.
    else:
        moveset = attacking.get_moveset()
    best_move = None
    best_damage = 0
    best_index = -1
    index = 0
    for move in moveset:
        damage = calculate_damage(attacking, defending, move)
        print(str(move) + " will do " + str(damage))
        if damage > best_damage:
            best_damage = damage
            best_move = move
            best_index = index
        index += 1
    print("Best move is: " + str(best_move))
    return best_damage


def calculate_best_utility(attacking, defending):
    """
    Figure out utility from other aspects of move.
    :param attacking:
    :param defending:
    :return:
    """


def is_kill(attacking, defending, move):
    """
    Returns true if the move will kill the defending Pokemon.
    :param attacking:
    :param defending:
    :param move:
    :return:
    """
    damage = calculate_damage(attacking, defending, move)
    defending_hp = defending.get_hp()
    if damage > defending_hp:
        return True
    return False
