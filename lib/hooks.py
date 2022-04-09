import os
import time

# import allure
from loguru import logger
from selenium.webdriver.support.events import AbstractEventListener

# Global execution speed
TIME_INTERVAL = 0.1


class MyListen(AbstractEventListener):
    window_context_set = set()

    def before_navigate_to(self, url, driver):
        time.sleep(TIME_INTERVAL)

    def after_navigate_to(self, url, driver):
        logger.debug(f'navigate_to: {url}')

    def before_find(self, by, value, driver):
        time.sleep(TIME_INTERVAL)

    def after_find(self, by, value, driver):
        logger.debug(f'find_out_element: {by, value}')

    def after_click(self, element, driver):
        logger.debug(f'click_element: {element}')

    def after_change_value_of(self, element, driver):
        logger.debug(f'change_element_value: {element}')

    def on_exception(self, exception, driver):
        """Catch the exception of selenium operation element failure, and other exceptions will not be caught"""
        pass

    def after_close(self, driver):
        logger.debug(f'window_handles: {driver.window_handles}')

    def before_execute_script(self, script: str, driver):
        time.sleep(TIME_INTERVAL)
        if script.startswith('window.open'):
            logger.debug(f'The JS script to be executed is:{script}')
            self.window_context_set = set(driver.window_handles)

    def after_execute_script(self, script, driver):
        if script.startswith('window.open'):
            window_handles = set(driver.window_handles)
            context = list(window_handles - self.window_context_set)
            if len(context) == 1:
                driver.switch_to.window(context[0])
            else:
                driver.switch_to.window(context.pop())
