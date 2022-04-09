"""
封装启动不同浏览器的初始化工作
"""

from selenium import webdriver

from selenium.webdriver.support.events import EventFiringWebDriver
from lib.hooks import MyListen
from lib.scaffold import absolute_path
from lib.session import Session
import setting


def chrome_browser() -> EventFiringWebDriver:
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver import ChromeOptions
    options = ChromeOptions()

    if setting.HEADLESS_MODE:
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
    else:
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--auto-open-devtools-for-tabs")

    server = Service(executable_path=setting.executable_path)

    driver = webdriver.Chrome(service=server, options=options)
    Session.DEFAULT_DRIVER = driver
    Session.DEFAULT_WINDOW_HANDLE = driver.current_window_handle
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.implicitly_wait(3)

    with open(absolute_path('stealth.min.js')) as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

    return EventFiringWebDriver(driver, MyListen())
