import re
from showdownNavigator.consolelogprocessor import ConsoleLogProcessor
from showdownNavigator.pokewebdriver import ShowdownDriver
from battle.battle import get_index_of_best_move
from consolelogprocessor import ConsoleLogProcessor
from showdownNavigator.pokemon import Pokemon


web = ShowdownDriver()
input("Press a key when the battle is ready.")

enemy = "p2a:"
console_log = web.driver.get_log('browser')
clp = ConsoleLogProcessor(console_log)
initial_turn = clp.initial_turn

cleaned_data = initial_turn.replace("\"", "").replace("\\", " ")
index = cleaned_data.find('|player|')
data = cleaned_data[index:]
data = data.replace("|", " ").split()
print(data)
for i in range(0, len(data)):
    entry = data[i]
    if entry == "switch":
        if data[i + 1] == enemy:
            species = data[i + 2]
            level = data[i + 4]
            level = int(re.sub('[^0-9]', '', level))
            hp = data[i + 5]
            if "/" in hp:
                print("Found enemy pokemon: " + str(species))
                enemy_pokemon = Pokemon(species, level, hp)
                print(enemy_pokemon)
            else:
                hp = data[i + 6]
                if "/" in hp:
                    print("Found enemy pokemon: " + str(species))
                    enemy_pokemon = Pokemon(species, level, hp)
                    print(enemy_pokemon)