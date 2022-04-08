import time

import pytest
import allure
from selenium.webdriver.remote.webdriver import WebDriver

from page.baidu import IndexPage, ContentPage


class TestBaiduDemo:

    @allure.title('demo')
    def test_baidu_demo(self, driver: WebDriver):
        IndexPage(driver=driver).search('java')
        ContentPage(driver=driver).get_url()
        IndexPage(driver=driver).search('python')
        IndexPage(driver=driver).clear_session()
        time.sleep(5)


if __name__ == '__main__':
    pytest.main(['-s'])
