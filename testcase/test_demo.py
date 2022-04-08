import pytest
import allure
from selenium.webdriver.remote.webdriver import WebDriver

from page.baidu.index import IndexPage


class TestBaiduDemo:

    @allure.title('demo')
    def test_baidu_demo(self, driver: WebDriver):
        IndexPage(driver=driver).search('python')


if __name__ == '__main__':
    pytest.main(['-s'])
