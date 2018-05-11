from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time


class ShowdownDriver:
    # Login information
    USERNAME = "csc665"
    PASSWORD = "csc665"
    SHOWDOWN_URL = "https://play.pokemonshowdown.com/"
    # Element names
    LOGIN_ELEMENT = 'login'
    USERNAME_ELEMENT = 'username'
    PASSWORD_ELEMENT = 'password'
    # Web driver
    driver = None
    # console log to retrieve
    console_log = None

    def __init__(self, browser="Chrome"):
        # TODO: Some options in constructor. Let it select tiers, select teams in the future?
        """
        Create web driver, launches browser, goes to Pokemon Showdown.
        """
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities['loggingPrefs'] = {'browser': 'ALL'}
        if browser=="Chrome":
            self.driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        else:
            self.driver = webdriver.Firefox()
        self.driver.get(self.SHOWDOWN_URL)
        self.login()

    def login(self):
        # TODO VERIFY LOGIN AFTER THIS METHOD HAS RUN.
        """
        Logs the user into Pokemon showdown by using
        selenium selectors based on eleme nt name.
        :param      A web driver:
        :return:    True if the user is logged in, false otherwise.
        """
        # Waits until the page has loaded, then selects the "Choose name" button
        self.verify_element_has_loaded(self.LOGIN_ELEMENT)
        login_button = self.driver.find_element_by_name("login")
        login_button.click()
        # Types in the username and hits return to open the password field
        username_field = self.driver.find_element_by_name("username")
        username_field.send_keys(self.USERNAME)
        username_field.send_keys(Keys.RETURN)
        # Verifies that the password field has loaded, then types in the password
        self.verify_element_has_loaded(self.PASSWORD_ELEMENT)
        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys(self.PASSWORD)
        password_field.send_keys(Keys.RETURN)
        # Delay to give the page time to load.
        time.sleep(3)

    def verify_element_has_loaded(self, element_name, delay=3):
        """
        Helper function to ensure that an element loads before clicking on it.
        Given an element name, waits until it has loaded onto the screen then
        prints a success method to the console.
        :param  element_name    to wait for
        :param delay            The time to wait for in seconds.
        :return: None
        :except TimeoutException
        """
        try:
            test_element = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.NAME, element_name)))
            print("Page is ready!")
        except TimeoutException:
            print("Timeout has occurred.")

    def start_battle(self, battle_type="gen7randombattle"):
        """
        Selects the type of battle to get itself into.
        Be default, I had it set to gen 7 random battles.
        For future extensions, look up the name of the element and pass it.
        :param battle_type:    The type of battle to start.
        :return:        None
        """
        battle = self.driver.find_element_by_name("format")
        battle.click()
        battle = self.driver.find_element_by_xpath("//button[@name='selectFormat' and @value='%s']" % battle_type);
        battle.click()
        battle = self.driver.find_element_by_name("search")
        battle.click()
        time.sleep(5)

    def get_moves(self):
        """
        Returns a list of legal moves. Legal moves are moves
        not locked out by choice items or moves that have remaining PP.
        :param      self
        :return:    A list of legal moves.
        """
        legal_moves = []
        move_set = self.driver.find_elements_by_xpath("//button[@name='chooseMove']")
        for element in move_set:
            legal_moves.append(element.get_attribute('data-move'))
        return legal_moves

    def select_move(self, index):
        # TODO: Pass move information to the json parser to give to the
        # TODO: expectimax tree.
        """
        Selects a move to use given the index.
        When moves run out of PP or are locked due to choice items, they're marked
        as the name being 'disabled'. This function should pass the moves
        to the json damage evaluator first in order to allow choices based on the
        remaining moves rather than the available moves.
        Class "PP" stores pp information.
        :param      index:
        :return:    None
        """
        moveset = self.driver.find_elements_by_xpath("//button[@name='chooseMove']")
        move = moveset[index]
        move.click()

    def mega_evolve(self):
        """
        Selects the mega evolution checkbox so that the Pokemon can mega evolve the next
        turn. The AI will select this as soon as possible.
        Lparam      none
        :return:    None
        """
        mega = self.driver.find_element_by_name("megaevo")
        mega.click()

    def switch_pokemon(self, index):
        # Check for shadow tag, mean look, etc first before calling this function.
        """
        Selects a Pokemon to switch to.
        If a Pokemon is unusable, it is marked with the html tag as "chooseDisabled"
        and the value contains "fainted".
        :param      index:   Index of the pokemon to switch to
        :return:    None
        """
        remaining_pokemon = self.driver.find_elements_by_xpath("//button[@name='chooseSwitch']")
        next_pokemon = remaining_pokemon[index]
        next_pokemon.click()

    def get_team_data(self):
        # TODO: Parse information from the console about your team.
        # The console automatically displays information about your Pokemon when the battle starts
        pass

    def get_turn_information(self):
        """
        TODO: Figure out a way to get the right dictionary if there is chat.
        Each passing turn will generate a list of dictionaries in the console log.
        The first dictionary contains information about the game instance.
        The second dictionary contains information about the game state.
        The third dictionary contains information about the turn.
            The first entry in the third dictionary signifies that it is logging information
            The second entry in the third dictionary is the message item, which is what we want to parse.
            The third entry is the source, not important.
            The fourth entry is the timestamp, not important for our purposes.
        :return:
        """
        self.console_log = self.driver.get_log('browser')
        turn_log = self.console_log[2].get('message')
        index = turn_log.find('|')
        end_index = len(turn_log)
        turn_information = turn_log[index:]
        turn_information = turn_information.split("\\n")
        print(type(turn_information))
        return turn_information

    def get_current_health(self):
        # TODO: Get information about this Pokemon's health.
        pass

    def get_opponent_health(self):
        # TODO: Get information about the opponent's health
        pass

