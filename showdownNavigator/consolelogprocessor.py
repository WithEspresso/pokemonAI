



def clean_console_log(console_log):
    # Gets the dictionary with the game state out of the console log.
    game_state_dictionary = console_log[1]
    # Gets the string containing the game state information out of the dictionary
    data = game_state_dictionary.get('message')
    cleaned_data = data.replace("\"", "").replace("\\", " ")
    # Gets the side pokemon information
    index = cleaned_data.find('side')
    side_pokemon_data = cleaned_data[index:]

    # Get remaining Pokemon's names
    species_names = list()
    side = side_pokemon_data.split()
    for i in range(0, len(side)):
        if side[i] == "ident":
            species_names.append(side[i + 3])
    # Get remaining Pokemon's stats



