from battle.formatsdata import *
from battle import pokedex
import math

IV = 31
EV = 86


class Pokemon:
    stats = {
            "atk": 0,
            "def": 0,
            "spatk": 0,
            "spdef": 0,
            "spd": 0
        }
    species = None
    type_1 = None
    type_2 = None

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
        self.species = species
        self.level = level
        self.hp = hp

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
        types = list()
        types.append(self.type1)
        types.append(self.type2)
        return types

    def set_type(self, type_1, type_2=None):
        """
        TODO: Retrieve Pokemon type from json file.
        :param type_1:
        :param type_2:
        :return:
        """
        self.type_1 = type_1
        self.type_2 = type_2

    def get_stat(self, stat=None):
        """
        Looks up the stat in the dictionary of stats and returns
        the result.
        :param stat: Valid stats are hp, atk, def, spatk, spdef, spd
        :return:
        """
        return self.stats.get(stat)

    def take_damage(self, new_hp):
        """
        Updates the current hp value to a new hp value.
        :param new_hp: Taken in form of a fraction (e.g. 76/100)
        :return: None
        """
        self.hp = new_hp

    def calculate_stats(self):
        """
        Called in the constructor when an enemy pokemon is given.
        Gets the stats from the pokedex and uses that
        :return:
        """
        base_stats = pokedex.get_base_stats(self.species)
        for key in self.stats:
            value = math.floor(((((base_stats.get("key") + IV) * 2 + (EV ** 0.5 / 4)) * self.level) / 100) + 5)
            self.stats[key] = value

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
        TODO: Hard code modifier words like "sharply/greatly" to appropriate levels.
        :param new_hp: Taken in form of a fraction (e.g. 76/100)
        :return: None
        """
        modified_stat = float(self.stats.get(stat)) * modifier
        self.stats[stat] = modified_stat

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
            + "\n\tMoves: " + str(self.moveset)

        return string_representation


class FriendlyPokemon(Pokemon):
    def __init__(self):
        pass


class EnemyPokemon(Pokemon):
    def __init__(self):
        pass
