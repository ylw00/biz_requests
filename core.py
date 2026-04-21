# -*- coding: UTF-8 -*-
from __future__ import annotations

from typing import Any, Callable

try:
    from .request import Request
    from .tools.wrapper import Wrapper
except ImportError:
    from request import Request
    from tools.wrapper import Wrapper


class BizRequest(Request):
    """Base class for business request clients."""

    def __init__(self) -> None:
        if type(self) is BizRequest:
            raise TypeError("BizRequest cannot be instantiated directly.")
        super().__init__()

    @staticmethod
    def safe_retry_until_done(
            callback_func: Callable[..., Any],
            *args: Any,
            retries: int = 3,
            delay: int = 3,
            **kwargs: Any,
    ) -> Any:
        return Wrapper.retry_until_done(retries=retries, delay=delay)(callback_func)(*args, **kwargs)

    @staticmethod
    def safe_parse(callback_func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        return Wrapper.log_resp_if_exception(callback_func)(*args, **kwargs)

    def save2db(self, *args: Any, **kwargs: Any) -> None:
        """Persist data to database in subclasses."""

    def init_attributes(self, *args: Any, **kwargs: Any) -> None:
        """Initialize subclass attributes."""

    def start(self, *args: Any, **kwargs: Any) -> None:
        """Main entry point for subclasses."""
