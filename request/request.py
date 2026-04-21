# -*- coding: UTF-8 -*-
from __future__ import annotations

from typing import Any, Optional

from loguru import logger

from .headers import Headers
from .session import Session, SessionConfig

try:
    from ..db_engine import Engine, EngineConfig
except ImportError:
    from db_engine import Engine, EngineConfig


class Request:
    def __init__(self) -> None:
        self.request: Optional[Session] = None
        self.engine: Optional[Engine] = None
        self.headers: Optional[Headers] = None

    @staticmethod
    def create_request(
            retries: int = 0,
            delay: int = 0,
            encoding: Optional[str] = None,
            headers: Optional[dict] = None,
            http2: bool = False,
            **kwargs: Any,
    ) -> Session:
        return Session(SessionConfig(
            retries=retries,
            delay=delay,
            encoding=encoding,
            headers=headers or {},
            http2=http2,
            **kwargs,
        ))

    @staticmethod
    def create_engine(dbname: str, user: str, pwd: str, host: str, port: int, charset: str = "utf8mb4") -> Engine:
        return Engine(EngineConfig(
            dbname=dbname, user=user, pwd=pwd, host=host, port=port, charset=charset
        ))

    def init_request(
            self,
            retries: int = 0,
            delay: int = 0,
            encoding: Optional[str] = None,
            headers: Optional[dict] = None,
            http2: bool = False,
            **kwargs: Any,
    ) -> "Request":
        self.request = self.create_request(retries, delay, encoding, headers, http2, **kwargs)
        self.headers = self.headers or self.request.headers
        return self

    def init_engine(self, dbname: str, user: str, pwd: str, host: str, port: int,
                    charset: str = "utf8mb4") -> "Request":
        if hasattr(self, "engine") and isinstance(self.engine, Engine):
            logger.info("禁止重复初始化 `Engine`;")
            return self

        self.engine = self.create_engine(dbname, user, pwd, host, port, charset)
        return self
