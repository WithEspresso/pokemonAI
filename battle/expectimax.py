

class ExpectimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        depth = 2
        playerIndex = 0
        move = self.expectimax(gameState, depth, playerIndex)
        return move[0]

    def expectimax(self, gameState, depth, playerIndex):
        if playerIndex >= 2
            playerIndex = 0
            depth += 1

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), 0)

        if playerIndex == 0:
            bestValue = (-1*float('inf'), "")
            legalActions = gameState.getLegalActions()
            listOfActions = []

            for action in legalActions:
                minValue = (self.expectimax(gameState.generateSuccessor(action))[0], action)
                if type(minValue) is tuple:
                    minValue = minValue[0]
                newValue = max(bestValue[0], minValue)
                if newValue is not bestValue[0]:
                    bestValue = (newValue, action)

            return bestValue

        else:
            expValue = [0, ""]
            legalActions = gameState.getLegalActions()

            probability = 1.0/float(len(legalActions))
            for action in legalActions:
                returnValue = (self.expectimax(gameState.generateSuccessor(action))[0], action)
                if type(returnValue) is tuple:
                    returnValue = returnValue[0]

                expValue[1] = action
                expValue[0] += returnValue*probability

            return tuple(expValue)

    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generateSuccessor(action)
        speedEvaluation, damageEvaluation, opposingDamageEvaluation, nondamageEvaluation, switchEvaluation = 0
        outSpeedCheck = false
        if(currentPokemon.speed >= opposingPokemon.speed): #evaluate speed
			speedEvaluation += weight
			outSpeedCheck = True
        else:
			speedEvaluation -= weight

        #megaEvolution
		megaCheck = currentPokemon.item[:-3] #check for "ite"
		whiteitemCheck = currentPokemon.item[:5] #Not to accidentally get white apricon, white herb etc.
		if(megaCheck == "ite" and whiteitemCheck != "white"):	#mega evolution if a move is selected rather than a switch, update the pokemon
			currentPokemon.species = currentPokemon.species + "mega"
			currentPokemon.stats = pokedex[currentPokemon.species]["baseStats"]
			currentPokemon.ability = pokedex[currentPokemon.species]["abilities"]["0"]

        #damageEvaluation
        if(action in currentPokemon.moveset and battleMovedex[action]["category"] == ("Special" or "Physical")): #need to adjust evaluation weight we outsped
			damageEvaluation += calculate_damage(currentPokemon, opposingPokemon, action)
			if(outSpeedCheck == True):
				damageEvaluation *= 1.5 #need to adjust evaluation weight we outsped

        #opposingDamageEvaluation
        highestOpposingDamage = 0
        highestOpposingDamageMove = ""
        for move in opposingPokemon.moveset: #calculate highest damaging move from opposingPokemon
			if(battleMovedex[move]["category"] == ("Special" or "Physical"):
				opposingDamage = calculate_damage(opposingPokemon, currentPokemon, move)
				if(calculate_damage(opposingDamage > highestOpposingDamage):
					highestOpposingDamage = opposingDamage
					highestOpposingDamageMove = move
		opposingDamageEvaluation -= highestOpposingDamage
		if(outSpeedCheck = false): #should give higher evaluation if we don't outSpeed opposingPokemon
			opposingDamageEvaluation *= 1.5 #need to adjust evaluation weight we are outsped

		#non-damageCalculation goes here

        #switchEvaluation
		switchCheck = action[:8]
		if(action[:8] == "SwitchTo")): #remember to properly index, i.e 0 = Pokemon1, Switch prediction for highestOpposingDamageMove. A sample swich action would be "SwitchToBulbasaur"
			pokemonName = action[8:] #splice all but SwitchTo
			pokemonName.lower()#pokemon switched to in lowercase
			calculate_damage(opposingPokemon, pokemonName, highestOpposingDamageMove) #need to get pokemonClass given string pokemonName from action
			switchEvaluation += weight

		return speedEvaluation + damageEvaluation + opposingDamageEvaluation
