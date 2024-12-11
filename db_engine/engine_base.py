# -*- coding: UTF-8 -*-
# @author: ylw
# @file: engine_base
# @time: 2024/12/10
# @desc:
# import sys
# import os
from urllib import parse
from functools import wraps
from dataclasses import dataclass, field
from typing import TypeVar, Callable, Any, cast, ContextManager, Optional

from sqlalchemy import create_engine
from sqlalchemy import __version__ as sqlalchemy_version
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from .switch_db import SwitchDB

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

F = TypeVar('F', bound=Callable[..., Optional[Any]])


@dataclass
class EngineConfig:
    user: str
    password: str
    host: str
    port: int
    dbname: str
    charset: str = field(default='utf8mb4')


class EngineBase:
    _CONN_MODE = "mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset={charset}"
    engine: Optional[Engine] = None
    engine_config = EngineConfig

    def __new__(cls, *args, **kwargs):
        if cls is EngineBase:
            raise TypeError("Cannot instantiate MysqlEngineBase directly. It must be subclassed.")
        return super().__new__(cls)

    def __init__(self, engine_config: EngineConfig):
        self.engine: Engine = self.create_engine(engine_config)
        self.__dbname = engine_config.dbname

    def __del__(self):
        self.close_engine()

    def create_engine(self, engine_config: EngineConfig) -> Engine:
        _mysql_config = engine_config
        return create_engine(self._CONN_MODE.format(
            user=engine_config.user,
            pwd=parse.quote(engine_config.password),
            host=engine_config.host,
            port=engine_config.port,
            db=engine_config.dbname,
            charset=engine_config.charset
        ), pool_recycle=3600, pool_pre_ping=True)

    def close_engine(self):
        try:
            self.engine.dispose()
        except:
            pass

    def get_connect(self, close_with_result=False) -> Connection:
        """
        获取数据库连接，并根据不同版本和配置来处理事务。
        :param close_with_result: 是否在操作后关闭连接（默认为 False）。
        :return: 数据库连接对象，可能会自动管理事务。
        """
        if sqlalchemy_version.startswith('2.'):
            return self.engine.begin(close_with_result=close_with_result)
        return self.engine.connect(close_with_result=close_with_result)

    def with_switch_db(self, dbname: str) -> ContextManager:
        return SwitchDB(self.engine, dbname, current_dbname=self.__dbname)

    def with_txn_wrapper(self, func):
        """事务装饰器, 自动处理事务的开始, 提交和回滚"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取数据库连接
            with self.get_connect() as conn:
                with conn.begin():
                    return func(*args, **kwargs, conn=conn)

        return cast(F, wrapper)


if __name__ == '__main__':
    pass
