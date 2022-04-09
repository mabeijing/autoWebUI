import time

import pytest
import allure
from selenium.webdriver.remote.webdriver import WebDriver

from page import BaiduIndexPage, SoGouIndexPage


class TestBaiduDemo:

    @allure.title('demo')
    def test_baidu_demo(self, driver: WebDriver):
        SoGouIndexPage(driver=driver).search('杜甫')
        BaiduIndexPage(driver=driver).search('李白')
        time.sleep(3)
        SoGouIndexPage(driver=driver).search('北京')
        time.sleep(5)


if __name__ == '__main__':
    pytest.main(['-s'])
