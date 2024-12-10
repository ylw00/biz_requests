# -*- coding: UTF-8 -*-
# @author: ylw
# @file: conn_mysql
# @time: 2024/1/15
# @desc:
# import sys
# import os
import pandas as pd
from typing import Callable, Optional, Union, Any, List

from sqlalchemy.sql import text as sqlalchemy_text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from .engine_base import EngineBase
from .engine_business_tools import EngineBusinessTools


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

class Engine(EngineBase):

    def __init__(self, engine_config: EngineBase.engine_config):
        super(Engine, self).__init__(engine_config)
        self.__business_tools: Optional[EngineBusinessTools] = None  # 懒加载

    @property
    def business_tools(self):
        """懒加载个性化工具类 只有通用方法处理不了的情况下, 再来初始化"""
        if self.__business_tools is None:
            self.__business_tools = EngineBusinessTools(self)
        return self.__business_tools

    @staticmethod
    def tool_insert_dict2sql(data: dict, table: str) -> str:
        keys = list(data.keys())
        col = ','.join(keys)
        placeholder = ', '.join(['%s'] * len(keys))
        return f"""insert into {table} ({col}) values ({placeholder});"""

    @staticmethod
    def tool_replace_dict2sql(data: dict, table: str) -> str:
        keys = list(data.keys())
        col = ','.join(keys)
        placeholder = ', '.join(['%s'] * len(keys))
        return f"""replace into {table} ({col}) values ({placeholder});"""

    @staticmethod
    def __c_execute(sql: str, values: Optional[tuple] = None, *, conn: Connection, safe_ignorePK: bool = False) -> bool:
        """自定义 execute"""
        try:
            conn.execute(sql, values) if values else conn.execute(sqlalchemy_text(sql))
        except IntegrityError as e:
            if safe_ignorePK is True:
                return False
            raise e
        return True

    def execute_onesql(self, sql: str, values: Optional[tuple] = None, conn: Optional[Connection] = None) -> bool:
        """执行一个sql语句"""
        if isinstance(conn, Connection):
            conn.execute(sql, values) if values else conn.execute(sqlalchemy_text(sql))
            return True

        with self.get_connect() as conn:
            conn.execute(sql, values) if values else conn.execute(sqlalchemy_text(sql))
        return True

    def insert_execute(self, item: Union[dict, List[dict]], *, table: str, safe_ignorePK=False, conn: Connection):
        data_list = [item] if isinstance(item, dict) else item
        if not isinstance(data_list, list):
            raise ValueError("Invalid input type, expected dict, list of dicts")

        for idx, data in enumerate(data_list):
            if not isinstance(data, dict):
                raise ValueError(f"Invalid data at index {idx}: Expected a dictionary, but got {type(data).__name__}.")

            sql = self.tool_insert_dict2sql(data, table)
            self.__c_execute(sql, tuple(data.values()), conn=conn, safe_ignorePK=safe_ignorePK)

    def replace_execute(self, item: Union[dict, List[dict], pd.DataFrame], *, table: str, conn: Connection):
        if isinstance(item, dict):
            data_list = [item]
        elif isinstance(item, list):
            data_list = item
        elif isinstance(item, pd.DataFrame):
            data_list = item.to_dict('records')
        else:
            raise ValueError("Invalid input type, expected dict, list of dicts, or DataFrame.")

        for idx, data in enumerate(data_list):
            if not isinstance(data, dict):
                raise ValueError(f"Invalid data at index {idx}: Expected a dictionary, but got {type(data).__name__}.")
            sql = self.tool_replace_dict2sql(data, table=table)
            self.__c_execute(sql, tuple(data.values()), conn=conn)

    def insert_df2table(
            self, df: pd.DataFrame, *, table, schema=None, conn: Optional[Connection] = None) -> Optional[bool]:
        """执行 DataFrame > 【insert】操作"""
        if not isinstance(df, pd.DataFrame) or df.empty:
            return None

        if isinstance(conn, Connection):
            df.to_sql(table, conn, if_exists='append', index=False, schema=schema, chunksize=20000)
            return True

        with self.get_connect() as conn:
            df.to_sql(table, conn, if_exists='append', index=False, schema=schema, chunksize=20000)
        return True

    def insert_data2table(self, item: Union[dict, List[dict]], *, table: str, safe_ignorePK=False):
        """执行【insert】操作"""
        with self.get_connect() as conn:
            self.insert_execute(item, table=table, safe_ignorePK=safe_ignorePK, conn=conn)

    def txn_insert_data2table(self, item: Union[dict, List[dict]], *, table: str, safe_ignorePK=False):
        """事务 执行【insert】操作"""
        return self.with_txn_wrapper(self.insert_execute)(item, table=table, safe_ignorePK=safe_ignorePK)

    def replace_data2table(self, item: Union[dict, List[dict], pd.DataFrame], *, table: str):
        """执行【replace】操作"""
        with self.get_connect() as conn:
            return self.replace_execute(item, table=table, conn=conn)

    def txn_replace_data2table(self, item: Union[dict, List[dict], pd.DataFrame], *, table: str):
        """事务 执行【replace】操作"""
        return self.with_txn_wrapper(self.replace_execute)(item, table=table)

    def txn_callback(self, func: Callable, *args, **kwargs) -> Any:
        """事务 回调 自动添加关键词参数【conn】"""
        return self.with_txn_wrapper(func)(*args, **kwargs)

    def fetch_data(self, sql: str, fetch_number: Optional[int] = None) -> List[dict]:
        _fetch_number = fetch_number if isinstance(fetch_number, int) and fetch_number > 0 else -1
        with self.get_connect() as conn:
            result = conn.execute(sqlalchemy_text(sql))
            data_row = result.fetchmany(_fetch_number) if _fetch_number > 0 else result.fetchall()
            return [dict(row) for row in data_row]

    def fetch_data2df(self, sql) -> pd.DataFrame:
        with self.get_connect() as conn:
            return pd.read_sql(sql, conn)


if __name__ == '__main__':
    def demo_func():
        engine = Engine('spider')
        # data = [{'id': 112, 'name': 222}]
        # engine.insert_data2table(data, table='demo_rollback')
        #
        # with engine.with_switch_db('ulike_tmall'):
        #     engine.insert_data2table(data, table='demo_rollback')
        #
        # engine.insert_data2table({'id': 1123, 'name': 2223}, table='demo_rollback')
        sql = 'update demo_rollback set id="1211" where id="1213";'
        df = pd.DataFrame([{'id': 456, 'name': 222}])
        # engine.execute_onesql(sql)

        engine.business_tools.txn_execute_sql_then_insert(sql, df, table='demo_rollback')


    demo_func()
