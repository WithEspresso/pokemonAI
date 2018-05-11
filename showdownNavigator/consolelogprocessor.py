import re


def clean_console_log(console_log):
    # Gets the dictionary with the game state out of the console log.
    game_state_dictionary = console_log[1]
    # Gets the string containing the game state information out of the dictionary
    data = game_state_dictionary.get('message')
    cleaned_data = data.replace("\"", "").replace("\\", " ")
    # Gets the side pokemon information
    index = cleaned_data.find('side')
    side_pokemon_data = cleaned_data[index:]

    # Get the information about the side Pokemon
    side = side_pokemon_data.split()

    # Get the names of the species
    species_names = list()
    for i in range(0, len(side)):
        if side[i] == "ident":
            species_names.append(side[i + 3])

    # Get the levels of the Pokemon
    levels = list()
    for i in range(0, len(side)):
        item = side[i]
        if item[0] == "L" and item[1].isdigit():
            level = item[1] + item[2]
            levels.append(level)

    # Get Pokemon's current HP and status
    side_pokemon_hp = list()
    side_pokemon_status = list()
    for i in range(0, len(side)):
        item = side[i]
        if item == "condition":
            current_hp = side[i + 2]
            side_pokemon_hp.append(current_hp)
            status = side[i + 3]
            if status is ',':
                status = "Healthy"
            side_pokemon_status.append(status)

    # Get remaining Pokemon's stats
    side_pokemon_stats = list()
    for i in range(0, len(side)):
        item = side[i]
        if item == "stats":
            stat = dict()
            stat['atk'] = re.sub('[^0-9]+', '', side[i + 3])
            stat['def'] = re.sub('[^0-9]+', '', side[i + 5])
            stat['spa'] = re.sub('[^0-9]+', '', side[i + 7])
            stat['spd'] = re.sub('[^0-9]+', '', side[i + 9])
            stat['spe'] = re.sub('[^0-9]+', '', side[i + 11])
            print(stat)
            side_pokemon_stats.append(stat)




