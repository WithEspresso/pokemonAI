from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time


class ShowdownBrowserDriver:
    # Login information
    USERNAME = "csc665"
    PASSWORD = "csc665"
    SHOWDOWN_URL = "https://play.pokemonshowdown.com/"
    # Element names
    LOGIN_ELEMENT = 'login'
    USERNAME_ELEMENT = 'username'
    PASSWORD_ELEMENT = 'password'
    driver = None

    def __init__(self):
        # TODO: Some options in constructor. Let it select tiers, select teams in the future?
        """
        Create web driver, launches browser, goes to Pokemon Showdown.
        """
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities['loggingPrefs'] = {'browser': 'ALL'}
        self.driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
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
        # TODO: If mega evolution is available, mega evolve before selecting a move.
        # Mega evolving as soon as possible is best for the AI,
        pass

    def switch_pokemon(self, index):
        # TODO: Given an index of a Pokemon to switch to, switch to that Pokemon.
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

    def get_current_health(self):
        # TODO: Get information about this Pokemon's health.
        pass

    def get_opponent_health(self):
        # TODO: Get information about the opponent's health
        pass

