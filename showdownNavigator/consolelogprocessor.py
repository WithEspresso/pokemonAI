import os.path
import sys
import re
from showdownNavigator.pokemon import Pokemon


sys.path.append("C:\\Users\\dnune\\OneDrive\\Documents\\GitHub\\pokemonAI")


def clean_console_log(console_log):
    # Gets the dictionary with the game state out of the console log.
    data = None
    for entry in console_log:
        if "request" in entry.get("message"):
            data = entry
    # Gets the string containing the game state information out of the dictionary
    cleaned_data = data.replace("\"", "").replace("\\", " ")
    # Gets the side pokemon information
    index = cleaned_data.find('side')
    side_pokemon_data = cleaned_data[index:]

    # Get the information about the side Pokemon
    side = side_pokemon_data.split()

    # Get the names of the species
    side_pokemon_species_names = list()
    side_pokemon_levels = list()
    side_pokemon_hp = list()
    side_pokemon_status = list()
    side_pokemon_stats = list()
    side_pokemon_held_items = list()
    side_pokemon_abilities = list()

    for i in range(0, len(side)):
        item = side[i]
        # Get species names
        if side[i] == "ident":
            side_pokemon_species_names.append(side[i + 3])
        # Get the levels of the Pokemon
        if item[0] == "L" and item[1].isdigit():
            level = item[1] + item[2]
            side_pokemon_levels.append(level)
        # Get hp and status
        if item == "condition":
            current_hp = side[i + 2]
            side_pokemon_hp.append(current_hp)
            status = side[i + 3]
            if status is ',':
                status = "Healthy"
            side_pokemon_status.append(status)
        # Get stats dictionary
        if item == "stats":
            stat = dict()
            stat['atk'] = re.sub('[^0-9]+', '', side[i + 3])
            stat['def'] = re.sub('[^0-9]+', '', side[i + 5])
            stat['spa'] = re.sub('[^0-9]+', '', side[i + 7])
            stat['spd'] = re.sub('[^0-9]+', '', side[i + 9])
            stat['spe'] = re.sub('[^0-9]+', '', side[i + 11])
            side_pokemon_stats.append(stat)
        # Get the item of the Pokemon
        if item == "item":
            hold_item = side[i + 2]
            side_pokemon_held_items.append(hold_item)
        # Get the ability of the Pokemon
        if item == "ability":
            ability = side[i + 2]
            side_pokemon_abilities.append(ability)

    print(side_pokemon_species_names)
    print(side_pokemon_levels)
    print(side_pokemon_hp)
    print(side_pokemon_status)
    print(side_pokemon_stats)
    print(side_pokemon_held_items)
    print(side_pokemon_abilities)

    pokemon_team = list()
    active_pokemon = None

    for i in range(0, len(side_pokemon_species_names)):
        pokemon = Pokemon(side_pokemon_species_names[i],
                          side_pokemon_levels[i],
                          side_pokemon_hp[i],
                          side_pokemon_stats[i],
                          side_pokemon_status[i],
                          side_pokemon_held_items[i],
                          side_pokemon_abilities[i])
        if i == 0:
            active_pokemon = pokemon
        print(pokemon)
        pokemon_team.append(pokemon)

    print("ACTIVE POKEMON is: " + active_pokemon)



