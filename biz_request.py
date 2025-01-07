# -*- coding: UTF-8 -*-
# @author: ylw
# @file: request
# @time: 2024/12/10
# @desc:
from loguru import logger
from pandas import DataFrame
from typing import Optional, Callable, Union, List

from request import Headers, Session, RequestConfig
from db_engine import Engine, EngineConfig
from tools.wrapper import Wrapper


class Request:
    def __init__(self):
        self.request: Optional[Session] = None
        self.engine: Optional[Engine] = None
        self.headers: Optional[Headers] = None

    @staticmethod
    def create_request(retries=0, delay=0, encoding: Optional[str] = None, headers=None, http2=False):
        return Session(RequestConfig(
            retries=retries, delay=delay, encoding=encoding, headers=headers, http2=http2
        ))

    @staticmethod
    def create_engine(dbname, user, pwd, host, port, charset: str = 'utf8mb4'):
        return Engine(EngineConfig(
            dbname=dbname, user=user, pwd=pwd, host=host, port=port, charset=charset
        ))

    def init_request(self, retries=0, delay=0, encoding: Optional[str] = None, headers=None, http2=False):
        self.request = self.create_request(retries, delay, encoding, headers, http2)
        self.headers = self.request.headers
        return self

    def init_engine(self, dbname, user, pwd, host, port, charset: str = 'utf8mb4'):
        if hasattr(self, 'engine') and isinstance(self.engine, Engine):
            logger.info("禁止重复初始化 `Engine`;")
            return self

        self.engine = self.create_engine(dbname, user, pwd, host, port, charset)
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
    def safe_retry_until_done(callback_func: Callable, *args, retries=3, delay=3, **kwargs):
        """
        轮询直至返回正确得返回值
        业务示例:
            1, 循环等待报表导出完成
            ...
        """
        return Wrapper.retry_until_done(retries=retries, delay=delay)(callback_func)(*args, **kwargs)

    @staticmethod
    def safe_parse(callback_func: Callable, *args, **kwargs):
        """安全的解析"""
        return Wrapper.log_resp_if_exception(callback_func)(*args, **kwargs)

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
