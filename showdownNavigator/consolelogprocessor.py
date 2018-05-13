import os.path
import sys
import re

# TODO: Make system independent
sys.path.append("C:\\Users\\dnune\\OneDrive\\Documents\\GitHub\\pokemonAI")

from showdownNavigator.pokemon import Pokemon


def get_team_data_from_console_log(console_log):
    # Gets the dictionary with the game state out of the console log.
    for entry in console_log:
        # Get the team data
        if "request" in entry.get("message"):
            data = entry.get("message")
        # Get the initial turn
        if "|seed|" in entry.get("message"):
            initial_turn = entry.get("message")
        # Get the current turn's update
        if "|move|" in entry.get("message") or "|switch|" in entry.get("message"):
            current_turn = entry


def get_current_turn(log, active_pokemon, enemy_pokemon):
    """
    Updates the game state with the results of the last turn.
    :param log:
    :return:
    """
    ai_id = "p1a:"
    enemy = "p2a:"

    cleaned_data = log.replace("\"", "").replace("\\", " ")
    move_index = cleaned_data.find('|move|')
    switch_index = cleaned_data.find('|switch|')
    index = -1
    if move_index > switch_index:
        index = switch_index
    turn_data = cleaned_data[index:]
    turn_data = turn_data.replace("|", " ").split()

    # Iterate through the split data and parse for turn information.
    for i in range(0, len(turn_data)):
        item = turn_data[i]
        # Search for damage done.
        if item == "-damage":
            if turn_data[i + 1] == enemy:
                enemy_pokemon.take_damage(turn_data[i + 2])
            else:
                active_pokemon.take_damage(turn_data[i + 2])
        # Search for stat boosts
        if item == "-boost":
            stat = turn_data[i + 2]
            modifier = turn_data[i + 3]
            if turn_data[i + 1] == enemy:
                enemy_pokemon.modify_stat(stat, modifier)
            else:
                active_pokemon.modify_stat(stat, modifier)
        # Search for debuffs
        if item == "-unboost":
            stat = turn_data[i + 2]
            modifier = "-" + turn_data[i + 3]
            if turn_data[i + 1] == enemy:
                enemy_pokemon.modify_stat(stat, modifier)
            else:
                active_pokemon.modify_stat(stat, modifier)
        # Search for switching Pokemon. Your Pokemon will be
        # updated with the get_team function. This is only
        # for getting data about the enemy Pokemon
        if item == "switch":
            if turn_data[i + 1] == enemy:
                species = turn_data[i + 2]
                level = turn_data[i + 4]
                hp = turn_data[i + 6]
                enemy_pokemon = Pokemon(species, level, hp)


def get_team_data(log):
    # Gets the string containing the game state information out of the dictionary
    # Clean the data and prepare it for parsing by splitting it into an array.
    cleaned_data = log.replace("\"", "").replace("\\", " ")
    index = cleaned_data.find('side')
    side_pokemon_data = cleaned_data[index:]
    side = side_pokemon_data.split()

    # Create list of pokemon attributes to iterate over and create team.
    side_pokemon_species_names = list()
    side_pokemon_levels = list()
    side_pokemon_hp = list()
    side_pokemon_status = list()
    side_pokemon_stats = list()
    side_pokemon_held_items = list()
    side_pokemon_abilities = list()
    side_pokemon_moves = list()

    for i in range(0, len(side)):
        item = side[i]
        # Get species names
        if item == "ident":
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
        # Get Pokemon moves
        if item == "moves":
            moveset = list()
            moveset.append(side[i + 2])
            moveset.append(side[i + 4])
            moveset.append(side[i + 6])
            moveset.append(side[i + 8])
            side_pokemon_moves.append(moveset)

    # Create friendly pokemon team.
    pokemon_team = list()
    for i in range(0, len(side_pokemon_species_names)):
        pokemon = Pokemon(side_pokemon_species_names[i],
                          side_pokemon_levels[i],
                          side_pokemon_hp[i],
                          side_pokemon_stats[i],
                          side_pokemon_status[i],
                          side_pokemon_held_items[i],
                          side_pokemon_abilities[i],
                          side_pokemon_moves[i])
        pokemon_team.append(pokemon)
    return pokemon_team



