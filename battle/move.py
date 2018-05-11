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
    modifier = 0
    burnMod = 1
    typeAdvantageMod = 1
    weatherMod = 1
    stabMod = 1
    attack = 1
    oppDefense = 1
    power = self.base_power
    moveAttr = self.is_physical
    # damage = ((((2 * attacker.level) / 5 ) * Move.base_power * attacker.attack/defender.defense) / 50) + 2) * modifier

    #Check if we need to use attack/defense or spAtt/spDef for damage calculation depending on move attribute
    if moveAttr == True:
        attack = attacker.attack
        oppDefense = defender.defense

        #If there is a burn effect in play, adjust the modifier for the attacker
        #if burn:
            #burnMod = 0.5
    else:
        attack = attacker.special_attack
        oppDefense = defender.special_defense

    #Check for move type advantage and adjust the modifier if needed
    defendingTypes = defender.type
    moveType = "normal" #arbritrary value until we have a function to fill in the move type
    modifiers = []
    for defType in defendingTypes:
        modifiers.append(damage_multipliers.get(moveType).get(defType, 1))
    typeAdvantageMod = modifiers[0] * modifiers[1]

    #Check if there is STAB needs to be accounted for and adjust the stat value used
    attackerTypes = attacker.type
    for attType in attackerTypes:
        if attType == moveType:
            stabMod = 1.5

    #Check if weather will increase/decrease/not effect move power
    if weather != None:
        if weather == "harsh sunlight" && moveType == "fire":
            weatherMod = 1.5

        else if weather == "harsh sunlight" && moveType == "water":
            weatherMod = 0.5

        if weather == "rain" && moveType == "water":
            weatherMod = 1.5

        else if weather == "rain" && moveType == "fire":
            weatherMod = 0.5

    #Calculate actual Stat values based on EVs and IVs
    attack = (((attack + 31)*2 + ((85**0.5)/4)*attacker.level)/100) + 5
    oppDefense = (((oppDefense + 31)*2 + ((85**0.5)/4)*defender.level)/100) + 5

    #Calculate the modifier
    modifier = weatherMod * stabMod * typeAdvantageMod * burnMod

    damage = ((((2 * attacker.level) / 5 ) * Move.base_power * attacker.attack/defender.defense) / 50) + 2) * modifier

    return damage
