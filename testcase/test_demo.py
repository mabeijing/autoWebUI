import time

import pytest
import allure
from selenium.webdriver.remote.webdriver import WebDriver

from page import BaiduIndexPage, SoGouIndexPage, BaiduContentPage


class TestBaiduDemo:

    @allure.title('demo')
    def test_baidu_demo(self, driver: WebDriver):
        SoGouIndexPage(driver=driver).search('杜甫')
        time.sleep(2)
        BaiduIndexPage(driver=driver).search('李白')
        time.sleep(2)
        print(BaiduContentPage(driver=driver).get_title())
        time.sleep(2)
        SoGouIndexPage(driver=driver).search('北京')
        time.sleep(2)
        BaiduIndexPage(driver=driver).search('二狗')
        print(BaiduContentPage(driver=driver).get_title())
        time.sleep(5)


if __name__ == '__main__':
    pytest.main(['-s'])
