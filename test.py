from showdownNavigator.consolelogprocessor import ConsoleLogProcessor
from showdownNavigator.pokewebdriver import ShowdownDriver
from battle.pokemonmove import *


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

# Testing turn information

cleaned_data = clp.current_turn.replace("\"", "").replace("\\", " ")
move_index = cleaned_data.find('|move|')
switch_index = cleaned_data.find('|switch|')
index = -1
if move_index > switch_index:
    index = switch_index
turn_data = cleaned_data[index:]
turn_data = turn_data.replace("|", " ").split()
print("Cleaned data is: ")
print(turn_data)
print("End Cleaned Data")

clp.get_current_turn()

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
