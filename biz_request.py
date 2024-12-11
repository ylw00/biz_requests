# -*- coding: UTF-8 -*-
# @author: ylw
# @file: request
# @time: 2024/12/10
# @desc:
# import sys
# import os
from abc import ABC, abstractmethod
from typing import Optional, Callable

from request import Session, RequestConfig
from db_engine import Engine, EngineConfig

from tools.wrapper import Wrapper


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))


class Request:
    def __init__(self):
        self.request: Optional[Session] = None
        self.engine: Optional[Engine] = None

    def set_request(self, retries=0, delay=0, headers=None, encoding=None, http2=False):
        self.request = Session(RequestConfig(
            retries=retries, delay=delay, headers=headers, r_encoding=encoding, http2=http2
        ))
        return self

    def set_engine(self, dbname, user, pwd, host, port, charset):
        self.engine = Engine(EngineConfig(
            dbname=dbname, user=user, password=pwd, host=host, port=port, charset=charset
        ))
        return self


class BizRequest(Request, ABC):
    """
    在这里拓展业务代码/封装
    """

    def __init__(self):
        if type(self) is BizRequest:
            raise TypeError("BizRequest cannot be instantiated directly.")
        super(BizRequest, self).__init__()

    @staticmethod
    def safe_return(callback_func: Callable, retries=3, delay=10, *args, **kwargs):
        """安全的解析：业务demo: 1,等待报表导出完成"""
        return Wrapper.retry2success(retries=retries, delay=delay)(callback_func)(*args, **kwargs)

    @staticmethod
    def safe_parse(callback_func: Callable, *args, **kwargs):
        """安全的解析"""
        return Wrapper.save_resp_error(callback_func)(*args, **kwargs)

    # @abstractmethod
    def start(self):
        ...

    # @abstractmethod
    def init_attribute(self):
        ...


if __name__ == '__main__':
    ...
