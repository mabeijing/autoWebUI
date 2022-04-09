from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from page.base_page import BasePage
from lib.scaffold import log


class IndexPage(BasePage):
    _loc_input_box = (By.CSS_SELECTOR, 'input.s_ipt')
    _loc_submit_btn = (By.CSS_SELECTOR, 'input#su')
    _loc_content = (By.CSS_SELECTOR, 'div#content_left h3 a')

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @log
    def _pom_search(self, text: str):
        self.get('https://www.baidu.com')
        self.find_element_by_loc(self._loc_input_box).send_keys(text)
        self.find_element_by_loc(self._loc_submit_btn).click()
        self.find_element_by_loc(self._loc_content).click()

    def search(self, text: str):
        self._pom_search(text=text)
