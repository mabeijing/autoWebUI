"""
脚手架，实现一些装饰器，性能采集之类的功能
"""
from functools import wraps
import os.path


def log(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        print('-----')
        response = fun(*args, **kwargs)
        print('######')
        return response

    return wrapper


def absolute_path(file: str):
    return os.path.join(os.path.dirname(__file__), file)
