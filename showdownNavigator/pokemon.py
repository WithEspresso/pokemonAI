from battle.formatsdata import *
from battle import pokedex
import math

IV = 31
EV = 86

modifier_multiplier = {
    -6: round((3/9), 2),
    -5: round((4/9), 2),
    -4: round((5/9), 2),
    -3: round((6/9), 2),
    -2: round((7/9), 2),
    -1: round((8/9), 2),
    0: 1,
    1: round((4/9), 2),
    2: round((5/9), 2),
    3: round((6/9), 2),
    4: round((7/9), 2),
    5: round((8/9), 2),
    6: 3,
}


class Pokemon:
    stats = dict()

    # Dictionary of base stats.
    base_stats = {
        "hp": 0,
        "atk": 0,
        "def": 0,
        "spa": 0,
        "spd": 0,
        "spe": 0
    }

    # Dictionary of current modifiers for the stats.
    modifiers = {
        "hp": 0,
        "atk": 0,
        "def": 0,
        "spa": 0,
        "spd": 0,
        "spe": 0
    }

    species = None
    types = [None, None]

    hp = 0
    level = 0
    status = "Healthy"
    item = None
    ability = None
    moveset = None

    def __init__(self, species, level, hp, stats=None, status=None, item=None, ability=None, moveset=None):
        """
        Constructor sets the species of the pokemon.
        The species is used to populate pokemon type.
        :param species:     The name of the Pokemon species.
        :param stats:       A dictionary of stats.
        """

        self.species = species.lower()
        self.level = level
        self.hp = hp
        print("CREATING POKEMON WITH SPECIES: " + str(self.species))

        self.get_base_stats()
        self.set_type()

        # If these arguments are provided, it's a friendly Pokemon. If not, it's an
        # enemy poke and we're going to do a best guesstimate of their stats.
        if stats is None:
            self.calculate_stats()
        else:
            self.stats = stats
        if status is None:
            self.status = status
        else:
            self.status = "Healthy"
        if item is None:
            self.item = None
        else:
            self.item = item
        if ability is None:
            self.ability = self.get_ability()
        else:
            self.ability = ability
        if moveset is None:
            self.moveset = self.get_moveset()
        else:
            self.moveset = moveset

    def get_type(self):
        """
        Type retrieval for damage calc purposes.
        :return: types:     A list of the Pokemon's types.
        """
        return self.types

    def set_type(self):
        """
        :return:
        """
        self.types = pokedex.get_types(self.species)

    def get_stat(self, stat=None):
        """
        Looks up the stat in the dictionary of stats and returns
        the result.
        :param stat: Valid stats are hp, atk, def, spatk, spdef, spd
        :return:
        """
        return self.stats.get(stat)

    def get_hp(self):
        return self.hp.split('/')[0]

    def take_damage(self, new_hp):
        """
        Updates the current hp value to a new hp value.
        :param new_hp: Taken in form of a fraction (e.g. 76/100)
        :return: None
        """
        self.hp = new_hp

    def get_base_stats(self):
        self.base_stats = pokedex.get_base_stats(self.species)

    def calculate_stats(self):
        """
        Called in the constructor when an enemy pokemon is given.
        Gets the stats from the pokedex and uses that
        :return:
        """
        base_stats = pokedex.get_base_stats(self.species)
        print("Base stats are: ")
        print(base_stats)
        for key in base_stats:
            base_stat = base_stats.get(key)
            term = EV / 4.0
            numerator = (2.0 * base_stat + IV + term) * int(self.level)
            fraction = numerator / 100.0
            if key is not "hp":
                value = math.floor(fraction + 5)
            else:
                value = math.floor(fraction + self.level + 10)
            self.stats[key] = value
        for key in self.modifiers:
            multiplier = modifier_multiplier.get(self.modifiers.get(key))
            new_value = self.stats.get(key) * multiplier
            self.stats[key] = new_value
        self.calculate_hp()

    def calculate_hp(self):
        hp_as_fraction = self.hp.split('/')
        hp_as_percentage = float(hp_as_fraction[0]) / float(hp_as_fraction[1])
        current_hp = math.floor(self.get_stat("hp") * hp_as_percentage)
        self.hp = current_hp
        print("Current hp is: " + str(current_hp))

    def get_ability(self):
        """
        Called in the constructor when an enemy pokemon is given.
        Returns the first ability a pokemon has in its valid abilities
        dictionary.
        :return: Ability
        """
        return pokedex.get_abilities(self.species).get("0")

    def get_moveset(self):
        """
        Called in the constructor when an enemy pokemon is given.
        Returns the random generated moveset a pokemon can have.
        Note: It will be more than four moves unless it's Ditto.
        :return: A moveset list.
        """
        return get_random_battle_moveset(self.species)

    def modify_stat(self, stat, modifier):
        """
        Modifies a stat and calculates the new stats after modifiecation.
        :param stat:
        :param modifier:
        :return:
        """
        self.modifiers[stat] = modifier
        self.calculate_stats()

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def __str__(self):
        """
        Prints string representation of the Pokemon
        :return:    A string representation of the Pokemon
        """
        string_representation = "Pokemon: " + str(self.species) \
            + "\n\tLV: " + str(self.level)\
            + "\n\tHP: " + str(self.hp) \
            + "\n\tStats: " + str(self.stats) \
            + "\n\tStatus: " + str(self.status) \
            + "\n\tHeld Item: " + str(self.item) \
            + "\n\tAbility: " + str(self.ability) \
            + "\n\tMoves: " + str(self.moveset) \
            + "\n\tTypes: " + str(self.types)

        return string_representation
