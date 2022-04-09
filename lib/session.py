from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

"""
Session.DEFAULT_DRIVER: 保存浏览器刚拉起的时候的driver
Session.DEFAULT_DRIVER: 保存浏览器刚拉起的时候的默认window_handle
Session.NEW_FLAG:   刚拉起浏览器的第一个项目

Session.main_app_handle:   用来标记项目的主window_handle，就是主项目句柄
    定义。项目有主操作页面，大部分Page都在该window_handle下，其他跳转Page操作完还会回到主页面。
    如果某些操作后，主页面切换了。需要重新指定主页面。
    在该项目下的新增Page，默认window_handle都是main_app_handle
    main_app_handle = {'baidu': 'window_handle1', 'sogou': 'window_handle2'}
    
Session.page_map:   保存page._signature_code和window_handle的映射
    核心map，是实现切换的主要记录表，获取到的数据需要检查是否有效，就是看下是否in driver.window_handles
    基本上一个项目的所有page都来自于main_app_handle，值都一样
    有些是跳转page，值与main_app_handle不一样。这个值是untreated_window_handles处理的
    page_map = {'page.baidu.index.IndexPage': 'window_handle'}

Session.untreated_window_handles:   保存未处理的window_handle。
    高优先级处理，一旦这里有值，下一次page的绑定，会优先和这里绑定。所以，这里的值一定要控制绑定
    添加后第一时间要做处理，比如click后打开N个window_handle，就必须实例化指定Page来绑定这个未处理窗口。否则会产生错误绑定
        大部分情况下，Session.untreated_window_handles只有1个值，比如click跳转新tab展示详情，则实例化DetailPage来绑定这个handle
        少数情况下，untreated_window_handles有多个值，pop()取值，后进先出的原则一次和Page进行绑定。
        特殊情况下，click后弹出广告window，未弹出指定window，则Page绑定不会失败，但是Page.operation会失败。
        

使用说明
1.  根据每个page注册map
2.  根据page._signature_code区分项目注册map
3.  page调用_pom_方法时，会调用exchange_handle()
"""


def handle_signature_code(signature_code: str) -> str:
    data: list = signature_code.split('.')
    assert data[0] == 'page'
    return data[1]


class Session:
    DEFAULT_DRIVER: Optional[WebDriver] = None
    DEFAULT_WINDOW_HANDLE: Optional[str] = None
    NEW_FLAG: bool = True

    main_app_handle: dict = {}
    page_map: dict = {}
    untreated_window_handles: list = []

    @staticmethod
    def show() -> dict:
        """查看当前Session数据"""
        return {
            'main_app_handle': Session.main_app_handle,
            'page_map': Session.page_map,
            'untreated_window_handles': Session.untreated_window_handles
        }

    @staticmethod
    def clear():
        """清理浏览器打开的window，继续下一个测试，浏览器不关闭场景"""
        all_handles: list = list(set(Session.DEFAULT_DRIVER.window_handles) - {Session.DEFAULT_WINDOW_HANDLE})
        for handle in all_handles:
            Session.DEFAULT_DRIVER.switch_to.window(handle)
            Session.DEFAULT_DRIVER.close()
        Session.page_map.clear()
        Session.main_app_handle.clear()
        Session.untreated_window_handles.clear()
        Session.NEW_FLAG = True

    @staticmethod
    def reset():
        """初始化Session数据，用于需要新打开浏览器的场景"""
        Session.NEW_FLAG = True
        Session.DEFAULT_DRIVER = None
        Session.DEFAULT_WINDOW_HANDLE = None
        Session.page_map.clear()
        Session.main_app_handle.clear()
        Session.untreated_window_handles.clear()

    def __init__(self, instance):
        """
        :type instance: BasePage, UserWebDriver, WebDriver
        """
        self.instance = instance
        self.__setup()

    def __setup(self):
        """
        根据page._signature_code去page_map取handle
            如果handle不存在，认为是首次访问，或者绑定未处理page。
                注意，这里untreated_window_handles处理优先级高于new_window，所以一旦操作产生window。必须第一时间处理。
                如果len(untreated_window_handles) > 0
                    untreated_window_handles.pop()，就使用该handle创建map
                否则需要新增window
                    如果Page的app已经存在，直接切换到main_window_handle，创建map
                    如果Page是新app。new_tab后切入，创建map，创建main_window_handle
            否则如果handle in driver.windows_handles里，认为浏览器窗口还在，直接切换
            否则报错。被关闭的page会主动去掉map，在map里面的page，都认为未关闭。map存在，但是handle不存在是错误场景。

        """
        window_handle: Optional[str] = Session.page_map.get(self.instance._signature_code, None)
        if not window_handle:
            if len(Session.untreated_window_handles) > 0:
                handle: str = Session.untreated_window_handles.pop()
                self.instance.switch_to.window(handle)
                Session.page_map[self.instance._signature_code] = handle
            else:
                app: str = handle_signature_code(self.instance._signature_code)
                main_handle: Optional[str] = Session.main_app_handle.get(app, None)
                if not main_handle:
                    _window_handles: set = set(self.instance.window_handles)
                    self.instance.switch_to.new_window('tab')
                    new_handle: list = list(set(self.instance.window_handles) - _window_handles)
                    assert len(new_handle) == 1, f'new_window should open one window_handle but {new_handle}.'
                    self.instance.switch_to.window(new_handle[0])
                    Session.main_app_handle[app] = new_handle[0]
                    Session.page_map[self.instance._signature_code] = new_handle[0]
                else:
                    if Session.NEW_FLAG:
                        self.instance.switch_to.window(Session.DEFAULT_WINDOW_HANDLE)
                        Session.page_map[self.instance._signature_code] = Session.DEFAULT_WINDOW_HANDLE
                        Session.NEW_FLAG = False
                    else:
                        self.instance.switch_to.window(main_handle)
                        Session.page_map[self.instance._signature_code] = main_handle

        elif window_handle in self.instance.window_handles:
            self.instance.switch_to.window(window_handle)

        else:
            print(self.instance._signature_code)
            print(Session.show())
            raise ValueError(f'the map exist but the browser window_handle is not exist')

    def switch_handle(self):
        """特殊方法_pom_开头的，会调用该方法切换窗口"""
        handle = Session.page_map.get(self.instance._signature_code, None)
        assert handle
        self.instance.switch_to.window(handle)

    def remove(self):
        """移除page的特征码映射"""
        if self.instance._signature_code in Session.page_map.keys():
            Session.page_map.pop(self.instance.page_name)
