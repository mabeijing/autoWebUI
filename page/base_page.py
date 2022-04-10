"""
所有page的基类
实现page的一些公共方法，
Page要分成2类。一类是固定的BasePage，创建后不会再变化。比如index，除非测试结束，否则不会变化。单例Page，id相同
             还有一类是可变的InnerPage，每次点击后，弹窗就是可变的，弹窗操作完需要关闭，下次打开，又是新的。非单例Page，id不同
             SinglePage类，必须定义在创建这个类的模块下。
                比如，IndexPage(BasePage)下click触发ContentPage(InnerPage),这两个类最好放在一个模块下，防止循环导入问题

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


class InnerPage(UserWebDriver):
    # instance = None

    # def __new__(cls, *args, **kwargs):
    #     if not cls.instance:
    #         cls.instance = super().__new__(cls)
    #     return cls.instance

    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver)
