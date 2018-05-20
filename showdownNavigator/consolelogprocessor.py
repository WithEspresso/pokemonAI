import re

from showdownNavigator import pokemon
from battle.pokedex import check_name
from battle.gamestate import GameState


class ConsoleLogProcessor:

    team_data = None
    initial_turn = None
    current_turn = None

    active_pokemon = None

    player = None

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

    def set_console_log(self, console_log):
        if console_log is not None:
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
            print("Console log updated.")
        else:
            print("Error: Console log contains no updates.")

    def generate_initial_gamestate(self):
        """
        Generates an initial game state. Called when
        the game first starts.
        :return:    The initial game state.
        """
        team = self.get_team_data()
        enemy = self.get_enemy_as_p1a_or_p2a()
        enemy_active = self.get_enemy_active_initial(enemy)
        return GameState(team, enemy_active, enemy)

    def get_enemy_as_p1a_or_p2a(self):
        """
        Determines if the bot is p1a or p2a for purposes of processing the
        console log's turn entries. Called during the first turn.
        :return: p1a if the bot is player 1, p2a otherwise.
        """
        cleaned_data = self.initial_turn.replace("\"", "").replace("\\", " ")
        index = cleaned_data.find('|player|')
        data = cleaned_data[index:]
        data = data.replace("|", " ").split()
        for i in range(0, len(data)):
            entry = data[i]
            if entry == "player":
                if data[i + 1] == "p2":
                    if data[i + 2] == "csc665":
                        return "p1a:"
                    else:
                        return "p2a:"

    def get_enemy_active_initial(self, enemy):
        """
        Enemy can be p1a: or p2a:
        :param enemy:
        :return:
        """
        cleaned_data = self.initial_turn.replace("\"", "").replace("\\", " ")
        index = cleaned_data.find('|player|')
        data = cleaned_data[index:]
        data = data.replace("|", " ").split()
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
                        enemy_pokemon = pokemon.Pokemon(species, level, hp)
                        return enemy_pokemon
                    else:
                        hp = data[i + 6]
                        if "/" in hp:
                            print("Found enemy pokemon: " + str(species))
                            enemy_pokemon = pokemon.Pokemon(species, level, hp)
                            return enemy_pokemon

    def get_current_turn(self, game_state):
        """
        Gets information about the current turn. Modifies the given
        pokemon provided in the method signature to reflect
        changes in the game state.
        :param active_pokemon:
        :param enemy_pokemon:
        :return:
        """
        active_pokemon = game_state.get_active_pokemon()
        enemy_pokemon = game_state.get_enemy_active_pokemon()
        enemy = game_state.get_enemy_player()

        # DEBUG
        print("*****************************")
        print("Before the turn has occurred: ")
        print("\tActive pokemon is: " + str(active_pokemon))
        print()
        print("\tEnemy pokemon is: " + str(enemy_pokemon))
        print("*****************************")
        print()
        print()

        cleaned_data = self.current_turn.replace("\"", "").replace("\\", " ")
        move_index = cleaned_data.find('|move|')
        switch_index = cleaned_data.find('|switch|')
        index = -1
        if move_index > switch_index:
            index = move_index
        else:
            index = switch_index
        turn_data = cleaned_data[index:]
        turn_data = turn_data.replace("|", " ").split()

        # Iterate through the split data and parse for turn information.
        for i in range(0, len(turn_data)):
            item = turn_data[i]

            # Search for damage done.
            if item == "-damage":
                species = turn_data[i + 2]
                # Case where the Pokemon's name has two words in it.
                if not check_name(species.lower()):
                    damage_taken = turn_data[i + 4]
                else:
                    damage_taken = turn_data[i + 3]
                if turn_data[i + 1] == enemy:
                    enemy_pokemon.take_damage(damage_taken)
                    print("Enemy " + enemy_pokemon.species + " has taken damage: " + damage_taken)
                else:
                    active_pokemon.take_damage(damage_taken)
                    print("Friendly " + active_pokemon.species + " has taken damage: " + damage_taken)

            # Search for healing.
            if item == "-heal":
                species = turn_data[i + 2]
                # Case where the Pokemon's name has two words in it.
                if not check_name(species.lower()):
                    damage_healed = turn_data[i + 4]
                else:
                    damage_healed = turn_data[i + 3]
                if turn_data[i + 1] == enemy:
                    enemy_pokemon.take_damage(damage_healed)
                    print("Enemy pokemon has healed: " + damage_healed)
                else:
                    active_pokemon.take_damage(turn_data[i + 2])
                    print("Friendly pokemon has healed: " + damage_healed)

            # Search for fainted pokemon
            if item == 'faint':
                if turn_data[i + 1] == enemy:
                    enemy_pokemon.status = "fnt"
                    print("Enemy " + enemy_pokemon.species + "has fainted.")
                    game_state.enemy_remaining_pokemon -= 1
                else:
                    active_pokemon.status = "fnt"
                    print("Your " + enemy_pokemon.species + "has fainted.")
                    game_state.remaining_pokemon -= 1

            # Search for status changes (i.e. brn, paralysis, etc.)
            if item == "-status":
                species = turn_data[i + 2]
                # Case where the Pokemon's name has two words in it.
                if not check_name(species.lower()):
                    status = turn_data[i + 4]
                else:
                    status = turn_data[i + 3]
                if turn_data[i + 1] == enemy:
                    enemy_pokemon.set_status(status)
                    print("Enemy " + enemy_pokemon.species + " has been inflicted with " + status)
                else:
                    active_pokemon.set_status(status)
                    print("Friendly " + enemy_pokemon.species + " has been inflicted with " + status)

            # Search for stat boosts
            if item == "-boost":
                species = turn_data[i + 2]
                # Case where the Pokemon's name has two words in it.
                if not check_name(species.lower()):
                    stat = turn_data[i + 4]
                    print("Boosting " + stat)
                    modifier = turn_data[i + 5]
                    print("by " + modifier + "levels")
                # Case where the pokemon has a one word name.
                else:
                    stat = turn_data[i + 3]
                    print("Boosting " + stat)
                    modifier = turn_data[i + 4]
                    print("by " + modifier + "levels")
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
                species = turn_data[i + 2]
                # Case where the Pokemon's name has two words in it.
                if not check_name(species.lower()):
                    species += turn_data[i + 3]
                    level = turn_data[i + 6]
                    hp = turn_data[i + 7]
                # Case where the pokemon has a one word name.
                else:
                    level = turn_data[i + 4]
                    hp = turn_data[i + 6]
                level = int(re.sub('[^0-9]', '', level))
                if turn_data[i + 1] == enemy:
                    print("Enemy pokemon " + enemy_pokemon.species + " has switched out to " + species)
                    enemy_pokemon = pokemon.Pokemon(species, level, hp)
                else:
                    print("You switched out " + active_pokemon.species + " to " + species)
                    active_pokemon = self.get_team_data()[0]

                    """
                    if turn_data[i + 1] == enemy:
                    species = turn_data[i + 2]
                    if not check_name(species):
                        species += turn_data[i + 3]
                        level = turn_data[i + 6]
                        hp = turn_data[i + 7]
                    level = turn_data[i + 4]
                    hp = turn_data[i + 6]
                    print("Enemy pokemon " + enemy_pokemon.species + " has switched out to " + species)
                    enemy_pokemon = pokemon.Pokemon(species, level, hp)
                    """

            # Case where a move will force a switch (i.e. Dragon Tail)
            if item == "drag":
                species = turn_data[i + 2]
                # Case where the Pokemon's name has two words in it.
                if not check_name(species.lower()):
                    species += turn_data[i + 3]
                    level = turn_data[i + 6]
                    level = int(re.sub('[^0-9]', '', level))
                    hp = turn_data[i + 7]
                # Case where the pokemon has a one word name.
                else:
                    level = turn_data[i + 4]
                    hp = turn_data[i + 6]
                if turn_data[i + 1] == enemy:
                    print("Enemy pokemon " + species + " was dragged out! ")
                    enemy_pokemon = pokemon.Pokemon(species, level, hp)
                else:
                    print("Your " + species + "was dragged out!")
                    active_pokemon = self.get_team_data()[0]

        # DEBUG
        print()
        print()
        print("*****************************")
        print("After the turn has occurred: ")
        print("\tActive pokemon is: " + str(active_pokemon))
        print("\tEnemy pokemon is: " + str(enemy_pokemon))
        print("*****************************")
        # END DEBUG

        game_state.set_active_pokemon(active_pokemon)
        game_state.set_enemy_active_pokemon(enemy_pokemon)
        return game_state

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
            # Get species name. Checks for names with two words in it
            # like tapu koko.
            if item == "ident":
                species_name = side[i + 3].lower()
                if check_name(species_name):
                    side_pokemon_species_names.append(species_name)
                else:
                    species_name += side[i + 4].lower()
            # Get the levels of the Pokemon
            if item[0] == "L" and item[1].isdigit():
                level = item[1] + item[2]
                side_pokemon_levels.append(level)
            # Get hp and status
            if item == "condition":
                current_hp = str(side[i + 2])
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
        self.active_pokemon = pokemon_team[0]
        return pokemon_team



