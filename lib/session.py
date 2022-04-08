from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

"""
根据page的特征码_signature_code和window_handle做映射。

在拉起浏览器的时候，保存当前driver，window_handle，设置current_window_handle = DEFAULT_WINDOW_HANDLE
实例化Page的时候，如果查不到特征码，切换到current_window_handle，并且保存_session_dict。否则直接切换到对应的window_handle

session_dict = {'Page.instance._signature_code': current_window_handle}
"""


class Session:
    DEFAULT_DRIVER: Optional[WebDriver] = None
    DEFAULT_WINDOW_HANDLE: Optional[str] = None

    current_window_handle: Optional[str] = None

    _session_dict: dict = {}

    def __init__(self, instance):
        """
        :type instance: BasePage, UserWebDriver, WebDriver
        """
        self.instance = instance
        self.__setup()

    def __setup(self):
        """
        Page如果存在，切换到已有window_handle
        Page如果不存在，切换到Session.current_window_handle。并且创建Page的特征码映射。
        """
        window_handle = Session._session_dict.get(self.instance._signature_code, None)
        if window_handle:
            self.instance.switch_to.window(window_handle)
        else:
            self.instance.switch_to.window(Session.current_window_handle)
            Session._session_dict[self.instance._signature_code] = Session.current_window_handle

    def add(self):
        """将当前页面的句柄 映射 page的特征码"""
        Session._session_dict[self.instance._signature_code] = self.instance.current_window_handle

    def remove(self):
        """移除page的特征码映射"""
        if self.instance.page_name in Session._session_dict.keys():
            Session._session_dict.pop(self.instance.page_name)

    @staticmethod
    def clear():
        """
        静态方法，清理多余的window句柄。只保留拉起浏览器的时候默认句柄。
        """
        all_handles: list = list(set(Session.DEFAULT_DRIVER.window_handles) - {Session.DEFAULT_WINDOW_HANDLE})
        for handle in all_handles:
            Session.DEFAULT_DRIVER.switch_to.window(handle)
            Session.DEFAULT_DRIVER.close()
        Session._session_dict.clear()
        Session.current_window_handle = None

    @staticmethod
    def show():
        print(Session._session_dict, Session.current_window_handle)
        return Session._session_dict
