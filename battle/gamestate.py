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
        pass

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
        # If the move is an attack, update the active pokemon's status.
        if is_attack(action) and player == self.player:
            damage_done = calculate_damage(self.active_pokemon, self.enemy_active_pokemon, action)
            previous_hp = self.enemy_active_pokemon.get_hp().split('/')[0]
            max_hp = self.enemy_active_pokemon.get_hp().split('/')[1]
            new_hp = previous_hp - damage_done
            if new_hp <= 0:
                self.enemy_active_pokemon.status = "fnt"
                self.enemy_active_pokemon.take_damage(0)
            else:
                self.enemy_active_pokemon.take_damage(str(new_hp) + "/" + str(max_hp))
        # If the move is a switch, update the active pokemon's status.
        else:
            if player == self.player and target is not None:
                self.active_pokemon = target




    def get_legal_actions(self):
        pass
