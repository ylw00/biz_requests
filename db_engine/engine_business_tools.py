# -*- coding: UTF-8 -*-
# @author: ylw
# @file: engine_business_tools
# @time: 2024/12/10
# @desc:
# import sys
# import os
import pandas as pd
from typing import Union, Dict, List
from sqlalchemy.exc import IntegrityError


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

class EngineBusinessTools:  # 面向业务层的工具封装
    def __init__(self, engine):
        self._engine = engine

    def txn_insert_multiple_tables(self, table_item: Dict[str, Union[dict, List[dict]]], safe_ignorePK=False) -> bool:
        """
        插入多个数据格式到多张表
        :param table_item: { 表名【str】: 数据【Union[dict, List[dict]]】 }
        :param safe_ignorePK: { 表名【str】: 数据【Union[dict, List[dict]]】 }
        """

        def _insert(conn):
            for table, item in table_item.items():
                data_list = [item] if isinstance(item, dict) else item
                for data in data_list:
                    sql = self._engine.tool_insert_dict2sql(data, table=table)
                    try:
                        conn.execute(sql, tuple(data.values()))
                    except IntegrityError as e:
                        if safe_ignorePK is False:
                            raise e
            return True

        return self._engine.with_txn_wrapper(_insert)()

    def txn_execute_sql_then_insert(
            self, sql: str, item: Union[dict, List[dict], pd.DataFrame], *, table: str, safe_ignorePK: bool = False):
        """事务 执行一个sql, 然后再插入数据;"""

        def _insert(conn):
            conn.execute(sql)
            if isinstance(item, pd.DataFrame):
                item.to_sql(table, conn, if_exists='append', index=False, chunksize=20000)
            else:
                self._engine.insert_execute(item, table=table, safe_ignorePK=safe_ignorePK, conn=conn)

        return self._engine.with_txn_wrapper(_insert)()


if __name__ == '__main__':
    pass
