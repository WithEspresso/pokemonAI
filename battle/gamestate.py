from battle.pokemonmove import calculate_damage
from battle.battleMovedex import is_attack
from showdownNavigator.pokemon import Pokemon


class GameState:

    friendly_team = list()
    enemy_team = list()

    active_pokemon = None
    enemy_active_pokemon = None

    remaining_pokemon = 6
    enemy_remaining_pokemon = 6

    enemy_player = "p2a"

    weather = None

    legal_actions = list()
    legal_moves = list()
    legal_switches = list()

    turn_number = 0

    def __init__(self, friendly_team, enemy_active_pokemon, enemy_player):
        self.friendly_team = friendly_team
        self.enemy_active_pokemon = enemy_active_pokemon
        self.enemy_player = enemy_player

        self.active_pokemon = friendly_team[0]

        # We only know what the enemy has shown us so far about their team.
        # If we haven't already seen their Pokemon, we add it to their team
        # in order to keep track of their team.
        if enemy_active_pokemon not in self.enemy_team:
            self.enemy_team.append(enemy_active_pokemon)

        for poke in friendly_team:
            self.remaining_pokemon = 0
            if poke.get_status() is not "fnt":
                self.remaining_pokemon += 1
        self.enemy_remaining_pokemon = 6

    def is_win(self):
        """
        Win condition where all enemy pokemon have fainted
        :return: True if all enemy pokemon have fainted, false otherwise.
        """
        if self.enemy_remaining_pokemon <= 0:
            return True
        return False

    def is_lose(self):
        """
        Lose condition where all of the player's pokemon have fainted
        :return: True if all player pokemon have fainted, false otherwise
        """
        if self.remaining_pokemon <= 0:
            return True
        return False

    @staticmethod
    def count_living_pokemon(team):
        remaining_pokemon = 0
        for poke in team:
            if poke.get_status() is not "fnt":
                remaining_pokemon += 1
        return remaining_pokemon

    def get_active_pokemon(self):
        """
        Returns the current active pokemon on the field.
        :return: The current active pokemon as a pokemon.Pokemon object
        """
        return self.active_pokemon

    def get_enemy_active_pokemon(self):
        """
        Returns the current active enemy on the field.
        :return: The current active pokemon as a pokemon.Pokemon object
        """
        return self.enemy_active_pokemon

    def set_active_pokemon(self, active_pokemon):
        """
        Returns the current active pokemon on the field.
        :return: The current active pokemon as a pokemon.Pokemon object
        """
        self.active_pokemon = active_pokemon

    def set_enemy_active_pokemon(self, enemy_active_pokemon):
        """
        Returns the current active enemy on the field.
        :return: The current active pokemon as a pokemon.Pokemon object
        """
        self.enemy_active_pokemon = enemy_active_pokemon

    def set_team(self, team):
        self.friendly_team = team
        self.active_pokemon = team[0]
        self.remaining_pokemon = self.count_living_pokemon(team)

    def set_enemy_team(self, team):
        self.enemy_team = team

    def set_enemy_player(self, enemy):
        """
        Set the enemy to p1a: or p2a: in order to process the console log.
        :param      enemy:
        :return:    None
        """
        self.enemy_player = enemy

    def get_enemy_player(self):
        return self.enemy_player

    def set_weather(self, weather):
        self.weather = weather

    def generate_successor(self, action):
        """
        The action is a legal action that may be a move or a Pokemon.
        :param action:
        :return:
        """
        # Copy the values from the current game state.
        successor = GameState(friendly_team=self.friendly_team,
                              enemy_active_pokemon=self.enemy_active_pokemon,
                              enemy_player=self.enemy_player)
        successor.enemy_remaining_pokemon = self.enemy_remaining_pokemon
        successor.weather = self.weather
        successor.turn_number = self.turn_number + 1

        # If the move is an attack, update the active pokemon's status.
        if is_attack(action):
            print("Generating successor state for attacking action: " + action)
            enemy_pokemon = successor.get_enemy_active_pokemon()
            active_pokemon = successor.get_active_pokemon()
            damage_done = calculate_damage(active_pokemon, enemy_pokemon, action)
            enemy_hp = enemy_pokemon.hp
            if type(enemy_hp) is str:
                enemy_hp = int(enemy_pokemon.get_hp())
            previous_hp = enemy_hp
            max_hp = successor.enemy_active_pokemon.get_stat("hp")
            new_hp = int(previous_hp) - int(damage_done)
            if new_hp <= 0:
                successor.enemy_active_pokemon.status = "fnt"
                successor.enemy_active_pokemon.take_damage(0)
                successor.enemy_remaining_pokemon = successor.enemy_remaining_pokemon - 1
            else:
                successor.enemy_active_pokemon.take_damage(str(new_hp) + "/" + str(max_hp))
        # If the move is a switch, update the active pokemon's status.
        elif type(action) is Pokemon:
            print("Generating successor state for switch: " + action.species)
            successor.active_pokemon = action
        # Return the successor game state.
        return successor

    def get_legal_actions(self):
        """
        Returns a list of legal moves to do and legal
        pokemon to switch to.
        :return:
        """
        self.legal_actions.clear()
        legal_switches = self.get_legal_switches()
        for pokemon in legal_switches:
            self.legal_actions.append(pokemon)
        legal_moves = self.get_legal_moves()
        for move in legal_moves:
            self.legal_actions.append(move)
        return self.legal_actions

    def get_legal_moves(self):
        return self.legal_moves

    def set_legal_moves(self, legal_moves):
        self.legal_moves = legal_moves

    def set_legal_switches(self, legal_switches):
        """
        Converts legal switches of String species names
        into matching Pokemon objects
        :param legal_switches:
        :return:
        """
        self.legal_switches.clear()
        for switch in legal_switches:
            for pokemon in self.friendly_team:
                if switch == pokemon.species:
                    self.legal_switches.append(pokemon)

    def get_legal_switches(self):
        return self.legal_switches

    def __str__(self):
        """
        String representation of the game state.
        :return: String
        """
        representation = "Team is: "
        for pokemon in self.friendly_team:
            representation += (str(pokemon) + " ")
        representation += "\n Enemy team is: "
        for pokemon in self.enemy_team:
            representation += (str(pokemon) + " ")
        representation += "\n Active pokemon is: \n" + str(self.active_pokemon)
        representation += "\n Enemy active pokemon is: \n" + str(self.enemy_active_pokemon)
        representation += "\n Enemy is player: " + str(self.enemy_player)
        return str(representation)

















