# -*- coding: UTF-8 -*-
# @author: ylw
# @file: request
# @time: 2025/1/23
# @desc:
# import sys
# import os
from loguru import logger
from typing import Optional

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from .headers import Headers
from .session import Session, SessionConfig
from db_engine import Engine, EngineConfig


class Request:
    def __init__(self):
        self.request: Optional[Session] = None
        self.engine: Optional[Engine] = None
        self.headers: Optional[Headers] = None

    @staticmethod
    def create_request(retries=0, delay=0, encoding: Optional[str] = None, headers=None, http2=False) -> Session:
        return Session(SessionConfig(
            retries=retries, delay=delay, encoding=encoding, headers=headers, http2=http2
        ))

    @staticmethod
    def create_engine(dbname, user, pwd, host, port, charset: str = 'utf8mb4') -> Engine:
        return Engine(EngineConfig(
            dbname=dbname, user=user, pwd=pwd, host=host, port=port, charset=charset
        ))

    def init_request(self, retries=0, delay=0, encoding: Optional[str] = None, headers=None, http2=False):
        self.request = self.create_request(retries, delay, encoding, headers, http2)
        self.headers = self.headers or self.request.headers
        return self

    def init_engine(self, dbname, user, pwd, host, port, charset: str = 'utf8mb4'):
        if hasattr(self, 'engine') and isinstance(self.engine, Engine):
            logger.info("禁止重复初始化 `Engine`;")
            return self

        self.engine = self.create_engine(dbname, user, pwd, host, port, charset)
        return self


if __name__ == '__main__':
    ...
