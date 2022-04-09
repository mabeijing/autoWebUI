from selenium.webdriver.remote.webdriver import WebDriver

from page.base_page import BasePage
from lib.scaffold import log


class ContentPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @property
    @log
    def _pom_title(self):
        return self.title

    def current_title(self):
        print(self._pom_title)
        # return self._pom_url
