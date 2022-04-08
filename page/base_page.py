"""
所有page的基类
实现page的一些公共方法，
"""
from selenium.webdriver.remote.webdriver import WebDriver

from lib.custom_driver import UserWebDriver


class BasePage(UserWebDriver):
    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver)
