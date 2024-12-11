# -*- coding: UTF-8 -*-
# @author: ylw
# @file: request
# @time: 2024/12/10
# @desc:
from pandas import DataFrame
from abc import ABC, abstractmethod
from typing import Optional, Callable, Union, List

from request import Session, RequestConfig
from db_engine import Engine, EngineConfig
from tools.wrapper import Wrapper


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


class BizRequest(Request):
    """
    在这里拓展业务代码/封装
    """

    def __init__(self):
        if type(self) is BizRequest:
            raise TypeError("BizRequest cannot be instantiated directly.")
        super(BizRequest, self).__init__()

    @staticmethod
    def safe_retry_until_success(callback_func: Callable, *args, retries=3, delay=3, **kwargs):
        """安全的解析：业务demo: 1,等待报表导出完成"""
        return Wrapper.retry_until_success(retries=retries, delay=delay)(callback_func)(*args, **kwargs)

    @staticmethod
    def safe_parse(callback_func: Callable, *args, **kwargs):
        """安全的解析"""
        return Wrapper.save_resp_error(callback_func)(*args, **kwargs)

    def save2db(self, item: Union[dict, List[dict], DataFrame]):
        """数据入库"""

    def init_attribute(self):
        """初始化属性到self"""
        ...

    def start(self):
        """主入口函数"""
        ...


if __name__ == '__main__':
    ...
