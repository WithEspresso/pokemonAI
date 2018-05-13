from battle.pokemonmove import calculate_damage
from battle.battleMovedex import is_attack
from showdownNavigator.pokemon import Pokemon


class GameState:
    player = None

    friendly_team = list()
    enemy_team = list()

    active_pokemon = None
    enemy_active_pokemon = None

    remaining_pokemon = 6
    enemy_remaining_pokemon = 6

    weather = None

    def __init__(self, friendly_team, enemy_team, active_pokemon, enemy_active_pokemon):
        self.friendly_team = friendly_team
        self.enemy_team = enemy_team
        self.active_pokemon = active_pokemon
        self.enemy_active_pokemon = enemy_active_pokemon
        for poke in friendly_team:
            if poke.get_status() is not "fnt":
                self.remaining_pokemon += 1
        for poke in enemy_team:
            if poke.get_status() is not "fnt":
                self.enemy_remaining_pokemon += 1

    def is_win(self):
        """
        Win condition where all enemy pokemon have fainted
        :return: True if all enemy pokemon have fainted, false otherwise.
        """
        if self.enemy_remaining_pokemon == 0:
            return True
        return False

    def is_lose(self):
        """
        Lose condition where all of the player's pokemon have fainted
        :return: True if all player pokemon have fainted, false otherwise
        """
        if self.remaining_pokemon == 0:
            return True
        return False

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
