"""
脚手架，实现一些装饰器，性能采集之类的功能
"""
from functools import wraps


def log(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        print('-----')
        response = fun(*args, **kwargs)
        print('######')
        return response

    return wrapper
