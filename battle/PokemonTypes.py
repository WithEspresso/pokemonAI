"""
The dictionary name is the defender
The value in the dictionary is the attacker

"""

damage_multipliers = {
    "Normal": {
        "Fighting": 2.0,
        "Ghost": 0.0
    },
    "Fire": {
        "Fire": 0.5,
        "Water": 2.0,
        "Grass": 0.5,
        "Ground": 0.5,
        "Rock": 2.0,
        "Bug": 0.5,
        "Steel": 0.5,
        "Ice": 0.5,
        "Fairy": 0.5
    },
    "Water": {
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2.0,
        "Electric": 2.0,
        "Ice": 0.5,
        "Steel": 0.5,
    },
    "Electric": {
        "Electric": 0.5,
        "Flying": 0.5,
        "Ground": 2.0,
        "Steel": 0.5,
    },
    "Grass": {
        "Fire": 2.0,
        "Water": 0.5,
        "Grass": 0.5,
        "Electric": 0.5,
        "Ice": 2.0,
        "Flying": 2.0,
        "Poison": 2.0,
        "Ground": 0.5,
        "Bug": 2.0,
    },
    "Ice": {
        "Fire": 2.0,
        "Ice": 0.5,
        "Fighting": 2.0,
        "Rock": 2.0,
        "Steel": 2.0,
    },
    "Fighting": {
        "Flying": 2.0,
        "Rock": 0.5,
        "Bug": 0.5,
        "Psychic": 2.0,
        "Dark": 0.5,
        "Fairy": 2.0
    },
    "Poison": {
        "Grass": 0.5,
        "Fighting": 0.5,
        "Poison": 0.5,
        "Ground": 2.0,
        "Bug": 0.5,
        "Psychic": 2.0,
        "Fairy": 0.5
    },
    "Ground": {
        "Water": 2.0,
        "Grass": 2.0,
        "Electric": 0.0,
        "Ice": 2.0,
        "Poison": 0.5,
        "Rock": 0.5,
    },
    "Flying": {
        "Grass": 0.5,
        "Electric": 2.0,
        "Ice": 2.0,
        "Fighting": 0.5,
        "Ground": 0.0,
        "Rock": 2.0,
        "Bug": 0.5,
    },
    "Psychic": {
        "Fighting": 0.5,
        "Bug": 2.0,
        "Ghost": 2.0,
        "Psychic": 0.5,
        "Dark": 2.0
    },
    "Bug": {
        "Fire": 2.0,
        "Grass": 0.5,
        "Fighting": 0.5,
        "Flying": 2.0,
        "Ground": 0.5,
        "Rock": 2.0,
    },
    "Rock": {
        "Normal": 0.5,
        "Fire": 0.5,
        "Water": 2.0,
        "Grass": 2.0,
        "Fighting": 2.0,
        "Poison": 0.5,
        "Ground": 2.0,
        "Flying": 0.5,
        "Steel": 2.0,
    },
    "Ghost": {
        "Normal": 0.0,
        "Fighting": 0.0,
        "Poison": 0.5,
        "Bug": 0.5,
        "Ghost": 2.0,
        "Dark": 2.0
    },
    "Dragon": {
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 0.5,
        "Electric": 0.5,
        "Ice": 2.0,
        "Dragon": 2.0,
        "Fairy": 2.0
    },
    "Dark": {
        "Fighting": 2.0,
        "Bug": 2.0,
        "Ghost": 0.5,
        "Psychic": 0.0,
        "Dark": 0.5,
        "Fairy": 2.0
    },
    "Steel": {
        "Normal": 0.5,
        "Fire": 2.0,
        "Grass": 0.5,
        "Ice": 0.5,
        "Fighting": 2.0,
        "Poison": 0.0,
        "Ground": 2.0,
        "Flying": 0.5,
        "Rock": 0.5,
        "Bug": 0.5,
        "Steel": 0.5,
        "Psychic": 0.5,
        "Dragon": 0.5,
        "Fairy": 0.5
    },
    "Fairy": {
        "Fighting": 0.5,
        "Poison": 2.0,
        "Bug": 0.5,
        "Steel": 2.0,
        "Dragon": 0.0,
        "Dark": 0.5
    },
}


def get_multiplier(attacking_type, defending_types):
    """
    Returns the damage multiplier for the move.
    :param attacking_type:  The type of the move being used to attack with.
    :param defending_types: The types of the defending pokemon
    :return:    The damage multiplier.
    """
    total_multiplier = 1.0
    for defending_type in defending_types:
        multiplier = damage_multipliers.get(defending_type).get(attacking_type)
        # print(attacking_type + " attacking " + defending_type + "'s multiplier is " + str(multiplier))
        if multiplier is not None:
            total_multiplier = total_multiplier * multiplier
    return total_multiplier
