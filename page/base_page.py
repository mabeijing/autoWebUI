"""
所有page的基类
实现page的一些公共方法，
"""
from selenium.webdriver.remote.webdriver import WebDriver

from lib.custom_driver import UserWebDriver


class BasePage(UserWebDriver):
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver)
