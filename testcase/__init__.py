"""

tip:
case编写规则
1.  page类实例化，
    有2种场景，一种是page不会发生变化，可以用page = Page(driver)操作。
    还有一种场景，是page.operate之后才产生的，这里的Page()，就必须跟在operate后面创建。
    page已经单例。推荐每次都Page(driver).operate
"""
