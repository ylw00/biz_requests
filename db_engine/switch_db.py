# -*- coding: UTF-8 -*-
# @author: ylw
# @file: switch_bB
# @time: 2024/12/10
# @desc:
# import sys
# import os
from typing import Optional
from sqlalchemy.engine.base import Engine


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))


class SwitchDB:
    def __init__(self, engine: Engine, dbname: str, current_dbname: Optional[str] = None):
        self.__engine: Engine = engine
        self.__dbname: str = dbname
        self.__current_dbname: Optional[str] = current_dbname
        self.__status_name: str = 'switched'  # 默认为不同 【switched or same】

    def __enter__(self):
        self.__current_dbname: str = self.__current_dbname or self.__engine.execute("SELECT DATABASE();").fetchone()[0]
        if self.__current_dbname.lower() == self.__dbname.lower():
            self.__status_name = 'same'
            return self.__engine

        self.__engine.execute(f"USE {self.__dbname};")  # 切换
        return self.__engine  # 返回原本

    def __exit__(self, exc_type, exc_value, traceback):
        if self.__status_name == 'same':
            return
        self.__engine.execute(f"USE {self.__current_dbname};")  # 还原


if __name__ == '__main__':
    pass
