from battle.battleMovedex import *
from battle.PokemonTypes import *
from battle.pokemonmove import calculate_damage


def calculate_best_damaging_move(attacking, defending):
    """
    Returns the index of the best damaging move.
    :param attacking:   The attacking pokemon.
    :param defending:   The defending pokemon.
    :return:    The index of the best damaging move as an integer.
    """
    moveset = attacking.get_moveset()
    best_move = None
    best_damage = 0
    best_index = 0
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


def calculate_best_utility(attacking, defending):
    """
    Figure out utility from other aspects of move.
    :param attacking:
    :param defending:
    :return:
    """