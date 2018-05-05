class Pokemon:
    def __init__(self, species=None):
        # Stats
        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.special_attack = 0
        self.special_defense = 0
        self.speed = 0
        self.level = 0
        # Species
        self.species = species
        # Item
        self.item = None
        # Pokemon types. Initialize to none for mono typed pokemon
        self.type_1 = None
        self.type_2 = None

    def get_hp(self):
        return self.hp

    def set_hp(self, hp):
        self.hp = hp

    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack

    def get_defense(self):
        return self.defense

    def set_defense(self, defense):
        self.defense = defense

    def get_special_attack(self):
        return self.special_attack

    def set_special_attack(self, special_attack):
        self.special_attack= special_attack

    def get_special_defense(self):
        return self.special_defense

    def set_special_defense(self, special_defense):
        self.special_defense = special_defense

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed= speed

    def get_type(self):
        types = list()
        types.append(self.type1)
        types.append(self.type2)
        return types

    def set_type(self, type_1, type_2=None):
        self.type_1 = type_1
        self.type_2 = type_2

    def get_species(self):
        return self.species

    def set_species(self, species):
        self.species = species


class FriendlyPokemon(Pokemon):
    def __init__(self):
        pass


class EnemyPokemon(Pokemon):
    def __init__(self):
        pass
