from showdownNavigator.consolelogprocessor import ConsoleLogProcessor
from showdownNavigator.pokewebdriver import ShowdownDriver
from battle.battle import get_index_of_best_move
from battle.battle import calculate_best_damage
from battle.gamestate import GameState
from showdownNavigator.pokemon import Pokemon

import time

"""
Test file to check driver functionality.
"""


def run_game():
    web = ShowdownDriver()
    input("Press a key when the battle is ready.")
    # Initial setup of the game state.
    console_log = web.driver.get_log('browser')
    clp = ConsoleLogProcessor(console_log)
    team = clp.get_team_data()
    enemy = clp.get_enemy_as_p1a_or_p2a()
    enemy_pokemon = clp.get_enemy_active_initial(enemy)
    active_pokemon = team[0]
    state = clp.generate_initial_gamestate()

    # Start off by picking one move to do.
    best_index = get_index_of_best_move(active_pokemon, enemy_pokemon, web)
    web.select_move(best_index)
    input("Press a key when the next turn has started.")

    # Game loop.
    game = True
    while game:
        # Update the game state.
        console_log = web.driver.get_log('browser')
        clp.set_console_log(console_log)
        print_turn_data(clp)
        state = clp.get_current_turn(state)
        if state.is_lose() or state.is_win():
            game = False
            break
        enemy_pokemon = state.get_enemy_active_pokemon()
        active_pokemon = state.get_active_pokemon()
        # Wait for HTML elements to load.
        time.sleep(3)
        state.set_legal_moves(web.get_moves())
        state.set_legal_switches(web.get_legal_switches())

        # If we killed the enemy, just wait for them to switch.
        if enemy_pokemon.get_status() is "fnt" or active_pokemon.hp is 0:
            input("Press a key when they send out another pokemon.")
        # If we were just fainted, switch Pokemon.
        elif active_pokemon.get_status() is "fnt" or active_pokemon.hp is 0:
            switch_index = get_switch_index(state)
            next_pokemon = state.get_legal_switches()[switch_index].species
            print("Switching pokemon to : " + str(next_pokemon))
            web.switch_pokemon(switch_index)
            input("Press a key when your pokemon is out.")
        else:
            # Pick a move and fight.
            best_index = get_index_of_best_move(active_pokemon, enemy_pokemon, web)
            # If our pokemon is totally helpless, let's switch out to a safer one.
            if best_index is -1:
                switch_index = get_switch_index(state)
                next_pokemon = state.get_legal_switches()[switch_index].species
                print("Switching pokemon to : " + str(next_pokemon))
                web.switch_pokemon(switch_index)
                input("Press a key when your next pokemon is out.")
            else:
                web.select_move(best_index)
                # TODO: Implement a way to check if the turn is done. For now,
                # Just press a button to continue.
                input("Press a key when there is a new turn.")


def get_switch_index(game_state):
    """
    Returns the index of the pokemon best to switch to.
    :param game_state:
    :return: The index of the best pokemon to switch to as an integer.
    """
    available_pokemon = game_state.get_legal_switches()
    enemy_active_pokemon = game_state.get_enemy_active_pokemon()
    best_index = 0
    index = 0
    length = len(available_pokemon)
    if length > 0:
        minimum_damage = 999999
        for pokemon in available_pokemon:
            damage = calculate_best_damage(enemy_active_pokemon, pokemon)
            if type(pokemon.hp) == str:
                hp = pokemon.hp.split('/')[0]
            else:
                hp = pokemon.hp
            if damage < int(hp):
                if damage < minimum_damage:
                    minimum_damage = damage
                    best_switch = pokemon.species
                    best_index = index
                index += 1
        print("Best pokemon to switch to is: " + str(best_switch))
        print("This pokemon is at index: " + str(best_index))
    return best_index


def print_turn_data(clp):
    cleaned_data = clp.current_turn.replace("\"", "").replace("\\", " ")
    move_index = cleaned_data.find('|move|')
    switch_index = cleaned_data.find('|switch|')
    index = -1
    if move_index > switch_index:
        index = move_index
    else:
        index = switch_index

    turn_data = cleaned_data[index:]
    turn_data = turn_data.replace("|", " ").split()
    print(turn_data)


def print_initial_data(clp):
    cleaned_data = clp.data.replace("\"", "").replace("\\", " ")
    index = cleaned_data.find('side')
    side_pokemon_data = cleaned_data[index:]
    side = side_pokemon_data.split()
    print(side)

"""
cleaned_data = clp.data.replace("\"", "").replace("\\", " ")
index = cleaned_data.find('side')
side_pokemon_data = cleaned_data[index:]
side = side_pokemon_data.split()
print(side)
"""

# Start of game
"""
web = ShowdownDriver()

console_log = web.driver.get_log('browser')
clp = ConsoleLogProcessor(console_log)
team = clp.get_team_data()
player = clp.get_enemy_as_p1a_or_p2a()
enemy = "p2a:"
if player == "p1a":
    enemy = "p2a:"
else:
    enemy = "p1a:"

enemy_pokemon = clp.get_enemy_active_initial(enemy)
active_pokemon = team[0]
state = clp.generate_initial_gamestate()
state.set_legal_moves(web.get_moves())
state.set_legal_switches(web.get_legal_switches())
"""

