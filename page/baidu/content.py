from selenium.webdriver.remote.webdriver import WebDriver

from page.base_page import BasePage
from lib.scaffold import log


class ContentPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @log
    def _pom_url(self):
        return self.current_url

    def get_url(self):
        print(self._pom_url())
        self.show_session()
        # return self._pom_url
