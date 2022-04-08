"""
重载ShadowRoot类
"""
from typing import List
from selenium.webdriver.remote.shadowroot import ShadowRoot


class CustomShadowRoot(ShadowRoot):
    def __init__(self, session, id_):
        super().__init__(session, id_)

    def find_element_by_loc(self, loc: tuple) -> ShadowRoot:
        return self.find_element(*loc)

    def find_elements_by_loc(self, loc: tuple) -> List[ShadowRoot]:
        return self.find_elements(*loc)
