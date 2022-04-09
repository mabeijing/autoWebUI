from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

"""
解决窗口自动切换
1.  如果知道操作后，存在窗口切换，直接切换
2.  如果知道操作后，不会窗口切换，默认当前窗口
3.  recent_window_handle  上一次操作的窗口，产生切换是记录
4.  current_window_handle   当前页面的句柄

session_dict = {'Page.instance._signature_code': current_window_handle}

最简单的用法
1，打开page，检查在不在map，如果在map，等值等于当前窗口，不处理
2，打开page，检查在不在map，如果在map，值不等于当前窗口，表示已经失效
3，打开page，检查在不在map，如果不在map，添加上当前窗口
配合使用
1，如果存在点击新窗口跳转的，直接初始化page

"""


class Session:
    DEFAULT_DRIVER: Optional[WebDriver] = None
    DEFAULT_WINDOW_HANDLE: Optional[str] = None

    page_map: dict = {}
    recent_window_handle: Optional[str] = None
    current_window_handle: Optional[str] = None
    current_signature_code: Optional[str] = None

    @staticmethod
    def show():
        return Session.page_map

    @staticmethod
    def clear():
        """
        静态方法，清理多余的window句柄。只保留拉起浏览器的时候默认句柄。
        """
        all_handles: list = list(set(Session.DEFAULT_DRIVER.window_handles) - {Session.DEFAULT_WINDOW_HANDLE})
        for handle in all_handles:
            Session.DEFAULT_DRIVER.switch_to.window(handle)
            Session.DEFAULT_DRIVER.close()
        Session.page_map.clear()

    def __init__(self, instance):
        """
        :type instance: BasePage, UserWebDriver, WebDriver
        """
        self.instance = instance
        self.__setup()

    def __setup(self):
        """
        page特征码如果存在，切换到已有window_handle
        page特征码如果不存在
            如果有available_window_handle可用句柄，直接将page特征码和available句柄做映射，并且重置available_window_handle=None
            如果没有available_window_handle，需要new一个window_handle，
        """
        window_handle = Session.page_map.get(self.instance._signature_code, None)
        if not window_handle:
            # 如果没有map，表示新page
            # 新page有2个情况，一个是当前页面已经是对的了，一个是需要切换
            pass
        else:
            if window_handle != Session.current_window_handle:
                # 表示老page，但是浏览器不在目标窗口
                self.instance.switch_to.window(window_handle)
            else:
                # 表示老page，浏览器当前窗口就是目标窗口
                pass

    def add(self):
        """将当前页面的句柄 映射 page的特征码"""
        Session.page_map[self.instance._signature_code] = self.instance.current_window_handle

    def remove(self):
        """移除page的特征码映射"""
        if self.instance._signature_code in Session.page_map.keys():
            Session.page_map.pop(self.instance.page_name)
