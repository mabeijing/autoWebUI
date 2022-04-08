import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from lib.browser import chrome_browser
from lib.custom_element import CustomWebElement
from lib.custom_shadow_root import CustomShadowRoot


@pytest.fixture(scope='class', autouse=True)
def init():
    print('hello')
    WebDriver._web_element_cls = CustomWebElement
    WebDriver._shadowroot_cls = CustomShadowRoot
    print('world')


@pytest.fixture(scope='class')
def driver():
    yield chrome_browser()
