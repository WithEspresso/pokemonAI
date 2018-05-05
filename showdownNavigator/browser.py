from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Login information
USERNAME = "csc665"
PASSWORD = "csc665"

URL_BASE = "https://play.pokemonshowdown.com/"

# Element names
LOGIN_ELEMENT = 'login'
USERNAME_ELEMENT = 'username'
PASSWORD_ELEMENT = 'password'

# X paths
CHOOSE_NAME_X_PATH = "/html/body/div[5]/div/form/p[2]/button[1]/strong"


# enable browser logging
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities['loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
driver.get(URL_BASE)

# Wait for page elements to load
delay = 5  # in seconds
try:
    test_element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, LOGIN_ELEMENT)))
    print("Page is ready!")
except TimeoutException:
    print("Timeout has occurred.")


# Log in
login_button = driver.find_element_by_name("login")
login_button.click()

username_field = driver.find_element_by_name("username")
username_field.send_keys(USERNAME)
username_field.send_keys(Keys.RETURN)

delay = 5  # in seconds
try:
    test_element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, PASSWORD_ELEMENT)))
    print("Page is ready!")
except TimeoutException:
    print("Timeout has occurred.")

password_field = driver.find_element_by_name("password")
password_field.send_keys(PASSWORD)
password_field.send_keys(Keys.RETURN)

# print messages
print('LOGIN ATTEMPTED')
