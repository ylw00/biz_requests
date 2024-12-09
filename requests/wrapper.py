# -*- coding: UTF-8 -*-
# @author: ylw
# @file: wrapper
# @time: 2024/12/9
# @desc:
# import sys
# import os
import time
import traceback
from functools import wraps
from typing import cast, Optional, TypeVar, Callable, Any


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

class Wrapper:
    F = TypeVar('F', bound=Callable[..., Optional[Any]])

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
    def save_error_log(error_types: Optional[tuple] = None):
        """
        捕获自定义错误, 保存日志并抛出错误
        :error_types: tuple 目标错误
        """
        error_types = error_types or (Exception,)

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                except error_types as e:
                    logger.info(f"func_name : {func.__name__} , args : {args} , kwargs : {kwargs}")
                    raise e
                else:
                    return result

            return cast(Wrapper.F, wrapper)

        return decorator


if __name__ == '__main__':
    pass
