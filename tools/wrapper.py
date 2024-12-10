# -*- coding: UTF-8 -*-
# @author: ylw
# @file: wrapper
# @time: 2024/12/9
# @desc:
# import sys
# import os
import time
import traceback
import warnings
from functools import wraps
from typing import cast, Optional, TypeVar, Callable, Any
from loguru import logger


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

def is_instance_method(func):
    """
    判断回调函数是否是实例方法
    :param func: 待检查的回调函数
    :return: 如果是实例方法则返回 True，否则返回 False
    """
    return hasattr(func, '__self__') and func.__self__ is not None


class Wrapper:
    F = TypeVar('F', bound=Callable[..., Optional[Any]])

    @staticmethod
    def ignore_resource_warnings(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with warnings.catch_warnings(record=True):
                warnings.simplefilter('ignore', ResourceWarning)
                return func(*args, **kwargs)

        return cast(Wrapper.F, wrapper)

    @staticmethod
    def __traceback_str(error: Exception) -> str:
        return '\n'.join([i.strip().replace('    ', '  ') for i in traceback.format_tb(error.__traceback__)])

    @staticmethod
    def no_exception(func):
        """不异常"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                return None

        return cast(Wrapper.F, wrapper)

    @staticmethod
    def retry(retries=3, delay=0, *, save_error_log: bool = True):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                save_log_index = retries - 1

                for retry_index in range(retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if save_error_log:
                            erroe_str = f"{Wrapper.__traceback_str(e)}\n{retry_index + 1}/{retries}"
                            if retry_index == save_log_index:
                                logger.info(erroe_str)
                                raise e
                            print(erroe_str)
                        if delay > 0:
                            time.sleep(delay)

            return cast(Wrapper.F, wrapper)

        return decorator

    @staticmethod
    def save_req_error(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                logger.info(f"func_name : {func.__name__}; - Text: {self.text};")
                raise e

        return cast(Wrapper.F, wrapper)

    @staticmethod
    def save_resp_error(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.info(f"func_name: {func.__name__}; - args: {args}; - kwargs: {kwargs}")
                raise e

        return cast(Wrapper.F, wrapper)


if __name__ == '__main__':
    pass
