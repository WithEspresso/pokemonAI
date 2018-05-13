#Not Complete btw

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        return self.minimax(gameState)[1] #return the action
        
    def minimax(self, gameState):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), 0) #returns the current score when win, lose
        legalActions = gameState.getLegalActions(index) #move1, move2, move3, move4, switch to 1-6(keep track of actual HP), (z-move usage, mega evolution given check for proper items)
        listOfActions = []
        for action in legalActions:
            listOfActions.append((self.minimax(gameState.generateSuccessor(action))[0], action)) #recursive call until it returns tuple (score, action)           
        return max(listOfActions) #return best maximizing action for us, we already consider the best minimizing action of our opponent within our evaluation function
	
    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generateSuccessor(action)				
		speedEvaluation, damageEvaluation, opposingDamageEvaluation, nondamageEvaluation, switchEvaluation = 0;
		outSpeedCheck = false
		if(currentPokemon.speed >= opposingPokemon.speed){ #evaluate speed
			speedEvaluation += weight	
			outSpeedCheck = True
		}
		else{
			speedEvaluation -= weight
		}
        
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


		
	
