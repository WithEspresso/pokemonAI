import re

from showdownNavigator import pokemon


class ConsoleLogProcessor:

    team_data = None
    initial_turn = None
    current_turn = None

    def __init__(self, console_log):
        """
        Given a console log, parses it by finding keywords in the message
        key's value to determine what part of the console is important
        pertaining to the game state.
        :param console_log:
        """
        for entry in console_log:
            # Get the team data
            if "request" in entry.get("message"):
                self.data = entry.get("message")
            # Get the initial turn
            if "|seed|" in entry.get("message"):
                self.initial_turn = entry.get("message")
            # Get the current turn's update
            if "|move|" in entry.get("message") or "|switch|" in entry.get("message"):
                self.current_turn = entry.get('message')

    def get_current_turn(self, active_pokemon, enemy_pokemon):
        """
        Gets information about the current turn. Modifies the given
        pokemon provided in the method signature to reflect
        changes in the game state.
        :param active_pokemon:
        :param enemy_pokemon:
        :return:
        """
        ai_id = "p1a:"
        enemy = "p2a:"

        # DEBUG
        print("Before the turn has occurred: ")
        print("\tActive pokemon is: " + str(active_pokemon))
        print("\tEnemy pokemon is: " + str(enemy_pokemon))

        cleaned_data = self.current_turn.replace("\"", "").replace("\\", " ")
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
                damage_taken = turn_data[i + 2]
                if turn_data[i + 1] == enemy:
                    enemy_pokemon.take_damage(damage_taken)
                    print("Enemy pokemon has taken damage: " + damage_taken)
                else:
                    active_pokemon.take_damage(turn_data[i + 2])
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
                    enemy_pokemon = pokemon.Pokemon(species, level, hp)

        # DEBUG
        print("Before the turn has occurred: ")
        print("\tActive pokemon is: " + str(active_pokemon))
        print("\tEnemy pokemon is: " + str(enemy_pokemon))

    def get_team_data(self):
        """
        Returns a list of pokemon belonging to the player with all of
        their statistics, available moves, and remaining HP and statuses.
        :return: A list of pokemon belonging to the player and their stats.
        """
        # Gets the string containing the game state information out of the dictionary
        # Clean the data and prepare it for parsing by splitting it into an array.
        cleaned_data = self.data.replace("\"", "").replace("\\", " ")
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
            new_pokemon = pokemon.Pokemon(side_pokemon_species_names[i],
                                              side_pokemon_levels[i],
                                              side_pokemon_hp[i],
                                              side_pokemon_stats[i],
                                              side_pokemon_status[i],
                                              side_pokemon_held_items[i],
                                              side_pokemon_abilities[i],
                                              side_pokemon_moves[i])
            pokemon_team.append(new_pokemon)
        return pokemon_team



