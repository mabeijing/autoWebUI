import pytest
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.events import EventFiringWebDriver

from lib.hooks import MyListen
import setting


@pytest.fixture(scope='class')
def driver():
    options = ChromeOptions()
    if setting.HEADLESS_MODE:
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
    else:
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        # options.add_argument("--auto-open-devtools-for-tabs")

    server = Service(executable_path=setting.executable_path)
    chrome_driver = webdriver.Chrome(options=options, service=server)

    chrome_driver.set_window_size(1920, 1080)
    logger.debug(f'current windows size: {chrome_driver.get_window_size()}')
    driver = EventFiringWebDriver(chrome_driver, MyListen())

    driver.maximize_window()
    driver.implicitly_wait(3)

    yield driver
    driver.quit()
