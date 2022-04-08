"""
selenium 4.1.3

UserWebDriver : 定义浏览器操作和元素发现
MyWebElement： 定义元素操作
"""
import time
from typing import List, Union

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.events import EventFiringWebDriver

from lib.custom_element import MyWebElement
from lib.hooks import MyListen
from lib.scaffold import log

import setting

WebDriver._web_element_cls = MyWebElement


class UserWebDriver:
    def __init__(self, driver: Union[WebDriver, EventFiringWebDriver]):
        self._driver = driver

    @property
    def original_driver(self) -> WebDriver:
        return self._driver

    @property
    def session_id(self) -> str:
        return self._driver.session_id

    def get(self, url: str):
        self._driver.get(url=url)

    @log
    def find_element_by_loc(self, loc: tuple) -> MyWebElement:
        element = self._driver.find_element(*loc)
        element.location_once_scrolled_into_view
        return element

    def find_elements_by_loc(self, loc: tuple) -> List[MyWebElement]:
        return self._driver.find_elements(*loc)

    def quit(self):
        return self._driver.quit()


options = ChromeOptions()
prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
options.add_argument("--disable-blink-features=AutomationControlled")

server = Service(executable_path=setting.executable_path)

web_driver = webdriver.Chrome(service=server, options=options)
_driver = EventFiringWebDriver(web_driver, MyListen())
with open('stealth.min.js') as f:
    js = f.read()
_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

driver = UserWebDriver(_driver)
driver.get('https://www.baidu.com')

_loc_input = (By.CSS_SELECTOR, 'input.s_ipt')
_loc_submit = (By.CSS_SELECTOR, 'input#su')
driver.find_element_by_loc(_loc_input).send_keys('python')
driver.find_element_by_loc(_loc_submit).click()
print(driver.session_id)
time.sleep(2)
driver.quit()
