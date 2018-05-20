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

    def __init__(self, friendly_team, enemy_active_pokemon, enemy_player):
        self.friendly_team = friendly_team
        self.enemy_active_pokemon = enemy_active_pokemon
        self.enemy_player = enemy_player

        self.active_pokemon = friendly_team[0]
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

    def count_living_pokemon(self):
        for poke in self.friendly_team:
            if poke.get_status() is not "fnt":
                self.remaining_pokemon += 1
        return self.remaining_pokemon

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

    def generate_successor(self, action, player, target=None):
        # Copy the values from the current game state.
        successor = GameState(friendly_team=self.friendly_team,
                              enemy_team=self.enemy_team,
                              active_pokemon=self.active_pokemon,
                              enemy_active_pokemon=self.enemy_active_pokemon)

        # If the move is an attack, update the active pokemon's status.
        if is_attack(action) and player == self.player:
            damage_done = calculate_damage(successor.active_pokemon, successor.enemy_active_pokemon, action)
            previous_hp = successor.enemy_active_pokemon.get_hp().split('/')[0]
            max_hp = successor.enemy_active_pokemon.get_hp().split('/')[1]
            new_hp = previous_hp - damage_done

            if new_hp <= 0:
                successor.enemy_active_pokemon.status = "fnt"
                successor.enemy_active_pokemon.take_damage(0)
                successor.enemy_remaining_pokemon = successor.enemy_remaining_pokemon - 1
            else:
                successor.enemy_active_pokemon.take_damage(str(new_hp) + "/" + str(max_hp))
        # If the move is a switch, update the active pokemon's status.
        else:
            if player == successor.player and target is not None:
                successor.active_pokemon = target
        # Return the successor game state.
        return successor

    def get_legal_actions(self):
        pass

    def get_legal_switches(self):
        """
        Returns a list of indices of legal switches.
        :return:
        """
        legal_switches = list()
        for i in range(0, 6):
            pokemon = self.friendly_team[i]
            if pokemon.status is not "fnt" and pokemon.hp is not 0:
                if self.active_pokemon.species is not pokemon.species:
                    legal_switches.append(pokemon)
        return legal_switches


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
        return representation
















