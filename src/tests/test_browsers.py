"""
Test the browsers module.
"""
import pytest


from selenium.common.exceptions import TimeoutException

from selenium import webdriver 
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from src.tiktok_uploader.browsers import get_browser
from src.tiktok_uploader.auth import AuthBackend
from src.tiktok_uploader import config, logger
from src.tiktok_uploader.utils import bold, green


SUPPORTED_BROWSERS = ['chrome', 'firefox', 'safari', 'edge']
SERVICES = ['chrome', 'firefox', 'edge']

# Default behavior testing
# def test_get_browser():
#     """
#     Tests the get_browser function.

#     Requires all browsers to be installed on the system.
#     """
#     browser = browsers.get_browser()
#     assert browser is not None


# def test_get_driver():
#     """
#     Tests the get_driver function.
#     """
#     default = browsers.get_driver()
#     assert default is not None

#     # pytest throws exception test
#     with pytest.raises(browsers.UnsupportedBrowserException):
#         browsers.get_driver('invalid')


# def test_get_service():
#     """
#     Tests the get_service function.
#     """
#     default = browsers.get_service()

#     assert default is not None


# # Test each default
# def test_chrome_defaults():
#     """
#     Tests the chrome_defaults function.
#     """
#     options = browsers.chrome_defaults()
#     headless = browsers.chrome_defaults(headless=True)
#     assert options is not None
#     assert headless is not None


# def test_firefox_defaults():
#     """
#     Tests the firefox_defaults function.
#     """
#     options = browsers.firefox_defaults()
#     headless = browsers.firefox_defaults(headless=True)
#     assert options is not None
#     assert headless is not None


# def test_safari_defaults():
#     """
#     Tests the safari_defaults function.
#     """
#     options = browsers.safari_defaults()
#     headless = browsers.safari_defaults(headless=True)
#     assert options is not None
#     assert headless is not None


# def test_edge_defaults():
#     """
#     Tests the edge_defaults function.
#     """
#     options = browsers.edge_defaults()
#     headless = browsers.edge_defaults(headless=True)

#     assert options is not None
#     assert headless is not None

def test_user_agent():
    """
    Tests the user_agent function.
    """
    auth = AuthBackend(cookies='asset/cookies/ prize09pit.txt')

    driver = get_browser(name='chrome', headless=False)
    driver = auth.authenticate_agent(driver)
    driver.get(config['paths']['upload'])
    try:
        # if _ == 0:
        upload_box = WebDriverWait(driver, 70).until(
            EC.presence_of_element_located((By.XPATH, config['selectors']['upload']['upload_video']))
        )
        print("agent is good.")
        result = driver
    except TimeoutException:
        print("agent is not good.")
        result = None

    return result
