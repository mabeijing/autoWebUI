"""
重载WebElement类
click()可能会弹出新页面。
"""
from typing import List
from selenium.webdriver.remote.webelement import WebElement

from lib.session import Session


class CustomWebElement(WebElement):
    def __init__(self, parent, id_):
        super().__init__(parent, id_)

    def find_element_by_loc(self, loc: tuple) -> WebElement:
        return self.find_element(*loc)

    def find_elements_by_loc(self, loc: tuple) -> List[WebElement]:
        return self.find_elements(*loc)

    def click(self) -> None:
        _windows_handlers: set = set(self._parent.window_handles)
        _current_windows_handler: str = self._parent.current_window_handle
        super().click()
        new_tab: set = set(self._parent.window_handles) - _windows_handlers
        if len(new_tab) == 1:
            Session.current_window_handle = list(new_tab)[0]
