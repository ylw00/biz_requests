# -*- coding: UTF-8 -*-
# @author: ylw
# @file: request
# @time: 2024/12/10
# @desc:
from typing import Callable

from request import Request
from tools.wrapper import Wrapper


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

    def save2db(self, *args, **kwargs):
        """数据入库"""

    def init_attributes(self, *args, **kwargs):
        """初始化属性到self"""
        ...

    def start(self, *args, **kwargs):
        """主入口函数"""
        ...


if __name__ == '__main__':
    ...
