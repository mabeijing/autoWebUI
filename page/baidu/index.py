from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from page.base_page import BasePage
from lib.scaffold import log
from lib.session import Session


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
        self.find_element_by_loc(self._loc_content).click_and_switch_window_handle()
        _ContentPage(self.original_driver)
        with _ContentPage(self.original_driver) as page:
            print(Session.page_map)
            print(page.title)

    def search(self, text: str):
        self._pom_search(text=text)


class _ContentPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @property
    @log
    def _pom_title(self):
        return self.title

    def current_title(self):
        print(self._pom_title)
        # return self._pom_url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
