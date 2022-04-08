"""
重载WebElement类
"""
from typing import List
from selenium.webdriver.remote.webelement import WebElement


class CustomWebElement(WebElement):
    def __init__(self, parent, id_):
        super().__init__(parent, id_)

    def find_element_by_loc(self, loc: tuple) -> WebElement:
        return self.find_element(*loc)

    def find_elements_by_loc(self, loc: tuple) -> List[WebElement]:
        return self.find_elements(*loc)
