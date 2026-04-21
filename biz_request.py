# -*- coding: UTF-8 -*-
from __future__ import annotations

from typing import Any, Callable

try:
    from .request import Request
    from .request.headers import Headers
    from .request.session import Session
    from .db_engine.engine import Engine
    from .tools.cookies import CookieTools
    from .tools.wrapper import Wrapper
except ImportError:
    from request import Request
    from request.headers import Headers
    from request.session import Session
    from db_engine.engine import Engine
    from tools.cookies import CookieTools
    from tools.wrapper import Wrapper

__all__ = ["BizRequest", "Session", "Headers", "Engine", "Wrapper", "CookieTools"]


class BizRequest(Request):
    """
    在这里拓展业务代码/封装
    """

    def __init__(self) -> None:
        if type(self) is BizRequest:
            raise TypeError("BizRequest cannot be instantiated directly.")
        super(BizRequest, self).__init__()

    @staticmethod
    def safe_retry_until_done(callback_func: Callable[..., Any], *args: Any, retries: int = 3,
                              delay: int = 3, **kwargs: Any) -> Any:
        """
        轮询直至返回正确得返回值
        业务示例:
            1, 循环等待报表导出完成
            ...
        """
        return Wrapper.retry_until_done(retries=retries, delay=delay)(callback_func)(*args, **kwargs)

    @staticmethod
    def safe_parse(callback_func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """安全的解析"""
        return Wrapper.log_resp_if_exception(callback_func)(*args, **kwargs)

    def save2db(self, *args: Any, **kwargs: Any) -> None:
        """数据入库"""

    def init_attributes(self, *args: Any, **kwargs: Any) -> None:
        """初始化属性到self"""
        ...

    def start(self, *args: Any, **kwargs: Any) -> None:
        """主入口函数"""
        ...


if __name__ == '__main__':
    ...
