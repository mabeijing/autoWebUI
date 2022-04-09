import time

import pytest
import allure
from selenium.webdriver.remote.webdriver import WebDriver

from page import BaiduIndexPage, ContentPage, WsIndexPage


class TestBaiduDemo:

    @allure.title('demo')
    def test_baidu_demo(self, driver: WebDriver):
        BaiduIndexPage(driver=driver).search('李白')
        BaiduIndexPage(driver=driver).search('杜甫')
        WsIndexPage(driver=driver).login()
        time.sleep(5)


if __name__ == '__main__':
    pytest.main(['-s'])
