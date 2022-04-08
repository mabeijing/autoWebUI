import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from lib.browser import chrome_browser
from lib.custom_element import CustomWebElement
from lib.custom_shadow_root import CustomShadowRoot
from lib.scaffold import setup_loguru


@pytest.fixture(scope='session', autouse=True)
def log_init():
    print()
    setup_loguru()


@pytest.fixture(scope='class', autouse=True)
def driver_init():
    WebDriver._web_element_cls = CustomWebElement
    WebDriver._shadowroot_cls = CustomShadowRoot


@pytest.fixture(scope='class')
def driver():
    driver = chrome_browser()
    yield driver
    driver.quit()
