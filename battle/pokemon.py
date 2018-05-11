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
    status = "Healthy"
    item = None

    def __init__(self, species, stats, hp, status):
        """
        Constructor sets the species of the pokemon.
        The species is used to populate pokemon type.
        :param species:     The name of the Pokemon species.
        :param stats:       A dictionary of stats.
        """
        self.species = species
        self.stats = stats
        self.hp = hp
        self.status = status

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

    def get_stat(self, stat):
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

    def modify_stat(self, stat, modifier):
        """
        TODO: Hard code modifier words like "sharply/greatly" to appropriate levels.
        :param new_hp: Taken in form of a fraction (e.g. 76/100)
        :return: None
        """
        self.stats["hp"] = new_hp


class FriendlyPokemon(Pokemon):
    def __init__(self):
        pass


class EnemyPokemon(Pokemon):
    def __init__(self):
        pass