# Copy pasta for selecting the best move.
"""
best_index = get_index_of_best_move(active_pokemon, enemy_pokemon, web)
web.select_move(best_index)

print("You are player: " + str(clp.get_enemy_as_p1a_or_p2a()))
print("The enemy active pokemon is: " + str(enemy_pokemon))
print("Your active pokemon is: " + str(active_pokemon))

"""
# copy pasta for updating the game state.
"""
console_log = web.driver.get_log('browser')
clp.set_console_log(console_log)
print_turn_data(clp)
state = clp.get_current_turn(state)
if state.is_lose() or state.is_win():
    game = False
    break
enemy_pokemon = state.get_enemy_active_pokemon()
active_pokemon = state.get_active_pokemon()
# Wait for HTML elements to load.
time.sleep(3)
state.set_legal_moves(web.get_moves())
state.set_legal_switches(web.get_legal_switches())
"""

# Copy pasta for looking at turn data in cleaned form.
"""
cleaned_data = clp.current_turn.replace("\"", "").replace("\\", " ")
move_index = cleaned_data.find('|move|')
switch_index = cleaned_data.find('|switch|')
index = -1
if move_index > switch_index:
    index = move_index
else:
    index = switch_index
    

turn_data = cleaned_data[index:]
turn_data = turn_data.replace("|", " ").split()
print(turn_data)
"""
"""
game = True
while game:
    # Update console log and game state.
    console_log = web.driver.get_log('browser')
    clp.set_console_log(console_log)
    team = clp.get_team_data()
    active_pokemon = team[0]
    enemy_pokemon = clp.get_enemy_active_initial(enemy)

    # Calculate maximizer's best action
    moveset = web.get_moves()
    print("Your possible moves are: ")
    for move in moveset:
        print(move + " ", end='', flush=True)
    best_index = calculate_best_damaging_move(active_pokemon, enemy_pokemon, web)

    # Calculate minimizer's best action
    print("Enemy's possible moves are: ")
    for move in enemy_pokemon.get_moveset():
        print(move + " ", end='', flush=True)
    best_enemy_move = calculate_best_damaging_move(enemy_pokemon, active_pokemon)

    # TODO: Check for html elements before continuing rather than button presses.
    input("Press a key to fight:")
    web.select_move(best_index)
    input("Press a key when your enemy has selected a move")
    state = clp.get_current_turn(state)


clp.get_current_turn(enemy_pokemon)
enemy_pokemon = clp.get_enemy_active_initial(enemy)
print("The enemy active pokemon is: " + str(enemy_pokemon))
active_pokemon = team[0]
print("Your active pokemon is: " + str(active_pokemon))


#Testing if we can pull and calculate the highest damage move
maxDmgMove = ("" , 0)
current_pokemon = clp.get_active_pokemon()
active_enemy_pokemon = clp.get_enemy_active_pokemon()
for move in current_pokemon.get_moveset():
    moveDmg = calculate_damage(current_pokemon, active_enemy_pokemon, move, None)
    print(move + ": " + moveDmg)
    if moveDmg > maxDmgMove[1]:
        maxDmgMove = (move, moveDmg)
print("Choose: " + maxDmgMove[0])
print("Damage:", maxDmgMove[1])
#End damage test
"""

"""
enemy = "p1a"
# Iterate through the split data and parse for turn information.
        for i in range(0, len(turn_data)):
            item = turn_data[i]
            # Search for damage done.
            if item == "-damage":
                damage_taken = turn_data[i + 2]
                if turn_data[i + 1] == enemy:
                    # enemy_pokemon.take_damage(damage_taken)
                    print("Enemy pokemon has taken damage: " + damage_taken)
                else:
                    # active_pokemon.take_damage(turn_data[i + 2])
                    print("Friendly pokemon has taken damage: " + damage_taken)

            # Search for stat boosts
            if item == "-boost":
                stat = turn_data[i + 2]
                modifier = turn_data[i + 3]
                if turn_data[i + 1] == enemy:
                    enemy_pokemon.modify_stat(stat, modifier)
                    print("Enemy pokemon's " + stat + "has been improved by: " + modifier + "levels")
                else:
                    active_pokemon.modify_stat(stat, modifier)
                    print("Friendly pokemon's " + stat + "has been improved by: " + modifier + "levels")

            # Search for debuffs
            if item == "-unboost":
                stat = turn_data[i + 2]
                modifier = "-" + turn_data[i + 3]
                if turn_data[i + 1] == enemy:
                    enemy_pokemon.modify_stat(stat, modifier)
                    print("Enemy pokemon's " + stat + "has been lowered by: " + modifier + "levels")
                else:
                    active_pokemon.modify_stat(stat, modifier)
                    print("Friendly pokemon's " + stat + "has been lowered by: " + modifier + "levels")

            # Search for switching Pokemon. Your Pokemon will be
            # updated with the get_team function. This is only
            # for getting data about the enemy Pokemon
            if item == "switch":
                if turn_data[i + 1] == enemy:
                    species = turn_data[i + 2]
                    level = turn_data[i + 4]
                    hp = turn_data[i + 6]
                    print("Enemy pokemon " + enemy_pokemon.species + " has switched out to " + species)
                    enemy_pokemon = pokemon.Pokemon(species, level, hp)


input("Press a key when a turn has passed.")
console_log = web.driver.get_log('browser')
if console_log is not None:
    print("Found console log.")
    for log in console_log:
        print(log)
team = clp.get_team_data()
"""
