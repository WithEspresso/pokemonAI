from showdownNavigator.consolelogprocessor import ConsoleLogProcessor
from showdownNavigator.pokewebdriver import ShowdownDriver
from showdownNavigator.pokemon import Pokemon
from showdownNavigator.pokedex import *


"""
Test file to check driver functionality.
"""

web = ShowdownDriver()
input("Press a key when the battle is ready.")

console_log = web.driver.get_log('browser')
if console_log is not None:
    print("Found console log.")
    for log in console_log:
        print(log)

clp = ConsoleLogProcessor(console_log)
print("clp ready")
team = clp.get_team_data()
print("Your team is: ")
for pokemon in team:
    print(pokemon)
player = clp.get_p1a_or_p2a()
if player == "p1a":
    enemy = "p2a:"
else:
    enemy = "p1a:"
print("You are player: " + str(clp.get_p1a_or_p2a()))
enemy_pokemon = clp.get_enemy_active()
print("The enemy active pokemon is: " + str(enemy_pokemon))
print("Your possible moves are: ")
web.get_moves()


clp.get_current_turn()

"""
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
"""

input("Press a key when a turn has passed.")
console_log = web.driver.get_log('browser')
if console_log is not None:
    print("Found console log.")
    for log in console_log:
        print(log)
team = clp.get_team_data()
