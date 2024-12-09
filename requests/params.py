# -*- coding: UTF-8 -*-
# @author: ylw
# @file: requests_params
# @time: 2024/12/9
# @desc:
# import sys
# import os
from enum import Enum
from typing import Union, Optional, Dict, Any
from headers import Headers


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

class Method(Enum):
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    post = POST
    get = GET
    put = PUT
    delete = DELETE
    patch = PATCH


class Params:
    def __init__(self):
        self._method: Optional[Method] = None
        self._url: Optional[str] = None
        self._params: Optional[Dict[str, Any]] = None
        self._data: Optional[Dict[str, Any]] = None
        self._json: Optional[Dict[str, Any]] = None
        self._headers: Headers = Headers()
        self._cookies: Optional[Dict[str, str]] = None
        self._timeout: Optional[int] = None

        self.__current_call_func = None

    def get_method(self) -> 'Method':
        return self._method

    def set_method(self, method: Method):
        self._method = method
        return self

    def get_url(self) -> str:
        return self._url

    def set_url(self, url: str):
        self._url = url
        return self

    def get_headers(self) -> 'Headers':
        return self._headers

    def set_headers(self, headers: Dict[str, str]):
        self._headers.update(headers)
        return self

    def get_params(self) -> Dict[str, str]:
        return self._params

    def set_params(self, params: Dict[str, str]):
        self._params.update(params)
        return self

    def get_data(self) -> Dict[str, str]:
        return self._data

    def set_data(self, data: Dict[str, str]):
        self._data = data
        return self

    def get_json(self) -> Dict[str, Union[str, dict]]:
        return self._json

    def set_json(self, json: Dict[str, Union[str, dict]]):
        self._json = json
        return self

    def get_cookies(self) -> Dict[str, str]:
        return self._cookies

    def set_cookies(self, cookies: Dict[str, str]):
        self._cookies = cookies
        return self

    def get_timeout(self) -> int:
        return self._timeout

    def set_timeout(self, timeout: int):
        self._timeout = timeout
        return self

    def _request_kwargs(self):
        kwargs = {
            'headers': self._headers,
            'params': self._params,
            'data': self._data,
            'json': self._json,
            'timeout': self._timeout,
            'cookies': self._cookies
        }
        return {key: value for key, value in kwargs.items() if value is not None}



if __name__ == '__main__':
    print(Params().set_url().set_timeout())