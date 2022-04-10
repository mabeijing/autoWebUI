"""
selenium 4.1.3

UserWebDriver : 定义浏览器操作和元素发现

"""
import time
from typing import List

from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webdriver import WebDriver

from lib.session import Session
from lib.custom_element import CustomWebElement


class UserWebDriver:
    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._signature_code: str = self.__module__ + '.' + self.__class__.__name__
        self._session = Session(instance=self)

    @property
    def sleep(self):
        return time.sleep

    @property
    def switch_to(self) -> SwitchTo:
        return self._driver.switch_to

    @property
    def original_driver(self) -> WebDriver:
        return self._driver

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    @property
    def page_source(self) -> str:
        return self._driver.page_source

    @property
    def title(self) -> str:
        return self._driver.title

    @property
    def session_id(self) -> str:
        return self._driver.session_id

    @property
    def current_window_handle(self) -> str:
        return self._driver.current_window_handle

    @property
    def window_handles(self) -> List[str]:
        return self._driver.window_handles

    def start_client(self):
        self._driver.start_client()

    def get(self, url: str) -> None:
        self._driver.get(url=url)

    def back(self) -> None:
        self._driver.back()

    def forward(self) -> None:
        self._driver.forward()

    def refresh(self) -> None:
        return self._driver.refresh()

    def find_element_by_loc(self, loc: tuple) -> CustomWebElement:
        element = self._driver.find_element(*loc)
        # element.location_once_scrolled_into_view
        return element

    def find_elements_by_loc(self, loc: tuple) -> List[CustomWebElement]:
        return self._driver.find_elements(*loc)

    def execute_script(self, script, *args):
        return self._driver.execute_script(script, *args)

    def save_screenshot(self, filename: str) -> bool:
        return self._driver.save_screenshot(filename=filename)

    def close(self) -> None:
        self._driver.close()

    def quit(self) -> None:
        self._driver.quit()

    def show_session(self):
        return self._session.show()

    def clear_session(self):
        self._session.clear()

    def __getattribute__(self, item: str):
        """__attribute无法直接通过该方法调用，因为__attribute会被改写成_class__attribute属性，导致无法通过item直接获取"""
        item: str
        if item.startswith('_pom_'):
            self._session.switch_handle()
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        """直接读取self._driver的函数"""
        return getattr(self._driver, item)

    def print_self(self):
        return self.step_name
