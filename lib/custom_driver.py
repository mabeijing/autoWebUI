"""
selenium 4.1.3

UserWebDriver : 定义浏览器操作和元素发现

"""
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class UserWebDriver:
    def __init__(self, driver: WebDriver):
        self._driver = driver

    @property
    def original_driver(self) -> WebDriver:
        return self._driver

    @property
    def session_id(self) -> str:
        return self._driver.session_id

    def get(self, url: str):
        self._driver.get(url=url)

    def find_element_by_loc(self, loc: tuple) -> WebElement:
        element = self._driver.find_element(*loc)
        element.location_once_scrolled_into_view
        return element

    def find_elements_by_loc(self, loc: tuple) -> List[WebElement]:
        return self._driver.find_elements(*loc)

    def quit(self):
        return self._driver.quit()
