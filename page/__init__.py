"""
实现页面功能函数入口
page的结构一定是page/项目/模块/功能页面。page.baidu.myOrder.orderList
"""
from page.baidu.index import IndexPage as BaiduIndexPage
from page.baidu.index import ContentPage as BaiduContentPage
from page.baidu.content import ContentPage

from page.sogou.index import IndexPage as SoGouIndexPage

__all__ = [BaiduIndexPage, BaiduContentPage, ContentPage, SoGouIndexPage]
