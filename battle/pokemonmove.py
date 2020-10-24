from battle import battleMovedex
from battle import PokemonTypes


def calculate_damage(attacker, defender, move, weather=None):
    """
    Calculates the potential damage to be done.
    :param attacker:    The attacking pokemon
    :param defender:    The defending pokemon
    :param move:        The move to calculate damage for as a String
    :param weather:     Current weather conditions
    :return:            The total damage done
    """
    burn_modifier = 1
    stab_multiplier = 1.0
    weather_mod = 1
    attack = 1
    opp_defense = 1

    category = battleMovedex.get_category(move)
    base_power = battleMovedex.get_base_power(move)
    move_type = battleMovedex.get_type(move)

    # Not implemented here, leaving for convenience.
    """
    accuracy = battleMovedex.get_accuracy(move)
    secondary = battleMovedex.get_secondary(move)
    boosts = battleMovedex.get_boosts(move)
    """

    # damage = ((((2 * attacker.level) / 5 ) * Move.base_power * attacker.attack/defender.defense) / 50) + 2) * modifier

    # Check if we need to use attack/defense or spAtt/spDef for damage calculation depending on move attribute
    if category == "Physical":
        attack = int(attacker.get_stat("atk"))
        opp_defense = int(defender.get_stat("def"))
    if category == "Special":
        attack = int(attacker.get_stat("spa"))
        opp_defense = int(defender.get_stat("spd"))
    if category == "Status":
        # TODO: Implement evaluation function for status moves.
        print("Non attacking move. Damage will be zero. ")
        return 0

    # Gets the types as a list.
    defenders_types = defender.get_type()
    attacker_types = attacker.get_type()

    # Calculate type advantage multiplier.
    type_advantage_multiplier = PokemonTypes.get_multiplier(move_type, defenders_types)

    # Check if there is STAB needs to be accounted for and adjust the stat value used
    for attacker_type in attacker_types:
        if attacker_type == move_type:
            stab_multiplier = 1.5

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
    # attack = (((attack + 31.0)*2 + ((85.0 ** 0.5) / 4.0) * attacker.level) / 100) + 5
    # opp_defense = (((opp_defense + 31.0) * 2.0 + ((85.0 ** 0.5) / 4) * defender.level) / 100) + 5

    # Calculate burn modifier
    if category == "Physical" and attacker.get_status() == "burn":
        burn_modifier = 0.5

    # Calculate the modifier
    modifier = weather_mod * stab_multiplier * type_advantage_multiplier * burn_modifier

    # Calculate damage, truncate any digits following the decimal.
    damage = (((((2.0 * int(attacker.level)) / 5) * int(base_power) * attack/opp_defense) / 50.0) + 2.0) * modifier
    damage = round(damage, 0)

    return damage
