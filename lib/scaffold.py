"""
脚手架，实现一些装饰器，性能采集之类的功能
"""
import os
import time
from functools import wraps

from loguru import logger


def log(fun):
    _fun_name: str = fun.__name__
    _fun_module: str = fun.__module__
    _fun_code = fun.__code__

    @wraps(fun)
    def wrapper(*args, **kwargs):
        t = time.time()
        response = fun(*args, **kwargs)
        logger.debug(f'<{_fun_module}:{_fun_name}:{_fun_code.co_firstlineno + 1}> - duration: {time.time() - t}')
        return response

    return wrapper


def absolute_path(file: str):
    return os.path.join(os.path.dirname(__file__), file)
