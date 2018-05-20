from pokemonmove import calculate_damage
from battle.battleMovedex import get_category
from showdownNavigator.pokemon import Pokemon
from battle.battle import is_kill

class ExpectimaxAgent(MultiAgentSearchAgent):

    def get_action(self, gameState):
        depth = 2
        player_index = 0
        move = self.expectimax(gameState, depth, player_index)
        return move[0]

    def expectimax(self, game_state, depth, player_index):
        if player_index >= 2:
            player_index = 0
            depth += 1

        if depth == self.depth or game_state.isWin() or game_state.isLose():
            return self.evaluation_function(game_state)

        if player_index == 0:
            best_value = (-1*float('inf'), "")
            legal_actions = game_state.getLegalActions()
            listOfActions = []
            for action in legal_actions:
                min_value = (self.expectimax(game_state.generateSuccessor(action))[0], action)
                if type(min_value) is tuple:
                    min_value = min_value[0]
                new_value = max(best_value[0], min_value)
                if new_value is not best_value[0]:
                    best_value = (new_value, action)
            return best_value
        else:
            expValue = [0, ""]
            legal_actions = game_state.getLegalActions()
            probability = 1.0/float(len(legal_actions))
            for action in legal_actions:
                return_value = (self.expectimax(game_state.generateSuccessor(action))[0], action)
                if type(return_value) is tuple:
                    return_value = return_value[0]

                expValue[1] = action
                expValue[0] += return_value * probability

            return tuple(expValue)

    @staticmethod
    def evaluation_function(current_game_state, action):
        """
        :param current_game_state:
        :type action:       Move as a String or pokemon.Pokemon object
        :param action:      Can be a move or a pokemon to swtich to
        :rtype: integer
        :return: The utility value of the successor game state.
        """
        successor_game_state = current_game_state.generate_successor(action)
        current_pokemon = successor_game_state.get_active_pokemon()
        opposing_pokemon = successor_game_state.get_enemy_active_pokemon()

        if successor_game_state.is_win():
            return 99999
        if successor_game_state.is_lose():
            return -99999

        speed_evaluation = 0
        damage_evaluation = 0
        opposing_damage_evaluation = 0
        nondamageEvaluation = 0
        switch_evaluation = 0
        out_speed_check = False

        weight = 100

        # Check to see if we will be out sped by the opponent.
        speed = current_pokemon.get_stat("spe")
        opposing_speed = opposing_pokemon.get_stat("spe")
        if speed >= opposing_speed:  # evaluate speed
            speed_evaluation += weight
            out_speed_check = True
        else:
            speed_evaluation -= weight

        # megaEvolution
        mega_check = current_pokemon.item[:-3] # check for "ite"
        whiteitem_check = current_pokemon.item[:5] # Not to accidentally get white apricon, white herb etc.
        if mega_check == "ite" and whiteitem_check != "white":
            # mega evolution if a move is selected rather than a switch, update the pokemon
            current_pokemon.species = current_pokemon.species + "mega"
            current_pokemon.calculate_stats()
            current_pokemon.set_ability()
            current_pokemon.set_type()

        # damageEvaluation
        if action in current_pokemon.moveset and get_category(action) == ("Special" or "Physical"):
            # need to adjust evaluation weight we out sped
            damage_evaluation += calculate_damage(current_pokemon, opposing_pokemon, action)
            # Checks if we're going first and adds a multiplier. If we're killing the opponent,
            # and we're outrunning, returns 99999.
            if out_speed_check:
                damage_evaluation *= 1.5  # need to adjust evaluation weight we outsped
                if is_kill(current_pokemon, opposing_pokemon, action):
                    return 99999

        # opposingDamageEvaluation
        highest_opposing_damage = 0
        highest_opposing_damage_move = ""
        for move in opposing_pokemon.moveset:  # calculate highest damaging move from opposingPokemon
            if get_category(move) == ("Special" or "Physical"):
                opposing_damage = calculate_damage(opposing_pokemon, current_pokemon, move)
                if opposing_damage > highest_opposing_damage:
                    highest_opposing_damage = opposing_damage
                    highest_opposing_damage_move = move
        opposing_damage_evaluation -= highest_opposing_damage
        if not out_speed_check:  # should give higher evaluation if we don't outSpeed opposingPokemon
            opposing_damage_evaluation *= 1.5
        # need to adjust evaluation weight we are outsped

        # non-damageCalculation goes here

        # switchEvaluation
        if type(action) is Pokemon:
            current_pokemon = action
            calculate_damage(opposing_pokemon, current_pokemon, highest_opposing_damage_move)
            # need to get pokemonClass given string pokemonName from action
            switch_evaluation += weight

        return speed_evaluation + damage_evaluation + opposing_damage_evaluation
