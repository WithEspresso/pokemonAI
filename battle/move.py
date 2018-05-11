from PokemonTypes import *


class Move:
    """
    Data structure for information about a Pokemon move
    used for damage calculation.
    """
    def __init__(self):
        """
        Constructor for the move with default values.
        """
        self.is_physical = True     # For special moves, this field is false.
        self.base_power = 80        # Base power is used for damage calcu
        self.accuracy = 1.00        # 1.00 is 100% accuracy
        self.secondary = None       # Burn, paralysis, etc.

    def get_base_power(self):
        return self.base_power

    def get_accuracy(self):
        return self.accuracy

    def get_secondary(self):
        return self.secondary


def calculate_damage(attacker, defender, move, weather=None):
    """
    Calculates the potential damage to be done.
    :param attacker:    The attacking pokemon
    :param defender:    The defending pokemon
    :param move:        The move to calculate damage for
    :param weather:     Current weather conditions
    :return:            The total damage done
    """
    modifier = 1
    burn_mod = 1
    type_advantage_mod = 1
    weather_mod = 1
    stab_mod = 1
    attack = 1
    opp_defense = 1
    power = move.base_power
    # damage = ((((2 * attacker.level) / 5 ) * Move.base_power * attacker.attack/defender.defense) / 50) + 2) * modifier

    # Check if we need to use attack/defense or spAtt/spDef for damage calculation depending on move attribute
    if move.is_physical:
        attack = attacker.attack
        opp_defense = defender.defense

        # If there is a burn effect in play, adjust the modifier for the attacker
        # if burn:
        # burnMod = 0.5
    else:
        attack = attacker.special_attack
        opp_defense = defender.special_defense

    # Check for move type advantage and adjust the modifier if needed
    defending_types = defender.type
    move_type = "normal" # arbritrary value until we have a function to fill in the move type
    modifiers = []
    for defType in defending_types:
        modifiers.append(PokemonTypes.damage_multipliers.get(move_type).get(defType, 1))
    type_advantage_mod = modifiers[0] * modifiers[1]

    # Check if there is STAB needs to be accounted for and adjust the stat value used
    attacker_types = attacker.type
    for attType in attacker_types:
        if attType == move_type:
            stab_mod = 1.5

    # Check if weather will increase/decrease/not effect move power
    if weather is not None:
        if weather == "harsh sunlight" and move_type == "fire":
            weather_mod = 1.5

        elif weather == "harsh sunlight" and move_type == "water":
            weather_mod = 0.5

        if weather == "rain" and move_type == "water":
            weather_mod = 1.5

        elif weather == "rain" and move_type == "fire":
            weather_mod = 0.5

    # Calculate actual Stat values based on EVs and IVs
    attack = (((attack + 31)*2 + ((85**0.5)/4)*attacker.level)/100) + 5
    opp_defense = (((opp_defense + 31)*2 + ((85**0.5)/4)*defender.level)/100) + 5

    # Calculate the modifier
    modifier = weather_mod * stab_mod * type_advantage_mod * burn_mod

    damage = (((((2 * attacker.level) / 5 ) * Move.base_power * attack/opp_defense) / 50) + 2) * modifier

    return damage
