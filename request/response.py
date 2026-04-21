# -*- coding: UTF-8 -*-
from __future__ import annotations

from json import loads as json_loads
from typing import Any, Dict, Union, cast

import pandas as pd
from curl_cffi.requests import Response as CurlResponse

from .headers import Headers

try:
    from ..tools.cookies import CookieTools
    from ..tools.dataframe import Content2DfParamsConfig, content2df, non2none
    from ..tools.wrapper import Wrapper
except ImportError:
    from tools.cookies import CookieTools
    from tools.dataframe import Content2DfParamsConfig, content2df, non2none
    from tools.wrapper import Wrapper


def _decode_bytes(value: Any) -> Any:
    return value.decode() if isinstance(value, bytes) else value


def _headers_to_dict(headers: Any) -> Dict[str, str]:
    if headers is None:
        return {}
    if hasattr(headers, "items"):
        return {str(_decode_bytes(k)): str(_decode_bytes(v)) for k, v in headers.items()}
    return {str(_decode_bytes(k)): str(_decode_bytes(v)) for k, v in dict(headers).items()}


class BizResponse(CurlResponse):
    """curl_cffi response with biz_requests-compatible helper methods."""

    headers: Headers

    @classmethod
    def from_response(cls, response: CurlResponse) -> "BizResponse":
        if isinstance(response, cls):
            response.headers = Headers(_headers_to_dict(response.headers))
            return response

        biz_response = cls()
        biz_response.__dict__.update(response.__dict__)
        biz_response.headers = Headers(_headers_to_dict(response.headers))
        return biz_response

    def head_scookie(self, as_dict: bool = True) -> Union[str, Dict[str, str], None]:
        cookie = self.headers.get("set-cookie")
        if as_dict:
            return CookieTools.cookie_str2dict(cookie) if isinstance(cookie, str) else {}
        return cookie

    def set_encoding(self, encodeing: str) -> "BizResponse":
        if hasattr(self, "_text"):
            delattr(self, "_text")
        self._encoding = encodeing
        return self

    @property
    def text(self) -> str:
        if not hasattr(self, "_text"):
            content = getattr(self, "content", b"")
            self._text = "" if not content else self._decode(content)
        return cast(str, self._text)

    @Wrapper.log_text_if_exception
    def json(self, *args: Any, **kwargs: Any) -> Any:
        return super(BizResponse, self).json(**kwargs)

    @Wrapper.log_text_if_exception
    def jsonp(self) -> Any:
        text = self.text
        return json_loads(text[text.find("{"):text.rfind("}") + 1])

    @Wrapper.log_text_if_exception
    def dataframe(self, c_type: str, **kwargs: Any) -> pd.DataFrame:
        non_to_none = bool(kwargs.pop("non2none", False))
        df = content2df(
            c_type,
            self.text if "base64" in c_type else self.content,
            Content2DfParamsConfig(
                encoding=kwargs.get("encoding", "utf-8"),
                thousands=kwargs.get("thousands", None),
                dtype=kwargs.get("dtype", None),
                sheet_name=kwargs.get("sheet_name", 0),
                header=kwargs.get("header", 0),
                file_name=kwargs.get("file_name", None),
                engine=kwargs.get("engine", "openpyxl"),
            ),
        )
        return non2none(df) if non_to_none else df


def ResponseSetAttr(_self: Any, _req: Any, resp: CurlResponse) -> BizResponse:
    """Compatibility shim kept for code importing the old adapter helper."""
    return BizResponse.from_response(resp)
