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
from collections import OrderedDict
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


def get_traceback_str(error: Exception) -> str:
    return '\n'.join([i.strip().replace('    ', '  ') for i in traceback.format_tb(error.__traceback__)])


class WrapperKeyCache(OrderedDict):
    def __init__(self, max_size):
        super().__init__()
        self.max_size = max_size

    def get(self, key):
        if key in self:
            self.move_to_end(key)
            return self[key]
        return None

    def set(self, key, value):
        if key in self:
            self.move_to_end(key)
            return
        if len(self) >= self.max_size:
            self.popitem(last=False)
        self[key] = value


class Wrapper:
    F = TypeVar('F', bound=Callable[..., Optional[Any]])
    __cache = WrapperKeyCache(100)

    def __new__(cls, *args, **kwargs):  # 禁止继承
        if cls is not Wrapper:
            raise TypeError("Wrapper class cannot be subclassed.")
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):  # 禁止通过 __init__ 实例化
        raise NotImplementedError("Wrapper class cannot be instantiated directly.")

    @staticmethod
    def ignore_resource_warnings(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with warnings.catch_warnings(record=True):
                warnings.simplefilter('ignore', ResourceWarning)
                return func(*args, **kwargs)

        return cast(Wrapper.F, wrapper)

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
    def retry(retries=3, delay=0):
        def decorator(func):
            cache_key = (func, retries, delay)
            if cache_key in Wrapper.__cache:
                return Wrapper.__cache.get(cache_key)

            @wraps(func)
            def wrapper(*args, **kwargs):
                error = None
                error_str = None

                for retry_index in range(retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        error = e
                        error_str = traceback.format_exc()
                        print(error_str)
                        if delay > 0:
                            time.sleep(delay)
                logger.info(f"Traceback:\n{error_str}")
                raise error

            ww = cast(Wrapper.F, wrapper)
            Wrapper.__cache.set(cache_key, ww)
            return ww

        return decorator

    @staticmethod
    def retry2success(retries=3, delay=10, *, desc: str = None):
        """
        装饰器：在指定次数内尝试调用被装饰的函数，每次尝试之间有指定的停留时间。
        :param retries: 尝试次数
        :param delay: 每次尝试后的停留时间（秒）
        :param desc: 没有正确返回的返回值的简述提示
        """
        _desc = desc or 'None'

        def decorator(func):
            cache_key = (func, retries, delay)
            if cache_key in Wrapper.__cache:
                return Wrapper.__cache.get(cache_key)

            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(retries):
                    result: Optional[Any] = func(*args, **kwargs)
                    if result is None:
                        time.sleep(delay)
                        continue
                    return result
                logger.info(f"简述: {_desc};")
                raise ValueError(f"函数没有返回有效值; 简述: {_desc};")

            ww = cast(Wrapper.F, wrapper)
            Wrapper.__cache.set(cache_key, ww)
            return ww

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
        cache_key = (func,)
        if cache_key in Wrapper.__cache:
            return Wrapper.__cache.get(cache_key)

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.info(f"func_name: {func.__name__}; - args: {args}; - kwargs: {kwargs}")
                raise e

        ww = cast(Wrapper.F, wrapper)
        Wrapper.__cache.set(cache_key, ww)
        return ww


if __name__ == '__main__':
    ...
