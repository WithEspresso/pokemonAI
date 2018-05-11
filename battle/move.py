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
    # damage = ((((2 * attacker.level) / 5 ) * Move.base_power * attacker.attack/defender.defense) / 50) + 2) * modifier
