# -*- coding: UTF-8 -*-
from __future__ import annotations

from typing import Any

from .response import BizResponse, ResponseSetAttr


class CustomAdapterHtt1:
    """Compatibility adapter placeholder for legacy imports.

    curl_cffi does not use requests' HTTPAdapter/mount mechanism. The Session
    wrapper now performs response conversion directly after curl_cffi returns.
    """

    def __init__(self, debugger: bool = True):
        self.__debugger = debugger

    def build_response(self, req: Any, resp: Any) -> BizResponse:
        return ResponseSetAttr(self, req, resp)
