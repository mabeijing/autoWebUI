"""
实现页面功能函数入口
"""
from page.baidu.index import IndexPage as BaiduIndexPage
from page.baidu.content import ContentPage

from page.ws.index import IndexPage as WsIndexPage

__all__ = [BaiduIndexPage, ContentPage, WsIndexPage]
