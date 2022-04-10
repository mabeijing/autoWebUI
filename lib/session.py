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
    
Session.page_map:   保存page._signature_code和window_handle的映射，属于自动映射关系
    核心map，是实现切换的主要记录表，获取到的数据需要检查是否有效，就是看下是否in driver.window_handles
    基本上一个项目的所有page都来自于main_app_handle，值都一样
    有些是跳转page，值与main_app_handle不一样。这个值是untreated_window_handles处理的
    page_map = {'page.baidu.index.IndexPage': 'window_handle'}

Session.page_name_map : 主要用来保存page实例的的自定义名字， 属于指定映射关系
    通过修改单例实例的page_name,修改当前需要访问什么window_handle
    page_name_map = {hash('百度李白详情'): 'window_handle1', hash('百度杜甫详情'): 'window_handle2'}

Session.untreated_window_handle:   保存未处理的window_handle。
    高优先级处理，一旦这里有值，下一次page的绑定，会优先和这里绑定。所以，这里的值一定要控制绑定
    需要配合element.click_and_register_page(InnerPage)实现
    只支持点击一次，弹出一个未处理窗口场景，点击多次，默认切换到最后打开的窗口

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
    page_name_map: dict = {}
    untreated_window_handle: Optional[str] = None

    @staticmethod
    def show() -> dict:
        """查看当前Session数据"""
        return {
            'driver': Session.DEFAULT_DRIVER,
            'default_window_handle': Session.DEFAULT_WINDOW_HANDLE,
            'main_app_handle': Session.main_app_handle,
            'page_map': Session.page_map,
            'untreated_window_handles': Session.untreated_window_handle
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
        Session.untreated_window_handle = None
        Session.NEW_FLAG = True

    @staticmethod
    def reset():
        """初始化Session数据，用于需要新打开浏览器的场景"""
        Session.NEW_FLAG = True
        Session.DEFAULT_DRIVER = None
        Session.DEFAULT_WINDOW_HANDLE = None
        Session.page_map.clear()
        Session.main_app_handle.clear()
        Session.untreated_window_handle = None

    def __init__(self, instance):
        """
        :type instance: BasePage, UserWebDriver, WebDriver
        """
        self.instance = instance
        self.signature_code: str = instance._signature_code
        self.page_id: int = id(self)
        # print(f'{self.signature_code} -- id:{self.page_id}')
        self.__setup()

    def __setup(self):
        """
        通过 page.signature_code, page_name 来控制切换。
        注意，这里untreated_window_handle处理优先级高于new_window
            如果untreated_window_handle有值，说明在绑定InnerPage类
                更新page_map,Session.page_map[self.signature_code] = untreated_window_handle
            否则根据signature_code去page_map取handle。
                如果handle不存在，认为是首次访问，或者绑定未处理page。
                否则需要新增window
                    如果Page的app已经存在，直接切换到main_window_handle，创建map
                    如果Page是新app。new_tab后切入，创建map，创建main_window_handle
        否则如果handle in driver.windows_handles里，认为浏览器窗口还在，直接切换
        否则报错。被关闭的page会主动去掉map，在map里面的page，都认为未关闭。map存在，但是handle不存在是错误场景。

        """
        if Session.untreated_window_handle:
            # 绑定InnerPage类
            handle: str = Session.untreated_window_handle
            Session.untreated_window_handle = None
            self.instance.switch_to.window(handle)
            Session.page_map[self.signature_code] = handle
        else:
            # 新增/切换BasePage类
            window_handle: Optional[str] = Session.page_map.get(self.signature_code, None)
            if not window_handle:
                # 浏览器没有当前page的handle映射
                app: str = handle_signature_code(self.signature_code)
                main_handle: Optional[str] = Session.main_app_handle.get(app, None)
                if not main_handle:
                    # 新项目
                    if Session.NEW_FLAG:
                        # 浏览器首次操作
                        Session.main_app_handle[app] = Session.DEFAULT_WINDOW_HANDLE
                        Session.page_map[self.signature_code] = Session.DEFAULT_WINDOW_HANDLE
                        Session.NEW_FLAG = False
                    else:
                        _window_handles: set = set(self.instance.window_handles)
                        self.instance.switch_to.new_window('tab')
                        new_handle: list = list(set(self.instance.window_handles) - _window_handles)
                        assert len(new_handle) == 1, f'new_window should open one window_handle but {new_handle}.'
                        self.instance.switch_to.window(new_handle[0])
                        Session.main_app_handle[app] = new_handle[0]
                        Session.page_map[self.signature_code] = new_handle[0]
                else:
                    # 已打开项目
                    self.instance.switch_to.window(main_handle)
                    Session.page_map[self.signature_code] = main_handle

            elif window_handle in self.instance.window_handles:
                self.instance.switch_to.window(window_handle)
            else:
                print(Session.show())
                raise ValueError(f'the map exist but the browser window_handle is not exist')

    def switch_handle(self):
        """特殊方法_pom_开头的，会调用该方法切换窗口"""
        handle = Session.page_map.get(self.signature_code, None)
        assert handle
        self.instance.switch_to.window(handle)

    def remove(self):
        """移除page的特征码映射"""
        if self.signature_code in Session.page_map.keys():
            Session.page_map.pop(self.instance.page_name)
