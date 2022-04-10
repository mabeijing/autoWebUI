"""
自定义WebElement类
重载click。如果click打开了新窗口，将新窗口添加到session，得考虑多次打开
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

    def click_and_register_page(self, page) -> None:
        """
        :param page: SinglePage
        :return: None
        点击后，自动注册下SinglePage。并且将打开的句柄，添加到Session，先点击，后注册
        click_and_register_page(ContentPage1)
        click_and_register_page(ContentPage2)
        click_and_register_page(ContentPage3)
        依次注册3个page。
        未实现点击一次，注册多个Page。
        """
        _window_handles: set = set(self._parent.window_handles)
        super().click()
        new_handle: list = list(set(self._parent.window_handles) - _window_handles)
        assert len(new_handle) == 1
        Session.untreated_window_handle = new_handle[0]
        page(self._parent)
