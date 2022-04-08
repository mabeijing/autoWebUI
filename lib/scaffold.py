"""
脚手架，实现一些装饰器，性能采集之类的功能
"""
import os
import time
from functools import wraps

from loguru import logger

import setting


def setup_loguru(log_file: str = None):
    log_name: str = time.strftime('%Y%m%d%H%M%S', time.localtime())
    log_file: str = log_file if log_file else f'runtime_{log_name}.log'
    root = os.path.dirname(os.path.dirname(__file__))
    log_path = os.path.join(root, 'static', 'run_log', log_file)
    logger.add(log_path, level=setting.LOG_LEVEL, encoding='utf-8', enqueue=True)


def log(fun):
    _fun_name: str = fun.__name__
    _fun_module: str = fun.__module__
    _fun_code = fun.__code__

    @wraps(fun)
    def wrapper_log(*args, **kwargs):
        t = time.time()
        response = fun(*args, **kwargs)
        logger.debug(f'<{_fun_module}:{_fun_name}:{_fun_code.co_firstlineno + 1}> - duration: {time.time() - t}')
        return response

    return wrapper_log


def absolute_path(file: str):
    return os.path.join(os.path.dirname(__file__), file)
