from battle import pokedex
from showdownNavigator.pokemon import Pokemon
from pokemonmove import calculate_damage
from battleMovedex import get_category
import copy


class MinimaxAgent:

    def __init__(self, depth=2):
        self.depth = depth

    def get_action(self, game_state):
        depth = self.depth
        return self.minimax(game_state, depth)
        # return the action
        
    def minimax(self, game_state, depth):
        if depth == 0 or game_state.is_win() or game_state.is_lose():
            return self.evaluation_function(game_state, 0)
            # returns the current score when win, lose
        legal_actions = game_state.get_legal_actions()
        # move1, move2, move3, move4, switch to 1-6(keep track of actual HP),
        # (z-move usage, mega evolution given check for proper items)
        list_of_actions = []
        for action in legal_actions:
            list_of_actions.append((self.minimax(game_state.generateSuccessor(action))[0], action))
            # recursive call until it returns tuple (score, action)
        return max(list_of_actions)
        # return best maximizing action for us, we already consider
        # the best minimizing action of our opponent within our evaluation function

    def evaluation_function(self, game_state, action):
        successor_game_state = game_state.generateSuccessor(action)
        current_pokemon = successor_game_state.get_active_pokemon()
        opposing_pokemon = successor_game_state.get_enemy_active_pokemon()
        speed = current_pokemon.get_stat("spe")
        opposing_speed = opposing_pokemon.get_stat("spe")

        speed_evaluation = 0
        damage_evaluation = 0
        opposing_damage_evaluation = 0
        nondamage_evaluation = 0
        switch_evaluation = 0

        # evaluate speed
        out_speed_check = False
        if speed >= opposing_speed:
            speed_evaluation += 100
            out_speed_check = True
        else:
            speed_evaluation -= 100
        
        # megaEvolution
        # All mega items end with "ite". Ceck for item ending in "ite"
        mega_check = current_pokemon.item[:-3]
        whiteitem_check = current_pokemon.item[:5] # Not to accidentally get white apricon, white herb etc.
        if mega_check == "ite" and whiteitem_check != "white":
            # Mega evolution if a move is selected rather than a switch, update the pokemon
            current_pokemon.species = current_pokemon.species + "mega"
            current_pokemon.calculate_stats()
            current_pokemon.set_ability()
            current_pokemon.set_type()

        # damageEvaluation
        # need to adjust evaluation weight we outsped
        if action in current_pokemon.get_moveset() and get_category(action) == ("Special" or "Physical"):
            damage_evaluation += calculate_damage(current_pokemon, opposing_pokemon, action)/100
            if out_speed_check is True:
                damage_evaluation *= 1.5  # need to adjust evaluation weight we outsped

        #  opposingDamageEvaluation
        highest_opposing_damage = 0
        highest_opposing_damage_move = self.get_highest_damaging_move(self, opposing_pokemon, current_pokemon)
        if highest_opposing_damage_move is not None:
            highest_opposing_damage = calculate_damage(opposing_pokemon, current_pokemon, highest_opposing_damage_move)
        opposing_damage_evaluation -= highest_opposing_damage/100
        if not out_speed_check:                 # should give higher evaluation if we don't outSpeed opposingPokemon
            opposing_damage_evaluation *= 1.5   # need to adjust evaluation weight we are outspeed

        # non-damageCalculation goes here

        # switchEvaluation
        """
        switchCheck = action[:8]
        switchDamage = 0
        if(action[:8] == "SwitchTo"):   # remember to properly index, i.e 0 = Pokemon1,
                                        # Switch prediction for highestOpposingDamageMove.
                                        # A sample swich action would be "SwitchToBulbasaur"
            pokemonName = action[8:]    # splice all but SwitchTo
            pokemonName.lower()         # pokemon switched to in lowercase
            switchDamage = calculate_damage(opposingPokemon, pokemonName, highest_opposing_damage_move)
                                        # need to get pokemonClass given string pokemonName from action
            switch_evaluation += switchDamage / 50
        """

        if type(action) is Pokemon:
            switched_pokemon = action
            if pokedex.check_name(action.species):
                highest_opposing_damage_move = self.get_highest_damaging_move(self, opposing_pokemon, current_pokemon)
                switch_damage = calculate_damage(opposing_pokemon, switched_pokemon, highest_opposing_damage_move)
                switch_evaluation += switch_damage
                
        return speed_evaluation + damage_evaluation + opposing_damage_evaluation + switch_evaluation

    @staticmethod
    def get_highest_damaging_move(self, attacker, defender):
        opposing_damage = 0
        highest_opposing_damage = 0
        highest_opposing_damage_move = None
        for move in attacker.moveset:   # calculate highest damaging move from opposingPokemon
            if get_category(move) == ("Special" or "Physical"):
                opposing_damage = calculate_damage(attacker, defender, move)
                if opposing_damage > highest_opposing_damage:
                    highest_opposing_damage = opposing_damage
                    highest_opposing_damage_move = move
        return highest_opposing_damage_move

