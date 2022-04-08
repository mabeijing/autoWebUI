"""
selenium 4.1.3

UserWebDriver : 定义浏览器操作和元素发现

"""
import time
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from lib.session import Session


class UserWebDriver:
    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._signature_code: str = self.__module__ + '.' + self.__class__.__name__
        self._session = Session(instance=self)

    @property
    def sleep(self):
        return time.sleep

    @property
    def switch_to(self):
        return self._driver.switch_to

    @property
    def original_driver(self) -> WebDriver:
        return self._driver

    @property
    def current_url(self):
        return self._driver.current_url

    @property
    def session_id(self) -> str:
        return self._driver.session_id

    @property
    def current_window_handle(self):
        return self._driver.current_window_handle

    @property
    def window_handles(self):
        return self._driver.window_handles

    def get(self, url: str):
        self._driver.get(url=url)

    def find_element_by_loc(self, loc: tuple) -> WebElement:
        element = self._driver.find_element(*loc)
        # element.location_once_scrolled_into_view
        return element

    def find_elements_by_loc(self, loc: tuple) -> List[WebElement]:
        return self._driver.find_elements(*loc)

    def quit(self):
        return self._driver.quit()

    def close(self):
        return self._driver.close()

    def show_session(self):
        return self._session.show()

    def clear_session(self):
        self._session.clear()

    def __getattribute__(self, item: str):
        """__attribute无法直接通过该方法调用，因为__attribute会被改写成_class__attribute属性，导致无法通过item直接获取"""
        item: str
        if item.startswith('_pom_'):
            self._session.add()
            return object.__getattribute__(self, item)
        else:
            return super().__getattribute__(item)
