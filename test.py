from showdownNavigator.consolelogprocessor import ConsoleLogProcessor
from showdownNavigator.pokewebdriver import ShowdownDriver
from pokemonmove import *


"""
Test file to check driver functionality. 
"""

web = ShowdownDriver()
input("Press a key when the battle is ready.")

console_log = web.driver.get_log('browser')
if console_log is not None:
    print("Found console log.")

clp = ConsoleLogProcessor(console_log)
print("clp ready")
team = clp.get_team_data()
print("Your team is: ")
for pokemon in team:
    print(pokemon)

input("Press a key when a turn has passed.")
console_log = web.driver.get_log('browser')
if console_log is not None:
    print("Found console log.")
team = clp.get_team_data()
